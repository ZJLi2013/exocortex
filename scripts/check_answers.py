"""Score an answers file against the query set below."""

import re
import sys
from pathlib import Path

WIKI = "wiki/"

# question -> (path substrings that must be cited, keywords that must appear)
GOLD = {
    "Q1": ([WIKI], ["AlphaEvolve", "EmbodiedRSI", "EmbodiedEvo", "ASPIRE", "RAX"]),
    "Q2": ([WIKI], ["56%", "75%"]),
    "Q3": ([WIKI], ["AlphaEvolve", "RSIGym", "Argon"]),
    "Q4": ([WIKI], ["EmbodiedRSI", "EmbodiedEvo", "RoboQuest", "Argon", "RSIGym", "SGS", "WorldScape"]),
    "Q5": ([WIKI], ["56.26", "Agent Laboratory", "RSIAgent"]),
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
