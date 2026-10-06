"""Fetch the public GitHub contribution calendar without an API token."""
from datetime import date
import json
from pathlib import Path
import re

import requests
from bs4 import BeautifulSoup

USERNAME = "franklinpeguerodev"


def main() -> None:
    url = f"https://github.com/users/{USERNAME}/contributions"
    response = requests.get(url, headers={"User-Agent": "profile-readme-generator"}, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    tooltips = {
        tooltip.get("for"): tooltip.get_text(" ", strip=True)
        for tooltip in soup.select("tool-tip[for]")
    }
    days = []
    for cell in soup.select("td[data-date]"):
        tooltip = tooltips.get(cell.get("id"), "")
        match = re.search(r"([\d,]+) contributions?", tooltip, re.IGNORECASE)
        count = int(match.group(1).replace(",", "")) if match else 0
        level = cell.get("data-level", "0")
        try:
            level = max(0, min(4, int(level)))
        except (TypeError, ValueError):
            level = 0
        days.append({"date": cell["data-date"], "count": count, "level": level})
    if not days:
        raise SystemExit("No se encontraron contribuciones; puede haber cambiado el HTML público de GitHub.")
    days.sort(key=lambda item: item["date"])
    output = Path("data/contributions.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"username": USERNAME, "updated": date.today().isoformat(), "days": days}, indent=2), encoding="utf-8")
    print(f"Guardados {len(days)} días en {output}")


if __name__ == "__main__":
    main()
