"""Preset library for the v3 engine: extra sound effects, animated charts, subscribe/like widgets,
intro wordmark, end screen, newspaper collage and helpers. Everything is drawn in code (no images),
uses the locked palette, and is triggered from the beat sheet."""
import math
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

SR = 48000
NAVY, MUSTARD, RED, CREAM = (27, 42, 74), (212, 162, 58), (200, 16, 46), (244, 238, 223)
INK = (14, 22, 38)
GREY = (150, 150, 150)


def c01(rgb):
    return tuple(v / 255 for v in rgb)


def ease_out(x):
    x = min(1.0, max(0.0, x)); return 1 - (1 - x) ** 3


def back_out(x):
    x = min(1.0, max(0.0, x)); c = 1.70158
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


# ---------------- sound effects ----------------
def extra_sfx(out, events):
    """Adds the sounds the base engine does not have. events: [(t, kind, arg)]"""
    n = len(out); rng = np.random.default_rng(7)

    def add(at, sig):
        i = int(at * SR)
        if i < 0:
            sig = sig[-i:]; i = 0
        if i < n:
            j = min(n, i + len(sig)); out[i:j] += sig[:j - i]

    def tone(f0, f1, dur, amp, decay=0.0):
        L = int(dur * SR); tt = np.arange(L) / SR
        f = f0 + (f1 - f0) * tt / max(dur, 1e-3)
        env = np.minimum(1, tt / 0.01) * np.minimum(1, (dur - tt) / 0.04)
        if decay:
            env *= np.exp(-tt * decay)
        return amp * np.sin(2 * np.pi * np.cumsum(f) / SR) * env

    for at, kind, arg in events:
        if kind == "ding":                       # end of a counter / reveal
            L = int(0.9 * SR); tt = np.arange(L) / SR
            s = sum(a * np.sin(2 * np.pi * f * tt) for f, a in ((1760, 0.5), (3520, 0.18), (5280, 0.06)))
            add(at, 0.22 * s * np.exp(-tt * 5))
        elif kind == "bell":                     # notification bell
            L = int(1.2 * SR); tt = np.arange(L) / SR
            s = sum(a * np.sin(2 * np.pi * f * tt) for f, a in ((1320, 0.5), (1980, 0.3), (2740, 0.2), (3610, 0.1)))
            trem = 1 + 0.25 * np.sin(2 * np.pi * 14 * tt)
            add(at, 0.2 * s * trem * np.exp(-tt * 3.5))
        elif kind == "click":                    # mouse click
            L = int(0.02 * SR); tt = np.arange(L) / SR
            add(at, 0.35 * rng.standard_normal(L) * np.exp(-tt * 400))
        elif kind == "cash":                     # cash register: two clicks + high bell
            for k in range(2):
                L = int(0.02 * SR); tt = np.arange(L) / SR
                add(at + 0.05 * k, 0.3 * rng.standard_normal(L) * np.exp(-tt * 300))
            L = int(0.8 * SR); tt = np.arange(L) / SR
            s = sum(a * np.sin(2 * np.pi * f * tt) for f, a in ((2093, 0.5), (4186, 0.25), (6279, 0.1)))
            add(at + 0.12, 0.2 * s * np.exp(-tt * 6))
        elif kind == "rise":                     # bar growing: pitch climbs with height (arg = seconds, 0..1 height)
            dur, h = arg
            add(at, tone(300, 300 + 900 * h, dur, 0.07))
        elif kind == "fall":
            dur, h = arg
            add(at, tone(900, 900 - 600 * h, dur, 0.07))
        elif kind == "swoosh":                   # softer, brighter whoosh for transitions
            L = int(0.45 * SR); tt = np.arange(L) / SR
            nz = rng.standard_normal(L)
            k = np.ones(4) / 4; b = np.convolve(nz, k, "same") - np.convolve(nz, np.ones(40) / 40, "same")
            add(at - 0.2, 0.25 * b * np.sin(np.pi * tt / tt[-1]) ** 3)
        elif kind == "shutter":
            for k in range(2):
                L = int(0.03 * SR); tt = np.arange(L) / SR
                add(at + 0.06 * k, 0.3 * rng.standard_normal(L) * np.exp(-tt * 200))
        elif kind == "paper":                    # paper rustle for newspaper clippings
            L = int(0.25 * SR); tt = np.arange(L) / SR
            nz = rng.standard_normal(L) * (rng.random(L) > 0.7)
            add(at, 0.12 * np.convolve(nz, np.ones(3) / 3, "same") * np.sin(np.pi * tt / tt[-1]))
        elif kind == "hit":                      # cinematic hit for chapter cards / big numbers
            L = int(1.0 * SR); tt = np.arange(L) / SR
            body = np.sin(2 * np.pi * (70 * np.exp(-tt * 4) + 38) * tt) * np.exp(-tt * 5)
            add(at, 0.5 * body + 0.15 * rng.standard_normal(L) * np.exp(-tt * 40))
        elif kind == "type":                     # typewriter ticks across arg seconds
            k = 0.0
            while k < arg:
                L = int(0.015 * SR); tt = np.arange(L) / SR
                add(at + k, 0.12 * rng.standard_normal(L) * np.exp(-tt * 500)); k += rng.uniform(0.05, 0.11)
    return out


