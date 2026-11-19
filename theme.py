"""Channel theme. CHANNEL=ee (env) switches the whole engine to Eldor Explains: Ledger palette, its fonts, English
UI strings, no new-alphabet conversion, English transcription. Default = Bilmasboy (unchanged).
The colour names are kept (NAVY = main dark, MUSTARD = label fill, RED = accent, CREAM = paper) so the
renderer code needs no changes; in Eldor Explains they map to ink / gold / money green / paper."""
import os
from pathlib import Path

CHANNEL = os.environ.get("CHANNEL", "bilmasboy").lower()
EN = CHANNEL in ("ee", "en", "eldor", "eldorexplains")
FONTS = Path(__file__).parent / "fonts"
ASSETS = Path(__file__).parent / "assets"

if EN:
    NAVY = (17, 20, 24)            # ink
    MUSTARD = (227, 179, 65)       # gold (fills only)
    RED = (15, 123, 90)            # money green: circles, arrows, stamps, highlights
    CREAM = (247, 245, 240)        # paper
    INK = (17, 20, 24)
    LOSS = (214, 69, 69)           # only for losses / falling bars
    ANTON = str(FONTS / "Outfit-Black.ttf")        # labels, tags, stamps, big numbers
    MONT = str(FONTS / "Inter-ExtraBold.ttf")      # captions, small tags
    TITLE = str(FONTS / "Fraunces-Black.ttf")      # chapter and title cards
    AVATAR = Path(__file__).parent / "brand" / "eldor-explains" / "logo" / "v2" / "EE_avatar_dark_1024.png"
    HANDLE = "@EldorExplains"
    LANG = "en"
else:
    NAVY = (27, 42, 74); MUSTARD = (212, 162, 58); RED = (200, 16, 46); CREAM = (244, 238, 223)
    INK = (14, 22, 38)
    LOSS = RED
    ANTON = str(FONTS / "Anton-Regular.ttf"); MONT = str(FONTS / "Montserrat-ExtraBold.ttf")
    TITLE = ANTON
    AVATAR = ASSETS / "brand" / "avatar.png"
    HANDLE = "@bilmasboy"
    LANG = "uz"

# On-screen UI strings (cfg "ui" in a beat sheet still overrides the ones it names)
_UI = {
    "full_video": ("TO'LIQ VIDEO KANALDA", "FULL VIDEO ON THE CHANNEL"),
    "clip_from": ("BU LAVHA: {mm:02d}:{ss:02d} DAN", "THIS CLIP: FROM {mm:02d}:{ss:02d}"),
    "next_head": ("KEYINGI QISMDA:", "NEXT TIME:"),
    "next": ("KEYINGI VIDEO", "WATCH NEXT"),
    "subscribe": ("OBUNA BO'LING", "SUBSCRIBE"),
    "subscribe_btn": ("OBUNA", "SUBSCRIBE"),
}


def T(key):
    uz, en = _UI[key]
    return en if EN else uz
