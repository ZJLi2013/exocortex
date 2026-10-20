"""Write a single-page site from wiki/: works per approved lens and a graph of lenses, sources and their relations."""

import argparse
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RELATIONS = {"基于": "#2b6cb0", "对照": "#718096", "相悖": "#c53030"}

PAGE = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>exocortex</title>
<script src="https://unpkg.com/vis-network@9.1.9/standalone/umd/vis-network.min.js"></script>
<style>
body { font-family: system-ui, sans-serif; max-width: 960px; margin: 2rem auto; padding: 0 1rem; line-height: 1.6; color: #222; }
#graph { height: 560px; border: 1px solid #ddd; border-radius: 6px; }
.legend span { margin-right: 1rem; }
h2 { margin-top: 2.5rem; border-bottom: 1px solid #eee; }
.scope { font-weight: 600; }
li { margin: .3rem 0; }
footer { margin: 3rem 0 1rem; color: #888; font-size: .9em; }
</style>
</head>
<body>
<h1>exocortex</h1>
<p>研究领域的个人知识库，每个 lens 是一个研究方向。点图上的工作打开原文，点 lens 跳到它那一节。</p>
<div id="graph"></div>
<p class="legend">__LEGEND__</p>
__SECTIONS__
<footer>由 <a href="https://github.com/ZJLi2013/exocortex">ZJLi2013/exocortex</a> 的 wiki/ 生成；更新于 __DATE__。</footer>
<script>
const data = __DATA__;
const network = new vis.Network(document.getElementById("graph"),
  { nodes: new vis.DataSet(data.nodes), edges: new vis.DataSet(data.edges) },
  { groups: { lens: { shape: "box", color: "#2c5282", font: { color: "#fff", size: 16 } },
              source: { shape: "dot", size: 10, color: "#90cdf4" } },
    physics: { solver: "forceAtlas2Based", stabilization: { iterations: 200 } },
    interaction: { hover: true } });
network.on("click", (e) => {
  const node = data.nodes.find((n) => n.id === e.nodes[0]);
  if (!node) return;
  if (node.group === "lens") location.hash = node.id;
  else window.open(node.url, "_blank");
});
</script>
</body>
</html>
"""


def front(text: str, name: str) -> str:
    m = re.search(rf"^{name}:\s*(.*)$", text.split("---")[1], flags=re.M)
    return m.group(1).strip() if m else ""


def section(text: str, title: str) -> str:
    m = re.search(rf"^## {title}\n(.*?)(?=^## |\Z)", text, flags=re.M | re.S)
    return m.group(1).strip() if m else ""


def plain(text: str) -> str:
    return re.sub(r"\[\[(?:[^\]|]+\|)?([^\]]+)\]\]", r"\1", html.escape(text, quote=False))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out", type=Path, help="output directory for index.html")
    args = parser.parse_args()

    sources = {}
    for page in sorted((ROOT / "wiki/sources").glob("*.md")):
        text = page.read_text(encoding="utf-8")
        name = re.search(r"^# (.+)", text, flags=re.M).group(1).strip()
        sources[page.stem] = {"name": name, "url": front(text, "url"), "text": text}

    nodes, edges, sections, kept = [], [], [], set()
    for page in sorted((ROOT / "wiki/lenses").glob("*.md")):
        text = page.read_text(encoding="utf-8")
        if re.search(r"^status: proposed", text, flags=re.M):
            continue
        nodes.append({"id": page.stem, "label": page.stem, "group": "lens"})
        rows = []
        for slug, highlight in re.findall(r"^- \[\[([^\]|]+)\]\]：(.*)$", section(text, "工作"), flags=re.M):
            s = sources[slug]
            kept.add(slug)
            edges.append({"from": page.stem, "to": slug, "color": "#cbd5e0"})
            rows.append(f'<li><a href="{html.escape(s["url"])}">{html.escape(s["name"])}</a>：{plain(highlight)}</li>')
        sections.append(f'<h2 id="{page.stem}">{page.stem}</h2>\n<p class="scope">{plain(section(text, "范围"))}</p>\n'
                        f'<p>{plain(section(text, "总结"))}</p>\n<ul>\n' + "\n".join(rows) + "\n</ul>")

    for slug in sorted(kept):
        s = sources[slug]
        nodes.append({"id": slug, "label": s["name"], "group": "source", "url": s["url"]})
        for rel, target in re.findall(rf"^- ({'|'.join(RELATIONS)}) \[\[([^\]|]+)\]\]", section(s["text"], "关联"), flags=re.M):
            if target in kept:
                edges.append({"from": slug, "to": target, "color": RELATIONS[rel], "title": rel, "arrows": "to", "width": 2})

    legend = "".join(f'<span style="color:{c}">━ {r}</span>' for r, c in RELATIONS.items()) + '<span style="color:#a0aec0">━ lens 收录</span>'
    data = json.dumps({"nodes": nodes, "edges": edges}, ensure_ascii=False).replace("</", "<\\/")
    dates = [front(s["text"], "ingested") for s in sources.values()]
    page = (PAGE.replace("__LEGEND__", legend).replace("__SECTIONS__", "\n".join(sections))
            .replace("__DATE__", max(dates)).replace("__DATA__", data))
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "index.html").write_text(page, encoding="utf-8")
    print(f"{len(nodes)} nodes, {len(edges)} edges, {len(kept)} sources -> {args.out / 'index.html'}")


if __name__ == "__main__":
    main()
