import json

from radar.daily import read_rows, run

TYPES = {"star": "STARRED_REPOSITORY", "create": "CREATED_REPOSITORY", "recommended": "REPOSITORY_RECOMMENDATION",
         "pr": "MERGED_PULL_REQUEST"}


def card(signal, actor, repo, at, sub=None):
    meta = json.dumps({"feed_card": {"card_type": TYPES[signal], "created_at": at, "record_id": 1,
                                     "card_sub_position": sub}}, separators=(",", ":")).replace('"', "&quot;")
    user = f'<a data-hovercard-type="user" href="/{actor}">{actor}</a>' if actor and not sub else ""
    return (f'<div class="js-feed-item-component x" data-hydro-view="{meta}">{user}'
            f'<a data-hovercard-type="repository" href="/{repo}">{repo}</a></div>')


def page(*cards):
    return "<div>" + "".join(cards) + "</div>"


# Newest first, as the feed serves them; P3 holds the newest card round 1 sees.
P1 = page(card("star", "alice", "a/new1", "2026-10-22T08:00:00-07:00"),
          card("recommended", None, "g/pick", "2026-10-19T17:00:00-07:00"),
          card("pr", "bob", "b/pr", "2026-10-22T07:00:00-07:00"))
P2 = page(card("create", "bob", "b/new2", "2026-10-22T05:00:00-07:00"),
          card("star", "carol", "c/first", "2026-10-22T04:00:00-07:00"),
          card("star", "carol", "c/second", "2026-10-22T03:59:00-07:00", sub=1))
P3 = page(card("star", "dave", "d/old1", "2026-10-21T10:00:00-07:00"))
P4 = page(card("star", "erin", "e/old2", "2026-10-21T06:00:00-07:00"),
          card("recommended", None, "g/pick", "2026-10-19T17:00:00-07:00"))
P5 = page(card("star", "frank", "f/old3", "2026-10-21T02:00:00-07:00"))
A = {"repo": {"full_name": "x/a"}, "starred_at": "2026-10-21T09:00:00Z"}
B = {"repo": {"full_name": "x/b"}, "starred_at": "2026-10-22T07:00:00Z"}


def pages(*ps):
    return lambda n: ps[n - 1] if n <= len(ps) else page()


def stars(*ss):
    return lambda n: list(ss) if n == 1 else []


def keys(rows):
    return sorted(((r["actor"] or ""), r["repo"]) for r in rows)


def test_three_rounds_write_each_signal_and_star_once(tmp_path):
    r1 = run(tmp_path, pages(P3, P4, P5), stars(A), "r1", "cron")
    assert keys(read_rows(tmp_path / "signals.jsonl")) == [("", "g/pick"), ("dave", "d/old1"), ("erin", "e/old2"),
                                                          ("frank", "f/old3")]
    assert (r1["new_signals"], r1["new_adoptions"], r1["gap"], r1["errors"]) == (4, 1, False, [])

    r2 = run(tmp_path, pages(P1, P2, P3, P4, P5), stars(B, A), "r2", "cron")
    new = [r for r in read_rows(tmp_path / "signals.jsonl") if r["run"] == "r2"]
    assert keys(new) == [("alice", "a/new1"), ("bob", "b/new2"), ("carol", "c/first"), ("carol", "c/second")]
    assert [r["repo"] for r in read_rows(tmp_path / "adoptions.jsonl") if r["run"] == "r2"] == ["x/b"]
    assert (r2["pages"], r2["gap"]) == (3, False)

    r3 = run(tmp_path, pages(P1, P2, P3, P4, P5), stars(B, A), "r3", "cron")
    assert (r3["new_signals"], r3["new_adoptions"]) == (0, 0)
    assert len(read_rows(tmp_path / "signals.jsonl")) == 8 and len(read_rows(tmp_path / "adoptions.jsonl")) == 2


def test_cursor_older_than_the_feed_is_a_gap(tmp_path):
    run(tmp_path, pages(P5), stars(), "r1", "cron")
    row = run(tmp_path, pages(P1, P2), stars(), "r2", "cron")
    assert row["gap"] is True and row["errors"] == []


def test_login_page_instead_of_cards_is_an_error(tmp_path):
    row = run(tmp_path, pages("<html>Sign in to GitHub</html>"), stars(), "r1", "cron")
    assert row["errors"] and row["new_signals"] == 0
