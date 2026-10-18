"""Structural check of the wiki: source pages, raw files, lens pages, unresolved links."""

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIELDS = ["type", "url", "published", "ingested", "tags", "concepts", "lenses"]
# raw/ is local-only (third-party full texts); fresh clones do not have it.
HAS_RAW = (ROOT / "raw").is_dir()


def unresolved_links() -> list[str]:
    # Resolved like Obsidian: by file name or by vault-relative path, ignoring #heading and |alias.
    files = [p.relative_to(ROOT).with_suffix("").as_posix() for p in ROOT.rglob("*.md")]
    targets = set(files) | {f.rsplit("/", 1)[-1] for f in files}
    broken = []
    for page in sorted((ROOT / "wiki").rglob("*.md")):
        for link in re.findall(r"\[\[([^\]|#]+)", page.read_text(encoding="utf-8")):
            if link.strip() not in targets and (HAS_RAW or not link.startswith("raw/")):
                broken.append(f"{link} (in {page.relative_to(ROOT).as_posix()})")
    return broken


def split(text: str, prefix: str) -> dict[str, str]:
    parts = re.split(rf"^{prefix} ", text, flags=re.M)[1:]
    return {p.split("\n", 1)[0].strip(): p.split("\n", 1)[-1] for p in parts}


def lens_problems(page: Path) -> list[str]:
    text = page.read_text(encoding="utf-8")
    if re.search(r"^status: proposed", text, flags=re.M):
        return []
    name, out = page.name, []
    sections = split(text, "##")
    missing = [s for s in ["范围", "问题", "判断", "冲突"] if s not in sections]
    if missing:
        return [f"{name}: missing section {', '.join(missing)}"]
    ids = Counter(re.findall(r"^### ([QC]\d+)", text, flags=re.M))
    out += [f"{name}: duplicate {i}" for i, n in ids.items() if n > 1]
    questions = {h.split()[0]: body for h, body in split(sections["问题"], "###").items()}
    claims = {h.split()[0]: body for h, body in split(sections["判断"], "###").items()}
    if not 2 <= len(questions) <= 5:
        out.append(f"{name}: {len(questions)} questions, expected 2–5")
    for q, body in questions.items():
        answer = re.search(r"^当前答案：(.*)", body, flags=re.M)
        if not answer:
            out.append(f"{name}: {q} has no 当前答案")
            continue
        out += [f"{name}: {q} cites missing {c}" for c in re.findall(r"C\d+", answer.group(1)) if c not in claims]
    for c, body in claims.items():
        fields = dict(re.findall(r"^- (回答|支持|限定|反驳|推翻)：(.*)", body, flags=re.M))
        absent = [f for f in ["回答", "支持", "限定", "反驳", "推翻"] if f not in fields]
        if absent:
            out.append(f"{name}: {c} missing {', '.join(absent)}")
            continue
        if fields["回答"].strip() not in questions:
            out.append(f"{name}: {c} answers unknown {fields['回答'].strip()}")
        if not re.search(r"^- 支持：\n  - ", body, flags=re.M):
            out.append(f"{name}: {c} has no supporting evidence")
        for item in re.findall(r"^  - (.*)", body, flags=re.M):
            m = re.match(r"\[\[([^\]]+)\]\]（(自报|第三方)）", item)
            if not m:
                out.append(f"{name}: {c} evidence not '[[slug]]（自报|第三方）…': {item[:40]}")
            elif not (ROOT / "wiki/sources" / f"{m.group(1)}.md").exists():
                out.append(f"{name}: {c} evidence links non-source {m.group(1)}")
    out += [f"{name}: conflict cites missing {c}" for c in re.findall(r"\[!contradiction\] (C\d+)", sections["冲突"]) if c not in claims]
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

    for lens in sorted((ROOT / "wiki/lenses").glob("*.md")):
        problems += lens_problems(lens)

    broken = unresolved_links()
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
