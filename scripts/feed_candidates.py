"""Append a `feed` section to inbox/proposals.md from the human's GitHub feed and the company-channel radar,
or (`--label`) record the human's disposition of a feed repo as a preference label."""

import argparse
import datetime
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request

from search_candidates import ROOT, known_keys, url_key

ENTRIES = "https://raw.githubusercontent.com/ZJLi2013/embodied_radar/main/wiki/embodied/entries.jsonl"
LIMIT = 10


def remote(command: str, stdin: str | None = None) -> str:
    """Run `command` on the private store host; `{store}` expands to the store path."""
    value = os.environ.get("RADAR_FEED") or sys.exit("set RADAR_FEED=<user@host>:<private store path>")
    host, _, store = value.partition(":")
    return subprocess.run(["ssh", "-o", "BatchMode=yes", host, command.format(store=store)], input=stdin,
                          capture_output=True, text=True, encoding="utf-8", check=True).stdout


def rows(text: str) -> list[dict]:
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def judgments() -> dict[str, dict]:
    return {j["repo"]: j for j in rows(remote("cat {store}/judgments.jsonl"))}


def candidates() -> list[tuple[str, str, str, str]]:
    """(url, name, one line, origin), in delivery order: rising, company channels, judged yes."""
    judged = judgments()
    rising = json.loads(remote("cat {store}/rising.json"))["repos"]
    out = []
    for r in sorted(rising, key=lambda r: -r["followers"]):
        origin = f"上升：{r['followers']} 位关注者" if r["followers"] >= 2 else "上升：GitHub trending"
        out.append((f"https://github.com/{r['repo']}", r["repo"].split("/")[1], judged[r["repo"]]["meta"]["description"], origin))
    with urllib.request.urlopen(ENTRIES, timeout=30) as resp:
        entries = rows(resp.read().decode("utf-8"))
    for e in sorted(entries, key=lambda e: e["date"], reverse=True):
        out.append((e["url"], e["title"], e["reason"], f"公司渠道：{e['team']}"))
    shown = {r["repo"] for r in rising}
    for j in sorted(judged.values(), key=lambda j: -(j["confidence"] or 0)):
        if j["verdict"] == "yes" and j["repo"] not in shown:
            out.append((f"https://github.com/{j['repo']}", j["repo"].split("/")[1], j["meta"]["description"], "判定"))
    return out


def deliver() -> None:
    seen, lines = known_keys(), []
    for url, name, text, origin in candidates():
        if url_key(url) in seen or len(lines) == LIMIT:
            continue
        seen.add(url_key(url))
        lines.append(f"{len(lines) + 1}. {url} — {name}。{' '.join(text.split()).rstrip('。.')}（{origin}）")
    if not lines:
        print("no new feed candidates")
        return
    path = ROOT / "inbox/proposals.md"
    text = path.read_text(encoding="utf-8").rstrip("\n")
    path.write_text(f"{text}\n\n## [{datetime.date.today()}] feed\n\n" + "\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def label(url: str, value: str) -> None:
    parts = urllib.parse.urlsplit(url).path.strip("/").split("/")
    repo = next((r for r in judgments() if r.lower() == "/".join(parts[:2]).lower()), None)
    if repo is None:
        print(f"{url} is not a judged feed repo; no label")
        return
    at = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    row = json.dumps({"repo": repo, "label": value, "from": "proposal", "at": at})
    remote("cat >> {store}/labels.jsonl", stdin=row + "\n")
    print(row)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--label", nargs=2, metavar=("URL", "yes|no"))
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if args.label:
        if args.label[1] not in ("yes", "no"):
            sys.exit("label must be yes or no")
        label(*args.label)
    else:
        deliver()


if __name__ == "__main__":
    main()
