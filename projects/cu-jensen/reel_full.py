"""California Uzbek reel: Jensen Huang / Nvidia. Style B: captions + tags + full-screen pictures, no music.
python3 reel_full.py [PREVIEW=t1,t2,...]"""
import os, sys, json, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, "/home/claude/explainer-engine")
import fx, motion, build

W, H, FPS, SR = 1080, 1920, 30, 48000
SRC = "raw.mp4"
END_SPEECH = 137.3                      # after this the clip is left untouched
F = "/home/claude/explainer-engine/fonts/"
MONT, ANTON = F + "Montserrat-ExtraBold.ttf", F + "Anton-Regular.ttf"
RED, BLACK, WHITE, GREEN, DGREEN = (226, 35, 26), (12, 12, 12), (255, 255, 255), (118, 185, 0), (30, 160, 80)
DUR = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", SRC], capture_output=True, text=True).stdout)

# ---------------- words ----------------
SEGS = [   # first 47 s: speech regions (silence detection) + spoken text; Whisper fails on this part
    (0.15, 2.80, "Bir insonning mehnati dollarda necha pulga baholanishi mumkin?"),
    (3.24, 6.14, "AQSh birjasidagi eng katta kompaniya"),
    (6.45, 7.03, "qanday qilib"),
    (7.25, 8.71, "bir kunda trillion dollar"),
    (9.04, 9.96, "qiymatda bir kishi sabab"),
    (10.33, 11.60, "o'zgarishlarga sabab bo'lmoqda?"),
    (12.17, 13.60, "Trillion dollar, Karl!"),
    (13.94, 19.11, "Mana bu Jensen Huang, u barchamiz guvohi bo'layotgan ChatGPT va Claude sun'iy idrok platformalari rivojlanishi"),
    (19.45, 23.52, "va poygasining eng markazida turgan Nvidia deb nomlangan ilg'or chip ishlab chiqaruvchi"),
    (23.89, 26.55, "kompaniya asoschisi va ko'p yillik rahbari edi."),
    (27.03, 28.51, "Aytganday, kompaniyaning birjadagi"),
    (28.80, 31.53, "hozirgacha eng yuqori bozor qiymati taxminan"),
    (31.71, 32.77, "5 trillion dollardan"),
    (33.18, 34.75, "qimmatroqqa baholangan edi."),
    (34.99, 40.00, "O'tgan haftalar davomida, u uzoq yillik turmush o'rtog'iga bir necha ayollar bilan xiyonat qilgani,"),
    (40.00, 44.00, "ulardan biri esa aynan AQSh sun'iy idrok borasida musobaqalashayotgan"),
    (44.00, 47.08, "Xitoyning ayol josusi ekanligi sizib chiqqandi."),
]
TAIL = [   # from 47 s: aligned to Whisper word times (DP, like build.py)
    "Bu xabardan keyin esa Jensen yaqin aloqada bo'lgan boshqa ayollar haqida ham turli xabarlar tarqalgandi.",
    "Jensen dastlabki tarqalgan xabarlarning ertasi kunidayoq tan olib, kompaniya xodimlaridan va oilasidan e-mail orqali ommaviy uzr so'rab chiqqandi.",
    "Keyinroq ayollarning soni ko'payishi, AQSh hukumatining tekshiruvlari, jamoatchilik va kompaniya boshqaruv kengashi bosimi ostida iste'fo berib, ishdan bo'shashini e'lon qilgandi.",
    "Bugun u ko'plab yuqori darajadagi insonlar, xususan Ilon Mask va Tramp kabi insonlarning va ko'p sonli xodimlari tomonidan qo'llab-quvvatlanishi asosida o'z lavozimiga qaytgandi.",
    "Endi asosiy mavzuga qaytsak,",
    "U ketishi bilan kompaniya o'sha vaqtdagi 4 trillion qiymatidan deyarli 1 trillion dollar qiymatini yo'qotib, 3 trillionga tushgandi.",
    "Bugun uning boshqaruvchi sifatida qaytishi, kompaniya qiymatini yana qaytib 4 trillion dollardan oshirib yubordi.",
    "@@@ @@@ @@@ @@@ @@@ @@@ @@@",       # 99.1-102.6: unclear in the recording, no caption (placeholder words)
    "Uni qo'llab-quvvatlaganlar ham, qoralaganlar ham bo'ldi albatta.",
    "Ammo axloqiy va oilaviy muammolarga qaramasdan o'z ishiga qayta tiklanishi, uning davrimizning eng ilg'or kompaniyasidagi o'rni qanchalik muhim ekanini,",
    "Nvidia kompaniyasi tashkil topgandan buyon qilingan mehnati va hozirgi ta'sir doirasiga zarar bera olmadi.",
    "Masalaga qaysi tomondan qaramang, uning uzoq yillik mehnati va ayni sohadagi bilimlari, har qanday oilaviy mojarodan ustunroq bo'lib chiqdi.",
    "Aytganday, o'zimizdagi Imarat va Iman ishlari qalay ketyapti?",
    "Hal bo'lib qoldimi? Fikrlaringizni izohlarda qoldirishni unutmang.",
]
words = []      # [t0, t1, word, group]
for si, (a, b, txt) in enumerate(SEGS):
    ws = txt.split(); tot = sum(len(w) + 2 for w in ws); t = a
    for w in ws:
        d = (b - a) * (len(w) + 2) / tot; words.append([t, t + d, w, si]); t += d
