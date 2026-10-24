#!/usr/bin/env python3
"""Motion-graphics renderer (v2): layered scenes, sticker cut-outs, bouncing labels,
tags, stamps, word-highlight captions, dissolves, SFX + music.
Usage: python3 motion.py <project_dir>   (needs build.py artefacts: tmp/voice_clean.wav)
"""
import json, math, random, subprocess, sys, wave
from pathlib import Path
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

sys.path.insert(0, str(Path(__file__).parent))
import build

W, H, FPS, SR = 1080, 1920, 30, 48000
NAVY = (27, 42, 74); MUSTARD = (212, 162, 58); RED = (200, 16, 46); CREAM = (244, 238, 223)
FONTS = Path(__file__).parent / "fonts"
ANTON = str(FONTS / "Anton-Regular.ttf"); MONT = str(FONTS / "Montserrat-ExtraBold.ttf")
DISSOLVE = 0.20
random.seed(7)


# ---------------- easing ----------------
def back_out(x, s=2.2):
    x = min(max(x, 0.0), 1.0) - 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2

def ease_out(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3


# ---------------- sprites ----------------
class Sprite:
    def __init__(self, rgba):
        a = np.asarray(rgba, dtype=np.float32) / 255.0
        self.rgb = a[..., :3] * a[..., 3:4]          # premultiplied
        self.a = a[..., 3:4]
        self.h, self.w = a.shape[:2]

    def draw(self, canvas, cx, cy, scale=1.0, rot=0.0, alpha=1.0):
        if alpha <= 0.01 or scale <= 0.01:
            return
        M = cv2.getRotationMatrix2D((self.w / 2, self.h / 2), rot, scale)
        M[0, 2] += cx - self.w / 2
        M[1, 2] += cy - self.h / 2
        pts = np.array([[0, 0, 1], [self.w, 0, 1], [0, self.h, 1], [self.w, self.h, 1]]) @ M.T
        x0, y0 = np.floor(pts.min(0)).astype(int); x1, y1 = np.ceil(pts.max(0)).astype(int)
        CH, CW = canvas.shape[:2]
        x0, y0 = max(x0, 0), max(y0, 0); x1, y1 = min(x1, CW), min(y1, CH)
        if x1 <= x0 or y1 <= y0:
            return
        M2 = M.copy(); M2[0, 2] -= x0; M2[1, 2] -= y0
        size = (x1 - x0, y1 - y0)
        rgb = cv2.warpAffine(self.rgb, M2, size, flags=cv2.INTER_LINEAR)
        a = cv2.warpAffine(self.a, M2, size, flags=cv2.INTER_LINEAR)[..., None]
        reg = canvas[y0:y1, x0:x1]
        reg *= (1 - a * alpha)
        reg += rgb * alpha


def text_size(font, text):
    b = font.getbbox(text)
    return b[2] - b[0], b[3] - b[1], b


def torn_box(w, h, fill, jitter=6):
    pts = []
    for x in range(0, w + 1, 18):
        pts.append((x, random.uniform(0, jitter)))
    for y in range(0, h + 1, 18):
        pts.append((w - random.uniform(0, jitter / 2), y))
    for x in range(w, -1, -18):
        pts.append((x, h - random.uniform(0, jitter)))
    for y in range(h, -1, -18):
        pts.append((random.uniform(0, jitter / 2), y))
    return pts


def with_shadow(img, offset=(9, 11), blur=6, opacity=0.35):
    pad = 30
    out = Image.new("RGBA", (img.width + pad * 2, img.height + pad * 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
    a = img.split()[3].point(lambda v: int(v * opacity))
    shade = Image.new("RGBA", img.size, NAVY + (255,)); shade.putalpha(a)
    sh.paste(shade, (pad + offset[0], pad + offset[1]), shade)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    out.alpha_composite(sh); out.alpha_composite(img, (pad, pad))
    return out


def label_sprite(text, size=92):
    f = ImageFont.truetype(ANTON, size)
    tw, th, b = text_size(f, text)
    pw, ph = 34, 22
    w, h = tw + pw * 2, th + ph * 2
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.polygon(torn_box(w, h, MUSTARD), fill=MUSTARD + (255,))
    d.text((pw - b[0], ph - b[1]), text, font=f, fill=NAVY + (255,))
    return Sprite(with_shadow(img))


def tag_sprite(text, size=44, fg=NAVY, bg=(255, 255, 255)):
    f = ImageFont.truetype(MONT, size)
    tw, th, b = text_size(f, text)
    pw, ph = 24, 16
    w, h = tw + pw * 2, th + ph * 2
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.polygon(torn_box(w, h, bg, 4), fill=bg + (255,))
    d.text((pw - b[0], ph - b[1]), text, font=f, fill=fg + (255,))
    return Sprite(with_shadow(img, (6, 8), 5, 0.3))


def stamp_sprite(text, size=104):
    f = ImageFont.truetype(ANTON, size)
    tw, th, b = text_size(f, text)
    pw, ph, bw = 30, 18, 9
    w, h = tw + pw * 2, th + ph * 2
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle((bw // 2, bw // 2, w - bw // 2, h - bw // 2), 10, outline=RED + (255,), width=bw)
    d.text((pw - b[0], ph - b[1]), text, font=f, fill=RED + (255,))
    a = np.array(img)
    rng = np.random.default_rng(3)
    speck = rng.random(a.shape[:2]) < 0.10                     # rubber-stamp wear
    a[..., 3] = np.where(speck, (a[..., 3] * 0.35).astype(np.uint8), a[..., 3])
    return Sprite(Image.fromarray(a))


def caption_sprites(words, size=78):
    """One sprite per active word (that word in mustard)."""
    f = ImageFont.truetype(MONT, size)
    text = " ".join(words)
    tw, th, b = text_size(f, text)
    maxw = W - 120
    if tw > maxw:
        f = ImageFont.truetype(MONT, int(size * maxw / tw)); tw, th, b = text_size(f, text)
    out = []
    for k in range(len(words)):
        img = Image.new("RGBA", (tw + 40, th + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
        x = 20 - b[0]
        for j, w in enumerate(words):
            col = MUSTARD if j == k else (255, 255, 255)
            d.text((x, 20 - b[1]), w, font=f, fill=col + (255,), stroke_width=9, stroke_fill=NAVY + (255,))
            x += f.getlength(w + " ")
        out.append(Sprite(img))
    return out


# ---------------- scene layers ----------------
def prepare_scene(d, img_name, use_cutout):
    im = cv2.cvtColor(cv2.imread(str(d / img_name)), cv2.COLOR_BGR2RGB)
    scale = W / im.shape[1]
    big = cv2.resize(im, (W, round(im.shape[0] * scale)), interpolation=cv2.INTER_LANCZOS4)
    bh = big.shape[0]
    top = (bh - H) // 2 if bh > H else 0
    if bh < H:
        big = cv2.resize(im, (round(im.shape[1] * H / im.shape[0]), H), interpolation=cv2.INTER_LANCZOS4)
        left = (big.shape[1] - W) // 2; big = big[:, left:left + W]; top = 0
    base = big[top:top + H] if big.shape[0] >= H else big
    sticker = None
    if use_cutout:
        m = cv2.imread(str(d / "layers" / f"{img_name[:2]}_mask.png"), cv2.IMREAD_GRAYSCALE)
        m = cv2.resize(m, (big.shape[1], big.shape[0]))[top:top + H]
        hard = (m > 110).astype(np.uint8) * 255
        # background with subject painted out (done small, then upscaled)
        sm = cv2.resize(base, (W // 3, H // 3)); smm = cv2.resize(cv2.dilate(hard, np.ones((25, 25))), (W // 3, H // 3))
        filled = cv2.inpaint(sm, smm, 9, cv2.INPAINT_TELEA)
        filled = cv2.GaussianBlur(cv2.resize(filled, (W, H)), (0, 0), 3)
        mk = (cv2.GaussianBlur(cv2.dilate(hard, np.ones((25, 25))), (0, 0), 6) / 255.0)[..., None]
        bg = (base * (1 - mk) + filled * mk).astype(np.uint8)
        # sticker: subject + white outline + shadow, cropped to bbox
        alpha = cv2.GaussianBlur(hard, (0, 0), 1.2)
        outline = cv2.GaussianBlur(cv2.dilate(hard, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (23, 23))), (0, 0), 1.5)
        ys, xs = np.where(outline > 10)
        y0, y1 = max(ys.min() - 30, 0), min(ys.max() + 30, H); x0, x1 = max(xs.min() - 30, 0), min(xs.max() + 30, W)
        rgba = np.zeros((H, W, 4), np.float32)
        oa = outline[..., None] / 255.0; sa = alpha[..., None] / 255.0
        rgba[..., :3] = 255 * oa * (1 - sa) + base * sa
        rgba[..., 3:] = 255 * np.maximum(oa, sa)
        img = Image.fromarray(rgba[y0:y1, x0:x1].astype(np.uint8), "RGBA")
        sticker = (Sprite(with_shadow(img, (10, 14), 10, 0.35)), ((x0 + x1) / 2, (y0 + y1) / 2))
    else:
        bg = base
    return {"bg": bg.astype(np.float32) / 255.0, "sticker": sticker}


def render_bg(scene, t, dur, idx):
    zin = idx % 2 == 0
    p = t / max(dur, 0.1)
    s = (1.0 + 0.07 * p) if zin else (1.07 - 0.07 * p)
    if scene["sticker"] is None:
        s += 0.05 * (1 - ease_out(t / 0.5))        # punch-in on flat scenes
        s += 0.03 * p
    dx = (12 if idx % 3 else -12) * p
    M = np.float32([[s, 0, (1 - s) * W / 2 + dx], [0, s, (1 - s) * H / 2]])
    return cv2.warpAffine(scene["bg"], M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT), s, dx


def render_frame(scene, spec, t, dur, idx):
    canvas, s, dx = render_bg(scene, t, dur, idx)
    canvas = canvas.copy()
    if scene["sticker"] is not None:
        sp, (cx, cy) = scene["sticker"]
        pop = back_out(t / 0.45)
        k = (0.78 + 0.22 * pop) * (1 + 0.035 * t / max(dur, 0.1))
        bob = 7 * math.sin(t * 2.1)
        px = W / 2 + s * (cx - W / 2) + dx * 0.4
        py = H / 2 + s * (cy - H / 2) + bob
        sp.draw(canvas, px, py, s * k, 0, min(1.0, t / 0.12))
    for el in spec:
        lt = t - el["t"]
        if lt < 0:
            continue
        if el["kind"] in ("label", "tag"):
            sc = back_out(lt / 0.38)
            el["sprite"].draw(canvas, el["x"], el["y"], sc, el["rot"] * sc, min(1, lt / 0.08))
        elif el["kind"] == "stamp":
            p = ease_out(lt / 0.16)
            el["sprite"].draw(canvas, el["x"], el["y"], 2.3 - 1.3 * p, el["rot"], min(1, lt / 0.06))
    return canvas


# ---------------- audio ----------------
def sfx_track(n, events):
    out = np.zeros(n, np.float32); rng = np.random.default_rng(1)
    def add(at, sig):
        i = int(at * SR)
        if 0 <= i < n:
            j = min(n, i + len(sig)); out[i:j] += sig[:j - i]
    for at, kind in events:
        if kind == "pop":
            L = int(0.09 * SR); tt = np.arange(L) / SR
            f = 900 * np.exp(-tt * 25) + 300
            add(at, 0.35 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 45))
        elif kind == "whoosh":
            L = int(0.35 * SR); tt = np.arange(L) / SR
            noise = rng.standard_normal(L).astype(np.float32)
            env = np.sin(np.pi * tt / tt[-1]) ** 2
            b = np.convolve(noise, np.ones(12) / 12, "same")
            add(at - 0.15, 0.22 * b * env)
        elif kind == "thud":
            L = int(0.3 * SR); tt = np.arange(L) / SR
            body = np.sin(2 * np.pi * (110 * np.exp(-tt * 9) + 45) * tt) * np.exp(-tt * 14)
            click = rng.standard_normal(L) * np.exp(-tt * 90)
            add(at, 0.55 * body + 0.25 * click)
    return out


def write_wav(path, x):
    x = np.clip(x, -1, 1)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


# ---------------- main ----------------
def main():
    d = Path(sys.argv[1]).resolve()
    cfg = json.loads((d / "script.json").read_text(encoding="utf-8"))
    sentences, scenes = cfg["sentences"], cfg["scenes"]
    fx = cfg.get("fx", {})
    cutouts = set(cfg.get("cutouts", []))
    asr = json.loads((d / "words.json").read_text(encoding="utf-8"))
    total = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                  "-of", "csv=p=0", d / "raw.wav"], capture_output=True, text=True).stdout)
    sw = [(w, si) for si, s in enumerate(sentences) for w in s.split()]
    times, _ = build.align([w for w, _ in sw], asr)
    tmap, pieces, new_total = build.make_timemap(build.speech_regions(d / "raw.wav", total))
    nt = [(tmap(s), tmap(e)) for s, e in times]

    def word_time(si, prefix):
        for (w, s_i), (s, e) in zip(sw, nt):
            if s_i == si and build.norm(w).startswith(build.norm(prefix)):
                return s
        return next(s for (w, s_i), (s, e) in zip(sw, nt) if s_i == si)

    sent_start = {}
    for (w, si), (s, e) in zip(sw, nt):
        sent_start.setdefault(si, s)
    starts = [0.0] + [max(0.0, sent_start[sc[0]] - 0.12) for sc in scenes[1:]]
    ends = starts[1:] + [new_total]

    # build scene specs
    print("Preparing layers...")
    prepared, specs, sfx = [], [], []
    for i, sc in enumerate(scenes):
        prepared.append(prepare_scene(d, sc[1], sc[1] in cutouts))
        spec = [{"kind": "label", "t": 0.15, "sprite": label_sprite(sc[2]), "x": W / 2, "y": 215,
                 "rot": random.choice([-2.2, -1.5, 1.5, 2.2])}]
        sfx += [(starts[i], "whoosh"), (starts[i] + 0.15, "pop")]
        tag_y = 345
        for e in fx.get(str(i + 1), []):
            at = word_time(e["s"], e["w"]) - starts[i]
            if e["k"] == "tag":
                x = e.get("x", W / 2); y = e.get("y", tag_y)
                if "y" not in e:
                    tag_y += 88
                spec.append({"kind": "tag", "t": at, "sprite": tag_sprite(e["text"], fg=e.get("fg") and tuple(e["fg"]) or NAVY),
                             "x": x, "y": y, "rot": random.uniform(-2, 2)})
                sfx.append((starts[i] + at, "pop"))
            else:
                spec.append({"kind": "stamp", "t": at, "sprite": stamp_sprite(e["text"]),
                             "x": e.get("x", W / 2), "y": e.get("y", 1120), "rot": e.get("rot", -8)})
                sfx.append((starts[i] + at + 0.14, "thud"))
                e["_hit"] = starts[i] + at + 0.14
        specs.append(spec)
    shakes = [e["_hit"] for v in fx.values() for e in v if "_hit" in e]

    # captions
    chunks, cur = [], []
    for k, ((w, si), (s, e)) in enumerate(zip(sw, nt)):
        cur.append((w.upper(), s, e))
        last = k == len(sw) - 1 or sw[k + 1][1] != si
        if len(cur) == 3 or last or w.endswith((",", ":")):
            chunks.append(cur); cur = []
    cap = []
    for ci, ch in enumerate(chunks):
        st = ch[0][1]; en = chunks[ci + 1][0][1] if ci + 1 < len(chunks) else new_total
        en = min(en, max(ch[-1][2] + 0.4, st + 0.4))
        cap.append((st, en, [x[1] for x in ch], caption_sprites([x[0] for x in ch])))

    # render
    nframes = int(new_total * FPS)
    print(f"Rendering {nframes} frames...")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
                           "-crf", "19", "-pix_fmt", "yuv420p", str(d / "tmp" / "v2_video.mp4")], stdin=subprocess.PIPE)
    ci = 0
    for fi in range(nframes):
        t = fi / FPS
        i = max(k for k in range(len(scenes)) if starts[k] <= t)
        dur = ends[i] - starts[i]
        frame = render_frame(prepared[i], specs[i], t - starts[i], dur, i)
        if i + 1 < len(scenes) and ends[i] - t < DISSOLVE:      # dissolve into next scene
            w = 1 - (ends[i] - t) / DISSOLVE
            nxt = render_frame(prepared[i + 1], specs[i + 1], 0.0, ends[i + 1] - starts[i + 1], i + 1)
            frame = frame * (1 - w) + nxt * w
        while ci + 1 < len(cap) and cap[ci + 1][0] <= t:
            ci += 1
        st, en, wst, sprs = cap[ci]
        if st <= t < en:
            k = max(j for j in range(len(wst)) if wst[j] <= t or j == 0)
            sc = 0.9 + 0.1 * back_out((t - st) / 0.18)
            sprs[k].draw(frame, W / 2, 1560, sc)
        for hit in shakes:
            if 0 <= t - hit < 0.25:
                amp = 14 * (1 - (t - hit) / 0.25)
                M = np.float32([[1, 0, random.uniform(-amp, amp)], [0, 1, random.uniform(-amp, amp)]])
                frame = cv2.warpAffine(frame, M, (W, H), borderMode=cv2.BORDER_REFLECT)
        ff.stdin.write((np.clip(frame, 0, 1) * 255).astype(np.uint8).tobytes())
        if fi % 300 == 0:
            print(f"  {fi}/{nframes}", flush=True)
    ff.stdin.close(); ff.wait()

    # audio: voice + sfx + ducked music
    n = int(new_total * SR)
    write_wav(d / "tmp" / "sfx.wav", sfx_track(n, sfx))
    music = d / "music.wav"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", d / "tmp" / "v2_video.mp4",
           "-i", d / "tmp" / "voice_clean.wav", "-i", d / "tmp" / "sfx.wav"]
    if music.exists():
        cmd += ["-stream_loop", "-1", "-i", music]
        fc = ("[1:a]asplit=2[v][vk];[3:a]volume=0.32,afade=t=out:st=%.2f:d=1.5[m];"
              "[m][vk]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[md];"
              "[v][2:a][md]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.95[a]") % (new_total - 1.5)
    else:
        fc = "[1:a][2:a]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]"
    cmd += ["-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-t", f"{new_total:.2f}",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", d / "final_v2.mp4"]
    subprocess.run([str(c) for c in cmd], check=True)
    print("Done:", d / "final_v2.mp4")


if __name__ == "__main__":
    main()
