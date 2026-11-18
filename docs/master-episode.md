# Master episode: one script, two channels

One research pass and one set of pictures feed two channels:

- **Bilmasboy** (Uzbek, YouTube @bilmasboy) for Uzbek viewers.
- **Eldor Explains** (English, @EldorExplains on YouTube/TikTok/Instagram/Facebook) for US/UK viewers.

The master is written in English with neutral, global framing. Each channel gets its own adaptation of
the marked blocks below; everything else is shared and translated as is.

## Files per episode

```
projects/epNN-<slug>/
  master.md          English master script, blocks marked [CORE] / [LOCAL] / [BRAND] / [CTA]
  sources.md         every fact with its source (shared)
  uz/script.txt      Bilmasboy voiceover (translated CORE + Uzbek LOCAL/BRAND/CTA), one sentence per line
  en/script.txt      Eldor Explains voiceover (CORE + US/UK LOCAL/BRAND/CTA), one sentence per line
  picture_prompts.json, layers/   shared pictures (no text in any picture)
  make_beats.py      one beat sheet; beats tied to CORE sentences are shared, LOCAL/BRAND beats per language
  uz/ en/            voice, words.json, thumbs/, upload_texts.txt, covers per channel
```

## Episode structure (same order in both languages)

| # | Block | Type | Notes |
|---|---|---|---|
| 1 | Hook (0-30 s) | CORE + LOCAL | Global hook with a number; one local comparison line per language |
| 2 | Intro | BRAND | Uzbek: recorded Bilmas intro. English: "I'm Eldor, and this is Eldor Explains." |
| 3 | What it is | CORE | Definitions, first facts |
| 4 | Subscribe ask | CTA | Right after section 3, between paragraphs, < 5 s, written natively per language |
| 5 | How it was supposed to work | CORE | |
| 6 | How it actually worked | CORE | Reality gap, case studies from several countries |
| 7 | The debate | CORE | Both sides, no advice |
| 8 | What it means for you | LOCAL (60-90 s) | Uzbek: Uzbekistan angle. English: US/UK paycheck, rent, prices in $/£, or skip |
| 9 | The answer + catchphrase | CORE + BRAND | Catchphrase per channel |
| 10 | Question + final subscribe | CTA | Opinion question and subscribe line written natively |

## Rules for the master

- Global framing: comparisons that work anywhere (a famous building, a world company, per person, per day, then vs now).
  Country-specific comparisons go only in LOCAL blocks.
- Explain, never advise (YouTube bars AI personas giving money advice). "Here's what the data shows", never "you should buy".
- Every episode is built around its own dataset or finding, and the structure varies a little from episode to episode
  (different hook types, scene order) so the channels never read as one template.
- No idioms or sarcasm that break in translation (the Uzbek version is a translation of CORE).
- Each fact appears once in sources.md; both channels use the same numbers.

## What differs per channel

| | Bilmasboy (uz) | Eldor Explains (en) |
|---|---|---|
| Voice | Eldor British clone, Uzbek lexicon.json | Eldor British clone, English lexicon (to build) |
| On-screen text | New Uzbek alphabet (v3.new_alphabet) | Plain English |
| Mascot look | Navy suit, red tie, gold pocket watch | Own signature look (not the navy suit), gold item that isn't a watch |
| Partners line | California Uzbek + Bysmillah | None by default (Bysmillah only on Islamic-finance topics) |
| End screen | "KEYINGI QISMDA", Uzbek socials | "NEXT", English socials |
| Titles, thumbnails, descriptions | Written natively in Uzbek | Written natively in English, search-friendly titles |
| Shorts | 7 per episode | 7 per episode; TikTok cuts just over 1 minute (Creator Rewards) |

## Costs per episode (approx.)

- Pictures: once (~25-50 Higgsfield images, 2 credits each).
- Voice: twice (~9-10k ElevenLabs credits each); the ~39.5k/month plan covers about 2 episodes in both languages.
- Render: twice (~1.5 h each on the 2-core container).

## Engagement rules (owner, 2026-11-18: "push engagement as much as possible without being annoying")

Owner delegates English script review to Claude. Every English (and master) script and edit follows these:

Script
- Hook <= 30 s: a contrast or surprise ("price crashed 30%, central banks bought more"), the episode question, then 2 open loops
  naming payoffs that come later ("you'll see how one country sold half its gold at the worst moment"). Pay off every loop.
- A "take a guess" beat in the first 2-3 minutes (2-3 options spoken, then the reveal); no "comment your guess" ask.
- Re-hook at least every 60-90 s with a bridging line ("But here's the strange part", "And now the number that shows...").
- Every big number gets a human-scale comparison (per person, vs a building, then vs now).
- Spoken asks stay at three: short subscribe after the first content section, a two-camp opinion question at the end
  ("team gold or team Buffett?"), final subscribe. Like button on screen only.
- Never clickbait: title and thumbnail promise only what the video pays off.

Edit
- First 5 s: the strongest picture plus a moving number (counter, crash line); no logo or intro before the hook.
- On-screen "coming up" card when an open loop is named; chapter cards titled as questions.
- Visual change every 2-3 s; pattern interrupt (zoom, whip, SFX hit) at each re-hook line; guess beat shows the options as
  cards, holds ~1.5 s silence, then reveals.
- Not annoying: one like pill, subscribe animation only at the two spoken asks, no SFX more often than ~every 8 s,
  no fake urgency, music ducked well under the voice.
- Shorts are cut from the payoffs (each open loop's answer is a ready Short).
