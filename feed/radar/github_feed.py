"""The human's github.com/feed, read with their session cookie. Standard library only."""
import html
import json
import re
import urllib.request

FEED = "https://github.com/conduit/for_you_feed?initial_per_page=5&page={page}&source=feed_page&button="
HEADERS = {"Accept": "text/html", "X-Requested-With": "XMLHttpRequest", "GitHub-Verified-Fetch": "true",
           "User-Agent": "exocortex-feed"}
CARD_START = re.compile(r'<[a-z-]+ [^>]*class="js-feed-item-component ')
FEED_CARD = re.compile(r'"feed_card":(\{.*?\})')
GITHUB_PICKS = {"REPOSITORY_RECOMMENDATION", "TRENDING_REPOSITORY"}
# Signals that a project is worth a look; pull requests, releases and follows are dropped.
SIGNALS = {"STARRED_REPOSITORY": "star", "CREATED_REPOSITORY": "create", "FORKED_REPOSITORY": "fork",
           "PRIVATE_TO_PUBLIC_REPOSITORY": "public", "ADDED_TO_LIST": "list",
           "TRENDING_REPOSITORY": "trending", "REPOSITORY_RECOMMENDATION": "recommended"}
HOVERCARD = re.compile(r'data-hovercard-type="(user|repository|organization)"[^>]*?href="/([^"?#]+)"'
                       r'|href="/([^"?#]+)"[^>]*?data-hovercard-type="(user|repository|organization)"')


def fetch_page(page: int, session: str) -> str:
    request = urllib.request.Request(FEED.format(page=page), headers=HEADERS | {"Cookie": f"user_session={session}"})
    with urllib.request.urlopen(request, timeout=30) as resp:
        return resp.read().decode("utf-8")


def parse_cards(page_html: str) -> list[dict]:
    """Project-signal cards: signal, time, the user who acted (None for GitHub's own picks) and the repository."""
    starts = [m.start() for m in CARD_START.finditer(page_html)] + [len(page_html)]
    cards, actor = [], None
    for begin, end in zip(starts, starts[1:]):
        chunk = page_html[begin:end]
        meta = FEED_CARD.search(html.unescape(chunk[:20000]))
        if not meta:
            continue
        card = json.loads(meta.group(1))
        users, repos = [], []
        for m in HOVERCARD.finditer(chunk):
            kind, path = (m.group(1), m.group(2)) if m.group(1) else (m.group(4), m.group(3))
            target = users if kind in ("user", "organization") else repos
            if path not in target:
                target.append(path)
        # A "starred 2 repositories" card is split into sub-cards; only the first links the user who starred.
        if not card.get("card_sub_position"):
            actor = None if card["card_type"] in GITHUB_PICKS else (users[0] if users else None)
        if card["card_type"] in SIGNALS and repos:
            cards.append({"id": card["record_id"], "signal": SIGNALS[card["card_type"]], "at": card["created_at"],
                          "actor": actor, "repo": repos[0]})
    return cards
