import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = "mallikarjunav"
URL = f"https://github.com/users/{USERNAME}/contributions"
OUTPUT = Path("data/contributions.json")


def number(value):
    if value is None:
        return 0

    match = re.search(r"\d+", str(value).replace(",", ""))
    return int(match.group()) if match else 0


def fetch():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(URL, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    days = []

    for cell in soup.select("td.ContributionCalendar-day"):
        date = cell.get("data-date")

        if not date:
            continue

        count = number(
            cell.get("data-count")
            or cell.get("data-level")
            or cell.get("aria-label")
        )

        level = number(cell.get("data-level"))

        days.append(
            {
                "date": date,
                "count": count,
                "level": min(level, 4)
            }
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "username": USERNAME,
        "days": days,
        "total": sum(day["count"] for day in days)
    }

    OUTPUT.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8"
    )

    print(f"Saved {len(days)} contribution days to {OUTPUT}")


if __name__ == "__main__":
    fetch()