"""Score an answers file against the query set in docs/mvp.md (t2 acceptance)."""

import re
import sys
from pathlib import Path

RSI_TRACK = "raw/agent_loop/research-rsi-track.md"
ROBOTRSI = "raw/robotrsi/"

# question -> (path substrings that must be cited, keywords that must appear)
GOLD = {
    "Q1": ([RSI_TRACK, ROBOTRSI], ["RSIGym", "EmbodiedRSI", "EmbodiedEvo", "ASPIRE", "RAX"]),
    "Q2": (["raw/robotrsi/works/gemini-argon.md"], ["56%", "75%"]),
    "Q3": ([RSI_TRACK, ROBOTRSI], ["AlphaEvolve", "RSIGym", "Argon"]),
    "Q4": ([RSI_TRACK, ROBOTRSI], ["RSIGym", "ScienceDiscovery", "EmbodiedEvo", "Argon", "RAX"]),
    "Q5": ([RSI_TRACK, ROBOTRSI], ["56.26", "autoresearch", "Agent Laboratory", "RSIAgent"]),
}
PASS_AT = 4


def main() -> None:
    text = Path(sys.argv[1]).read_text(encoding="utf-8").replace("\\", "/")
    sections = dict(re.findall(r"^## (Q\d)\b(.*?)(?=^## Q\d\b|\Z)", text, flags=re.M | re.S))
    passed = 0
    for q, (paths, keywords) in GOLD.items():
        body = sections.get(q, "")
        missing = [p for p in paths if p not in body] + [k for k in keywords if k.lower() not in body.lower()]
        passed += not missing
        print(f"{q}: " + ("pass" if not missing else "missing " + ", ".join(missing)))
    print(f"{passed}/{len(GOLD)} passed (need {PASS_AT})")
    sys.exit(0 if passed >= PASS_AT else 1)


if __name__ == "__main__":
    main()
