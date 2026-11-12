"""Builds ep04_beats.json (Diamonds & De Beers) from ep04_sentences.json + this beat plan.
New pictures in layers/ (Higgsfield, 2026-11-11, prompts in picture_prompts.json); mascot sheets, map_world,
prop_dollar, prop_gold, bg_diamond, bg_debate_scale, bg_conference, bg_tashkent_far reused from E03."""
import json
S = json.load(open("ep04_sentences.json", encoding="utf-8"))["sentences"]
# map_world coordinates (same map as E01-E03)
US, UK, IN, ZA, BW, SL, RU, JP = (.22, .37), (.475, .29), (.69, .49), (.545, .76), (.545, .71), (.445, .56), (.78, .2), (.85, .37)
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
def CT(at, to, x=.5, y=.3, **kw):
    d = {"at": at, "k": "counter", "to": to, "x": x, "y": y}; d.update(kw); return d
def BARS(at, items, **kw):
    d = {"at": at, "k": "bars", "x": .5, "w": .45, "items": items}; d.update(kw); return d
B = []
def beat(at, typ, **kw):
    d = {"at": at, "type": typ}; d.update(kw); B.append(d)

# ---------------- Hook ----------------
beat([0, "Bir"], "scene", bg="bg_ring_buy", mood="curious", ev=[T([0, "uylanmoqchi"], "UYLANMOQCHI"),
     T([1, "ikki"], "2 OYLIK MAOSH", True), C([1, "uzugi"], .5, .55, .1, .12)])
beat([2, "Uzukda"], "object", props=[P([2, "Uzukda"], "prop_carbon", .5, .5, .55)],
     ev=[T([2, "uglerod"], "UGLEROD", x=.3, y=.82), T([2, "ko'mirning"], "KO'MIRNING QARINDOSHI", True, x=.7, y=.82)])
beat([3, "Oradan"], "scene", bg="bg_ring_sell", mood="dramatic", tagpos=[.5, .09], ev=[T([3, "yil"], "BIR NECHA YIL O'TIB..."), T([3, "sotmoqchi"], "SOTMOQCHI"),
     ST([4, "yarmini"], "YARMI HAM YO'Q", y=.76)])
beat([5, "Ba'zi"], "scene", bg="bg_diamond", ev=[T([5, "uydan"], "UYDAN HAM QIMMAT", True)])
beat([6, "Xo'sh"], "object", ev=[M([6, "Xo'sh"], 4), T([6, "qimmat"], "NEGA QIMMAT?", x=.36, y=.35), T([7, "qaytib"], "NEGA SOTIB BO'LMAYDI?", True, x=.36, y=.5),
     ])
# ---------------- Intro ----------------
beat([8, "Va"], "scene", bg="bg_ad_poster", crop="left", tagpos=[.24, .15], ev=[T([8, "to'rtta"], "4 SO'Z"), T([8, "reklama"], "BITTA REKLAMA", True), T([8, "dunyoni"], "BUTUN DUNYO")])
beat([9, "Mening"], "intro", pose=3)
beat([10, "Bilganlarim"], "object", ev=[M([10, "Bilganlarim"], 3), T([10, "Bilganlarim"], "BILIM = BOYLIK", x=.32, y=.3),
     T([10, "savollar"], "SO'RAYMAN", x=.32, y=.45), T([10, "izlanaman"], "IZLANAMAN", x=.32, y=.58), T([11, "ulashib"], "ULASHAMAN", True, x=.32, y=.71)])
beat([12, "O'tgan"], "object", props=[P([12, "Singapur"], "prop_gold", .3, .5, .42)],
     ev=[L([12, "O'tgan"], "3-QISM: SINGAPUR"), T([12, "boyib"], "RESURSSIZ OROL QANDAY BOYIDI?", x=.7, y=.5)])
beat([13, "Bugun"], "scene", bg="bg_diamond_stage", ev=[T([13, "narxni"], "NARXNI NIMA BELGILAYDI?"), T([13, "buyumning"], "BUYUMNING O'ZIMI?"), T([13, "hikoya"], "YOKI HIKOYA?", True)])
beat([14, "Demak"], "title", title="BUGUNGI MAVZU", title2="OLMOSLAR VA ENG MUVAFFAQIYATLI REKLAMA")
beat([14, "eng"], "object", props=[P([14, "eng"], "prop_ring", .3, .5, .5)], ev=[T([14, "eng"], "OLMOSLAR", x=.7, y=.42),
     T([14, "reklama"], "ENG MUVAFFAQIYATLI REKLAMA", True, x=.7, y=.58)])
