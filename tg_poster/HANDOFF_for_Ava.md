# Task for Ava: run the Bilmasboy Telegram poster on the VPS

## Goal
Post Bilmasboy's scheduled posts to the Telegram channel **@bilmas_boy** automatically, at the right time,
with the correct YouTube link in each post. Your bot is already an admin of @bilmas_boy.

## What you get (this folder, tg_poster/)
- `poster.py`: the poster (Python 3, standard library only, nothing to install).
- `posts.json`: the queue: 10 posts, 7 to send (3 are marked "skip": Eldor posted them by hand).
- `photos/E02_thumb_A.jpg`: image for the E02 episode announcement.
- `make_posts.py`: used by Claude to rebuild posts.json from the content schedule. You don't need to run it.
- `README.md`: short technical notes.

## How it works
- Run `poster.py` every 5 minutes. On each run it sends every post whose time (`at_utc`, UTC) has passed and
  that is not in `sent.json` yet.
- It finds each video's link itself by matching the title in Bilmasboy's public YouTube RSS feed
  (channel @bilmasboy). No YouTube key is needed.
- If the video isn't public yet, it skips and retries on the next run. After 3 hours it posts with the channel link instead.
- Episode announcements go out as a photo post (thumbnail + caption). Shorts posts go out as text with the link.
- `sent.json` (created automatically) records what was sent. Never delete it, or posts will repeat.

## Setup steps
1. Put the whole `tg_poster/` folder on the VPS, e.g. `~/bilmasboy-poster/`.
2. Check the VPS can reach `api.telegram.org` and `www.youtube.com` over HTTPS.
3. Dry run, which prints posts and sends nothing: `cd ~/bilmasboy-poster && python3 poster.py --dry`.
   Before Nov 13 the links will show the channel fallback (`youtube.com/@bilmasboy`), because the videos aren't public yet. That's expected.
4. Add the cron job, using your bot token (keep the token out of any file you share):
   `*/5 * * * * cd ~/bilmasboy-poster && TG_BOT_TOKEN=<your bot token> TG_CHANNEL=@bilmas_boy python3 poster.py >> poster.log 2>&1`
5. Optional test before the first real post: run once with `TG_CHANNEL=` set to a private test channel
   where the bot is admin and one post's `at_utc` set in the past. Check it looks right, then delete that test
   channel's `sent.json` entry before going live. Don't test on @bilmas_boy.

## Queue (San Francisco time = UTC-8)
| Post | Time (SF) | Type |
|---|---|---|
| E01 Shorts 6, 7 | Nov 11, 12 | SKIP (posted by Eldor) |
| E02 episode announcement | Fri Nov 13, 4:15 AM | photo + caption + episode link |
| E02 Short 1 | Nov 13 | SKIP (posted by Eldor) |
| E02 Shorts 2-7 | Nov 14-19, 6:05 AM daily | text + Short link + full-episode link |

**Must be running before Fri Nov 13, 4:15 AM SF (12:15 UTC).**

## Each new episode
Claude sends a new `posts.json` (and the new thumbnail in `photos/`). Replace those files only. Keep `sent.json`.

## Report back to Eldor
- After setup: the result of the dry run and confirmation that the cron job is active.
- After each run that posts or fails: the `poster.log` lines (`posted`, `not live yet`, or an error).
- If a post fails (for example the bot loses admin rights, or a title doesn't match the YouTube title), tell Eldor the same day.
  Don't retype or invent post text. All texts come from posts.json.

## Not in scope
- Telegram Stories: bots can't post channel Stories. Eldor posts those himself.
- Instagram, TikTok, YouTube posting: separate.
