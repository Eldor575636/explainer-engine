"""Eldor Explains 2.5 s logo sting: bubble pops, bars rise, arrow draws, mark slides left, name wipes in.
python3 sting.py out.mp4 [--dark]"""
import os, sys, subprocess, tempfile
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
import logo_v2 as L
import v3, fx

W, H, FPS, DUR = 1920, 1080, 30, 2.6
N = int(FPS * DUR)
DARK = '--dark' in sys.argv
out_path = [a for a in sys.argv[1:] if not a.startswith('--')][0]


def ease(x):
    x = min(1.0, max(0.0, x)); return 1 - (1 - x) ** 3


def bg():
    col, line = (L.INK, '#1D2622') if DARK else (L.PAPER, '#E4E9E2')
    im = Image.new('RGB', (W, H), col); d = ImageDraw.Draw(im)
    for x in range(0, W, 60): d.line([x, 0, x, H], fill=line, width=2)
    for y in range(0, H, 60): d.line([0, y, W, y], fill=line, width=2)
    return im.convert('RGBA')


BG = bg()
MS = 300                                     # mark size at rest
word = L.wordmark(MS, ink=L.PAPER if DARK else L.INK, accent='#3FB58A' if DARK else L.GREEN)
text = word.crop((int(MS * 1.0), 0, word.size[0], word.size[1]))   # text part only
final_x = (W - word.size[0]) // 2           # where the mark sits when the name is shown
cy = (H - MS) // 2

tmp = tempfile.mkdtemp()
frames = []
for i in range(N):
    t = i / FPS
    im = BG.copy()
    s = fx.back_out(t / 0.30) if t < 0.30 else 1.0          # pop
    bars = [ease((t - 0.30 - k * 0.12) / 0.25) for k in range(3)]
    arrow = ease((t - 0.62) / 0.35)
    slide = ease((t - 1.05) / 0.35)
    wipe = ease((t - 1.20) / 0.45)
    size = max(2, int(MS * 1.25 * s - (MS * 0.25) * slide))   # big in the centre, settles to MS
    m = L.mark(size, bars=bars, arrow=arrow)
    cx_centre = (W - size) // 2
    x = int(cx_centre + (final_x - cx_centre) * slide)
    y = (H - size) // 2
    im.alpha_composite(m, (x, y))
    if wipe > 0:
        tw = int(text.size[0] * wipe)
        if tw > 0:
            im.alpha_composite(text.crop((0, 0, tw, text.size[1])), (final_x + int(MS * 1.0), cy))
    p = os.path.join(tmp, f'{i:04d}.png'); im.convert('RGB').save(p); frames.append(p)

# sound
n = int(DUR * v3.SR)
events = [(0.0, 'pop'), (0.33, 'tick'), (0.45, 'tick'), (0.57, 'tick'), (0.62, 'draw'), (1.05, 'whoosh')]
a = v3.synth_sfx(n, events)
fx.extra_sfx(a, [(0.97, 'ding', None)])
a = np.clip(a * 0.9, -1, 1).astype(np.float32)
wav = os.path.join(tmp, 'a.f32')
a.tofile(wav)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', os.path.join(tmp, '%04d.png'),
                '-f', 'f32le', '-ar', str(v3.SR), '-ac', '1', '-i', wav,
                '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '16', '-preset', 'medium',
                '-c:a', 'aac', '-b:a', '192k', '-shortest', out_path], check=True)
print(out_path)
