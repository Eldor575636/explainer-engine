#!/usr/bin/env python3
"""Bilmasboy YouTube banner (2560x1440). Everything important sits in the 1546x423 centre area that every
device shows; the socials column on the right only shows on desktop/TV. Usage: python3 banner.py <out_dir>"""
import random, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from logo import logo, _txt, _shadow
from v3 import new_alphabet

NAVY, RED, MUSTARD, CREAM, INK = (27, 42, 74), (200, 16, 46), (212, 162, 58), (244, 238, 223), (14, 22, 38)
W, H = 2560, 1440
SAFE = (507, 508, 2053, 931)          # visible on all devices
DESK = (0, 508, 2560, 931)            # visible on desktop
ANTON = str(HERE / "fonts" / "Anton-Regular.ttf")
MONT = str(HERE / "fonts" / "Montserrat-ExtraBold.ttf")
RUBIK = str(HERE / "fonts" / "brand" / "Rubik-ExtraBold.ttf")


def background():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W * 0.5) / W) ** 2 + ((yy - H * 0.5) / H * 0.55) ** 2)
    light = np.clip(1 - r * 1.6, 0, 1)[..., None]
    a = np.array(NAVY, np.float32) * (0.72 + 0.45 * light)
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(img, "RGBA"); step = 26
    for y in range(0, H, step):
        for x in range((y // step % 2) * step // 2, W, step):
            d.ellipse((x - 2.2, y - 2.2, x + 2.2, y + 2.2), fill=(255, 255, 255, 7))
    return img


def ghost_marks(img):
    """Big faint question marks and bubbles at the edges (desktop only), like doodles in a notebook margin."""
    rnd = random.Random(7)
    spots = [(150, 610, 300, -14), (420, 860, 150, 10), (300, 1000, 110, -6), (2130, 600, 120, 12),
             (2440, 880, 280, 14), (2250, 1010, 120, -10), (90, 380, 140, 8), (2480, 420, 130, -12)]
    for x, y, s, rot in spots:
        q = _txt("?", ImageFont.truetype(RUBIK, s), CREAM + (rnd.choice([16, 20, 24]),))
        q = q.rotate(rot, expand=True, resample=Image.BICUBIC)
        img.alpha_composite(q, (x - q.width // 2, y - q.height // 2))


def torn_label(text, size, fill=MUSTARD, ink=NAVY):
    f = ImageFont.truetype(ANTON, size)
    t = _txt(text, f, ink, track=2)
    pw, ph = t.width + int(size * 0.9), t.height + int(size * 0.55)
    lab = Image.new("RGBA", (pw, ph), (0, 0, 0, 0)); d = ImageDraw.Draw(lab)
    rnd = random.Random(3); pts = []
    for x in range(0, pw + 1, 14):                       # torn top edge
        pts.append((x, rnd.randint(0, 7)))
    for x in range(pw, -1, -14):                         # torn bottom edge
        pts.append((x, ph - 1 - rnd.randint(0, 7)))
    d.polygon(pts, fill=fill)
    lab.alpha_composite(t, ((pw - t.width) // 2, (ph - t.height) // 2))
    return lab.rotate(-1.2, expand=True, resample=Image.BICUBIC)


def socials_column(items, icon=46, size=34):
    f = ImageFont.truetype(MONT, size)
    rows = []
    for plat, handle in items:
        ic = Image.open(HERE / "assets" / "brand" / "platforms" / f"{plat}.png").convert("RGBA")
        ic = ic.resize((icon, int(ic.height * icon / ic.width)), Image.LANCZOS)
        tx = _txt(handle, f, CREAM)
        r = Image.new("RGBA", (icon + 18 + tx.width, max(icon, tx.height)), (0, 0, 0, 0))
        r.alpha_composite(ic, (0, (r.height - ic.height) // 2)); r.alpha_composite(tx, (icon + 18, (r.height - tx.height) // 2))
        rows.append(r)
    gap = 26
    col = Image.new("RGBA", (max(r.width for r in rows), sum(r.height for r in rows) + gap * (len(rows) - 1)), (0, 0, 0, 0))
    y = 0
    for r in rows:
        col.alpha_composite(r, (0, y)); y += r.height + gap
    return col


def banner():
    img = background(); ghost_marks(img)
    x0, y0, x1, y1 = SAFE; cx = (x0 + x1) // 2
    lg = _shadow(logo("rubik", 210, "dark"), (0, 10), 12, 0.45)
    if lg.width > (x1 - x0) - 120:
        lg = lg.resize(((x1 - x0) - 120, int(lg.height * ((x1 - x0) - 120) / lg.width)), Image.LANCZOS)
    tag = _shadow(torn_label(new_alphabet("DUNYONI O'ZGARTIRGAN G'OYALAR"), 74), (0, 8), 8, 0.35)
    sub = _txt(new_alphabet("o'zbek tilida, oddiy qilib"), ImageFont.truetype(MONT, 44), CREAM + (230,))
    gap1, gap2 = 22, 18
    total = lg.height + gap1 + tag.height + gap2 + sub.height
    room = (y1 - y0) - 70                                  # fit the stack inside the all-devices band
    if total > room:
        k = room / total
        lg, tag, sub = [im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS) for im in (lg, tag, sub)]
        gap1, gap2 = int(gap1 * k), int(gap2 * k)
        total = lg.height + gap1 + tag.height + gap2 + sub.height
    y = (y0 + y1) // 2 - total // 2
    img.alpha_composite(lg, (cx - lg.width // 2, y)); y += lg.height + gap1
    img.alpha_composite(tag, (cx - tag.width // 2, y)); y += tag.height + gap2
    img.alpha_composite(sub, (cx - sub.width // 2, y))
    col = socials_column([("youtube", "@bilmasboy"), ("instagram", "@bilmas.boy"),
                          ("tiktok", "@bilmas.boy"), ("telegram", "@bilmas_boy")])
    col = _shadow(col, (0, 4), 4, 0.5)
    img.alpha_composite(col, (x1 + 70, (y0 + y1) // 2 - col.height // 2))
    return img.convert("RGB")


def previews(img, out):
    """What each device shows: desktop strip, phone strip, and a TV view with the safe area marked."""
    desk = img.crop(DESK); desk.save(out / "preview_desktop.jpg", quality=90)
    img.crop(SAFE).save(out / "preview_phone.jpg", quality=90)
    tv = img.copy(); d = ImageDraw.Draw(tv)
    d.rectangle(SAFE, outline=RED, width=6); d.rectangle(DESK, outline=MUSTARD, width=4)
    tv.resize((1280, 720), Image.LANCZOS).save(out / "preview_zones.jpg", quality=88)


if __name__ == "__main__":
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "banner"); out.mkdir(parents=True, exist_ok=True)
    b = banner()
    b.save(out / "bilmasboy_banner_2560x1440.jpg", quality=92, optimize=True)
    previews(b, out)
    print(out, (out / "bilmasboy_banner_2560x1440.jpg").stat().st_size // 1024, "KB")
