"""Page fetching and one DeepSeek call, shared by feed_judge."""

import copy
import gzip
import hashlib
import json
import os
import re
import threading
from datetime import datetime, timezone
from pathlib import Path

import requests
import trafilatura

HTTP_RETRY_BUDGET = 3
# requests' read timeout counts gaps between bytes; DeepSeek keep-alive bytes defeat it, so cap each call's wall time.
CALL_DEADLINE_SECONDS = 120
UA = {"User-Agent": "Mozilla/5.0 (compatible; exocortex-feed/0.1)"}


def evidence_url(item: dict) -> str:
    """Where the readable text of an item lives: README / card for repos, the page itself otherwise."""
    parts = item["key"].split("/")
    if parts[0] == "github.com" and len(parts) >= 3:
        return f"https://api.github.com/repos/{parts[1]}/{parts[2]}/readme"
    if parts[0] == "huggingface.co" and len(parts) >= 3 and parts[1] not in ("blog", "papers"):
        return f"https://huggingface.co/{'/'.join(parts[1:])}/raw/main/README.md"
    return item["url"]


def slug(key: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", key).strip("_")[:120]


def fetch_evidence(item: dict, evidence_dir: Path, get=None) -> dict:
    """Fetch once (retry once), keep the raw response, the extracted text and their hashes."""
    url = evidence_url(item)
    headers = {**UA}
    if url.startswith("https://api.github.com"):
        headers["Accept"] = "application/vnd.github.raw+json"
        if os.environ.get("GITHUB_TOKEN"):
            headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    get = get or (lambda u: requests.get(u, headers=headers, timeout=30))
    meta = {"key": item["key"], "request_url": url, "attempts": 0, "status": None, "error": None}
    body = b""
    for attempt in (1, 2):
        meta["attempts"] = attempt
        meta["fetched_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        try:
            resp = get(url)
        except requests.RequestException as exc:
            meta["error"] = type(exc).__name__
            continue
        meta["status"], body = resp.status_code, resp.content
        meta["error"] = None if resp.status_code < 400 else f"http_{resp.status_code}"
        if meta["error"] is None:
            break

    is_markdown = url.startswith("https://api.github.com") or url.endswith("README.md")
    text, title = "", None
    if body and meta["error"] is None:
        html_or_md = body.decode("utf-8", errors="replace")
        if not is_markdown:
            text = trafilatura.extract(html_or_md, url=url) or ""
            page_meta = trafilatura.extract_metadata(html_or_md)
            title = page_meta.title if page_meta else None
        else:
            text = html_or_md
    meta["title"] = title
    name = slug(item["key"])
    evidence_dir.mkdir(parents=True, exist_ok=True)
    (evidence_dir / f"{name}.raw.gz").write_bytes(gzip.compress(body))
    (evidence_dir / f"{name}.txt").write_text(text, encoding="utf-8")
    meta |= {"raw_file": f"{name}.raw.gz", "text_file": f"{name}.txt", "raw_sha256": hashlib.sha256(body).hexdigest(),
             "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(), "text_chars": len(text)}
    (evidence_dir / f"{name}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    return meta


def call_with_deadline(fn, seconds: float):
    """A hung call is abandoned on a daemon thread and reported as a timeout."""
    box = {}

    def target():
        try:
            box["value"] = fn()
        except BaseException as exc:
            box["error"] = exc

    thread = threading.Thread(target=target, daemon=True)
    thread.start()
    thread.join(seconds)
    if thread.is_alive():
        raise requests.Timeout(f"no answer within {seconds}s")
    if "error" in box:
        raise box["error"]
    return box["value"]


PARAMS = {"temperature": 0.0, "max_tokens": 400, "response_format": {"type": "json_object"}}


def call_once(provider, messages: list[dict], model: str):
    """One attempt: (content, raw response or None, error or None); errors are 'http:<Exc>' or 'provider:<msg>'."""
    # A fresh copy per call: an abandoned call that answers late must not overwrite this call's response.
    call = copy.copy(provider)
    call.last_response = None
    try:
        content = call_with_deadline(lambda: call.chat(messages, model=model, **PARAMS), CALL_DEADLINE_SECONDS)
        return content, call.last_response, None
    except requests.RequestException as exc:
        return None, call.last_response, f"http:{type(exc).__name__}"
    except ValueError as exc:  # truncated or empty answer from the provider
        return None, call.last_response, f"provider:{exc}"


def make_provider():
    from llm_provider.deepseek_provider import DeepSeekProvider

    model = os.environ.get("DEEPSEEK_MODEL", "deepseek-v4-flash")
    return DeepSeekProvider(api_key=os.environ["DEEPSEEK_API_KEY"], default_model=model, max_retries=0), model
