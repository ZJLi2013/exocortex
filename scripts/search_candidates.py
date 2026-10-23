"""Search alphaXiv for each `<lens> | <keyword|embedding> | <query>` line and print results not already known to the wiki."""

import argparse
import datetime
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KNOWN = ["wiki/sources/*.md", "inbox/links.md", "inbox/proposals.md", "wiki/search-rejections.yaml"]
API = "https://api.alphaxiv.org/search/v2/paper/discover"


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


def known_locations(exclude: str | None = None) -> dict[str, str]:
    # Only URLs that open a line or a `url:` field count; URLs cited in page bodies are fair candidates.
    locations = {}
    for pattern in KNOWN:
        for f in ROOT.glob(pattern):
            rel = f.relative_to(ROOT).as_posix()
            if rel == exclude:
                continue
            text = f.read_text(encoding="utf-8")
            for url in re.findall(r"^(?:- )?(?:url:\s*|\d+\.\s+)?(https?://\S+)", text, flags=re.M):
                locations.setdefault(url_key(url), rel)
    return locations


def known_keys(exclude: str | None = None) -> set[str]:
    return set(known_locations(exclude))


def known_work(title: str, content: str) -> str | None:
    # A source ingested from its repo or project page comes back from search as its paper, under another URL.
    for page in (ROOT / "wiki/sources").glob("*.md"):
        name = re.search(r"^# (.+)", page.read_text(encoding="utf-8"), flags=re.M).group(1).strip()
        n = re.escape(name)
        if re.match(rf"{n}\s*:", title) or re.search(rf"\bintroduces?\s+{n}\b", content):
            return name
    return None


def search(strategy: str, query: str, since: str | None) -> list[dict]:
    params = {"q": query, "prioritize": "default"}
    if since:
        params["publishedAfter"] = since
    req = urllib.request.Request(f"{API}/{strategy}?{urllib.parse.urlencode(params)}",
                                 headers={"user-agent": "exocortex-search"})
    for attempt in range(1, 4):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 3:
                raise
            wait = e.headers.get("Retry-After", "")
            time.sleep(int(wait) if wait.isdigit() else attempt)
    return []


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("queries", type=Path, help="file with one `<lens> | <keyword|embedding> | <query>` per line")
    parser.add_argument("--days", type=int, default=30, help="only papers published in the last N days; 0 = no lower bound")
    parser.add_argument("--include-known", action="store_true",
                        help="keep works already in the wiki and mark where they are (for novelty checks)")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    since = (datetime.date.today() - datetime.timedelta(days=args.days)).isoformat() if args.days else None
    known = known_locations()
    out: dict[str, dict] = {}
    for line in args.queries.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        lens, strategy, query = (s.strip() for s in line.split("|", 2))
        for r in search(strategy, query, since):
            paper_id = re.sub(r"v\d+$", "", r["paperId"])
            url = f"https://arxiv.org/abs/{paper_id}"
            key = url_key(url)
            if key in out:
                out[key]["queries"].append(f"{lens}: {query}")
                continue
            work = known_work(r.get("title", ""), r.get("abstract", ""))
            where = known.get(key) or (f"work {work}" if work else None)
            if where and not args.include_known:
                print(f"skip {url}: known in {where}", file=sys.stderr)
                continue
            out[key] = {"lens": lens, "queries": [f"{lens}: {query}"], "url": url, "title": r.get("title", ""),
                        "published": (r.get("publicationDate") or "")[:10], "known": where,
                        "abstract": r.get("abstract") or "摘要缺失"}
    print(json.dumps(list(out.values()), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