# ---------------- text helpers ----------------
def font(path, size):
    return ImageFont.truetype(str(path), int(size))


def text_rgba(text, path, size, fill, stroke=0, stroke_fill=NAVY):
    f = font(path, size)
    b = f.getbbox(text, stroke_width=stroke)
    w, h = b[2] - b[0] + 8, b[3] - b[1] + 8
    img = Image.new("RGBA", (max(1, w), max(1, h)), (0, 0, 0, 0))
    ImageDraw.Draw(img).text((4 - b[0], 4 - b[1]), text, font=f, fill=fill + (255,),
                             stroke_width=stroke, stroke_fill=stroke_fill + (255,))
    return img


def paste(canvas, rgba, cx, cy, scale=1.0, alpha=1.0):
    """Alpha-composite a PIL RGBA image onto the float canvas, centred at (cx, cy)."""
    if alpha <= 0.01 or scale <= 0.01:
        return
    if abs(scale - 1) > 1e-3:
        rgba = rgba.resize((max(1, int(rgba.width * scale)), max(1, int(rgba.height * scale))), Image.LANCZOS)
    a = np.asarray(rgba, np.float32) / 255.0
    H, W = canvas.shape[:2]
    x0, y0 = int(cx - a.shape[1] / 2), int(cy - a.shape[0] / 2)
    sx0, sy0 = max(0, -x0), max(0, -y0)
    x0c, y0c = max(0, x0), max(0, y0)
    x1c, y1c = min(W, x0 + a.shape[1]), min(H, y0 + a.shape[0])
    if x1c <= x0c or y1c <= y0c:
        return
    sub = a[sy0:sy0 + (y1c - y0c), sx0:sx0 + (x1c - x0c)]
    al = sub[..., 3:4] * alpha
    canvas[y0c:y1c, x0c:x1c] = canvas[y0c:y1c, x0c:x1c] * (1 - al) + sub[..., :3] * al


def rrect(canvas, x0, y0, x1, y1, color, r=18, alpha=1.0, outline=None, thick=4):
    ov = canvas.copy()
    col = c01(color); x0, y0, x1, y1 = map(int, (x0, y0, x1, y1)); r = int(min(r, (x1 - x0) / 2, (y1 - y0) / 2))
    if x1 <= x0 or y1 <= y0:
        return
    cv2.rectangle(ov, (x0 + r, y0), (x1 - r, y1), col, -1)
    cv2.rectangle(ov, (x0, y0 + r), (x1, y1 - r), col, -1)
    for cx, cy in ((x0 + r, y0 + r), (x1 - r, y0 + r), (x0 + r, y1 - r), (x1 - r, y1 - r)):
        cv2.circle(ov, (cx, cy), r, col, -1, cv2.LINE_AA)
    if outline:
        cv2.rectangle(ov, (x0, y0), (x1, y1), c01(outline), thick, cv2.LINE_AA)
    canvas[:] = canvas * (1 - alpha) + ov * alpha


