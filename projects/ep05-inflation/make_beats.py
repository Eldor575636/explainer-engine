"""Builds ep05_beats.json (Inflation) from ep05_sentences.json + this beat plan.
New pictures in layers/ (Higgsfield, 2026-11-13, prompts in picture_prompts.json); mascot sheets, map_world,
prop_gold, prop_dollar, bg_debate_scale, bg_inflation, bg_tashkent_far reused from E03/E04."""
import json
S = json.load(open("ep05_sentences.json", encoding="utf-8"))["sentences"]
# map_world coordinates (same map as E01-E04)
US, DE, FR, HU, ZW, UZ, JP = (.22, .37), (.51, .28), (.485, .31), (.535, .31), (.56, .68), (.645, .35), (.85, .37)
def L(at, t): return {"at": at, "k": "label", "text": t}
def T(at, t, red=False, **kw):
    d = {"at": at, "k": "tag", "text": t}; d.update(kw)
    if red: d["fg"] = "red"
    return d
def ST(at, t, **kw):
    d = {"at": at, "k": "stamp", "text": t}; d.update(kw); return d
def AR(at, a, b, straight=False): return {"at": at, "k": "arrow", "from": list(a), "to": list(b), "straight": straight}
def PIN(at, p): return {"at": at, "k": "pin", "x": p[0], "y": p[1]}
def RG(at, p): return {"at": at, "k": "rings", "x": p[0], "y": p[1]}
def M(at, pose, side="right"): return {"at": at, "k": "mascot", "pose": pose, "side": side}
def F(at, code, **kw):
    d = {"at": at, "k": "flag", "code": code}; d.update(kw); return d
def PR(at, img, x, y, h, **kw):
    d = {"at": at, "k": "prop", "img": img, "x": x, "y": y, "h": h}; d.update(kw); return d
def P(at, img, x, y, h, **kw):
    d = {"img": img, "x": x, "y": y, "h": h, "at": at}; d.update(kw); return d
def C(at, x, y, rx, ry): return {"at": at, "k": "circle", "x": x, "y": y, "rx": rx, "ry": ry}
def BIG(at, t, x=.5, y=.45, **kw):
    d = {"at": at, "k": "bigtext", "text": t, "x": x, "y": y}; d.update(kw); return d
def BARS(at, items, **kw):
    d = {"at": at, "k": "bars", "x": .5, "w": .45, "items": items}; d.update(kw); return d
B = []
def beat(at, typ, **kw):
    d = {"at": at, "type": typ}; d.update(kw); B.append(d)

# ---------------- Hook ----------------
beat([0, "1923-yil"], "scene", bg="bg_cafe_1923", mood="curious", ev=[L([0, "1923-yil"], "1923 · GERMANIYA"), F([0, "Germaniya"], "de"),
     T([1, "5"], "QAHVA: 5 000 MARKA")])
beat([2, "Qahvasini"], "object", props=[P([2, "Qahvasini"], "prop_coffee", .5, .48, .55)],
     ev=[T([2, "hisobni"], "HISOB?", x=.5, y=.85), ST([3, "8"], "8 000 MARKA", y=.22)])
beat([4, "Chunki"], "scene", bg="bg_cafe_1923", crop="right", ev=[T([4, "qisqa"], "BIR FINJON QAHVA VAQTIDA"), T([4, "qadri"], "PULNING QADRI TUSHDI", True)])
beat([5, "Bu"], "scene", bg="bg_bazaar_prices", mood="curious", ev=[T([5, "uzoq"], "UZOQ EMAS"), F([6, "O'zbekistonda"], "uz")])
beat([6, "Bugun"], "scene", bg="bg_bazaar_prices", crop="right", tagpos=[.3, .12],
     ev=[T([6, "100"], "1 YIL OLDIN: 100 000 SO'M"), T([6, "106"], "BUGUN: 106 500 SO'M", True)])
beat([7, "Benzin"], "scene", bg="bg_petrol", ev=[T([7, "Benzin"], "BENZIN ↑"), T([7, "go'shti"], "QO'Y GO'SHTI ↑"), ST([7, "20"], "~20% / 1 YIL", y=.78)])
beat([8, "Xo'sh"], "object", ev=[M([8, "Xo'sh"], 4), T([8, "nega"], "NEGA NARXLAR OSHADI?", x=.36, y=.32),
     T([9, "qadri"], "SO'MNING QADRI QAYERGA KETADI?", True, x=.36, y=.47)])
