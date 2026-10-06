"""Convert source-prepped.png into a monochrome, self-typing ASCII SVG."""
from pathlib import Path
import html

from PIL import Image

RAMP = " .`:-=+*cs#%@"   # bright (sparse) -> dark (dense)
COLS, ROWS = 38, 45
CELL_W, CELL_H = 8, 16
PADDING = 12


def main() -> None:
    source = Path("source-prepped.png")
    if not source.is_file():
        raise SystemExit("Falta source-prepped.png. Ejecuta primero scripts/prep_photo.py con tu foto.")
    image = Image.open(source).convert("L").resize((COLS, ROWS))
    pixels = list(image.getdata())
    lines = []
    for row in range(ROWS):
        chars = "".join(
            RAMP[min(len(RAMP) - 1, (255 - pixels[row * COLS + col]) * (len(RAMP) - 1) // 255)]
            for col in range(COLS)
        )
        lines.append(chars)

    width, height = COLS * CELL_W + PADDING * 2, ROWS * CELL_H + PADDING * 2
    chunks = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<defs>
  <pattern id="terminal-stripes" width="6" height="6" patternUnits="userSpaceOnUse"><path d="M0 0H6" fill="none" stroke="#39d878" stroke-opacity=".22" stroke-width="1"/></pattern>
</defs>
<rect width="100%" height="100%" rx="10" fill="#0c281b"/>
<rect width="100%" height="100%" rx="10" fill="url(#terminal-stripes)"/>
<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="10" fill="none" stroke="#2ea043" stroke-opacity=".55" stroke-width="1.5"/>
<style>text{{font:14px monospace;fill:#d7e4e8;white-space:pre}}</style>''']
    for i, line in enumerate(lines):
        y = PADDING + (i + 1) * CELL_H
        delay = i * 0.045
        chunks.append(
            f'<clipPath id="row{i}"><rect x="{PADDING}" y="{y - CELL_H + 2}" width="0" height="{CELL_H}">'
            f'<animate attributeName="width" from="0" to="{COLS * CELL_W}" dur="0.75s" begin="{delay:.3f}s" fill="freeze"/>'
            f'</rect></clipPath>'
        )
        chunks.append(f'<text xml:space="preserve" x="{PADDING}" y="{y}" clip-path="url(#row{i})">{html.escape(line)}</text>')
    chunks.append("</svg>")
    Path("franklin-ascii.svg").write_text("\n".join(chunks), encoding="utf-8")
    print("Generado franklin-ascii.svg")


if __name__ == "__main__":
    main()