asr = json.load(open("asr_tail.json"))
tw, gid = [], []
for k, s in enumerate(TAIL):
    for w in s.split(): tw.append(w); gid.append(100 + k)
times, nmatch = build.align(tw, asr)
for w, g, (a, b) in zip(tw, gid, times):
    words.append([a, max(b, a + 0.12), w, g])
# placeholder words: hide, and keep times monotonic
words = [w for w in words if not w[2].startswith("@@@")]
for i in range(1, len(words)):
    if words[i][0] < words[i - 1][0]: words[i][0] = words[i - 1][0] + 0.05
print("aligned", nmatch, "of", len(tw))

def wt(prefix, n=0, after=0):
    hits = [w for w in words if w[0] >= after and w[2].lower().strip(",.?!").startswith(prefix.lower())]
    return hits[n][0]

_cf = ImageFont.truetype(MONT, 82)
def _w(ws): return sum(_cf.getbbox(x[2].upper(), stroke_width=6)[2] for x in ws) + 26 * (len(ws) - 1)
chunks, cur = [], []
for w in words:
    if cur and (len(cur) == 3 or w[3] != cur[-1][3] or cur[-1][2][-1] in ",.?!" or _w(cur + [w]) > 900 or w[0] - cur[-1][1] > 0.6):
        chunks.append(cur); cur = []
    cur.append(w)
chunks.append(cur)

# ---------------- drawing helpers ----------------
_fc = {}
def font(p, s):
    k = (p, int(s))
    if k not in _fc: _fc[k] = ImageFont.truetype(p, int(s))
    return _fc[k]
