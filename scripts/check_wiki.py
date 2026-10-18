"""Structural check of the wiki: source pages, raw files, lens pages, unresolved links."""

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIELDS = ["type", "url", "published", "ingested", "tags", "concepts", "benchmarks", "lenses"]
RELATIONS = ["基于", "对照", "相悖"]
# raw/ is local-only (third-party full texts); fresh clones do not have it.
HAS_RAW = (ROOT / "raw").is_dir()


def benchmarks(page: Path) -> list[str]:
    m = re.search(r"^benchmarks:\s*\[(.*)\]", page.read_text(encoding="utf-8"), flags=re.M)
    return re.findall(r"\[\[([^\]]+)\]\]", m.group(1)) if m else []


def unresolved_links(allowed: set[str]) -> list[str]:
    # Resolved like Obsidian: by file name or by vault-relative path, ignoring #heading and |alias.
    # Benchmarks have no pages on purpose; they are shared nodes in the graph view.
    files = [p.relative_to(ROOT).with_suffix("").as_posix() for p in ROOT.rglob("*.md")]
    targets = set(files) | {f.rsplit("/", 1)[-1] for f in files} | allowed
    broken = []
    for page in sorted((ROOT / "wiki").rglob("*.md")):
        for link in re.findall(r"\[\[([^\]|#]+)", page.read_text(encoding="utf-8")):
            if link.strip() not in targets and (HAS_RAW or not link.startswith("raw/")):
                broken.append(f"{link} (in {page.relative_to(ROOT).as_posix()})")
    return broken


def split(text: str, prefix: str) -> dict[str, str]:
    parts = re.split(rf"^{prefix} ", text, flags=re.M)[1:]
    return {p.split("\n", 1)[0].strip(): p.split("\n", 1)[-1] for p in parts}


def lens_problems(page: Path, pages: list[Path]) -> list[str]:
    text = page.read_text(encoding="utf-8")
    if re.search(r"^status: proposed", text, flags=re.M):
        return []
    name, out = page.name, []
    sections = split(text, "##")
    missing = [s for s in ["范围", "总结", "工作", "冲突"] if s not in sections]
    if missing:
        return [f"{name}: missing section {', '.join(missing)}"]
    listed = re.findall(r"^- \[\[([^\]|]+)\]\]：", sections["工作"], flags=re.M)
    out += [f"{name}: duplicate row {s}" for s, n in Counter(listed).items() if n > 1]
    owned = {p.stem for p in pages if f'"[[{page.stem}]]"' in p.read_text(encoding="utf-8").split("---")[1]}
    out += [f"{name}: {s} has lens but no row" for s in sorted(owned - set(listed))]
    out += [f"{name}: row {s} is not a source with this lens" for s in sorted(set(listed) - owned)]
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", type=int, required=True, help="expected number of source pages")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    problems = []

    pages = sorted((ROOT / "wiki/sources").glob("*.md"))
    if len(pages) != args.sources:
        problems.append(f"{len(pages)} source pages, expected {args.sources}")
    for page in pages:
        text = page.read_text(encoding="utf-8")
        front = text.split("---")[1] if text.startswith("---") else ""
        missing = [f for f in FIELDS if not re.search(rf"^{f}:", front, flags=re.M)]
        if missing:
            problems.append(f"{page.name}: missing {', '.join(missing)}")
        if f"[[raw/{page.stem}]]" not in text or (HAS_RAW and not (ROOT / "raw" / page.name).exists()):
            problems.append(f"{page.name}: no raw/{page.name} or no link to it")
        related = split(text, "##").get("关联", "")
        for line in related.strip().splitlines():
            m = re.match(rf"- ({'|'.join(RELATIONS)}) \[\[([^\]|]+)\]\]：", line)
            if not m:
                problems.append(f"{page.name}: 关联 line not '- <{'/'.join(RELATIONS)}> [[slug]]：…': {line[:40]}")
            elif m.group(2) == page.stem or not (ROOT / "wiki/sources" / f"{m.group(2)}.md").exists():
                problems.append(f"{page.name}: 关联 links non-source {m.group(2)}")

    for lens in sorted((ROOT / "wiki/lenses").glob("*.md")):
        problems += lens_problems(lens, pages)

    broken = unresolved_links({b for p in pages for b in benchmarks(p)})
    if broken:
        problems.append("unresolved links: " + "; ".join(broken))

    tags = Counter()
    for page in pages:
        m = re.search(r"^concepts:\s*\[(.*)\]", page.read_text(encoding="utf-8"), flags=re.M)
        if m:
            tags.update(t.strip() for t in m.group(1).split(",") if t.strip())
    shared = [(t, n) for t, n in tags.most_common() if n > 1]
    print(f"{len(pages)} sources, {len(tags)} concept tags, {len(shared)} shared by 2+ sources")
    for t, n in shared:
        print(f"  {t}: {n}")
    for p in problems:
        print("FAIL", p)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
