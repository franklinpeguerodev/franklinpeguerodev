"""Generate Franklin's terminal/neofetch-style profile card."""
from pathlib import Path
import os


def main() -> None:
    animated = os.getenv("STATIC") != "1"
    rows = [
        ("user", "franklinpeguerodev", "#79c0ff"),
        ("role", "Developer", "#d2a8ff"),
        ("focus", "Building useful things", "#a5d6ff"),
        ("stack", "C# · Java", "#7ee787"),
        ("status", "Open to collaboration", "#ffa657"),
    ]
    svg = ['''<svg xmlns="http://www.w3.org/2000/svg" width="490" height="300" viewBox="0 0 490 300">
<rect width="490" height="300" rx="12" fill="#0d1117" stroke="#30363d"/>
<rect width="490" height="42" rx="12" fill="#161b22"/><path d="M0 30h490v12H0z" fill="#161b22"/>
<circle cx="22" cy="21" r="6" fill="#ff7b72"/><circle cx="42" cy="21" r="6" fill="#d29922"/><circle cx="62" cy="21" r="6" fill="#3fb950"/>
<text x="245" y="26" text-anchor="middle" fill="#8b949e" font-family="monospace" font-size="13">franklinpeguerodev — neofetch</text>
<style>text{font-family:monospace}.line{opacity:1;transform:translateY(0)}''']
    if animated:
        svg.append('.line{opacity:0;transform:translateY(5px);animation:show .45s ease forwards}@keyframes show{to{opacity:1;transform:translateY(0)}}')
    svg.append('</style><text x="24" y="82" fill="#7ee787" font-size="18">franklinpeguerodev@github</text><text x="24" y="101" fill="#8b949e" font-size="13">────────────────────────────</text>')
    for i, (key, value, color) in enumerate(rows):
        y = 137 + i * 30
        delay = f' style="animation-delay:{i * 0.13:.2f}s"' if animated else ""
        svg.append(f'<text class="line"{delay} x="28" y="{y}" fill="{color}" font-size="14">{key}</text><text class="line"{delay} x="112" y="{y}" fill="#c9d1d9" font-size="14">{value}</text>')
    svg.append('<text x="24" y="278" fill="#8b949e" font-size="12">$ Personaliza scripts/make_info_card.py con tu perfil</text></svg>')
    Path("info-card.svg").write_text("\n".join(svg), encoding="utf-8")
    print("Generado info-card.svg")


if __name__ == "__main__":
    main()
