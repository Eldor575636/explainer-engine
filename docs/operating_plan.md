# Operating plan: what we make, how often, with which tools (decided 2026-11-26)

Read with CLAUDE.md. Proposed by Claude from the tools and credits on 2026-11-26; owner to confirm or change.

## Lines

| Line | Language | What | Cadence | Status |
| --- | --- | --- | --- | --- |
| Bilmasboy | Uzbek | 10-14 min explainer + 7 Shorts | 1 per week, Friday 04:00 PST | Running (E01-E06 out/scheduled, E07 Dec 18) |
| Eldor Explains | English | Same master episode, US/UK framing + 7 Shorts | 1 per week, Tuesday 09:00 PST (12:00 ET) | Launch E01 Gold, target Tue Dec 8 |
| California Uzbek reels | Uzbek | Owner's own talking-head video, edited by talkinghead.py | Whenever the owner films (aim 2-3 a week) | Depends on owner footage |
| Bysmillah UZ | Uzbek | Business explainers | Own chat and notes | Has priority on ElevenLabs credits |
| Paused | | Podcast, caraoke_cab | | Owner, 2026-11-17 |

## One master episode feeds both channels

- One research + master script per week (docs/master-episode.md), pictures generated once and shared.
- Bilmasboy releases first (Friday); Eldor Explains gets the English version the following Tuesday.
- Backlog: E01 Dollar, E02 Sanctions, E03 Singapore, E04 Diamonds, E05 Inflation already have research and pictures.
  Their English versions only need adaptation, English mascot pictures, voice and render, so Eldor Explains can publish
  weekly from the start while new masters come online. Order: Gold, Dollar, Inflation, Sanctions, Diamonds, Singapore.

## Tools per step

| Step | Tool | Cost |
| --- | --- | --- |
| Topics | vidIQ keyword research + web search | vidIQ credits (150/month) |
| Script | Claude (English approved by Claude; Uzbek reviewed by owner) | none |
| Pictures | Higgsfield: nano_banana_pro only for mascot (2 cr), gpt_image_2_6 for the rest (0.25 cr) | ~50 cr per master + ~20 cr English mascot set |
| Voice, Uzbek | ElevenLabs clone "Eldor British" | ~11.5k credits per episode |
| Voice, English | Free Kokoro blend adam 0.7 / onyx 0.3 (`voice_kokoro.py`) | free, ~8 min |
| Edit/render | v3.py, fx.py, thumbnail.py, shorts_cover.py | free, ~1.5 h CPU per long render |
| Publish | vidIQ (YouTube/TikTok/Instagram), Chrome (Studio, Telegram, Meta Business Suite) | free |
| Owner by hand | Uzbek script review; YouTube Studio checklist (Test & Compare, quiz, end screen, collab) | ~30-45 min per release |

## Monthly budget (4 masters = 8 long videos + 56 Shorts)

- ElevenLabs (121k/month, resets the 7th): Bilmasboy ~46k + Bysmillah UZ first claim; ~60k left as buffer.
- Higgsfield (600/month, renews ~22nd): ~280 for 4 masters + English sets; rest for Bysmillah and thumbnails/covers.
- vidIQ (150/month + add-ons): topic research and the occasional music track; publishing is free.
- Not the limit: credits. The limit is production sessions (one episode per chat) and the owner's review and
  Studio time. So: no second weekly episode until the weekly rhythm holds for a month.

## Weekly rhythm

- Mon: master script (EN) + Uzbek translation -> owner reviews by Tue.
- Tue-Wed: shared pictures, Uzbek voice (ElevenLabs), English voice (Kokoro), beat sheets.
- Thu: render both, visual audit, Shorts, covers, thumbnails A/B/C, quizzes, upload texts.
- Fri: Bilmasboy release + schedule its Shorts; Eldor Explains English version scheduled for next Tuesday.

## Open decisions / next builds

- 30-topic list that works in both languages, ranked by search demand (vidIQ) -> fills the masters after the backlog.
- Own-voice English clone (RVC on Kaggle) only if the owner's English recording makes it clearly better; Kokoro stays until then.
- Owner to-dos for Eldor Explains launch: connect @EldorExplains accounts in vidIQ, upload avatars/banners/bios, slogan.
