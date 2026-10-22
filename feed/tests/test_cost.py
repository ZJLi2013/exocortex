from datetime import datetime, timezone

import pytest

from radar import cost, feed_judge
from radar.daily import append_rows, read_rows
from test_feed_judge import NOW, RUN, Provider, fake_github, make_store

USAGE = {"prompt_tokens": 3000, "completion_tokens": 100, "prompt_cache_hit_tokens": 2000, "prompt_cache_miss_tokens": 1000}


def test_peak_hours_cost_double():
    tokens = {"hit": 1_000_000, "miss": 1_000_000, "out": 1_000_000}
    assert cost.cny(tokens, datetime.fromisoformat("2026-10-22T10:00:00+08:00")) == pytest.approx(10.04)
    assert cost.cny(tokens, datetime.fromisoformat("2026-10-22T07:30:00+08:00")) == pytest.approx(5.02)
    assert cost.cny(tokens, datetime.fromisoformat("2026-10-24T10:00:00+08:00")) == pytest.approx(5.02)


def test_judge_run_records_its_tokens_once(tmp_path):
    class Paid(Provider):
        def chat(self, messages, model, **params):
            content = super().chat(messages, model, **params)
            self.last_response = {"model": "fake", "usage": USAGE}
            return content

    store = make_store(tmp_path, [("star", "u1", "a/x"), ("star", "u1", "b/y")])
    feed_judge.run(store, fake_github({}, {}, []), Paid(), "m", RUN, NOW)
    feed_judge.run(store, fake_github({}, {}, []), Paid(), "m", "20261022T000000Z", NOW)
    [row] = read_rows(store / "cost.jsonl")
    assert (row["job"], row["hit"], row["miss"], row["out"]) == ("judge", 4000, 2000, 200)


def test_claude_tokens_sum_every_model_and_month_total_skips_other_months(tmp_path):
    result = {"modelUsage": {
        "deepseek-flash": {"inputTokens": 500, "cacheCreationInputTokens": 100, "cacheReadInputTokens": 9000, "outputTokens": 300},
        "small": {"inputTokens": 50, "outputTokens": 10}}}
    assert cost.claude_tokens(result) == {"hit": 9000, "miss": 650, "out": 310}
    append_rows(tmp_path / "cost.jsonl", [
        {"job": "judge", "at": "2026-09-30T23:00:00+08:00", "cny": 5.0},
        {"job": "judge", "at": "2026-10-01T07:00:00+08:00", "cny": 0.25},
        {"job": "balance", "at": "2026-10-01T07:00:00+08:00", "balance_cny": 100.0},
        {"job": "ingest", "at": "2026-10-21T23:30:00+00:00", "cny": 0.5}])
    assert cost.month_total(tmp_path, datetime(2026, 10, 22, tzinfo=timezone.utc)) == 0.75