beat([10, "Va"], "scene", bg="bg_inflation", tagpos=[.6, .16], ev=[T([10, "oshmasligini"], "NOL EMAS..."), T([10, "o'zgina"], "NEGA \"O'ZGINA\" OSHISHI KERAK?", True)])
# ---------------- Intro ----------------
beat([11, "Mening"], "intro", pose=3)
beat([12, "Bilganlarim"], "object", ev=[M([12, "Bilganlarim"], 5), T([12, "Bilganlarim"], "BILIM = BOYLIK", x=.32, y=.3),
     T([12, "savollar"], "SO'RAYMAN", x=.32, y=.45), T([12, "izlanaman"], "IZLANAMAN", x=.32, y=.58)])
beat([13, "Hamda"], "object", ev=[M([13, "Hamda"], 6), T([13, "ulashib"], "ULASHAMAN", True, x=.32, y=.5)])
beat([14, "O'tgan"], "object", props=[P([14, "O'tgan"], "prop_gold", .3, .5, .42)],
     ev=[L([14, "O'tgan"], "4-QISM: OLMOSLAR"), T([14, "uydan"], "TOSH NEGA UYDAN QIMMAT?", x=.7, y=.5)])
beat([15, "Bugun"], "scene", bg="bg_wallet", ev=[T([15, "hamyonimizdagi"], "HAMYONIMIZDAGI HAR BIR SO'M", True)])
beat([16, "Demak"], "title", title="BUGUNGI MAVZU", title2="INFLYATSIYA")
beat([16, "pulimiz"], "scene", bg="bg_inflation", ev=[T([16, "pulimiz"], "PULIMIZ NEGA QADRSIZLANADI?", True)])
# ---------------- 1-qism: inflyatsiya nima ----------------
beat([17, "Avval"], "chapter", num="1-QISM", title="INFLYATSIYA NIMA?")
beat([18, "Inflyatsiya"], "object", props=[P([18, "Inflyatsiya"], "prop_basket", .3, .5, .55)],
     ev=[T([18, "bitta"], "BITTA MAHSULOT EMAS", x=.7, y=.38), T([18, "hamma"], "DEYARLI HAMMA NARSA ↑", True, x=.7, y=.52)])
beat([19, "Boshqacha"], "scene", bg="bg_wallet", crop="left", ev=[T([19, "shu"], "XUDDI SHU PUL"), T([19, "kamroq"], "KAMROQ NARSA", True)])
beat([20, "Buni"], "scene", bg="bg_stat_office", mood="calm", ev=[L([20, "statistika"], "STATISTIKA AGENTLIGI"), T([20, "har"], "HAR OY"),
     T([20, "yuzlab"], "YUZLAB NARX", True)])
beat([21, "Non"], "scene", bg="bg_bazaar_prices", crop="left", tagpos=[.72, .14], ev=[T([21, "Non"], "NON"), T([21, "go'sht"], "GO'SHT"), T([21, "tuxum"], "TUXUM"),
     T([21, "benzin"], "BENZIN"), T([21, "kommunal"], "KOMMUNAL"), T([21, "avtobus"], "AVTOBUS"), T([21, "sartaroshxona"], "SARTAROSHXONA")])
beat([22, "Bularning"], "object", props=[P([22, "Bularning"], "prop_basket", .5, .5, .6)], ev=[T([22, "savatga"], "ISTE'MOL SAVATI", x=.5, y=.12),
     T([22, "har"], "HAR OY SOLISHTIRILADI", True, x=.5, y=.88)])
beat([23, "2026-yil"], "number", prop="prop_basket", value="6,5%", sub="O'ZBEKISTON · 2026-YIL OKTYABR", show=[23, "6,5"])
beat([24, "Lekin"], "scene", bg="bg_butcher", ev=[T([24, "bir"], "HAMMASI BIR XIL EMAS")])
beat([25, "Tuxum"], "object", ev=[BARS([25, "Tuxum"], [{"label": "TUXUM", "value": 13, "at": [25, "13"]},
     {"label": "MOL GO'SHTI", "value": 17, "hl": True, "at": [25, "17"]}], suffix="%"),
     L([25, "Tuxum"], "NARXLAR O'ZGARISHI")])
