"""Generate 1200x630 og-image.jpg for Telegram / messengers."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "og-image.jpg"
PHOTO = ROOT / "photo.png"

W, H = 1200, 630
BG = (9, 9, 11)
ACCENT = (96, 165, 250)
TEXT = (244, 244, 245)
MUTED = (161, 161, 170)


def main():
    canvas = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(canvas)

    # Subtle accent glow
    for i in range(120, 0, -4):
        alpha = int(18 * (i / 120))
        draw.ellipse((720 - i * 2, -80 - i, 1180 + i, 380 + i), fill=(59, 130, 246, alpha) if canvas.mode == "RGBA" else (12, 20, 36))

    # Photo (right)
    photo = Image.open(PHOTO).convert("RGB")
    target_h = 520
    ratio = target_h / photo.height
    target_w = int(photo.width * ratio)
    photo = photo.resize((target_w, target_h), Image.Resampling.LANCZOS)
    px = W - target_w - 56
    py = (H - target_h) // 2
    canvas.paste(photo, (px, py))

    # Border on photo
    draw.rounded_rectangle(
        (px - 2, py - 2, px + target_w + 2, py + target_h + 2),
        radius=20,
        outline=(59, 130, 246),
        width=2,
    )

    try:
        font_title = ImageFont.truetype("arial.ttf", 52)
        font_role = ImageFont.truetype("arial.ttf", 30)
        font_sub = ImageFont.truetype("arial.ttf", 24)
        font_badge = ImageFont.truetype("arialbd.ttf", 22)
    except OSError:
        font_title = ImageFont.load_default()
        font_role = font_sub = font_badge = font_title

    x = 64
    draw.rounded_rectangle((x, 56, x + 200, 96), radius=999, outline=(255, 255, 255, 40), width=1)
    draw.text((x + 24, 64), "Executive CV", fill=MUTED, font=font_badge)

    draw.text((x, 130), "Denis Parshentsev", fill=TEXT, font=font_title)
    draw.text((x, 200), "CEO / COO / Head of E-commerce", fill=TEXT, font=font_role)
    draw.text((x, 248), "LOKO · VARUS · ALLO", fill=ACCENT, font=font_sub)
    draw.text((x, 300), "Dnipro, Ukraine", fill=MUTED, font=font_sub)

    canvas.save(OUT, "JPEG", quality=88, optimize=True, progressive=False)
    share = ROOT / "share.jpg"
    canvas.save(share, "JPEG", quality=90, optimize=True, progressive=False)
    print(f"Wrote {OUT} ({OUT.stat().st_size // 1024} KB)")
    print(f"Wrote {share} ({share.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