# ---------------- 1-qism: tarix ----------------
beat([15, "Avval"], "chapter", num="1-QISM", title="NOYOB TOSH")
beat([16, "Asrlar"], "scene", bg="bg_india_diamonds", mood="curious", ev=[T([16, "kam"], "JUDA KAM UCHRAYDI"), ])
beat([17, "Uni"], "scene", bg="bg_india_diamonds", crop="right", ev=[F([17, "Hindistonda"], "in"), T([17, "Hindistonda"], "HINDISTON"), T([17, "podshohlar"], "FAQAT PODSHOHLAR", True)])
beat([18, "1870-yillarda"], "map", bg="map_world", zf=[.55, .7], ev=[L([18, "1870-yillarda"], "1870-YILLAR"), F([19, "Afrikaning"], "za"), PIN([19, "Kimberli"], ZA),
     RG([19, "ulkan"], ZA), T([19, "Kimberli"], "KIMBERLI", x=.5, y=.85)])
beat([20, "Minglab"], "scene", bg="bg_kimberley_rush", ev=[T([20, "Minglab"], "MINGLAB KONCHILAR"), T([21, "ko'payib"], "OLMOS KO'PAYDI", True)])
beat([22, "Muammo"], "object", ev=[M([22, "Muammo"], 7), T([22, "ko'paysa"], "TAKLIF ↑", x=.36, y=.4), T([22, "tushadi"], "NARX ↓", True, x=.36, y=.56),
     ST([23, "noyob"], "NOYOB EMAS", x=.36, y=.75)])
beat([24, "Shu"], "portrait", fig="rhodes_cut", vfocus=.2, ev=[F([24, "ingliz"], "gb"), L([24, "Sesil"], "SESIL RODS"), T([24, "yosh"], "YOSH INGLIZ")])
beat([25, "U"], "scene", bg="bg_rhodes_pumps", ev=[T([25, "nasoslarini"], "SUV NASOSLARI IJARASI"), T([26, "sotib"], "KONLARNI SOTIB OLDI", True)])
beat([27, "Yigirma"], "scene", bg="bg_debeers_1888", mood="dramatic", ev=[CT([27, "Yigirma"], 20, suffix=" YIL", x=.15, y=.25), T([27, "birlashtirdi"], "MINGLAB KONLAR → BITTA KOMPANIYA"),
     L([27, "De"], "DE BEERS")])
beat([28, "1888-yilga"], "map", bg="map_world", zf=[.55, .72], ev=[L([28, "1888-yilga"], "1888"), PIN([28, "Janubiy"], ZA), RG([28, "barcha"], ZA),
     T([28, "barcha"], "DEYARLI BARCHA KONLAR · DE BEERS", True, x=.5, y=.85)])
beat([29, "Keyinroq"], "scene", bg="bg_vault_release", tint=.45,
     ev=[{"at": [29, "90"], "k": "pie", "x": .28, "y": .55, "r": .22, "slices": [{"label": "DE BEERS", "value": 90}, {"label": "BOSHQALAR", "value": 10}]},
         T([29, "taklifining"], "DUNYO TAKLIFINING ~90%", True, x=.5, y=.13)])
beat([30, "Ularning"], "scene", bg="bg_vault_release", crop="right", ev=[T([30, "ko'p"], "KO'P QAZIB OL"), T([30, "oz-ozdan"], "OZ-OZDAN SOT", True)])
beat([31, "Shunda"], "object", props=[P([31, "Shunda"], "prop_ring", .3, .5, .5)], ev=[ST([31, "noyob"], "NOYOB KO'RINADI", x=.7, y=.4), T([31, "yuqori"], "NARX YUQORI", True, x=.7, y=.62)])
beat([32, "Lekin"], "scene", bg="bg_depression", mood="dramatic", ev=[L([32, "1930-yillarda"], "1930-YILLAR"), T([33, "Buyuk"], "BUYUK DEPRESSIYA", True)])
beat([34, "Odamlarda"], "scene", bg="bg_depression", crop="right", ev=[T([34, "pul"], "PUL YO'Q"), T([34, "keskin"], "OLMOS SOTUVI ↓", True)])
beat([35, "Taklifni"], "object", ev=[M([35, "Taklifni"], 0), T([35, "Taklifni"], "TAKLIF: NAZORATDA ✓", x=.36, y=.4), T([35, "talabni"], "TALAB: QANDAY?", True, x=.36, y=.56),
     T([36, "muhtoj"], "OLMOSGA MUHTOJ QILISH?", x=.36, y=.72)])
