"""Structural check of the wiki: source pages, lens pages, unresolved links."""

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

from search_candidates import known_keys, url_key

ROOT = Path(__file__).resolve().parent.parent
NODE_FIELDS = ["benchmarks", "methods", "models_used", "models_compared"]
FIELDS = ["type", "url", "published", "ingested", "tags", "concepts", *NODE_FIELDS, "lenses"]
RELATIONS = ["基于", "对照", "相悖"]


def links(page: Path, field: str) -> list[str]:
    m = re.search(rf"^{field}:\s*\[(.*)\]", page.read_text(encoding="utf-8"), flags=re.M)
    return re.findall(r"\[\[([^\]]+)\]\]", m.group(1)) if m else []


def model_names() -> set[str]:
    text = (ROOT / "docs/model-names.md").read_text(encoding="utf-8")
    return {re.sub(r"^\[\[|\]\]$", "", m) for m in re.findall(r"^\| ([^|]+?) \|", text, flags=re.M)}


def unresolved_links(allowed: set[str]) -> list[str]:
    # Resolved like Obsidian: by file name or by vault-relative path, ignoring #heading and |alias.
    # Benchmark, method and model nodes have no pages on purpose; they are shared nodes in the graph view.
    files = [p.relative_to(ROOT).with_suffix("").as_posix() for p in ROOT.rglob("*.md")]
    targets = set(files) | {f.rsplit("/", 1)[-1] for f in files} | allowed
    broken = []
    for page in sorted((ROOT / "wiki").rglob("*.md")):
        for link in re.findall(r"\[\[([^\]|#]+)", page.read_text(encoding="utf-8")):
            if link.strip() not in targets:
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
    missing = [s for s in ["范围", "总结", "工作"] if s not in sections]
    if missing:
        return [f"{name}: missing section {', '.join(missing)}"]
    listed = re.findall(r"^- \[\[([^\]|]+)\]\]：", sections["工作"], flags=re.M)
    out += [f"{name}: duplicate row {s}" for s, n in Counter(listed).items() if n > 1]
    owned = {p.stem for p in pages if f'"[[{page.stem}]]"' in p.read_text(encoding="utf-8").split("---")[1]}
    out += [f"{name}: {s} has lens but no row" for s in sorted(owned - set(listed))]
    out += [f"{name}: row {s} is not a source with this lens" for s in sorted(set(listed) - owned)]
    return out


def proposal_problems() -> list[str]:
    path = ROOT / "inbox/proposals.md"
    if not path.exists():
        return []
    approved = {p.stem for p in (ROOT / "wiki/lenses").glob("*.md")
                if not re.search(r"^status: proposed", p.read_text(encoding="utf-8"), flags=re.M)}
    known = known_keys(exclude="inbox/proposals.md")
    sections = split(path.read_text(encoding="utf-8"), "##")
    out, keys = [], Counter()
    for title, body in sections.items():
        entries = re.findall(r"^\d+\. (\S+)(.*)$", body, flags=re.M)
        for url, rest in entries:
            keys[url_key(url)] += 1
            if url_key(url) in known:
                out.append(f"proposals.md: {url} already in sources, links.md or search-rejections.yaml")
            if not set(re.findall(r"\[\[([^\]|]+)\]\]", rest)) & approved:
                out.append(f"proposals.md: {url} links no approved lens")
    if sections and len(re.findall(r"^\d+\. ", list(sections.values())[-1], flags=re.M)) > 10:
        out.append("proposals.md: latest search has more than 10 candidates")
    return out + [f"proposals.md: {k} proposed twice" for k, n in keys.items() if n > 1]


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
        related = split(text, "##").get("关联", "")
        for line in related.strip().splitlines():
            m = re.match(rf"- ({'|'.join(RELATIONS)}) \[\[([^\]|]+)\]\]：", line)
            if not m:
                problems.append(f"{page.name}: 关联 line not '- <{'/'.join(RELATIONS)}> [[slug]]：…': {line[:40]}")
            elif m.group(2) == page.stem or not (ROOT / "wiki/sources" / f"{m.group(2)}.md").exists():
                problems.append(f"{page.name}: 关联 links non-source {m.group(2)}")

    for lens in sorted((ROOT / "wiki/lenses").glob("*.md")):
        problems += lens_problems(lens, pages)
    problems += proposal_problems()

    canonical = model_names() | {p.stem for p in pages}
    methods = Counter()
    for page in pages:
        for field in NODE_FIELDS:
            values = links(page, field)
            problems += [f"{page.name}: {field} lists {v} twice" for v, n in Counter(values).items() if n > 1]
            if field.startswith("models_"):
                problems += [f"{page.name}: {field} {v} not in docs/model-names.md" for v in values if v not in canonical]
        methods.update(links(page, "methods"))
    problems += [f"method {m} used by only one source" for m, n in methods.items() if n < 2]

    broken = unresolved_links({v for p in pages for f in NODE_FIELDS for v in links(p, f)})
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
