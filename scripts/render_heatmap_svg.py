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
    cell, gap, left, top = 11, 4, 36, 48
    columns = min(53, (last - start).days // 7 + 1)
    width, height = left + columns * (cell + gap) + 18, 190
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><rect width="100%" height="100%" rx="12" fill="#0d1117"/>', '<style>text{font-family:monospace;fill:#8b949e;font-size:11px}.day{opacity:0;animation:reveal .3s ease forwards}@keyframes reveal{to{opacity:1}}</style>', f'<text x="{left}" y="23" fill="#c9d1d9">{data["username"]} · contributions in the last year</text>']
    seen_months = set()
    for week in range(columns):
        week_start = date.fromordinal(start.toordinal() + week * 7)
        month_key = (week_start.year, week_start.month)
        if month_key not in seen_months:
            seen_months.add(month_key)
            parts.append(f'<text x="{left + week * (cell + gap)}" y="40">{week_start.strftime("%b")}</text>')
    for weekday, label in ((0, "Sun"), (2, "Tue"), (4, "Thu")):
        parts.append(f'<text x="7" y="{top + weekday * (cell + gap) + 9}">{label}</text>')
    for week in range(columns):
        for row in range(7):
            current = date.fromordinal(start.toordinal() + week * 7 + row)
            record = by_date.get(current.isoformat())
            if record is None:
                continue
            weekday = (current.weekday() + 1) % 7
            x, y = left + week * (cell + gap), top + weekday * (cell + gap)
            level = max(0, min(4, int(record["level"])))
            delay = (week + weekday) * 0.018
            title = f'{record["count"]} contributions on {record["date"]}'
            parts.append(f'<rect class="day" x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{PALETTE[level]}" style="animation-delay:{delay:.3f}s"><title>{title}</title></rect>')
    total = sum(int(day["count"]) for day in days)
    footer_y = height - 14
    parts.append(f'<text x="{left}" y="{footer_y}" fill="#c9d1d9">{total:,} contributions</text><text x="{width - 114}" y="{footer_y}">Less</text>')
    for i, color in enumerate(PALETTE):
        parts.append(f'<rect x="{width - 79 + i * 14}" y="{height - 24}" width="10" height="10" rx="2" fill="{color}"/>')
    parts.append("</svg>")
    Path("contrib-heatmap.svg").write_text("\n".join(parts), encoding="utf-8")
    print("Generado contrib-heatmap.svg")


if __name__ == "__main__":
    main()
