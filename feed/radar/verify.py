"""Locked verifiers for radar tasks. Exit 0 iff the acceptance criteria in the plan hold."""

import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

def check_page_states(report: dict) -> list[str]:
    """Each page state file: seen and pending are disjoint, cover the current links, and match the summary."""
    problems = []
    for eid, e in report["entities"].items():
        for r in e["channels"]:
            if r["type"] != "page" or r["status"] == "failed":
                continue
            if not r.get("snapshot") or not Path(r["snapshot"]).exists():
                problems.append(f"{eid}: page {r['target']} wrote no snapshot ({r.get('snapshot')})")
                continue
            state = json.loads(Path(r["snapshot"]).read_text(encoding="utf-8"))
            seen, pending = set(state["seen"]), set(state["pending"])
            if seen & pending:
                problems.append(f"{eid}: {len(seen & pending)} links are both seen and pending")
            if missing := set(r["links"]) - seen - pending:
                problems.append(f"{eid}: {len(missing)} current links in neither seen nor pending")
            if len(pending) != r["pending"]:
                problems.append(f"{eid}: state has {len(pending)} pending, summary says {r['pending']}")
    return problems


def check_feed_replay(pages_dir: Path, sample_path: Path) -> list[str]:
    """Parsed feed pages hold every actor -> repo pair the human saw on /feed."""
    from radar.github_feed import parse_cards

    sample = json.loads(sample_path.read_text(encoding="utf-8"))
    t = lambda s: datetime.fromisoformat(s.replace("Z", "+00:00"))
    start, end = t(sample["window"]["start"]), t(sample["window"]["end"])
    cards = [c for p in sorted(pages_dir.glob("page*.html")) for c in parse_cards(p.read_text(encoding="utf-8"))]
    problems = []
    # GitHub re-inserts its own recommendations on later pages; only followed users' cards must be unique.
    if dup := [k for k, n in Counter((c["signal"], c["actor"], c["repo"], c["at"]) for c in cards if c["actor"]).items() if n > 1]:
        problems.append(f"{len(dup)} cards repeat across pages, first: {dup[0]}")
    in_window = [c for c in cards if start <= t(c["at"]) <= end]
    seen = {((c["actor"] or "").lower(), c["signal"], c["repo"].lower()) for c in in_window}
    missed = [p for p in sample["pairs"] if (p["actor"].lower(), p["action"], p["repo"].lower()) not in seen]
    problems += [f"{p['actor']} -> {p['repo']} ({p['action']}) not parsed from the feed pages" for p in missed]
    print(f"pages {len(list(pages_dir.glob('page*.html')))}; signal cards {len(cards)}, in window {len(in_window)}, "
          f"repos in window {len({c['repo'] for c in in_window})}; pairs hit {len(sample['pairs']) - len(missed)}/{len(sample['pairs'])}")
    print("in-window signals: " + ", ".join(f"{k} {v}" for k, v in Counter(c["signal"] for c in in_window).most_common()))
    return problems


def check_daily(store: Path) -> list[str]:
    """The latest cron run on the private store: no errors, within budget, and no duplicate keys in the store."""
    from radar.daily import adoption_key, signal_key

    runs = [r for r in read_rows(store / "runs.jsonl") if r["trigger"] == "cron"]
    if not runs:
        return ["no cron run recorded"]
    r, problems = runs[-1], []
    if r["errors"]:
        problems.append(f"run {r['run']}: errors {r['errors']}")
    if r["pages"] > 6 or r["star_calls"] > 5 or r["seconds"] > 120:
        problems.append(f"run {r['run']}: {r['pages']} pages, {r['star_calls']} star calls, {r['seconds']} s")
    signals, adoptions = read_rows(store / "signals.jsonl"), read_rows(store / "adoptions.jsonl")
    for name, rows, key in (("signals", signals, signal_key), ("adoptions", adoptions, adoption_key)):
        if dup := [k for k, n in Counter(map(key, rows)).items() if n > 1]:
            problems.append(f"{len(dup)} duplicate {name}, first: {dup[0]}")
    print(f"cron run {r['run']}: new signals {r['new_signals']}, new adoptions {r['new_adoptions']}; "
          f"totals {len(signals)} signals, {len(adoptions)} adoptions")
    return problems


