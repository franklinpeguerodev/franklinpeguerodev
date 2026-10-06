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
    # Crop to the head and upper shoulders so the face fills the ASCII grid.
    photo = photo.crop((int(width * 0.10), int(height * 0.02), int(width * 0.90), int(height * 0.85)))
    rgba = np.asarray(photo)
    alpha = rgba[:, :, 3:4].astype(np.float32) / 255.0
    white = np.full(rgba[:, :, :3].shape, 255, dtype=np.float32)
    composite = (rgba[:, :, :3] * alpha + white * (1 - alpha)).astype(np.uint8)
    gray = cv2.cvtColor(composite, cv2.COLOR_RGB2GRAY)
    # Local contrast (CLAHE) brings out highlights and shadows on a flat-lit
    # face so it doesn't convert to a dark blob. Then composite back onto
    # pure white so background pixels map to the blank end of the ramp.
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)
    bright_wall = gray >= 215
    gray[bright_wall] = 255
    prepared = cv2.GaussianBlur(gray, (3, 3), 0.45)
    output = Path("source-prepped.png")
    cv2.imwrite(str(output), prepared)
    print(f"Imagen preparada: {output}")


if __name__ == "__main__":
    main()
