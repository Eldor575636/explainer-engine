# Explainer Engine — project brain

Read this first in every session. It holds the decisions, style rules and lessons for this project.
Detailed references live in `docs/`.

## What this is

A partly automated pipeline for **daily 1–3 minute vertical (9:16) explainer reels in Uzbek**
about political ideas, systems and historical figures (democracy, communism, Stalin, NATO…).

- New channel, run in collaboration with the creator's existing Instagram account **california_uzbek**
  (37k Uzbek YouTube subscribers on the related channel). Channel name: **not decided yet**.
- Cadence goal: **one video per day**, produced in weekly batches of 7.
- Quality bar: the "Bir Foiz" (@birfoiz_) Marco Rubio reel. See `docs/reference-analysis.md`.
  We must match its polish while keeping a clearly different look of our own.
- Owner records the Uzbek voiceover himself (ElevenLabs clone only if a side-by-side test proves
  Uzbek sounds natural).

## Pipeline (one video)

1. **Script** (Claude): English draft → Uzbek translation (owner reviews). 250–400 words.
2. **Pictures**: one image per scene in the locked style (below). Today: Gemini/Nano Banana by hand.
   Next: Higgsfield via the connector, generated **in layers** (background / character / props).
3. **Voiceover** (owner): one take, **1-second pause after every sentence**, phone or RØDECaster.
4. **Align**: `transcribe.py` (faster-whisper medium, `language=uz`) gives word times; `build.py`
   aligns the *exact script* to them (DP alignment), so captions always use correct spelling.
5. **Trim**: pauses shortened to ~0.3 s (a 2:13 recording became 1:45).
6. **Render**: `motion.py` (v2) → layered motion graphics + captions + SFX + ducked music.

See `README.md` for commands.

## Script rules

- Structure: hook (0–5 s) → what it is → how it's supposed to work → how it actually worked
  (the reality gap) → why it matters to you → follow call ("Har kuni dunyoni o'zgartirgan bitta
  g'oya uchun obuna bo'ling.").
- Plain language. **No idioms or sarcasm that break in Uzbek translation.** Light, knowing tone.
- Hand the owner clean voiceover text only (no production notes), **one sentence per line**.
- Every historical detail must be correct in the script **and in the image prompts**
  (e.g. Athenians voted by raised hands and pottery shards, not paper ballots).
- Political red lines: global history and ideas are safe. Avoid mocking or attacking current
  Uzbek/Russian leaders; the owner decides which actors to avoid. Real living people are drawn
  stylized, never photorealistic, never in mocking poses.

## Locked visual style: "bold graphic editorial"

| Element | Spec |
|---|---|
| Background | cream `#F4EEDF` with subtle halftone dots, filled with a pale washed-out navy scene |
| Main | deep navy `#1B2A4A` |
| Accent | signal red `#C8102E` (highlights, pen circles, stamps) — ties to california_uzbek red |
| Secondary | mustard `#D4A23A` (labels, maps) |
| Headline font | Anton (labels, stamps) |
| Caption / tag font | Montserrat ExtraBold |
| Motifs | torn-paper mustard labels, white paper tags, red editor's-pen circles/arrows/✓/✗, red rubber stamps |
| Dark variant | navy-black `#0E1626` background for heavy topics (purges, famines, wars) |

**Image prompts never contain text** — every word on screen is added by the engine (correct Uzbek
spelling, editable). Full prompt templates: `docs/style-guide.md`.

## Engine status

- **v1** (`build.py`): flat pictures, slow zoom, labels, 3-word captions. Owner verdict: too flat,
  no motion, no music.
- **v2** (`motion.py`): rembg sticker cut-outs with white outline that pop in and float over an
  inpainted background, bouncing labels, word-timed tags, red stamps with screen shake,
  active-word caption highlight, 0.2 s dissolves, synthesized SFX (pop/whoosh/thud), music ducked
  under voice (sidechaincompress), loudness -14 LUFS. Owner verdict: "a bit better, can be much more
  perfect".
- Effects are declared per scene in `projects/<name>/script.json` → `fx` (triggered by sentence
  index + word prefix), `cutouts` lists which images get a sticker cut-out.

## v3 to-do (priority order)

1. **Layered pictures**: generate background, character and props separately so characters can
   walk in and props can move (the biggest gap vs the reference). Prefer Higgsfield.
2. **Faster pacing**: a new visual event every 2–3 s; no scene longer than ~6 s without a change
   (pilot scene 12 sat for 12.8 s).
3. **Hook**: fast visual hook in the first 2 s.
4. **Bigger, bolder tags** (pilot tags at 44 px were too small; try 54+ px).
5. Red pen circles/arrows that **draw themselves on**, animated map arrows, number counters,
   scoreboards (like the reference's "99 | 0").
6. Recurring **narrator character** (stylized owner or mascot) + logo + intro sting once the name exists.
7. More variety in transitions and SFX.

## Environment notes (cloud sessions)

- `huggingface.co` may be blocked: run with `HF_ENDPOINT=https://hf-mirror.com`.
- faster-whisper 1.2.1 + newer PyAV breaks `decode_audio`; `transcribe.py` decodes with ffmpeg to a
  numpy array instead.
- rembg downloads `u2net.onnx` from GitHub releases (works).
- Fonts came from npm `@fontsource/anton` and `@fontsource/montserrat` (woff → ttf via fontTools).
- Music: generated through the owner's **vidIQ** connector (`vidiq_generate_music`, 25 credits per
  track, 150 credits/month). Never reuse other creators' audio.
- 2-core CPU: v2 render of a 105 s video takes ~5 min.

## Open items

- Pilot picture 13 (two ballot boxes) reads as ballot stuffing → owner is regenerating it.
- Owner will send 3–5 more reference reels with timestamped notes → add to `docs/reference-analysis.md`.
- Higgsfield paid plan and ElevenLabs Uzbek test are pending.
