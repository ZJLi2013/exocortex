"""Write the site from wiki/: index.html lists works per approved lens, each with a graph of its sources' relations; insights.html holds the insight pages."""

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
<title>__TITLE__</title>
<script src="https://unpkg.com/vis-network@9.1.9/standalone/umd/vis-network.min.js"></script>
<style>
body { font-family: system-ui, sans-serif; max-width: 960px; margin: 2rem auto; padding: 0 1rem; line-height: 1.6; color: #222; }
nav a { margin-right: 1rem; }
.graph { height: 320px; border: 1px solid #ddd; border-radius: 6px; margin: .5rem 0; }
.legend span { margin-right: 1rem; }
h2 { margin-top: 2.5rem; border-bottom: 1px solid #eee; }
.scope { font-weight: 600; }
li { margin: .3rem 0; }
.insight { background: #f7fafc; border-left: 3px solid #2c5282; padding: .2rem 1rem; margin: 1rem 0; }
.insight table { border-collapse: collapse; } .insight td, .insight th { border: 1px solid #ddd; padding: .2rem .5rem; }
footer { margin: 3rem 0 1rem; color: #888; font-size: .9em; }
</style>
</head>
<body>
<h1>exocortex</h1>
<nav><a href="index.html">方向与工作</a><a href="insights.html">Insights</a></nav>
__BODY__
<footer>由 <a href="https://github.com/ZJLi2013/exocortex">ZJLi2013/exocortex</a> 的 wiki/ 生成；更新于 __DATE__。</footer>
<script>
const graphs = __DATA__;
for (const [id, data] of Object.entries(graphs)) {
  const network = new vis.Network(document.getElementById("g-" + id),
    { nodes: new vis.DataSet(data.nodes), edges: new vis.DataSet(data.edges) },
    { nodes: { shape: "dot", size: 10, color: "#90cdf4", font: { size: 15 } },
      physics: { solver: "forceAtlas2Based", stabilization: { iterations: 200 } },
      interaction: { hover: true } });
  network.on("click", (e) => {
    const node = data.nodes.find((n) => n.id === e.nodes[0]);
    if (node) window.open(node.url, "_blank");
  });
}
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


def inline(text: str, sources: dict) -> str:
    def link(m):
        s = sources.get(m.group(1))
        return f'<a href="{html.escape(s["url"])}">{html.escape(s["name"])}</a>' if s else html.escape(m.group(2) or m.group(1))
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html.escape(text, quote=False))
    return re.sub(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", link, out)


def insight_html(text: str, sources: dict) -> str:
    """The small markdown subset agents/insight.md uses: ## / ### headings, bullets, one table, paragraphs."""
    body = text.split("---", 2)[2].split("\n", 2)[2] if text.startswith("---") else text
    out, rows = [], []
    for line in body.splitlines() + [""]:
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if not all(set(c) <= set("-: ") for c in cells):
                rows.append(cells)
            continue
        if rows:
            tag = lambda r, t: "<tr>" + "".join(f"<{t}>{inline(c, sources)}</{t}>" for c in r) + "</tr>"
            out.append("<table>" + tag(rows[0], "th") + "".join(tag(r, "td") for r in rows[1:]) + "</table>")
            rows = []
        if line.startswith("### "):
            out.append(f"<h4>{inline(line[4:], sources)}</h4>")
        elif line.startswith("## "):
            out.append(f"<h3>{inline(line[3:], sources)}</h3>")
        elif line.startswith("- "):
            out.append(f"<li>{inline(line[2:], sources)}</li>")
        elif line.strip():
            out.append(f"<p>{inline(line, sources)}</p>")
    return '<div class="insight">\n' + re.sub(r"((?:<li>.*?</li>\n?)+)", r"<ul>\1</ul>", "\n".join(out)) + "\n</div>"


def relation_graph(slugs: list, sources: dict) -> dict:
    """Sources of one lens and the relations among them; empty when none of them relate."""
    edges = []
    for slug in slugs:
        for rel, target in re.findall(rf"^- ({'|'.join(RELATIONS)}) \[\[([^\]|]+)\]\]", section(sources[slug]["text"], "关联"), flags=re.M):
            if target in slugs:
                edges.append({"from": slug, "to": target, "color": RELATIONS[rel], "title": rel, "arrows": "to", "width": 2})
    if not edges:
        return {}
    nodes = [{"id": s, "label": sources[s]["name"], "url": sources[s]["url"]} for s in slugs]
    return {"nodes": nodes, "edges": edges}


def render(title: str, body: str, date: str, graphs: dict) -> str:
    data = json.dumps(graphs, ensure_ascii=False).replace("</", "<\\/")
    return (PAGE.replace("__TITLE__", title).replace("__BODY__", body)
            .replace("__DATE__", date).replace("__DATA__", data))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out", type=Path, help="output directory for index.html and insights.html")
    args = parser.parse_args()

    sources = {}
    for page in sorted((ROOT / "wiki/sources").glob("*.md")):
        text = page.read_text(encoding="utf-8")
        name = re.search(r"^# (.+)", text, flags=re.M).group(1).strip()
        sources[page.stem] = {"name": name, "url": front(text, "url"), "text": text}

    sections, insights, graphs = [], [], {}
    for page in sorted((ROOT / "wiki/lenses").glob("*.md")):
        text = page.read_text(encoding="utf-8")
        if re.search(r"^status: proposed", text, flags=re.M):
            continue
        lens, rows, slugs = page.stem, [], []
        for slug, highlight in re.findall(r"^- \[\[([^\]|]+)\]\]：(.*)$", section(text, "工作"), flags=re.M):
            s = sources[slug]
            slugs.append(slug)
            rows.append(f'<li><a href="{html.escape(s["url"])}">{html.escape(s["name"])}</a>：{plain(highlight)}</li>')
        graph = relation_graph(slugs, sources)
        if graph:
            graphs[lens] = graph
        insight = ROOT / "wiki/insights" / page.name
        link = ""
        if insight.exists():
            insights.append(f'<h2 id="{lens}">{lens}</h2>\n<p class="scope">{plain(section(text, "范围"))}</p>\n'
                            + insight_html(insight.read_text(encoding="utf-8"), sources))
            link = f'<p><a href="insights.html#{lens}">这个方向的 insight：方向与未解决问题 →</a></p>\n'
        sections.append(f'<h2 id="{lens}">{lens}</h2>\n<p class="scope">{plain(section(text, "范围"))}</p>\n{link}'
                        f'<p>{plain(section(text, "总结"))}</p>\n'
                        + (f'<div class="graph" id="g-{lens}"></div>\n' if graph else "")
                        + "<ul>\n" + "\n".join(rows) + "\n</ul>")

    legend = '<p class="legend">图中边：' + "".join(f'<span style="color:{c}">━ {r}</span>' for r, c in RELATIONS.items()) + "点工作打开原文。</p>"
    date = max(front(s["text"], "ingested") for s in sources.values())
    index = '<p>研究领域的个人知识库，每个 lens 是一个研究方向。</p>\n' + legend + "\n" + "\n".join(sections)
    insights_body = ('<p>以下是 insight agent 对各方向的判断：下一个值得做的方向与未解决的问题。它们是判断，不是证据；'
                     '证据见<a href="index.html">方向与工作</a>里对应的 lens。</p>\n' + "\n".join(insights))
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "index.html").write_text(render("exocortex", index, date, graphs), encoding="utf-8")
    (args.out / "insights.html").write_text(render("exocortex · insights", insights_body, date, {}), encoding="utf-8")
    edges = sum(len(g["edges"]) for g in graphs.values())
    print(f"{len(sections)} lenses, {len(graphs)} graphs, {edges} relation edges, {len(insights)} insights -> {args.out}")


if __name__ == "__main__":
    main()
