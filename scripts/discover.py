"""Best-effort discovery of biomedical AI venues not yet in your tracker.

The community ai-deadlines dataset stores one YAML file per venue, and each
file is a LIST of yearly editions:

    - title: MICCAI
      year: 2026
      full_name: International Conference on Medical Image Computing ...
      link: https://conferences.miccai.org/2026/
      tags: [computer-vision]
      deadlines:
        - type: abstract
          date: '2026-02-12 23:59:59'
        - type: paper
          date: '2026-02-26 23:59:59'

This reads those files, keeps venues whose text matches biomedical keywords,
drops anything you already track, and writes the single nearest upcoming
edition of each match to site/discovered.json for review. Nothing is added to
data/conferences.yml automatically.

Run: python scripts/discover.py
"""

from datetime import date, datetime
from pathlib import Path
import json
import urllib.request

import yaml

ROOT = Path(__file__).resolve().parent.parent
TRACKED_FILE = ROOT / "data" / "conferences.yml"
OUTPUT_FILE = ROOT / "site" / "discovered.json"

# GitHub API directory listing for the upstream dataset (one YAML per venue).
SOURCE_API = "https://api.github.com/repos/huggingface/ai-deadlines/contents/src/data/conferences"

KEYWORDS = [
    "medical", "biomedical", "imaging", "health", "healthcare", "clinical",
    "radiology", "pathology", "bioinformatics", "genomic", "cancer", "surgery",
    "miccai", "isbi", "ipmi", "midl",
]

# Deadline types worth surfacing, in order of preference.
PAPER_DEADLINE_TYPES = ("paper", "abstract")


def fetch_json(url):
    request = urllib.request.Request(
        url, headers={"User-Agent": "biomedical-ai-conference-tracker/1.0"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode())


def fetch_text(url):
    request = urllib.request.Request(
        url, headers={"User-Agent": "biomedical-ai-conference-tracker/1.0"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode()


def tracked_tokens():
    """Acronym base names already tracked, e.g. {'miccai', 'isbi', ...}."""
    tracked = yaml.safe_load(TRACKED_FILE.read_text())["conferences"]
    return {c["acronym"].split()[0].lower() for c in tracked}


def matches_biomedical(edition):
    """Return the first matching keyword for an edition, or None."""
    blob = " ".join(
        str(edition.get(field, "")) for field in ("title", "full_name", "tags")
    ).lower()
    return next((kw for kw in KEYWORDS if kw in blob), None)


def paper_deadline(edition):
    """Return the paper (preferred) or abstract deadline date, or None."""
    best = None
    for item in edition.get("deadlines", []) or []:
        if item.get("type") not in PAPER_DEADLINE_TYPES:
            continue
        try:
            parsed = datetime.strptime(str(item.get("date", ""))[:10], "%Y-%m-%d").date()
        except ValueError:
            continue
        if best is None or item.get("type") == "paper":
            best = parsed
    return best


def edition_year(edition):
    try:
        return int(edition.get("year", 0))
    except (TypeError, ValueError):
        return 0


def pick_edition(editions, today):
    """Pick the nearest upcoming edition; fall back to the latest year."""
    dated = [(paper_deadline(e), e) for e in editions]
    upcoming = [(dl, e) for dl, e in dated if dl is not None and dl >= today]
    if upcoming:
        return min(upcoming, key=lambda pair: pair[0])
    return max(dated, key=lambda pair: edition_year(pair[1]))


def main():
    today = date.today()
    already = tracked_tokens()
    listing = fetch_json(SOURCE_API)

    candidates = []
    for item in listing:
        if not item["name"].endswith((".yml", ".yaml")):
            continue
        editions = yaml.safe_load(fetch_text(item["download_url"]))
        if not isinstance(editions, list) or not editions:
            continue

        keyword = matches_biomedical(editions[0])
        if keyword is None:
            continue

        title = str(editions[0].get("title", ""))
        if title.lower() in already:
            continue

        deadline, edition = pick_edition(editions, today)
        candidates.append({
            "title": title,
            "full_name": edition.get("full_name", ""),
            "year": edition.get("year", ""),
            "submission_deadline": deadline.isoformat() if deadline else "TBD",
            "url": edition.get("link", ""),
            "matched_keyword": keyword,
        })

    candidates.sort(key=lambda c: c["submission_deadline"])
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps({"candidates": candidates}, indent=2))
    return candidates


if __name__ == "__main__":
    main()
