"""Builds config.json for the midterms reel: captions + pictures only (no cards), no face zoom,
account card kept clear, ad end screen untouched. Real photos when downloaded, else AI pictures."""
import json, os
S = """Amerikada Tramp uchun siyosiy hayot endi deyarli muddatidan avval yakuniga yetdi.
Prezidentning qo'lida Oq uy bor, lekin Kongress va xatto Senat ustidan nazorat ham Demokratlarga o'tmoqda.
Xullas, Trampning siyosiy rejalari endilikda, Washington koridorlarida katta tirbandlikka tushib qoladiganga o'xshaydi.
Nega?
Bugun 2026-yilgi oraliq saylovlarda Demokratlar Senat nazoratini qo'lga kiritdi.
Respublikachilardan kamida 6 ta Senat o'rni Demokratlar tomoniga o'tdi.
Vakillar palatasida yani Kongressda yoki bizning tilda Parlamentda ham Demokratlar katta yutuqlarga erishdi va kamida 12 o'rinni qaytarib olishgani takidlanmoqda.
Endi esa eng qiziq joyiga keldik!
Trampning katta-katta rejalari bor, lekin ularni Kongressdan o'tkazish oson bo'lmaydi.
Aniqrogi endilik deyarli imkonsiz bo'lib qoladi.
Respublikachilar qonun taklif qilsa, Demokratlar qonunni ovozdan o'tkazishmaydi, xattoki ovozga qo'ymasliklari ham mumkin.
Demokratlar qonun taklif qilgan taqdirda esa, Tramp veto qo'yishi yani so'nggi nuqtada Prezident sifatida imzolab qonunni tasdiqlab, kuchga kirishiga imkon bermaydi.
Xullas, keyingi ikki yillik davomida AQSh siyosatida ikki tomonning biri gazni bosadi, ikkinchisi tormozni!
Mashina esa joyidan deyarli qimirlamasdan turaveradi.
Ikkinchidan, Tramp ma'muriyati yani vazirlar uchun Kongress eshiklari endi haqiqiy prokroturaga aylanadi.
Demokratlar vazirlarni chaqirishi, hujjatlar talab qilishi, hukumat faoliyatini tekshirishi va ayrim qarorlar yuzasidan tergovlar boshlashga kirishib ketishadi.
Buning ortidan esa ko'plab vazirlab istefo beradi.
Trampning o'zi esa endi siyosiy raqiblari bilan kurashishdan tashqari, Kongressdagi eshituvlar va tekshiruvlarga ham vaqt ajratishiga to'g'ri keladi.
Eng muhimi, Senat federal sudyalar va yuqori lavozimli amaldorlarni tasdiqlashda katta rol o'ynaydi va bu qudrat endilikda demokratlar qo'liga o'tadi.
Demak, Tramp kimnidir muhim lavozimga tayinlamoqchi bo'lsa, endi Demokratlarning roziligiga olishga majbur bo'ladi.
Bu degani tomonlar kelisholmasligi va qaysar Trampning odatiga ko'ra, oldimizda balki bir necha government shutdown yani hukumat o'z faoliyatini to'xtatishi hodisalari sodir bo'ladi.
Bu o'zgarishlar 2027-yil 3-yanvardan, yangi Kongress ish boshlaganidan keyin kuchga kiradi.
Trampning prezidentlik muddati davom etadi, lekin uning siyosiy rejalarini amalga oshirish ancha qiyinlashadi.
Demokratlar tomoni allaqachon Trampning qolgan ikki yillik Prezidentlik davrini, soxta qo'g'irchoqqa va xatto qo'lidan hech bir ish kelmaydigan irkit o'rdakchaga taqqoslashmoqda.
Xullas, Oq uyda Tramp, Kongressda esa Demokratlar hukmronlik qilishadi.
Keyingi ikki yil Amerikada siyosiy o'zgaruvchan boshqaruvdan ko'ra siyosiy besamar tortishuvlar ko'proq bo'ladiganga o'xshaydi!
Sizningcha, Tramp keyingi ikki yilni samarali o'tkaza oladimi yoki Vashingtonda katta siyosiy tirbandlik boshlanadimi?""".split("\n")
here = os.path.dirname(os.path.abspath(__file__))
def ph(real, ai):
    return real if os.path.exists(os.path.join(here, real)) and os.path.getsize(os.path.join(here, real)) > 50000 else ai
TRUMP = ph("photos/trump.jpg", "pics/p2.png"); WH = ph("photos/whitehouse.jpg", "pics/p2.png")
JOINT = ph("photos/joint_session.jpg", "pics/p3.png"); SEN = ph("photos/senate_vote.jpg", "pics/p3.png")
HEAR = ph("photos/hearing.jpg", "pics/p6.png"); OVAL = ph("photos/oval_signing.jpg", "pics/p5.png")
F = lambda at, img, fy=0.5: {"at": at, "mode": "full", "img": img, "fy": fy}
FACE = lambda at: {"at": at, "mode": "face"}
L = [FACE(0),
 F([0, "Tramp"], TRUMP, 0.25), FACE([0, "deyarli"]),
 F([1, "Oq"], WH), F([1, "Kongress"], JOINT),
 FACE([2, "Xullas,"]), F([2, "Washington"], "pics/p1.png"),
 FACE([3, "Nega?"]),
 F([4, "Demokratlar"], SEN), FACE([5, "Respublikachilardan"]),
 F([6, "Vakillar"], JOINT), FACE([6, "katta"]),
 F([8, "Trampning"], OVAL), FACE([9, "Aniqrogi"]),
 F([10, "Respublikachilar"], "pics/p3.png"), FACE([11, "Demokratlar"]), F([11, "veto"], "pics/p5.png"),
 FACE([12, "Xullas,"]), F([12, "gazni"], "pics/p4.png"), F([13, "Mashina"], "pics/p1.png"),
 FACE([14, "Ikkinchidan,"]), F([14, "Kongress"], HEAR), F([15, "tekshirishi"], "pics/p6.png"),
 FACE([16, "Buning"]),
 F([17, "Trampning"], TRUMP, 0.25), FACE([17, "Kongressdagi"]),
 F([18, "federal"], "pics/p7.png"), F([18, "qudrat"], SEN),
 FACE([19, "Demak,"]), F([19, "tayinlamoqchi"], OVAL),
 FACE([20, "Bu"]), F([20, "government"], "pics/p8.png"),
 F([21, "Bu"], "pics/p9.png"),
 FACE([22, "Trampning"]), F([22, "siyosiy"], TRUMP, 0.25),
 FACE([23, "Demokratlar"]), F([23, "irkit"], "pics/p10.png"),
 F([24, "Oq"], WH), F([24, "Kongressda"], JOINT),
 FACE([25, "Keyingi"]),
 F([26, "Vashingtonda"], "pics/p1.png"), FACE([26, "boshlanadimi?"])]
cfg = {"sentences": S, "face": [0.52, 0.30], "zoom": False, "events": [],
       "music": "assets/music/dramatic.mp3", "music_vol": 0.14,
       "overlay": "ig_card_clean.png", "overlay_modes": ["full"],
       "capy": {"full": 0.70, "face": 0.70}, "untouched_from": 171.7, "layout": L}
json.dump(cfg, open(os.path.join(here, "config.json"), "w"), ensure_ascii=False, indent=1)
print("photos used:", [x for x in (TRUMP, WH, JOINT, SEN, HEAR, OVAL) if x.startswith("photos")])