beat([25, "Toshkentda"], "scene", bg="bg_tashkent_metro", ev=[T([25, "avtobus"], "TOSHKENT: METRO, AVTOBUS"), BIG([25, "26"], "+26%", y=.5)])
beat([26, "Shakar"], "object", props=[P([26, "Shakar"], "prop_sugar", .5, .5, .55)], ev=[ST([26, "2"], "-2% / 1 OY", y=.2), T([26, "arzonladi"], "ARZONLADI", x=.5, y=.85)])
beat([27, "Shuning"], "scene", bg="bg_three_families", ev=[T([27, "o'rtacha"], "6,5% = O'RTACHA"), T([27, "oilaning"], "HAR OILANING O'Z INFLYATSIYASI", True)])
# ---------------- 2-qism: sabablar ----------------
beat([28, "Endi"], "chapter", num="2-QISM", title="NEGA NARXLAR OSHADI?")
beat([29, "Iqtisodchilar"], "object", ev=[M([29, "Iqtisodchilar"], 6), T([29, "uchta"], "3 TA SABAB", True, x=.36, y=.4),
     T([30, "pul"], "1. PUL KO'PAYSA", x=.36, y=.56)])
beat([31, "Tasavvur"], "scene", bg="bg_island", mood="curious", ev=[T([31, "10"], "10 TA OLMA"), T([31, "so'm"], "10 SO'M", True), T([32, "1"], "1 OLMA = 1 SO'M")])
beat([33, "Bir"], "scene", bg="bg_island_ship", ev=[T([33, "yana"], "+10 SO'M", True), T([33, "olma"], "OLMA: HALI HAM 10 TA")])
beat([34, "Endi"], "object", ev=[BIG([34, "2"], "1 OLMA = 2 SO'M"), T([34, "ko'p"], "PUL KO'P, OLMA KAM", x=.5, y=.75)])
beat([35, "Olmaning"], "scene", bg="bg_island", crop="left", ev=[T([35, "o'zgarmadi"], "OLMA O'ZGARMADI"), T([35, "qadri"], "PULNING QADRI TUSHDI", True)])
beat([36, "Amerikalik"], "portrait", fig="friedman_cut", vfocus=.2, ev=[F([36, "Amerikalik"], "us"), L([36, "Milton"], "MILTON FRIDMAN")])
beat([36, "uning"], "object", props=[P([36, "uning"], "prop_banknote_stack", .3, .5, .45)], ev=[T([36, "har"], "\"HAR DOIM VA HAMMA JOYDA\"", x=.68, y=.42),
     T([36, "pul"], "PUL BILAN BOG'LIQ", True, x=.68, y=.58)])
beat([37, "Bir"], "object", sfx=[[0, "ding"]], ev=[M([37, "Bir"], 7), {"at": [37, "obuna"], "k": "subscribe", "x": .4, "y": .45, "dur": 3.4}])
beat([39, "Ikkinchi"], "scene", bg="bg_bakery_gas", mood="calm", ev=[T([39, "Ikkinchi"], "2. ISHLAB CHIQARISH QIMMATLASHSA", True)])
beat([40, "Agar"], "scene", bg="bg_petrol", crop="right", ev=[T([40, "gaz"], "YOQILG'I, ELEKTR, GAZ ↑", True), T([40, "tashish"], "NON VA YUK TASHISH ↑")])
beat([41, "Bu"], "scene", bg="bg_bakery_gas", crop="right", ev=[T([41, "do'kondagi"], "XARAJAT → NARX")])
beat([42, "Masalan"], "scene", bg="bg_tashkent_far", crop="left", ev=[L([42, "2024-yilda"], "2024 · O'ZBEKISTON"), F([42, "O'zbekistonda"], "uz")])
beat([42, "gaz"], "object", ev=[L([42, "gaz"], "2024 · NARX OSHISHI"),
     BARS([42, "gaz"], [{"label": "GAZ ×2,3", "value": 230, "at": [42, "2,3"]}, {"label": "ELEKTR ×1,7", "value": 170, "hl": True, "at": [42, "1,7"]}], novalue=True),
     PR([42, "gaz"], "prop_meter", .8, .52, .26)])
beat([43, "O'sha"], "number", prop="prop_meter", value="9,8%", sub="O'ZBEKISTON · 2024-YIL INFLYATSIYASI", show=[43, "9,8"])
beat([44, "Uchinchi"], "object", ev=[M([44, "Uchinchi"], 8), T([44, "Uchinchi"], "3. KUTISH", True, x=.36, y=.42), T([44, "e'tibordan"], "KO'PINCHA SEZILMAYDI", x=.36, y=.57)])
beat([45, "Agar"], "scene", bg="bg_price_up", ev=[T([45, "do'kondorlar"], "DO'KON: NARX ↑"), T([45, "ishchilar"], "ISHCHI: MAOSH ↑", True)])
beat([46, "Shu"], "scene", bg="bg_price_up", crop="left", ev=[T([46, "kutishning"], "KUTISHNING O'ZI NARXNI OSHIRADI")])
beat([47, "Markaziy"], "number", prop="prop_basket", value="8,7%", sub="AHOLI KUTAYOTGAN INFLYATSIYA", show=[47, "8,7"])
# ---------------- 3-qism: giperinflyatsiya ----------------
beat([48, "Odatda"], "chapter", num="3-QISM", title="GIPERINFLYATSIYA")
beat([49, "Lekin"], "scene", bg="bg_printing_press", mood="dramatic", ev=[T([49, "byudjet"], "BYUDJET TESHIGI"), T([49, "bosib"], "PUL BOSISH", True),
     ST([50, "giperinflyatsiya"], "GIPERINFLYATSIYA", y=.78)])