beat([37, "Bir"], "object", sfx=[[0.0, "ding"]], ev=[M([37, "Bir"], 11), {"at": [37, "obuna"], "k": "subscribe", "x": .36, "y": .5, "dur": 3.4}])
# ---------------- 2-qism: reklama ----------------
beat([39, "1938-yilda"], "chapter", num="2-QISM", title="REKLAMA")
beat([39, "Amerikadagi"], "scene", bg="bg_adagency_1938", mood="curious", ev=[L([39, "Amerikadagi"], "1938 · N. W. AYER"), F([39, "Amerikadagi"], "us"), T([40, "boshqalarga"], "BOSHQACHA AGENTLIK")])
beat([41, "U"], "scene", bg="bg_adagency_1938", crop="right", ev=[T([41, "do'konni"], "DO'KON EMAS"), ST([41, "brendni"], "BREND EMAS")])
beat([42, "U"], "scene", bg="bg_ad_poster", ev=[T([42, "g'oyani"], "BITTA G'OYA:"), T([42, "sevgi"], "HAQIQIY SEVGI = OLMOS UZUK", True)])
beat([43, "Gazetalarga"], "scene", bg="bg_movie_star", ev=[T([43, "Gazetalarga"], "GAZETALAR"), T([43, "kino"], "KINO YULDUZLARI", True)])
beat([44, "Maktablarga"], "scene", bg="bg_school_lecture", ev=[T([44, "Maktablarga"], "MAKTABLARDA MA'RUZA"), T([44, "yoshlarga"], "YOSHLARGA", True)])
beat([45, "1941-yilga"], "object", props=[P([45, "1941-yilga"], "prop_ring", .3, .5, .45)], ev=[L([45, "1941-yilga"], "1941 · AMERIKA"),
     CT([45, "55"], 55, prefix="+", suffix="%", x=.7, y=.45), T([45, "sotuvi"], "OLMOS SOTUVI", True, x=.7, y=.65)])
beat([46, "1947-yilda"], "portrait", fig="gerety_cut", vfocus=.2, ev=[L([46, "1947-yilda"], "1947"), T([46, "Frensis"], "FRANCES GERETY"),
     T([46, "kopirayteri"], "YOSH KOPIRAYTER", True)])
beat([47, "Bu"], "scene", bg="bg_ad_meeting", ev=[T([47, "to'rtta"], "4 SO'Z", x=.82, y=.1), {"at": [47, "diamond"], "k": "bigtext", "text": "\"A DIAMOND IS FOREVER\"", "x": .5, "y": .8, "size": 130},
     T([48, "abadiydir"], "OLMOS ABADIYDIR", True, x=.82, y=.19)])
beat([49, "Bu"], "scene", bg="bg_ad_poster", crop="right", ev=[ST([49, "mashhur"], "ENG MASHHUR SHIORLARDAN", y=.8)])
beat([50, "Uning"], "object", props=[P([50, "Uning"], "prop_ring", .3, .5, .5)], ev=[T([50, "ikki"], "IKKI MA'NO", x=.7, y=.3),
     T([51, "sevgingiz"], "1. SEVGINGIZ ABADIY", x=.7, y=.45)])
beat([52, "Ikkinchisi"], "scene", bg="bg_ad_poster", crop="right", ev=[T([52, "ko'zga"], "IKKINCHI MA'NO...", True)])
beat([53, "Ammo"], "object", ev=[M([53, "Ammo"], 9), T([53, "tadqiqotchilar"], "TADQIQOTCHILAR FIKRICHA", x=.36, y=.4), T([53, "sotmang"], "2. HECH QACHON SOTMANG", True, x=.36, y=.58)])
beat([54, "Nega"], "scene", bg="bg_vault_release", crop="left", tint=.5, ev=[T([54, "sotmasligi"], "NEGA SOTMASLIK MUHIM?", True)])
beat([55, "Chunki"], "scene", bg="bg_ring_sell", crop="left", tagpos=[.55, .45], ev=[T([55, "sotishni"], "HAMMA SOTSA → OLMOS KO'PAYADI"), T([55, "narx"], "NARX TUSHADI", True)])
beat([56, "Odamlar"], "object", props=[P([56, "Odamlar"], "prop_ring", .3, .5, .5)], ev=[T([56, "ikkinchi"], "IKKINCHI BOZOR YO'Q", x=.7, y=.4), ST([56, "ushlab"], "NARX YUQORIDA", x=.7, y=.62)])
beat([57, "Natija"], "scene", bg="bg_wedding_usa", mood="calm", ev=[ST([57, "hayratlanarli"], "HAYRATLANARLI", y=.8)])
beat([58, "1940-yilda"], "object", ev=[F([58, "Amerikadagi"], "us"), L([58, "1940-yilda"], "OLMOS UZUKLI KELINLAR"),
     BARS([58, "1940-yilda"], [{"label": "1940", "value": 10, "color": "red", "at": [58, "10"]}, {"label": "1980", "value": 80, "hl": True, "at": [58, "80"]}], suffix="%")])
