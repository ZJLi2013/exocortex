"""Structural check of the wiki: source pages, raw files, unresolved links."""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIELDS = ["type", "url", "published", "ingested", "concepts", "lenses"]


def unresolved_links() -> list[str]:
    # Resolved like Obsidian: by file name or by vault-relative path, ignoring #heading and |alias.
    files = [p.relative_to(ROOT).with_suffix("").as_posix() for p in ROOT.rglob("*.md")]
    targets = set(files) | {f.rsplit("/", 1)[-1] for f in files}
    broken = []
    for page in sorted((ROOT / "wiki").rglob("*.md")):
        for link in re.findall(r"\[\[([^\]|#]+)", page.read_text(encoding="utf-8")):
            if link.strip() not in targets:
                broken.append(f"{link} (in {page.relative_to(ROOT).as_posix()})")
    return broken


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
        if not (ROOT / "raw" / page.name).exists() or f"[[raw/{page.stem}]]" not in text:
            problems.append(f"{page.name}: no raw/{page.name} or no link to it")

    broken = unresolved_links()
    if broken:
        problems.append("unresolved links: " + "; ".join(broken))

    concepts = sorted((ROOT / "wiki/concepts").glob("*.md"))
    print(f"{len(pages)} sources, {len(concepts)} concepts")
    for c in concepts:
        print(f"  {c.stem}: {c.read_text(encoding='utf-8').count('- [[')} sources")
    for p in problems:
        print("FAIL", p)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
