"""Voice a whole episode script with a free Kokoro voice blend.
Usage: python3 voice_kokoro.py script.txt out.wav   (Eldor Explains, owner pick 2026-11-25)
Skips '## ...' section headers; 0.38 s between sentences, 0.9 s at a new section.
Writes out.wav (24 kHz) and out.wav.sentences.json (the spoken lines, in order).
Setup (cloud session): pip install kokoro-onnx soundfile; download kokoro-v1.0.onnx + voices-v1.0.bin from
github.com/thewh1teagle/kokoro-onnx releases (model-files-v1.0) into $KOKORO_DIR (default /home/claude/tts).
Polish for listening: highpass 70, +2.5 dB @180 Hz, +2 dB @3.2 kHz, -2 dB @7.5 kHz, compressor 3:1, loudnorm -16."""
import os, sys, json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

BLEND = {"am_adam": 0.7, "am_onyx": 0.3}  # owner pick 2026-11-25 (sample F2)
SPEED = 0.95

k = Kokoro(os.environ.get("KOKORO_DIR", "/home/claude/tts") + "/kokoro-v1.0.onnx", os.environ.get("KOKORO_DIR", "/home/claude/tts") + "/voices-v1.0.bin")
voice = sum(k.get_voice_style(n) * w for n, w in BLEND.items())

parts, sents, sr, gap = [], [], 24000, 0.0
for line in open(sys.argv[1], encoding="utf-8"):
    line = line.strip()
    if not line:
        continue
    if line.startswith("##"):
        gap = 0.9 if parts else 0.0
        continue
    audio, sr = k.create(line, voice=voice, speed=SPEED, lang="en-us")
    parts += [np.zeros(int(sr * (gap or 0.38)), dtype=np.float32), audio.astype(np.float32)]
    sents.append(line)
    gap = 0.0
    print(len(sents), flush=True)
parts.append(np.zeros(int(sr * 0.5), dtype=np.float32))
sf.write(sys.argv[2], np.concatenate(parts), sr)
json.dump(sents, open(sys.argv[2] + ".sentences.json", "w"), ensure_ascii=False, indent=0)
print("sentences", len(sents), "seconds", round(sum(len(p) for p in parts) / sr, 1))