# ---------------- charts ----------------
class Bars:
    """Animated bar chart. items: [{label, value, color?}], bars grow one after another,
    values count up, the highlighted bar gets a red outline. Sound: pop + rising tone per bar."""
    def __init__(self, e, fonts, W, H):
        self.e = e; self.items = e["items"]; self.fonts = fonts
        self.x, self.y = e.get("x", 0.5) * W, e.get("y", 0.55) * H
        self.w, self.h = e.get("w", 0.62) * W, e.get("h", 0.5) * H
        self.vmax = max(i["value"] for i in self.items) * 1.08
        self.step = e.get("step", 0.55); self.grow = 0.7
        self.suffix = e.get("suffix", "")
        self.labels = [text_rgba(i["label"], fonts["mont"], 40, NAVY) for i in self.items]

    def sounds(self, t0):
        out = []
        for k, it in enumerate(self.items):
            at = t0 + k * self.step
            out += [(at, "pop", None), (at, "rise", (self.grow, it["value"] / self.vmax))]
        out.append((t0 + (len(self.items) - 1) * self.step + self.grow, "ding", None))
        return out

    def draw(self, c, lt):
        n = len(self.items); gap = self.w / n; bw = gap * 0.58
        base = self.y + self.h / 2
        appear = min(1, lt / 0.3)
        cv2.line(c, (int(self.x - self.w / 2), int(base)), (int(self.x - self.w / 2 + self.w * ease_out(lt / 0.4)), int(base)),
                 c01(NAVY), 5, cv2.LINE_AA)
        for k, it in enumerate(self.items):
            p = ease_out((lt - k * self.step) / self.grow)
            if p <= 0:
                continue
            cx = self.x - self.w / 2 + gap * (k + 0.5)
            hh = self.h * 0.82 * it["value"] / self.vmax * p
            col = {"red": RED, "mustard": MUSTARD, "grey": GREY}.get(it.get("color"), NAVY)
            rrect(c, cx - bw / 2, base - hh, cx + bw / 2, base, col, r=10)
            if it.get("hl") and p >= 1:
                cv2.rectangle(c, (int(cx - bw / 2 - 10), int(base - hh - 10)), (int(cx + bw / 2 + 10), int(base + 4)), c01(RED), 6, cv2.LINE_AA)
            if not self.e.get("novalue"):
                v = it["value"] * p
                vs = (f"{v:,.0f}".replace(",", " ") if it["value"] >= 10 or p < 1 else f"{v:g}") + self.suffix
                paste(c, text_rgba(vs, self.fonts["anton"], 64, col if col != GREY else NAVY), cx, base - hh - 46, 1.0, appear)
            paste(c, self.labels[k], cx, base + 40, 1.0, min(1, p * 3))