beat([51, "Ko'rsatuv"], "map", bg="map_world", zf=[.51, .3], ev=[F([51, "Germaniyaga"], "de"), PIN([51, "Germaniyaga"], DE), L([52, "Birinchi"], "1918 · URUSHDAN KEYIN"),
     T([52, "qarzlar"], "QARZ + TOVON TO'LOVLARI", x=.5, y=.85)])
beat([53, "1923-yilda"], "scene", bg="bg_ruhr", ev=[L([53, "1923-yilda"], "1923 · RUR"), F([53, "Fransiya"], "fr"), T([53, "Rur"], "FRANSIYA RURNI EGALLADI")])
beat([53, "hukumat"], "scene", bg="bg_printing_press", ev=[T([53, "ish"], "ISH TASHLASH"), T([53, "bosib"], "MAOSH = YANGI PUL", True)])
beat([54, "1922-yilning"], "scene", bg="bg_bakery_1923", ev=[L([54, "1922-yilning"], "1922 · DEKABR"), T([54, "163"], "1 NON = 163 MARKA")])
beat([55, "Bir"], "object", ev=[L([55, "1923-yil"], "1923 · NOYABR"), BIG([55, "201"], "201 000 000 000"), T([55, "marka"], "MARKA · 1 NON", True, x=.5, y=.72)])
beat([56, "Odamlar"], "scene", bg="bg_money_carts", ev=[T([56, "savat"], "MAOSH SAVATDA")])
beat([57, "Olov"], "scene", bg="bg_money_stove", ev=[T([57, "gazeta"], "GAZETADAN ARZON", True)])
beat([58, "1923-yil"], "scene", bg="bg_printing_press", crop="right", ev=[L([58, "1923-yil"], "1923 · NOYABR"), T([58, "rentenmarka"], "RENTENMARKA"),
     T([58, "1"], "1 YANGI = 1 000 000 000 000 ESKI", True)])
beat([59, "Narxlar"], "scene", bg="bg_savings_lost", mood="dramatic", ev=[T([59, "to'xtadi"], "NARXLAR TO'XTADI"), ST([59, "jamg'armasi"], "JAMG'ARMALAR YO'Q", y=.78)])
beat([60, "Ko'plab"], "scene", bg="bg_unrest", ev=[T([60, "ishonchsizlik"], "ISHONCHSIZLIK + G'AZAB"), T([60, "ekstremistlarning"], "EKSTREMISTLAR KUCHAYDI", True)])
beat([61, "Lekin"], "map", bg="map_world", zf=[.53, .32], ev=[F([61, "Vengriyada"], "hu"), PIN([61, "Vengriyada"], HU), T([61, "eng"], "TARIXDAGI ENG KUCHLI", True, x=.5, y=.85)])
beat([62, "1946-yil"], "scene", bg="bg_budapest", ev=[L([62, "1946-yil"], "1946 · VENGRIYA"), ST([62, "15"], "HAR 15 SOATDA ×2", y=.78)])
beat([63, "Ya'ni"], "scene", bg="bg_budapest", crop="left", ev=[T([63, "ertalab"], "BUGUN ERTALAB: MAOSH"), T([63, "yarmidan"], "ERTAGA: YARMIDAN KAM", True)])
beat([64, "Yaqin"], "map", bg="map_world", zf=[.56, .66], ev=[F([64, "Zimbabve"], "zw"), PIN([64, "Zimbabve"], ZW), L([65, "2008-yil"], "2008 · ZIMBABVE")])
beat([65, "2008-yil"], "scene", bg="bg_harare", ev=[ST([65, "har"], "HAR KUNI ×2", y=.2)])
beat([66, "Hatto"], "object", props=[P([66, "Hatto"], "prop_huge_note", .5, .45, .55)], ev=[L([66, "2009-yil"], "2009 · YANVAR"),
     T([66, "100"], "100 000 000 000 000 DOLLAR", True, x=.5, y=.85)])
