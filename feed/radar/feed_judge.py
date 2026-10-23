"""Daily judgment of works from the feed and company channels: filters, the rising gate, one DeepSeek yes / no per work."""
import argparse
import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import yaml

from radar.daily import API, append_rows, parse_time, read_rows
from radar.urls import normalize

SKIPPED_SIGNALS = {"recommended", "fork"}  # GitHub's picks and the forked copies are not signals (human, 2026-10-21)
MAX_AGE_DAYS = 180
COMPANY_FRESH_DAYS = 14  # company blogs post irregularly; stale posts must not hold queue slots (human, 2026-10-21)
OWN_ACTIVE_DAYS = 90
MAX_OWN_REPOS = 15
README_LIMIT = 2000
RECENT_STARS = 30
MAX_CALLS = 80
MAX_EXAMPLES = 60
HUMAN_LABELS = {"gold", "batch", "proposal", "spot_check", "rejection"}
OUTPUT_KEYS = {"verdict", "reason", "confidence"}

SYSTEM = """exocortex 是一个研究知识库，目的是给领域 researcher 方向 insight：下一个值得做的方向、未解决的问题、可证伪的预测。你决定一个工作（GitHub 仓库、论文、博客或模型页）值不值得收进这个库，也就是它能不能成为这类 insight 的证据或启发。
下面 human 的 star、在做的仓库与标注，帮你了解他关心什么，不必局限于此。只依据给的内容，不要猜。
只输出 JSON：{"verdict": "yes|no", "reason": "<一句：收它能给库带来什么，或为什么不值得>", "confidence": <0-1，对 verdict 的把握>}"""


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def feed_key(repo: str) -> str:
    return f"github.com/{repo}"


def repo_of(key: str) -> str | None:
    parts = key.split("/")
    return f"{parts[1]}/{parts[2]}" if parts[0] == "github.com" and len(parts) == 3 else None


def display(key: str) -> str:
    return key.removeprefix("github.com/")


def snapshot_name(key: str) -> str:
    repo = repo_of(key)
    return repo.replace("/", "__") if repo else re.sub(r"[^A-Za-z0-9]+", "_", key).strip("_")[:120]


def channel_rows(store: Path) -> list[dict]:
    """Company channel signals plus 3dgen_tracker's daily picks (`tracker/signals.jsonl`, same row shape, mounted read-only)."""
    return read_rows(store / "company" / "signals.jsonl") + read_rows(store / "tracker" / "signals.jsonl")


def aggregate(signals: list[dict], company: list[dict] = ()) -> dict:
    works = defaultdict(lambda: {"followers": set(), "kinds": set(), "trending": False, "channels": [],
                                 "url": None, "title": "", "published": None, "first_seen": None})
    for s in signals:
        if s["signal"] in SKIPPED_SIGNALS:
            continue
        w = works[feed_key(s["repo"])]
        if s["signal"] == "trending":
            w["trending"] = True
        elif s["actor"]:
            w["followers"].add(s["actor"])
            w["kinds"].add(s["signal"])
    for c in company:
        w = works[c["key"]]
        w["channels"].append({"entity": c["entity"], "type": c["type"]})
        w["url"] = w["url"] or c["url"]
        w["title"] = w["title"] or c.get("title") or ""
        w["published"] = w["published"] or c.get("published")
        w["first_seen"] = min(filter(None, (w["first_seen"], c.get("run_date"))), default=None)
    return works


def is_rising(w: dict) -> bool:
    return len(w["followers"]) >= 2 or w["trending"]


def is_fresh(w: dict, today: date) -> bool:
    """Works with a feed signal are always eligible; company-only works for 14 days after publication (or first seen)."""
    if w["followers"] or w["trending"]:
        return True
    day = w["published"] or w["first_seen"]
    return bool(day) and (today - date.fromisoformat(day[:10])).days <= COMPANY_FRESH_DAYS


def signal_parts(w: dict) -> list[str]:
    parts = [f"{len(w['followers'])} 位关注者 {' / '.join(sorted(w['kinds']))}"] if w["followers"] else []
    parts += ["GitHub trending"] if w["trending"] else []
    published = f"，发布于 {w['published']}" if w["published"] else ""
    return parts + [f"3dgen_tracker 精选{published}" if c["type"] == "tracker" else f"公司渠道 {c['entity']}（{c['type']}{published}）"
                    for c in w["channels"]]


