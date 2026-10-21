import json
import time

import requests

from radar import judge

ITEMS = [
    {"url": "https://example.com/blog/robot", "key": "example.com/blog/robot"},
    {"url": "https://example.com/blog/gone", "key": "example.com/blog/gone"},
]
ARTICLE = b"<html><body><article><p>We release a robot manipulation policy trained on home data.</p>" \
          b"<p>It folds laundry and loads dishwashers.</p></article></body></html>"


class Resp:
    def __init__(self, body: bytes, status: int):
        self.content, self.status_code = body, status


class FakeProvider:
    """Replies are content strings, exceptions, or ("hang", seconds, content); consumed in order."""

    def __init__(self, replies):
        self.replies, self.last_response = list(replies), None

    def chat(self, messages, **kwargs):
        reply = self.replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        if isinstance(reply, tuple):
            time.sleep(reply[1])
            reply = reply[2]
        self.last_response = {"model": "fake-model", "choices": [{"message": {"content": reply}}]}
        return reply


def test_fetch_keeps_text_and_failed_fetches_as_evidence(tmp_path):
    pages = {"https://example.com/blog/robot": Resp(ARTICLE, 200), "https://example.com/blog/gone": Resp(b"", 404)}
    ok, gone = (judge.fetch_evidence(i, tmp_path, get=lambda u: pages[u]) for i in ITEMS)
    assert ok["error"] is None and "robot manipulation policy" in (tmp_path / ok["text_file"]).read_text(encoding="utf-8")
    assert gone["status"] == 404 and gone["error"] == "http_404" and gone["attempts"] == 2 and gone["text_chars"] == 0
    assert json.loads((tmp_path / "example_com_blog_gone.json").read_text(encoding="utf-8"))["error"] == "http_404"


def test_call_once_returns_content_or_a_typed_error():
    content, raw, error = judge.call_once(FakeProvider(['{"verdict": "yes"}']), [], "m")
    assert content == '{"verdict": "yes"}' and raw["model"] == "fake-model" and error is None
    assert judge.call_once(FakeProvider([requests.ConnectionError("down")]), [], "m")[2] == "http:ConnectionError"
    assert judge.call_once(FakeProvider([ValueError("empty")]), [], "m")[2] == "provider:empty"


def test_hung_call_times_out_and_its_late_answer_is_not_recorded(monkeypatch):
    monkeypatch.setattr(judge, "CALL_DEADLINE_SECONDS", 0.2)
    provider = FakeProvider([("hang", 0.5, "late")])
    content, raw, error = judge.call_once(provider, [], "m")
    time.sleep(0.5)
    assert content is None and raw is None and error == "http:Timeout"