beat([67, "Lekin"], "scene", bg="bg_harare", crop="right", ev=[T([67, "qadrsizlandi"], "TEZDA QADRSIZLANDI"), T([67, "voz"], "O'Z PULIDAN VOZ KECHDI", True)])
# ---------------- 4-qism: O'zbekiston ----------------
beat([68, "Endi"], "chapter", num="4-QISM", title="O'ZBEKISTON VA SO'M")
beat([69, "Mustaqillikning"], "scene", bg="bg_tashkent_1990s", mood="calm", ev=[F([69, "O'zbekiston"], "uz"), L([69, "Mustaqillikning"], "1990-YILLAR BOSHI"),
     T([69, "kuchli"], "KUCHLI INFLYATSIYA", True)])
beat([70, "1993-yil"], "object", props=[P([70, "1993-yil"], "prop_coupons", .5, .48, .55)], ev=[L([70, "1993-yil"], "1993 · NOYABR"), T([70, "so'm-kupon"], "SO'M-KUPON", x=.5, y=.85),
     T([71, "gazeta"], "GAZETA QOG'OZIDA", True, x=.5, y=.85)])
beat([72, "1994-yil"], "scene", bg="bg_tashkent_1990s", ev=[L([72, "1994-yil"], "1994 · 1-IYUL"), T([72, "so'm"], "BUGUNGI SO'M", True)])
beat([72, "yangi"], "object", ev=[L([72, "yangi"], "1994 · 1-IYUL"), BIG([72, "ming"], "1 SO'M = 1000 KUPON")])
beat([73, "Xalqaro"], "number", prop="prop_coupons", value="~425%", sub="1994-YIL INFLYATSIYASI · XVJ MA'LUMOTI", show=[73, "425"])
beat([74, "Keyingi"], "scene", bg="bg_tashkent_far", ev=[T([74, "sekinlashdi"], "INFLYATSIYA SEKINLASHDI"), T([74, "qadri"], "SO'M QADRI ↓", True)])
beat([75, "2017-yil"], "scene", bg="bg_exchange_2017", ev=[L([75, "2017-yil"], "2017 · SENTABR"), T([75, "erkinlashtirildi"], "VALYUTA ERKINLASHTIRILDI")])
beat([75, "bir"], "object", ev=[L([75, "bir"], "1 DOLLAR = ? SO'M"),
     BARS([75, "bir"], [{"label": "2017 (OLDIN)", "value": 4210, "at": [75, "4"]}, {"label": "2017 (KEYIN)", "value": 8100, "at": [75, "8"]},
                        {"label": "2026", "value": 11974, "hl": True, "at": [76, "12"]}])])
beat([77, "2022-yildan"], "object", props=[P([77, "2022-yildan"], "prop_banknote_stack", .5, .5, .55)], ev=[L([77, "2022-yildan"], "2022"),
     T([77, "200"], "200 000 SO'MLIK PUL", True, x=.5, y=.85)])
# ---------------- 5-qism: Markaziy bank ----------------
beat([78, "Xo'sh"], "chapter", num="5-QISM", title="KIM KURASHADI?")
beat([79, "Bu"], "scene", bg="bg_central_bank", mood="calm", ev=[L([79, "Markaziy"], "MARKAZIY BANK")])
beat([80, "Uning"], "scene", bg="bg_central_bank", crop="right", ev=[T([80, "quroli"], "ASOSIY QUROL"), T([80, "stavkasi"], "ASOSIY STAVKA", True), T([80, "narxi"], "= PULNING NARXI")])
beat([80, "yana"], "scene", bg="bg_bank_desk", crop="left", ev=[T([80, "banklarga"], "BANKLARGA BERILADIGAN QARZ"), T([80, "foizlari"], "= FOIZ", True)])
beat([81, "Qayta"], "scene", bg="bg_bank_desk", ev=[T([81, "kredit"], "STAVKA ↑ → KREDIT QIMMAT", True), T([81, "bankka"], "OMONAT FOYDALIROQ")])
beat([82, "Odamlar"], "scene", bg="bg_bank_desk", crop="left", ev=[T([82, "kamroq"], "KAMROQ QARZ, KAMROQ XARAJAT"), T([82, "sekinlashadi"], "NARXLAR SEKINLASHADI", True)])
beat([83, "Chunki"], "scene", bg="bg_payslip", ev=[T([83, "qimmatligi"], "QARZ QIMMAT → SARFLASH KAM")])
beat([84, "O'zbekiston"], "number", prop="prop_banknote_stack", value="14%", sub="ASOSIY STAVKA · 2025-YIL MARTIDAN BERI", show=[84, "14"])
beat([85, "Maqsad"], "object", ev=[L([85, "Maqsad"], "O'ZBEKISTON INFLYATSIYASI"),
     BARS([85, "Maqsad"], [{"label": "2024", "value": 9.8}, {"label": "2025", "value": 7.3}, {"label": "2026", "value": 6.5},
                           {"label": "2027 ★", "value": 5, "hl": True, "at": [85, "5"]}], suffix="%")])
