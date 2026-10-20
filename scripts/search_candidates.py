"""Search SearXNG for each `<lens> | <query>` line and print results not already known to the wiki."""

import argparse
import datetime
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KNOWN = ["raw/*.md", "wiki/sources/*.md", "inbox/links.md", "inbox/proposals.md", "wiki/search-rejections.yaml"]


def url_key(url: str) -> str:
    m = re.search(r"arxiv\.org/(?:abs|html|pdf)/(\d{4}\.\d{4,5})", url)
    if m:
        return f"arxiv:{m.group(1)}"
    parts = urllib.parse.urlsplit(url.strip().lower())
    host = parts.netloc.removeprefix("www.")
    path = parts.path.rstrip("/").removesuffix(".git")
    if host == "github.com":
        path = "/".join(path.split("/")[:3])
    return host + path


def known_keys(exclude: str | None = None) -> set[str]:
    # Only URLs that open a line or a `url:` field count; URLs cited inside raw full texts are fair candidates.
    keys = set()
    for pattern in KNOWN:
        for f in ROOT.glob(pattern):
            if f.relative_to(ROOT).as_posix() == exclude:
                continue
            text = f.read_text(encoding="utf-8")
            for url in re.findall(r"^(?:- )?(?:url:\s*|\d+\.\s+)?(https?://\S+)", text, flags=re.M):
                keys.add(url_key(url))
    return keys


def known_work(title: str, content: str) -> str | None:
    # A source ingested from its repo or project page comes back from search as its paper, under another URL.
    for page in (ROOT / "wiki/sources").glob("*.md"):
        name = re.search(r"^# (.+)", page.read_text(encoding="utf-8"), flags=re.M).group(1).strip()
        n = re.escape(name)
        if re.match(rf"{n}\s*:", title) or re.search(rf"\bintroduces?\s+{n}\b", content):
            return name
    return None


def search(base: str, query: str, engines: str) -> dict:
    params = urllib.parse.urlencode({"q": query, "format": "json", "engines": engines})
    with urllib.request.urlopen(f"{base}/search?{params}", timeout=90) as resp:
        return json.load(resp)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("queries", type=Path, help="file with one `<lens> | <query>` per line")
    parser.add_argument("--engines", default="arxiv")
    parser.add_argument("--days", type=int, default=30, help="drop results published longer ago; undated results are kept")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    base = os.environ.get("SEARXNG_URL") or sys.exit("set SEARXNG_URL, e.g. http://127.0.0.1:8888")

    seen = known_keys()
    since = datetime.date.today() - datetime.timedelta(days=args.days)
    out = []
    for line in args.queries.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        lens, query = (s.strip() for s in line.split("|", 1))
        data = search(base.rstrip("/"), query, args.engines)
        if data.get("unresponsive_engines"):
            print(f"unresponsive for {query!r}: {data['unresponsive_engines']}", file=sys.stderr)
        for r in data["results"]:
            published = (r.get("publishedDate") or "")[:10]
            if published and published < since.isoformat():
                continue
            key = url_key(r["url"])
            if key in seen:
                continue
            seen.add(key)
            work = known_work(r.get("title", ""), r.get("content", ""))
            if work:
                print(f"skip {r['url']}: known work {work}", file=sys.stderr)
                continue
            out.append({"lens": lens, "query": query, "url": r["url"], "title": r.get("title", ""),
                        "published": published, "engine": r.get("engine"), "content": r.get("content", "")[:400]})
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
