#!/usr/bin/env python3
"""Two-line name avatar: "bilmas" / "boy" + the red "?" bubble. Drawn at 3x and downsampled.

Layouts: stack_left (bubble beside the two lines), stack_top (bubble above, centred),
boy_bubble (bubble sits after "boy" like a question). Themes: navy, cream.
Usage: python3 avatar_name.py <out_dir>
"""
import math, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from avatar import bubble, circle_preview
NAVY, RED, MUSTARD, CREAM, INK = (27, 42, 74), (200, 16, 46), (212, 162, 58), (244, 238, 223), (14, 22, 38)
RUBIK = str(HERE / "fonts" / "brand" / "Rubik-ExtraBold.ttf")
OUT, K = 1024, 3
S = OUT * K


def word(text, size, fill, track=-0.03):
    f = ImageFont.truetype(RUBIK, size)
    asc, desc = f.getmetrics()
    ws = [f.getlength(c) for c in text]
    w = int(sum(ws) + track * size * (len(text) - 1) + size * 0.2)
    img = Image.new("RGBA", (w, asc + desc), (0, 0, 0, 0)); d = ImageDraw.Draw(img); x = size * 0.1
    for c, cw in zip(text, ws):
        d.text((x, 0), c, font=f, fill=fill); x += cw + track * size
    # trim horizontally only, keep a common baseline box
    bb = img.getbbox(); return img.crop((bb[0], 0, bb[2], img.height)), asc


def soft_shadow(img, off, blur, alpha):
    pad = blur * 3
    out = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", img.size, INK + (0,)); sh.putalpha(img.split()[3].point(lambda v: int(v * alpha)))
    out.alpha_composite(sh, (pad + off[0], pad + off[1])); out = out.filter(ImageFilter.GaussianBlur(blur))
    out.alpha_composite(img, (pad, pad)); return out, pad


def background(theme):
    base = np.array(NAVY if theme == "navy" else CREAM, np.float32)
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32) / S
    r = np.sqrt((xx - 0.42) ** 2 + (yy - 0.36) ** 2)
    light = np.clip(1.0 - r * 0.9, 0, 1)[..., None]                     # gentle radial light
    if theme == "navy":
        a = base * (0.82 + 0.32 * light)
    else:
        a = base * (0.93 + 0.08 * light)
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(img, "RGBA"); step, rad = 30 * K, 3.0 * K       # halftone texture, very subtle
    dot = (255, 255, 255, 18) if theme == "navy" else (27, 42, 74, 16)
    for y in range(0, S, step):
        for x in range((y // step % 2) * step // 2, S, step):
            d.ellipse((x - rad, y - rad, x + rad, y + rad), fill=dot)
    return img


def compose(layout, theme):
    img = background(theme)
    c1 = CREAM if theme == "navy" else NAVY
    if layout == "stack_left":
        a, asc = word("bilmas", int(S * 0.185), c1); b, _ = word("boy", int(S * 0.185), MUSTARD)
        bub = bubble(int(S * 0.2))
        lh = int(asc * 0.98)                                             # line spacing = cap/x-height based
        text = Image.new("RGBA", (max(a.width, b.width), lh + b.height), (0, 0, 0, 0))
        text.alpha_composite(a, (0, 0)); text.alpha_composite(b, (0, lh))
        tw = bub.width + int(S * 0.03) + text.width
        x0 = (S - tw) // 2; y0 = (S - text.height) // 2 + int(S * 0.02)
        bs, bp = soft_shadow(bub, (0, 12 * K), 10 * K, 0.45)
        img.alpha_composite(bs, (x0 - bp, y0 + int(S * 0.02) - bp))
        ts, tp = soft_shadow(text, (0, 10 * K), 8 * K, 0.4)
        img.alpha_composite(ts, (x0 + bub.width + int(S * 0.03) - tp, y0 - tp))
    elif layout == "stack_top":
        a, asc = word("bilmas", int(S * 0.25), c1); b, _ = word("boy", int(S * 0.25), MUSTARD)
        bub = bubble(int(S * 0.22))
        lh = int(asc * 0.98)
        text = Image.new("RGBA", (max(a.width, b.width), lh + b.height), (0, 0, 0, 0))
        text.alpha_composite(a, ((text.width - a.width) // 2, 0)); text.alpha_composite(b, ((text.width - b.width) // 2, lh))
        total = bub.height + int(S * 0.0) + text.height
        y0 = (S - total) // 2 + int(S * 0.03)
        bs, bp = soft_shadow(bub, (0, 12 * K), 10 * K, 0.45)
        img.alpha_composite(bs, ((S - bub.width) // 2 - bp + int(S * 0.02), y0 - bp))
        ts, tp = soft_shadow(text, (0, 10 * K), 8 * K, 0.4)
        img.alpha_composite(ts, ((S - text.width) // 2 - tp, y0 + bub.height - int(S * 0.04) - tp))
    else:                                                                # boy_bubble
        a, asc = word("bilmas", int(S * 0.255), c1); b, _ = word("boy", int(S * 0.255), MUSTARD)
        bub = bubble(int(S * 0.2))
        lh = int(asc * 0.98)
        line2 = Image.new("RGBA", (b.width + int(S * 0.025) + bub.width, max(b.height, bub.height)), (0, 0, 0, 0))
        line2.alpha_composite(b, (0, line2.height - b.height))
        line2.alpha_composite(bub, (b.width + int(S * 0.025), int(line2.height - b.height + asc * 0.12) - int(bub.height * 0.1)))
        text = Image.new("RGBA", (max(a.width, line2.width), lh + line2.height), (0, 0, 0, 0))
        text.alpha_composite(a, ((text.width - a.width) // 2, 0))
        text.alpha_composite(line2, ((text.width - line2.width) // 2, lh - (line2.height - b.height)))
        ts, tp = soft_shadow(text, (0, 10 * K), 8 * K, 0.4)
        img.alpha_composite(ts, ((S - text.width) // 2 - tp, (S - text.height) // 2 + int(S * 0.03) - tp))
    return img.resize((OUT, OUT), Image.LANCZOS)


if __name__ == "__main__":
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "avatars"); out.mkdir(parents=True, exist_ok=True)
    combos = [(l, t) for l in ("stack_left", "stack_top", "boy_bubble") for t in ("navy", "cream")]
    sheet = Image.new("RGB", (len(combos) * 270, 400), (236, 236, 236))
    sizes = {"youtube_800": 800, "instagram_320": 320, "tiktok_200": 200, "telegram_640": 640}
    for i, (l, t) in enumerate(combos):
        im = compose(l, t)
        im.convert("RGB").save(out / f"name_{l}_{t}_1024.png")
        for n, px in sizes.items():
            im.convert("RGB").resize((px, px), Image.LANCZOS).save(out / f"name_{l}_{t}_{n}.png")
        c = circle_preview(im, 240); sheet.paste(c, (i * 270 + 15, 15), c)
        s = circle_preview(im, 64); sheet.paste(s, (i * 270 + 103, 280), s)
        ImageDraw.Draw(sheet).text((i * 270 + 15, 360), f"{l} / {t}", fill=(30, 30, 30))
    sheet.save(out / "name_avatar_options.png"); print(out)
