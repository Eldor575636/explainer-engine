#!/usr/bin/env python3
"""v3 long-form renderer: 16:9 1920x1080, beat-based storyboard with scene types
(scene, object, map, number, title, chapter, portrait), word-triggered overlays
(label, tag, stamp, circle, arrow, pin, mascot, prop, counter, bigtext, rings),
highlighted captions, dissolves, synthesized SFX and mood-switching ducked music.

Usage: python3 v3.py <beats.json> <work_dir> <out.mp4>
work_dir must hold raw.wav (voice) and words.json (transcribe.py output).
"""
import json, math, random, subprocess, sys
from pathlib import Path
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import build, motion

W, H, FPS, SR = 1920, 1080, 25, 48000
motion.W, motion.H = W, H                       # Sprite.draw / captions read these
NAVY, MUSTARD, RED, CREAM = motion.NAVY, motion.MUSTARD, motion.RED, motion.CREAM
INK = (14, 22, 38)
DISSOLVE = 0.25
back_out, ease_out = motion.back_out, motion.ease_out
build.KEEP_PAUSE, build.PAD = 0.45, 0.14         # long-form keeps a little more breath


# ---------------- cut-outs ----------------
_session = None
def mask_for(path, cache):
    global _session
    mp = cache / (path.stem + "_mask.png")
    if not mp.exists():
        from rembg import remove, new_session
        _session = _session or new_session("u2net")
        remove(Image.open(path).convert("RGB"), session=_session, only_mask=True).save(mp)
    return np.array(Image.open(mp).convert("L"))


def sticker(path, cache, height_px, part=None, nparts=3, outline=14):
    rgb = np.array(Image.open(path).convert("RGB"))
    hard = (mask_for(path, cache) > 110).astype(np.uint8)
    if part is not None:
        grown = cv2.dilate(hard, np.ones((31, 31), np.uint8))
        n, lab, stats, cents = cv2.connectedComponentsWithStats(grown)
        comps = sorted(range(1, n), key=lambda i: -stats[i, cv2.CC_STAT_AREA])[:nparts]
        comps = sorted(comps, key=lambda i: cents[i][0])
        hard = hard * (lab == comps[part]).astype(np.uint8)
    hard *= 255
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * outline + 1, 2 * outline + 1))
    out_a = cv2.GaussianBlur(cv2.dilate(hard, k), (0, 0), 1.5)
    sub_a = cv2.GaussianBlur(hard, (0, 0), 1.0)
    ys, xs = np.where(out_a > 10)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    oa = out_a[y0:y1, x0:x1, None] / 255.0; sa = sub_a[y0:y1, x0:x1, None] / 255.0
    rgba = np.zeros((y1 - y0, x1 - x0, 4), np.float32)
    rgba[..., :3] = 255 * oa * (1 - sa) + rgb[y0:y1, x0:x1] * sa
    rgba[..., 3:] = 255 * np.maximum(oa, sa)
    img = Image.fromarray(rgba.astype(np.uint8), "RGBA")
    s = height_px / img.height
    img = img.resize((max(1, int(img.width * s)), int(height_px)), Image.LANCZOS)
    return motion.Sprite(motion.with_shadow(img, (10, 14), 10, 0.35))


# ---------------- backgrounds ----------------
def cover(img, crop=None, tint=0.0):
    a = np.array(img.convert("RGB")).astype(np.float32) / 255.0
    h, w = a.shape[:2]
    if crop == "left":
        a = a[:, : int(w * 0.75)]
    elif crop == "right":
        a = a[:, int(w * 0.25):]
    h, w = a.shape[:2]
    s = max(W / w, H / h)
    a = cv2.resize(a, (int(w * s) + 1, int(h * s) + 1), interpolation=cv2.INTER_AREA)
    y0, x0 = (a.shape[0] - H) // 2, (a.shape[1] - W) // 2
    a = a[y0:y0 + H, x0:x0 + W]
    if tint:
        a = a * (1 - tint) + np.array(INK, np.float32) / 255 * tint
    return a


