#!/usr/bin/env python3
"""Bilmasboy thumbnail template (1280x720, YouTube). One JSON spec per thumbnail; the layout is fixed so
every episode looks like the same channel.

Layout (left to right): episode badge + 2-3 line headline on the left 60%, hero cut-out (mascot pose,
historical figure or prop) on the right, optional prop with a red editor's-pen circle, optional red
stamp, small Bilmasboy wordmark bottom-left (bottom-right stays clear for YouTube's timestamp).

Spec keys:
  bg            background image (path relative to the spec), darkened with the navy ink colour
  dark          0..1 how much navy over the background (default 0.55)
  headline      list of lines (current spelling; converted to the new alphabet)
  accent        index of the line drawn on a mustard torn label (default: last line)
  red           list of words to colour signal red inside white lines
  hero          {img, part, nparts, h (0..1 of height), x (0..1 centre), y_off}
  props         [{img, part, nparts, h, x, y, rot, circle: true}]
  stamp         short text for a red rubber stamp, {text, x, y}
  badge         e.g. "1-QISM"
  arrow         {from: [x,y], to: [x,y]} red pen arrow (0..1 coordinates)

Usage: python3 thumbnail.py <spec.json> [<spec2.json> ...]   -> writes <spec>.jpg next to each spec
"""
import json, math, sys
from pathlib import Path
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import motion, fx
import v3
from v3 import new_alphabet

W, H = 1280, 720
NAVY, RED, MUSTARD, CREAM, INK = (27, 42, 74), (200, 16, 46), (212, 162, 58), (244, 238, 223), (14, 22, 38)
ANTON, MONT = motion.ANTON, motion.MONT


def fit_font(text, max_w, size):
    while size > 40:
        f = ImageFont.truetype(ANTON, size)
        if f.getlength(text) <= max_w:
            return f
        size -= 4
    return ImageFont.truetype(ANTON, size)


def paste_sprite(canvas, sprite, cx, cy, scale=1.0, rot=0.0):
    arr = np.asarray(canvas, np.float32) / 255
    sprite.draw(arr, cx, cy, scale, rot, 1.0)
    return Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8))


def pen_circle(d, cx, cy, rx, ry, width=10):
    pts = [(cx + rx * math.cos(a) * (1 + 0.04 * math.sin(3 * a)), cy + ry * math.sin(a)) for a in
           np.linspace(-0.6, 2 * math.pi + 0.35, 90)]
    d.line(pts, fill=RED, width=width, joint="curve")


def pen_arrow(d, a, b, width=12):
    (x0, y0), (x1, y1) = a, b
    mx, my = (x0 + x1) / 2 + (y1 - y0) * 0.18, (y0 + y1) / 2 - (x1 - x0) * 0.18
    pts = [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t * t * y1)
           for t in np.linspace(0, 1, 40)]
    d.line(pts, fill=RED, width=width, joint="curve")
    ang = math.atan2(y1 - pts[-4][1], x1 - pts[-4][0])
    for s in (2.6, -2.6):
        d.line([(x1, y1), (x1 - 46 * math.cos(ang + s * 0.2), y1 - 46 * math.sin(ang + s * 0.2))], fill=RED, width=width)


