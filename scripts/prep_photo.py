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

    rgba = np.asarray(Image.open(source).convert("RGBA"))
    alpha = rgba[:, :, 3:4].astype(np.float32) / 255.0
    white = np.full(rgba[:, :, :3].shape, 255, dtype=np.float32)
    composite = (rgba[:, :, :3] * alpha + white * (1 - alpha)).astype(np.uint8)
    gray = cv2.cvtColor(composite, cv2.COLOR_RGB2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    prepared = clahe.apply(gray)
    output = Path("source-prepped.png")
    cv2.imwrite(str(output), prepared)
    print(f"Imagen preparada: {output}")


if __name__ == "__main__":
    main()