beat([59, "Reklama"], "object", props=[P([59, "Reklama"], "prop_salary_scale", .3, .5, .55)], ev=[T([59, "qancha"], "QANCHA SARFLASH KERAK?", True, x=.7, y=.5)])
beat([60, "Avval"], "scene", bg="bg_wedding_usa", crop="right", ev=[T([60, "bir"], "AVVAL: 1 OYLIK MAOSH"), T([60, "ikki"], "KEYIN: 2 OYLIK MAOSH", True), T([60, "sevgining"], "SEVGINING NARXI")])
beat([61, "Keyin"], "map", bg="map_world", zf=[.8, .4], ev=[F([61, "Yaponiyaga"], "jp"), PIN([61, "Yaponiyaga"], JP), AR([61, "e'tiborini"], US, JP)])
beat([62, "Aslida"], "scene", bg="bg_japan_traditional", ev=[ST([62, "yo'q"], "UZUK AN'ANASI YO'Q"), L([63, "1960-yilda"], "1960"),
     T([63, "5"], "5% DAN KAM", True)])
beat([64, "Keyin"], "scene", bg="bg_japan_modern", mood="curious", ev=[T([65, "zamonaviy"], "ZAMONAVIY"), T([65, "G'arbcha"], "G'ARBCHA HAYOT", True)])
beat([66, "1981-yilga"], "scene", bg="bg_japan_modern", crop="left",
     ev=[BARS([66, "1981-yilga"], [{"label": "1960", "value": 5, "color": "red"}, {"label": "1981", "value": 60, "hl": True, "at": [66, "60"]}], suffix="%")])
# ---------------- 3-qism: haqiqat ----------------
beat([67, "Ya'ni"], "scene", bg="bg_japan_traditional", crop="right", ev=[T([67, "qadimiy"], "QADIMIY AN'ANALAR"), T([67, "yigirma"], "YANGI AN'ANA 20 YILDA", True)])
beat([68, "Endi"], "chapter", num="3-QISM", title="HAQIQATAN QIMMATMI?")
beat([68, "olmos"], "object", ev=[M([68, "olmos"], 4), {"at": [68, "qimmatmi"], "k": "bigtext", "text": "QIMMATMI?", "x": .33, "y": .45}])
beat([69, "Sotib"], "scene", bg="bg_ring_buy", crop="left", tagpos=[.25, .1], ev=[T([69, "qimmat"], "SOTIB OLISH: JUDA QIMMAT")])
beat([70, "Lekin"], "scene", bg="bg_ring_sell", crop="right", mood="dramatic", tagpos=[.42, .08], ev=[ST([70, "yarmiga"], "~50%", x=.3, y=.78), T([70, "sotmoqchi"], "SOTISH: YARMIGA YAQIN", True)])
beat([71, "Yangi"], "object", props=[P([71, "Yangi"], "prop_car", .3, .5, .45)], ev=[AR([71, "kabi"], (.45, .5), (.6, .5), True),
     PR([71, "olmos"], "prop_ring", .75, .5, .38), T([71, "yo'qotadi"], "DO'KONDAN CHIQDI = QADRI ↓", True, x=.5, y=.85)])
beat([72, "Sababi"], "scene", bg="bg_diamond_stage", ev=[T([72, "tabiati"], "TABIATI EMAS"), T([72, "hikoya"], "HIKOYA BELGILAYDI", True)])
beat([73, "Lekin"], "chapter", num="4-QISM", title="IKKINCHI TOMON")
beat([73, "bu"], "object", ev=[M([73, "bu"], 10), {"at": [73, "ikkinchi"], "k": "bigtext", "text": "IKKINCHI TOMON", "x": .33, "y": .45}])
beat([74, "1990-yillarda"], "scene", bg="bg_sierra_leone", mood="dramatic", ev=[L([74, "1990-yillarda"], "1990-YILLAR"), F([74, "Syerra-Leoneda"], "sl", x=.08, y=.12),
     T([74, "urushi"], "FUQAROLAR URUSHI")])
