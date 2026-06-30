"""Regenerate site/data.json from data/conferences.yml.

For each conference this computes the countdown, status, and -7/-14 day alert
windows relative to today, and checks whether its website is reachable. The
result is written to site/data.json, which the dashboard reads.

Run: python scripts/update.py
"""

from datetime import date, datetime, timezone
from pathlib import Path
import json
import urllib.request
import urllib.error

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "conferences.yml"
OUTPUT_FILE = ROOT / "site" / "data.json"

# A deadline this many days out or fewer (and not past) counts as "Upcoming".
UPCOMING_WINDOW_DAYS = 120
LINK_TIMEOUT_SECONDS = 15


def parse_date(value):
    """Return a date for an ISO 'YYYY-MM-DD' value, or None for 'TBD'/blank.

    PyYAML already turns bare YYYY-MM-DD values into date objects; strings and
    dates are both accepted here.
    """
    if isinstance(value, date):
        return value
    if not value or str(value).strip().upper() == "TBD":
        return None
    return datetime.strptime(str(value).strip(), "%Y-%m-%d").date()


def as_text(value):
    """Render a date or string field as a plain string for JSON output."""
    if isinstance(value, date):
        return value.isoformat()
    return str(value) if value else "TBD"


def classify(deadline, today):
    """Map a deadline date to a status bucket and a days-left integer."""
    if deadline is None:
        return "TBD", None
    days_left = (deadline - today).days
    if days_left < 0:
        return "Past Due", days_left
    if days_left <= UPCOMING_WINDOW_DAYS:
        return "Upcoming", days_left
    return "Far Out", days_left


def check_link(url):
    """Return (ok, status) for a URL. ok is False when it is unreachable."""
    request = urllib.request.Request(
        url,
        method="GET",
        headers={"User-Agent": "biomedical-ai-conference-tracker/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=LINK_TIMEOUT_SECONDS) as response:
            return True, response.status
    except urllib.error.HTTPError as error:
        # The server answered, just not with 2xx. 403/405 usually means the page
        # exists but blocks bots, so treat those as reachable.
        ok = error.code in (403, 405)
        return ok, error.code
    except urllib.error.URLError:
        return False, None


def build_record(entry, today):
    deadline = parse_date(entry.get("submission_deadline"))
    status, days_left = classify(deadline, today)
    link_ok, link_status = check_link(entry["url"])

    return {
        "name": entry["name"],
        "acronym": entry["acronym"],
        "track": entry.get("track", ""),
        "location": entry.get("location", "TBD"),
        "submission_deadline": as_text(entry.get("submission_deadline")),
        "deadline_confidence": entry.get("deadline_confidence", "tbd"),
        "notification_date": as_text(entry.get("notification_date")),
        "conference_date": as_text(entry.get("conference_date")),
        "url": entry["url"],
        "notes": entry.get("notes", ""),
        "status": status,
        "days_left": days_left,
        "alert_7": days_left is not None and 0 <= days_left <= 7,
        "alert_14": days_left is not None and 0 <= days_left <= 14,
        "link_ok": link_ok,
        "link_status": link_status,
    }


def main():
    today = date.today()
    conferences = yaml.safe_load(DATA_FILE.read_text())["conferences"]
    records = [build_record(entry, today) for entry in conferences]

    # Sort so the most urgent upcoming deadlines come first, TBD next, past last.
    order = {"Upcoming": 0, "Far Out": 1, "TBD": 2, "Past Due": 3}
    records.sort(key=lambda r: (order[r["status"]], r["days_left"] if r["days_left"] is not None else 10**6))

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "count": len(records),
        "broken_links": [r["acronym"] for r in records if not r["link_ok"]],
        "conferences": records,
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(payload, indent=2))
    return payload


if __name__ == "__main__":
    main()
