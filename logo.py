#!/usr/bin/env python3
"""Bilmasboy wordmark concepts. logo(style, height, theme) -> RGBA PIL image.

theme "dark" = for navy/dark backgrounds, "light" = for cream/light backgrounds.
Run directly to render a comparison sheet: python3 logo.py <out.png>
"""
import math, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).parent
B = HERE / "fonts" / "brand"
NAVY, RED, MUSTARD, CREAM, INK = (27, 42, 74), (200, 16, 46), (212, 162, 58), (244, 238, 223), (14, 22, 38)


def _txt(text, font, fill, stroke=0, stroke_fill=None, track=0):
    f = font
    widths = [f.getlength(c) for c in text]
    w = int(sum(widths) + track * (len(text) - 1) + 2 * stroke + 4)
    asc, desc = f.getmetrics()
    img = Image.new("RGBA", (w, asc + desc + 2 * stroke + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(img); x = stroke + 2
    for c, cw in zip(text, widths):
        d.text((x, stroke + 2), c, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
        x += cw + track
    return img.crop(img.getbbox())


def _word(parts, font, stroke=0, stroke_fill=None, track=0):
    """[(text, colour), ...] drawn on ONE baseline, so mixed colours line up."""
    widths = [[font.getlength(c) for c in t] for t, _ in parts]
    w = int(sum(sum(x) for x in widths) + track * sum(len(t) for t, _ in parts) + 2 * stroke + 20)
    asc, desc = font.getmetrics()
    img = Image.new("RGBA", (w, asc + desc + 2 * stroke + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(img); x = stroke + 10
    for (t, col), ws in zip(parts, widths):
        for c, cw in zip(t, ws):
            d.text((x, stroke + 10), c, font=font, fill=col, stroke_width=stroke, stroke_fill=stroke_fill)
            x += cw + track
    return img.crop(img.getbbox())


def _row(parts, gap):
    h = max(p.height for p in parts)
    w = sum(p.width for p in parts) + gap * (len(parts) - 1)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0)); x = 0
    for p in parts:
        out.alpha_composite(p, (x, h - p.height)); x += p.width + gap
    return out


def _shadow(img, off=(0, 6), blur=6, alpha=0.4):
    pad = blur * 3
    out = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); sh.putalpha(img.split()[3].point(lambda v: int(v * alpha)))
    out.alpha_composite(sh, (pad + off[0], pad + off[1])); out = out.filter(ImageFilter.GaussianBlur(blur))
    out.alpha_composite(img, (pad, pad))
    return out.crop(out.getbbox())


def logo(style="lilita", height=120, theme="dark"):
    S = 400                                                # draw big, scale down at the end
    main = CREAM if theme == "dark" else NAVY
    if style == "paytone":                                 # friendly lowercase, red pen underline under "boy"
        f = ImageFont.truetype(str(B / "PaytoneOne.ttf"), S)
        img = _word([("bilmas", main), ("boy", MUSTARD)], f, track=4)
        aw = f.getlength("bilmas") + 24
        c = Image.new("RGBA", (img.width, img.height + 60), (0, 0, 0, 0)); c.alpha_composite(img, (0, 0))
        d = ImageDraw.Draw(c); x0 = aw; x1 = c.width - 4; y = img.height + 18
        d.line([(x0 + (x1 - x0) * t, y + 18 * math.sin(t * math.pi) - 10 * t) for t in [i / 30 for i in range(31)]], fill=RED, width=34, joint="curve")
        img = c
    elif style == "unbounded":                             # geometric caps, BOY on a mustard block
        f = ImageFont.truetype(str(B / "Unbounded-ExtraBold.ttf"), S)
        a = _txt("BILMAS", f, main, track=-6)
        b = _txt("BOY", f, NAVY, track=-6)
        box = Image.new("RGBA", (b.width + 80, a.height + 80), (0, 0, 0, 0))
        ImageDraw.Draw(box).rounded_rectangle((0, 0, box.width - 1, box.height - 1), 40, fill=MUSTARD)
        box.alpha_composite(b, (40, (box.height - b.height) // 2))
        img = _row([a, box], 30)
    elif style == "lilita":                                # cartoon sticker: matches the mascot
        f = ImageFont.truetype(str(B / "LilitaOne.ttf"), S)
        img = _word([("Bilmas", CREAM), ("boy", MUSTARD)], f, stroke=24, stroke_fill=NAVY, track=-4)
    elif style == "archivo":                               # stacked, with a red question-mark badge
        f = ImageFont.truetype(str(B / "ArchivoBlack.ttf"), S)
        f2 = ImageFont.truetype(str(B / "ArchivoBlack.ttf"), int(S * 0.62))
        a = _txt("BILMAS", f, main, track=-4)
        b = _txt("BOY", f2, MUSTARD, track=40)
        stack = Image.new("RGBA", (max(a.width, b.width), a.height + b.height + 30), (0, 0, 0, 0))
        stack.alpha_composite(a, (0, 0)); stack.alpha_composite(b, (0, a.height + 30))
        r = stack.height
        badge = Image.new("RGBA", (r, r), (0, 0, 0, 0)); bd = ImageDraw.Draw(badge)
        bd.ellipse((0, 0, r - 1, r - 1), fill=RED)
        qf = ImageFont.truetype(str(B / "ArchivoBlack.ttf"), int(r * 0.78))
        q = _txt("?", qf, (255, 255, 255)); badge.alpha_composite(q, ((r - q.width) // 2, (r - q.height) // 2))
        img = _row([badge, stack], 40)
    elif style == "rubik":                                 # rounded bold lowercase + speech-bubble "?"
        f = ImageFont.truetype(str(B / "Rubik-ExtraBold.ttf"), S)
        word = _word([("bilmas", main), ("boy", MUSTARD)], f, track=-8)
        h = int(f.getbbox("bilmas")[3] - f.getbbox("bilmas")[1])
        bub = Image.new("RGBA", (int(h * 1.1), int(h * 1.15)), (0, 0, 0, 0)); bd = ImageDraw.Draw(bub)
        bd.rounded_rectangle((0, 0, bub.width - 1, int(h * 0.95)), int(h * 0.3), fill=RED)
        bd.polygon([(int(h * 0.25), int(h * 0.9)), (int(h * 0.55), int(h * 0.9)), (int(h * 0.2), bub.height - 1)], fill=RED)
        q = _txt("?", ImageFont.truetype(str(B / "Rubik-ExtraBold.ttf"), int(h * 0.85)), (255, 255, 255))
        bub.alpha_composite(q, ((bub.width - q.width) // 2, (int(h * 0.95) - q.height) // 2))
        img = _row([bub, word], 34)
    else:                                                  # "montserrat": heavy caps, pen circle round BOY
        f = ImageFont.truetype(str(B / "Montserrat-Black.ttf"), S)
        a = _txt("BILMAS", f, main, track=-10); b = _txt("BOY", f, MUSTARD, track=-10)
        img = _row([a, b], 70)
        c = Image.new("RGBA", (img.width + 80, img.height + 120), (0, 0, 0, 0)); c.alpha_composite(img, (20, 60))
        d = ImageDraw.Draw(c); cx = 20 + a.width + 70 + b.width / 2; cy = 60 + img.height / 2
        rx, ry = b.width / 2 + 34, img.height / 2 + 40
        d.line([(cx + rx * math.cos(t) * (1 + 0.03 * math.sin(3 * t)), cy + ry * math.sin(t)) for t in
                [-0.5 + i * (2 * math.pi + 0.3) / 60 for i in range(61)]], fill=RED, width=22, joint="curve")
        img = c.crop(c.getbbox())
    img = _shadow(img, (0, 10), 8, 0.35 if theme == "dark" else 0.18)
    s = height / img.height
    return img.resize((max(1, int(img.width * s)), height), Image.LANCZOS)


STYLES = ["lilita", "rubik", "archivo", "unbounded", "paytone", "montserrat"]

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "logo_sheet.png"
    rows = []
    for st in STYLES:
        row = Image.new("RGB", (1600, 220))
        row.paste(NAVY, (0, 0, 800, 220)); row.paste(CREAM, (800, 0, 1600, 220))
        for k, th in enumerate(("dark", "light")):
            lg = logo(st, 120, th)
            if lg.width > 740:
                lg = lg.resize((740, int(lg.height * 740 / lg.width)), Image.LANCZOS)
            row.paste(lg, (k * 800 + (800 - lg.width) // 2, (220 - lg.height) // 2), lg)
        d = ImageDraw.Draw(row); d.text((10, 8), f"{STYLES.index(st) + 1}. {st}", fill=RED)
        rows.append(row)
    sheet = Image.new("RGB", (1600, 220 * len(rows)))
    for i, r in enumerate(rows):
        sheet.paste(r, (0, i * 220))
    sheet.save(out)
    print(out)