beat([86, "Bu"], "map", bg="map_world", zf=[.3, .4], ev=[T([86, "nafaqat"], "NAFAQAT BIZDA", x=.5, y=.85), F([87, "Amerikada"], "us"), PIN([87, "Amerikada"], US)])
beat([87, "xususan"], "scene", bg="bg_us_store_2022", ev=[L([87, "2022-yil"], "2022 · IYUN · AQSH"), BIG([87, "9,1"], "9,1%", y=.5)])
beat([88, "Bu"], "scene", bg="bg_us_store_2022", crop="left", ev=[F([88, "AQSh"], "us"), T([88, "40"], "40 YILDAGI ENG YUQORI", True)])
beat([89, "Lekin"], "object", ev=[M([89, "Lekin"], 9), T([89, "yomon"], "INFLYATSIYA YOMON BO'LSA...", x=.36, y=.4), T([89, "nolga"], "NEGA NOL EMAS?", True, x=.36, y=.56)])
beat([90, "Chunki"], "object", ev=[M([90, "Chunki"], 10), BIG([90, "tushishi"], "NARX TUSHISHI HAM XAVFLI", x=.33, y=.45)])
beat([91, "Buni"], "map", bg="map_world", zf=[.85, .37], ev=[F([91, "Yaponiya"], "jp"), PIN([91, "Yaponiya"], JP), L([92, "1990-yillardan"], "1990-YILLARDAN"),
     T([92, "o'smadi"], "NARXLAR O'SMADI", x=.5, y=.85)])
beat([93, "Shu"], "scene", bg="bg_tokyo", ev=[T([93, "qimmatlashib"], "PUL QIMMATLASHADI"), T([93, "ushlab"], "SARFLASH O'RNIGA SAQLASH", True)])
beat([94, "Maoshlar"], "scene", bg="bg_tokyo", crop="left", ev=[T([94, "Maoshlar"], "MAOSH O'SMADI"), T([94, "investitsiya"], "INVESTITSIYA ↓"), ST([94, "qotib"], "IQTISOD QOTDI", y=.78)])
beat([95, "Shuning"], "object", ev=[L([95, "rivojlangan"], "RIVOJLANGAN DAVLATLAR"), BIG([95, "2"], "~2% / YIL"), T([95, "maqsad"], "MAQSAD: NOL EMAS", True, x=.5, y=.72)])
beat([96, "O'zgina"], "object", ev=[M([96, "O'zgina"], 11), T([96, "O'zgina"], "O'ZGINA = HARAKAT ✓", x=.36, y=.42), T([96, "kuchli"], "KUCHLI = YEMIRADI ✗", True, x=.36, y=.57)])
# ---------------- 6-qism: kim yutadi ----------------
beat([97, "Albatta"], "chapter", num="6-QISM", title="KIM YUTADI, KIM YUTQAZADI?")
beat([98, "Uyda"], "scene", bg="bg_cash_mattress", ev=[T([98, "naqd"], "NAQD PUL UYDA"), ST([98, "yo'qotadi"], "HAR YILI ERIYDI", y=.78)])
beat([99, "Qat'iy"], "scene", bg="bg_bank_desk", crop="right", ev=[T([99, "qarzi"], "QAT'IY FOIZLI QARZ"), T([99, "yengillashtiradi"], "QARZ YENGILLASHADI ✓", True),
     T([100, "miqdori"], "QARZ = O'ZGARMAYDI")])
beat([101, "Iqtisodchilar"], "scene", bg="bg_debate_scale", mood="calm", ev=[L([101, "bahs"], "IQTISODCHILAR BAHSI")])
beat([102, "Bir"], "scene", bg="bg_printing_press", crop="left", ev=[T([102, "ortiqcha"], "1-FIKR: ORTIQCHA PUL"), T([102, "hukumatlarning"], "HUKUMAT XARAJATI", True)])
beat([103, "Boshqa"], "scene", bg="bg_petrol", crop="left", ev=[T([103, "urushlar"], "2-FIKR: TASHQI ZARBALAR"), T([103, "energiya"], "URUSH, ENERGIYA, YETKAZIB BERISH", True)])
beat([104, "Aslida"], "scene", bg="bg_debate_scale", crop="right", ev=[T([104, "ikkala"], "KO'PINCHA IKKALASI BIRGA", True)])
# ---------------- Saboq ----------------
beat([105, "Xo'sh"], "chapter", num="BIZ UCHUN", title="NIMA UCHUN MUHIM?")
beat([106, "Agar"], "object", ev=[BARS([106, "Agar"], [{"label": "MAOSH", "value": 5, "at": [106, "5"]}, {"label": "NARXLAR", "value": 6.5, "color": "red", "at": [106, "6,5"]}],
     suffix="%"), T([106, "kambag'allashgansiz"], "AMALDA KAMBAG'ALLASHDINGIZ", True, x=.5, y=.1)])
