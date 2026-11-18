"""Eldor Explains avatar concepts v2: flat, bold, Bilmasboy-family (simple symbol on a textured ground)."""
import math, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, '..', '..', '..', 'fonts')
PAPER, INK, GREEN, GOLD, WHITE = '#F7F5F0', '#111418', '#0F7B5A', '#E3B341', '#FFFFFF'
ARCH = os.path.join(FONTS, 'ArchivoBlack-Regular.ttf')
N = 1024
S = 3
W = N * S


def ground(bg='ink'):
    col, line = (INK, '#1E2A26') if bg == 'ink' else (PAPER, '#E2E8E1')
    im = Image.new('RGB', (W, W), col)
    d = ImageDraw.Draw(im)
    step = W // 16
    for i in range(0, W + 1, step):
        d.line([i, 0, i, W], fill=line, width=S * 3)
        d.line([0, i, W, i], fill=line, width=S * 3)
    return im


def shadow(im, shape_mask, off=(0, 18 * S), blur=20 * S, alpha=110):
    sh = Image.new('L', im.size, 0)
    sh.paste(shape_mask.point(lambda v: alpha if v else 0), off)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    im.paste(Image.new('RGB', im.size, '#000000'), (0, 0), sh)


def bubble_mask(box, r, tail):
    m = Image.new('L', (W, W), 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle(box, radius=r, fill=255)
    d.polygon(tail, fill=255)
    return m


def chart_arrow(d, x0, y0, x1, y1, w, col):
    pts = [(x0, y1), (x0 + (x1 - x0) * 0.33, y0 + (y1 - y0) * 0.45), (x0 + (x1 - x0) * 0.55, y0 + (y1 - y0) * 0.68), (x1 - w * 1.2, y0 + w * 0.6)]
    d.line(pts, fill=col, width=int(w), joint='curve')
    r = w / 2
    for p in pts[:-1]:
        d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=col)
    ang = math.atan2(pts[-1][1] - pts[-2][1], pts[-1][0] - pts[-2][0])
    ax, ay = pts[-1]
    L = w * 2.6
    tip = (ax + L * 0.75 * math.cos(ang), ay + L * 0.75 * math.sin(ang))
    l = (ax + L * 0.7 * math.cos(ang + 2.25), ay + L * 0.7 * math.sin(ang + 2.25))
    rr = (ax + L * 0.7 * math.cos(ang - 2.25), ay + L * 0.7 * math.sin(ang - 2.25))
    d.polygon([tip, l, rr], fill=col)


def concept_bubble_chart(bg='ink'):
    """A: green speech bubble (the answer to Bilmasboy's red '?') with a gold rising arrow."""
    im = ground(bg)
    box = [W * 0.17, W * 0.2, W * 0.83, W * 0.72]
    tail = [(W * 0.30, W * 0.68), (W * 0.24, W * 0.84), (W * 0.45, W * 0.70)]
    m = bubble_mask(box, W * 0.09, tail)
    shadow(im, m)
    im.paste(Image.new('RGB', im.size, GREEN), (0, 0), m)
    d = ImageDraw.Draw(im)
    chart_arrow(d, W * 0.29, W * 0.31, W * 0.71, W * 0.60, W * 0.055, GOLD)
    return im.resize((N, N), Image.LANCZOS)


def concept_bubble_ee(bg='ink'):
    """B: green speech bubble with bold white EE, gold underline."""
    im = ground(bg)
    box = [W * 0.15, W * 0.2, W * 0.85, W * 0.72]
    tail = [(W * 0.30, W * 0.68), (W * 0.24, W * 0.84), (W * 0.45, W * 0.70)]
    m = bubble_mask(box, W * 0.09, tail)
    shadow(im, m)
    im.paste(Image.new('RGB', im.size, GREEN), (0, 0), m)
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(ARCH, int(W * 0.30))
    bb = d.textbbox((0, 0), 'EE', font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    x, y = W / 2 - tw / 2 - bb[0], W * 0.43 - th / 2 - bb[1]
    d.text((x, y), 'EE', font=f, fill=WHITE)
    d.rounded_rectangle([W / 2 - tw / 2, y + bb[3] + W * 0.03, W / 2 + tw / 2, y + bb[3] + W * 0.075], radius=W * 0.02, fill=GOLD)
    return im.resize((N, N), Image.LANCZOS)


def concept_coin_flat(bg='ink'):
    """C: flat gold coin, thick ink ring, single bold E with a rising tick, no gradients or ridges."""
    im = ground(bg)
    c, R = W / 2, W * 0.34
    m = Image.new('L', (W, W), 0)
    ImageDraw.Draw(m).ellipse([c - R, c - R, c + R, c + R], fill=255)
    shadow(im, m)
    d = ImageDraw.Draw(im)
    d.ellipse([c - R, c - R, c + R, c + R], fill=GOLD, outline=INK if bg == 'paper' else GOLD, width=int(W * 0.02))
    r2 = R * 0.80
    d.ellipse([c - r2, c - r2, c + r2, c + r2], outline=INK, width=int(W * 0.018))
    f = ImageFont.truetype(ARCH, int(W * 0.26))
    bb = d.textbbox((0, 0), 'EE', font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    d.text((c - tw / 2 - bb[0], c - th / 2 - bb[1]), 'EE', font=f, fill=INK)
    return im.resize((N, N), Image.LANCZOS)


def concept_face(head_png, bg='ink'):
    """D: mascot head sticker (white outline) + small green answer bubble with a gold arrow."""
    im = ground(bg)
    head = Image.open(head_png).convert('RGBA')
    hw = int(W * 0.66)
    head = head.resize((hw, int(head.height * hw / head.width)), Image.LANCZOS)
    pad = 40
    big = Image.new('RGBA', (head.width + 2 * pad, head.height + 2 * pad), (0, 0, 0, 0)); big.paste(head, (pad, pad)); head = big
    a = head.split()[3]
    outline = a.filter(ImageFilter.MaxFilter(51)).filter(ImageFilter.GaussianBlur(3))
    hx, hy = int(W * 0.05), W - head.height + int(W * 0.06)
    sh = Image.new('L', (W, W), 0)
    sh.paste(outline, (hx, hy))
    shadow(im, sh.point(lambda v: 255 if v > 128 else 0))
    im.paste(Image.new('RGB', outline.size, WHITE), (hx, hy), outline)
    im.paste(head, (hx, hy), head)
    box = [W * 0.56, W * 0.14, W * 0.84, W * 0.36]
    tail = [(W * 0.60, W * 0.33), (W * 0.55, W * 0.44), (W * 0.68, W * 0.35)]
    m = bubble_mask(box, W * 0.05, tail)
    im.paste(Image.new('RGB', im.size, GREEN), (0, 0), m)
    d = ImageDraw.Draw(im)
    chart_arrow(d, W * 0.61, W * 0.185, W * 0.80, W * 0.31, W * 0.028, GOLD)
    return im.resize((N, N), Image.LANCZOS)


if __name__ == '__main__':
    head = sys.argv[1]
    out = os.path.join(HERE, 'concepts')
    os.makedirs(out, exist_ok=True)
    tiles = []
    for name, fn in [('A_bubble_chart', concept_bubble_chart), ('B_bubble_EE', concept_bubble_ee), ('C_coin_flat', concept_coin_flat)]:
        for bg in ('ink', 'paper'):
            im = fn(bg); im.save(os.path.join(out, f'{name}_{bg}.png')); tiles.append(im)
    for bg in ('ink', 'paper'):
        im = concept_face(head, bg); im.save(os.path.join(out, f'D_face_{bg}.png')); tiles.append(im)
    print('ok')
