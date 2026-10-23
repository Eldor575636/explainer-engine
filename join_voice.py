#!/usr/bin/env python3
"""Join voiceover pieces recorded one paragraph per file into one raw.wav.

Usage: python3 join_voice.py <out.wav> part01.m4a part02.m4a ...
Files are joined in the order given (name them 01, 02, ... so a shell glob sorts them).
Each piece is levelled on its own first, so takes recorded at different distances match,
and 0.6 s of silence goes between pieces (v3.py trims it to a breath anyway).
"""
import subprocess, sys

out, parts = sys.argv[1], sys.argv[2:]
if not parts:
    sys.exit(__doc__)
inputs, chain = [], ""
for i, p in enumerate(parts):
    inputs += ["-i", p]
    chain += f"[{i}:a]aformat=sample_rates=48000:channel_layouts=mono,loudnorm=I=-18:TP=-2,aresample=48000[p{i}];"
gap = "anullsrc=r=48000:cl=mono,atrim=0:0.6"
seq = ""
for i in range(len(parts)):
    if i:
        chain += f"{gap}[g{i}];"; seq += f"[g{i}]"
    seq += f"[p{i}]"
fc = chain + seq + f"concat=n={seq.count('[')}:v=0:a=1[a]"
subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", fc, "-map", "[a]", "-ar", "48000", out], check=True)
print(f"Joined {len(parts)} pieces -> {out}")