def ease(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3
def back(x, s=1.7): x = max(0, min(1, x)) - 1; return x * x * ((s + 1) * x + s) + 1

def text_img(txt, p, size, fill, stroke=0, sfill=BLACK):
    f = font(p, size); bb = f.getbbox(txt, stroke_width=stroke)
    im = Image.new("RGBA", (bb[2] - bb[0] + 4, bb[3] - bb[1] + 4))
    ImageDraw.Draw(im).text((2 - bb[0], 2 - bb[1]), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=sfill)
    return im

def shadowed(im, r=14, off=8, a=110):
    s = Image.new("RGBA", (im.width + 4 * r, im.height + 4 * r))
    m = Image.new("RGBA", im.size, (0, 0, 0, a)); m.putalpha(im.split()[3].point(lambda v: v * a // 255))
    s.alpha_composite(m, (2 * r, 2 * r + off)); s = s.filter(ImageFilter.GaussianBlur(r))
    s.alpha_composite(im, (2 * r, 2 * r)); return s

def chip(txt, size=56, fg=WHITE, bg=BLACK, dot=None, maxw=980):
    t = text_img(txt, MONT, size, fg)
    while t.width > maxw - 120 and size > 30:
        size -= 2; t = text_img(txt, MONT, size, fg)
    pad = (30, 18); extra = 34 if dot else 0
    w, h = t.width + pad[0] * 2 + extra, t.height + pad[1] * 2
    im = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=h // 2, fill=bg)
    if dot: d.ellipse([pad[0], h // 2 - 10, pad[0] + 20, h // 2 + 10], fill=dot)
    im.alpha_composite(t, (pad[0] + extra, pad[1]))
    return shadowed(im)

def big_card(top, sub, color=RED):
    a = text_img(top, ANTON, 118, color); b = text_img(sub, MONT, 38, BLACK)
    w = max(a.width, b.width) + 90; h = a.height + b.height + 70
    im = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=30, fill=WHITE)
    im.alpha_composite(a, ((w - a.width) // 2, 24)); im.alpha_composite(b, ((w - b.width) // 2, a.height + 40))
    return shadowed(im)

def stamp(lines, color=RED, sizes=(120, 190)):
    ims = [text_img(l, ANTON, s, color, 7, WHITE) for l, s in zip(lines, sizes)]
    w = max(i.width for i in ims); h = sum(i.height for i in ims) - 10 * (len(ims) - 1)
    out = Image.new("RGBA", (w, h)); y = 0
    for i in ims: out.alpha_composite(i, ((w - i.width) // 2, y)); y += i.height - 10
    return out

def put(canvas, im, cx, cy, scale=1.0, alpha=1.0, rot=0):
    if scale <= 0.01 or alpha <= 0.01: return
    if scale != 1: im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BICUBIC)
    if rot: im = im.rotate(rot, Image.BICUBIC, expand=True)
    if alpha < 1:
        im = im.copy(); im.putalpha(im.split()[3].point(lambda v: int(v * alpha)))
    canvas.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))

def pop_in(t, t0, t1, dur=0.35):
    if t < t0 or t > t1 + 0.25: return 0, 0
    s = back((t - t0) / dur); a = min(1, (t - t0) / 0.12)
    if t > t1: k = (t - t1) / 0.25; s *= 1 - 0.3 * k; a *= 1 - k
    return s, a

def portrait(path, px, box):
    im = Image.open(path).convert("RGB"); w, h = im.size
    im = im.crop((int(w * box[0]), int(h * box[1]), int(w * box[2]), int(h * box[3]))).resize((px, px), Image.LANCZOS)
    m = Image.new("L", (px, px)); ImageDraw.Draw(m).ellipse([0, 0, px - 1, px - 1], fill=255)
    out = Image.new("RGBA", (px + 16, px + 16)); ImageDraw.Draw(out).ellipse([0, 0, px + 15, px + 15], fill=WHITE)
    out.paste(im, (8, 8), m); return out

def nametag():
    p = portrait("photos/jensen1.jpg", 190, (0.30, 0.10, 0.62, 0.34))
    n1 = text_img("JENSEN HUANG", ANTON, 92, WHITE); n2 = text_img("Nvidia asoschisi va rahbari", MONT, 40, BLACK)
    w = max(n1.width, n2.width) + 60
    card = Image.new("RGBA", (w + 150, n1.height + n2.height + 72)); d = ImageDraw.Draw(card)
    d.rectangle([110, 0, w + 150, n1.height + 40], fill=RED); d.rectangle([110, n1.height + 40, w + 110, card.height - 1], fill=WHITE)
    card.alpha_composite(n1, (180, 20)); card.alpha_composite(n2, (180, n1.height + 52))
    out = Image.new("RGBA", (card.width + 110, max(card.height, p.height)))
    out.alpha_composite(card, (110, (out.height - card.height) // 2)); out.alpha_composite(p, (0, (out.height - p.height) // 2))
    return shadowed(out)

# ---------------- pictures ----------------
_pc = {}
def cover(path, focus_y=0.4):
    if path not in _pc:
        im = Image.open(path).convert("RGB"); r = max(W / im.width, H / im.height) * 1.12
        im = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
        if im.width / im.height > W / H * 1.3 or path in CARD:   # landscape: blurred fill + sharp picture
            src = Image.open(path).convert("RGB")
            bg = src.resize((int(src.width * H * 1.12 / src.height), int(H * 1.12))).filter(ImageFilter.GaussianBlur(40))
            bg = Image.eval(bg, lambda v: int(v * 0.55))
            fh = 1000; fw = max(int(W * 1.12), int(src.width * fh / src.height)); fh = int(src.height * fw / src.width)
            sharp = src.resize((fw, fh), Image.LANCZOS)
            x0 = (bg.width - fw) // 2; bg.paste(sharp, (x0, int(bg.height * 0.36 - fh / 2)))
            im = bg.crop(((bg.width - int(W * 1.12)) // 2, 0, (bg.width - int(W * 1.12)) // 2 + int(W * 1.12), bg.height))
        _pc[path] = im
    return _pc[path]

def pic_frame(path, p, zin, focus_y=0.35):
    im = cover(path); z = 1 + 0.10 * (p if zin else 1 - p)
    vw, vh = int(im.width / z), int(im.height / z)
    x0 = (im.width - vw) // 2; y0 = int((im.height - vh) * focus_y)
    return im.crop((x0, y0, x0 + vw, y0 + vh)).resize((W, H), Image.BILINEAR)

def duo():
    out = Image.new("RGB", (W, H), BLACK)
    for k, (p, fy) in enumerate((("photos/musk.jpg", 0.15), ("photos/trump.jpg", 0.12))):
        im = Image.open(p).convert("RGB"); r = max(W / im.width, (H / 2) / im.height)
        im = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
        y0 = int((im.height - H // 2) * fy); x0 = (im.width - W) // 2
        out.paste(im.crop((x0, y0, x0 + W, y0 + H // 2)), (0, k * H // 2))
    ImageDraw.Draw(out).rectangle([0, H // 2 - 4, W, H // 2 + 4], fill=WHITE)
    out.save("duo.jpg", quality=95); return "duo.jpg"

CARD = {"photos/nvidia_hq.jpg", "photos/capitol.jpg"}

# chart cutaway: Nvidia market value bars
_bg = None
def chart(t, t0, stage):
    global _bg
    if _bg is None:
        b = Image.open("img1.png").convert("RGB").resize((W, H)).filter(ImageFilter.GaussianBlur(18))
        _bg = Image.eval(b, lambda v: int(v * 0.35))
    c = _bg.copy().convert("RGBA"); d = ImageDraw.Draw(c)
    title = text_img("NVIDIA BOZOR QIYMATI", ANTON, 96, WHITE); c.alpha_composite(title, ((W - title.width) // 2, 220))
    bars = [("OLDIN", 4.0, WHITE, "$4T"), ("KETGACH", 3.0, RED, "$3T")] + ([("BUGUN", 4.0, GREEN, "$4T+")] if stage == 2 else [])
    base, top = 1110, 470; bw = 230; gap = 70; n = len(bars)
    x = (W - (n * bw + (n - 1) * gap)) // 2
    for k, (lab, v, col, txt) in enumerate(bars):
        start = t0 + (0.3 + 0.5 * k if stage == 1 else (0 if k < 2 else 0.6))
        p = ease((t - start) / 0.9)
        if stage == 2 and k < 2: p = 1
        h = (base - top) * v / 4.4 * p
        d.rounded_rectangle([x, base - h, x + bw, base], radius=16, fill=col)
        lt = text_img(lab, MONT, 40, WHITE); c.alpha_composite(lt, (x + (bw - lt.width) // 2, base + 20))
        if p > 0.6:
            vt = text_img(txt, ANTON, 84, WHITE, 5, BLACK); c.alpha_composite(vt, (x + (bw - vt.width) // 2, int(base - h - vt.height - 12)))
        x += bw + gap
    return c

# ---------------- timeline ----------------
T = dict(karl=12.17, jen=13.94, gpt=wt("chatgpt"), cl=wt("claude"), nv=wt("nvidia"), yrs=wt("asoschisi"),
         five=31.71, nyt=wt("boshqa", after=47), uzr=wt("ommaviy"), kong=wt("tekshiruvlari"), istefo=wt("iste'fo"),
         mask=wt("ilon"), xod=wt("xodimlari", after=70), qayt=wt("lavozimiga"), drop=wt("ketishi"), tush=wt("3", after=84),
         bugun2=wt("bugun", after=92), osh=wt("oshirib"), qol=wt("qo'llab-quvvatlaganlar"), qor=wt("qoralaganlar"),
         ilgor=wt("davrimizning"), nv2=wt("nvidia", after=110), izoh=wt("fikrlaringizni"))
print({k: round(v, 2) for k, v in T.items()})
DUO = duo()
CUTS = [  # t0, t1, picture, zoom-in?, focus
    (3.24, 6.30, "photos/nyse.jpg", 1, 0.3),
    (7.25, 11.70, "img4.png", 1, 0.3),
    (T["jen"], 17.10, "photos/jensen2.jpg", 0, 0.15),
    (T["nv"] - 0.2, 23.60, "photos/nvidia_hq.jpg", 1, 0.3),
    (28.80, 33.10, "img3.png", 1, 0.35),
    (35.40, 39.80, "img5.png", 1, 0.35),
    (40.20, 46.10, "img7.png", 0, 0.35),
    (T["nyt"] - 0.3, T["nyt"] + 3.6, "photos/jensen1.jpg", 1, 0.12),
    (T["uzr"] - 1.5, T["uzr"] + 2.6, "img6.png", 1, 0.35),
    (T["kong"] - 0.4, T["kong"] + 3.2, "photos/capitol.jpg", 1, 0.3),
    (T["mask"] - 0.3, T["mask"] + 3.0, DUO, 0, 0.0),
    (T["ilgor"] - 0.2, T["ilgor"] + 4.0, "photos/nvidia_hq.jpg", 0, 0.3),
    (T["nv2"], T["nv2"] + 4.2, "photos/jensen2.jpg", 1, 0.12),
]
CHARTS = [(T["drop"] + 0.6, 92.6, 1), (T["bugun2"] + 0.8, 102.7, 2)]
TAGS = [  # t0, t1, sprite, y
    (0.3, 2.8, "hook", 1230),
    (3.3, 6.3, chip("AQSh BIRJASI: ENG KATTA KOMPANIYA", 50, dot=RED), 1230),
    (T["jen"], 19.1, nametag(), 1230),
    (T["nv"], 23.5, chip("NVIDIA", 66, BLACK, GREEN), 1230),
    (T["yrs"], 26.8, chip("1993 → BUGUN · 33 YIL RAHBAR", 52, dot=RED), 1230),
    (T["five"], 34.8, big_card("$5 TRILLION+", "OKTYABR 2026 · TARIXIY CHO'QQI"), 1180),
    (35.8, 39.9, chip("XIYONAT JANJALI", 60, dot=RED), 1230),
    (44.0, 47.3, chip("GUMON: XITOY JOSUSI", 60, WHITE, RED), 1230),
    (T["nyt"], T["nyt"] + 3.5, chip("NEW YORK TIMES VA REUTERS", 52, dot=RED), 1230),
    (T["uzr"], T["uzr"] + 2.6, chip("9-NOYABR: OMMAVIY UZR", 56, dot=RED), 1230),
    (T["kong"], T["kong"] + 3.2, chip("KONGRESS TEKSHIRUVI", 58, dot=RED), 1230),
    (T["istefo"], T["istefo"] + 2.6, chip("12-NOYABR: ISTE'FO", 60, WHITE, RED), 1230),
    (T["xod"], T["xod"] + 2.4, chip("PETITSIYA: 190 000+ IMZO", 54, dot=RED), 1230),
    (T["qayt"], T["qayt"] + 2.4, chip("23-NOYABR: QAYTDI", 60, BLACK, GREEN), 1230),
    (T["qol"], 105.8, chip("QO'LLAGANLAR", 56, WHITE, DGREEN), 1150),
    (T["qor"], 105.8, chip("QORALAGANLAR", 56, WHITE, RED), 1290),
    (T["nv2"] + 0.2, T["nv2"] + 4.1, chip("1993-YILDAN BERI", 60, dot=RED), 1230),
    (T["izoh"], END_SPEECH, chip("FIKRINGIZNI IZOHLARDA YOZING ↓", 50, BLACK, WHITE), 1230),
]
STAMPS = [(T["karl"], 13.85, stamp(["TRILLION DOLLAR,", "KARL!"])),
          (T["tush"], 92.5, stamp(["-$1 TRILLION"], RED, (150,))),
          (T["osh"], 102.6, stamp(["+$1 TRILLION"], DGREEN, (150,)))]

def hook_card(t):
    a = text_img("1 INSON MEHNATI =", MONT, 54, BLACK); b = text_img("?" if int(t * 8) % 2 == 0 else "$", ANTON, 120, RED)
    w = a.width + 160; h = 150; im = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=28, fill=WHITE)
    im.alpha_composite(a, (36, (h - a.height) // 2)); im.alpha_composite(b, (w - 36 - b.width, (h - b.height) // 2))
    return shadowed(im)

def counter(t, t0):
    v = int(1_000_000_000_000 * ease((t - t0) / 1.4))
    return big_card("$" + f"{v:,}".replace(",", " "), "1 TRILLION DOLLAR")

CAP_Y = 1470
def caption(t):
    if t >= END_SPEECH: return None, 0
    for i, ch in enumerate(chunks):
        end = chunks[i + 1][0][0] if i + 1 < len(chunks) else ch[-1][1] + 0.4
        end = min(end, ch[-1][1] + 0.6)
        if ch[0][0] - 0.05 <= t < end: break
    else: return None, 0
    f = font(MONT, 82); sp = 26; parts = [w[2].upper() for w in ch]
    sizes = [f.getbbox(p, stroke_width=6) for p in parts]
    tw_ = sum(b[2] - b[0] for b in sizes) + sp * (len(parts) - 1)
    im = Image.new("RGBA", (tw_ + 60, 140)); d = ImageDraw.Draw(im); x = 30
    for k, (w, p, b) in enumerate(zip(ch, parts, sizes)):
        ww = b[2] - b[0]; nxt = ch[k + 1][0] if k + 1 < len(ch) else w[1] + 0.3
        if w[0] <= t < nxt: d.rounded_rectangle([x - 14, 14, x + ww + 14, 126], radius=18, fill=RED)
        d.text((x - b[0], 70 - (b[3] + b[1]) // 2), p, font=f, fill=WHITE, stroke_width=6, stroke_fill=BLACK)
        x += ww + sp
    age = t - ch[0][0]; k = min(1.0, 1000 / im.width)
    return im, (back(age / 0.18, 1.2) if age < 0.18 else 1.0) * k

# ---------------- audio (voice + sound effects, no music) ----------------
def audio():
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", SRC, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout
    voice = np.frombuffer(raw, np.float32).copy(); n = len(voice)
    sfx = [(a, "pop") for a, _, _, _ in TAGS] + [(a, "whoosh") for a, *_ in CUTS] + [(a, "whoosh") for a, *_ in CHARTS]
    xs = [(T["karl"], "hit", None), (9.0, "cash", None), (T["tush"], "hit", None), (T["osh"], "cash", None),
          (CHARTS[0][0] + 0.8, "fall", (0.8, 0.6)), (CHARTS[1][0] + 0.6, "rise", (0.9, 0.8))]
    s = motion.sfx_track(n, sfx); s = fx.extra_sfx(s, xs)
    out = voice + 0.55 * s; out /= max(1.0, np.abs(out).max() / 0.98)
    motion.write_wav("mix_full.wav", out)

# ---------------- frame ----------------
def frame(fr, t):
    if t >= END_SPEECH: return fr
    if T["karl"] <= t < 13.9:      # punch-in zoom
        k = 1 + 0.10 * ease((t - T["karl"]) / 0.25); vw, vh = int(W / k), int(H / k)
        y0 = int((H - vh) * 0.3); fr = fr.crop(((W - vw) // 2, y0, (W - vw) // 2 + vw, y0 + vh)).resize((W, H), Image.BILINEAR)
    for a, b, path, zin, fy in CUTS:
        if a <= t < b:
            pf = pic_frame(path, (t - a) / (b - a), zin, fy); m = min(1, (t - a) / 0.2, (b - t) / 0.2)
            fr = pf if m >= 1 else Image.blend(fr, pf, m)
    c = fr.convert("RGBA")
    for a, b, stage in CHARTS:
        if a <= t < b:
            ch = chart(t, a, stage); m = min(1, (t - a) / 0.2, (b - t) / 0.2)
            c = ch if m >= 1 else Image.blend(c, ch, m)
    for a, b, sp, y in TAGS:
        s_, a_ = pop_in(t, a, b)
        if a_ <= 0: continue
        im = hook_card(t) if sp == "hook" else sp
        if sp is TAGS[2][2]: put(c, im, W / 2 + (1 - ease((t - a) / 0.35)) * -700, y, 1, a_)
        else: put(c, im, W / 2, y, s_, a_)
    if 7.3 <= t < 11.8:
        s_, a_ = pop_in(t, 7.3, 11.6); put(c, counter(t, 7.3), W / 2, 1210, s_, a_)
    for a, b, sp in STAMPS:
        if a <= t < b + 0.25:
            s_, a_ = pop_in(t, a, b, 0.22); sh = max(0, a + 0.35 - t) * 40
            dx, dy = int(np.sin(t * 90) * sh), int(np.cos(t * 70) * sh)
            put(c, sp, W / 2 + dx, (1230 if sp is STAMPS[0][2] else 1330) + dy, s_ * (1.4 - 0.4 * min(1, (t - a) / 0.2)), a_, rot=6)
    cap, cs = caption(t)
    if cap: put(c, cap, W / 2, CAP_Y, cs)
    return c.convert("RGB")

prev = os.environ.get("PREVIEW")
if prev:
    for ts in prev.split(","):
        t = float(ts); r = subprocess.run(["ffmpeg", "-v", "error", "-ss", ts, "-i", SRC, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
        frame(Image.frombuffer("RGB", (W, H), r), t).resize((360, 640)).save(f"pv_{ts}.jpg")
    sys.exit()

audio()
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", SRC, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", "mix_full.wav",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", "jensen_reel.mp4"], stdin=subprocess.PIPE)
i = 0
while True:
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    enc.stdin.write(frame(Image.frombuffer("RGB", (W, H), buf), i / FPS).tobytes()); i += 1
enc.stdin.close(); enc.wait(); dec.wait()
print("done", i, "frames")
