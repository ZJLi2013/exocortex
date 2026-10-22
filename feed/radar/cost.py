"""Model spend ledger: one row per judge or ingest run in <store>/cost.jsonl, priced at DeepSeek's rates."""
import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

from radar.daily import append_rows, read_rows

# deepseek-flash, CNY per million tokens at peak; off-peak is half (api-docs.deepseek.com/zh-cn/quick_start/pricing, 2026-10-22).
# Public holidays are off-peak but are priced as weekdays here: the ledger may overstate, never understate.
PEAK_PRICES = {"hit": 0.04, "miss": 2.0, "out": 8.0}
PEAK_HOURS = [(9, 12), (14, 18)]
BEIJING = timezone(timedelta(hours=8))


def is_peak(at: datetime) -> bool:
    t = at.astimezone(BEIJING)
    return t.weekday() < 5 and any(start <= t.hour < end for start, end in PEAK_HOURS)


def cny(tokens: dict, at: datetime) -> float:
    scale = 1.0 if is_peak(at) else 0.5
    return sum(PEAK_PRICES[k] * scale * tokens[k] for k in PEAK_PRICES) / 1e6


def openai_tokens(usage: dict) -> dict:
    """Tokens from one DeepSeek OpenAI-format response."""
    return {"hit": usage.get("prompt_cache_hit_tokens", 0), "miss": usage.get("prompt_cache_miss_tokens", 0),
            "out": usage.get("completion_tokens", 0)}


def claude_tokens(result: dict) -> dict:
    """Tokens from Claude Code's `--output-format json` result, summed over every model it called."""
    tokens = {"hit": 0, "miss": 0, "out": 0}
    for u in result["modelUsage"].values():
        tokens["hit"] += u.get("cacheReadInputTokens", 0)
        tokens["miss"] += u.get("inputTokens", 0) + u.get("cacheCreationInputTokens", 0)
        tokens["out"] += u.get("outputTokens", 0)
    return tokens


def record(store: Path, job: str, run_id: str, tokens: dict, at: datetime) -> dict:
    row = {"run": run_id, "job": job, "at": at.isoformat(timespec="seconds"), **tokens, "cny": round(cny(tokens, at), 4)}
    append_rows(store / "cost.jsonl", [row])
    return row


def month_total(store: Path, now: datetime) -> float:
    month = now.astimezone(BEIJING).strftime("%Y-%m")
    return round(sum(r["cny"] for r in read_rows(store / "cost.jsonl")
                     if "cny" in r and datetime.fromisoformat(r["at"]).astimezone(BEIJING).strftime("%Y-%m") == month), 4)


def balance() -> float:
    r = requests.get("https://api.deepseek.com/user/balance", timeout=30,
                     headers={"Authorization": f"Bearer {os.environ['DEEPSEEK_API_KEY']}"})
    r.raise_for_status()
    return next(float(b["total_balance"]) for b in r.json()["balance_infos"] if b["currency"] == "CNY")


def main() -> int:
    parser = argparse.ArgumentParser(description="Model spend ledger")
    parser.add_argument("store", type=Path)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("month", help="print this month's spend in CNY")
    sub.add_parser("balance", help="append the DeepSeek CNY balance to the ledger")
    ingest = sub.add_parser("ingest", help="record a Claude Code run from its JSON result")
    ingest.add_argument("result", type=Path)
    ingest.add_argument("--run", required=True)
    ingest.add_argument("--at", required=True, help="run start, ISO 8601 with offset")
    args = parser.parse_args()
    now = datetime.now(timezone.utc)
    if args.cmd == "month":
        print(month_total(args.store, now))
    elif args.cmd == "balance":
        row = {"job": "balance", "at": now.isoformat(timespec="seconds"), "balance_cny": balance()}
        append_rows(args.store / "cost.jsonl", [row])
        print(json.dumps(row))
    else:
        result = json.loads(args.result.read_text(encoding="utf-8"))
        print(json.dumps(record(args.store, "ingest", args.run, claude_tokens(result), datetime.fromisoformat(args.at))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