def candidates(works: dict, judgments: list[dict], today: date) -> list[dict]:
    """Works judged yes: rising ones first (more followers first), then by confidence."""
    rows = []
    for j in judgments:
        w = works.get(j["key"])
        if w is None or j["verdict"] != "yes" or not is_fresh(w, today):
            continue
        repo = repo_of(j["key"])
        rows.append({"key": j["key"], "url": j["url"], "name": repo.split("/")[1] if repo else j["meta"].get("title") or j["key"],
                     "line": j["meta"]["description"], "signals": signal_parts(w), "rising": is_rising(w),
                     "followers": len(w["followers"]), "verdict": j["verdict"], "confidence": j["confidence"]})
    rows.sort(key=lambda r: (not r["rising"], -r["followers"] if r["rising"] else 0, -(r["confidence"] or 0), r["key"]))
    return rows


def clean_readme(markdown: str) -> str:
    text = re.sub(r"<!--.*?-->", " ", markdown, flags=re.S)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)|<[^>]+>", " ", text)
    text = html.unescape(re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text))
    lines = [re.sub(r"[ \t]+", " ", l).strip() for l in text.splitlines()]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def first_sentence(text: str) -> str:
    for line in text.splitlines():
        line = re.sub(r"[#*_`>|]", " ", line)
        line = re.sub(r"\s+", " ", line).strip(" -·:")
        if len(line) >= 12 and not line.lower().startswith(("http", "license", "news", "table of contents")):
            return line[:160]
    return ""


def recent_stars(store: Path) -> list[tuple[str, str]]:
    described = {}
    for p in sorted((store / "snapshots").glob("*/starred*.json")):
        for s in json.loads(p.read_text(encoding="utf-8")):
            described[feed_key(s["repo"]["full_name"])] = s["repo"].get("description") or ""
    rows = sorted(read_rows(store / "adoptions.jsonl"), key=lambda r: r["starred_at"], reverse=True)[:RECENT_STARS]
    return [(feed_key(r["repo"]), described.get(feed_key(r["repo"]), "")) for r in rows]


def human_examples(store: Path, described: dict) -> list[tuple[str, str]]:
    """Rejected URLs without fetched text stay labels but are never shown as bare keys."""
    latest = {}
    for l in sorted(read_rows(store / "labels.jsonl"), key=lambda l: l["at"]):
        if l["from"] in HUMAN_LABELS and (l["from"] != "rejection" or described.get(l["key"])):
            latest.pop(l["key"], None)
            latest[l["key"]] = l["label"]
    return list(latest.items())[-MAX_EXAMPLES:]


def own_repos(get, user: str, now: datetime) -> list[dict]:
    """The human's own public non-fork repos pushed in the last 90 days, newest first."""
    repos = [r for r in get(f"users/{user}/repos?type=owner&sort=pushed&per_page=100")
             if not r["fork"] and now - parse_time(r["pushed_at"]) <= timedelta(days=OWN_ACTIVE_DAYS)]
    rows = []
    for r in sorted(repos, key=lambda r: r["pushed_at"], reverse=True)[:MAX_OWN_REPOS]:
        raw = get(f"repos/{r['full_name']}/readme", raw=True)
        rows.append({"repo": r["full_name"], "pushed_at": r["pushed_at"], "fork": r["fork"],
                     "description": (r.get("description") or "").strip(), "readme": first_sentence(clean_readme(raw)) if raw else ""})
    return rows


