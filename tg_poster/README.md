# Bilmasboy Telegram poster

Posts each Short and episode announcement to @bilmas_boy on schedule, with the right YouTube link found
automatically from the channel's public RSS feed (no YouTube API key). Runs from cron on the VPS.

## Set up once (on the VPS)
1. Copy this folder to the VPS, e.g. `~/bilmasboy-poster/` (or `git pull` the explainer-engine repo).
2. Test without posting: `python3 poster.py --dry` (prints every post with real links found so far).
3. Add to crontab (`crontab -e`), using Ava's bot token:
   `*/5 * * * * cd ~/bilmasboy-poster && TG_BOT_TOKEN=xxxx python3 poster.py >> poster.log 2>&1`

## Every new episode
- Claude updates the schedule and runs `make_posts.py <schedule.xlsx> [ids already posted by hand]` → new posts.json.
- Copy posts.json to the VPS folder (sent.json remembers what already went out, so nothing posts twice).

## Rules
- Shorts posts go out 5 min after the Short is live on YouTube; if YouTube has not published it yet the
  post waits (checks every 5 min, up to 3 h, then posts with the channel link instead).
- Titles must match the YouTube titles in the schedule; for long episodes all three Test & Compare titles are tried.
- SF_OFFSET in make_posts.py is 8 in winter (PST) and 7 in summer (PDT).