class Pie:
    """Donut that sweeps in slice by slice; the first slice is the hero (red) and pops out."""
    def __init__(self, e, fonts, W, H):
        self.e = e; self.sl = e["slices"]; self.fonts = fonts
        self.x, self.y = e.get("x", 0.35) * W, e.get("y", 0.55) * H
        self.r = e.get("r", 0.3) * H
        tot = sum(s["value"] for s in self.sl)
        self.frac = [s["value"] / tot for s in self.sl]
        self.legend = [text_rgba(f'{s["label"]}  {s["value"]:g}%', fonts["mont"], 44, NAVY) for s in self.sl]

    def sounds(self, t0):
        return [(t0 + 0.45 * k, "pop", None) for k in range(len(self.sl))] + [(t0 + 0.45 * len(self.sl), "ding", None)]

    def draw(self, c, lt):
        cols = [RED, NAVY, MUSTARD, GREY, (120, 140, 170)]
        start = -90
        for k, f in enumerate(self.frac):
            p = ease_out((lt - 0.45 * k) / 0.5)
            if p <= 0:
                start += 360 * f; continue
            off = 18 * p if k == 0 else 0
            mid = math.radians(start + 180 * f)
            cx, cy = self.x + off * math.cos(mid), self.y + off * math.sin(mid)
            cv2.ellipse(c, (int(cx), int(cy)), (int(self.r), int(self.r)), 0, start, start + 360 * f * p, c01(cols[k % len(cols)]), -1, cv2.LINE_AA)
            start += 360 * f
        cv2.circle(c, (int(self.x), int(self.y)), int(self.r * 0.55), c01(CREAM), -1, cv2.LINE_AA)
        for k, lg in enumerate(self.legend):
            a = min(1, max(0, (lt - 0.45 * k) / 0.3))
            lx = self.x + self.r + 60
            ly = self.y - self.r * 0.6 + k * 80
            cv2.rectangle(c, (int(lx), int(ly - 18)), (int(lx + 36), int(ly + 18)), c01(cols[k % len(cols)]), -1)
            paste(c, lg, lx + 60 + lg.width / 2, ly, 1.0, a)


class Subscribe:
    """Red OBUNA button pops in a corner, a cursor glides to it, clicks, the bell rings."""
    def __init__(self, e, fonts, W, H, label, done):
        self.W, self.H = W, H; self.fonts = fonts
        self.btn = text_rgba(label, fonts["mont"], 40, (255, 255, 255))
        self.btn2 = text_rgba(done, fonts["mont"], 40, (255, 255, 255))
        self.x = e.get("x", 0.17) * W; self.y = e.get("y", 0.86) * H
        self.dur = e.get("dur", 3.2)

    def sounds(self, t0):
        return [(t0, "pop", None), (t0 + 1.0, "click", None), (t0 + 1.15, "bell", None)]

    def draw(self, c, lt):
        if lt > self.dur:
            return
        sc = back_out(lt / 0.35) * (1 - ease_out((lt - self.dur + 0.3) / 0.3))
        if sc <= 0.01:
            return
        clicked = lt > 1.0
        b = self.btn2 if clicked else self.btn
        w, h = (b.width + 70) * sc, (b.height + 34) * sc
        rrect(c, self.x - w / 2, self.y - h / 2, self.x + w / 2, self.y + h / 2, GREY if clicked else RED, r=h / 2)
        paste(c, b, self.x, self.y, sc)
        # bell icon to the right
        bx, by = self.x + w / 2 + 50 * sc, self.y
        ang = math.sin(lt * 30) * 18 * math.exp(-(lt - 1.15) * 3) if lt > 1.15 else 0
        r = 26 * sc
        M = cv2.getRotationMatrix2D((bx, by - r), ang, 1.0)
        pts = np.array([[bx - r, by + r * 0.6], [bx - r * 0.8, by - r * 0.5], [bx, by - r * 1.2], [bx + r * 0.8, by - r * 0.5], [bx + r, by + r * 0.6]])
        pts = (np.c_[pts, np.ones(len(pts))] @ M.T).astype(np.int32)
        cv2.fillPoly(c, [pts], c01(MUSTARD), cv2.LINE_AA)
        cv2.circle(c, tuple(int(v) for v in (np.array([bx, by + r * 0.85, 1]) @ M.T)), int(r * 0.25), c01(MUSTARD), -1, cv2.LINE_AA)
        # cursor
        if 0.35 < lt < 1.6:
            p = ease_out((lt - 0.35) / 0.6)
            cx = self.x + self.W * 0.18 * (1 - p); cy = self.y + self.H * 0.12 * (1 - p)
            tri = np.array([[cx, cy], [cx, cy + 46], [cx + 13, cy + 34], [cx + 32, cy + 34]], np.int32)
            cv2.fillPoly(c, [tri], (1, 1, 1), cv2.LINE_AA); cv2.polylines(c, [tri], True, c01(INK), 3, cv2.LINE_AA)


