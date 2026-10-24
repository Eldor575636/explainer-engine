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
import build, motion, fx

W, H, FPS, SR = 1920, 1080, 25, 48000
motion.W, motion.H = W, H                       # Sprite.draw / captions read these
NAVY, MUSTARD, RED, CREAM = motion.NAVY, motion.MUSTARD, motion.RED, motion.CREAM
INK = (14, 22, 38)
DISSOLVE = 0.25
VW, VH = 1080, 1920                              # Shorts / Reels canvas
FONTS = None
back_out, ease_out = motion.back_out, motion.ease_out
# pause targets (seconds of silence kept), chosen per gap by what the gap sits between
PAUSE_WORD, PAUSE_COMMA, PAUSE_SENT, PAUSE_BEAT = 0.20, 0.28, 0.38, 0.55


def smart_pieces(wav, total, words, beat_starts):
    """Cut every silence down to a target that depends on its position:
    inside a sentence (hesitations while reading) -> short, after a comma -> a bit more,
    between sentences -> a breath, at a new picture (beat) -> a slightly longer breath.
    words: [(word, sentence_idx, start, end)] on the raw timeline. Returns (pieces, total_new, tmap)."""
    log = subprocess.run(["ffmpeg", "-i", str(wav), "-af", "silencedetect=noise=-38dB:d=0.18", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    import re
    st = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", log)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    sil = [(max(0.0, a), b) for a, b in zip(st, en + [total] * (len(st) - len(en)))]
    bounds = []                                    # (time, target) at each word boundary
    for i in range(len(words) - 1):
        w, si, s, e = words[i]; nxt = words[i + 1]
        t = (e + nxt[2]) / 2
        if nxt[1] != si:
            target = PAUSE_BEAT if nxt[1] in beat_starts else PAUSE_SENT
        elif w.endswith((",", ":", ";")):
            target = PAUSE_COMMA
        else:
            target = PAUSE_WORD
        bounds.append((t, target))
    pieces, cur, newt = [], 0.0, 0.0
    for a, b in sil:
        if a <= 0.01:                              # leading silence: keep 0.15 s
            cur = max(0.0, b - 0.15); continue
        mid = (a + b) / 2
        near = [x for x in bounds if a - 0.35 <= x[0] <= b + 0.35]
        target = max((x[1] for x in near), default=PAUSE_WORD)
        keep = min(b - a, target)
        cut_s, cut_e = a + keep / 2, b - keep / 2
        if cut_e - cut_s < 0.02 or cut_s <= cur:
            continue
        pieces.append((cur, cut_s, newt)); newt += cut_s - cur; cur = cut_e
    end = total
    if end > cur:
        pieces.append((cur, end, newt)); newt += end - cur

    def tmap(x):
        for s, e, ns in pieces:
            if x < s:
                return ns
            if x <= e:
                return ns + (x - s)
        return newt
    return pieces, newt, tmap


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


_STK = {}
def sticker(path, cache, height_px, part=None, nparts=3, outline=14):
    key = (str(path), int(height_px), part, nparts)
    if key not in _STK:
        _STK[key] = _sticker(path, cache, height_px, part, nparts, outline)
    return _STK[key]


def _sticker(path, cache, height_px, part=None, nparts=3, outline=14):
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


SHOT = 4.5          # long beats are split into "shots" of about this length


def smooth(x):
    x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)


def camera(c, t, dur, idx, kind, shots=None):
    """Virtual camera over the composed world layer. Short beats get a slow push;
    long beats get a new framing (zoom + focus point) every ~SHOT seconds with a quick eased move."""
    maxz = 1.20 if kind in ("scene", "map", "portrait") else 1.07
    if shots:
        bounds = sorted(set([0.0] + [x for x in shots if 0.5 < x < dur - 0.5]))
    else:
        n0 = max(1, int(dur // SHOT)); bounds = [j * dur / n0 for j in range(n0)]
    n = len(bounds)
    rng = random.Random(idx * 7919 + 17)
    keys = []
    for j in range(n):
        if j == 0:
            z = 1.0 + (0.03 if idx % 2 else 0.0); fx, fy = 0.5, 0.5
        else:
            z = rng.uniform(1.10, maxz) if j % 2 else rng.uniform(1.0, 1.05)
            fx, fy = rng.uniform(0.3, 0.7), rng.uniform(0.35, 0.6)
        keys.append((z, fx, fy))
    j = max(i for i, x in enumerate(bounds) if x <= t + 1e-9); L = (bounds[j + 1] if j + 1 < n else dur) - bounds[j]; u = t - bounds[j]
    z, fx, fy = keys[j]
    if j > 0 and u < 0.8:
        w = smooth(u / 0.8); z0, fx0, fy0 = keys[j - 1]
        z0 *= 1 + (0.035 if kind in ("scene", "map") else 0.015)   # where the previous shot's drift ended
        z, fx, fy = z0 + (z - z0) * w, fx0 + (fx - fx0) * w, fy0 + (fy - fy0) * w
    z *= 1 + (0.035 if kind in ("scene", "map") else 0.015) * (u / L)
    dx = (12 if idx % 3 else -12) * (u / L)
    tx = min(0.0, max(W - z * W, W / 2 - z * fx * W + dx))
    ty = min(0.0, max(H - z * H, H / 2 - z * fy * H))
    if abs(z - 1) < 1e-4 and abs(tx) < 0.5 and abs(ty) < 0.5:
        return c
    M = np.float32([[z, 0, tx], [0, z, ty]])
    return cv2.warpAffine(c, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


# ---------------- new Uzbek alphabet (law signed 21 Oct 2026) ----------------
# On-screen text uses the new letters: oʻ→ö, gʻ→ğ, sh→ş, ch→ç; the remaining apostrophe is the
# tutuq belgisi ʼ. The script and the alignment keep the current spelling; only what is drawn changes.
import re as _re
_APOS = "'ʻʼ‘’`"
def new_alphabet(text):
    if not text:
        return text
    t = _re.sub(f"([oO])[{_APOS}]", lambda m: "ö" if m.group(1) == "o" else "Ö", text)
    t = _re.sub(f"([gG])[{_APOS}]", lambda m: "ğ" if m.group(1) == "g" else "Ğ", t)
    for a, b in (("SH", "Ş"), ("Sh", "Ş"), ("sh", "ş"), ("CH", "Ç"), ("Ch", "Ç"), ("ch", "ç")):
        t = t.replace(a, b)
    return _re.sub(f"[{_APOS}]", "ʼ", t)


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
    beat_starts = {b["at"][0] for b in beats[1:]}
    pieces, T, tmap = smart_pieces(work / "raw.wav", total,
                                   [(w, si, s, e) for (w, si), (s, e) in zip(sw, times)], beat_starts)
    nt = [(tmap(s), tmap(e)) for s, e in times]
    print(f"Voice {total:.1f}s -> {T:.1f}s ({len(pieces)} pieces)")

    import difflib
    def wt(at):
        si, pre = at
        cands = [((w, s_i), (s, e)) for (w, s_i), (s, e) in zip(sw, nt) if s_i == si]
        for (w, _), (s, e) in cands:
            if build.norm(w).startswith(build.norm(pre)):
                return s
        # fuzzy fallback: the script line was reworded after the beat sheet was written
        best = max(cands, key=lambda c: difflib.SequenceMatcher(None, build.norm(c[0][0]), build.norm(pre)).ratio())
        print(f"  ~ '{pre}' not exact in sentence {si}, using closest word '{best[0][0]}'")
        return best[1][0]

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
    sfx, xsfx, shakes, music_segs, mood = [], [], [], [], "curious"
    F = {"anton": motion.ANTON, "mont": motion.MONT}
    LBL = {k: new_alphabet(v) for k, v in cfg.get("ui", {}).items()}
    cream = cream_bg()
    pose_sprites = {}
    def pose(i, side):
        key = (i, side)
        if key not in pose_sprites:
            m = cfg.get("mascot", {"img": "mascot_sheet", "parts": 3, "full_body": False})
            h = (1.32 if side == "center" else 1.15) if m.get("full_body") else (0.78 if side == "center" else 0.68)
            pose_sprites[key] = sticker(layers / f"{m['img']}.jpg", cache, H * h, part=i, nparts=m["parts"])
            pose_sprites[key].full = m.get("full_body", False)
        return pose_sprites[key]

    print("Preparing beats...")
    for bi, b in enumerate(beats):
        b["t0"], b["t1"] = starts[bi], ends[bi]
        if b.get("mood", mood) != mood or bi == 0:
            mood = b.get("mood", mood); music_segs.append((starts[bi], mood))
        typ = b["type"]
        if typ in ("scene", "map"):
            b["_bgkey"] = ("cover", b["bg"], b.get("crop"), b.get("tint", 0))
        elif typ in ("object", "number"):
            b["_bg"] = cream
        elif typ in ("title", "chapter", "intro"):
            b["_bg"] = solid(NAVY)
        elif typ == "end":
            b["_bg"] = cream
        elif typ == "split":
            b["_bgkey"] = ("split", b["left"], b["right"], b.get("tint", 0))
        elif typ == "portrait":
            bg = cream.copy(); bg[:, : int(W * 0.46)] = np.array(MUSTARD, np.float32) / 255
            b["_bg"] = bg
            b["_fig"] = sticker(layers / f"{b['fig']}.jpg", cache, H * 0.86)
        if "fig" in b and isinstance(b["fig"], dict):
            b["_fig"] = sticker(layers / f"{b['fig']['img']}.jpg", cache, H * b["fig"]["h"])
        b["_props"] = []
        for p in b.get("props", []):
            sp = sticker(layers / f"{p['img']}.jpg", cache, H * p["h"], part=p.get("part"), nparts=p.get("nparts", 3))
            at = wt(p["at"]) - b["t0"]
            b["_props"].append((sp, p, at))
            sfx.append((b["t0"] + at, "thud" if p.get("slam") else "pop"))
            if p.get("slam"):
                shakes.append(b["t0"] + at + 0.14)
        if typ == "number":
            b["_prop"] = sticker(layers / f"{b['prop']}.jpg", cache, H * 0.55)
            b["_val"] = text_sprite(b["value"], motion.ANTON, 300, MUSTARD, 12)
            b["_sub"] = seeded(motion.tag_sprite, new_alphabet(b["sub"]), 50)
            b["_show"] = wt(b["show"]) - b["t0"]
            sfx.append((b["t0"] + b["_show"], "thud"))
        if typ == "title":
            b["_t1"] = text_sprite(new_alphabet(b["title"]), motion.ANTON, 120, CREAM)
            b["_t2"] = text_sprite(new_alphabet(b["title2"]), motion.ANTON, 150, MUSTARD)
            sfx += [(b["t0"] + 0.05, "riser"), (b["t0"] + 0.15, "thud")]
        if typ == "chapter":
            b["_n"] = text_sprite(new_alphabet(b["num"]), motion.ANTON, 80, MUSTARD)
            b["_t"] = text_sprite(new_alphabet(b["title"]), motion.ANTON, 220, CREAM)
            sfx += [(b["t0"] + 0.05, "riser"), (b["t0"] + 0.2, "thud")]
        if typ == "intro":
            b["_wm"] = fx.wordmark(F, 190)
            b["_pose"] = pose(b.get("pose", 3), "center")
            xsfx += [(b["t0"] + 0.1, "swoosh", None), (b["t0"] + 0.55, "hit", None), (b["t0"] + 0.9, "ding", None)]
        if typ == "end":
            b["_pose"] = pose(b.get("pose", 1), "center")
            xsfx += [(b["t0"] + 0.15 * k, "pop", None) for k in range(4)]
        if typ == "chapter":
            xsfx.append((b["t0"] + 0.2, "hit", None))
        if bi:
            prev = beats[bi - 1]
            tr = prev.get("trans") or ("zoom" if typ in ("chapter", "title", "intro") else
                                       "whip" if typ == prev["type"] and typ in ("scene", "map") and bi % 2 else "dissolve")
            prev["_trans"] = tr
            if tr == "dissolve":
                sfx.append((b["t0"], "whoosh"))
            else:
                xsfx.append((b["t0"], "swoosh", None))
        if typ in ("scene", "map", "portrait", "split"):     # soft swoosh on every camera reframe
            nshot = max(1, int((b["t1"] - b["t0"]) // SHOT))
            xsfx += [(b["t0"] + j * (b["t1"] - b["t0"]) / nshot + 0.2, "paper" if j % 2 else "swoosh", None) for j in range(1, nshot)]
        tag_slot = 0
        evs = []
        for e in b.get("ev", []):
            e = dict(e); e["t"] = wt(e["at"]) - b["t0"]; k = e["k"]
            if k == "label":
                e["_s"] = seeded(motion.label_sprite, new_alphabet(e["text"]), 84); e["x"], e["y"] = W / 2, 105
                e["rot"] = random.choice([-1.5, 1.5]); sfx.append((b["t0"] + e["t"], "pop"))
            elif k == "tag":
                fg = RED if e.get("fg") == "red" else NAVY
                e["_s"] = seeded(motion.tag_sprite, new_alphabet(e["text"]), 50, fg)
                if "x" in e:
                    e["x"], e["y"] = e["x"] * W, e["y"] * H
                else:
                    e["x"], e["y"] = W * 0.74, 230 + 92 * tag_slot; tag_slot += 1
                e["rot"] = random.uniform(-2, 2); sfx.append((b["t0"] + e["t"], "pop"))
            elif k == "stamp":
                e["_s"] = seeded(motion.stamp_sprite, new_alphabet(e["text"]), 130); e["x"], e["y"] = W * 0.5, H * 0.46
                sfx.append((b["t0"] + e["t"] + 0.14, "thud")); shakes.append(b["t0"] + e["t"] + 0.14)
            elif k == "circle":
                e["_pts"] = ellipse_pts(e["x"] * W, e["y"] * H, e["rx"] * W, e["ry"] * H); sfx.append((b["t0"] + e["t"], "draw"))
            elif k == "arrow":
                e["_pts"] = curve((e["from"][0] * W, e["from"][1] * H), (e["to"][0] * W, e["to"][1] * H), e.get("straight", False))
                sfx.append((b["t0"] + e["t"], "draw"))
            elif k == "mascot":
                e["_s"] = pose(e["pose"], e["side"]); sfx.append((b["t0"] + e["t"], "whoosh"))
            elif k == "prop":
                e["_s"] = sticker(layers / f"{e['img']}.jpg", cache, H * e["h"], part=e.get("part"), nparts=e.get("nparts", 3)); sfx.append((b["t0"] + e["t"], "pop"))
            elif k == "counter":
                lo = e.get("from", 0); stp = max(1, (e["to"] - lo) // 60)
                vals = list(range(lo, e["to"] + 1, stp)) + ([e["to"]] if (e["to"] - lo) % stp else [])
                e["_frames"] = [seeded(motion.label_sprite, new_alphabet(f"{e.get('prefix', '')}{v}{e.get('suffix', '')}"), 150) for v in vals]
                sfx += [(b["t0"] + e["t"] + 0.9 * i / 12, "tick") for i in range(12)]
                xsfx.append((b["t0"] + e["t"] + 0.95, "ding", None))
            elif k in ("bars", "pie", "subscribe", "like", "news"):
                def mk(ee, Wd, Hd):
                    if k == "bars":
                        return fx.Bars(dict(ee, suffix=new_alphabet(ee.get("suffix", "")), items=[dict(i, label=new_alphabet(i["label"])) for i in ee["items"]]), F, Wd, Hd)
                    if k == "pie":
                        return fx.Pie(dict(ee, slices=[dict(i, label=new_alphabet(i["label"])) for i in ee["slices"]]), F, Wd, Hd)
                    if k == "subscribe":
                        return fx.Subscribe(ee, F, Wd, Hd, LBL.get("subscribe", "OBUNA"), LBL.get("subscribed", "OBUNA"))
                    if k == "like":
                        return fx.Like(ee, F, Wd, Hd, LBL.get("like", "LAYK"))
                    return fx.News(ee, F, Wd, Hd, new_alphabet(ee["text"]))
                e["_o"] = mk(e, W, H)
                vert = {"bars": dict(x=0.5, y=0.42, w=0.9, h=0.32), "pie": dict(x=0.32, y=0.4, r=0.13),
                        "subscribe": dict(x=0.42, y=0.84), "like": dict(x=0.5, y=0.9), "news": {}}[k]
                e["_ov"] = mk(dict(e, **vert), VW, VH)
                xsfx += e["_o"].sounds(b["t0"] + e["t"])
            elif k == "bigtext":
                e["_s"] = text_sprite(new_alphabet(e["text"]), motion.ANTON, 300, RED, 0); sfx.append((b["t0"] + e["t"], "pop"))
            if k in ("label", "tag", "stamp"):
                e["vx"], e["vy"] = VW / 2, {"label": 260, "stamp": VH * 0.45}.get(k, 470 + 110 * sum(1 for x in evs if x["k"] == "tag"))
            evs.append(e)
        b["_ev"] = evs

    # --- captions: up to 5 words, never across sentences ---
    chunks, cur = [], []
    for k, ((w, si), (s, e)) in enumerate(zip(sw, nt)):
        cur.append((new_alphabet(w).upper(), s, e))
        last = k == len(sw) - 1 or sw[k + 1][1] != si
        if len(cur) == 5 or last or w.endswith((",", ":")):
            chunks.append(cur); cur = []
    caps = []
    for ci, ch in enumerate(chunks):
        st = ch[0][1]; en = chunks[ci + 1][0][1] if ci + 1 < len(chunks) else T
        en = min(en, max(ch[-1][2] + 0.5, st + 0.5))
        caps.append((st, en, [x[1] for x in ch], tuple(x[0] for x in ch)))
    from functools import lru_cache as _lru
    @_lru(maxsize=6)
    def cap_sprites(words):
        return motion.caption_sprites(list(words), 50)

    # --- auto-director: fill dead stretches (>4 s with no new visual) with keyword tags ---
    def vis_times():
        return sorted([b["t0"] for b in beats] + [b["t0"] + e["t"] for b in beats for e in b["_ev"]] +
                      [b["t0"] + at for b in beats for _, _, at in b["_props"]] + [T])
    shown = {new_alphabet(e.get("text", "")).upper() for b in beats for e in b["_ev"]}
    added = 0
    for _ in range(3):
        v = vis_times()
        for a_, b_ in zip(v, v[1:]):
            if b_ - a_ <= 4.0:
                continue
            bi_ = max(i for i, bb in enumerate(beats) if bb["t0"] <= a_ + 1e-6)
            bb = beats[bi_]
            if bb["type"] in ("title", "chapter", "intro", "end"):
                continue
            cands = []
            for k, ((w, si), (s0, e0)) in enumerate(zip(sw, nt)):
                if a_ + 1.2 < s0 < b_ - 1.0:
                    clean = w.strip(".,:;?!\"—()")
                    first = k == 0 or sw[k - 1][1] != si
                    if any(ch.isdigit() for ch in clean) or (clean[:1].isupper() and not first and len(clean) > 3):
                        cands.append((s0, clean))
            cands = [c_ for c_ in cands if new_alphabet(c_[1]).upper() not in shown]
            if not cands:
                continue
            s0, word = cands[len(cands) // 2]
            slot = sum(1 for e in bb["_ev"] if e["k"] == "tag")
            e = {"k": "tag", "text": word.upper(), "t": s0 - bb["t0"], "auto": True,
                 "_s": seeded(motion.tag_sprite, new_alphabet(word.upper()), 50, NAVY), "rot": random.uniform(-2, 2),
                 "x": W * 0.74 if bb["type"] != "portrait" else W * 0.74, "y": 230 + 92 * slot, "vx": VW / 2, "vy": 470 + 110 * slot}
            bb["_ev"].append(e); shown.add(new_alphabet(word).upper()); sfx.append((bb["t0"] + e["t"], "pop")); added += 1
    print(f"Auto-director: added {added} keyword tags")

    # --- camera shots: uniform every SHOT s, plus an extra reframe in the middle of any gap > 3.5 s ---
    for bb in beats:
        if bb["type"] in ("title", "chapter", "intro", "end"):
            continue
        d = bb["t1"] - bb["t0"]; n0 = max(1, int(d // SHOT))
        sh = [j * d / n0 for j in range(n0)]
        evt = sorted([0.0] + [e["t"] for e in bb["_ev"]] + [at for _, _, at in bb["_props"]] + sh + [d])
        for a_, b_ in zip(evt, evt[1:]):
            if b_ - a_ > 3.5:
                sh.append((a_ + b_) / 2); xsfx.append((bb["t0"] + (a_ + b_) / 2 + 0.2, "swoosh", None))
        bb["_shots"] = sorted(sh)

    # --- automatic edit check: no dead stretches, sound under motion ---
    vis = sorted([b["t0"] for b in beats] + [b["t0"] + e["t"] for b in beats for e in b["_ev"]] +
                 [b["t0"] + at for b in beats for _, _, at in b["_props"]] +
                 [b["t0"] + x for b in beats for x in b.get("_shots", [])] + [T])
    def beat_at(x):
        i = max(i for i, bb in enumerate(beats) if bb["t0"] <= x + 1e-6); return f"{i}:{beats[i]['type']}"
    dead = [(round(a, 1), round(b_ - a, 1), beat_at(a)) for a, b_ in zip(vis, vis[1:]) if b_ - a > 4.0 and "end" not in beat_at(a)]
    snd = sorted([t for t, _ in sfx] + [t for t, _, _ in xsfx] + [0, T])
    quiet = [(round(a, 1), round(b_ - a, 1)) for a, b_ in zip(snd, snd[1:]) if b_ - a > 7.0]
    report = {"visual_events": len(vis), "avg_gap_s": round(T / max(1, len(vis)), 2), "dead_stretches_over_4s": dead,
              "no_sfx_over_7s": quiet}
    (work / "edit_report.json").write_text(json.dumps(report, indent=1))
    print(f"Edit check: {len(vis)} visual events, avg every {report['avg_gap_s']}s, "
          f"{len(dead)} stretches >4s without a change, {len(quiet)} stretches >7s without SFX")

    from functools import lru_cache
    @lru_cache(maxsize=4)
    def bg_for(key):
        if key[0] == "cover":
            return cover(Image.open(layers / f"{key[1]}.jpg"), key[2], key[3])
        l = cover(Image.open(layers / f"{key[1]}.jpg"), None, key[3]); r = cover(Image.open(layers / f"{key[2]}.jpg"), None, key[3])
        bg = l.copy(); bg[:, : W // 2] = l[:, W // 4: W // 4 + W // 2]; bg[:, W // 2:] = r[:, W // 4: W // 4 + W - W // 2]
        return bg

    def render_world(bi, t):
        b = beats[bi]; dur = b["t1"] - b["t0"]; typ = b["type"]
        c = (bg_for(b["_bgkey"]) if "_bgkey" in b else b["_bg"]).copy()
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
                b["_val"].draw(c, W * 0.66, H * 0.43, (1.8 - 0.8 * ease_out(lt / 0.2)) * min(1, W * 0.6 / b["_val"].w), 0, min(1, lt / 0.08))
                b["_sub"].draw(c, W * 0.66, H * 0.68, back_out((lt - 0.3) / 0.4), -1.5, min(1, max(0, lt - 0.3) / 0.1))
        if typ == "title":
            b["_t1"].draw(c, W / 2, H * 0.40, (1.5 - 0.5 * ease_out(t / 0.25)) * min(1, W * 0.9 / b["_t1"].w), 0, min(1, t / 0.1))
            lt = t - 0.35
            if lt > 0:
                b["_t2"].draw(c, W / 2, H * 0.58, (1.5 - 0.5 * ease_out(lt / 0.25)) * min(1, W * 0.9 / b["_t2"].w), 0, min(1, lt / 0.1))
                cv2.line(c, (int(W * 0.25), int(H * 0.72)), (int(W * 0.25 + W * 0.5 * ease_out(lt / 0.6)), int(H * 0.72)),
                         tuple(v / 255 for v in RED), 8, cv2.LINE_AA)
        if typ == "chapter":
            b["_n"].draw(c, W / 2, H * 0.36, back_out(t / 0.35), 0, min(1, t / 0.1))
            lt = t - 0.2
            if lt > 0:
                b["_t"].draw(c, W / 2, H * 0.56, (1.6 - 0.6 * ease_out(lt / 0.2)) * min(1, W * 0.9 / b["_t"].w), 0, min(1, lt / 0.08))
                cv2.line(c, (int(W * 0.3), int(H * 0.73)), (int(W * 0.3 + W * 0.4 * ease_out(lt / 0.5)), int(H * 0.73)),
                         tuple(v / 255 for v in RED), 10, cv2.LINE_AA)
        if typ == "split":
            p = ease_out(t / 0.5)
            cv2.line(c, (W // 2, int(H * (1 - p))), (W // 2, H), (1, 1, 1), 14)
            cv2.line(c, (W // 2, int(H * (1 - p))), (W // 2, H), fx.c01(RED), 6)
        c = draw_events(c, b, t, dur, WORLD)
        if typ not in ("title", "chapter", "intro", "end"):
            c = camera(c, t, dur, bi, typ, b.get("_shots"))
        return c

    def render(bi, t, V=False):
        b = beats[bi]; dur = b["t1"] - b["t0"]
        c = render_world(bi, t)
        if V:
            c = vcrop(c, b, t)
        Wd, Hd = (VW, VH) if V else (W, H)
        if b["type"] == "intro":
            sp = b["_pose"]
            sp.draw(c, Wd * (0.5 if V else 0.74), Hd * (0.62 if V else 0.16) + sp.h / 2 * (0.8 if V else 1) + (1 - ease_out(t / 0.6)) * Hd * 0.7, 0.8 if V else 1.0)
            wm = b["_wm"]; sc = (0.55 if V else 1.0) * (1.6 - 0.6 * ease_out((t - 0.45) / 0.25))
            if t > 0.45:
                fx.paste(c, wm, Wd * (0.5 if V else 0.34), Hd * (0.3 if V else 0.45), sc, min(1, (t - 0.45) / 0.1))
                q = ease_out((t - 0.7) / 0.5); y = int(Hd * (0.3 if V else 0.45) + wm.height * sc / 2 + 10)
                x0 = int(Wd * (0.5 if V else 0.34) - wm.width * sc / 2)
                cv2.line(c, (x0, y), (int(x0 + wm.width * sc * q), y), fx.c01(RED), 10, cv2.LINE_AA)
        if b["type"] == "end":
            if not V:
                fx.end_frames(c, t, W, H, F, LBL.get("next", "KEYINGI VIDEO"))
            sp = b["_pose"]
            sp.draw(c, Wd * 0.5, Hd * (0.55 if V else 0.2) + sp.h / 2 + (1 - ease_out(t / 0.6)) * Hd * 0.7, 0.85 if V else 0.9)
        return draw_events(c, b, t, dur, SCREEN, V)

    def vcrop(c, b, t):
        """9:16 window out of the 16:9 world frame, centred on the beat's focus, scaled to 1080x1920."""
        fxp = b.get("vfocus", 0.5)
        cw = int(H * VW / VH)
        x0 = int(min(W - cw, max(0, fxp * W - cw / 2)))
        return cv2.resize(c[:, x0:x0 + cw], (VW, VH), interpolation=cv2.INTER_LINEAR)

    WORLD = {"circle", "arrow", "pin", "rings", "prop"}
    SCREEN = {"label", "tag", "stamp", "mascot", "counter", "bigtext", "bars", "pie", "subscribe", "like", "news"}

    def draw_events(c, b, t, dur, kinds, V=False):
        Wd, Hd = (VW, VH) if V else (W, H)
        for e in b["_ev"]:
            lt = t - e["t"]
            k = e["k"]
            if lt < 0 or k not in kinds:
                continue
            ex, ey = (e.get("vx"), e.get("vy")) if V else (e.get("x"), e.get("y"))
            if k in ("label", "tag"):
                sc = back_out(lt / 0.38) * (1.15 if V else 1)
                e["_s"].draw(c, ex, ey, sc, e["rot"] * sc, min(1, lt / 0.08))
            elif k == "stamp":
                e["_s"].draw(c, ex, ey, 2.3 - 1.3 * ease_out(lt / 0.16), -7, min(1, lt / 0.06))
            elif k in ("bars", "pie", "subscribe", "like", "news"):
                (e["_ov"] if V else e["_o"]).draw(c, lt)
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
                sp = e["_s"]
                if V:
                    vs = 0.8
                    sp.draw(c, VW * 0.72, VH * 0.6 + sp.h * vs / 2 + (1 - ease_out(lt / 0.6)) * VH * 0.5 + 4 * math.sin(lt * 2), vs)
                    continue
                x = W * (0.81 if e["side"] == "right" else 0.5)
                if getattr(sp, "full", False):      # full-body sheet: frame him waist-up, legs below the edge
                    top = H * (0.16 if e["side"] == "center" else 0.30)
                    y = top + sp.h / 2 + (1 - ease_out(lt / 0.6)) * H * 0.8
                else:
                    y = H - sp.h / 2 + 25 + (1 - ease_out(lt / 0.6)) * sp.h * 0.9
                sp.draw(c, x, y + 4 * math.sin(lt * 2), 1.0)
            elif k == "prop":
                sc = back_out(lt / 0.4) * ((0.8 + 0.5 * ease_out(lt / max(dur - e["t"], 1))) if e.get("grow") else 1)
                e["_s"].draw(c, e["x"] * W, e["y"] * H + 6 * math.sin(lt * 2), sc, 0, min(1, lt / 0.1))
            elif k == "counter":
                fr = e["_frames"]; v = int(round((len(fr) - 1) * ease_out(lt / 0.9)))
                fr[v].draw(c, (0.5 if V else e["x"]) * Wd, (0.38 if V else e["y"]) * Hd, back_out(lt / 0.3), 0, min(1, lt / 0.08))
            elif k == "bigtext":
                e["_s"].draw(c, (0.5 if V else e["x"]) * Wd, (0.42 if V else e["y"]) * Hd, back_out(lt / 0.35) * (0.8 if V else 1), 0, min(1, lt / 0.08))
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

    # --- preview mode: PREVIEW="12.5,40,..." saves stills (16:9 and 9:16) and exits ---
    import os
    if os.environ.get("PREVIEW"):
        def ptime(x):
            if x.startswith("@"):                     # @sentence:word[+offset]
                sw_, off = (x[1:].split("+") + ["1.5"])[:2]; si_, w_ = sw_.split(":")
                return wt([int(si_), w_]) + float(off)
            return float(x)
        for tt in [ptime(x) for x in os.environ["PREVIEW"].split(",")]:
            bi_ = max(i for i, b in enumerate(beats) if b["t0"] <= tt)
            for V in (False, True):
                fr = render(bi_, tt - beats[bi_]["t0"], V)
                if not V:
                    ci_ = max([i for i, cp in enumerate(caps) if cp[0] <= tt] or [0]); st, en, wst, sprs = caps[ci_]
                    if st <= tt < en:
                        cap_sprites(sprs)[max(j for j in range(len(wst)) if wst[j] <= tt or j == 0)].draw(fr, W / 2, H - 78)
                Image.fromarray((np.clip(fr, 0, 1) * 255).astype(np.uint8)).save(work / f"prev_{'v' if V else 'h'}_{tt:06.1f}.jpg", quality=85)
        print("preview saved"); return

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
        if bi + 1 < len(beats):
            tr = beats[bi].get("_trans", "dissolve"); left = beats[bi]["t1"] - t
            if tr == "zoom" and left < 0.45:
                p = 1 - left / 0.45; zf = beats[bi].get("zf", [0.5, 0.45])
                frame = fx.zoom_into(frame, zf[0], zf[1], p, W, H)
                if p > 0.55:
                    w = (p - 0.55) / 0.45; frame = frame * (1 - w) + render(bi + 1, 0.0) * w
            elif tr == "whip" and left < 0.3:
                frame = fx.whip(frame, render(bi + 1, 0.0), 1 - left / 0.3, W)
            elif tr == "dissolve" and left < DISSOLVE:
                w = 1 - left / DISSOLVE
                frame = frame * (1 - w) + render(bi + 1, 0.0) * w
        while ci + 1 < len(caps) and caps[ci + 1][0] <= t:
            ci += 1
        st, en, wst, sprs = caps[ci]
        if st <= t < en:
            k = max(j for j in range(len(wst)) if wst[j] <= t or j == 0)
            cap_sprites(sprs)[k].draw(frame, W / 2, H - 78, 0.94 + 0.06 * back_out((t - st) / 0.18))
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
    motion.write_wav(work / "sfx.wav", 0.85 * fx.extra_sfx(synth_sfx(n, sfx), xsfx))
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

    # --- Shorts / Reels: 9:16 clips cut from the long episode ---
    for sh in cfg.get("shorts", []):
        ta = max(0.0, wt(sh["from"]) - 0.15)
        si_end = sh["to"][0]
        tb = max(e for (w, s_i), (s, e) in zip(sw, nt) if s_i == si_end) + 0.45
        name = out_path.parent / f"{out_path.stem}_short_{sh['name']}.mp4"
        print(f"Short {sh['name']}: {ta:.1f}-{tb:.1f}s -> {name.name}")
        motion.W, motion.H = VW, VH
        vchunks, cur = [], []
        for k, ((w, si), (s0, e0)) in enumerate(zip(sw, nt)):
            if s0 < ta - 0.01 or s0 > tb:
                continue
            cur.append((new_alphabet(w).upper(), s0, e0))
            last = k == len(sw) - 1 or sw[k + 1][1] != si
            if len(cur) == 3 or last or w.endswith((",", ":")):
                vchunks.append(cur); cur = []
        if cur:
            vchunks.append(cur)
        vcaps = []
        for ci_, ch in enumerate(vchunks):
            st = ch[0][1]; en = vchunks[ci_ + 1][0][1] if ci_ + 1 < len(vchunks) else tb
            vcaps.append((st, min(en, max(ch[-1][2] + 0.5, st + 0.5)), [x[1] for x in ch], motion.caption_sprites([x[0] for x in ch], 76)))
        hook = seeded(motion.label_sprite, new_alphabet(sh.get("hook", "")), 70) if sh.get("hook") else None
        motion.W, motion.H = W, H
        tmpv = work / f"short_{sh['name']}_v.mp4"
        ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{VW}x{VH}",
                               "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                               "-pix_fmt", "yuv420p", str(tmpv)], stdin=subprocess.PIPE)
        bi = 0; cj = 0
        for fi in range(int((tb - ta) * FPS)):
            t = ta + fi / FPS
            while bi + 1 < len(beats) and beats[bi + 1]["t0"] <= t:
                bi += 1
            frame = render(bi, t - beats[bi]["t0"], True)
            if bi + 1 < len(beats) and beats[bi]["t1"] - t < DISSOLVE:
                w = 1 - (beats[bi]["t1"] - t) / DISSOLVE
                frame = frame * (1 - w) + render(bi + 1, 0.0, True) * w
            if hook is not None and t - ta < 3.0:
                hook.draw(frame, VW / 2, 150, back_out((t - ta) / 0.35) * (1 - ease_out((t - ta - 2.7) / 0.3)), -1.5)
            while cj + 1 < len(vcaps) and vcaps[cj + 1][0] <= t:
                cj += 1
            if vcaps:
                st, en, wst, sprs = vcaps[cj]
                if st <= t < en:
                    k = max(j for j in range(len(wst)) if wst[j] <= t or j == 0)
                    sprs[k].draw(frame, VW / 2, VH * 0.76, 0.94 + 0.06 * back_out((t - st) / 0.18))
            ff.stdin.write((np.clip(frame, 0, 1) * 255).astype(np.uint8).tobytes())
        ff.stdin.close(); ff.wait()
        d = tb - ta
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(tmpv), "-ss", f"{ta:.2f}", "-t", f"{d:.2f}", "-i", str(out_path),
                        "-map", "0:v", "-map", "1:a", "-af", f"afade=t=in:d=0.25,afade=t=out:st={max(0, d - 0.4):.2f}:d=0.4",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", str(name)], check=True)


if __name__ == "__main__":
    main()
