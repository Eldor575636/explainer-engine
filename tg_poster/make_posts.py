#!/usr/bin/env python3
"""Build posts.json for poster.py from the Bilmasboy content schedule (Posting calendar tab).
Usage: python3 make_posts.py <schedule.xlsx> [skip_id ...]"""
import json, sys, datetime as dt
from openpyxl import load_workbook

FULL = {"E01": ["Dollar tugayaptimi? AQSh dollari qanday qilib dunyo puliga aylandi",
                "Nega butun dunyo aynan dollarga ishonadi?", "So'mingiz nega dollarga bog'liq? Dollar tarixi"],
        "E02": ["Sanksiyalar qanday ishlaydi? Mir kartasidan 300 milliard dollargacha",
                "Sanksiyalar ishlaydimi? Amerikaning eng kuchli quroli",
                "Sanksiya nima va u O'zbekistonga qanday ta'sir qiladi?"]}
PARTNERS = "Hamkorlarimiz: @california_uzbek va @bysmillahcom loyihalari (californiauzbek.com, bysmillah.com)."
SF_OFFSET = 8          # PST (Nov-Mar); use 7 in PDT (Mar-Nov)
DELAY_MIN = 5          # post 5 minutes after the YouTube video goes live

ws = load_workbook(sys.argv[1])["Posting calendar"]
skip = set(sys.argv[2:])
posts = []
for r in ws.iter_rows(min_row=5, values_only=True):
    d, t, ep, post, yt_title, yt_desc, done = r[0], r[2], r[4], r[5], r[8], r[9], r[14]
    if not d or done == "Yes":
        continue
    code = ep.split()[0]
    at = dt.datetime.combine(d.date() if hasattr(d, "date") else d, t) + dt.timedelta(hours=SF_OFFSET)
    if post.startswith("Short"):
        name = post.split()[1]
        cap = yt_desc.split(" To'liq video kanalda.")[0].strip()
        tags = yt_desc.strip().split("\n")[-1]
        text = f"{cap}\n{{link}}\nTo'liq video: {{full}}\n{tags}\n{PARTNERS}\n@bilmas_boy"
        p = {"id": f"{code}_{name}", "at_utc": (at + dt.timedelta(minutes=DELAY_MIN)).isoformat(),
             "video_title": yt_title.replace(" #shorts", ""), "full_title": FULL[code], "text": text}
    elif post == "Telegram post":
        text = r[10].replace("[YouTube link]", "{link}").strip() + "\n@bilmas_boy"
        p = {"id": f"{code}_episode", "at_utc": at.isoformat(), "video_title": FULL[code], "text": text,
             "photo": f"photos/{code}_thumb_A.jpg"}
    else:
        continue
    if p["id"] in skip:
        p["skip"] = True
    posts.append(p)
json.dump({"note": "Times are UTC. Built from Bilmasboy_content_schedule.xlsx by make_posts.py.", "posts": posts},
          open("posts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for p in posts:
    print(p["id"], p["at_utc"], "SKIP" if p.get("skip") else "")