class Like:
    """Heart + LAYK pill, pops and beats twice."""
    def __init__(self, e, fonts, W, H, label):
        self.x = e.get("x", 0.83) * W; self.y = e.get("y", 0.86) * H
        self.lbl = text_rgba(label, fonts["mont"], 40, (255, 255, 255)); self.dur = e.get("dur", 3.0)

    def sounds(self, t0):
        return [(t0, "pop", None), (t0 + 0.6, "click", None)]

    def draw(self, c, lt):
        if lt > self.dur:
            return
        sc = back_out(lt / 0.35) * (1 - ease_out((lt - self.dur + 0.3) / 0.3))
        beat = 1 + 0.12 * max(0, math.sin((lt - 0.6) * 12)) if 0.6 < lt < 1.4 else 1
        w, h = (self.lbl.width + 120) * sc, (self.lbl.height + 34) * sc
        rrect(c, self.x - w / 2, self.y - h / 2, self.x + w / 2, self.y + h / 2, RED, r=h / 2)
        hx, hy, r = self.x - w / 2 + 44 * sc, self.y, 13 * sc * beat
        cv2.circle(c, (int(hx - r), int(hy - r * 0.3)), int(r), (1, 1, 1), -1, cv2.LINE_AA)
        cv2.circle(c, (int(hx + r), int(hy - r * 0.3)), int(r), (1, 1, 1), -1, cv2.LINE_AA)
        cv2.fillPoly(c, [np.int32([[hx - 2 * r, hy], [hx + 2 * r, hy], [hx, hy + 2.2 * r]])], (1, 1, 1), cv2.LINE_AA)
        paste(c, self.lbl, self.x + 22 * sc, self.y, sc)


