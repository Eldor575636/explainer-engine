"""Eldor Explains platform covers: YouTube banner, Facebook cover, X header, a 'find me everywhere' card, avatars.
Same handle everywhere: @EldorExplains. python3 make_covers.py -> ./covers/"""
import io, os, re
import cairosvg
from PIL import Image, ImageDraw, ImageFont
import logo_v2 as L

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SVG = os.path.join(ROOT, 'assets', 'brand', 'platforms', 'svg')
CHAR = os.path.join(ROOT, 'brand', 'eldor-explains', 'char', 'A_analyst_cut.png')
OUT = os.path.join(HERE, 'covers')
HANDLE = '@EldorExplains'
SLOGAN = 'Money, explained with real numbers.'
PLATFORMS = ['youtube', 'tiktok', 'instagram', 'facebook', 'telegram']
OUTFIT = L.HEADLINE_FONT
INTER = L.INTER


def icon(name, px, col):
    svg = open(os.path.join(SVG, name + '.svg')).read()
    svg = re.sub(r'<svg ', f'<svg fill="{col}" ', svg, count=1)
    png = cairosvg.svg2png(bytestring=svg.encode(), output_width=px, output_height=px)
    return Image.open(io.BytesIO(png)).convert('RGBA')


def chip(name, px, dark=False):
    """Platform icon in a filled circle."""
    S = 4
    c = Image.new('RGBA', (px * S, px * S), (0, 0, 0, 0))
    ImageDraw.Draw(c).ellipse([0, 0, px * S - 1, px * S - 1], fill=L.PAPER if dark else L.INK)
    c = c.resize((px, px), Image.LANCZOS)
    ic = icon(name, int(px * 0.54), L.INK if dark else L.PAPER)
    c.alpha_composite(ic, ((px - ic.width) // 2, (px - ic.height) // 2))
    return c


def grid(W, H, step=60, dark=False):
    col, line = (L.INK, '#1D2622') if dark else (L.PAPER, '#E4E9E2')
    im = Image.new('RGB', (W, H), col)
    d = ImageDraw.Draw(im)
    for x in range(0, W, step): d.line([x, 0, x, H], fill=line, width=2)
    for y in range(0, H, step): d.line([0, y, W, y], fill=line, width=2)
    return im.convert('RGBA')


def handle_row(h, platforms=PLATFORMS, dark=False):
    """[icons] @EldorExplains  as one RGBA strip of height h."""
    f = ImageFont.truetype(OUTFIT, int(h * 0.62))
    tw = ImageDraw.Draw(Image.new('RGB', (1, 1))).textlength(HANDLE, font=f)
    gap = int(h * 0.18)
    W = int(len(platforms) * (h + gap) + gap * 1.5 + tw)
    im = Image.new('RGBA', (W, h), (0, 0, 0, 0))
    x = 0
    for p in platforms:
        im.alpha_composite(chip(p, h, dark), (x, 0)); x += h + gap
    d = ImageDraw.Draw(im)
    bb = d.textbbox((0, 0), HANDLE, font=f)
    d.text((x + gap * 0.5, (h - (bb[1] + bb[3])) / 2), HANDLE, font=f, fill=L.PAPER if dark else L.INK)
    return im


def character(h):
    c = Image.open(CHAR).convert('RGBA')
    return c.resize((int(c.width * h / c.height), h), Image.LANCZOS)


def fit(im, w):
    return im if im.width <= w else im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)


def compose(W, H, safe, wm_h, row_h, char_h=None, char_dx=0, char_dy=0, slogan_px=None, dark=False, char_top=None):
    """safe = (x0, y0, x1, y1): everything readable sits inside it; the character may bleed beyond."""
    im = grid(W, H, dark=dark)
    x0, y0, x1, y1 = safe
    sw = x1 - x0
    wm = L.wordmark(wm_h, ink=L.PAPER if dark else L.INK, accent='#3FB58A' if dark else L.GREEN)
    row = handle_row(row_h, dark=dark)
    text_w = int(sw * (0.66 if char_h else 1.0))
    wm, row = fit(wm, text_w), fit(row, text_w)
    f = ImageFont.truetype(INTER, slogan_px or int(wm.height * 0.2))
    d = ImageDraw.Draw(im)
    sl_h = int(f.size * 1.3)
    gap = int(wm.height * 0.18)
    block_h = wm.height + gap + sl_h + gap * 1.4 + row.height
    by = int(y0 + ((y1 - y0) - block_h) // 2)
    bx = x0 if char_h else x0 + (sw - max(wm.width, row.width)) // 2
    if char_h:
        ch = character(char_h)
        cx = x1 - ch.width + char_dx
        cy = char_top if char_top is not None else H - ch.height + char_dy
        im.alpha_composite(ch, (cx, cy))
    im.alpha_composite(wm, (bx, by))
    d.text((bx + int(wm.height * 1.22), by + wm.height + gap), SLOGAN, font=f, fill='#B9C2BE' if dark else '#3A4047')
    im.alpha_composite(row, (bx + int(wm.height * 0.05), int(by + wm.height + gap + sl_h + gap * 1.4)))
    return im.convert('RGB')


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    # YouTube: 2560x1440, safe area 1546x423 centred; character stands at the right of the safe area
    W, H = 2560, 1440
    sx0, sy0 = (W - 1546) // 2, (H - 423) // 2
    yt = compose(W, H, (sx0, sy0, sx0 + 1546, sy0 + 423), wm_h=200, row_h=74, char_h=1000, char_dx=200, char_top=sy0 + 18)
    yt.save(os.path.join(OUT, 'YouTube_banner_2560x1440.jpg'), quality=94)
    # Facebook Page cover: 1640x624 (desktop 820x312 @2x); phones crop the sides, so keep the middle 1230 px
    fb = compose(1640, 624, (205 + 30, 70, 1435 - 10, 560), wm_h=150, row_h=60, char_h=720, char_dx=40, char_dy=300)
    fb.save(os.path.join(OUT, 'Facebook_cover_1640x624.jpg'), quality=94)
    # X header: 1500x500; the profile photo covers the bottom-left, so content sits right of x=420
    xh = compose(1500, 500, (430, 40, 1460, 460), wm_h=120, row_h=50, char_h=600, char_dx=20, char_dy=330)
    xh.save(os.path.join(OUT, 'X_header_1500x500.jpg'), quality=94)
    # Find-me-everywhere card (posts, Stories, Telegram pin): 1080x1350
    card = grid(1080, 1350).copy()
    ch = character(900)
    card.alpha_composite(ch, (1080 - ch.width + 30, 1350 - ch.height + 40))
    wm = fit(L.wordmark(120), 960)
    card.alpha_composite(wm, ((1080 - wm.width) // 2, 70))
    d = ImageDraw.Draw(card)
    f = ImageFont.truetype(INTER, 34)
    tw = d.textlength(SLOGAN, font=f); d.text(((1080 - tw) / 2, 70 + wm.height + 18), SLOGAN, font=f, fill='#3A4047')
    y = 330
    fo = ImageFont.truetype(OUTFIT, 46)
    for p in PLATFORMS:
        d.rounded_rectangle([60, y, 560, y + 92], radius=46, fill='#FFFFFF', outline=L.INK, width=4)
        card.alpha_composite(chip(p, 72), (72, y + 10))
        d.text((164, y + 18), HANDLE, font=fo, fill=L.INK)
        y += 116
    card.convert('RGB').save(os.path.join(OUT, 'Find_me_everywhere_1080x1350.jpg'), quality=94)
    # Avatars: one image for every platform (all crop to a circle)
    av = L.avatar(1024, True)
    av.save(os.path.join(OUT, 'Avatar_all_platforms_1024.png'))
    av.resize((400, 400), Image.LANCZOS).save(os.path.join(OUT, 'Avatar_400.png'))
    print('ok')