def cream_bg():
    a = np.ones((H, W, 3), np.float32) * np.array(CREAM, np.float32) / 255
    img = Image.new("L", (W, H), 0); d = ImageDraw.Draw(img)
    for y in range(0, H, 14):
        for x in range((y // 14) % 2 * 7, W, 14):
            d.ellipse((x, y, x + 2.4, y + 2.4), fill=255)
    dots = np.array(img, np.float32)[..., None] / 255 * 0.07
    yy, xx = np.mgrid[0:H, 0:W]
    vig = (((xx - W / 2) / W) ** 2 + ((yy - H / 2) / H) ** 2)[..., None] * 0.35
    navy = np.array(NAVY, np.float32) / 255
    return a * (1 - dots - vig * 0.35) + navy * (dots + vig * 0.35)


def solid(rgb):
    return np.ones((H, W, 3), np.float32) * np.array(rgb, np.float32) / 255


def push(bg, t, dur, idx, amount=0.06):
    p = t / max(dur, 0.1)
    s = 1 + amount * p if idx % 2 == 0 else 1 + amount * (1 - p)
    dx = (18 if idx % 3 else -18) * p
    M = np.float32([[s, 0, (1 - s) * W / 2 + dx], [0, s, (1 - s) * H / 2]])
    return cv2.warpAffine(bg, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


# ---------------- text sprites ----------------
def text_sprite(text, font, size, fill, stroke=0, stroke_fill=NAVY):
    f = ImageFont.truetype(font, size)
    tw, th, b = motion.text_size(f, text)
    pad = 20 + stroke
    img = Image.new("RGBA", (tw + 2 * pad, th + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(img).text((pad - b[0], pad - b[1]), text, font=f, fill=fill + (255,),
                             stroke_width=stroke, stroke_fill=stroke_fill + (255,))
    return motion.Sprite(img)


def seeded(fn, *a, **k):
    random.seed(7)
    return fn(*a, **k)


# ---------------- drawing helpers ----------------
def draw_partial(canvas, pts, frac, color, thick):
    n = max(2, int(len(pts) * min(max(frac, 0), 1)))
    poly = np.int32(pts[:n] * 4)
    col = tuple(c / 255 for c in color)
    cv2.polylines(canvas, [poly], False, col, thick, cv2.LINE_AA, shift=2)
    return pts[n - 1], pts[max(0, n - 6)]


def arrowhead(canvas, tip, back, color, size=34):
    d = tip - back
    if np.linalg.norm(d) < 1e-3:
        return
    d = d / np.linalg.norm(d); n = np.array([-d[1], d[0]])
    p = np.array([tip, tip - d * size + n * size * 0.55, tip - d * size - n * size * 0.55])
    cv2.fillPoly(canvas, [np.int32(p * 4)], tuple(c / 255 for c in color), cv2.LINE_AA, shift=2)


def curve(a, b, straight=False, n=120):
    a, b = np.array(a, float), np.array(b, float)
    t = np.linspace(0, 1, n)[:, None]
    if straight:
        return a + (b - a) * t
    mid = (a + b) / 2 + np.array([0, -abs(b[0] - a[0]) * 0.28])
    return (1 - t) ** 2 * a + 2 * (1 - t) * t * mid + t ** 2 * b


def ellipse_pts(cx, cy, rx, ry, n=160):
    rng = np.random.default_rng(5)
    th = np.linspace(-0.3, 2 * math.pi + 0.35, n)
    j = 1 + rng.normal(0, 0.012, n).cumsum() * 0.15
    return np.stack([cx + rx * j * np.cos(th), cy + ry * j * np.sin(th)], 1)


# ---------------- audio ----------------
def synth_sfx(n, events):
    out = motion.sfx_track(n, [(t, k) for t, k in events if k in ("pop", "whoosh", "thud")])
    rng = np.random.default_rng(2)
    def add(at, sig):
        i = int(at * SR)
        if 0 <= i < n:
            j = min(n, i + len(sig)); out[i:j] += sig[:j - i]
    for at, k in events:
        if k == "tick":
            L = int(0.03 * SR); tt = np.arange(L) / SR
            add(at, 0.18 * np.sin(2 * np.pi * 2200 * tt) * np.exp(-tt * 160))
        elif k == "riser":
            L = int(0.9 * SR); tt = np.arange(L) / SR
            nz = np.convolve(rng.standard_normal(L), np.ones(6) / 6, "same")
            add(at - 0.9, 0.16 * nz * (tt / tt[-1]) ** 2)
        elif k == "draw":
            L = int(0.7 * SR); tt = np.arange(L) / SR
            nz = np.convolve(rng.standard_normal(L), np.ones(3) / 3, "same")
            add(at, 0.06 * nz * np.sin(np.pi * tt / tt[-1]))
    return out


def load_audio(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def music_bed(n, segments, files):
    """segments: [(start_s, mood)], crossfaded, each mood keeps its own playhead (looped)."""
    tracks = {m: load_audio(p) for m, p in files.items()}
    heads = {m: 0 for m in tracks}
    out = np.zeros(n, np.float32); xf = int(1.5 * SR)
    bounds = [int(s * SR) for s, _ in segments] + [n]
    for (s, mood), a, b in zip(segments, bounds, bounds[1:]):
        tr = tracks[mood]; L = min(n, b + xf) - a
        idx = (heads[mood] + np.arange(L)) % len(tr)
        seg = tr[idx].copy()
        if a > 0:
            seg[:xf] *= np.linspace(0, 1, min(xf, L))[: len(seg[:xf])]
        if b < n:
            tail = seg[b - a:]; tail *= np.linspace(1, 0, len(tail))
        out[a:a + L] += seg
        heads[mood] += b - a
    return out


# ---------------- main ----------------
def main():
    cfg_path, work, out_path = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
    proj = cfg_path.parent
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    layers = proj / cfg["layers"]
    cache = work / "cache"; cache.mkdir(exist_ok=True)
    sentences, beats = cfg["sentences"], cfg["beats"]

    # --- timing ---
    asr = json.loads((work / "words.json").read_text(encoding="utf-8"))
    total = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                  work / "raw.wav"], capture_output=True, text=True).stdout)
    sw = [(w, si) for si, s in enumerate(sentences) for w in s.split()]
    times, matched = build.align([w for w, _ in sw], asr)
    print(f"Aligned {matched}/{len(sw)} words")
    regions = build.speech_regions(work / "raw.wav", total)
    tmap, pieces, T = build.make_timemap(regions)
    nt = [(tmap(s), tmap(e)) for s, e in times]
    print(f"Voice {total:.1f}s -> {T:.1f}s")

    def wt(at):
        si, pre = at
        for (w, s_i), (s, e) in zip(sw, nt):
            if s_i == si and build.norm(w).startswith(build.norm(pre)):
                return s
        print(f"  ! '{pre}' not found in sentence {si}, using sentence start")
        return next(s for (w, s_i), (s, e) in zip(sw, nt) if s_i == si)

    # --- clean voice (same chain as build.py) ---
    parts = "".join(f"[0:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS[p{i}];" for i, (s, e, _) in enumerate(pieces))
    gaps, chain = [], ""
    for i, (s, e, ns) in enumerate(pieces):
        if i:
            g = ns - (pieces[i - 1][2] + pieces[i - 1][1] - pieces[i - 1][0])
            if g > 0.001:
                gaps.append(f"anullsrc=r=48000:cl=mono,atrim=0:{g:.3f}[g{i}];"); chain += f"[g{i}]"
        chain += f"[p{i}]"
    fc = parts + "".join(gaps) + chain + f"concat=n={chain.count('[')}:v=0:a=1,highpass=f=80,acompressor=threshold=0.1:ratio=3:attack=10:release=200,loudnorm=I=-16:TP=-2:LRA=9[a]"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(work / "raw.wav"), "-filter_complex", fc,
                    "-map", "[a]", "-ar", "48000", str(work / "voice_clean.wav")], check=True)

    # --- beats ---
    starts = [0.0] + [max(0.0, wt(b["at"]) - 0.12) for b in beats[1:]]
    ends = starts[1:] + [T]
    sfx, shakes, music_segs, mood = [], [], [], "curious"
    cream = cream_bg()
    pose_sprites = {}
    def pose(i, side):
        key = (i, side)
        if key not in pose_sprites:
            pose_sprites[key] = sticker(layers / "mascot_sheet.jpg", cache, H * (0.78 if side == "center" else 0.68), part=i, nparts=3)
        return pose_sprites[key]

    print("Preparing beats...")
    for bi, b in enumerate(beats):
        b["t0"], b["t1"] = starts[bi], ends[bi]
        if b.get("mood", mood) != mood or bi == 0:
            mood = b.get("mood", mood); music_segs.append((starts[bi], mood))
        typ = b["type"]
        if typ in ("scene", "map"):
            b["_bg"] = cover(Image.open(layers / f"{b['bg']}.jpg"), b.get("crop"), b.get("tint", 0))
        elif typ in ("object", "number"):
            b["_bg"] = cream
        elif typ in ("title", "chapter"):
            b["_bg"] = solid(NAVY)
        elif typ == "portrait":
            bg = cream.copy(); bg[:, : int(W * 0.46)] = np.array(MUSTARD, np.float32) / 255
            b["_bg"] = bg
            b["_fig"] = sticker(layers / f"{b['fig']}.jpg", cache, H * 0.86)
        if "fig" in b and isinstance(b["fig"], dict):
            b["_fig"] = sticker(layers / f"{b['fig']['img']}.jpg", cache, H * b["fig"]["h"])
        b["_props"] = []
        for p in b.get("props", []):
            sp = sticker(layers / f"{p['img']}.jpg", cache, H * p["h"], part=p.get("part"))
            at = wt(p["at"]) - b["t0"]
            b["_props"].append((sp, p, at))
            sfx.append((b["t0"] + at, "thud" if p.get("slam") else "pop"))
            if p.get("slam"):
                shakes.append(b["t0"] + at + 0.14)
        if typ == "number":
            b["_prop"] = sticker(layers / f"{b['prop']}.jpg", cache, H * 0.55)
            b["_val"] = text_sprite(b["value"], motion.ANTON, 300, MUSTARD, 12)
            b["_sub"] = seeded(motion.tag_sprite, b["sub"], 50)
            b["_show"] = wt(b["show"]) - b["t0"]
            sfx.append((b["t0"] + b["_show"], "thud"))
        if typ == "title":
            b["_t1"] = text_sprite(b["title"], motion.ANTON, 120, CREAM)
            b["_t2"] = text_sprite(b["title2"], motion.ANTON, 150, MUSTARD)
            sfx += [(b["t0"] + 0.05, "riser"), (b["t0"] + 0.15, "thud")]
        if typ == "chapter":
            b["_n"] = text_sprite(b["num"], motion.ANTON, 80, MUSTARD)
            b["_t"] = text_sprite(b["title"], motion.ANTON, 220, CREAM)
            sfx += [(b["t0"] + 0.05, "riser"), (b["t0"] + 0.2, "thud")]
        if bi:
            sfx.append((b["t0"], "whoosh"))
        tag_slot = 0
        evs = []
        for e in b.get("ev", []):
            e = dict(e); e["t"] = wt(e["at"]) - b["t0"]; k = e["k"]
            if k == "label":
                e["_s"] = seeded(motion.label_sprite, e["text"], 84); e["x"], e["y"] = W / 2, 105
                e["rot"] = random.choice([-1.5, 1.5]); sfx.append((b["t0"] + e["t"], "pop"))
            elif k == "tag":
                fg = RED if e.get("fg") == "red" else NAVY
                e["_s"] = seeded(motion.tag_sprite, e["text"], 50, fg)
                if "x" in e:
                    e["x"], e["y"] = e["x"] * W, e["y"] * H
                else:
                    e["x"], e["y"] = W * 0.74, 230 + 92 * tag_slot; tag_slot += 1
                e["rot"] = random.uniform(-2, 2); sfx.append((b["t0"] + e["t"], "pop"))
            elif k == "stamp":
                e["_s"] = seeded(motion.stamp_sprite, e["text"], 130); e["x"], e["y"] = W * 0.5, H * 0.46
                sfx.append((b["t0"] + e["t"] + 0.14, "thud")); shakes.append(b["t0"] + e["t"] + 0.14)
            elif k == "circle":
                e["_pts"] = ellipse_pts(e["x"] * W, e["y"] * H, e["rx"] * W, e["ry"] * H); sfx.append((b["t0"] + e["t"], "draw"))
            elif k == "arrow":
                e["_pts"] = curve((e["from"][0] * W, e["from"][1] * H), (e["to"][0] * W, e["to"][1] * H), e.get("straight", False))
                sfx.append((b["t0"] + e["t"], "draw"))
            elif k == "mascot":
                e["_s"] = pose(e["pose"], e["side"]); sfx.append((b["t0"] + e["t"], "whoosh"))
            elif k == "prop":
                e["_s"] = sticker(layers / f"{e['img']}.jpg", cache, H * e["h"]); sfx.append((b["t0"] + e["t"], "pop"))
            elif k == "counter":
                e["_frames"] = [seeded(motion.label_sprite, f"{v}{e.get('suffix', '')}", 150) for v in range(e["to"] + 1)]
                sfx += [(b["t0"] + e["t"] + 0.9 * i / 12, "tick") for i in range(12)]
            elif k == "bigtext":
                e["_s"] = text_sprite(e["text"], motion.ANTON, 300, RED, 0); sfx.append((b["t0"] + e["t"], "pop"))
            evs.append(e)
        b["_ev"] = evs

    # --- captions: up to 5 words, never across sentences ---
    chunks, cur = [], []
    for k, ((w, si), (s, e)) in enumerate(zip(sw, nt)):
        cur.append((w.upper(), s, e))
        last = k == len(sw) - 1 or sw[k + 1][1] != si
        if len(cur) == 5 or last or w.endswith((",", ":")):
            chunks.append(cur); cur = []
    caps = []
    for ci, ch in enumerate(chunks):
        st = ch[0][1]; en = chunks[ci + 1][0][1] if ci + 1 < len(chunks) else T
        en = min(en, max(ch[-1][2] + 0.5, st + 0.5))
        caps.append((st, en, [x[1] for x in ch], motion.caption_sprites([x[0] for x in ch], 50)))

    def render(bi, t):
        b = beats[bi]; dur = b["t1"] - b["t0"]; typ = b["type"]
        if typ in ("scene", "map"):
            c = push(b["_bg"], t, dur, bi, 0.07 if typ == "scene" else 0.05)
        else:
            c = b["_bg"].copy()
        if typ == "scene" and "_fig" in b:
            f = b["fig"]; tx = f["x"] * W
            x = tx - (1 - ease_out(t / 0.7)) * W * 0.55
            fh = b["_fig"].h; y = H - fh / 2 + 10 + 5 * math.sin(t * 2)
            b["_fig"].draw(c, x, y, 1.0, 0, min(1, t / 0.15))
        if typ == "portrait":
            sp = b["_fig"]; x = W * 0.23 - (1 - ease_out(t / 0.7)) * W * 0.4
            sp.draw(c, x, H - sp.h / 2 + 30, 1.0, 0, min(1, t / 0.15))
        for sp, p, at in b["_props"]:
            lt = t - at
            if lt < 0:
                continue
            if p.get("slam"):
                sc = 2.2 - 1.2 * ease_out(lt / 0.16)
            else:
                sc = back_out(lt / 0.4)
            sp.draw(c, p["x"] * W, p["y"] * H + 6 * math.sin(lt * 2.2), sc * (1 + 0.02 * lt / max(dur, 1)),
                    math.sin(lt * 1.3) * 1.2, min(1, lt / 0.1))
        if typ == "number":
            b["_prop"].draw(c, W * 0.27, H * 0.5 + 6 * math.sin(t * 2), back_out(t / 0.4))
            lt = t - b["_show"]
            if lt >= 0:
                b["_val"].draw(c, W * 0.66, H * 0.43, 1.8 - 0.8 * ease_out(lt / 0.2), 0, min(1, lt / 0.08))
                b["_sub"].draw(c, W * 0.66, H * 0.68, back_out((lt - 0.3) / 0.4), -1.5, min(1, max(0, lt - 0.3) / 0.1))
        if typ == "title":
            b["_t1"].draw(c, W / 2, H * 0.40, 1.5 - 0.5 * ease_out(t / 0.25), 0, min(1, t / 0.1))
            lt = t - 0.35
            if lt > 0:
                b["_t2"].draw(c, W / 2, H * 0.58, 1.5 - 0.5 * ease_out(lt / 0.25), 0, min(1, lt / 0.1))
                cv2.line(c, (int(W * 0.25), int(H * 0.72)), (int(W * 0.25 + W * 0.5 * ease_out(lt / 0.6)), int(H * 0.72)),
                         tuple(v / 255 for v in RED), 8, cv2.LINE_AA)
        if typ == "chapter":
            b["_n"].draw(c, W / 2, H * 0.36, back_out(t / 0.35), 0, min(1, t / 0.1))
            lt = t - 0.2
            if lt > 0:
                b["_t"].draw(c, W / 2, H * 0.56, 1.6 - 0.6 * ease_out(lt / 0.2), 0, min(1, lt / 0.08))
                cv2.line(c, (int(W * 0.3), int(H * 0.73)), (int(W * 0.3 + W * 0.4 * ease_out(lt / 0.5)), int(H * 0.73)),
                         tuple(v / 255 for v in RED), 10, cv2.LINE_AA)
        for e in b["_ev"]:
            lt = t - e["t"]
            if lt < 0:
                continue
            k = e["k"]
            if k in ("label", "tag"):
                sc = back_out(lt / 0.38)
                e["_s"].draw(c, e["x"], e["y"], sc, e["rot"] * sc, min(1, lt / 0.08))
            elif k == "stamp":
                e["_s"].draw(c, e["x"], e["y"], 2.3 - 1.3 * ease_out(lt / 0.16), -7, min(1, lt / 0.06))
            elif k == "circle":
                draw_partial(c, e["_pts"], ease_out(lt / 0.7), RED, 9)
            elif k == "arrow":
                tip, back = draw_partial(c, e["_pts"], ease_out(lt / 0.8), RED, 10)
                if lt > 0.1:
                    arrowhead(c, np.array(tip), np.array(back), RED)
            elif k == "pin":
                x, y = int(e["x"] * W), int(e["y"] * H)
                cv2.circle(c, (x, y), int(14 * back_out(lt / 0.3)), tuple(v / 255 for v in RED), -1, cv2.LINE_AA)
                r = int(14 + (lt % 1.2) * 60)
                cv2.circle(c, (x, y), r, tuple(v / 255 for v in RED), 3, cv2.LINE_AA)
            elif k == "mascot":
                sp = e["_s"]; x = W * (0.83 if e["side"] == "right" else 0.5)
                y = H - sp.h / 2 + 25 + (1 - ease_out(lt / 0.6)) * sp.h * 0.9
                sp.draw(c, x, y + 4 * math.sin(lt * 2), 1.0)
            elif k == "prop":
                sc = back_out(lt / 0.4) * ((0.8 + 0.5 * ease_out(lt / max(dur - e["t"], 1))) if e.get("grow") else 1)
                e["_s"].draw(c, e["x"] * W, e["y"] * H + 6 * math.sin(lt * 2), sc, 0, min(1, lt / 0.1))
            elif k == "counter":
                fr = e["_frames"]; v = int(round((len(fr) - 1) * ease_out(lt / 0.9)))
                fr[v].draw(c, e["x"] * W, e["y"] * H, back_out(lt / 0.3), 0, min(1, lt / 0.08))
            elif k == "bigtext":
                e["_s"].draw(c, e["x"] * W, e["y"] * H, back_out(lt / 0.35), 0, min(1, lt / 0.08))
            elif k == "rings":
                for j in range(3):
                    ph = (lt - j * 0.45) % 1.35
                    if lt - j * 0.45 < 0:
                        continue
                    r = int(80 + ph * 420); a = max(0, 1 - ph / 1.35)
                    ov = c.copy()
                    cv2.circle(ov, (int(e["x"] * W), int(e["y"] * H)), r, tuple(v / 255 for v in RED), 6, cv2.LINE_AA)
                    c = c * (1 - a) + ov * a
        return c

    # --- render ---
    nframes = int(T * FPS)
    print(f"Rendering {nframes} frames at {W}x{H}...")
    tmp_video = work / "v3_video.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                           "-pix_fmt", "yuv420p", str(tmp_video)], stdin=subprocess.PIPE)
    ci, bi = 0, 0
    rng = random.Random(3)
    for fi in range(nframes):
        t = fi / FPS
        while bi + 1 < len(beats) and beats[bi + 1]["t0"] <= t:
            bi += 1
        frame = render(bi, t - beats[bi]["t0"])
        if bi + 1 < len(beats) and beats[bi]["t1"] - t < DISSOLVE:
            w = 1 - (beats[bi]["t1"] - t) / DISSOLVE
            frame = frame * (1 - w) + render(bi + 1, 0.0) * w
        while ci + 1 < len(caps) and caps[ci + 1][0] <= t:
            ci += 1
        st, en, wst, sprs = caps[ci]
        if st <= t < en:
            k = max(j for j in range(len(wst)) if wst[j] <= t or j == 0)
            sprs[k].draw(frame, W / 2, H - 78, 0.94 + 0.06 * back_out((t - st) / 0.18))
        for hit in shakes:
            if 0 <= t - hit < 0.25:
                amp = 16 * (1 - (t - hit) / 0.25)
                M = np.float32([[1, 0, rng.uniform(-amp, amp)], [0, 1, rng.uniform(-amp, amp)]])
                frame = cv2.warpAffine(frame, M, (W, H), borderMode=cv2.BORDER_REFLECT)
        ff.stdin.write((np.clip(frame, 0, 1) * 255).astype(np.uint8).tobytes())
        if fi % 500 == 0:
            print(f"  {fi}/{nframes}", flush=True)
    ff.stdin.close(); ff.wait()

    # --- audio mix ---
    n = int(T * SR)
    motion.write_wav(work / "sfx.wav", synth_sfx(n, sfx))
    files = {m: (proj / p).resolve() for m, p in cfg["music"].items()}
    motion.write_wav(work / "music.wav", 0.9 * music_bed(n, music_segs, files))
    fc = ("[1:a]asplit=2[v][vk];[3:a]volume=0.30,afade=t=in:d=1.0,afade=t=out:st=%.2f:d=2.5[m];"
          "[m][vk]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=450[md];"
          "[v][2:a][md]amix=inputs=3:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]") % max(0, T - 2.5)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(tmp_video), "-i", str(work / "voice_clean.wav"),
                    "-i", str(work / "sfx.wav"), "-i", str(work / "music.wav"), "-filter_complex", fc,
                    "-map", "0:v", "-map", "[a]", "-t", f"{T:.2f}", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-ar", "48000", "-movflags", "+faststart", str(out_path)], check=True)
    (work / "beat_times.json").write_text(json.dumps([[b["type"], round(b["t0"], 2), round(b["t1"], 2)] for b in beats]))
    print("Done:", out_path)


if __name__ == "__main__":
    main()
