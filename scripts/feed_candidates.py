"""Append the top works from feed/'s candidates.json that the wiki has not seen to inbox/links.md for ingest."""

import json
import os
import subprocess
import sys
from pathlib import Path

from search_candidates import ROOT, known_keys, url_key

LIMIT = 5


def read_candidates() -> str:
    """RADAR_FEED is the private store path, or <user@host>:<path> to read it over ssh."""
    value = os.environ.get("RADAR_FEED") or sys.exit("set RADAR_FEED=<private store path> or <user@host>:<path>")
    host, sep, store = value.partition(":")
    if not sep:
        return (Path(value) / "candidates.json").read_text(encoding="utf-8")
    return subprocess.run(["ssh", "-o", "BatchMode=yes", host, f"cat {store}/candidates.json"],
                          capture_output=True, text=True, encoding="utf-8", check=True).stdout


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    seen, picked = known_keys(), []
    for work in json.loads(read_candidates())["works"]:
        if len(picked) < LIMIT and url_key(work["url"]) not in seen:
            seen.add(url_key(work["url"]))
            picked.append(work)
    if not picked:
        print("no new feed works")
        return
    path = ROOT / "inbox/links.md"
    text = path.read_text(encoding="utf-8").strip("\n")
    path.write_text("\n".join([text] * bool(text) + [w["url"] for w in picked]) + "\n", encoding="utf-8")
    for w in picked:
        print(f"{w['url']} — {w['name']}（{' · '.join(w['signals']) or '判定'}）")


if __name__ == "__main__":
    main()
