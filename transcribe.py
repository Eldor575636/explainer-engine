import json, sys
from faster_whisper import WhisperModel
m = WhisperModel(sys.argv[2], compute_type="int8", cpu_threads=2)
import subprocess, numpy as np
raw = subprocess.run(["ffmpeg","-v","error","-i",sys.argv[1],"-f","f32le","-ac","1","-ar","16000","-"],capture_output=True,check=True).stdout
audio = np.frombuffer(raw, np.float32)
import os as _os; _lang = "en" if _os.environ.get("CHANNEL", "").lower() in ("ee", "en", "eldor", "eldorexplains") else "uz"
segs, info = m.transcribe(audio, language=_lang, word_timestamps=True, vad_filter=False)
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from translit import to_latin
words = [[to_latin(w.word.strip()), round(w.start,3), round(w.end,3)] for s in segs for w in s.words]
json.dump(words, open(sys.argv[3], "w"), ensure_ascii=False)
print(len(words), "words")