def render(spec_path):
    spec_path = Path(spec_path)
    s = json.loads(spec_path.read_text(encoding="utf-8"))
    root = spec_path.parent
    cache = root / ".thumb_cache"; cache.mkdir(exist_ok=True)

    # background: cover-crop, navy wash, soft vignette on the left so the headline always reads
    bg = Image.open(root / s["bg"]).convert("RGB")
    sc = max(W / bg.width, H / bg.height)
    bg = bg.resize((math.ceil(bg.width * sc), math.ceil(bg.height * sc)), Image.LANCZOS)
    bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
    a = np.asarray(bg, np.float32)
    light = s.get("theme") == "light"                     # light theme: cream wash, navy text
    wash = np.array(CREAM if light else INK, np.float32)
    dark = s.get("dark", 0.7 if light else 0.55)
    a = a * (1 - dark) + wash * dark
    grad = np.clip(1.15 - np.linspace(0, 1, W) * 1.1, 0, 1)[None, :, None] * 0.45
    a = a * (1 - grad) + wash * grad
    img = Image.fromarray(a.astype(np.uint8)).convert("RGB")

    # props (behind the hero) with optional pen circle
    circles = []
    for p in s.get("props", []):
        sp = v3.sticker(root / p["img"], cache, H * p.get("h", 0.35), part=p.get("part"), nparts=p.get("nparts", 3), outline=10)
        cx, cy = p.get("x", 0.6) * W, p.get("y", 0.7) * H
        img = paste_sprite(img, sp, cx, cy, 1.0, p.get("rot", 0))
        if p.get("circle"):
            circles.append((cx, cy, sp.w * 0.62, sp.h * 0.62))

    # hero cut-out, bottom-anchored on the right
    if s.get("hero"):
        h = s["hero"]
        sp = v3.sticker(root / h["img"], cache, H * h.get("h", 0.95), part=h.get("part"), nparts=h.get("nparts", 3), outline=12)
        img = paste_sprite(img, sp, h.get("x", 0.78) * W, H - sp.h / 2 + h.get("y_off", 0.04) * H, 1.0, h.get("rot", 0))

    d = ImageDraw.Draw(img)
    for c in circles:
        pen_circle(d, *c)
    if s.get("arrow"):
        ar = s["arrow"]
        pen_arrow(d, (ar["from"][0] * W, ar["from"][1] * H), (ar["to"][0] * W, ar["to"][1] * H))

    # headline block: every line fitted to the text column, then the whole block scaled to the free height
    lines = [new_alphabet(l).upper() for l in s["headline"]]
    accent = s.get("accent", len(lines) - 1)
    red_words = {new_alphabet(w).upper() for w in s.get("red", [])}
    x0, max_w = 54, W * s.get("text_w", 0.58)
    top = 128 if s.get("badge") else 60
    bottom = H - 118                                       # room for the wordmark
    gap = 14
    def plan(scale):
        out = []
        for i, line in enumerate(lines):
            f = fit_font(line, max_w - (50 if i == accent else 0), int(s.get("size", 190) * scale))
            bb = f.getbbox(line); hh = bb[3] - bb[1]
            out.append((line, f, bb, hh + (34 if i == accent else 0)))
        return out
    scale = 1.0
    while True:
        pl = plan(scale)
        if sum(p[3] for p in pl) + gap * (len(pl) - 1) <= bottom - top or scale < 0.4:
            break
        scale -= 0.05
    y = top
    for i, (line, f, bb, hh) in enumerate(pl):
        if i == accent:                                   # mustard torn label, navy text, slight tilt
            tw = f.getlength(line)
            lab = Image.new("RGBA", (int(tw + 50), int(hh)), (0, 0, 0, 0))
            ld = ImageDraw.Draw(lab)
            edge = [(x, 3 + (5 if (x // 18) % 2 else 0)) for x in range(0, lab.width + 18, 18)]
            bot = [(x, lab.height - 3 - (5 if (x // 22) % 2 else 0)) for x in range(lab.width + 22, -22, -22)]
            ld.polygon(edge + bot, fill=MUSTARD + (255,))
            ld.text((25, 17 - bb[1]), line, font=f, fill=NAVY + (255,))
            lab = lab.rotate(-2.0, expand=True, resample=Image.BICUBIC)
            sh = lab.split()[3].point(lambda v: int(v * 0.45)).filter(ImageFilter.GaussianBlur(6))
            img.paste((0, 0, 0), (x0 - 10 + 8, int(y) + 10), sh)
            img.paste(lab, (x0 - 10, int(y)), lab)
        else:                                             # white Anton with ink outline; chosen words in red
            xx = x0
            for word in line.split(" "):
                base = NAVY if light else (255, 255, 255)
                col = RED if word.strip("?!.,:") in red_words or word in red_words else base
                d.text((xx, y - bb[1]), word, font=f, fill=col, stroke_width=7, stroke_fill=CREAM if light else INK)
                xx += f.getlength(word + " ")
        y += hh + gap

    if s.get("stamp"):
        st = s["stamp"]
        sp = motion.stamp_sprite(new_alphabet(st["text"]).upper(), st.get("size", 96))
        img = paste_sprite(img, motion.Sprite(sp) if not hasattr(sp, "draw") else sp, st.get("x", 0.5) * W, st.get("y", 0.5) * H, 1.0, -8)
        d = ImageDraw.Draw(img)

    if s.get("badge"):                                    # red episode badge, top-left
        bf = ImageFont.truetype(ANTON, 44)
        t = new_alphabet(s["badge"]).upper(); tw = bf.getlength(t)
        d.rounded_rectangle((x0, 36, x0 + tw + 36, 98), 10, fill=RED)
        d.text((x0 + 18, 36 + 31 - (bf.getbbox(t)[1] + bf.getbbox(t)[3]) / 2), t, font=bf, fill=(255, 255, 255))

    wm = fx.wordmark({"anton": ANTON}, 64)                 # brand, bottom-left
    if s.get("theme") == "light":                          # "Bilmas" in navy on light thumbnails
        wa = np.array(wm); cream = (np.abs(wa[..., :3].astype(int) - np.array(CREAM)).sum(-1) < 60) & (wa[..., 3] > 0)
        wa[cream, :3] = NAVY; wm = Image.fromarray(wa)
    sh = Image.new("RGBA", wm.size, (0, 0, 0, 0)); sh.putalpha(wm.split()[3])
    img.paste((0, 0, 0), (x0 + 3, H - wm.height - 28 + 3), sh.split()[3])
    img.paste(wm, (x0, H - wm.height - 28), wm)

    out = spec_path.with_suffix(".jpg")
    img.convert("RGB").save(out, quality=93)
    return out


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(render(p))