class News:
    """Newspaper clippings fly in one by one; the last one carries the key word in a red box."""
    def __init__(self, e, fonts, W, H, word):
        self.W, self.H = W, H; self.n = e.get("n", 3)
        self.word = text_rgba(word, fonts["anton"], 96, NAVY)
        rng = np.random.default_rng(len(word))
        self.pos = [(W * (0.3 + 0.4 * rng.random()), H * (0.35 + 0.25 * rng.random()), rng.uniform(-9, 9)) for _ in range(self.n)]
        self.pos[-1] = (W * 0.5, H * 0.48, -3)
        self.cards = [self._card(rng, k == self.n - 1) for k in range(self.n)]

    def _card(self, rng, hero):
        w, h = (int(self.word.width + 160), 360) if hero else (int(rng.uniform(420, 560)), int(rng.uniform(280, 360)))
        img = Image.new("RGBA", (w, h), (250, 247, 238, 255)); d = ImageDraw.Draw(img)
        d.rectangle((0, 0, w - 1, h - 1), outline=(190, 185, 170, 255), width=3)
        d.rectangle((24, 22, w - 24, 52), fill=NAVY + (255,))
        y = 140 if hero else 76
        while y < h - 20:
            ww = rng.uniform(0.55, 0.95) * (w - 48)
            d.rectangle((24, y, 24 + ww, y + 9), fill=(185, 182, 172, 255)); y += 22
        if hero:
            img.alpha_composite(self.word, ((w - self.word.width) // 2, 62))
        return img

    def sounds(self, t0):
        return [(t0 + 0.35 * k, "paper", None) for k in range(self.n)] + [(t0 + 0.35 * (self.n - 1) + 0.45, "thud", None)]

    def draw(self, c, lt):
        for k, (x, y, rot) in enumerate(self.pos):
            p = ease_out((lt - 0.35 * k) / 0.35)
            if p <= 0:
                continue
            card = self.cards[k].rotate(rot, expand=True, resample=Image.BICUBIC)
            paste(c, card, x + (1 - p) * self.W * 0.6 * (1 if k % 2 else -1), y, 1.0, min(1, p * 2))
            if k == self.n - 1 and lt - 0.35 * k > 0.5:
                q = ease_out((lt - 0.35 * k - 0.5) / 0.4)
                ww, hh = self.word.width + 30, self.word.height + 20
                cv2.rectangle(c, (int(x - ww / 2), int(y - 180 + 62 + 4 - 10)), (int(x - ww / 2 + ww * q), int(y - 180 + 62 + hh)), c01(RED), 6, cv2.LINE_AA)


def end_frames(c, lt, W, H, fonts, label):
    """Four empty 'watch next' frames (YouTube end-screen slots) around the centre."""
    lab = text_rgba(label, fonts["mont"], 34, NAVY)
    fw, fh = W * 0.27, W * 0.27 * 9 / 16
    slots = [(W * 0.2, H * 0.3), (W * 0.2, H * 0.68), (W * 0.8, H * 0.3), (W * 0.8, H * 0.68)]
    for k, (x, y) in enumerate(slots):
        p = back_out((lt - 0.15 * k) / 0.4)
        if p <= 0.01:
            continue
        w, h = fw * p, fh * p
        rrect(c, x - w / 2, y - h / 2, x + w / 2, y + h / 2, (233, 226, 208), r=14)
        x0, y0, x1, y1 = int(x - w / 2), int(y - h / 2), int(x + w / 2), int(y + h / 2)
        for xx in range(x0, x1, 28):                    # dashed border
            cv2.line(c, (xx, y0), (min(xx + 14, x1), y0), c01(NAVY), 3); cv2.line(c, (xx, y1), (min(xx + 14, x1), y1), c01(NAVY), 3)
        for yy in range(y0, y1, 28):
            cv2.line(c, (x0, yy), (x0, min(yy + 14, y1)), c01(NAVY), 3); cv2.line(c, (x1, yy), (x1, min(yy + 14, y1)), c01(NAVY), 3)
        cv2.circle(c, (int(x), int(y)), int(34 * p), c01(RED), -1, cv2.LINE_AA)
        cv2.fillPoly(c, [np.int32([[x - 10 * p, y - 16 * p], [x - 10 * p, y + 16 * p], [x + 16 * p, y]])], (1, 1, 1), cv2.LINE_AA)
        paste(c, lab, x, y + h / 2 + 34, p)


def wordmark(fonts, size=230):
    """'Bilmas' in cream + 'boy' in mustard, one image."""
    a = text_rgba("Bilmas", fonts["anton"], size, CREAM)
    b = text_rgba("boy", fonts["anton"], size, MUSTARD)
    img = Image.new("RGBA", (a.width + b.width - 8, max(a.height, b.height)), (0, 0, 0, 0))
    img.alpha_composite(a, (0, 0)); img.alpha_composite(b, (a.width - 8, 0))
    return img


def zoom_into(frame, fx, fy, p, W, H):
    """Transition helper: zoom the frame towards (fx, fy) by up to 4x."""
    z = 1 + 3 * p ** 2
    M = np.float32([[z, 0, fx * W * (1 - z)], [0, z, fy * H * (1 - z)]])
    M[0, 2] += (W / 2 - fx * W) * p; M[1, 2] += (H / 2 - fy * H) * p
    return cv2.warpAffine(frame, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def whip(a, b, p, W):
    """Whip-pan transition: a slides out left with motion blur, b slides in from the right."""
    off = int(W * ease_out(p))
    out = np.empty_like(a)
    out[:, : W - off] = a[:, off:]
    out[:, W - off:] = b[:, : off]
    k = int(5 + 60 * math.sin(math.pi * p))
    return cv2.blur(out, (k, 1)) if k > 1 else out
