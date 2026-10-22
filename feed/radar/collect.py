"""One collection run: every channel of every team."""

import argparse
import json
import os
from datetime import date
from pathlib import Path

import requests
import trafilatura

from radar import config
from radar.channels import COLLECTORS
from radar.channels.common import Context
from radar.daily import append_rows, read_rows

UA = {"User-Agent": "Mozilla/5.0 (compatible; embodied-radar/0.1)"}


def make_context(run_date: date, state_dir: Path, date_fetch_budget: int) -> Context:
    session = requests.Session()
    session.headers.update(UA)
    token = os.environ.get("GITHUB_TOKEN")

    def get(url: str):
        headers = {}
        if token and url.startswith("https://api.github.com"):
            headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
        return session.get(url, headers=headers, timeout=30)

    def page_date(url: str) -> str | None:
        try:
            resp = get(url)
            if resp.status_code >= 400:
                return None
            doc = trafilatura.extract(resp.text, url=resp.url, output_format="json", with_metadata=True)
        except Exception:  # trafilatura raises on some markup; treat as undated
            return None
        return json.loads(doc).get("date") if doc else None

    return Context(run_date, state_dir, get, page_date, date_fetch_budget)


STATE_KIND = {"rss": "feeds", "page": "pages"}


def channel_key(entity_id: str, channel: dict, index: int) -> str:
    """Stable state key; `index` counts earlier channels of the same type in this entity."""
    return f"{STATE_KIND.get(channel['type'], channel['type'])}/{entity_id}" + (f"-{index}" if index else "")


def run_channel(channel: dict, ctx: Context, key: str) -> dict:
    try:
        return COLLECTORS[channel["type"]](channel, ctx, key)
    except Exception as exc:  # one broken channel must not stop the run
        return {"status": "failed", "fetched": 0, "new": [], "baseline": 0, "error": type(exc).__name__}


def run(domain_dir: str, out_dir: str, state_dir: str, run_date: date | None = None) -> dict:
    domain = config.load(domain_dir)
    run_date = run_date or date.today()
    ctx = make_context(run_date, Path(state_dir), int(domain.page.get("date_fetch_budget", 150)))

    entities, items = {}, {}
    for entity in domain.entities:
        if entity["tier"] == "dormant":
            continue
        rows, per_type = [], {}
        for channel in entity["channels"]:
            target = channel.get("url") or channel.get("org")
            index = per_type.get(channel["type"], 0)
            per_type[channel["type"]] = index + 1
            if channel.get("broken"):
                rows.append({"type": channel["type"], "target": target, "status": "broken", "error": channel["broken"],
                             "fetched": 0, "new": [], "baseline": 0})
                continue
            result = run_channel(channel, ctx, channel_key(entity["id"], channel, index))
            rows.append({"type": channel["type"], "target": target, **result})
            for item in result["new"]:
                merged = items.setdefault(item["key"], {**item, "sources": []})
                merged["sources"].append({"entity": entity["id"], "type": channel["type"]})
        entities[entity["id"]] = {"direction": entity["direction"], "channels": rows}

    all_rows = [r for e in entities.values() for r in e["channels"]]
    by_type = {}
    for r in all_rows:
        t = by_type.setdefault(r["type"], {"channels": 0, "failed": 0, "broken": 0, "no_update": 0, "updated": 0, "new": 0})
        t["channels"] += 1
        t[r["status"]] += 1
        t["new"] += len(r["new"])
    summary = {
        "run_date": run_date.isoformat(),
        "window": {"start": ctx.window_start.isoformat(), "end": run_date.isoformat()},
        "totals": {"channels": len(all_rows), "failed": sum(r["status"] == "failed" for r in all_rows),
                   "broken": sum(r["status"] == "broken" for r in all_rows), "new_items": len(items)},
        "by_type": by_type,
        "page_date_fetches": {"used": ctx.date_fetches, "budget": ctx.date_fetch_budget},
        "entities": entities,
    }

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "items.jsonl", "w", encoding="utf-8") as f:
        for item in items.values():
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def append_signals(items_path: Path, signals_path: Path, run_date: str) -> int:
    """items.jsonl holds only this run's new items and is overwritten, so keep one row per (work, team) across runs."""
    seen = {(r["key"], r["entity"]) for r in read_rows(signals_path)}
    rows = []
    for item in read_rows(items_path):
        published = item.get("published") or item.get("page_date")
        for source in item["sources"]:
            if (item["key"], source["entity"]) not in seen:
                seen.add((item["key"], source["entity"]))
                rows.append({"key": item["key"], "url": item["url"], "title": item.get("title", ""),
                             "published": published[:10] if published else None, "entity": source["entity"],
                             "type": source["type"], "run_date": run_date})
    append_rows(signals_path, rows)
    append_rows(signals_path.with_name("collect_runs.jsonl"), [{"run_date": run_date, "new_signals": len(rows)}])
    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect this week's new items for a domain")
    parser.add_argument("--domain", default="embodied")
    parser.add_argument("--out", default=None, help="default: out/<domain>/latest")
    parser.add_argument("--state", default=None, help="default: state/<domain>")
    parser.add_argument("--signals", default=None, help="append this run's new items to a cumulative signals.jsonl")
    args = parser.parse_args()
    out = args.out or f"out/{args.domain}/latest"
    summary = run(f"domains/{args.domain}", out, args.state or f"state/{args.domain}")
    if args.signals:
        summary["new_signals"] = append_signals(Path(out) / "items.jsonl", Path(args.signals), summary["run_date"])
    print(json.dumps({k: summary[k] for k in ("run_date", "totals", "by_type", "new_signals") if k in summary},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
