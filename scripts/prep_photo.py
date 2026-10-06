"""Prepare a high-contrast grayscale portrait against a white background."""
from pathlib import Path
import sys

import cv2
import numpy as np
from PIL import Image


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Uso: python scripts/prep_photo.py ruta/a/foto.jpg")
    source = Path(sys.argv[1])
    if not source.is_file():
        raise SystemExit(f"No se encontró la foto: {source}")

    photo = Image.open(source).convert("RGBA")
    width, height = photo.size
    # Crop away some empty wall and the lower shirt so the face reads clearly
    # in the narrow profile-README column.
    photo = photo.crop((int(width * 0.12), int(height * 0.015), int(width * 0.88), int(height * 0.80)))
    rgba = np.asarray(photo)
    alpha = rgba[:, :, 3:4].astype(np.float32) / 255.0
    white = np.full(rgba[:, :, :3].shape, 255, dtype=np.float32)
    composite = (rgba[:, :, :3] * alpha + white * (1 - alpha)).astype(np.uint8)
    gray = cv2.cvtColor(composite, cv2.COLOR_RGB2GRAY)
    # The source already has soft lighting. Avoid CLAHE, which amplified the
    # wall texture into distracting ASCII noise. Flatten the light wall/shirt
    # highlights, then slightly strengthen the remaining facial contrast.
    rgb_spread = composite.max(axis=2).astype(np.int16) - composite.min(axis=2).astype(np.int16)
    neutral_background = (rgb_spread < 25) & (gray > 145)
    gray[neutral_background] = 255
    gray = cv2.convertScaleAbs(gray, alpha=1.18, beta=-24)
    gray[gray >= 218] = 255
    prepared = cv2.GaussianBlur(gray, (3, 3), 0.45)
    output = Path("source-prepped.png")
    cv2.imwrite(str(output), prepared)
    print(f"Imagen preparada: {output}")


if __name__ == "__main__":
    main()
