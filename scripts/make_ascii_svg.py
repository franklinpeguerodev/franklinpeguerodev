"""Convert source-prepped.png into a monochrome, self-typing ASCII SVG."""
from pathlib import Path
import html
import math

from PIL import Image

RAMP = "  .,:-=+*#%@"
COLS, ROWS = 76, 58
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
<defs>
  <linearGradient id="terminal-bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#0c281b"/><stop offset="1" stop-color="#07130d"/></linearGradient>
  <radialGradient id="portrait-halo"><stop stop-color="#31e58b" stop-opacity=".16"/><stop offset="1" stop-color="#31e58b" stop-opacity="0"/></radialGradient>
  <pattern id="terminal-stripes" width="12" height="8" patternUnits="userSpaceOnUse"><path d="M0 1H12" fill="none" stroke="#39d878" stroke-opacity=".14" stroke-width="1"/></pattern>
</defs>
<rect width="100%" height="100%" rx="12" fill="url(#terminal-bg)"/>
<ellipse cx="{width / 2:.0f}" cy="{height / 2:.0f}" rx="{width * 0.48:.0f}" ry="{height * 0.44:.0f}" fill="url(#portrait-halo)"/>
<rect width="100%" height="100%" rx="12" fill="url(#terminal-stripes)"/>
<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="12" fill="none" stroke="#39d878" stroke-opacity=".42"/>
<style>text{{font:14px monospace;fill:#d7e4e8;white-space:pre}}</style>''']
    for i, line in enumerate(lines):
        y = 20 + (i + 1) * CELL_H
        delay = i * 0.055
        chunks.append(f'<clipPath id="row{i}"><rect x="12" y="{y - CELL_H + 2}" width="0" height="{CELL_H}"><animate attributeName="width" from="0" to="{COLS * CELL_W}" dur="0.75s" begin="{delay:.3f}s" fill="freeze"/></rect></clipPath>')
        chunks.append(f'<text xml:space="preserve" x="12" y="{y}" clip-path="url(#row{i})">{html.escape(line)}</text>')
    chunks.append("</svg>")
    Path("franklin-ascii.svg").write_text("\n".join(chunks), encoding="utf-8")
    print("Generado franklin-ascii.svg")


if __name__ == "__main__":
    main()
