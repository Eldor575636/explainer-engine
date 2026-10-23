# Explainer Engine (pilot)

Turns numbered pictures + a voiceover + the exact script into a vertical 9:16 explainer.

## Files
- build.py: aligns script words to the recording, trims pauses, cleans audio (also makes the simple v1 video)
- motion.py: v2 motion renderer (sticker cut-outs, bouncing labels, tags, stamps, highlighted captions, dissolves, SFX, ducked music)
- transcribe.py: word timings with faster-whisper (set HF_ENDPOINT=https://hf-mirror.com if huggingface.co is blocked)
- fonts/: Anton + Montserrat ExtraBold (SIL Open Font License)
- projects/democracy/: pilot inputs (script.json holds sentences, scenes, labels, cut-out list and word-timed effects)

## Run
pip install faster-whisper rembg[cpu] opencv-python-headless pillow numpy
python3 transcribe.py projects/X/raw.wav medium projects/X/words.json
python3 build.py projects/X        # alignment + clean voice (+ v1 video)
python3 motion.py projects/X       # v2 video -> projects/X/final_v2.mp4
(Each project also needs raw.wav, layers/NN_mask.png from rembg, optional music.wav)

## Long-form (v3, 16:9)
1. Voice: record one paragraph per file, then join them:
   python3 join_voice.py WORK/raw.wav voice/01.m4a voice/02.m4a ...
2. python3 transcribe.py WORK/raw.wav medium WORK/words.json
3. python3 v3.py projects/ep01-dollar/test_beats.json WORK WORK/out.mp4
   (pauses are trimmed automatically; the beat sheet holds sentences, beats, events, music and mascot)
