import json
import re
from datetime import datetime, timezone

import pytest

from radar import collect, feed_judge
from radar.daily import append_rows, read_rows
from radar.verify import check_feed_judge

NOW = datetime(2026, 10, 21, tzinfo=timezone.utc)
RUN = "20261021T000000Z"
FRESH = {"created_at": "2026-10-10T00:00:00Z", "description": "desc", "stargazers_count": 1, "language": "Python"}
OWN = [{"full_name": "me/stale", "fork": False, "pushed_at": "2026-05-01T00:00:00Z", "description": "Old"},
       {"full_name": "me/active", "fork": False, "pushed_at": "2026-10-01T00:00:00Z", "description": "My robot repo"},
       {"full_name": "me/forked", "fork": True, "pushed_at": "2026-10-20T00:00:00Z", "description": "Fork"}]


class Provider:
    def __init__(self, yes=()):
        self.yes, self.calls, self.prompts, self.last_response = set(yes), [], {}, None

    def chat(self, messages, model, **params):
        work = re.search(r"## 待判工作\nhttps://(?:github\.com/)?(\S+?)（", messages[1]["content"]).group(1)
        self.calls.append(work)
        self.prompts[work] = messages[1]["content"]
        self.last_response = {"model": "fake", "usage": {}}
        return json.dumps({"verdict": "yes" if work in self.yes else "no", "reason": "r", "confidence": 0.9})


def make_store(tmp_path, signals, stars=(), company=()):
    store = tmp_path / "store"
    (store / "company").mkdir(parents=True)
    append_rows(store / "signals.jsonl", [{"signal": s, "actor": a, "repo": r, "at": "2026-10-20T00:00:00Z", "run": "r0"}
                                          for s, a, r in signals])
    append_rows(store / "adoptions.jsonl", [{"repo": r, "starred_at": f"2026-10-2{i}T00:00:00Z", "run": "r0"}
                                            for i, r in enumerate(stars)])
    append_rows(store / "company" / "signals.jsonl", [
        {"key": k, "url": f"https://{k}", "title": t, "published": p, "entity": e, "type": "rss", "run_date": "2026-10-20"}
        for k, t, p, e in company])
    append_rows(store / "company" / "collect_runs.jsonl", [{"run_date": d, "new_signals": 0} for d in ("2026-10-20", "2026-10-21")])
    return store


def fake_github(metas, readmes, seen):
    def get(path, raw=False):
        if path.startswith("users/"):
            return OWN
        repo = path.removeprefix("repos/").removesuffix("/readme")
        seen.append(repo)
        return readmes.get(repo) if raw else metas.get(repo, FRESH)
    return get


def fake_pages(pages):
    return lambda key, url: pages[key]


def label(key, value, source, at):
    return {"key": key, "label": value, "from": source, "at": at}


