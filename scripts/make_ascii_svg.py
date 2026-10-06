"""Convert source-prepped.png into a monochrome, self-typing ASCII SVG."""
from pathlib import Path
import html
import math

from PIL import Image

RAMP = " .`:-=+*cs#%@"
COLS, ROWS = 76, 42
CELL_W, CELL_H = 10, 16


def main() -> None:
    source = Path("source-prepped.png")
    if not source.is_file():
        raise SystemExit("Falta source-prepped.png. Ejecuta primero scripts/prep_photo.py con tu foto.")
    image = Image.open(source).convert("L").resize((COLS, ROWS))
    pixels = list(image.getdata())
    lines = []
    for row in range(ROWS):
        chars = "".join(RAMP[min(len(RAMP) - 1, (255 - pixels[row * COLS + col]) * (len(RAMP) - 1) // 255)] for col in range(COLS))
        lines.append(chars)

    width, height = COLS * CELL_W + 24, ROWS * CELL_H + 24
    chunks = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" rx="12" fill="#0d1117"/><style>text{{font:14px monospace;fill:#c9d1d9}}</style>''']
    for i, line in enumerate(lines):
        y = 20 + (i + 1) * CELL_H
        delay = i * 0.055
        chunks.append(f'<clipPath id="row{i}"><rect x="12" y="{y - CELL_H + 2}" width="0" height="{CELL_H}"><animate attributeName="width" from="0" to="{COLS * CELL_W}" dur="0.75s" begin="{delay:.3f}s" fill="freeze"/></rect></clipPath>')
        chunks.append(f'<text x="12" y="{y}" clip-path="url(#row{i})">{html.escape(line)}</text>')
    chunks.append("</svg>")
    Path("avi-ascii.svg").write_text("\n".join(chunks), encoding="utf-8")
    print("Generado avi-ascii.svg")


if __name__ == "__main__":
    main()
