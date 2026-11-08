#!/usr/bin/env python3
"""Bilmasboy Telegram poster. Run every 5 minutes from cron on the VPS.

For each post in posts.json whose time has come and that was not sent yet:
  1. find the YouTube video by its title in the channel's public RSS feed (no API key needed),
  2. put its link into the text, 3. send it to the channel through the bot.
If the video is not live yet, it waits and tries again on the next run (up to 3 hours, then it sends
the post with the channel link instead so the post is never lost). Sent posts are written to sent.json.

Settings (environment variables): TG_BOT_TOKEN (required), TG_CHANNEL (default @bilmas_boy),
YT_HANDLE (default bilmasboy). Test without posting: python3 poster.py --dry
"""
import json, os, re, sys, time, unicodedata, urllib.parse, urllib.request
from datetime import datetime, timezone
from xml.etree import ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
POSTS, SENT, CACHE = (os.path.join(HERE, n) for n in ("posts.json", "sent.json", "channel_id.txt"))
TOKEN = os.environ.get("TG_BOT_TOKEN", "")
CHANNEL = os.environ.get("TG_CHANNEL", "@bilmas_boy")
HANDLE = os.environ.get("YT_HANDLE", "bilmasboy")
GIVE_UP = 3 * 3600
DRY = "--dry" in sys.argv
UA = {"User-Agent": "Mozilla/5.0 (bilmasboy-poster)"}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read().decode("utf-8", "replace")


def channel_id():
    if os.path.exists(CACHE):
        return open(CACHE).read().strip()
    m = re.search(r'"(?:channelId|externalId)":"(UC[\w-]{22})"', get(f"https://www.youtube.com/@{HANDLE}"))
    if not m:
        raise SystemExit("could not find the YouTube channel id")
    open(CACHE, "w").write(m.group(1))
    return m.group(1)


def norm(s):
    s = unicodedata.normalize("NFKC", s).lower().replace("#shorts", "")
    return re.sub(r"[^\w]+", " ", s.replace("ʼ", "'").replace("‘", "'").replace("’", "'")).strip()


def feed():
    xml = get(f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id()}")
    ns = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}
    return [(e.find("a:title", ns).text or "", e.find("yt:videoId", ns).text) for e in ET.fromstring(xml).findall("a:entry", ns)]


def find(titles, videos):
    """titles: one title or a list (all Test & Compare variants of the same video)."""
    for title in ([titles] if isinstance(titles, str) else titles):
        t = norm(title)
        for vt, vid in videos:
            if norm(vt) == t or (len(t) > 15 and (t in norm(vt) or norm(vt) in t)):
                return f"https://youtu.be/{vid}"
    return None


def send(text):
    if DRY:
        print("---- would post ----\n" + text + "\n")
        return
    data = urllib.parse.urlencode({"chat_id": CHANNEL, "text": text}).encode()
    r = json.loads(urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data, timeout=30).read())
    if not r.get("ok"):
        raise RuntimeError(r)


def main():
    if not TOKEN and not DRY:
        raise SystemExit("set TG_BOT_TOKEN")
    posts = json.load(open(POSTS, encoding="utf-8"))["posts"]
    sent = json.load(open(SENT)) if os.path.exists(SENT) else {}
    now = time.time(); videos = None
    for p in posts:
        due = datetime.fromisoformat(p["at_utc"]).replace(tzinfo=timezone.utc).timestamp()
        if p["id"] in sent or p.get("skip") or (now < due and not DRY):
            continue
        videos = videos if videos is not None else feed()
        link = p.get("link") or find(p["video_title"], videos)
        full = p.get("full_link") or (find(p["full_title"], videos) if p.get("full_title") else None)
        late = now - due > GIVE_UP
        if (not link or (p.get("full_title") and not full)) and not late and not DRY:
            print(p["id"], "video not live yet, will retry"); continue
        fallback = f"https://www.youtube.com/@{HANDLE}"
        text = p["text"].replace("{link}", link or fallback).replace("{full}", full or fallback)
        send(text)
        if not DRY:
            sent[p["id"]] = datetime.now(timezone.utc).isoformat()
            json.dump(sent, open(SENT, "w"), indent=1)
            print(p["id"], "posted")


if __name__ == "__main__":
    main()