def import_rejections(store: Path, path: Path, judgments: list[dict], get, fetch) -> int:
    """Each URL the human rejected in exocortex becomes a `no` label once; its text is fetched once and cached."""
    labels_path, texts_path = store / "labels.jsonl", store / "rejection_texts.json"
    labelled = {(l["key"], l["from"]) for l in read_rows(labels_path)}
    texts = json.loads(texts_path.read_text(encoding="utf-8")) if texts_path.exists() else {}
    described = {j["key"]: j["meta"]["description"] for j in judgments}
    rows = []
    for r in yaml.safe_load(path.read_text(encoding="utf-8")) or []:
        key = normalize(r["url"])
        if (key, "rejection") in labelled:
            continue
        labelled.add((key, "rejection"))
        rows.append({"key": key, "label": "no", "from": "rejection", "at": str(r["rejected"])})
        if key not in described and key not in texts:
            texts[key] = rejection_text(key, r["url"], get, fetch)
    append_rows(labels_path, rows)
    texts_path.write_text(json.dumps(texts, ensure_ascii=False), encoding="utf-8")
    return len(rows)


def rejection_text(key: str, url: str, get, fetch) -> str:
    """Empty when nothing can be fetched; the label is kept but never shown as an example."""
    try:
        if repo := repo_of(key):
            return ((get(f"repos/{repo}") or {}).get("description") or "").strip()
        raw, title = fetch(key, url)
        return (title or "").strip() or first_sentence(clean_readme(raw))
    except Exception:  # noqa: BLE001 - a missing text only drops the example
        return ""