def test_feed_and_company_works_filtered_judged_and_queued(tmp_path):
    store = make_store(tmp_path, [
        ("star", "u1", "a/rising"), ("star", "u2", "a/rising"), ("trending", None, "b/trend"),
        ("star", "u1", "c/one"), ("star", "u1", "d/old"), ("star", "u1", "e/notext"),
        ("recommended", None, "f/rec"), ("fork", "u1", "u1/fork")],
        company=[("lab.org/blog/robot", "Robot post", "2026-10-15", "lab"),
                 ("lab.org/blog/ancient", "Old post", "2025-01-01", "lab"),
                 ("lab.org/blog/empty", "", "2026-10-15", "lab"),
                 ("github.com/c/one", "one", "2026-10-10", "lab")])
    metas = {"c/one": FRESH | {"description": None}, "d/old": FRESH | {"created_at": "2025-01-01T00:00:00Z"},
             "e/notext": FRESH | {"description": ""}}
    readmes = {"a/rising": "# A\n\nRising work.", "c/one": "<p><img src='x'></p>\n# C one\n\nA tool for robot learning."}
    pages = {"lab.org/blog/robot": ("<p>A robot policy that folds laundry.</p>", None), "lab.org/blog/empty": ("", None)}
    seen, provider = [], Provider(yes={"lab.org/blog/robot", "c/one"})
    row = feed_judge.run(store, fake_github(metas, readmes, seen), provider, "m", RUN, NOW, fetch=fake_pages(pages))

    judged = {j["key"]: j for j in read_rows(store / "judgments.jsonl")}
    assert sorted(judged) == ["github.com/a/rising", "github.com/b/trend", "github.com/c/one", "lab.org/blog/robot"]
    assert {s["key"]: s["reason"] for s in read_rows(store / "skipped.jsonl")} == {
        "github.com/d/old": "old", "github.com/e/notext": "no_text", "lab.org/blog/ancient": "old", "lab.org/blog/empty": "no_text"}
    assert "f/rec" not in seen and "u1/fork" not in seen
    assert (judged["github.com/c/one"]["meta"]["description"], judged["github.com/c/one"]["meta"]["description_from"]) == (
        "A tool for robot learning.", "readme")
    assert judged["lab.org/blog/robot"]["meta"]["description"] == "Robot post"
    assert "公司渠道 lab（rss，发布于 2026-10-10）" in provider.prompts["c/one"] and "1 位关注者 star" in provider.prompts["c/one"]
    queue = json.loads((store / "candidates.json").read_text(encoding="utf-8"))["works"]
    assert [c["key"] for c in queue] == ["github.com/a/rising", "github.com/b/trend", "github.com/c/one", "lab.org/blog/robot"]
    assert (store / "snapshots" / RUN / "readme" / "a__rising.md").exists()
    assert row["errors"] == []
    assert check_feed_judge(store) == []


def test_human_labels_are_examples_but_never_for_their_own_work(tmp_path):
    store = make_store(tmp_path, [("star", "u1", "a/x"), ("star", "u1", "b/y")])
    append_rows(store / "labels.jsonl", [label("github.com/a/x", "yes", "gold", "2026-10-20T00:00:00+08:00"),
                                         label("github.com/b/y", "no", "gold", "2026-10-20T00:00:00+08:00"),
                                         label("github.com/z/z", "yes", "star", "2026-10-20T00:00:00Z")])
    provider = Provider()
    feed_judge.run(store, fake_github({"b/y": FRESH | {"description": "B does things"}}, {}, []), provider, "m", RUN, NOW)
    examples = provider.prompts["a/x"].split("## 待判工作")[0]
    assert "a/x" not in examples and "no：\n- b/y：B does things" in examples and "z/z" not in examples
    assert "b/y" not in provider.prompts["b/y"].split("## 待判工作")[0]


def test_second_run_judges_nothing_and_star_labels_once(tmp_path):
    store = make_store(tmp_path, [("star", "u1", "a/x"), ("create", "u2", "b/y")], stars=["a/x", "z/z"])
    provider = Provider()
    for run_id in (RUN, "20261022T000000Z"):
        feed_judge.run(store, fake_github({}, {"a/x": "# A x readme"}, []), provider, "m", run_id, NOW)
    assert sorted(provider.calls) == ["a/x", "b/y"]
    assert len(read_rows(store / "judgments.jsonl")) == 2
    assert sorted((l["key"], l["from"]) for l in read_rows(store / "labels.jsonl")) == [
        ("github.com/a/x", "star"), ("github.com/z/z", "star")]


