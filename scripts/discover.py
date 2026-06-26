"""Best-effort discovery of biomedical AI venues not yet in your tracker.

This reads the community-maintained ai-deadlines dataset, keeps entries whose
text matches biomedical keywords, drops anything you already track, and writes
the candidates to site/discovered.json for you to review.

It is intentionally non-authoritative: the dashboard shows these in a separate
"Discovered — review" panel. Nothing is added to data/conferences.yml
automatically; you copy across the ones you want.

Run: python scripts/discover.py
"""

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


def matches_biomedical(entry):
    blob = " ".join(
        str(entry.get(field, ""))
        for field in ("title", "full_name", "sub", "tags")
    ).lower()
    return next((kw for kw in KEYWORDS if kw in blob), None)


def main():
    already = tracked_tokens()
    listing = fetch_json(SOURCE_API)

    candidates = []
    for item in listing:
        if not item["name"].endswith((".yml", ".yaml")):
            continue
        entry = yaml.safe_load(fetch_text(item["download_url"]))
        if not isinstance(entry, dict):
            continue

        keyword = matches_biomedical(entry)
        if keyword is None:
            continue
        if str(entry.get("title", "")).lower() in already:
            continue

        candidates.append({
            "title": entry.get("title", ""),
            "full_name": entry.get("full_name", ""),
            "year": entry.get("year", ""),
            "submission_deadline": str(entry.get("deadline", "TBD")),
            "url": entry.get("link", ""),
            "matched_keyword": keyword,
        })

    candidates.sort(key=lambda c: (c["title"], str(c["year"])))
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps({"candidates": candidates}, indent=2))
    return candidates


if __name__ == "__main__":
    main()