beat([107, "Agar"], "scene", bg="bg_payslip", crop="right", ev=[T([107, "past"], "FOIZ < INFLYATSIYA"), T([107, "erib"], "JAMG'ARMA ERIYDI", True)])
beat([108, "Shuning"], "object", ev=[M([108, "Shuning"], 0), T([108, "raqamga"], "FAQAT RAQAM EMAS", True, x=.36, y=.5)])
beat([108, "inflyatsiyadan"], "scene", bg="bg_wallet", ev=[T([108, "haqiqiy"], "HAQIQIY QIYMAT = FOIZ - INFLYATSIYA", True), T([109, "maslahat"], "MOLIYAVIY MASLAHAT EMAS")])
# ---------------- Javob ----------------
beat([110, "Demak"], "title", title="JAVOB", title2="NEGA NARXLAR HAR YILI OSHADI?")
beat([111, "Buning"], "scene", bg="bg_inflation", crop="left", ev=[T([111, "pul"], "1. PUL KO'PAYADI"), T([111, "ishlab"], "2. XARAJAT OSHADI"),
     T([111, "kutsa"], "3. HAMMA KUTADI", True)])
beat([112, "Yo'qolgan"], "scene", bg="bg_cash_mattress", crop="right", ev=[T([112, "saqlovchilardan"], "NAQD PUL EGASIDAN →"), T([112, "qarzdorlarga"], "→ QARZDORGA", True),
     T([112, "davlatning"], "→ DAVLATGA")])
beat([113, "O'zgina"], "scene", bg="bg_money_carts", crop="left", ev=[T([113, "normal"], "O'ZGINA = NORMAL ✓"), T([113, "nazoratdan"], "NAZORATSIZ = XAVFLI ✗", True)])
beat([114, "Inflyatsiya"], "title", title="INFLYATSIYA HAQIDA MEN HAM BILMAS EDIM", title2="ENDI ESA HAMMAMIZ BILAMIZ")
beat([116, "Ana"], "object", ev=[M([116, "Ana"], 4), T([116, "so'mda"], "JAMG'ARMA SO'MDA...", x=.36, y=.38),
     T([116, "oqlaydimi"], "...O'ZINI OQLAYDIMI?", True, x=.36, y=.55), T([117, "izohlarda"], "IZOHDA YOZING", x=.36, y=.72),
     {"at": [116, "sizningcha"], "k": "like", "x": .82, "y": .2}])
beat([118, "Keyingi"], "object", props=[P([118, "Keyingi"], "prop_gold", .32, .52, .38)], ev=[L([118, "Keyingi"], "KEYINGI QISM"),
     T([118, "oltin"], "NEGA BANKLAR OLTIN OLMOQDA?", True, x=.68, y=.5)])
beat([119, "O'tkazib"], "end", pose=1, ev=[{"at": [119, "obuna"], "k": "subscribe", "x": .47, "y": .35, "dur": 3.4}])