def test_company_only_works_leave_the_queue_after_14_days(tmp_path):
    store = make_store(tmp_path, [("star", "u1", "a/both")], company=[
        ("lab.org/p/fresh", "Fresh", "2026-10-10", "lab"), ("lab.org/p/stale", "Stale", "2026-10-01", "lab"),
        ("github.com/a/both", "Both", "2026-09-01", "lab")])
    append_rows(store / "company" / "signals.jsonl", [
        {"key": k, "url": f"https://{k}", "title": k, "published": None, "entity": "lab", "type": "page", "run_date": d}
        for k, d in (("lab.org/p/new", "2026-10-15"), ("lab.org/p/undated", "2026-10-01"))])
    pages = {k: ("<p>A robot post.</p>", None) for k in ("lab.org/p/fresh", "lab.org/p/stale", "lab.org/p/new", "lab.org/p/undated")}
    provider = Provider(yes={"a/both", *pages})
    feed_judge.run(store, fake_github({}, {}, []), provider, "m", RUN, NOW, fetch=fake_pages(pages))
    assert len(read_rows(store / "judgments.jsonl")) == 5
    queue = json.loads((store / "candidates.json").read_text(encoding="utf-8"))["works"]
    assert sorted(c["key"] for c in queue) == ["github.com/a/both", "lab.org/p/fresh", "lab.org/p/new"]
    assert check_feed_judge(store) == []


def test_own_active_repos_enter_the_context(tmp_path):
    store = make_store(tmp_path, [("star", "u1", "a/x")])
    provider = Provider()
    feed_judge.run(store, fake_github({}, {"me/active": "# Active\n\nA harness for robot policies."}, []), provider, "m", RUN, NOW)
    own = json.loads((store / "own_repos.json").read_text(encoding="utf-8"))["repos"]
    assert [r["repo"] for r in own] == ["me/active"]
    assert "## human 最近 3 个月在做的仓库（越靠前越新）\n- me/active：My robot repo A harness for robot policies." in provider.prompts["a/x"]
    assert check_feed_judge(store) == []


def test_rejections_become_no_labels_once_and_examples_only_with_text(tmp_path):
    store = make_store(tmp_path, [("star", "u1", "a/x"), ("star", "u1", "b/judged")])
    feed_judge.run(store, fake_github({"b/judged": FRESH | {"description": "Judged repo"}}, {}, []), Provider(), "m", RUN, NOW)
    rejections = tmp_path / "search-rejections.yaml"
    rejections.write_text("- url: https://arxiv.org/abs/2610.00001v2\n  rejected: 2026-10-20\n"
                          "- url: https://lab.org/bad/\n  rejected: 2026-10-20\n"
                          "- url: https://github.com/b/judged\n  rejected: 2026-10-21\n", encoding="utf-8")
    append_rows(store / "signals.jsonl", [{"signal": "star", "actor": "u1", "repo": "c/new", "at": "x", "run": "r1"}])
    fetched, provider = [], Provider()

    def fetch(key, url):
        fetched.append(key)
        if key == "lab.org/bad":
            raise RuntimeError("http_502")
        return "<p>body</p>", "A paper title"
    for run_id in ("20261022T000000Z", "20261023T000000Z"):
        row = feed_judge.run(store, fake_github({}, {}, []), provider, "m", run_id, NOW, fetch=fetch, rejections=rejections)
    assert fetched == ["arxiv.org/abs/2610.00001", "lab.org/bad"] and row["new_rejection_labels"] == 0
    assert sorted(l["key"] for l in read_rows(store / "labels.jsonl") if l["from"] == "rejection") == [
        "arxiv.org/abs/2610.00001", "github.com/b/judged", "lab.org/bad"]
    examples = provider.prompts["c/new"].split("## 待判工作")[0]
    assert "- arxiv.org/abs/2610.00001：A paper title" in examples and "- b/judged：Judged repo" in examples
    assert "lab.org/bad" not in examples
    assert check_feed_judge(store, rejections) == []
    rejections.write_text(rejections.read_text(encoding="utf-8") + "- url: https://lab.org/new\n  rejected: 2026-10-22\n", encoding="utf-8")
    assert any("rejection labels differ" in p for p in check_feed_judge(store, rejections))


