#!/usr/bin/env python3
"""Pronunciation check for AI narration: transcribe each voice part back and compare it, sentence by
sentence, with the text the voice was asked to read. Low scores = words the voice probably mangled.

Usage: python3 check_voice.py <voice_chunks.json> <folder with 01.mp3, 02.mp3 ...> [threshold=0.6]
Writes <folder>/voice_check.json and prints the weakest sentences.
"""
import json, re, subprocess, sys, difflib
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
import build
from translit import to_latin
from faster_whisper import WhisperModel

chunks = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
folder = Path(sys.argv[2]); thr = float(sys.argv[3]) if len(sys.argv) > 3 else 0.6
m = WhisperModel("medium", compute_type="int8", cpu_threads=2)
norm = lambda s: re.sub(r"[^a-z' ]", "", to_latin(s).lower().replace("ʻ", "'").replace("’", "'"))
report = []
for ci, ch in enumerate(chunks):
    f = folder / f"{ci + 1:02d}.mp3"
    if not f.exists():
        continue
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
                         capture_output=True, check=True).stdout
    segs, _ = m.transcribe(np.frombuffer(raw, np.float32), language="uz", word_timestamps=True, vad_filter=True, condition_on_previous_text=False)  # no snowballing errors
    asr = [[to_latin(w.word.strip()), w.start, w.end] for s in segs for w in s.words]
    sents = [s for p in ch["text"].split("\n\n") for s in re.split(r"(?<=[.?!])\s+", p) if s.strip()]
    sw = [(w, si) for si, s in enumerate(sents) for w in s.split()]
    times, _ = build.align([w for w, _ in sw], asr)
    for si, s in enumerate(sents):
        ts = [t for (w, k), t in zip(sw, times) if k == si]
        a, b = ts[0][0] - 0.3, ts[-1][1] + 0.3
        heard = " ".join(w for w, s0, e0 in asr if s0 >= a and e0 <= b)
        score = difflib.SequenceMatcher(None, norm(s), norm(heard)).ratio()
        report.append({"part": ci + 1, "t": round(ts[0][0], 1), "score": round(score, 2), "text": s, "heard": heard})
    print(f"part {ci + 1}: {len(sents)} sentences checked", flush=True)
json.dump(report, open(folder / "voice_check.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
weak = sorted([r for r in report if r["score"] < thr], key=lambda r: r["score"])
print(f"\n{len(weak)} of {len(report)} sentences below {thr}:")
for r in weak:
    print(f"  part {r['part']} @{r['t']}s  score {r['score']}\n    said: {r['text']}\n    heard: {r['heard']}")
