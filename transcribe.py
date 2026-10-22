import json, sys
from faster_whisper import WhisperModel
m = WhisperModel(sys.argv[2], compute_type="int8", cpu_threads=2)
import subprocess, numpy as np
raw = subprocess.run(["ffmpeg","-v","error","-i",sys.argv[1],"-f","f32le","-ac","1","-ar","16000","-"],capture_output=True,check=True).stdout
audio = np.frombuffer(raw, np.float32)
segs, info = m.transcribe(audio, language="uz", word_timestamps=True, vad_filter=False)
words = [[w.word.strip(), round(w.start,3), round(w.end,3)] for s in segs for w in s.words]
json.dump(words, open(sys.argv[3], "w"), ensure_ascii=False)
print(len(words), "words")
