"""Per-platform brand kits for Eldor Explains (@EldorExplains everywhere), each sized to that platform's
upload size and safe zones. python3 make_platforms.py -> ./platforms/<Platform>/ (files + README.txt)"""
import os
from PIL import Image, ImageDraw, ImageFont
import logo_v2 as L
import make_covers as C

OUT = os.path.join(C.HERE, 'platforms')


def save(img, plat, name, q=94):
    d = os.path.join(OUT, plat); os.makedirs(d, exist_ok=True)
    p = os.path.join(d, name)
    (img.convert('RGB').save(p, quality=q) if name.endswith('.jpg') else img.save(p))


def avatar(px):
    return L.avatar(1024, True).resize((px, px), Image.LANCZOS)


def card(W, H, top, bottom):
    """Find-me card: wordmark + slogan at the top, character bottom-left, handle pills on the right.
    top/bottom = pixels kept clear for the app's own buttons (Stories)."""
    im = C.grid(W, H).copy()
    d = ImageDraw.Draw(im)
    wm = C.fit(L.wordmark(120), W - 120)
    im.alpha_composite(wm, ((W - wm.width) // 2, top + 40))
    f = ImageFont.truetype(C.INTER, 34)
    tw = d.textlength(C.SLOGAN, font=f)
    d.text(((W - tw) / 2, top + 40 + wm.height + 18), C.SLOGAN, font=f, fill='#3A4047')
    avail = H - bottom - (top + 40 + wm.height + 90)
    ch = C.character(int(min(1150, avail)))
    im.alpha_composite(ch, (-40, H - bottom - ch.height + 40))
    fo = ImageFont.truetype(C.OUTFIT, 46)
    y = top + 40 + wm.height + 90 + max(0, (avail - 5 * 116) // 2)
    for p in C.PLATFORMS:
        d.rounded_rectangle([520, y, 1020, y + 92], radius=46, fill='#FFFFFF', outline=L.INK, width=4)
        im.alpha_composite(C.chip(p, 72), (532, y + 10))
        d.text((624, y + 18), C.HANDLE, font=fo, fill=L.INK)
        y += 116
    return im


README = {
'YouTube': """YouTube (@EldorExplains)
- YouTube_avatar_800.png: profile picture (YouTube shows it as a circle; 800x800 recommended).
- YouTube_banner_2560x1440.jpg: channel banner. Phones show only the middle 1546x423; logo, handle and face sit inside it.
- YouTube_watermark_150.png: Settings > Channel > Branding > Video watermark (transparent, shown bottom-right of every video).
Upload: YouTube Studio > Customisation > Branding.""",
'Facebook': """Facebook Page (@EldorExplains)
- Facebook_avatar_720.png: Page profile picture (shown as a circle).
- Facebook_cover_1640x624.jpg: Page cover (desktop shows it at 820x312, phones crop to the middle; everything readable is
  centred in the middle 1060 px and the bottom-left is kept clear because the profile photo can overlap it). No character here.""",
'Instagram': """Instagram (@EldorExplains)
- Instagram_avatar_1080.png: profile picture (shown as a small circle).
- Instagram_post_find_me_1080x1350.jpg: first/pinned post (4:5 portrait).
- Instagram_story_find_me_1080x1920.jpg: Story / highlight (top 250 px and bottom 340 px kept clear for Instagram's buttons).
- Instagram_highlight_cover_1080.png: highlight cover (the bubble mark, centred for the circle crop).""",
'TikTok': """TikTok (@EldorExplains)
- TikTok_avatar_1080.png: profile picture (TikTok has no cover image).""",
'Telegram': """Telegram channel (@EldorExplains)
- Telegram_avatar_640.png: channel photo (Telegram stores 640x640, shown as a circle).
- Telegram_pin_find_me_1080x1350.jpg: first post to pin in the channel.""",
'X': """X (@EldorExplains, claim it if not done yet)
- X_avatar_400.png: profile picture (400x400, circle).
- X_header_1500x500.jpg: header. The profile photo covers the bottom-left and phones trim the top and bottom, so the logo
  and handle sit right of centre in the middle band. No character (he would be hidden by the photo).""",
}

if __name__ == '__main__':
    # YouTube
    save(avatar(800), 'YouTube', 'YouTube_avatar_800.png')
    W, H = 2560, 1440
    sx0, sy0 = (W - 1546) // 2, (H - 423) // 2
    save(C.compose(W, H, (sx0, sy0, sx0 + 1546, sy0 + 423), wm_h=200, row_h=74, char_h=1000, char_dx=60, char_top=sy0 + 18),
         'YouTube', 'YouTube_banner_2560x1440.jpg')
    save(L.mark(150, shadow=False), 'YouTube', 'YouTube_watermark_150.png')
    # Facebook: no character; readable content in the middle 1060 px, a little above centre
    save(avatar(720), 'Facebook', 'Facebook_avatar_720.png')
    save(C.compose(1640, 624, (290, 50, 1350, 520), wm_h=150, row_h=60), 'Facebook', 'Facebook_cover_1640x624.jpg')
    # Instagram
    save(avatar(1080), 'Instagram', 'Instagram_avatar_1080.png')
    save(card(1080, 1350, 30, 40), 'Instagram', 'Instagram_post_find_me_1080x1350.jpg')
    save(card(1080, 1920, 250, 340), 'Instagram', 'Instagram_story_find_me_1080x1920.jpg')
    hl = Image.new('RGBA', (1080, 1080), L.INK); m = L.mark(700)
    hl.alpha_composite(m, ((1080 - 700) // 2, (1080 - 700) // 2 + 20)); save(hl, 'Instagram', 'Instagram_highlight_cover_1080.png')
    # TikTok
    save(avatar(1080), 'TikTok', 'TikTok_avatar_1080.png')
    # Telegram
    save(avatar(640), 'Telegram', 'Telegram_avatar_640.png')
    save(card(1080, 1350, 30, 40), 'Telegram', 'Telegram_pin_find_me_1080x1350.jpg')
    # X
    save(avatar(400), 'X', 'X_avatar_400.png')
    save(C.compose(1500, 500, (430, 70, 1460, 430), wm_h=110, row_h=46), 'X', 'X_header_1500x500.jpg')
    for plat, txt in README.items():
        open(os.path.join(OUT, plat, 'README.txt'), 'w').write(txt + '\n')
    print('ok')
