# Explainer Engine — project brain

Read this first in every session. It holds the decisions, style rules and lessons for this project.
Detailed references live in `docs/`.

## What this is

A partly automated pipeline for **daily 1–3 minute vertical (9:16) explainer reels in Uzbek**
about political ideas, systems and historical figures (democracy, communism, Stalin, NATO…).

- New channel, run in collaboration with the creator's existing Instagram account **california_uzbek**
  (37k Uzbek YouTube subscribers on the related channel). Channel name: **Bilmasboy** ("the one who
  doesn't know" + "boy" = rich man). Handles: YouTube @bilmasboy, Instagram/TikTok @bilmas.boy,
  Telegram @bilmas_boy. Closing line: "Bu haqida men ham bilmas edim. Endi hammamiz bilamiz."
  Character bible: https://claude.ai/artifact/Wh7S4aWNjcpK8cCpQyyxm6
- Cadence goal: **one video per day**, produced in weekly batches of 7.
- Quality bar: the "Bir Foiz" (@birfoiz_) Marco Rubio reel. See `docs/reference-analysis.md`.
  We must match its polish while keeping a clearly different look of our own.
- Owner records the Uzbek voiceover himself (ElevenLabs clone only if a side-by-side test proves
  Uzbek sounds natural).

## Pipeline (one video)

1. **Script** (Claude): English draft → Uzbek translation (owner reviews). 250–400 words.
2. **Pictures**: one image per scene in the locked style (below). Today: Gemini/Nano Banana by hand.
   Next: Higgsfield via the connector, generated **in layers** (background / character / props).
3. **Voiceover** (owner): phone or RØDECaster. Long-form: record **one paragraph per file** (01.m4a, 02.m4a…),
   re-record a piece instead of cutting audio by hand; `join_voice.py` levels and joins them into raw.wav.
   The owner never trims pauses himself: the engine does it.
4. **Align**: `transcribe.py` (faster-whisper medium, `language=uz`) gives word times; `build.py`
   aligns the *exact script* to them (DP alignment), so captions always use correct spelling.
5. **Trim**: v1/v2 cap every pause at ~0.3 s. v3 is position-aware (`smart_pieces`): 0.20 s inside a
   sentence (reading hesitations), 0.28 s after a comma, 0.38 s between sentences, 0.55 s at a new
   picture. Ep01 test: 5:01 raw → 4:12.
6. **Render**: `motion.py` (v2) → layered motion graphics + captions + SFX + ducked music.

See `README.md` for commands.

## Script rules

- Structure: hook (0–5 s) → what it is → how it's supposed to work → how it actually worked
  (the reality gap) → why it matters to you → follow call ("Har kuni dunyoni o'zgartirgan bitta
  g'oya uchun obuna bo'ling.").
- Plain language. **No idioms or sarcasm that break in Uzbek translation.** Light, knowing tone.
- Hand the owner clean voiceover text only (no production notes), **one sentence per line**.
- Owner (2026-11-17, E06): pack every episode with as many concrete facts and comparisons as possible (per person, per day,
  vs a famous building/country/company, then vs now) and link sections with a bridging question or line, never a cold jump.
  The mid-video subscribe ask goes right after the first content section, between paragraphs, never inside one.
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

**On-screen text uses the new Uzbek alphabet** (law signed 21 Oct 2026: oʻ→ö, gʻ→ğ, sh→ş, ch→ç,
apostrophe → ʼ). Scripts stay in current spelling; `v3.new_alphabet()` converts captions and labels at
render time. Fonts in `fonts/` include the extended-Latin glyphs.

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

- **v3** (`v3.py`, 16:9): beat sheet (`projects/<ep>/test_beats.json`) with scene types scene/object/map/
  number/title/chapter/portrait and word-triggered events. Two layers per frame: *world* (background,
  figures, props, circles, arrows, pins, rings) goes through a virtual camera that reframes every ~4.5 s
  on long beats; *screen* (labels, tags, stamps, mascot, counters) stays fixed on top. Word triggers fall
  back to the closest word when a line was reworded. Mascot sheet set in the beat sheet (`mascot`:
  img, parts, full_body → framed waist-up).

- **v3 presets** (`fx.py`): animated bar chart (rising/falling tones, optional `novalue`), donut chart,
  subscribe button (cursor, click, bell), like pill, newspaper collage with highlighted word, intro
  wordmark (Bilmas cream + boy mustard), end screen with 4 "watch next" slots, zoom-through and whip
  transitions, extra SFX (ding, bell, click, cash register, swoosh, paper, hit, typewriter, shutter).
  Beat types added: `intro`, `end`, `split`. Transitions are chosen automatically (zoom into chapter/
  title cards, whip between same-type scenes, dissolve otherwise) unless a beat sets `trans`.
- **Auto-director**: adds keyword tags (numbers, names) in any stretch >4 s without a new visual, and an
  extra camera reframe + swoosh in any gap >3.5 s. `edit_report.json` lists what is still slow.
- **Shorts**: `shorts` list in the beat sheet → `<out>_short_<name>.mp4`, 1080x1920, cut from the long
  render: 9:16 crop of the world layer (`vfocus` per beat), re-laid-out labels/charts, 3-word captions
  at 76 px, hook banner for the first 3 s, audio taken from the final long mix.
- **Preview**: `PREVIEW="12.5,@96:57+2" python3 v3.py …` saves 16:9 and 9:16 stills and exits.
- Memory: backgrounds load on demand (LRU 4), captions build on demand; a 13-min episode fits in 8 GB.
- Full episode beat sheet: `projects/ep01-dollar/make_beats.py` → `ep01_beats.json` (84 beats).

## Long-form decisions (2026-10-23)

- Main product is now **YouTube long-form, 16:9 (1920x1080), 12–18 min**; reels/Shorts are 9:16 clips cut from it.
- Owner voice + cartoon mascot; no on-camera footage for now.
- Shared assets: `assets/music/` (curious, dramatic, calm; rotate, never regenerate per episode).
- First episode: `projects/ep01-dollar/` — layers for the test segment + `storyboard_test.md`.
- The v1/v2 engine is vertical; v3 must render 16:9 and support the 10 scene types in the storyboard.

## Open items

- Next end-screen round: put the channel avatar inside the red subscribe ring (empty ring looks unfinished); fix E03 slow spots (chapter card 6:48 holds 6.2 s); owner to pick from the 2026-11-10 suggestions (signature music theme, decisions tracker, Uzbekistan bar, source tags).

- Pilot picture 13 (two ballot boxes) reads as ballot stuffing → owner is regenerating it.
- Owner will send 3–5 more reference reels with timestamped notes → add to `docs/reference-analysis.md`.
- ElevenLabs Uzbek test is pending.
- Mascot: `layers/mascot_v2.jpg` (Higgsfield job cacb2082, 4 poses: thinking, pointing, surprised,
  presenting). Face is close to the owner, clean-shaven; build is still shorter/stockier than asked
  ("slimmer and taller") → owner to judge.

## AI narration (2026-11-04)

- Owner's ElevenLabs clone: "Eldor British" (voice_id 1azPJbJwsAdHELWK7HI3), model eleven_v4, via the ElevenLabs connector.
  ~1 credit per character (a 12-min episode ≈ 10,600 credits for one take). Higgsfield clones did not sound like him.
- `voice_text.py` + `lexicon.json`: text for the voice only (captions keep the script). Years/dates/numbers in Uzbek
  words, "AQSh dollari" → "Amerika dollari" first time then "dollar", "AQSh" → "Amerika Qo'shma Shtatlari" then "Amerika".
- Voice in ~2,000-char parts (01.mp3…), then `check_voice.py` transcribes each part back and scores every sentence;
  low scores are often Whisper errors (digits, Turkish-like spelling), so re-check a slice before regenerating.
- Whisper sometimes answers Uzbek in Cyrillic: `translit.py` converts; transcribe/patch use it automatically.
- `v3.py` event `flag` (code or list of ISO codes; flag-icons SVGs in assets/flags): pops on the spoken word;
  a newer flag in the same beat replaces the older one. `projects/ep01-dollar/enrich_beats.py` shows the pattern.

## Voice: name pronunciation and reusable lines (2026-11-06)

- "Bilmas" / "Bilmasboy" are sent to the voice as IPA with final stress (/bilˈmas/, /bilmasˈboj/), set in lexicon.json.
- E06 (owner): "kon" is read KON, not "kan": lexicon sends koni/konidir/konlari as IPA with a plain /o/ (/koˈni/); "Muruntov" needs
  the stress on the last syllable (/muɾunˈtov/, /muɾunˈtovniŋ/). For a single bad word, regenerate only its sentences, splice them
  into raw.wav (level-matched, same silence padding) and re-transcribe; cheaper than redoing a part.
- The intro block and sign-off are recorded once in `assets/voice/` (see its README) and spliced into each episode
  instead of being regenerated. E02 uses them.
- ElevenLabs audio tags ([curious], [serious]...) were tested on E02's opening; owner chose no tags for now.
- ElevenLabs credits are limited (~39.5k/month on the current plan; a 10-min episode is ~9k). Estimate before big runs.

## Calls to action (2026-11-10)

- Spoken asks only three times: one short subscribe line (<5 s) at the first curiosity point (~first third),
  one yes/no-style opinion question at the end, and the final subscribe/bell/share line before the sign-off.
- Like button mid-video is on screen only (animated pill + SFX), never spoken.
- "Which topic next?" goes in the pinned comment and as end-screen text, not in the voice:
  "Keyingi qismda kim yoki nima haqida bilishni xohlaysiz? Yozing, eng ko'p layk to'plagan mavzuni albatta yoritamiz 👇"

## Owner review rules (2026-11-10, E03)

- No spoken sign-off at the end and no "BILMASBOY" end tag; the episode ends on the subscribe line + end screen.
- When the narration is about a person (e.g. "Li Kuan Yuning fikricha"), show that person, not the mascot.
  The mascot is only for narrator commentary with no main character. Real people get several scene pictures
  (young/old, at work), drawn stylized, with arms visible; portrait cut-outs are generated on flat mustard.
- Mascot has 12 poses: 0-3 mascot_v2, 4-11 single files mascot_v3a_0..3 / mascot_v3b_0..3 (in E03 layers, cfg `mascot.more`).
  Rotate poses; don't repeat the same pose twice in a row.
- No picture on screen longer than ~10 s: split long beats and generate extra scene pictures.
- Engine: charts/counters on pictures get a cream card; long tags are clamped inside the frame; stamps accept x/y;
  the corner logo only opens when the top-left is clear; Shorts logo sits at (52, 74) and the hook banner at y=235.
- End screen layout (from E03 on): cfg `end_slots: 2` = 3-column grid: socials header; mascot left pointing right;
  middle column = subscribe animation, then a red ring + "OBUNA BO'LING" (place YouTube's Subscribe element on it)
  above a "KEYINGI QISMDA: <cfg end_next>" teaser; 2 dashed video frames on the right; partner logos + websites as a
  footer strip that appears only after the last caption is off screen. Tweak via cfg `end_layout`. End screen lasts
  ~15 s: cfg `end_hold`. Subscribe event on the end beat: x .47 y .35. Partner logos (assets/partners/, from the owner's Media Projects brand folders): cfg `partner_logos` → logo card with websites on the end screen (after the subscribe animation) and on every Short end card.

## E04 lessons (2026-11-11)

- The AI voice reads ~6-8 s per sentence and the pause trim barely shortens it (673.5 s -> 673.2 s), so plan ~1 beat
  per sentence; after the first PREVIEW run check `beat_times.json` (now written in preview mode too) for beats >10 s
  and split them (a crop variant of the same picture, a prop object beat or a map counts as a new picture).
- Long chapter/title cards: start the next beat on a later word of the same sentence (e.g. `[68, "olmos"]`).
- Pause + sound around the subscribe ask (owner's request): insert ~0.9 s of silence in raw.wav at that boundary
  (shift words.json), set cfg `pauses` {sentence_idx: seconds}, and beat `sfx` [[offset, "ding"]].
- `bigtext` shrinks itself to fit the frame (16:9 and 9:16); auto-director skips beats with bars/pie.
- Picture prompts for an episode live in `projects/<ep>/picture_prompts.json` (Higgsfield nano_banana_pro, 16:9,
  2 credits each). Check contact sheets for stray words (E04: "SCHOOL" on a building -> regenerated).
- Owner chose: no spoken sign-off (keep it off), English pronunciation for foreign place names when the Uzbek
  spelling sounds off (Sierra Leone), "De Birs" for the voice.

## E05 lessons (2026-11-13)

- Shorts `to` is inclusive: it names the LAST sentence of the clip, not the first one after it ([10, ...] ends before the intro).
  Check that consecutive Shorts don't overlap and that none ends on the subscribe ask or a chapter card.
- Before the full render, list every on-screen word from the beat sheet and check spelling (E05: "OZGINA" for o'zgina, also
  in the script captions). The new-alphabet converter can't fix a missing apostrophe.
- A label that appears with the first word of a Short's opening beat collides with the hook banner: trigger it ~3 s later.
- When a re-recorded line is longer than the original, the splice shifts everything after it: transcribe raw.wav again
  instead of shifting words.json by hand.
- device_commit_files with stagedPath fails for files over ~200 MB (HTTP 400): send the file with SendUserFile and commit its fileUuid.

## Mascot library and empty scenes (2026-11-14, owner feedback on E05)

- Owner: some scenes felt empty, some text sat on other text or on faces, and some mascot poses didn't fit the moment.
  Standing go-ahead: create new mascot poses/situations whenever a beat needs one, and keep them reusable.
- Library in `assets/mascot/` (README lists every item and what it fits): poses `p_*` (full body holding a prop, on cream;
  beat event `M(at, "p_name")`, drawn as the whole figure at 0.9 H) and scenes `s_*` (16:9, mascot in the left third,
  right half calm for tags; use as a scene `bg`). Copy the ones an episode uses into its layers/.
- New items: same prompt prefix as `assets/mascot/prompts.json`, references = mascot_v2 + mascot_v3a_0 (Higgsfield
  nano_banana_pro, 2 credits each), then add a row to the README.
- Picking: a narrator beat with only tags on cream counts as empty -> give the mascot a pose that matches the sentence
  (prices -> basket/receipt, savings -> piggy, lists/reasons -> pointer, news/expectations -> newspaper, debate -> scale,
  maths -> calculator) or a library scene. Never show an unrelated prop (E05 showed gold while talking about diamonds).
- Number beats: prop is capped to the left column (.11-.41 W), value and sub to the right (.45-.89 W).
- During the audit, look for tags on faces and move them with `tagpos`; on busy scenes put tags in empty sky/wall areas.
- Shorts: object/number beats have their own vertical layout (props stacked mid-frame at full size, number = prop / value / sub);
  when a Short still puts a tag on a face, give that beat `vzoom` 1.3-1.5 + `vfy` 0.6 in VF (medium shot, figures sit lower).

## Visual audit rules (2026-11-11, E04 owner feedback)

- Before every full render, audit one PREVIEW still per beat (end of beat, all events on) as numbered contact sheets,
  both 16:9 and 9:16. Look for: text over faces/subjects, words cut by the frame, missing glyphs, unreadable stamps.
- Beat `tagpos: [x, y]` moves the default tag column (and auto-director tags) off faces; stamps take x/y.
- Fonts carry →←✓✗✔✘≈★ (copied from DejaVu by `fonts/patch_symbols.py`; originals in *.orig.ttf). ✓/✗ render as ✔/✘.
- Bars: each item can have `at` (word trigger) so a bar rises when its number is spoken; set it for every chart.
- Stamps (112 px) sit on a cream paper patch; bigtext (default 240) fits the frame around its x and gets a cream card on pictures.
- Auto-director never tags bare numbers (except years) and skips cfg `auto_skip` words (e.g. "Birs").
- Shorts flags sit at (0.86, 0.64).
- Shorts framing is chosen by eye per beat (owner: Shorts lost the characters with a centre crop). Run
  `WORLD_SHEET="ids"` (raw pictures with .1-.9 ticks, no camera), then set per beat in make_beats `VF`:
  `vfocus` x (tight crop, ~0.32 of the width), `vfocus: [a, b]` (pan from subject a to b: hold, glide, hold),
  `vzoom` 1.2-2.0 (medium shot: wider window, blurred bands). Shorts skip the 16:9 camera and use a gentle push-in.
  Saliency models (rembg u2net / human_seg) were tested and miss second characters in these drawings: don't rely on them.
- Shorts: stamps sit at 0.62 height (off faces), long tags shrink to 92% width, charts on pictures get a cream card.

## Delivery (2026-11-12, owner)

- Deliver every file straight into the episode folder on the owner's Mac ("AI Bilmas Boy/Season 1/EXX <name>/1 Script ...
  6 Shorts"), replacing the old copy (one copy per file). Don't attach files in chat; commit them with
  `device_commit_files` using `stagedPath` (under /mnt/user-data/outputs/) and just say what changed and where.

## Thumbnails and titles (2026-11-08)

- Owner (2026-11-17): never reuse the same mascot sheet poses on every thumbnail. Each of A/B/C gets its own topic pose
  (emotion + a topic prop, e.g. hugging a gold bar, wobbling tower, magnifier), generated like the library (`t_<topic>_<what>` in
  assets/mascot, README table) and used as `hero` {part 0, nparts 1}. Same template, different posture/emotion/prop every time.

- Owner's rule: every episode gets **3 titles + 3 thumbnails** (A/B/C, different angles), all run together in YouTube Test & Compare.
  Specs live in `projects/<ep>/thumbs/A.json`, `B.json`, `C.json` (thumbnail.py). Track results in the schedule's "AB tests" tab.
- Every episode gets **7 Shorts** (one a day until the next Friday episode).
- Every long episode gets a **3-question quiz** (4 options max, one correct, one marked Main in case YouTube allows only one),
  written with the script, each with a "Show at" time just after the answer is explained, listed in the schedule's "Quizzes" tab and added in YouTube Studio at upload.
- Partners line (from E03 on, everywhere): "Hamkorlarimiz: californiauzbek.com va bysmillah.com loyihalari." Set `partners` in the
  beat sheet cfg: v3.py shows it on the long-video end screen (under the socials row) and on every Short's end card; also end
  every YouTube description, Shorts caption and Telegram post with it. In text (not on screen) tag the accounts:
  "Hamkorlarimiz: @california_uzbek va @bysmillahcom loyihalari (californiauzbek.com, bysmillah.com)." Handles per platform:
  California Uzbek = @california_uzbek (YouTube, Instagram, Telegram), @california_uz (TikTok), @california.uzbek (Facebook);
  Bysmillah = @bysmillahcom everywhere.

## Publishing via vidIQ (2026-11-15)

- YouTube uploads go through vidIQ: relay each file with Higgsfield media_upload + curl PUT + media_confirm (public CloudFront URL),
  then vidiq_video_upload(url) -> uploadId; thumbnails via vidiq_upload_image (PUT to its uploadUrl). One draft per video,
  publish only after the owner approves the list. Scheduled videos show as private (oEmbed 403) until their time.
- vidIQ free tier: credits ran out on 2026-11-15 (renew Nov 22); drafting, publishing and post status are free.
- TikTok: connect @bilmas.boy in a private browser window (it lives under the California Uzbek login, and OAuth otherwise
  reuses California Uzbek). Settings the owner chose: public, comments on, AI-generated label, music confirmation accepted.
- **Every Short/Reel gets a cover picture (owner, standing rule).** Style = the owner's Gemini covers in
  `EXX/5 Thumbnail/Shorts/` (E01-E03): cream paper with a faint beige sketch of the scene, one bold sticker figure/prop with a
  white outline in the middle, a mustard torn-paper label near the top with 1-2 words. Make them with nano_banana_pro 9:16
  using two of those covers as style references and NO text in the prompt; `shorts_cover.py --label` adds the label in the
  new alphabet. Save as `5 Thumbnail/Shorts/EXX_<n>_<name>.jpg`. Keep the label below the top ~13% (TikTok's grid crops to 3:4).
- vidIQ cannot set a cover, so TikTok/Instagram get a copy of each Short that opens on its cover for 0.2 s
  (`shorts_cover.py --video`); YouTube keeps the original file and its Shorts cover is picked in the YouTube app.
- **Owner's manual checklist per release (remind him the evening before every Friday episode, owner's request 2026-11-15):**
  YouTube Studio long video: Test & Compare B/C, quiz, end screen (2 previous episodes), California Uzbek collab invite,
  playlist, altered-content flag, pinned comment. Each Short: cover (from 5 Thumbnail/Shorts), Related video = the episode,
  collab if offered. Instagram: invite @california_uzbek as collaborator on each live Reel (from E06 on, add it in the draft
  instead). Telegram post, California Uzbek stories. vidIQ cannot do any of these.
- Connected in vidIQ (2026-11-15): YouTube Bilmas Boy; TikTok bilmas.boy (+ California Uzbek, unused); Instagram bilmas.boy
  (29287119210882726); Facebook Pages CFA Uzbekistan, Green Card Go, MyHelp, One_nation.uz, but NOT the Bilmas Boy Page.

## Telegram + Studio via Claude in Chrome (2026-11-15)

- Telegram @bilmas_boy is owned by the owner's personal "Eldor Ruziev" account (web.telegram.org account 3). The Auto Sales
  Manager and Bysmillah accounts are not admins. Posts are scheduled from Chrome: 720p copies of the cover Shorts (<9 MB,
  the upload tool caps at 10 MB; files must sit under /home/claude), captions pasted from the schedule's Telegram column with the
  real episode link, announcement at 4:15 AM with thumbnail A, Shorts at 6:00 AM. Telegram picks its own preview frame (no cover option on web).
  Wait ~8 s after each schedule click before the next upload, or captions merge into the draft. E03-E05 done (24 posts).
- YouTube Studio must be on the Bilmas Boy account (California Uzbek has no edit rights). Thumbnail Test & Compare, quizzes and
  the Shorts' Related video only work once the episode is public; do them on release day. Set Video language + title language = Uzbek.
- End screen: 2 video elements on the dashed frames + Subscribe on the red ring, all from the end-screen start (E03: 9:52).
  YouTube's minimum video element is ~20% larger than our 0.27 W frames: make END2 size ~0.32 from E06 on.

## Facebook Reels via Meta Business Suite (2026-11-16)

- vidIQ never imports the Bilmas Boy Page (only Pages the profile manages directly), so FB Reels are scheduled in Business Suite
  (reels_composer?asset_id=1417098538157897): untick Instagram in "Post to" every time, first suggested thumbnail = cover,
  turn off auto closed captions, Schedule 06:00 America/Los_Angeles. Caption ends with the @california.uzbek partners line.
- Meta stalls uploads at 0% after ~20 in a row; wait a few hours and it works again.
- Status 2026-11-16: every E02-E05 long video and Short is scheduled on all 5 platforms through Dec 10 (E02 TikTok/YouTube by owner).