beat([75, "Qurolli"], "scene", bg="bg_sierra_leone", crop="right", ev=[T([75, "moliyalashtirdi"], "URUSH OLMOS PULIDAN"), ST([76, "qonli"], "QONLI OLMOSLAR", y=.78)])
beat([77, "2000-yilda"], "scene", bg="bg_kimberley_process", mood="calm", ev=[L([77, "2000-yilda"], "2000"), T([77, "Kimberli"], "KIMBERLI JARAYONI")])
beat([78, "Bu"], "scene", bg="bg_kimberley_process", crop="right", ev=[T([78, "maqsadi"], "MAQSAD:"), T([78, "bozordan"], "URUSH OLMOSLARINI CHIQARISH", True)])
beat([79, "Lekin"], "scene", bg="bg_kimberley_process", crop="left", ev=[T([79, "to'liq"], "TO'LIQ KUZATMAYDI"), ST([79, "tanqid"], "TANQID")])
beat([80, "Olmos"], "map", bg="map_world", zf=[.72, .3], ev=[F([81, "Rossiyada"], "ru"), PIN([81, "Rossiyada"], RU), T([81, "uchdan"], "DUNYO XOM OLMOSINING ~1/3", x=.5, y=.85)])
beat([82, "2024-yil"], "scene", bg="bg_diamond_ban", ev=[L([82, "2024-yil"], "2024"), T([82, "G7"], "G7 TAQIQI", True)])
beat([83, "O'tgan"], "scene", bg="bg_russia_mine", ev=[T([83, "sanksiyalar"], "2-QISM: SANKSIYALAR"), T([83, "bozoriga"], "OLMOS BOZORIDA HAM", True)])
# ---------------- 5-qism: laboratoriya ----------------
beat([84, "Endi"], "chapter", num="5-QISM", title="LABORATORIYA OLMOSI")
beat([85, "U"], "scene", bg="bg_lab_diamond", mood="curious", ev=[T([85, "laboratoriyada"], "LABORATORIYADA O'STIRILADI", True)])
beat([86, "Bu"], "object", props=[P([86, "Bu"], "prop_carbon", .5, .45, .45)], ev=[ST([86, "soxta"], "SOXTA EMAS", y=.2), T([86, "kimyoviy"], "KIMYOVIY JIHATDAN BIR XIL", True, x=.5, y=.82)])
beat([87, "Ko'p"], "scene", bg="bg_gemologist", ev=[T([87, "maxsus"], "FAQAT MAXSUS ASBOB BILAN FARQLANADI"), C([87, "farqlay"], .5, .5, .2, .2)])
beat([88, "Va"], "scene", bg="bg_ring_compare", ev=[T([88, "arzon"], "ANCHA ARZON", True)])
beat([89, "2025-yilda"], "scene", bg="bg_ring_buy", crop="right", tagpos=[.5, .82], ev=[L([89, "2025-yilda"], "2025 · AMERIKA"), T([89, "tabiiy"], "O'RTACHA UNASHTIRUV UZUGI")])
beat([89, "bo'lsa"], "object", ev=[L([89, "bo'lsa"], "O'RTACHA UZUK NARXI"),
     BARS([89, "laboratoriya"], [{"label": "TABIIY", "value": 12961, "color": "red"}, {"label": "LABORATORIYA", "value": 4557, "hl": True, "at": [89, "4"]}], suffix="$", w=.55)])
beat([90, "2019-yilda"], "scene", bg="bg_ring_compare", crop="right", ev=[L([90, "2019-yilda"], "2019"), T([90, "6"], "LABORATORIYA OLMOSI: ATIGI 6%", True)])
beat([90, "2026-yilning"], "object", ev=[L([90, "2026-yilning"], "LABORATORIYA OLMOSLI YANGI UZUKLAR"),
     BARS([90, "2026-yilning"], [{"label": "2019", "value": 6, "color": "red"}, {"label": "2026", "value": 51, "hl": True, "at": [90, "51"]}], suffix="%", w=.5)])
