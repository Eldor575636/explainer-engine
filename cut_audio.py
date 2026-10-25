#!/usr/bin/env python3
"""Remove stretches (retakes, false starts) from raw.wav and shift words.json to match.

Usage: python3 cut_audio.py <work_dir> START-END [START-END ...]   (seconds on the current raw.wav)
Keeps a backup as raw_uncut.wav / words_uncut.json the first time.
"""
import json, shutil, subprocess, sys
from pathlib import Path

work = Path(sys.argv[1])
cuts = sorted(tuple(map(float, r.split("-"))) for r in sys.argv[2:])
raw, wj = work / "raw.wav", work / "words.json"
if not (work / "raw_uncut.wav").exists():
    shutil.copy(raw, work / "raw_uncut.wav"); shutil.copy(wj, work / "words_uncut.json")
words = json.load(open(wj, encoding="utf-8"))
total = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(raw)],
                             capture_output=True, text=True).stdout)
keep, cur = [], 0.0
for a, b in cuts:
    keep.append((cur, a)); cur = b
keep.append((cur, total))
fc = "".join(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[k{i}];" for i, (a, b) in enumerate(keep))
fc += "".join(f"[k{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=0:a=1[o]"
tmp = work / "raw_cut_tmp.wav"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-filter_complex", fc, "-map", "[o]", str(tmp)], check=True)
tmp.replace(raw)


def shift(t):
    removed = 0.0
    for a, b in cuts:
        if t >= b:
            removed += b - a
        elif t > a:
            return None
    return t - removed


out = []
for w, s, e in words:
    ns, ne = shift(s), shift(e)
    if ns is not None and ne is not None:
        out.append([w, round(ns, 3), round(ne, 3)])
json.dump(out, open(wj, "w", encoding="utf-8"), ensure_ascii=False)
print(f"Cut {len(cuts)} ranges ({sum(b - a for a, b in cuts):.1f}s); {len(words) - len(out)} words removed")
