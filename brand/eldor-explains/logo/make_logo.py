"""Eldor Explains logo set (Ledger kit). Draws at 4x and downsamples.
Outputs: coin.png (transparent), avatar.png (coin on green, 1024), wordmark.png (paper), wordmark_dark.png (ink), banner.png (2560x1440)."""
import math, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, '..', '..', '..', 'fonts')
PAPER, INK, GREEN, GOLD, GOLD_D, GOLD_L = '#F7F5F0', '#111418', '#0F7B5A', '#E3B341', '#B8892A', '#F3D27A'
ARCH = os.path.join(FONTS, 'ArchivoBlack-Regular.ttf')
INTER = os.path.join(FONTS, 'Inter-SemiBold.ttf')
S = 4


def font(path, px):
    return ImageFont.truetype(path, int(px))


def coin(size):
    """Gold coin with ink rim, reeded edge, inner ring and EE monogram. Returns RGBA of size x size."""
    W = size * S
    im = Image.new('RGBA', (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = W / 2
    R = W * 0.48
    rim = W * 0.035
    d.ellipse([c - R, c - R, c + R, c + R], fill=INK)
    r1 = R - rim
    d.ellipse([c - r1, c - r1, c + r1, c + r1], fill=GOLD_D)
    # reeded edge ticks
    r_out, r_in = r1, r1 - W * 0.05
    for i in range(120):
        a = 2 * math.pi * i / 120
        x1, y1 = c + r_out * math.cos(a), c + r_out * math.sin(a)
        x2, y2 = c + r_in * math.cos(a), c + r_in * math.sin(a)
        d.line([x1, y1, x2, y2], fill=GOLD, width=int(W * 0.007))
    r2 = r_in
    d.ellipse([c - r2, c - r2, c + r2, c + r2], fill=INK)
    r3 = r2 - W * 0.012
    d.ellipse([c - r3, c - r3, c + r3, c + r3], fill=GOLD)
    # soft highlight (top-left)
    hl = Image.new('L', (W, W), 0)
    hd = ImageDraw.Draw(hl)
    hd.ellipse([c - r3 * 0.95, c - r3 * 0.95, c + r3 * 0.35, c + r3 * 0.35], fill=70)
    hl = hl.filter(ImageFilter.GaussianBlur(W * 0.06))
    mask = Image.new('L', (W, W), 0)
    ImageDraw.Draw(mask).ellipse([c - r3, c - r3, c + r3, c + r3], fill=255)
    from PIL import ImageChops
    hl = ImageChops.multiply(hl, mask)
    im.paste(Image.new('RGBA', (W, W), GOLD_L), (0, 0), hl)
    # inner dotted ring
    r4 = r3 * 0.86
    for i in range(72):
        a = 2 * math.pi * i / 72
        x, y = c + r4 * math.cos(a), c + r4 * math.sin(a)
        rr = W * 0.006
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=INK)
    # monogram
    f = font(ARCH, W * 0.40)
    txt = 'EE'
    bb = d.textbbox((0, 0), txt, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    tx, ty = c - tw / 2 - bb[0], c - th / 2 - bb[1] - W * 0.035
    d.text((tx, ty), txt, font=f, fill=INK)
    # rising line under the monogram
    y0 = c + th / 2 + W * 0.02
    pts = [(c - tw * 0.46, y0 + W * 0.055), (c - tw * 0.16, y0 + W * 0.03), (c + tw * 0.04, y0 + W * 0.042), (c + tw * 0.36, y0 - W * 0.005)]
    lw = int(W * 0.03)
    d.line(pts, fill=GREEN, width=lw, joint='curve')
    rr = W * 0.015
    d.ellipse([pts[0][0] - rr, pts[0][1] - rr, pts[0][0] + rr, pts[0][1] + rr], fill=GREEN)
    # arrow head pointing up-right
    ax, ay = pts[-1]
    ang = math.atan2(pts[-1][1] - pts[-2][1], pts[-1][0] - pts[-2][0])
    L = W * 0.075
    tip = (ax + L * 0.6 * math.cos(ang), ay + L * 0.6 * math.sin(ang))
    left = (ax + L * 0.55 * math.cos(ang + 2.4), ay + L * 0.55 * math.sin(ang + 2.4))
    right = (ax + L * 0.55 * math.cos(ang - 2.4), ay + L * 0.55 * math.sin(ang - 2.4))
    d.polygon([tip, left, right], fill=GREEN)
    return im.resize((size, size), Image.LANCZOS)


def wordmark(h, bg, ink, accent):
    """Coin + 'Eldor Explains' + chart line. Height h; returns RGB."""
    H = h * S
    f = font(ARCH, H * 0.42)
    tmp = ImageDraw.Draw(Image.new('RGB', (10, 10)))
    w1 = tmp.textlength('Eldor ', font=f)
    w2 = tmp.textlength('Explains', font=f)
    cs = int(H * 0.78)
    pad = H * 0.16
    W = int(pad + cs + H * 0.16 + w1 + w2 + pad)
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)) if bg is None else Image.new('RGB', (W, H), bg)
    c = coin(cs // S * S)
    c = c.resize((cs, cs), Image.LANCZOS)
    im.paste(c, (int(pad), int((H - cs) / 2)), c)
    d = ImageDraw.Draw(im)
    x = pad + cs + H * 0.16
    bb = d.textbbox((0, 0), 'Eldor', font=f)
    y = H * 0.47 - (bb[3] + bb[1]) / 2
    d.text((x, y), 'Eldor ', font=f, fill=ink)
    d.text((x + w1, y), 'Explains', font=f, fill=accent)
    bbp = d.textbbox((x + w1, y), 'Explains', font=f)
    base = bbp[3] + H * 0.05
    L = w1 + w2
    pts = [(x, base + H * 0.06), (x + L * 0.22, base + H * 0.02), (x + L * 0.40, base + H * 0.045), (x + L * 0.62, base - H * 0.005), (x + L * 0.80, base + H * 0.015), (x + L * 0.97, base - H * 0.04)]
    d.line(pts, fill=accent, width=int(H * 0.035), joint='curve')
    rr = H * 0.03
    ex, ey = pts[-1]
    d.ellipse([ex - rr, ey - rr, ex + rr, ey + rr], fill=GOLD, outline=ink, width=int(H * 0.008))
    return im.resize((W // S, h), Image.LANCZOS)


def avatar(size=1024):
    im = Image.new('RGB', (size, size), GREEN)
    c = coin(int(size * 0.86))
    o = (size - c.size[0]) // 2
    im.paste(c, (o, o), c)
    return im


def banner():
    W, H = 2560, 1440
    im = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(im)
    # faint ledger grid
    for x in range(0, W, 80):
        d.line([x, 0, x, H], fill='#E4E9E2', width=2)
    for y in range(0, H, 80):
        d.line([0, y, W, y], fill='#E4E9E2', width=2)
    # safe area 1546x423 centred
    wm = wordmark(300, None, INK, GREEN)
    wm = wm.resize((1320, int(wm.size[1] * 1320 / wm.size[0])), Image.LANCZOS)
    im.paste(wm, ((W - wm.size[0]) // 2, H // 2 - wm.size[1] // 2 - 50), wm)
    f = font(INTER, 50)
    t = 'Money, explained with real numbers.  New video every week.'
    tw = d.textlength(t, font=f)
    d.text(((W - tw) / 2, H // 2 + wm.size[1] // 2 - 20), t, font=f, fill='#3A4047')
    return im


if __name__ == '__main__':
    out = HERE
    coin(1024).save(os.path.join(out, 'coin.png'))
    coin(150).save(os.path.join(out, 'watermark_150.png'))
    avatar().save(os.path.join(out, 'avatar.png'))
    wordmark(300, PAPER, INK, GREEN).save(os.path.join(out, 'wordmark.png'))
    wordmark(300, None, INK, GREEN).save(os.path.join(out, 'wordmark_transparent.png'))
    wordmark(300, INK, PAPER, '#3FB58A').save(os.path.join(out, 'wordmark_dark.png'))
    banner().save(os.path.join(out, 'banner.png'))
    print('ok')