# Shorts framing per beat (chosen by eye from the raw pictures, see CLAUDE.md "Visual audit rules")
VF = {  # Shorts framing chosen by eye from WORLD_SHEET (2026-11-13)
    (0, '1923-yil'): {"vfocus": [0.36, 0.62]},
    (4, 'Chunki'): {"vfocus": [0.32, 0.6]},
    (5, 'Bu'): {"vfocus": [0.45, 0.72]},
    (6, 'Bugun'): {"vfocus": [0.22, 0.6]},
    (7, 'Benzin'): {"vfocus": 0.45},
    (10, 'Va'): {"vfocus": 0.45},
    (19, 'Boshqacha'): {"vfocus": 0.45},
    (20, 'Buni'): {"vfocus": [0.3, 0.75]},
    (21, 'Non'): {"vfocus": [0.5, 0.8]},
    (24, 'Lekin'): {"vfocus": [0.38, 0.72]},
    (25, 'Toshkentda'): {"vfocus": 0.45},
    (27, 'Shuning'): {"vfocus": [0.25, 0.8]},
    (31, 'Tasavvur'): {"vfocus": 0.48},
    (33, 'Bir'): {"vfocus": [0.35, 0.65]},
    (35, 'Olmaning'): {"vfocus": 0.62},
    (51, "Ko'rsatuv"): {"vfocus": 0.51},
    (53, '1923-yilda'): {"vfocus": [0.2, 0.68]},
    (53, 'hukumat'): {"vfocus": [0.35, 0.75]},
    (54, '1922-yilning'): {"vfocus": [0.5, 0.82]},
    (56, 'Odamlar'): {"vfocus": [0.3, 0.7]},
    (57, 'Olov'): {"vfocus": 0.48},
    (58, '1923-yil'): {"vfocus": 0.55},
    (59, 'Narxlar'): {"vfocus": 0.53, "vzoom": 1.3},
    (60, "Ko'plab"): {"vfocus": 0.5},
    (61, 'Lekin'): {"vfocus": 0.53},
    (62, '1946-yil'): {"vfocus": 0.33},
    (63, "Ya'ni"): {"vfocus": 0.35},
    (64, 'Yaqin'): {"vfocus": 0.55},
    (65, '2008-yil'): {"vfocus": [0.3, 0.68]},
    (67, 'Lekin'): {"vfocus": 0.6},
    (69, 'Mustaqillikning'): {"vfocus": [0.38, 0.66]},
    (72, '1994-yil'): {"vfocus": [0.38, 0.66]},
    (74, 'Keyingi'): {"vfocus": 0.25},
    (75, '2017-yil'): {"vfocus": [0.3, 0.85]},
    (91, 'Buni'): {"vfocus": 0.83},
    (93, 'Shu'): {"vfocus": 0.3},
    (94, 'Maoshlar'): {"vfocus": 0.45},
}
for _d in B:
    if _d['type'] in ('scene', 'portrait', 'map'):
        _d.update(VF.get(tuple(_d['at']), {}))

cfg = {"layers": "layers", "auto_skip": ["Birs", "Beers"], "music": {"curious": "../../assets/music/curious.mp3", "dramatic": "../../assets/music/dramatic.mp3", "calm": "../../assets/music/calm.mp3"},
       "mascot": {"img": "mascot_v2", "parts": 4, "full_body": True,
                  "more": [{"img": f"mascot_v3{s_}_{i_}", "parts": 1} for s_ in "ab" for i_ in range(4)]},
       "ui": {"subscribe": "OBUNA BO'LING", "subscribed": "OBUNA BO'LDINGIZ", "like": "LAYK", "next": "KEYINGI VIDEO"},
       "sentences": S, "beats": B,
       "shorts": [{"name": "hook", "from": [0, "1923-yil"], "to": [11, "Mening"], "hook": ""},
                  {"name": "basket", "from": [18, "Inflyatsiya"], "to": [28, "Endi"], "hook": "HAR OILANING O'Z INFLYATSIYASI"},
                  {"name": "island", "from": [31, "Tasavvur"], "to": [37, "Bir"], "hook": "OROLDAGI 10 TA OLMA"},
                  {"name": "germany", "from": [51, "Ko'rsatuv"], "to": [61, "Lekin"], "hook": "1 NON = 201 MILLIARD MARKA"},
                  {"name": "record", "from": [61, "Lekin"], "to": [68, "Endi"], "hook": "NARX HAR 15 SOATDA ×2"},
                  {"name": "som", "from": [69, "Mustaqillikning"], "to": [78, "Xo'sh"], "hook": "SO'MNING TARIXI"},
                  {"name": "japan", "from": [89, "Lekin"], "to": [97, "Albatta"], "hook": "NEGA INFLYATSIYA NOL EMAS?"}],
       "end_hold": 9, "pauses": {"37": 1.2, "39": 1.1}, "end_slots": 2, "end_next": "OLTIN", "series_label": "5-QISM: INFLYATSIYA",
       "partners": "Hamkorlarimiz: californiauzbek.com va bysmillah.com loyihalari.",
       "partner_logos": [{"img": "assets/partners/californiauzbek.png", "anim": "assets/partners/californiauzbek_anim.webm", "site": "californiauzbek.com"},
                         {"img": "assets/partners/bysmillah.png", "anim": "assets/partners/bysmillah_anim.mp4", "loop": True, "site": "bysmillah.com", "round": True}], "handle": "@bilmasboy",
       "socials": [["youtube", "@bilmasboy"], ["instagram", "@bilmas.boy"], ["tiktok", "@bilmas.boy"], ["facebook", "@bilmas.boy"], ["telegram", "@bilmas_boy"]]}
json.dump(cfg, open("ep05_beats.json", "w"), ensure_ascii=False, indent=1)
print(len(B), "beats")
