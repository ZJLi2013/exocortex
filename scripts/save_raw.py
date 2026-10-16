"""Write raw/<slug>.md with frontmatter, from a fetched file or by downloading a URL."""

import argparse
import datetime
import sys
import urllib.request
from pathlib import Path

RAW = Path(__file__).resolve().parent.parent / "raw"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True, help="source URL recorded in frontmatter")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--from", dest="src", help="already-fetched markdown file; omit to download --fetch-url")
    parser.add_argument("--fetch-url", help="URL to download when it differs from --url (e.g. raw README)")
    args = parser.parse_args()

    target = RAW / f"{args.slug}.md"
    if target.exists():
        sys.exit(f"{target} exists; raw files are written once")
    if args.src:
        body = Path(args.src).read_text(encoding="utf-8")
    else:
        with urllib.request.urlopen(args.fetch_url or args.url, timeout=60) as resp:
            body = resp.read().decode("utf-8")
    front = f"---\nurl: {args.url}\nfetched: {datetime.date.today()}\ntitle: \"{args.title}\"\n---\n\n"
    RAW.mkdir(exist_ok=True)
    target.write_text(front + body, encoding="utf-8", newline="\n")
    print(f"{target.relative_to(RAW.parent)}: {len(body)} chars")


if __name__ == "__main__":
    main()
