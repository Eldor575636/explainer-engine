# Handover: Eldor Explains (English) — status 2026-11-23

Read CLAUDE.md first (Strategy, Eldor Explains brand, AI narration, docs/master-episode.md Engagement rules).

## What the project is
English YouTube channel (+ TikTok, Instagram, Facebook): "money and the economy explained with real data", made to earn
money. Fully automated production: cartoon likeness of Eldor + his voice clone, no filming. Shares a master script per
episode with Bilmasboy (docs/master-episode.md). US/UK viewers, US/UK comparisons, explain never advise.
Strategy research: projects/eldor-explains-e00-strategy/research_brief.md (live doc https://claude.ai/artifact/LP1C4SshvhaHmyu2JtoX9f).

## Decisions (owner, with dates)
- 2026-11-17: new English-only project; main goal is money from YouTube and social media; fully automated AI production.
  Podcast and caraoke_cab are off for now.
- 2026-11-17: adopted the research recommendation: education-style money/economy channel built on real data, YouTube
  long-form as the engine, short-form as the funnel; reuse the Bilmasboy engine (one master script, two channels).
- 2026-11-17: no filming at all; cartoon Eldor + voice clone only. Real-person signal via About page/descriptions.
- 2026-11-17: host name "Eldor" (not El/Al); El Dorado only as backstory/visual detail, not the brand.
- 2026-11-17: channel name **Eldor Explains** (personal, mascot is Eldor, not planning to sell). Details and rejected
  names: projects/eldor-explains-e00-strategy/naming_and_format.md.
- 2026-11-18: Kit A "Ledger" brand; Claude writes and approves English scripts; E01 = Gold (see CLAUDE.md Strategy).
- 2026-11-19: fonts Fraunces/Outfit/Inter (testing); logo = green answer bubble with gold chart; voice = same clone,
  eleven_v4, American news-anchor tag + mood tags (CLAUDE.md, AI narration).

- 2026-11-24/25: voice need not be the owner's; free tools first, paid voice last; picked Kokoro blend adam70/onyx30.

## Style rules
Shared rules live in CLAUDE.md (script rules, visual style, thumbnails, CTAs, audits). Channel-specific:
- Explain, never advise; every episode built on its own dataset/finding; vary structure so episodes don't read as one template.
- US spelling, US/UK comparisons in LOCAL blocks; catchphrase proposal "And now you know the numbers."
- Mascot Look A (white shirt, green vest, gold coin pin, tablet); real person on screen when the line is about them.
- TikTok cuts just over 1 minute (Creator Rewards); Shorts under 60 s pointing to the long video.

## Published / scheduled
Nothing published yet. Handles @EldorExplains looked free on YouTube/TikTok/Instagram/Facebook on 2026-11-17
(Telegram not checked). Brand kits, bios, avatars, banners: brand/eldor-explains/ and Mac
`/Users/eldorruziev/Desktop/Media Projects/Explainer/Eldor Explains/00 Brand`.

## Done
- Brand: Kit A "Ledger" colours, fonts Fraunces/Outfit/Inter, logo = green answer bubble with gold chart
  (brand/eldor-explains/logo/logo_v2.py, sting.py), character Look A (brand/eldor-explains/char/A_analyst.png),
  per-platform kits + bios (brand/eldor-explains/logo/platforms/, bios/; also on the Mac: Eldor Explains/00 Brand).
- Engine English mode: `CHANNEL=ee` (theme.py) switches colours, fonts, UI strings, no new alphabet, Whisper en.
- E01 Gold: `projects/ep06-gold/en/` — script.txt (113 sentences, US spelling), sources.md, picture_prompts.json (15),
  make_beats.py -> ee01_beats.json (105 beats; layers/ has PLACEHOLDER copies for the 15 new pictures), voice_chunks.json.
- The British take (voice/01-06.mp3, raw.wav) is superseded: owner chose the American news-anchor tag + mood tags
  (CLAUDE.md, AI narration). Never mix British and American parts.
- Media (audio/video) is not in git: Mac `/Users/eldorruziev/Desktop/Media Projects/Explainer/Eldor Explains/Season 1/E01 Gold`.

## Open items
- Slogan still open (banner uses "Money, explained with real numbers.").
- Shorts end card and end screen in EN need a visual check.
- Owner's to-dos: connect the @EldorExplains accounts in vidIQ (private browser window), fill his email into the YouTube
  About text, upload avatars/banners/bios; check @EldorExplains on Telegram.
- Not decided: side offer selling engine-made explainer videos to businesses (research_brief.md).

## Next
1. Generate the 15 pictures in picture_prompts.json (Higgsfield; e_* mascot poses need nano_banana_pro + references
   A_analyst.png, scenes/thumbnail poses can use gpt_image_2_6) and replace the placeholders.
2. Voice is DONE for free (2026-11-25): Kokoro blend adam 0.7 / onyx 0.3 via `voice_kokoro.py` ->
   projects/ep06-gold/en/voice/kokoro/raw.wav (9:53, 113 sentences; not in git: re-run the script, ~8 min, or take the
   MP3 sent in chat). Whisper check: only digit-formatting diffs; owner still to listen to the full take. Next: transcribe
   (CHANNEL=ee), re-check beat_times / slow spots, visual audit, render, 7 Shorts, 3 thumbnails + titles, upload texts.
   No ElevenLabs credits needed for Eldor Explains any more (owner: free first, paid last).
3. After launch: 90-day checkpoint (avg view % >= 40, CTR >= 5%, one video > 10k views; otherwise change topics, not format).

## Credits used
- Setup/strategy chat (2026-11-17 to 25): 0 ElevenLabs, 0 Higgsfield (web research, browser checks, free voice tests).
- Later chats: see git log for EE01 test takes (British take + expressive hook test), not tallied here.