beat([91, "Ya'ni"], "scene", bg="bg_lab_diamond", crop="right", ev=[T([91, "tarixda"], "TARIXDA BIRINCHI MARTA"), ST([91, "yarmidan"], "YARMIDAN KO'PI", x=.3, y=.8)])
beat([92, "Bu"], "scene", bg="bg_boardroom_sale", mood="dramatic", ev=[ST([92, "zarba"], "KATTA ZARBA")])
beat([93, "De"], "object", props=[P([93, "De"], "prop_dollar", .3, .5, .45)], ev=[T([93, "85"], "85% · ANGLO AMERICAN", True, x=.7, y=.5)])
beat([93, "uch"], "scene", bg="bg_boardroom_sale", crop="left", ev=[T([93, "uch"], "3 YIL KETMA-KET"), T([93, "pasaytirib"], "QIYMATI ↓", True)])
beat([94, "2025-yil"], "number", prop="prop_dollar", value="$2,3 MLRD", sub="2025-YIL OXIRI · 85% ULUSH BAHOSI", show=[94, "atigi"])
beat([95, "Oxir-oqibatda"], "scene", bg="bg_boardroom_sale", crop="right", ev=[T([95, "asrdan"], "100+ YIL BOZORNI BOSHQARDI"), ST([95, "sotuvga"], "SOTUVDA")])
beat([96, "2026-yil"], "scene", bg="bg_botswana_mine", ev=[L([96, "2026-yil"], "2026 · NOYABR"), F([96, "Botsvana"], "bw"),
     CT([96, "30"], 30, suffix="% ULUSH", x=.8, y=.3)])
beat([97, "Ya'ni"], "map", bg="map_world", zf=[.55, .68], ev=[F([97, "Afrika"], "bw"), PIN([97, "Afrika"], BW), RG([97, "aksiyadoriga"], BW),
     T([97, "aksiyadoriga"], "ENG KATTA AKSIYADOR", True, x=.5, y=.85)])
beat([98, "Shu"], "scene", bg="bg_debate_scale", ev=[L([98, "bahs"], "BAHS DAVOM ETADI")])
beat([99, "Bir"], "scene", bg="bg_russia_mine", crop="right", ev=[T([99, "millionlab"], "MILLIONLAB YIL YER OSTIDA"), T([99, "noyob"], "\"TABIIY OLMOS NOYOB\""),
     T([99, "qadrini"], "\"QADRI SAQLANADI\"", True)])
beat([100, "Boshqa"], "scene", bg="bg_ring_compare", crop="left", ev=[T([100, "reklama"], "\"NARXNI REKLAMA YARATGAN\"", True), T([100, "laboratoriya"], "LABORATORIYA OCHIB BERDI")])
beat([101, "Yana"], "scene", bg="bg_botswana_town", mood="calm", ev=[F([101, "Botsvana"], "bw"), T([101, "byudjetning"], "BYUDJETNING ASOSIY MANBAI", True)])
# ---------------- 6-qism: biz uchun ----------------
beat([102, "Olmos"], "scene", bg="bg_botswana_mine", crop="left", ev=[T([102, "tushganda"], "OLMOS NARXI ↓"), T([102, "oddiy"], "ODDIY AHOLI ZARAR KO'RADI", True)])
beat([103, "Xo'sh"], "chapter", num="6-QISM", title="BIZ UCHUN SABOQ")
beat([104, "O'zbekistonda"], "scene", bg="bg_uzbek_wedding", ev=[F([104, "O'zbekistonda"], "uz"), T([104, "to'y"], "TO'Y VA SOVG'ALAR"),
     T([105, "saqlash"], "PULNI SAQLASH USULIMI?", True)])
