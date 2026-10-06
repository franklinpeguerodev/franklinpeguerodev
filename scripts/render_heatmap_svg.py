"""Render the cached public contribution calendar as an animated SVG."""
import json
from datetime import date
from pathlib import Path

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]


def main() -> None:
    source = Path("data/contributions.json")
    data = json.loads(source.read_text(encoding="utf-8"))
    days = data["days"]
    if not days:
        raise SystemExit("El archivo de contribuciones no contiene días.")
    # Align the rolling year to Sunday and cap the view at the latest 53 weeks.
    first = date.fromisoformat(days[0]["date"])
    start = date.fromordinal(first.toordinal() - (first.weekday() + 1) % 7)
    last = date.fromisoformat(days[-1]["date"])
    by_date = {item["date"]: item for item in days}
    cell, gap, left, top = 11, 4, 42, 36
    columns = min(53, (last - start).days // 7 + 1)
    width, height = 42 + columns * (cell + gap), 150
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><rect width="100%" height="100%" rx="12" fill="#0d1117"/>', '<style>text{font-family:monospace;fill:#8b949e;font-size:11px}.day{opacity:0;animation:reveal .3s ease forwards}@keyframes reveal{to{opacity:1}}</style>', f'<text x="{left}" y="20">{data["username"]} · contributions in the last year</text>']
    for week in range(columns):
        for weekday in range(7):
            current = date.fromordinal(start.toordinal() + week * 7 + weekday)
            record = by_date.get(current.isoformat())
            if record is None:
                continue
            x, y = left + week * (cell + gap), top + weekday * (cell + gap)
            level = max(0, min(4, int(record["level"])))
            delay = (week + weekday) * 0.018
            title = f'{record["count"]} contributions on {record["date"]}'
            parts.append(f'<rect class="day" x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{PALETTE[level]}" style="animation-delay:{delay:.3f}s"><title>{title}</title></rect>')
    total = sum(int(day["count"]) for day in days)
    parts.append(f'<text x="{left}" y="{height - 14}">{total:,} contributions</text><text x="{width - 110}" y="{height - 14}">Less</text>')
    for i, color in enumerate(PALETTE):
        parts.append(f'<rect x="{width - 78 + i * 14}" y="{height - 24}" width="10" height="10" rx="2" fill="{color}"/>')
    parts.append("</svg>")
    Path("contrib-heatmap.svg").write_text("\n".join(parts), encoding="utf-8")
    print("Generado contrib-heatmap.svg")


if __name__ == "__main__":
    main()
