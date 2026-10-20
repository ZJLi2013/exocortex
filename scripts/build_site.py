"""Prepare a Quartz content directory from wiki/: copy lens and source pages, add node pages and a home page."""

import argparse
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NODE_FIELDS = {"benchmarks": "评测集", "methods": "方法", "models_used": "用到的模型", "models_compared": "直接对照的模型"}
NODE_TYPES = {"benchmarks": "benchmark", "methods": "method", "models_used": "model", "models_compared": "model"}
NODE_TEXT = {"benchmark": "评测集节点。报了它的数字的来源见下方反向链接。",
             "method": "方法节点。用这个方法的来源见下方反向链接。",
             "model": "模型节点。用到或对照它的来源见下方反向链接。"}


def field(front: str, name: str) -> str | None:
    m = re.search(rf"^{name}:\s*(.*)$", front, flags=re.M)
    return m.group(1).strip() if m else None


def links(front: str, name: str) -> list[str]:
    return re.findall(r"\[\[([^\]|]+)\]\]", field(front, name) or "")


def section(text: str, title: str) -> str:
    m = re.search(rf"^## {title}\n(.*?)(?=^## |\Z)", text, flags=re.M | re.S)
    return m.group(1).strip() if m else ""


def titled(text: str) -> str:
    # Quartz renders frontmatter title as the page heading; move the page's H1 there.
    m = re.search(r"^# (.+)\n+", text, flags=re.M)
    if not m:
        return text
    text = text[:m.start()] + text[m.end():]
    return text.replace("---\n", f'---\ntitle: "{m.group(1).strip()}"\n', 1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out", type=Path, help="Quartz content directory; replaced entirely")
    args = parser.parse_args()
    shutil.rmtree(args.out, ignore_errors=True)
    for sub in ["lenses", "sources", "nodes"]:
        (args.out / sub).mkdir(parents=True)

    sources = sorted((ROOT / "wiki/sources").glob("*.md"))
    lenses = sorted((ROOT / "wiki/lenses").glob("*.md"))
    stems = {p.stem.lower(): p.stem for p in sources + lenses}

    # Obsidian resolves [[RoboDojo]] to robodojo.md case-insensitively; Quartz slugs keep case.
    def fix_case(text: str) -> str:
        def repl(m: re.Match) -> str:
            target, rest = m.group(1), m.group(2) or ""
            slug = stems.get(target.lower())
            if slug and slug != target:
                return f"[[{slug}{rest or '|' + target}]]"
            return m.group(0)
        return re.sub(r"\[\[([^\]|#]+)((?:[#|][^\]]*)?)\]\]", repl, text)

    nodes: dict[str, str] = {}
    for page in sources:
        text = page.read_text(encoding="utf-8")
        front = text.split("---")[1]
        text = text.replace(f"[[raw/{page.stem}]]", f"[{field(front, 'url')}]({field(front, 'url')})")
        lines = []
        for name, label in NODE_FIELDS.items():
            values = links(front, name)
            if values:
                lines.append(f"- {label}：" + "、".join(f"[[{v}]]" for v in values))
            for v in values:
                if v.lower() not in stems:
                    nodes.setdefault(v, NODE_TYPES[name])
        if lines:
            text = text.rstrip("\n") + "\n\n## 节点\n\n" + "\n".join(lines) + "\n"
        (args.out / "sources" / page.name).write_text(fix_case(titled(text)), encoding="utf-8")

    for name, kind in sorted(nodes.items()):
        (args.out / "nodes" / f"{name}.md").write_text(
            f'---\ntitle: "{name}"\ntype: {kind}\n---\n{NODE_TEXT[kind]}\n', encoding="utf-8")

    home = ["---", "title: exocortex", "---", "研究领域的个人知识库，每个 lens 是一个研究方向。", ""]
    for page in lenses:
        text = page.read_text(encoding="utf-8")
        (args.out / "lenses" / page.name).write_text(fix_case(titled(text)), encoding="utf-8")
        if re.search(r"^status: proposed", text, flags=re.M):
            continue
        home += [f"## [[{page.stem}]]", "", section(text, "范围"), "", section(text, "总结"), ""]
    (args.out / "index.md").write_text(fix_case("\n".join(home)), encoding="utf-8")
    print(f"{len(sources)} sources, {len(lenses)} lenses, {len(nodes)} node pages -> {args.out}")


if __name__ == "__main__":
    main()