beat([106, "Lekin"], "object", props=[P([106, "Lekin"], "prop_scale_gold_diamond", .5, .5, .55)], ev=[ST([106, "emas"], "BIR XIL EMAS", y=.2)])
beat([107, "Oltinning"], "scene", bg="bg_gold_bazaar", ev=[T([107, "har"], "OLTIN: NARX HAR KUNI OCHIQ"), T([107, "oson"], "SOTISH OSON ✓")])
beat([108, "Olmosni"], "scene", bg="bg_ring_sell", crop="left", tagpos=[.55, .42], ev=[T([108, "arzonga"], "OLMOS: ANCHA ARZONGA ✗", True)])
beat([109, "Demak"], "object", ev=[M([109, "Demak"], 7), T([109, "sevgi"], "SEVGI RAMZI ✓", x=.36, y=.42), T([109, "investitsiya"], "INVESTITSIYA? ✗", True, x=.36, y=.58)])
beat([110, "Va"], "scene", bg="bg_diamond_stage", crop="left", ev=[L([110, "saboq"], "ENG KATTA SABOQ"), T([110, "hikoya"], "HIKOYA UCHUN TO'LAYMIZ", True)])
# ---------------- Javob ----------------
beat([111, "Xo'sh"], "title", title="JAVOB", title2="NEGA TOSH UYDAN QIMMAT?")
beat([112, "Chunki"], "object", ev=[M([112, "Chunki"], 1), {"at": [112, "odamlar"], "k": "bigtext", "text": "ODAMLAR BELGILAGAN", "x": .33, "y": .3}, T([112, "tabiat"], "TABIAT EMAS", x=.36, y=.55)])
beat([113, "Bir"], "scene", bg="bg_vault_release", crop="left", ev=[T([113, "taklifni"], "1. TAKLIF NAZORATI"), T([113, "talabni"], "2. REKLAMA = TALAB", True)])
beat([114, "degan"], "scene", bg="bg_ad_poster", crop="left", tagpos=[.28, .1], ev=[T([114, "to'rtta"], "3. \"OLMOS ABADIYDIR\"", True), T([114, "an'analarini"], "DUNYO AN'ANALARI O'ZGARDI")])
beat([115, "Bugun"], "scene", bg="bg_lab_diamond", crop="left", ev=[T([115, "laboratoriya"], "4. LABORATORIYA SINOVI", True)])
beat([116, "Olmoslar"], "title", title="OLMOSLAR HAQIDA MEN HAM BILMAS EDIM", title2="ENDI ESA HAMMAMIZ BILAMIZ")
beat([118, "Ana"], "object", ev=[M([118, "Ana"], 4), T([118, "shartmi"], "OLMOS UZUK SHARTMI...", x=.36, y=.38),
     T([118, "reklama"], "...YOKI REKLAMA ODATIMI?", True, x=.36, y=.55), T([119, "izohlarda"], "IZOHDA YOZING", x=.36, y=.72),
     {"at": [118, "sizningcha"], "k": "like", "x": .82, "y": .2}])
beat([120, "Keyingi"], "scene", bg="bg_inflation", mood="curious", ev=[L([120, "Keyingi"], "KEYINGI QISM"), T([120, "narxlar"], "NEGA NARXLAR OSHADI?"), T([120, "so'mimizning"], "SO'MNING QADRI", True)])
beat([121, "Gap"], "object", ev=[M([121, "Gap"], 2), {"at": [121, "inflyatsiya"], "k": "bigtext", "text": "INFLYATSIYA", "x": .33, "y": .45}])
beat([122, "O'tkazib"], "end", pose=1, ev=[{"at": [122, "obuna"], "k": "subscribe", "x": .47, "y": .35, "dur": 3.4}])

# Shorts framing per beat (chosen by eye from the raw pictures): vfocus = x centre, or [from, to] to pan between
# two subjects; vzoom > 1 = medium shot (wider window, blurred bands above and below).
VF = {
    (0, "Bir"): {'vfocus': 0.52, 'vzoom': 1.7},
    (3, "Oradan"): {'vfocus': [0.3, 0.7]},
    (5, "Ba'zi"): {'vfocus': 0.55, 'vzoom': 1.8},
    (8, "Va"): {'vfocus': 0.55, 'vzoom': 1.8},
    (25, "U"): {'vfocus': [0.27, 0.7]},
    (27, "Yigirma"): {'vfocus': 0.5, 'vzoom': 2.0},
    (29, "Keyinroq"): {'vfocus': 0.6, 'vzoom': 1.8},
    (30, "Ularning"): {'vfocus': 0.6, 'vzoom': 1.6},
    (32, "Lekin"): {'vfocus': 0.45, 'vzoom': 2.0},
    (39, "Amerikadagi"): {'vfocus': 0.62, 'vzoom': 1.8},
    (41, "U"): {'vfocus': 0.5, 'vzoom': 2.0},
    (42, "U"): {'vfocus': 0.5, 'vzoom': 1.8},
    (43, "Gazetalarga"): {'vfocus': 0.32},
    (44, "Maktablarga"): {'vfocus': 0.45, 'vzoom': 1.8},
    (47, "Bu"): {'vfocus': 0.53, 'vzoom': 1.6},
    (49, "Bu"): {'vfocus': 0.33, 'vzoom': 1.2},
    (52, "Ikkinchisi"): {'vfocus': 0.33, 'vzoom': 1.2},
    (54, "Nega"): {'vfocus': 0.55, 'vzoom': 1.6},
    (55, "Chunki"): {'vfocus': [0.3, 0.8]},
    (57, "Natija"): {'vfocus': 0.45, 'vzoom': 1.8},
    (62, "Aslida"): {'vfocus': 0.48},
    (64, "Keyin"): {'vfocus': 0.65, 'vzoom': 1.4},
    (66, "1981-yilga"): {'vfocus': [0.35, 0.75]},
    (67, "Ya'ni"): {'vfocus': 0.32},
    (74, "1990-yillarda"): {'vfocus': [0.25, 0.75]},
    (75, "Qurolli"): {'vfocus': [0.3, 0.75]},
    (77, "2000-yilda"): {'vfocus': 0.5, 'vzoom': 2.0},
    (78, "Bu"): {'vfocus': 0.5, 'vzoom': 1.8},
    (79, "Lekin"): {'vfocus': 0.5, 'vzoom': 1.8},
    (82, "2024-yil"): {'vfocus': 0.6, 'vzoom': 1.8},
    (83, "O'tgan"): {'vfocus': 0.55, 'vzoom': 1.6},
    (85, "U"): {'vfocus': 0.65, 'vzoom': 1.3},
    (87, "Ko'p"): {'vfocus': 0.45, 'vzoom': 1.2},
    (88, "Va"): {'vfocus': 0.62},
    (89, "2025-yilda"): {'vfocus': 0.4, 'vzoom': 1.8},
    (90, "2019-yilda"): {'vfocus': 0.45, 'vzoom': 1.3},
    (91, "Ya'ni"): {'vfocus': 0.58, 'vzoom': 1.4},
    (92, "Bu"): {'vfocus': 0.4, 'vzoom': 1.4},
    (93, "uch"): {'vfocus': 0.6, 'vzoom': 1.4},
    (95, "Oxir-oqibatda"): {'vfocus': 0.45, 'vzoom': 1.4},
    (96, "2026-yil"): {'vfocus': 0.45, 'vzoom': 1.6},
    (98, "Shu"): {'vfocus': 0.5, 'vzoom': 1.8},
}
for _d in B:
    if _d['type'] in ('scene', 'portrait', 'map'):
        _d.update(VF.get(tuple(_d['at']), {}))

