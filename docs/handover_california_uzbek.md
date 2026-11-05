# Handover: California Uzbek reels (for a new Claude Code chat)

Read this first. It carries everything decided so far for California Uzbek (Eldor's main Instagram/YouTube
channel, @california_uzbek), so the new chat can continue without the old one.

## 1. Where the tools live

- GitHub repo: **Eldor575636/explainer-engine** (clone it; CLAUDE.md there is the project brain).
- California Uzbek talking-head editor: `talkinghead.py` (vertical 1080x1920 reels from Eldor's own clip).
- Example projects to copy from:
  - `projects/cu-midterms/` — the latest CU reel (captions + pictures only). `make_config.py` builds `config.json`.
  - `projects/cu-survey/` — earlier survey reel (cut-out style).
- Usage: `python3 talkinghead.py <config.json> <video> <words.json> <out.mp4>`
  - words.json comes from `transcribe.py <audio.wav> medium <words.json>` (faster-whisper, Uzbek; run with
    `HF_ENDPOINT=https://hf-mirror.com`). Whisper sometimes answers in Cyrillic; `translit.py` converts it
    automatically.
  - Captions use the exact script (DP alignment), so pass the script sentences in the config.

## 2. California Uzbek reel style (owner's decisions — follow exactly)

- **Captions + pictures only.** No keyword cards, titles or text above his head or on his forehead.
  The owner said: "too much words; captions and pictures are enough".
- Captions: word by word, active word on a red pill, at chest height (0.70 of the height).
- **Never cover the california_uzbek account card**: it is burned into the bottom of his videos at about
  0.81–0.89 of the frame height. Nothing goes there. On full-screen pictures, re-draw that card on top
  (`overlay` + `overlay_modes: ["full"]` in the config; `ig_card_clean.png` is a clean copy).
- **No zoom on his face** (`"zoom": false`) — zooming would move the burned-in card.
- **The ending with his ads/partner accounts stays untouched** (`untouched_from: <seconds>`; detect it by the
  frame going dark).
- Full-screen pictures change every 3–6 s on the words he says; back to his face between them.
- **Real photos preferred** for real people/places (owner's request): public-domain images from Wikimedia
  Commons (official White House / Congress photos). Use a User-Agent header; Commons rate-limits hard
  (HTTP 429) — wait 15–60 s between downloads. AI pictures (Higgsfield) only for metaphors and jokes.
- Music: quiet bed (`music_vol` ~0.14), library tracks in `assets/music/`. The owner sometimes removes
  music on his side — ask whether to add one.
- Colours: California Uzbek red `#E2231A`, white, black.
- The owner does NOT want opinions on his political content when he says so — just edit. Facts can be flagged
  once, briefly.

## 3. The ElevenLabs voice (Eldor's own cloned voice)

- Connector: **ElevenLabs** (must be connected in the chat; it is on Eldor's account).
- Voice: **"Eldor British"**, voice_id **1azPJbJwsAdHELWK7HI3** (a cloned voice in his account; find it by
  listing voices with language Uzbek, or pass the id directly).
- Model: **eleven_v4**, default settings, no pronunciation dictionary, mp3 44.1 kHz 128 kbps.
- One take per request (generations_count 1) to save credits; about **1 credit per character**.
- Send text in ~2,000-character parts at paragraph breaks, blank line between paragraphs.
- Higgsfield voice clones were tested and did NOT sound like him — use ElevenLabs.

### Text prep for the voice (Uzbek) — `voice_text.py` + `lexicon.json` do this automatically

- First "AQSh dollari" → "Amerika dollari", afterwards just "dollar".
- First "AQSh" → "Amerika Qo'shma Shtatlari", afterwards "Amerika" (keep suffixes: AQShda → Amerikada).
- Years, dates, numbers in Uzbek words: 1944-yilda → "ming to'qqiz yuz qirq to'rtinchi yilda",
  15-avgust → "o'n beshinchi avgust", 35 dollar → "o'ttiz besh dollar", 9 tasining → "to'qqiztasining".
- SWIFT → Svift, BRIKS → Briks, Bretton-Vuds → Bretton Vuds, XVF → Xalqaro valyuta jamg'armasi,
  BMT → Birlashgan Millatlar Tashkiloti, California Uzbek → Kaliforniya Uzbek, Bysmillah → Bismillah.
- Dashes (—) → commas. Captions keep the original spelling; only the voice text changes.
- After generating, run `check_voice.py <chunks.json> <folder with 01.mp3…>` to compare each sentence with
  the script. Low scores are often Whisper errors (digits, Turkish-like spelling) — re-check that slice before
  paying for a regeneration. Add any word the voice says strangely to `lexicon.json`.

## 4. Practical notes

- Eldor's Mac folder (via the desktop bridge): `/Users/eldorruziev/Desktop/Media Projects/AI Bilmas Boy`
  (that one is for the Bilmasboy channel). Large files (>~30 MB) time out over the bridge: send them one at a
  time, or split into 25 MB parts and join on the Mac with `cat`. Deleting there needs his permission.
- The cloud machine has 2 CPU cores: a 3-minute reel renders in ~8 minutes; render in the background.
- Commit and push changes to the repo when done (the session hook asks for it).
- Keep replies short, no raw code in chat, critical co-founder tone; scripts are clean voiceover text only,
  no idioms that break in Uzbek.
