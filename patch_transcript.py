#!/usr/bin/env python3
"""Whisper sometimes drops whole stretches of speech in long recordings (gaps with no words while the
audio clearly has voice). This finds those gaps and re-transcribes just them, with a little context on
both sides, then merges the new words into words.json.

Usage: python3 patch_transcript.py <raw.wav> <words.json> [model=medium]
"""
import json, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel

wav, wpath = sys.argv[1], sys.argv[2]
model = sys.argv[3] if len(sys.argv) > 3 else "medium"
words = json.load(open(wpath, encoding="utf-8"))
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", wav, "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
                     capture_output=True, check=True).stdout
audio = np.frombuffer(raw, np.float32)
SR = 16000


def speech_seconds(a, b):
    seg = audio[int(a * SR):int(b * SR)]
    if len(seg) < SR // 10:
        return 0.0
    fr = seg[: len(seg) // 400 * 400].reshape(-1, 400)
    db = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-9)
    return float((db > -38).sum() * 400 / SR)


gaps = []
for (_, _, e0), (_, s1, _) in zip(words, words[1:]):
    if s1 - e0 > 3.0 and speech_seconds(e0, s1) > 1.5:
        gaps.append((e0, s1))
total = len(audio) / SR
if words and total - words[-1][2] > 3 and speech_seconds(words[-1][2], total) > 1.5:
    gaps.append((words[-1][2], total))
print(f"{len(gaps)} gaps with speech:", [(round(a, 1), round(b, 1)) for a, b in gaps])
if not gaps:
    sys.exit(0)

m = WhisperModel(model, compute_type="int8", cpu_threads=2)
for a, b in gaps:
    lo, hi = max(0.0, a - 1.0), min(total, b + 1.0)
    segs, _ = m.transcribe(audio[int(lo * SR):int(hi * SR)], language="uz", word_timestamps=True,
                           vad_filter=True, condition_on_previous_text=False)
    new = [[w.word.strip(), round(w.start + lo, 3), round(w.end + lo, 3)] for s in segs for w in s.words]
    new = [w for w in new if a - 0.05 <= w[1] <= b + 0.05]
    print(f"  {a:.1f}-{b:.1f}s: +{len(new)} words")
    words = [w for w in words if not (a < w[1] < b)] + new
words.sort(key=lambda w: w[1])
json.dump(words, open(wpath, "w", encoding="utf-8"), ensure_ascii=False)
print(len(words), "words after patch")