def check_feed_judge(store: Path, rejections: Path | None = None) -> list[str]:
    """Every work from the feed and company channels judged once or skipped, keyed by work;
    candidates.json matches the judgments; company signals accumulate; star labels complete;
    own repos, rejection labels and the star hit rate as the latest run recorded them."""
    from radar.feed_judge import (COMPANY_FRESH_DAYS, OWN_ACTIVE_DAYS, aggregate, candidates, display, feed_key,
                                  is_fresh, sha, snapshot_name, star_hits)

    runs = read_rows(store / "judge_runs.jsonl")
    if not runs:
        problems = ["no feed_judge run recorded"]
    else:
        problems = [f"run {runs[-1]['run']}: errors {runs[-1]['errors']}"] if runs[-1]["errors"] else []
    company = read_rows(store / "company" / "signals.jsonl")
    works = aggregate(read_rows(store / "signals.jsonl"), company)
    judgments, skipped_rows, labels = (read_rows(store / f) for f in ("judgments.jsonl", "skipped.jsonl", "labels.jsonl"))
    for name, rows in (("judgments", judgments), ("skipped", skipped_rows), ("labels", labels)):
        if stale := [r for r in rows if "repo" in r or "key" not in r]:
            problems.append(f"{len(stale)} {name} rows not keyed by work, first: {stale[0]}")
            return problems
    judged, skipped = Counter(j["key"] for j in judgments), {s["key"] for s in skipped_rows}
    if dup := [k for k, n in judged.items() if n > 1]:
        problems.append(f"{len(dup)} works judged twice, first: {dup[0]}")
    if both := sorted(set(judged) & skipped):
        problems.append(f"{len(both)} works both judged and skipped, first: {both[0]}")
    if missing := sorted(set(works) - set(judged) - skipped):
        problems.append(f"{len(missing)} works neither judged nor skipped, first: {missing[0]}")
    if extra := sorted((set(judged) | skipped) - set(works)):
        problems.append(f"{len(extra)} judged or skipped works have no signal (recommended / fork only?), first: {extra[0]}")
    for j in judgments:
        readme = store / "snapshots" / j["run"] / "readme" / f"{snapshot_name(j['key'])}.md"
        if not j["meta"]["description"] or not j["context_sha"] or (j["readme_sha"] and not readme.exists()):
            problems.append(f"{j['key']}: missing description, context_sha or text snapshot")
        if "lens" in j:
            problems.append(f"{j['key']}: judgment carries a lens (judged before r4?)")

    queue_doc = json.loads((store / "candidates.json").read_text(encoding="utf-8"))
    queue, run_at = queue_doc["works"], datetime.strptime(queue_doc["run"], "%Y%m%dT%H%M%SZ")
    if queue != json.loads(json.dumps(candidates(works, judgments, run_at.date()), ensure_ascii=False)):
        problems.append("candidates.json differs from the eligibility and order rules applied to the judgments")
    if stale := [c["key"] for c in queue if not is_fresh(works[c["key"]], run_at.date())]:
        problems.append(f"{len(stale)} company-only candidates published or first seen over {COMPANY_FRESH_DAYS} days ago, first: {stale[0]}")

    rejected = {l["key"] for l in labels if l["from"] == "rejection"}
    if runs:
        own = json.loads((store / "own_repos.json").read_text(encoding="utf-8"))
        latest_run = runs[-1]["run"]
        if own["run"] != latest_run:
            problems.append(f"own_repos.json from run {own['run']}, latest run {latest_run}")
        for r in own["repos"]:
            if r["fork"] or (run_at - datetime.fromisoformat(r["pushed_at"].replace("Z", "+00:00")).replace(tzinfo=None)).days > OWN_ACTIVE_DAYS:
                problems.append(f"own repo {r['repo']}: fork {r['fork']}, pushed {r['pushed_at']}")
        bare = {f"- {display(k)}" for k in rejected}
        latest = [j for j in judgments if j["run"] == latest_run]
        for j in latest:
            request = store / "snapshots" / latest_run / "calls" / f"{snapshot_name(j['key'])}.request.json"
            context = json.loads(request.read_text(encoding="utf-8"))["messages"][1]["content"].split("\n\n## 待判工作")[0]
            if sha(context) != j["context_sha"] or not all(f"- {r['repo']}" in context for r in own["repos"]):
                problems.append(f"{j['key']}: context_sha does not cover the own repos of run {latest_run}")
            if shown := bare & set(context.splitlines()):
                problems.append(f"{j['key']}: rejection examples without text: {sorted(shown)[:3]}")
        if (hits := star_hits(labels, judgments)) != {k: runs[-1].get(k) for k in hits}:
            problems.append(f"run {latest_run}: star hit rate {[runs[-1].get(k) for k in hits]}, recomputed {hits}")
        print(f"own repos {len(own['repos'])}; judged in run {latest_run}: {len(latest)}; star hit rate {hits}")

    if rejections:
        import yaml

        from radar.urls import normalize

        listed = {normalize(r["url"]) for r in yaml.safe_load(rejections.read_text(encoding="utf-8")) or []}
        if listed != rejected:
            problems.append(f"rejection labels differ from {rejections.name}: missing {sorted(listed - rejected)[:3]}, "
                            f"extra {sorted(rejected - listed)[:3]}")
    from_feed = [c for c in queue if works[c["key"]]["followers"] or works[c["key"]]["trending"]]
    from_company = [c for c in queue if works[c["key"]]["channels"]]

    if dup := [k for k, n in Counter((c["key"], c["entity"]) for c in company).items() if n > 1]:
        problems.append(f"{len(dup)} duplicate company signals, first: {dup[0]}")
    if len(collects := read_rows(store / "company" / "collect_runs.jsonl")) < 2:
        problems.append(f"{len(collects)} company collect runs recorded; expected at least 2")

    if dup := [k for k, n in Counter((l["key"], l["from"]) for l in labels).items() if n > 1]:
        problems.append(f"{len(dup)} duplicate labels, first: {dup[0]}")
    if unlabeled := sorted({feed_key(a["repo"]) for a in read_rows(store / "adoptions.jsonl")} - {l["key"] for l in labels if l["from"] == "star"}):
        problems.append(f"{len(unlabeled)} starred repos without a star label, first: {unlabeled[0]}")

    print(f"works {len(works)} ({len(company)} company signals): judged {len(judged)}, skipped {len(skipped)}; "
          f"candidates {len(queue)} ({len(from_feed)} feed, {len(from_company)} company); labels {Counter(l['from'] for l in labels)}")
    return problems


def read_rows(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()] if path.exists() else []


def main(kind: str, path: str, prev_path: str | None = None) -> int:
    if kind in ("feed-replay", "daily", "feed-judge"):
        checks = {"feed-replay": lambda: check_feed_replay(Path(path), Path(prev_path)),
                  "daily": lambda: check_daily(Path(path)),
                  "feed-judge": lambda: check_feed_judge(Path(path), Path(prev_path) if prev_path else None)}
        problems = checks[kind]()
        for line in problems:
            print(f"FAIL {line}")
        print("PASS" if not problems else "FAIL")
        return 1 if problems else 0
    raise SystemExit(f"unknown check {kind!r}")

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
