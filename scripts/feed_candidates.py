"""Append the top works from feed/'s candidates.json that the wiki has not seen to inbox/links.md for ingest."""

import json
import os
import subprocess
import sys

from search_candidates import ROOT, known_keys, url_key

LIMIT = 5


def remote(command: str) -> str:
    """Run `command` on the private store host; `{store}` expands to the store path."""
    value = os.environ.get("RADAR_FEED") or sys.exit("set RADAR_FEED=<user@host>:<private store path>")
    host, _, store = value.partition(":")
    return subprocess.run(["ssh", "-o", "BatchMode=yes", host, command.format(store=store)],
                          capture_output=True, text=True, encoding="utf-8", check=True).stdout


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    seen, picked = known_keys(), []
    for work in json.loads(remote("cat {store}/candidates.json"))["works"]:
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