cfg = {"layers": "layers", "auto_skip": ["Birs", "Beers"], "music": {"curious": "../../assets/music/curious.mp3", "dramatic": "../../assets/music/dramatic.mp3", "calm": "../../assets/music/calm.mp3"},
       "mascot": {"img": "mascot_v2", "parts": 4, "full_body": True,
                  "more": [{"img": f"mascot_v3{s_}_{i_}", "parts": 1} for s_ in "ab" for i_ in range(4)]},
       "ui": {"subscribe": "OBUNA BO'LING", "subscribed": "OBUNA BO'LDINGIZ", "like": "LAYK", "next": "KEYINGI VIDEO"},
       "sentences": S, "beats": B,
       "shorts": [{"name": "hook", "from": [0, "Bir"], "to": [8, "Va"], "hook": ""},
                  {"name": "cartel", "from": [24, "Shu"], "to": [32, "Lekin"], "hook": "BITTA KOMPANIYA, 90% OLMOS"},
                  {"name": "ad", "from": [39, "1938-yilda"], "to": [46, "1947-yilda"], "hook": "MAHSULOTSIZ REKLAMA"},
                  {"name": "forever", "from": [46, "1947-yilda"], "to": [57, "Natija"], "hook": "DUNYONI O'ZGARTIRGAN 4 SO'Z"},
                  {"name": "japan", "from": [61, "Keyin"], "to": [68, "Endi"], "hook": "YANGI AN'ANA 20 YILDA"},
                  {"name": "blood", "from": [74, "1990-yillarda"], "to": [84, "Endi"], "hook": "QONLI OLMOSLAR"},
                  {"name": "lab", "from": [85, "U"], "to": [98, "Shu"], "hook": "OLMOS BOZORI QULAYAPTIMI?"}],
       "end_hold": 9, "pauses": {"37": 1.2, "39": 1.1}, "end_slots": 2, "end_next": "INFLYATSIYA", "series_label": "4-QISM: OLMOSLAR", "partners": "Hamkorlarimiz: californiauzbek.com va bysmillah.com loyihalari.",
       "partner_logos": [{"img": "assets/partners/californiauzbek.png", "anim": "assets/partners/californiauzbek_anim.webm", "site": "californiauzbek.com"},
                         {"img": "assets/partners/bysmillah.png", "anim": "assets/partners/bysmillah_anim.mp4", "loop": True, "site": "bysmillah.com", "round": True}], "handle": "@bilmasboy",
       "socials": [["youtube", "@bilmasboy"], ["instagram", "@bilmas.boy"], ["tiktok", "@bilmas.boy"], ["facebook", "@bilmas.boy"], ["telegram", "@bilmas_boy"]]}
json.dump(cfg, open("ep04_beats.json", "w"), ensure_ascii=False, indent=1)
print(len(B), "beats")
