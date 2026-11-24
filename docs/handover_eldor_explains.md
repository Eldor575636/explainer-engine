# Handover: Eldor Explains (English) — status 2026-11-23

Read CLAUDE.md first (Strategy, Eldor Explains brand, AI narration, docs/master-episode.md Engagement rules).

## Done
- Brand: Kit A "Ledger" colours, fonts Fraunces/Outfit/Inter, logo = green answer bubble with gold chart
  (brand/eldor-explains/logo/logo_v2.py, sting.py), character Look A (brand/eldor-explains/char/A_analyst.png),
  per-platform kits + bios (brand/eldor-explains/logo/platforms/, bios/; also on the Mac: Eldor Explains/00 Brand).
- Engine English mode: `CHANNEL=ee` (theme.py) switches colours, fonts, UI strings, no new alphabet, Whisper en.
- E01 Gold: `projects/ep06-gold/en/` — script.txt (113 sentences, US spelling), sources.md, picture_prompts.json (15),
  make_beats.py -> ee01_beats.json (105 beats; layers/ has PLACEHOLDER copies for the 15 new pictures), voice_chunks.json.
- The British take (voice/01-06.mp3, raw.wav) is superseded: owner chose the American news-anchor tag + mood tags
  (CLAUDE.md, AI narration). Never mix British and American parts.

## Next
1. Generate the 15 pictures in picture_prompts.json (Higgsfield; e_* mascot poses need nano_banana_pro + references
   A_analyst.png, scenes/thumbnail poses can use gpt_image_2_6) and replace the placeholders.
2. After the ElevenLabs reset on Dec 7: re-voice the whole episode (~11k credits, generations_count 1), transcribe
   (CHANNEL=ee), re-check beat_times / slow spots, visual audit, render, 7 Shorts, 3 thumbnails + titles, upload texts.
3. Open engine items: Shorts end card and end screen in EN need a visual check.
4. Owner's to-dos: connect the @EldorExplains accounts in vidIQ (private browser window), fill his email into the YouTube
   About text, upload avatars/banners/bios. Slogan still open.
