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

## Next (v3)
Layered scenes (background / character / props), walk-ins, draw-on pen circles, counters,
faster pacing (new visual every 2-3s), hook, bigger tags, narrator character.
