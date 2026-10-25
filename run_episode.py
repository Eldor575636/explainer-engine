#!/usr/bin/env python3
"""One command from voice files to finished episode + Shorts.

Usage: python3 run_episode.py <beats.json> <voice file or folder> <work_dir> <out.mp4>

- A folder: every .m4a/.wav/.mp3/.aac inside, sorted by name (01, 02, …), is levelled and joined.
- A single file: used as is.
Then: transcription (faster-whisper medium, Uzbek) → alignment to the exact script → pause trim →
render (16:9 episode, then every Short listed in the beat sheet).
"""
import os, subprocess, sys
from pathlib import Path

HERE = Path(__file__).parent
beats, voice, work, out = (Path(a).resolve() for a in sys.argv[1:5])
work.mkdir(parents=True, exist_ok=True)
env = dict(os.environ, HF_ENDPOINT=os.environ.get("HF_ENDPOINT", "https://hf-mirror.com"))

if voice.is_dir():
    parts = sorted(p for p in voice.iterdir() if p.suffix.lower() in (".m4a", ".wav", ".mp3", ".aac", ".caf"))
    print("Joining", len(parts), "voice files:", ", ".join(p.name for p in parts))
    subprocess.run([sys.executable, str(HERE / "join_voice.py"), str(work / "raw.wav"), *map(str, parts)], check=True)
else:
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(voice), "-ac", "1", "-ar", "48000", str(work / "raw.wav")], check=True)

if not (work / "words.json").exists() or (work / "words.json").stat().st_mtime < (work / "raw.wav").stat().st_mtime:
    print("Transcribing…")
    subprocess.run([sys.executable, str(HERE / "transcribe.py"), str(work / "raw.wav"), "medium", str(work / "words.json")],
                   check=True, env=env)
    print("Patching stretches Whisper dropped…")
    subprocess.run([sys.executable, str(HERE / "patch_transcript.py"), str(work / "raw.wav"), str(work / "words.json")],
                   check=True, env=env)
print("Rendering…")
subprocess.run([sys.executable, str(HERE / "v3.py"), str(beats), str(work), str(out)], check=True, env=env)
print("All done:", out)
