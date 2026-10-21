"""Daily run: new project signals from the human's GitHub feed, and the human's new stars. Standard library only."""
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from radar.github_feed import fetch_page, parse_cards

MAX_PAGES = 6  # the feed endpoint returns nothing past page 6 (about 52 hours)
STAR_PAGES = 3
API = "https://api.github.com"


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def signal_key(card: dict) -> tuple:
    # GitHub repeats its own picks on later pages and later days; a followed user's card is one action.
    if card["actor"] is None:
        return (card["signal"], card["repo"])
    return (card["signal"], card["actor"], card["repo"], card["at"])


def adoption_key(star: dict) -> tuple:
    return (star["repo"], star["starred_at"])


def read_rows(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()] if path.exists() else []


def append_rows(path: Path, rows: list[dict]) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)


def github_starred(user: str, token: str):
    def get(page: int) -> list:
        request = urllib.request.Request(
            f"{API}/users/{user}/starred?per_page=100&page={page}",
            headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.star+json",
                     "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "embodied-radar"})
        with urllib.request.urlopen(request, timeout=30) as resp:
            return json.loads(resp.read())
    return get


def run(store: Path, get_page, get_starred, run_id: str, trigger: str) -> dict:
    """`get_page(n)` returns feed page n as HTML; `get_starred(n)` returns page n of the human's stars (star+json)."""
    started = time.time()
    store.mkdir(parents=True, exist_ok=True)
    snap = store / "snapshots" / run_id
    snap.mkdir(parents=True, exist_ok=True)
    cursor_path = store / "cursor.json"
    cursor = json.loads(cursor_path.read_text(encoding="utf-8")) if cursor_path.exists() else {}
    feed_cursor = parse_time(cursor["feed"]) if cursor.get("feed") else None
    star_cursor = parse_time(cursor["adoptions"]) if cursor.get("adoptions") else None
    errors = []

    cards, pages, reached = [], 0, feed_cursor is None
    try:
        for n in range(1, MAX_PAGES + 1):
            page_html = get_page(n)
            pages += 1
            (snap / f"page{n:02d}.html").write_text(page_html, encoding="utf-8")
            batch = parse_cards(page_html)
            if not batch:
                if n == 1:
                    errors.append("feed page 1 has no cards: session expired or the endpoint changed")
                break
            cards += batch
            if feed_cursor and any(c["actor"] and parse_time(c["at"]) <= feed_cursor for c in batch):
                reached = True
                break
    except Exception as e:  # noqa: BLE001 - recorded in runs.jsonl, the verifier fails the run
        errors.append(f"feed page {pages + 1}: {e}")

    stars, star_calls = [], 0
    try:
        for n in range(1, STAR_PAGES + 1):
            batch = get_starred(n)
            star_calls += 1
            (snap / f"starred{n:02d}.json").write_text(json.dumps(batch), encoding="utf-8")
            stars += [{"repo": s["repo"]["full_name"], "starred_at": s["starred_at"]} for s in batch]
            if len(batch) < 100 or (star_cursor and any(parse_time(s["starred_at"]) <= star_cursor for s in batch)):
                break
    except Exception as e:  # noqa: BLE001
        errors.append(f"starred page {star_calls + 1}: {e}")

    signal_path, adoption_path = store / "signals.jsonl", store / "adoptions.jsonl"
    known = {signal_key(r) for r in read_rows(signal_path)}
    new_signals = []
    for c in cards:
        if (k := signal_key(c)) not in known:
            known.add(k)
            new_signals.append({"signal": c["signal"], "actor": c["actor"], "repo": c["repo"], "at": c["at"], "run": run_id})
    adopted = {adoption_key(r) for r in read_rows(adoption_path)}
    new_adoptions = []
    for s in stars:
        if (k := adoption_key(s)) not in adopted:
            adopted.add(k)
            new_adoptions.append(s | {"run": run_id})
    append_rows(signal_path, new_signals)
    append_rows(adoption_path, new_adoptions)

    followed = [parse_time(c["at"]) for c in cards if c["actor"]]
    if followed:
        cursor["feed"] = max(followed + ([feed_cursor] if feed_cursor else [])).isoformat()
    if stars:
        cursor["adoptions"] = max([parse_time(s["starred_at"]) for s in stars] + ([star_cursor] if star_cursor else [])).isoformat()
    cursor_path.write_text(json.dumps(cursor), encoding="utf-8")
    row = {"run": run_id, "trigger": trigger, "started": datetime.fromtimestamp(started, timezone.utc).isoformat(),
           "seconds": round(time.time() - started, 1), "pages": pages, "star_calls": star_calls,
           "new_signals": len(new_signals), "new_adoptions": len(new_adoptions),
           "gap": not reached and not errors, "errors": errors}
    append_rows(store / "runs.jsonl", [row])
    return row


def main() -> int:
    store = Path(sys.argv[1])
    session, token, user = os.environ["GITHUB_SESSION"], os.environ["GITHUB_TOKEN"], os.environ.get("GITHUB_USER", "ZJLi2013")
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    row = run(store, lambda n: fetch_page(n, session), github_starred(user, token), run_id,
              os.environ.get("RADAR_TRIGGER", "manual"))
    print(json.dumps(row))
    return 1 if row["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
