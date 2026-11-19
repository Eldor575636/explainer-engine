"""Eldor Explains logo v2 (owner pick 2026-11-19: concept 1, green answer bubble with a rising gold chart).
mark(size, bars=(1,1,1), arrow=1.0) -> RGBA. Progress values 0..1 are used by the animated sting.
Run: python3 logo_v2.py  -> writes the static set into ./v2/"""
import math, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, '..', '..', '..', 'fonts')
PAPER, INK, GREEN, GREEN_D, GOLD = '#F7F5F0', '#111418', '#0F7B5A', '#0A5C43', '#E3B341'
ARCH = os.path.join(FONTS, 'ArchivoBlack-Regular.ttf')
INTER = os.path.join(FONTS, 'Inter-SemiBold.ttf')
S = 4  # supersample


def _bubble(d, W, col):
    # body + tail, geometry in units of W
    d.rounded_rectangle([W * 0.06, W * 0.10, W * 0.94, W * 0.76], radius=W * 0.17, fill=col)
    d.polygon([(W * 0.20, W * 0.66), (W * 0.15, W * 0.93), (W * 0.42, W * 0.74)], fill=col)


def mark(size, bars=(1, 1, 1), arrow=1.0, shadow=True):
    W = size * S
    im = Image.new('RGBA', (W, W), (0, 0, 0, 0))
    if shadow:
        sh = Image.new('L', (W, W), 0)
        sd = ImageDraw.Draw(sh)
        _bubble(sd, W, 255)
        sh = sh.transform(sh.size, Image.AFFINE, (1, 0, 0, 0, 1, -W * 0.025)).filter(ImageFilter.GaussianBlur(W * 0.025))
        im.paste(Image.new('RGBA', (W, W), (0, 0, 0, 110)), (0, 0), sh)
    d = ImageDraw.Draw(im)
    _bubble(d, W, GREEN)
    # three rising bars
    base = W * 0.62
    bw = W * 0.13
    xs = [W * 0.24, W * 0.43, W * 0.62]
    hs = [W * 0.13, W * 0.22, W * 0.32]
    for x, h, p in zip(xs, hs, bars):
        p = max(0.0, min(1.0, p))
        if p > 0:
            d.rounded_rectangle([x, base - h * p, x + bw, base], radius=W * 0.018, fill=GOLD)
    # rising arrow over the bars: quadratic curve + head, drawn up to `arrow`
    if arrow > 0:
        P0, P1, P2 = (W * 0.22, W * 0.40), (W * 0.48, W * 0.36), (W * 0.74, W * 0.21)
        n = 60
        k = max(2, int(n * min(1.0, arrow)))
        pts = []
        for i in range(k + 1):
            t = i / n
            x = (1 - t) ** 2 * P0[0] + 2 * (1 - t) * t * P1[0] + t ** 2 * P2[0]
            y = (1 - t) ** 2 * P0[1] + 2 * (1 - t) * t * P1[1] + t ** 2 * P2[1]
            pts.append((x, y))
        lw = W * 0.045
        d.line(pts, fill=GOLD, width=int(lw), joint='curve')
        r = lw / 2
        d.ellipse([pts[0][0] - r, pts[0][1] - r, pts[0][0] + r, pts[0][1] + r], fill=GOLD)
        if arrow >= 0.98:
            ax, ay = pts[-1]
            ang = math.atan2(pts[-1][1] - pts[-3][1], pts[-1][0] - pts[-3][0])
            L = W * 0.12
            tip = (ax + L * 0.55 * math.cos(ang), ay + L * 0.55 * math.sin(ang))
            l = (ax + L * 0.6 * math.cos(ang + 2.3), ay + L * 0.6 * math.sin(ang + 2.3))
            rr = (ax + L * 0.6 * math.cos(ang - 2.3), ay + L * 0.6 * math.sin(ang - 2.3))
            d.polygon([tip, l, rr], fill=GOLD)
    return im.resize((size, size), Image.LANCZOS)


def ground(size, dark=True):
    """Bilmasboy-style textured ground: ink with a faint ledger grid (or paper)."""
    col, line = (INK, '#1D2622') if dark else (PAPER, '#E2E8E1')
    W = size * S
    im = Image.new('RGB', (W, W), col)
    d = ImageDraw.Draw(im)
    step = W / 14
    for i in range(15):
        d.line([i * step, 0, i * step, W], fill=line, width=S * 2)
        d.line([0, i * step, W, i * step], fill=line, width=S * 2)
    return im.resize((size, size), Image.LANCZOS)


def avatar(size=1024, dark=True):
    im = ground(size, dark).convert('RGBA')
    m = mark(int(size * 0.74))
    o = (size - m.size[0]) // 2
    im.alpha_composite(m, (o, o + int(size * 0.03)))
    return im.convert('RGB')


def wordmark(h, ink=INK, accent=GREEN, bg=None):
    f = ImageFont.truetype(ARCH, int(h * 0.50))
    tmp = ImageDraw.Draw(Image.new('RGB', (10, 10)))
    w1, w2 = tmp.textlength('Eldor ', font=f), tmp.textlength('Explains', font=f)
    ms = int(h * 1.0)
    W = int(ms + h * 0.22 + w1 + w2 + h * 0.15)
    im = Image.new('RGBA', (W, h), (0, 0, 0, 0) if bg is None else bg)
    im.alpha_composite(mark(ms), (0, 0))
    d = ImageDraw.Draw(im)
    x = ms + h * 0.22
    bb = d.textbbox((0, 0), 'Eldor', font=f)
    y = h * 0.44 - (bb[1] + bb[3]) / 2
    d.text((x, y), 'Eldor ', font=f, fill=ink)
    d.text((x + w1, y), 'Explains', font=f, fill=accent)
    return im


def banner(slogan='Money, explained with real numbers.'):
    W, H = 2560, 1440
    g = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(g)
    for x in range(0, W, 80):
        d.line([x, 0, x, H], fill='#E4E9E2', width=2)
    for y in range(0, H, 80):
        d.line([0, y, W, y], fill='#E4E9E2', width=2)
    g = g.convert('RGBA')
    wm = wordmark(300)
    g.alpha_composite(wm, ((W - wm.size[0]) // 2, H // 2 - wm.size[1] // 2 - 55))
    d = ImageDraw.Draw(g)
    f = ImageFont.truetype(INTER, 54)
    tw = d.textlength(slogan, font=f)
    d.text(((W - tw) / 2, H // 2 + wm.size[1] // 2 - 15), slogan, font=f, fill='#3A4047')
    return g.convert('RGB')


if __name__ == '__main__':
    out = os.path.join(HERE, 'v2')
    os.makedirs(out, exist_ok=True)
    mark(1024).save(os.path.join(out, 'EE_mark_transparent.png'))
    mark(150, shadow=False).save(os.path.join(out, 'EE_watermark_150.png'))
    avatar(1024, True).save(os.path.join(out, 'EE_avatar_dark_1024.png'))
    avatar(1024, False).save(os.path.join(out, 'EE_avatar_light_1024.png'))
    wordmark(300).save(os.path.join(out, 'EE_wordmark_light.png'))
    wordmark(300, ink=PAPER, accent='#3FB58A').save(os.path.join(out, 'EE_wordmark_dark.png'))
    banner().save(os.path.join(out, 'EE_youtube_banner_2560x1440.png'))
    print('ok')