def test_star_hit_rate_counts_stars_after_judgment(tmp_path):
    store = make_store(tmp_path, [("star", "u1", "a/x"), ("star", "u1", "b/y")])
    feed_judge.run(store, fake_github({}, {}, []), Provider(yes={"a/x"}), "m", RUN, NOW)
    append_rows(store / "adoptions.jsonl", [{"repo": r, "starred_at": t, "run": "r1"} for r, t in (
        ("a/x", "2026-10-22T00:00:00Z"), ("b/y", "2026-10-23T00:00:00Z"), ("c/z", "2026-10-20T00:00:00Z"))])
    row = feed_judge.run(store, fake_github({}, {}, []), Provider(), "m", "20261024T000000Z", NOW)
    assert (row["star_after_judge"], row["judged_yes"]) == (2, 1)
    assert check_feed_judge(store) == []


def test_unjudged_work_and_repo_keyed_rows_fail_the_check(tmp_path):
    store = make_store(tmp_path, [("star", "u1", "a/x")])
    feed_judge.run(store, fake_github({}, {}, []), Provider(), "m", RUN, NOW)
    append_rows(store / "signals.jsonl", [{"signal": "star", "actor": "u3", "repo": "c/new", "at": "x", "run": "r9"}])
    assert any("neither judged nor skipped" in p for p in check_feed_judge(store))
    append_rows(store / "labels.jsonl", [{"repo": "a/x", "label": "no", "from": "proposal", "at": "x"}])
    assert any("not keyed by work" in p for p in check_feed_judge(store))


def test_company_signals_accumulate_across_overwritten_runs(tmp_path):
    items, signals = tmp_path / "items.jsonl", tmp_path / "signals.jsonl"
    item = {"url": "https://lab.org/p/", "key": "lab.org/p", "title": "P", "published": "2026-10-14T08:00:00+00:00",
            "sources": [{"entity": "lab", "type": "rss"}]}
    items.write_text(json.dumps(item) + "\n", encoding="utf-8")
    assert collect.append_signals(items, signals, "2026-10-20") == 1
    items.write_text(json.dumps(item | {"key": "lab.org/q", "url": "https://lab.org/q/"}) + "\n" + json.dumps(item) + "\n",
                     encoding="utf-8")
    assert collect.append_signals(items, signals, "2026-10-21") == 1
    assert [(r["key"], r["published"]) for r in read_rows(signals)] == [("lab.org/p", "2026-10-14"), ("lab.org/q", "2026-10-14")]
    assert len(read_rows(tmp_path / "collect_runs.jsonl")) == 2


@pytest.mark.parametrize("error, outcome", [("http_403", ""), ("http_502", RuntimeError), ("ConnectionError", RuntimeError)])
def test_page_client_errors_yield_no_text_and_others_retry(tmp_path, monkeypatch, error, outcome):
    from radar import judge

    monkeypatch.setattr(judge, "fetch_evidence", lambda item, d: {"error": error, "title": None, "text_file": "x.txt"})
    fetch = feed_judge.page_fetch(tmp_path)
    if outcome is RuntimeError:
        with pytest.raises(RuntimeError):
            fetch("openai.com/index/x", "https://openai.com/index/x")
    else:
        assert fetch("openai.com/index/x", "https://openai.com/index/x") == ("", None)


def test_malformed_answer_is_asked_again(tmp_path, monkeypatch):
    class Flaky(Provider):
        def chat(self, messages, model, **params):
            answer = super().chat(messages, model, **params)
            return '{"verdict": "no"}' if len(self.calls) == 1 else answer
    monkeypatch.setattr(feed_judge.time, "sleep", lambda s: None)
    store = make_store(tmp_path, [("star", "u1", "a/x")])
    row = feed_judge.run(store, fake_github({}, {}, []), Flaky(), "m", RUN, NOW)
    assert (row["calls"], row["judged"], row["errors"]) == (2, 1, [])


@pytest.mark.parametrize("content", [
    '{"verdict": "maybe", "reason": "r", "confidence": 0.5}',
    '{"verdict": "yes", "lens": "jev", "reason": "r", "confidence": 0.5}',
    '{"verdict": "yes", "reason": "r", "confidence": 2}',
    '{"verdict": "yes", "confidence": 0.5}'])
def test_invalid_judgment_is_rejected(content):
    with pytest.raises(ValueError):
        feed_judge.parse_judgment(content)
