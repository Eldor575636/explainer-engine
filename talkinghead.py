#!/usr/bin/env python3
"""Talking-head reel editor (California Uzbek style): your filmed 9:16 clip as the base layer, with
punch-in zooms that change on every sentence, word-by-word captions with the active word in red,
keyword cards, stat counters, a checklist, a 'link in comments' pointer, a retention progress bar,
sound effects and a ducked music bed. Same alignment as the explainer engine (exact script → words).

Usage: python3 talkinghead.py <config.json> <video> <words.json> <out.mp4>
"""
import json, math, random, subprocess, sys
from pathlib import Path
import numpy as np, cv2
from PIL import Image

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import build, motion, fx
from v3 import new_alphabet

W, H, FPS, SR = 1080, 1920, 30, 48000
motion.W, motion.H = W, H
RED, WHITE, BLACK, YELLOW = (226, 35, 26), (255, 255, 255), (12, 12, 12), (255, 210, 0)
ease, back = fx.ease_out, fx.back_out
F = {"anton": motion.ANTON, "mont": motion.MONT}


def caption_imgs(words, size=82):
    """One image per active word: white words, black outline, active word red on a white pill."""
    from PIL import ImageDraw, ImageFont
    f = ImageFont.truetype(motion.MONT, size)
    gap = f.getlength(" ")
    ws = [f.getlength(w) for w in words]
    tw = int(sum(ws) + gap * (len(words) - 1)) + 60
    if tw > W - 80:
        return caption_imgs(words, int(size * (W - 80) / tw))
    b = f.getbbox("ÖĞŞÇAgy"); th = b[3] - b[1] + 50
    out = []
    for k in range(len(words)):
        img = Image.new("RGBA", (tw, th), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
        x = 30
        for j, w in enumerate(words):
            if j == k:
                d.rounded_rectangle((x - 12, 10, x + ws[j] + 12, th - 8), 16, fill=RED + (255,))
                d.text((x, 25 - b[1]), w, font=f, fill=WHITE + (255,))
            else:
                d.text((x, 25 - b[1]), w, font=f, fill=WHITE + (255,), stroke_width=8, stroke_fill=BLACK + (255,))
            x += ws[j] + gap
        out.append(img)
    return out


def card(text, size=64, fg=WHITE, bg=RED, pad=(34, 18)):
    t = fx.text_rgba(text, F["anton"], size, fg)
    img = Image.new("RGBA", (t.width + 2 * pad[0], t.height + 2 * pad[1]), (0, 0, 0, 0))
    from PIL import ImageDraw
    ImageDraw.Draw(img).rounded_rectangle((0, 0, img.width - 1, img.height - 1), 18, fill=bg + (255,))
    img.alpha_composite(t, (pad[0], pad[1]))
    return img


def main():
    cfg = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    video, wpath, out = sys.argv[2], sys.argv[3], Path(sys.argv[4])
    work = out.parent / (out.stem + "_work"); work.mkdir(exist_ok=True)
    S = cfg["sentences"]
    asr = json.loads(Path(wpath).read_text(encoding="utf-8"))
    sw = [(w, si) for si, s in enumerate(S) for w in s.split()]
    times, m = build.align([w for w, _ in sw], asr)
    print(f"Aligned {m}/{len(sw)}")
    T = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video],
                             capture_output=True, text=True).stdout)

    def wt(at):
        si, pre = at
        for (w, s_i), (s, e) in zip(sw, times):
            if s_i == si and build.norm(w).startswith(build.norm(pre)):
                return s
        return next(s for (w, s_i), (s, e) in zip(sw, times) if s_i == si)

    sent_start = [wt([i, S[i].split()[0]]) for i in range(len(S))]
    # --- zoom plan: a new framing on every sentence, extra punch on 'punch' words ---
    fxp, fyp = cfg.get("face", [0.52, 0.28])
    zooms = []
    seq = [1.0, 1.18, 1.08, 1.28, 1.0, 1.15, 1.22, 1.06]
    for i, t0 in enumerate(sent_start):
        zooms.append((max(0, t0 - 0.05), seq[i % len(seq)]))
    for at in cfg.get("punch", []):
        zooms.append((wt(at), 1.35))
    zooms.sort()

    def zoom_at(t):
        z, prev, tz = 1.0, 1.0, 0.0
        for k, (a, zz) in enumerate(zooms):
            if a <= t:
                prev, z, tz = (zooms[k - 1][1] if k else 1.0), zz, a
        p = ease((t - tz) / 0.18)
        return prev + (z - prev) * p

    # --- events ---
    sfx, xsfx = [], []
    evs = []
    for e in cfg["events"]:
        e = dict(e); e["t"] = wt(e["at"]) + e.get("delay", 0.0); k = e["k"]
        if k == "card":
            e["img"] = card(new_alphabet(e["text"]), e.get("size", 64), bg=tuple(e.get("bg", RED)), fg=tuple(e.get("fg", WHITE)))
            sfx.append((e["t"], "pop"))
        elif k == "stat":
            e["frames"] = [card(new_alphabet(f"{v}{e.get('suffix', '')}"), e.get("size", 96)) for v in range(e.get("from", 0), e["to"] + 1)]
            e["lab"] = card(new_alphabet(e["label"]), e.get("lsize", 44), fg=BLACK, bg=tuple(e.get("lbg", WHITE)))
            sfx += [(e["t"] + 0.6 * i / 10, "tick") for i in range(10)]; xsfx.append((e["t"] + 0.65, "ding", None))
        elif k == "check":
            e["img"] = card(new_alphabet(e["text"]), 52, fg=BLACK, bg=WHITE)
            xsfx.append((e["t"], "ding", None))
        elif k == "link":
            e["img"] = card(new_alphabet(e["text"]), 60)
            xsfx += [(e["t"], "swoosh", None), (e["t"] + 0.5, "click", None)]
        elif k == "title":
            e["img"] = card(new_alphabet(e["text"]), e.get("size", 70), fg=BLACK, bg=YELLOW)
            xsfx += [(e["t"] + 0.05, "hit", None)]
        elif k == "emoji":
            e["img"] = card(e["text"], 70, fg=WHITE, bg=BLACK)
            sfx.append((e["t"], "pop"))
        evs.append(e)
    for t0, _ in zooms[1:]:
        xsfx.append((t0, "swoosh", None))

    # --- layout: face / split (picture top, face bottom) / full (picture or solid screen) ---
    PH = H // 2
    segs = []
    for L in cfg.get("layout", [{"at": [0, S[0].split()[0]], "mode": "face"}]):
        L = dict(L); L["t"] = 0.0 if L["at"] == 0 else wt(L["at"])
        size = (W, PH) if L["mode"] == "split" else (W, H)
        bg = np.zeros((size[1], size[0], 3), np.float32) + np.float32(L.get("bg", (245, 245, 245))) / 255
        if L.get("img"):
            im = Image.open(Path(sys.argv[1]).parent / L["img"]).convert("RGB")
            sc = max(size[0] / im.width, size[1] / im.height)
            im = im.resize((math.ceil(im.width * sc), math.ceil(im.height * sc)), Image.LANCZOS)
            fy = L.get("fy", 0.5); x0 = (im.width - size[0]) // 2; y0 = int((im.height - size[1]) * fy)
            bg = np.asarray(im.crop((x0, y0, x0 + size[0], y0 + size[1])), np.float32) / 255
        L["bgimg"] = bg
        segs.append(L)
    segs.sort(key=lambda L: L["t"])
    for L in segs[1:]:
        xsfx.append((L["t"], "swoosh", None))
    xsfx = [x for x in xsfx if not any(abs(x[0] - L["t"]) < 0.4 and x[0] != L["t"] for L in segs) or x[1] != "swoosh"]

    def seg_at(t):
        k = 0
        for i, L in enumerate(segs):
            if L["t"] <= t:
                k = i
        return k

    def panel(L, t):
        """Picture or solid panel with a slow push-in."""
        img = L["bgimg"]; lt = max(0.0, t - L["t"]); z = 1.0 + 0.012 * lt
        h, w = img.shape[:2]
        if img.std() < 1e-3:
            return img.copy()
        return cv2.warpAffine(img, np.float32([[z, 0, w / 2 * (1 - z)], [0, z, h / 2 * (1 - z)]]), (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

    def compose(L, src, t):
        m = L["mode"]
        if m == "full":
            return panel(L, t)
        if m == "split":
            out = np.empty((H, W, 3), np.float32)
            out[:PH] = panel(L, t)
            z = 1.05 + 0.5 * (zoom_at(t) - 1); cx, cy = fxp * W, fyp * H + 0.09 * H
            cx = min(max(cx, W / (2 * z)), W - W / (2 * z)); cy = min(max(cy, PH / (2 * z)), H - PH / (2 * z))
            out[PH:] = cv2.warpAffine(src, np.float32([[z, 0, W / 2 - z * cx], [0, z, PH / 2 - z * cy]]), (W, PH), flags=cv2.INTER_LINEAR)
            out[PH - 5:PH + 5] = np.float32(RED) / 255
            return out
        z = zoom_at(t); fr = src
        if abs(z - 1) > 1e-3:
            tx = min(0, max(W - z * W, W / 2 - z * fxp * W)); ty = min(0, max(H - z * H, H * 0.36 - z * fyp * H))
            fr = cv2.warpAffine(src, np.float32([[z, 0, tx], [0, z, ty]]), (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        return fr
    for e in evs:                                     # an overlay never outlives its layout
        nxt = [L["t"] for L in segs if L["t"] > e["t"] + 0.01]
        if nxt:
            e["dur"] = min(e.get("dur", 2.6), nxt[0] - e["t"] + 0.1)
    CAPY = {"face": 0.70, "split": 0.50, "full": 0.82}

    # captions (3 words, never across sentences)
    chunks, cur = [], []
    for k, ((w, si), (s, e)) in enumerate(zip(sw, times)):
        cur.append((new_alphabet(w).upper().strip("«»"), s, e))
        last = k == len(sw) - 1 or sw[k + 1][1] != si
        if len(cur) == 3 or last or w.endswith((",", ":")):
            chunks.append(cur); cur = []
    caps = []
    for ci, ch in enumerate(chunks):
        st = ch[0][1]; en = chunks[ci + 1][0][1] if ci + 1 < len(chunks) else T
        caps.append((st, min(en, ch[-1][2] + 0.6), [x[1] for x in ch], caption_imgs([x[0] for x in ch])))

    # --- render ---
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", video, "-vf", f"scale={W}:{H},fps={FPS}", "-f", "rawvideo",
                            "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    tmpv = work / "video.mp4"
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", str(tmpv)],
                           stdin=subprocess.PIPE)
    n = int(T * FPS); ci = 0; rng = random.Random(2)
    for fi in range(n):
        buf = dec.stdout.read(W * H * 3)
        if len(buf) < W * H * 3:
            break
        t = fi / FPS
        src = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(np.float32) / 255
        si_ = seg_at(t); L = segs[si_]; fr = compose(L, src, t)
        lt_ = t - L["t"]
        if si_ > 0 and lt_ < 0.2:                       # quick slide-in of the new layout
            prev = compose(segs[si_ - 1], src, t); p = ease(lt_ / 0.2); off = int((1 - p) * W * 0.25)
            fr = prev * (1 - p) + np.roll(fr, off, axis=1) * p
        # bottom gradient for caption legibility
        for e in evs:
            lt = t - e["t"]; dur = e.get("dur", 2.6)
            if lt < 0 or lt > dur:
                continue
            out_a = 1 - ease((lt - dur + 0.25) / 0.25)
            k = e["k"]; x, y = e.get("x", 0.5) * W, e.get("y", 0.5) * H
            if k in ("card", "check", "link", "emoji", "title"):
                sc = back(lt / 0.35)
                if k == "title":
                    sc = 1.4 - 0.4 * ease(lt / 0.25)
                fx.paste(fr, e["img"], x, y, sc * (1 if out_a > 0.01 else 0), min(1, lt / 0.08) * out_a)
                if k == "check" and lt > 0.15:
                    cx = x - e["img"].width / 2 - 50; p = ease((lt - 0.15) / 0.3)
                    cv2.circle(fr, (int(cx), int(y)), 38, (0.18, 0.7, 0.3), -1, cv2.LINE_AA)
                    pts = np.array([[cx - 18, y], [cx - 4, y + 15], [cx + 20, y - 14]])
                    m_ = int(1 + 2 * p); cv2.polylines(fr, [np.int32(pts[:m_ + 1])], False, (1, 1, 1), 8, cv2.LINE_AA)
                if k == "link" and lt > 0.3:          # bouncing arrow towards the comment button (bottom right)
                    b_ = 12 * math.sin(lt * 9); ax, ay = x + e["img"].width / 2 + 20, y + 30 + b_
                    tip = np.array([W * e.get("tx", 0.9), H * e.get("ty", 0.78)]); base = np.array([ax, ay])
                    cv2.arrowedLine(fr, tuple(int(v) for v in base), tuple(int(v) for v in tip), (1, 1, 1), 16, cv2.LINE_AA, tipLength=0.18)
                    cv2.arrowedLine(fr, tuple(int(v) for v in base), tuple(int(v) for v in tip), tuple(c / 255 for c in RED), 9, cv2.LINE_AA, tipLength=0.18)
            elif k == "stat":
                v = int(round((len(e["frames"]) - 1) * ease(lt / 0.6)))
                fx.paste(fr, e["frames"][v], x, y, back(lt / 0.3) * (1 if out_a > 0.01 else 0), out_a)
                fx.paste(fr, e["lab"], x, y + e["frames"][0].height / 2 + e["lab"].height / 2 + 14, back((lt - 0.2) / 0.3) * (1 if out_a > 0.01 else 0), min(1, max(0, lt - 0.2) / 0.1) * out_a)
        # captions
        while ci + 1 < len(caps) and caps[ci + 1][0] <= t:
            ci += 1
        st, en, wst, imgs = caps[ci]
        if st <= t < en:
            k = max(j for j in range(len(wst)) if wst[j] <= t or j == 0)
            fx.paste(fr, imgs[k], W / 2, H * CAPY[L['mode']], 0.94 + 0.06 * back((t - st) / 0.15))
        # progress bar
        cv2.rectangle(fr, (0, 0), (int(W * t / T), 12), tuple(c / 255 for c in RED), -1)
        enc.stdin.write((np.clip(fr, 0, 1) * 255).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait(); dec.stdout.close(); dec.wait()

    # --- audio: clean voice + sfx + ducked music ---
    N = int(T * SR)
    motion.write_wav(work / "sfx.wav", 0.8 * fx.extra_sfx(motion.sfx_track(N, [(a, b) for a, b in sfx if b in ("pop", "whoosh", "thud")]) +
                                                     _ticks(N, [a for a, b in sfx if b == "tick"]), xsfx))
    music = cfg.get("music")
    inputs = ["-i", str(tmpv), "-i", video, "-i", str(work / "sfx.wav")]
    fc = ("[1:a]highpass=f=80,acompressor=threshold=0.1:ratio=3:attack=10:release=200,loudnorm=I=-16:TP=-2[v];"
          "[v]asplit=2[vv][vk];")
    if music:
        inputs += ["-stream_loop", "-1", "-i", str(HERE / music)]
        fc += (f"[3:a]volume={cfg.get('music_vol', 0.22)},afade=t=in:d=0.8,afade=t=out:st={max(0, T - 2):.2f}:d=2[m];"
               "[m][vk]sidechaincompress=threshold=0.03:ratio=8:attack=15:release=400[md];"
               "[vv][2:a][md]amix=inputs=3:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5[a]")
    else:
        fc += "[vv][2:a]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5[a]"
    subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", fc, "-map", "0:v", "-map", "[a]",
                    "-t", f"{T:.2f}", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)], check=True)
    print("Done:", out)


def _ticks(n, ts):
    out = np.zeros(n, np.float32)
    for at in ts:
        L = int(0.03 * SR); tt = np.arange(L) / SR; i = int(at * SR)
        if i + L < n:
            out[i:i + L] += 0.18 * np.sin(2 * np.pi * 2200 * tt) * np.exp(-tt * 160)
    return out


if __name__ == "__main__":
    main()