def star_hits(labels: list[dict], judgments: list[dict]) -> dict:
    """Stars that came after the work was judged, and how many of those works had been judged yes."""
    judged = {j["key"]: j for j in judgments}
    hits = [judged[l["key"]]["verdict"] == "yes" for l in labels if l["from"] == "star" and l["key"] in judged
            and datetime.strptime(judged[l["key"]]["run"], "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc) < parse_time(l["at"])]
    return {"star_after_judge": len(hits), "judged_yes": sum(hits)}


def context_block(stars: list[tuple[str, str]], own: list[dict], examples: list[tuple[str, str]], described: dict, key: str) -> str:
    """The work under judgment never appears among its own examples."""
    def line(k, d):
        return f"- {display(k)}：{d}" if d else f"- {display(k)}"
    shown = [(k, label) for k, label in examples if k != key]
    text = f"## human 最近 star 的 {len(stars)} 个仓库（越靠前越新）\n" + "\n".join(line(k, d) for k, d in stars)
    text += "\n\n## human 最近 3 个月在做的仓库（越靠前越新）\n" + (
        "\n".join(line(feed_key(r["repo"]), " ".join(filter(None, (r["description"], r["readme"])))) for r in own) or "（无）")
    text += f"\n\n## human 标过的工作（最近 {len(shown)} 条）"
    for label in ("yes", "no"):
        text += f"\n{label}：\n" + ("\n".join(line(k, described.get(k, "")) for k, l in shown if l == label) or "（无）")
    return text


def build_messages(context: str, url: str, w: dict, meta: dict, body: str) -> list[dict]:
    if "stars" in meta:
        what = f"GitHub 仓库，{meta['language'] or '语言未知'}，{meta['stars']} star，创建于 {meta['created_at'][:10]}"
    else:
        what = f"发布于 {meta['published']}" if meta.get("published") else "发布日期未知"
    user = (f"{context}\n\n## 待判工作\n{url}（{what}）\n简介：{meta['description']}\n信号：{'；'.join(signal_parts(w))}\n"
            f"正文（去掉 HTML 与徽章，前 {README_LIMIT} 字）：\n{body[:README_LIMIT] if body else '（无正文）'}")
    return [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]


def parse_judgment(content: str) -> dict:
    data = json.loads(content)
    if not isinstance(data, dict) or not OUTPUT_KEYS - {"confidence"} <= set(data) <= OUTPUT_KEYS:
        raise ValueError(f"keys {sorted(data) if isinstance(data, dict) else type(data).__name__}")
    if data["verdict"] not in ("yes", "no"):
        raise ValueError(f"verdict {data['verdict']!r}")
    data.setdefault("confidence", None)
    if data["confidence"] is not None and (not isinstance(data["confidence"], (int, float)) or not 0 <= data["confidence"] <= 1):
        raise ValueError(f"confidence {data['confidence']!r}")
    return data


def github_get(token: str):
    def get(path: str, raw: bool = False):
        accept = "application/vnd.github.raw" if raw else "application/vnd.github+json"
        request = urllib.request.Request(f"{API}/{path}", headers={
            "Authorization": f"Bearer {token}", "Accept": accept, "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "exocortex-feed"})
        try:
            with urllib.request.urlopen(request, timeout=30) as resp:
                body = resp.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            raise
        return body.decode("utf-8", errors="replace") if raw else json.loads(body)
    return get


def page_fetch(evidence_dir: Path):
    def fetch(key: str, url: str) -> tuple[str, str | None]:
        from radar.judge import fetch_evidence

        meta = fetch_evidence({"key": key, "url": url}, evidence_dir)
        if (meta["error"] or "").startswith("http_4"):  # bot walls and gated pages never yield text; skip as no_text
            return "", meta["title"]
        if meta["error"]:
            raise RuntimeError(meta["error"])
        return (evidence_dir / meta["text_file"]).read_text(encoding="utf-8"), meta["title"]
    return fetch


def material(key: str, w: dict, get, fetch, now: datetime) -> tuple[str | None, dict | None, str | None, str]:
    """(skip reason, meta, raw text to snapshot, cleaned text). Network errors raise and are retried on the next run."""
    repo = repo_of(key)
    if repo:
        meta = get(f"repos/{repo}")
        if meta is None:
            return "gone", None, None, ""
        if now - parse_time(meta["created_at"]) > timedelta(days=MAX_AGE_DAYS):
            return "old", None, None, ""
        raw = get(f"repos/{repo}/readme", raw=True)
        text = clean_readme(raw) if raw else ""
        description = (meta.get("description") or "").strip()
        info = {"description": description or first_sentence(text), "description_from": "repo" if description else "readme",
                "stars": meta["stargazers_count"], "created_at": meta["created_at"], "language": meta.get("language")}
        return (None if info["description"] else "no_text"), info, raw, text
    if w["published"] and now - parse_time(f"{w['published'][:10]}T00:00:00Z") > timedelta(days=MAX_AGE_DAYS):
        return "old", None, None, ""
    raw, title = fetch(key, w["url"])
    text = clean_readme(raw)
    if not text:
        return "no_text", None, None, ""
    title = (title or w["title"] or "").strip()
    info = {"description": title or first_sentence(text), "description_from": "title" if title else "text",
            "title": title, "published": w["published"]}
    return None, info, raw, text


def run(store: Path, get, provider, model: str, run_id: str, now: datetime, fetch=None,
        user: str = "ZJLi2013", rejections: Path | None = None) -> dict:
    """`get(path, raw=False)` is a GitHub API GET returning JSON (or text when raw), None on 404;
    `fetch(key, url)` returns a page's (text, title); `rejections` is exocortex's wiki/search-rejections.yaml."""
    from radar.cost import openai_tokens, record
    from radar.judge import HTTP_RETRY_BUDGET, call_once

    started = time.time()
    spent = {"hit": 0, "miss": 0, "out": 0}
    snap = store / "snapshots" / run_id
    fetch = fetch or page_fetch(snap / "evidence")
    judgments_path, skipped_path, labels_path = store / "judgments.jsonl", store / "skipped.jsonl", store / "labels.jsonl"
    judgments = read_rows(judgments_path)
    judged = {j["key"] for j in judgments}
    skipped = {r["key"] for r in read_rows(skipped_path)}
    works = aggregate(read_rows(store / "signals.jsonl"), channel_rows(store))
    errors, calls, retries_left = [], 0, HTTP_RETRY_BUDGET
    new_rejections = import_rejections(store, rejections, judgments, get, fetch) if rejections else 0
    try:
        own = own_repos(get, user, now)
    except Exception as e:  # noqa: BLE001 - recorded in judge_runs, the verifier fails the run
        own = []
        errors.append(f"own repos: {e}")
    (store / "own_repos.json").write_text(json.dumps({"run": run_id, "repos": own}, ensure_ascii=False), encoding="utf-8")

    pending = []
    for key in sorted(works):
        if key in judged or key in skipped:
            continue
        try:
            reason, info, raw, text = material(key, works[key], get, fetch, now)
        except Exception as e:  # noqa: BLE001 - retried on the next run
            errors.append(f"{key}: fetch {e}")
            continue
        if reason:
            append_rows(skipped_path, [{"key": key, "reason": reason, "run": run_id}])
            skipped.add(key)
            continue
        pending.append((key, info, raw, text))

    texts_path = store / "rejection_texts.json"
    described = (json.loads(texts_path.read_text(encoding="utf-8")) if texts_path.exists() else {}) | {
        j["key"]: j["meta"]["description"] for j in judgments} | {key: info["description"] for key, info, _, _ in pending}
    stars, examples = recent_stars(store), human_examples(store, described)
    for key, info, raw, text in pending:
        if calls >= MAX_CALLS:
            errors.append(f"call budget {MAX_CALLS} reached")
            break
        w = works[key]
        url = w["url"] or f"https://{key}"
        context = context_block(stars, own, examples, described, key)
        messages = build_messages(context, url, w, info, text)
        name = snapshot_name(key)
        for sub in ("readme", "calls"):
            (snap / sub).mkdir(parents=True, exist_ok=True)
        if raw:
            (snap / "readme" / f"{name}.md").write_text(raw, encoding="utf-8")
        (snap / "calls" / f"{name}.request.json").write_text(
            json.dumps({"model": model, "messages": messages}, ensure_ascii=False, indent=1), encoding="utf-8")
        while True:
            calls += 1
            content, response, error = call_once(provider, messages, model)
            for k, v in openai_tokens((response or {}).get("usage") or {}).items():
                spent[k] += v
            if error is None:
                try:
                    verdict = parse_judgment(content)
                except (ValueError, json.JSONDecodeError) as e:
                    error = f"parse:{e}"
            if error and error.startswith(("http:", "parse:")) and retries_left > 0:
                retries_left -= 1
                time.sleep(2)
                continue
            break
        if response is not None:
            (snap / "calls" / f"{name}.response.json").write_text(json.dumps(response, ensure_ascii=False, indent=1), encoding="utf-8")
        if error:
            errors.append(f"{key}: {error}")
            continue
        row = {"key": key, "url": url, "run": run_id, "followers": len(w["followers"]), "kinds": sorted(w["kinds"]),
               "trending": w["trending"], "channels": w["channels"], "meta": info, "readme_sha": sha(raw) if raw else None,
               "context_sha": sha(context), "model": model, **verdict}
        append_rows(judgments_path, [row])
        judgments.append(row)
        judged.add(key)

    queue = candidates(works, judgments, now.date())
    (store / "candidates.json").write_text(json.dumps({"run": run_id, "works": queue}, ensure_ascii=False), encoding="utf-8")

    labelled = {(l["key"], l["from"]) for l in read_rows(labels_path)}
    new_stars = []
    for a in sorted(read_rows(store / "adoptions.jsonl"), key=lambda a: a["starred_at"]):
        if (feed_key(a["repo"]), "star") not in labelled:
            labelled.add((feed_key(a["repo"]), "star"))
            new_stars.append({"key": feed_key(a["repo"]), "label": "yes", "from": "star", "at": a["starred_at"]})
    append_rows(labels_path, new_stars)
    if calls:
        record(store, "judge", run_id, spent, now)

    row = {"run": run_id, "seconds": round(time.time() - started, 1), "calls": calls, "judged": len(judged),
           "skipped": len(skipped), "candidates": len(queue), "new_star_labels": len(new_stars),
           "new_rejection_labels": new_rejections, **star_hits(read_rows(labels_path), judgments), "errors": errors}
    append_rows(store / "judge_runs.jsonl", [row])
    return row


def main() -> int:
    from radar.judge import make_provider

    parser = argparse.ArgumentParser(description="Judge the works from the human's feed and the company channels")
    parser.add_argument("store")
    parser.add_argument("--rejections", type=Path, help="exocortex wiki/search-rejections.yaml")
    args = parser.parse_args()
    provider, model = make_provider()
    now = datetime.now(timezone.utc)
    row = run(Path(args.store), github_get(os.environ["GITHUB_TOKEN"]), provider, model,
              now.strftime("%Y%m%dT%H%M%SZ"), now, user=os.environ.get("GITHUB_USER", "ZJLi2013"), rejections=args.rejections)
    print(json.dumps(row, ensure_ascii=False))
    return 1 if row["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
