#!/usr/bin/env python3
"""Bilmasboy profile pictures (square master 1024px, safe for circular crops) + export sizes.

Variants:
  bubble_navy   red "?" speech bubble on navy           (icon only, best at tiny sizes)
  bubble_cream  red "?" bubble on cream
  mascot_navy   mascot face on navy with a small red "?" bubble
  mascot_mustard mascot face on mustard with the bubble
  mascot_red    mascot face on signal red, cream bubble

Usage: python3 avatar.py <out_dir>
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
NAVY, RED, MUSTARD, CREAM, INK = (27, 42, 74), (200, 16, 46), (212, 162, 58), (244, 238, 223), (14, 22, 38)
RUBIK = str(HERE / "fonts" / "brand" / "Rubik-ExtraBold.ttf")
S = 1024


def bubble(size, fill=RED, qcol=(255, 255, 255), outline=None):
    """The logo's speech bubble with a '?', as an RGBA image `size` wide."""
    w, h = size, int(size * 1.02)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    body = int(h * 0.84)
    d.rounded_rectangle((0, 0, w - 1, body), int(w * 0.28), fill=fill)
    d.polygon([(int(w * 0.2), body - 5), (int(w * 0.5), body - 5), (int(w * 0.14), h - 1)], fill=fill)
    f = ImageFont.truetype(RUBIK, int(body * 0.86))
    bb = f.getbbox("?")
    d.text(((w - (bb[2] - bb[0])) / 2 - bb[0], (body - (bb[3] - bb[1])) / 2 - bb[1]), "?", font=f, fill=qcol)
    if outline:
        a = img.split()[3]
        rim = a.filter(ImageFilter.MaxFilter(outline * 2 + 1))
        out = Image.new("RGBA", img.size, (255, 255, 255, 0)); out.putalpha(rim)
        out.alpha_composite(img); img = out
    return img


def shadow(img, off=(0, 14), blur=14, a=0.35):
    pad = blur * 3
    out = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); sh.putalpha(img.split()[3].point(lambda v: int(v * a)))
    out.alpha_composite(sh, (pad + off[0], pad + off[1])); out = out.filter(ImageFilter.GaussianBlur(blur))
    out.alpha_composite(img, (pad, pad))
    return out, pad


def halftone(bg, col, step=26, r=3.2, alpha=40):
    img = Image.new("RGBA", (S, S), bg + (255,)); d = ImageDraw.Draw(img, "RGBA")
    for y in range(0, S, step):
        for x in range((y // step % 2) * step // 2, S, step):
            d.ellipse((x - r, y - r, x + r, y + r), fill=col + (alpha,))
    return img


def mascot_head(pose=2):
    """Mascot cut-out (white sticker rim), cropped to head and shoulders."""
    import v3
    cache = HERE / "projects" / "ep01-dollar" / ".thumb_cache"; cache.mkdir(exist_ok=True)
    sp = v3.sticker(HERE / "projects" / "ep01-dollar" / "layers" / "mascot_v2.jpg", cache, 2400, part=pose, nparts=4, outline=16)
    rgba = np.concatenate([sp.rgb / np.maximum(sp.a, 1e-6), sp.a], -1)
    im = Image.fromarray((np.clip(rgba, 0, 1) * 255).astype(np.uint8), "RGBA")
    return im.crop((int(im.width * 0.06), 0, int(im.width * 0.94), int(im.height * 0.42)))


def mascot_avatar(bg, dots, bub_fill, bub_q, pose=2):
    img = halftone(bg, dots)
    head = mascot_head(pose)
    s = S * 0.92 / head.width
    head = head.resize((int(head.width * s), int(head.height * s)), Image.LANCZOS)
    head, pad = shadow(head, (0, 16), 16, 0.3)
    img.alpha_composite(head, ((S - head.width) // 2 - int(S * 0.03), int(S * 0.2) - pad))
    b, bp = shadow(bubble(int(S * 0.25), bub_fill, bub_q, outline=10), (0, 10), 10, 0.3)
    img.alpha_composite(b, (int(S * 0.64) - bp, int(S * 0.13) - bp))
    return img


def bubble_avatar(bg, dots, fill=RED, q=(255, 255, 255)):
    img = halftone(bg, dots)
    b, bp = shadow(bubble(int(S * 0.56), fill, q), (0, 18), 18, 0.35)
    img.alpha_composite(b, ((S - b.width) // 2 + 8, (S - b.height) // 2 + 20))
    return img


def circle_preview(img, size=240):
    im = img.resize((size, size), Image.LANCZOS)
    m = Image.new("L", (size, size), 0); ImageDraw.Draw(m).ellipse((0, 0, size - 1, size - 1), fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0)); out.paste(im, (0, 0), m)
    return out


if __name__ == "__main__":
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "avatars"); out.mkdir(parents=True, exist_ok=True)
    V = {
        "bubble_navy": bubble_avatar(NAVY, CREAM),
        "bubble_cream": bubble_avatar(CREAM, NAVY),
        "mascot_navy": mascot_avatar(NAVY, CREAM, RED, (255, 255, 255)),
        "mascot_mustard": mascot_avatar(MUSTARD, NAVY, RED, (255, 255, 255)),
        "mascot_red": mascot_avatar(RED, (255, 255, 255), CREAM, RED),
    }
    sizes = {"youtube_800": 800, "instagram_320": 320, "tiktok_200": 200, "telegram_640": 640}
    sheet = Image.new("RGB", (len(V) * 280, 560), (240, 240, 240))
    for i, (k, img) in enumerate(V.items()):
        img.convert("RGB").save(out / f"avatar_{k}_1024.png")
        for n, px in sizes.items():
            img.convert("RGB").resize((px, px), Image.LANCZOS).save(out / f"avatar_{k}_{n}.png")
        c = circle_preview(img, 240); sheet.paste(c, (i * 280 + 20, 20), c)
        small = circle_preview(img, 64); sheet.paste(small, (i * 280 + 108, 300), small)    # actual size in a feed
        ImageDraw.Draw(sheet).text((i * 280 + 20, 400), k, fill=(20, 20, 20))
    sheet.save(out / "avatar_options.png")
    print(out)
