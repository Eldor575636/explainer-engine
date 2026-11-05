#!/usr/bin/env python3
"""Bilmasboy platform kit: covers, headers, intro posts, Instagram highlight covers and avatars, all from the
"?" logo + slogan. Each layout keeps text out of the areas a platform crops or covers with the profile photo.
Usage: python3 brand_kit.py <out_dir>"""
import random, shutil, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from logo import logo, _txt, _shadow
from v3 import new_alphabet
from banner import torn_label, socials_column, SLOGAN, banner as yt_banner
from avatar import bubble

NAVY, RED, MUSTARD, CREAM = (27, 42, 74), (200, 16, 46), (212, 162, 58), (244, 238, 223)
MONT = str(HERE / "fonts" / "Montserrat-ExtraBold.ttf")
RUBIK = str(HERE / "fonts" / "brand" / "Rubik-ExtraBold.ttf")
SOCIALS = [("youtube", "@bilmasboy"), ("instagram", "@bilmas.boy"), ("tiktok", "@bilmas.boy"), ("facebook", "@bilmas.boy"), ("telegram", "@bilmas_boy")]
SUB = "o'zbek tilida, oddiy qilib"


def bg(w, h, dots=True):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt(((xx - w * 0.5) / max(w, h)) ** 2 + ((yy - h * 0.5) / max(w, h)) ** 2)
    light = np.clip(1 - r * 1.7, 0, 1)[..., None]
    a = np.array(NAVY, np.float32) * (0.72 + 0.45 * light)
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    if dots:
        d = ImageDraw.Draw(img, "RGBA"); step = max(18, int(min(w, h) * 0.02)); rr = step * 0.085
        for y in range(0, h, step):
            for x in range((y // step % 2) * step // 2, w, step):
                d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=(255, 255, 255, 8))
    return img


def ghosts(img, spots, seed=7):
    """Faint '?' doodles; spots are (fx, fy, size as fraction of height, rotation)."""
    rnd = random.Random(seed); w, h = img.size
    for fx, fy, fs, rot in spots:
        q = _txt("?", ImageFont.truetype(RUBIK, max(20, int(h * fs))), CREAM + (rnd.choice([16, 20, 24]),))
        q = q.rotate(rot, expand=True, resample=Image.BICUBIC)
        img.alpha_composite(q, (int(w * fx) - q.width // 2, int(h * fy) - q.height // 2))


def stack(box_w, box_h, with_sub=True):
    """Logo + torn slogan label (+ subline), scaled to fit box_w x box_h. Returns RGBA."""
    lg = _shadow(logo("rubik", 210, "dark"), (0, 10), 12, 0.45)
    tag = _shadow(torn_label(new_alphabet(SLOGAN.upper()), 70), (0, 8), 8, 0.35)
    parts = [lg, tag]
    if with_sub:
        parts.append(_txt(new_alphabet(SUB), ImageFont.truetype(MONT, 44), CREAM + (230,)))
    gaps = [22, 18][:len(parts) - 1]
    W_ = max(p.width for p in parts); H_ = sum(p.height for p in parts) + sum(gaps)
    out = Image.new("RGBA", (W_, H_), (0, 0, 0, 0)); y = 0
    for i, p in enumerate(parts):
        out.alpha_composite(p, ((W_ - p.width) // 2, y)); y += p.height + (gaps[i] if i < len(gaps) else 0)
    k = min(box_w / out.width, box_h / out.height, 1.0)
    return out.resize((int(out.width * k), int(out.height * k)), Image.LANCZOS)


def place(img, spr, cx, cy):
    img.alpha_composite(spr, (int(cx - spr.width / 2), int(cy - spr.height / 2)))


def socials_row(icon=46, size=34, gap=46):
    items = [socials_column([s], icon, size) for s in SOCIALS]
    W_ = sum(i.width for i in items) + gap * (len(items) - 1); H_ = max(i.height for i in items)
    out = Image.new("RGBA", (W_, H_), (0, 0, 0, 0)); x = 0
    for i in items:
        out.alpha_composite(i, (x, (H_ - i.height) // 2)); x += i.width + gap
    return _shadow(out, (0, 4), 4, 0.5)


# ---------------- layouts ----------------
def facebook_cover():
    """1640x624. Phones crop the sides (~1200 px centre stays); desktop puts the profile photo bottom-left."""
    w, h = 1640, 624; img = bg(w, h)
    ghosts(img, [(0.07, 0.3, 0.42, -12), (0.94, 0.62, 0.45, 12), (0.86, 0.15, 0.18, -8)])
    place(img, stack(980, 400), w / 2 + 40, h * 0.46)
    return img


def x_header():
    """1500x500. Profile photo covers bottom-left; X crops top/bottom a little on some screens."""
    w, h = 1500, 500; img = bg(w, h)
    ghosts(img, [(0.06, 0.25, 0.4, -12), (0.95, 0.65, 0.42, 12)])
    place(img, stack(860, 290), w * 0.56, h * 0.5)
    return img


def telegram_intro():
    """1280x720 pinned intro post / link image, with every handle."""
    w, h = 1280, 720; img = bg(w, h)
    ghosts(img, [(0.07, 0.22, 0.3, -12), (0.94, 0.3, 0.26, 12), (0.9, 0.86, 0.2, -6), (0.08, 0.84, 0.18, 8)])
    place(img, stack(1000, 400), w / 2, h * 0.42)
    row = socials_row(36, 27, 36)
    if row.width > w - 120:
        row = row.resize((w - 120, int(row.height * (w - 120) / row.width)), Image.LANCZOS)
    place(img, row, w / 2, h * 0.84)
    return img


def portrait_post(w=1080, h=1350):
    """Instagram / Facebook / TikTok-photo intro post (4:5); also used as 9:16 story at 1080x1920."""
    img = bg(w, h)
    ghosts(img, [(0.12, 0.12, 0.16, -12), (0.88, 0.2, 0.12, 12), (0.86, 0.78, 0.16, -8), (0.14, 0.9, 0.1, 10)])
    tall = h / w > 1.5                                     # 9:16: keep clear of TikTok/Reels captions and buttons
    place(img, stack(w - 160, h * (0.26 if tall else 0.36)), w / 2, h * (0.36 if tall else 0.42))
    col = _shadow(socials_column(SOCIALS, 52, 40), (0, 4), 4, 0.5)
    place(img, col, w / 2 - (40 if tall else 0), h * (0.6 if tall else 0.74))
    return img


def _globe(s):
    g = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(g); lw = max(6, s // 22); m = lw
    d.ellipse((m, m, s - m, s - m), outline=CREAM, width=lw)
    d.ellipse((s * 0.3, m, s * 0.7, s - m), outline=CREAM, width=lw)
    d.line((m, s / 2, s - m, s / 2), fill=CREAM, width=lw)
    for f in (0.25, 0.75):
        y = s * f; half = (s / 2 - m) * (1 - (2 * f - 1) ** 2) ** 0.5
        d.line((s / 2 - half, y, s / 2 + half, y), fill=CREAM, width=lw)
    return g


def _play(s):
    g = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
    d.rounded_rectangle((0, s * 0.12, s - 1, s * 0.88), s * 0.18, fill=RED)
    d.polygon([(s * 0.4, s * 0.32), (s * 0.4, s * 0.68), (s * 0.7, s * 0.5)], fill=(255, 255, 255))
    return g


def _glyph(ch, s, col):
    return _txt(ch, ImageFont.truetype(RUBIK, int(s * 1.05)), col)


def highlight(kind):
    """1080x1920 Instagram highlight cover; only the centre circle (~0.55 of width) shows."""
    w, h = 1080, 1920; img = bg(w, h, dots=False); s = 420
    icon = {"about": bubble(s), "episodes": _play(s), "money": _glyph("$", s, MUSTARD),
            "world": _globe(s)}[kind]
    place(img, _shadow(icon, (0, 10), 10, 0.4), w / 2, h / 2)
    return img


def build(out):
    out = Path(out)
    av = Path("/mnt/user-data/outputs/brand/avatars")
    jobs = {
        "YouTube": [("banner_2560x1440.jpg", yt_banner())],
        "Facebook": [("cover_1640x624.jpg", facebook_cover()), ("intro_post_1080x1350.jpg", portrait_post())],
        "Instagram": [("intro_post_1080x1350.jpg", portrait_post()), ("story_1080x1920.jpg", portrait_post(1080, 1920))]
                     + [(f"highlight_{k}_1080x1920.jpg", highlight(k)) for k in ("about", "episodes", "money", "world")],
        "TikTok": [("intro_post_1080x1920.jpg", portrait_post(1080, 1920))],
        "Telegram": [("intro_post_1280x720.jpg", telegram_intro())],
        "X (Twitter)": [("header_1500x500.jpg", x_header())],
    }
    avatars = {"YouTube": ("youtube_800", 800), "Facebook": ("1024", 1024), "Instagram": ("instagram_320", 320),
               "TikTok": ("tiktok_200", 200), "Telegram": ("telegram_640", 640), "X (Twitter)": ("1024", 400)}
    sheet = []
    for plat, files in jobs.items():
        d = out / plat; d.mkdir(parents=True, exist_ok=True)
        for name, im in files:
            im.convert("RGB").save(d / name, quality=92, optimize=True); sheet.append((plat, name, im))
        tag, px = avatars[plat]
        src = Image.open(av / f"avatar_bubble_navy_{tag}.png").convert("RGB")
        if src.width != px:
            src = src.resize((px, px), Image.LANCZOS)
        src.save(d / f"profile_picture_{px}x{px}.png")
    # contact sheet for review
    tw = 520; rows = []
    for plat, name, im in sheet:
        t = im.convert("RGB"); t = t.resize((tw, int(t.height * tw / t.width)), Image.LANCZOS)
        if t.height > 700:
            t = t.resize((int(t.width * 700 / t.height), 700), Image.LANCZOS)
        rows.append((f"{plat} / {name}", t))
    cols = 4; cw, chh = tw + 30, 760
    S = Image.new("RGB", (cols * cw, ((len(rows) + cols - 1) // cols) * chh), (235, 235, 235)); dd = ImageDraw.Draw(S)
    for i, (lab, t) in enumerate(rows):
        x, y = (i % cols) * cw + 15, (i // cols) * chh + 15
        S.paste(t, (x, y + 30)); dd.text((x, y), lab, fill=(20, 20, 20))
    S.save(out / "_overview.jpg", quality=85)
    return out


if __name__ == "__main__":
    print(build(sys.argv[1] if len(sys.argv) > 1 else "brand_kit"))
