"""Vertical cover (1080x1920) for a Short, plus a TikTok copy of the Short that opens on it.

TikTok shows the first frame as the cover when no cover is chosen in the app, and vidIQ cannot set one,
so the cover is spliced in as the first 0.2 s of a TikTok-only copy. YouTube keeps the original file.

Spec file (JSON list), one entry per Short:
  {"video": ".../6 Shorts/1_hook.mp4", "bg": "projects/ep03-singapore/layers/bg_tv_1965.jpg",
   "fx": 0.5, "label": "3-QISM: SINGAPUR", "headline": "YIG'LAGAN RAHBAR", "out": "dir/E03_1_hook"}
  fx = horizontal focus of the 9:16 crop (0..1 of the picture width).

  python3 shorts_cover.py spec.json            # covers only (out.jpg) + contact sheet
  python3 shorts_cover.py spec.json --video    # also out_tiktok.mp4
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v3 import new_alphabet

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
NAVY, CREAM, MUSTARD, RED = (27, 42, 74), (244, 238, 223), (212, 162, 58), (200, 16, 46)
ANTON = os.path.join(HERE, "fonts/Anton-Regular.ttf")
MONT = os.path.join(HERE, "fonts/Montserrat-ExtraBold.ttf")
COVER_SEC = 0.2


def crop_916(img, fx):
    w, h = img.size
    cw = int(h * 9 / 16)
    if cw > w:                                   # picture narrower than 9:16: crop height instead
        ch = int(w * 16 / 9)
        return img.crop((0, (h - ch) // 2, w, (h - ch) // 2 + ch)).resize((W, H), Image.LANCZOS)
    x0 = int(min(max(fx * w - cw / 2, 0), w - cw))
    return img.crop((x0, 0, x0 + cw, h)).resize((W, H), Image.LANCZOS)


def wrap(words, font, max_w):
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if font.getlength(t) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    return lines + [cur]


def headline_layout(text, max_w=960, max_lines=3):
    """'|' forces line breaks; otherwise words wrap to fit."""
    words = text.replace("|", " ").split()
    for size in range(190, 70, -6):
        f = ImageFont.truetype(ANTON, size)
        lines = [l.strip() for l in text.split("|")] if "|" in text else wrap(words, f, max_w)
        if len(lines) <= max_lines and all(f.getlength(l) <= max_w for l in lines):
            return f, lines
    return ImageFont.truetype(ANTON, 70), wrap(words, ImageFont.truetype(ANTON, 70), max_w)


def render_cover(e):
    img = crop_916(Image.open(os.path.join(HERE, e["bg"])).convert("RGB"), e.get("fx", 0.5))
    # navy fade over the lower half so the headline always reads
    fade = Image.new("L", (1, H))
    for y in range(H):
        t = (y - H * 0.40) / (H * 0.28)
        fade.putpixel((0, y), int(255 * 0.93 * max(0, min(1, t))))
    img = Image.composite(Image.new("RGB", (W, H), NAVY), img, fade.resize((W, H)))
    d = ImageDraw.Draw(img)

    # episode pill at the top
    lab = new_alphabet(e["label"])
    lf = ImageFont.truetype(MONT, 40)
    lw = lf.getlength(lab)
    d.rounded_rectangle((W / 2 - lw / 2 - 34, 120, W / 2 + lw / 2 + 34, 196), 38, fill=NAVY)
    d.text((W / 2, 158), lab, font=lf, fill=MUSTARD, anchor="mm")

    # headline, bottom-anchored; last line on a mustard label
    f, lines = headline_layout(new_alphabet(e["headline"]))
    lh = int(f.size * 1.12)
    y = 1650 - lh * len(lines)
    for i, line in enumerate(lines):
        last = i == len(lines) - 1 and len(lines) > 1
        tw = f.getlength(line)
        if last:
            pad = 26
            bb = d.textbbox((W / 2, y + lh / 2), line, font=f, anchor="mm")   # includes Ö/Ğ dots
            top = min(bb[1] - pad * 0.6, y + lh * 0.06)
            d.rectangle((W / 2 - tw / 2 - pad, top, W / 2 + tw / 2 + pad, bb[3] + pad * 0.6), fill=MUSTARD)
            d.text((W / 2, y + lh / 2), line, font=f, fill=NAVY, anchor="mm")
        else:
            d.text((W / 2, y + lh / 2), line, font=f, fill=CREAM, anchor="mm", stroke_width=4, stroke_fill=NAVY)
        y += lh
    d.rectangle((W / 2 - 90, y + 30, W / 2 + 90, y + 42), fill=RED)

    bf = ImageFont.truetype(ANTON, 64)
    d.text((W / 2 - bf.getlength("BOY") / 2, 1820), "BILMAS", font=bf, fill=CREAM, anchor="mm")
    d.text((W / 2 + bf.getlength("BILMAS") / 2, 1820), "BOY", font=bf, fill=MUSTARD, anchor="mm")
    return img


def tiktok_copy(video, cover_jpg, out_mp4):
    """Cover still for COVER_SEC, then the Short; audio delayed by the same amount."""
    probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                            "stream=r_frame_rate", "-of", "csv=p=0", video], capture_output=True, text=True)
    fps = probe.stdout.strip() or "30"
    ms = int(COVER_SEC * 1000)
    fc = (f"[0:v]scale={W}:{H},setsar=1,fps={fps},format=yuv420p,trim=duration={COVER_SEC}[c];"
          f"[1:v]scale={W}:{H},setsar=1,fps={fps},format=yuv420p[m];[c][m]concat=n=2:v=1:a=0[v];"
          f"[1:a]adelay={ms}|{ms}[a]")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-loop", "1", "-t", str(COVER_SEC), "-i", cover_jpg,
                    "-i", video, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264",
                    "-preset", "medium", "-crf", "19", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
                    out_mp4], check=True)


def torn_label(img, text, cy=0.215):
    """Mustard torn-paper label with navy Anton text (the owner's cover style), centred at cy * height."""
    import random
    rnd = random.Random(text)
    d = ImageDraw.Draw(img)
    text = new_alphabet(text)
    f = ImageFont.truetype(ANTON, 118)
    while f.getlength(text) > W * 0.70:
        f = ImageFont.truetype(ANTON, f.size - 4)
    bb = d.textbbox((0, 0), text, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    x0, x1 = W / 2 - tw / 2 - 60, W / 2 + tw / 2 + 60
    y0, y1 = H * cy - th / 2 - 46, H * cy + th / 2 + 46
    pts = []
    for i in range(13):                                       # torn top edge
        pts.append((x0 + (x1 - x0) * i / 12, y0 + rnd.uniform(-7, 7)))
    for i in range(1, 6):                                     # right edge
        pts.append((x1 + rnd.uniform(-6, 6), y0 + (y1 - y0) * i / 6))
    for i in range(12, -1, -1):                               # torn bottom edge
        pts.append((x0 + (x1 - x0) * i / 12, y1 + rnd.uniform(-7, 7)))
    for i in range(5, 0, -1):
        pts.append((x0 + rnd.uniform(-6, 6), y0 + (y1 - y0) * i / 6))
    shadow = Image.new("L", img.size, 0)
    ImageDraw.Draw(shadow).polygon([(x + 8, y + 10) for x, y in pts], fill=90)
    img.paste((60, 50, 30), (0, 0), shadow.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(img)
    d.polygon(pts, fill=MUSTARD)
    d.text((W / 2, H * cy), text, font=f, fill=NAVY, anchor="mm")
    return img


def main():
    spec = json.load(open(sys.argv[1]))
    do_video = "--video" in sys.argv
    thumbs = []
    for e in spec:
        os.makedirs(os.path.dirname(e["out"]) or ".", exist_ok=True)
        if "cover" in e:                                      # ready-made (Gemini/Higgsfield) cover
            img = Image.open(e["cover"]).convert("RGB").resize((W, H), Image.LANCZOS)
            if e.get("tag"):
                img = torn_label(img, e["tag"])
        else:
            img = render_cover(e)
        img.save(e["out"] + ".jpg", quality=92)
        thumbs.append(img.resize((270, 480)))
        if do_video:
            tiktok_copy(e["video"], e["out"] + ".jpg", e["out"] + "_tiktok.mp4")
            print("video", e["out"] + "_tiktok.mp4")
    cols = 7
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 280 + 10, rows * 490 + 10), "white")
    for i, t in enumerate(thumbs):
        sheet.paste(t, (10 + (i % cols) * 280, 10 + (i // cols) * 490))
    sheet.save(os.path.splitext(sys.argv[1])[0] + "_sheet.jpg", quality=85)
    print("sheet", os.path.splitext(sys.argv[1])[0] + "_sheet.jpg")


if __name__ == "__main__":
    main()
