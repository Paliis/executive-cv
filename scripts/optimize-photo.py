"""Compress hero photo to WebP/AVIF (display size ~320px, 2x = 640)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "photo.png"
MAX_WIDTH = 640


def main() -> int:
    im = Image.open(SRC)
    w, h = im.size
    print(f"source {SRC.name}: {w}x{h}, {SRC.stat().st_size // 1024} KB")
    if w > MAX_WIDTH:
        h = int(h * MAX_WIDTH / w)
        w = MAX_WIDTH
        im = im.resize((w, h), Image.Resampling.LANCZOS)
    rgb = im.convert("RGB")
    webp = ROOT / "photo.webp"
    rgb.save(webp, "WEBP", quality=82, method=6)
    print(f"wrote {webp.name}: {w}x{h}, {webp.stat().st_size // 1024} KB")
    avif = ROOT / "photo.avif"
    try:
        rgb.save(avif, "AVIF", quality=50)
        print(f"wrote {avif.name}: {avif.stat().st_size // 1024} KB")
    except Exception as exc:  # noqa: BLE001
        print(f"AVIF skipped ({exc})")
        if avif.exists():
            avif.unlink()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
