"""Structural check of the wiki: source pages, raw files, unresolved links, Bases view."""

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIELDS = ["type", "url", "published", "ingested", "concepts", "lenses"]


def obsidian(command: str) -> str:
    # base:query exits -1 on Windows unless launched through the shell.
    return subprocess.run(f"obsidian {command}", shell=True, cwd=ROOT, capture_output=True, text=True,
                          encoding="utf-8", check=True).stdout.strip()


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

    # raw/ keeps the original pages' relative links; only wiki/ must resolve.
    rows = [r.split("\t") for r in obsidian("unresolved verbose format=tsv").splitlines() if "\t" in r]
    broken = [f"{r[0]} (in {r[-1]})" for r in rows if r[-1].startswith("wiki/")]
    if broken:
        problems.append("unresolved links: " + "; ".join(broken))

    listed = obsidian("base:query path=wiki/index.base view=sources format=paths").splitlines()
    if len(listed) != args.sources:
        problems.append(f"Bases view lists {len(listed)} sources, expected {args.sources}")

    concepts = sorted((ROOT / "wiki/concepts").glob("*.md"))
    print(f"{len(pages)} sources, {len(concepts)} concepts")
    for c in concepts:
        print(f"  {c.stem}: {c.read_text(encoding='utf-8').count('- [[')} sources")
    for p in problems:
        print("FAIL", p)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
