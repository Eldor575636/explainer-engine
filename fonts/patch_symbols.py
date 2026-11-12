"""Copy symbols our fonts lack (arrows, check/cross marks...) from DejaVu Sans Bold into Anton and Montserrat,
scaled to each font's units-per-em, so tags/labels/stamps/captions can draw them. Run once; rewrites the .ttf files
(originals kept as *.orig.ttf)."""
import shutil, os
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
SRC = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
CHARS = "→←↑↓✓✗✔✘×≈•★"
here = os.path.dirname(os.path.abspath(__file__))
src = TTFont(SRC); scmap = src.getBestCmap(); sgs = src.getGlyphSet(); supm = src["head"].unitsPerEm
for name in ("Anton-Regular.ttf", "Montserrat-ExtraBold.ttf"):
    path = os.path.join(here, name); orig = path.replace(".ttf", ".orig.ttf")
    if not os.path.exists(orig):
        shutil.copy(path, orig)
    f = TTFont(orig); cmap = f.getBestCmap(); upm = f["head"].unitsPerEm
    capH = getattr(f["OS/2"], "sCapHeight", 0) or upm * 0.7
    s = upm / supm * (capH / (upm * 0.7)) ** 0.5          # roughly match the cap height of the target font
    glyf, hmtx, order = f["glyf"], f["hmtx"], f.getGlyphOrder()
    added = []
    for ch in CHARS:
        cp = ord(ch)
        if cp in cmap or cp not in scmap:
            continue
        gname = f"uni{cp:04X}"
        pen = TTGlyphPen(None)
        sgs[scmap[cp]].draw(TransformPen(pen, (s, 0, 0, s, 0, 0)))
        glyf[gname] = pen.glyph()
        adv = int(src["hmtx"][scmap[cp]][0] * s)
        hmtx[gname] = (adv, glyf[gname].xMin if hasattr(glyf[gname], "xMin") else 0)
        if gname not in order: order.append(gname)
        added.append(ch)
        for t in f["cmap"].tables:
            if t.isUnicode():
                t.cmap[cp] = gname
    glyf.glyphOrder = order
    f.setGlyphOrder(order)
    f["maxp"].numGlyphs = len(order)
    f.save(path)
    print(name, "added", "".join(added))
