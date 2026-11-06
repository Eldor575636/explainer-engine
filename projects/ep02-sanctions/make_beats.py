"""Builds ep02_beats.json (Sanctions) from ep02_sentences.json + this beat plan.
New pictures are in layers/ (Higgsfield, 2026-11-06); the rest are reused from E01."""
import json
S = json.load(open("ep02_sentences.json", encoding="utf-8"))["sentences"]
# map_world coordinates (same map as E01)
US, DC, UK, FR, BE, DE, GR, IT, ET, CU, UA, MOS, IRN, CN, IN, ZA, TAS, SG, TR, KZ, AM = (
    (.22, .37), (.27, .38), (.475, .29), (.49, .33), (.485, .30), (.51, .30), (.53, .37), (.505, .35), (.58, .55),
    (.26, .47), (.555, .30), (.57, .27), (.63, .43), (.76, .40), (.69, .50), (.535, .76), (.65, .38), (.765, .58),
    (.56, .37), (.66, .33), (.6, .36))
def L(at, t): return {"at": at, "k": "label", "text": t}
def T(at, t, red=False, **kw):
    d = {"at": at, "k": "tag", "text": t}; d.update(kw)
    if red: d["fg"] = "red"
    return d
def ST(at, t): return {"at": at, "k": "stamp", "text": t}
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
SS = "prop_sanction_sheet"   # parts: 0 card with red X, 1 frozen card, 2 black dossier, 3 cut phone
SH = "prop_sheet2"           # parts: 0 barrel, 1 bond, 2 scale, 3 yuan
B = []
def beat(at, typ, **kw):
    d = {"at": at, "type": typ}; d.update(kw); B.append(d)

# ---------------- Hook ----------------
beat([0, "Tasavvur"], "scene", bg="bg_samarkand_bank", mood="curious",
     ev=[L([0, "2022-yil"], "2022 · SENTABR"), F([1, "Samarqanddagi"], "uz"), T([1, "Samarqanddagi"], "SAMARQAND"),
         T([1, "Rossiyada"], "O'G'LI ROSSIYADA ISHLAYDI"), C([3, "ishlamadi"], .44, .45, .07, .1)])
beat([2, "O'g'li"], "object", props=[P([2, "Mir"], "prop_card_x", .3, .5, .42)],
     ev=[T([2, "Mir"], "\"MIR\" KARTASI", x=.3, y=.82), ST([3, "ishlamadi"], "ISHLAMADI"), T([4, "Ertasiga"], "ERTASIGA HAM...", True, x=.7, y=.4),
         T([5, "to'xtatilgan"], "XIZMAT TO'XTATILDI", x=.7, y=.58)])
beat([6, "Hech"], "scene", bg="bg_war", tint=.55, mood="dramatic",
     ev=[T([6, "o'q"], "O'Q UZILMADI"), T([6, "armiya"], "ARMIYA KIRMADI", True)])
beat([7, "Lekin"], "map", bg="map_world", zf=[.6, .4],
     ev=[AR([7, "minglab"], DC, TAS), AR([7, "qarorlar"], BE, TAS), PIN([7, "oilaning"], TAS), RG([7, "hamyoniga"], TAS)])
beat([8, "Bu"], "title", title="BU QUROLNING NOMI", title2="SANKSIYA")
beat([9, "Bugun"], "object", props=[P([9, "odamlar"], "prop_dossier", .2, .5, .36), P([9, "kompaniyalar"], "prop_card_frozen", .5, .5, .36),
     P([9, "davlatlarga"], "prop_phone_cut", .8, .5, .36)],
     ev=[F([9, "Amerika"], ["us", "eu"], x=.5, y=.18), T([9, "odamlar"], "ODAMLAR", x=.2, y=.8), T([9, "kompaniyalar"], "KOMPANIYALAR", x=.5, y=.8),
         T([9, "davlatlarga"], "DAVLATLAR", True, x=.8, y=.8)])
beat([10, "Xo'sh"], "object", ev=[M([10, "Xo'sh"], 0), T([10, "qanday"], "QANDAY ISHLAYDI?", x=.36, y=.4), T([11, "haqiqatan"], "ISHLAYDIMI O'ZI?", True, x=.36, y=.58)])
# ---------------- Intro ----------------
beat([12, "Mening"], "intro", pose=3)
beat([13, "Bilganlarim"], "object", ev=[M([13, "Bilganlarim"], 3), T([13, "Bilganlarim"], "BILIM = BOYLIK", x=.32, y=.3),
     T([13, "savollar"], "SO'RAYMAN", x=.32, y=.45), T([13, "izlanaman"], "IZLANAMAN", x=.32, y=.58), T([14, "ulashib"], "ULASHAMAN", True, x=.32, y=.71)])
beat([15, "O'tgan"], "object", props=[P([15, "dollar"], "prop_dollar", .3, .5, .5)],
     ev=[L([15, "O'tgan"], "1-QISM: DOLLAR"), AR([16, "kuch"], (.43, .5), (.66, .5), True),
         PR([16, "ishlatilishini"], "prop_phone_cut", .78, .5, .4)])
beat([17, "Demak"], "title", title="BUGUNGI MAVZU", title2="SANKSIYALAR")
# ---------------- 1-qism: tarix ----------------
beat([18, "Sanksiya"], "chapter", num="1-QISM", title="ESKI QUROL")
beat([19, "Miloddan"], "scene", bg="bg_ancient_harbor", mood="curious",
     ev=[L([19, "432-yilda"], "MIL. AVV. 432"), F([19, "Afina"], "gr"), T([19, "Afina"], "AFINA"), T([19, "Megara"], "MEGARA SAVDOGARLARI", True),
         ST([19, "yopib"], "YOPIQ"), T([20, "ilk"], "ILK SANKSIYALARDAN BIRI")])
beat([21, "Megara"], "map", bg="map_world", zf=[.53, .37], ev=[PIN([21, "Megara"], GR), RG([21, "qiynaldi"], GR), T([21, "taslim"], "TASLIM BO'LMADI", x=.5, y=.82)])
beat([22, "Aksincha"], "scene", bg="bg_war", mood="dramatic", ev=[T([22, "urush"], "KATTA URUSH"), T([23, "o'rnini"], "URUSH O'RNIGA...", x=.3, y=.3),
     ST([23, "urushga"], "URUSHGA OLIB KELDI")])
beat([24, "Yana"], "scene", bg="bg_ethiopia_1935", mood="dramatic",
     ev=[L([24, "yigirmanchi"], "XX ASR"), L([25, "1935-yilda"], "1935"), F([25, "Italiya"], "it"), F([25, "Efiopiyaga"], ["it", "et"]),
         T([25, "bostirib"], "ITALIYA BOSTIRIB KIRDI", True)])
beat([26, "O'sha"], "scene", bg="bg_league_nations", ev=[L([26, "Millatlar"], "MILLATLAR LIGASI"), T([26, "sanksiya"], "ITALIYAGA SANKSIYA")])
beat([27, "Lekin"], "object", props=[P([27, "neft"], SH, .5, .5, .5, part=0, nparts=4)],
     ev=[L([27, "muhim"], "ENG MUHIM MAHSULOT"), T([27, "neft"], "NEFT", x=.5, y=.82), ST([27, "kiritilmadi"], "RO'YXATDA YO'Q")])
beat([28, "Italiya"], "scene", bg="bg_ethiopia_1935", crop="right", ev=[T([28, "davom"], "URUSH DAVOM ETDI"), ST([28, "bekor"], "BEKOR QILINDI")])
beat([29, "Saboq"], "object", ev=[M([29, "Saboq"], 1), L([29, "Saboq"], "SABOQ"), T([29, "og'riydigan"], "OG'RIYDIGAN JOYGA TEGSA", x=.36, y=.45),
     T([29, "natija"], "NATIJA BERADI", True, x=.36, y=.6)])
# ---------------- 2-qism: turlari ----------------
beat([30, "Xo'sh"], "chapter", num="2-QISM", title="SANKSIYA NIMA?")
beat([31, "Oddiy"], "object", ev=[{"at": [31, "siz"], "k": "bigtext", "text": "X", "x": .5, "y": .45}, L([31, "ishlamaymiz"], "\"SIZ BILAN ISHLAMAYMIZ\""),
     T([32, "turi"], "4 TURI", x=.5, y=.8)])
beat([33, "Birinchisi"], "scene", bg="bg_havana", mood="curious",
     ev=[L([33, "Birinchisi"], "1. SAVDO EMBARGOSI"), T([34, "savdo"], "BUTUN DAVLAT BILAN SAVDO YO'Q"), F([35, "Kuba"], "cu"), T([35, "Kuba"], "KUBA"),
         F([36, "Amerika"], ["us", "cu"]), {"at": [36, "1962-yilda"], "k": "counter", "from": 1962, "to": 2026, "x": .5, "y": .5}, T([36, "hozirgacha"], "HALI HAM DAVOM ETMOQDA", True)])
beat([37, "Ikkinchisi"], "object", props=[P([37, "Ikkinchisi"], "prop_card_frozen", .3, .5, .46)],
     ev=[L([37, "Ikkinchisi"], "2. SHAXSIY SANKSIYALAR"), T([38, "muzlatiladi"], "PULLARI MUZLATILADI", x=.7, y=.42), T([38, "chiqa"], "CHET ELGA CHIQA OLMAYDI", True, x=.7, y=.6)])
beat([39, "Uchinchisi"], "scene", bg="bg_bank_network",
     ev=[L([39, "Uchinchisi"], "3. MOLIYAVIY SANKSIYALAR"), T([40, "uzib"], "XALQARO TIZIMDAN UZILADI", True)])
beat([41, "To'rtinchisi"], "object", ev=[L([41, "To'rtinchisi"], "4. IKKILAMCHI SANKSIYALAR"), ST([41, "kuchlisi"], "ENG KUCHLISI"),
     T([42, "Agar"], "SIZ ULAR BILAN ISHLASANGIZ...", x=.5, y=.55), T([42, "biz"], "...BIZ SIZ BILAN ISHLAMAYMIZ", True, x=.5, y=.7)])
beat([43, "Aynan"], "scene", bg="bg_bank_network", crop="left", ev=[T([43, "banklarini"], "DUNYO BANKLARI QO'RQADI", True)])
# ---------------- Nega Amerika kuchli ----------------
beat([44, "Nega"], "object", ev=[M([44, "Nega"], 0), T([44, "kuchli"], "NEGA AMERIKA?", x=.36, y=.4), F([44, "Amerika"], "us", x=.36, y=.2)])
beat([45, "Javob"], "object", props=[P([45, "dollar"], "prop_dollar", .5, .48, .6, slam=True)], ev=[L([45, "Javob"], "JAVOB: DOLLAR")])
beat([46, "Dunyodagi"], "number", prop="prop_dollar", value="9/10", sub="VALYUTA BITIMLARIDA DOLLAR BOR", show=[46, "9"])
beat([47, "Dollar"], "map", bg="map_world", zf=[.4, .4],
     ev=[AR([47, "o'tkazmalari"], TAS, DC), AR([47, "Amerika"], FR, DC), AR([47, "banklari"], CN, DC), PIN([47, "orqali"], DC), L([47, "orqali"], "AMERIKA BANKLARI ORQALI")])
beat([48, "Demak"], "object", ev=[T([48, "ishlamang"], "\"BU ODAM BILAN ISHLAMANG\"", x=.5, y=.35), T([48, "majbur"], "BANKLAR TINGLAYDI", True, x=.5, y=.55),
     T([49, "uzilib"], "AKS HOLDA: TIZIMDAN UZILADI", x=.5, y=.72)])
beat([50, "Bu"], "scene", bg="bg_treasury", mood="curious",
     ev=[F([50, "Vashingtondagi"], "us"), L([50, "Vashingtondagi"], "VASHINGTON"), T([50, "Moliya"], "MOLIYA VAZIRLIGI"), ST([50, "OFAK"], "OFAK"),
         L([51, "1950-yilda"], "1950 · KOREYA URUSHI")])
beat([52, "Bugun"], "scene", bg="bg_treasury", crop="left",
     ev=[L([52, "ro'yxatida"], "QORA RO'YXAT"), T([52, "odamlar"], "ODAMLAR"), T([52, "kompaniyalar"], "KOMPANIYALAR"), T([52, "kemalar"], "KEMALAR"), T([52, "samolyotlar"], "SAMOLYOTLAR", True)])
beat([53, "Bu"], "object", props=[P([54, "kartasi"], "prop_card_x", .2, .5, .36), P([54, "muzlaydi"], "prop_card_frozen", .5, .5, .36),
     P([54, "aloqa"], "prop_phone_cut", .8, .5, .36)],
     ev=[L([53, "kichrayib"], "DUNYO KICHRAYADI"), T([54, "kartasi"], "KARTA ISHLAMAYDI", x=.2, y=.8), T([54, "muzlaydi"], "HISOB MUZLAYDI", x=.5, y=.8),
         T([54, "aloqa"], "BANKLAR YO'Q", True, x=.8, y=.8)])
beat([55, "Sanksiya"], "scene", bg="bg_fed", ev=[L([55, "qo'yiladi"], "QANDAY QO'YILADI?"), F([56, "Amerikada"], "us"), T([56, "Prezident"], "PREZIDENT FARMONI"),
     T([56, "OFAK"], "OFAK: RO'YXAT")])
beat([57, "Yevropa"], "map", bg="map_world", zf=[.5, .3],
     ev=[F([57, "Yevropa"], "eu"), RG([57, "Ittifoqida"], BE), {"at": [57, "27"], "k": "counter", "to": 27, "suffix": " DAVLAT ROZI", "x": .5, "y": .8},
         T([58, "sekinroq"], "SEKIN QABUL QILINADI", x=.5, y=.2), ST([58, "yopadi"], "BOZOR YOPILADI")])
beat([59, "Bir"], "object", ev=[M([59, "Bir"], 1), {"at": [59, "obuna"], "k": "subscribe", "x": .36, "y": .5, "dur": 3.4}])
# ---------------- 3-qism: Eron ----------------
beat([61, "Sanksiya"], "chapter", num="3-QISM", title="ERON")
beat([62, "2012-yil"], "scene", bg="bg_bank_network", mood="dramatic",
     ev=[L([62, "2012-yil"], "2012 · MART"), F([62, "Eronning"], "ir"), {"at": [62, "o'ttizga"], "k": "counter", "to": 30, "prefix": "~", "suffix": " BANK", "x": .5, "y": .78},
         T([62, "markaziy"], "MARKAZIY BANK HAM"), ST([62, "uzib"], "SWIFT'DAN UZILDI")])
beat([63, "SWIFT"], "object", props=[P([63, "SWIFT"], "prop_phone_cut", .5, .5, .55)],
     ev=[L([63, "SWIFT"], "SWIFT = BANKLAR XABAR TIZIMI"), T([64, "pul"], "PUL BOR...", x=.25, y=.75), T([64, "yubora"], "...YUBORIB BO'LMAYDI", True, x=.75, y=.75)])
beat([65, "Eron"], "scene", bg="bg_oil_field", ev=[F([65, "Eron"], "ir"), L([65, "neftini"], "ERON NEFTI"),
     {"at": [65, "yarmiga"], "k": "bars", "novalue": True, "x": .5, "w": .4, "items": [{"label": "OLDIN", "value": 100}, {"label": "KEYIN", "value": 50, "color": "red", "hl": True}]}])
beat([66, "Eron"], "scene", bg="bg_tehran_exchange", ev=[L([66, "riyol"], "ERON RIYOLI"), T([66, "qadrsizlandi"], "KESKIN QADRSIZLANDI", True), T([66, "narxlar"], "NARXLAR OSHDI")])
beat([67, "Va"], "scene", bg="bg_conference", ev=[L([67, "2015-yilda"], "2015 · YADRO KELISHUVI"), F([67, "Eron"], "ir"), ST([68, "muvaffaqiyati"], "MUVAFFAQIYAT?")])
beat([69, "Lekin"], "object", ev=[M([69, "Lekin"], 2), L([70, "2018-yilda"], "2018"), F([70, "Amerika"], "us", x=.36, y=.25), T([70, "chiqdi"], "AMERIKA KELISHUVDAN CHIQDI", x=.36, y=.45),
     T([70, "qaytdi"], "SANKSIYALAR QAYTDI", True, x=.36, y=.6)])
beat([71, "Ya'ni"], "object", ev=[T([71, "muzokara"], "MUZOKARAGA OLIB KELDI", x=.5, y=.4), T([71, "hal"], "MUAMMONI HAL QILMADI", True, x=.5, y=.6)])
# ---------------- 4-qism: Rossiya ----------------
beat([72, "Endi"], "chapter", num="4-QISM", title="ROSSIYA")
beat([73, "2022-yil"], "map", bg="map_world", zf=[.56, .3], ev=[L([73, "2022-yil"], "2022 · FEVRAL"), F([73, "Rossiya"], "ru"), PIN([73, "Ukrainaga"], UA),
     RG([73, "Ukrainaga"], UA), T([73, "eng"], "TARIXDAGI ENG KATTA SANKSIYALAR", x=.5, y=.82)])
beat([74, "Rossiya"], "scene", bg="bg_moscow_vault", mood="dramatic",
     ev=[F([74, "Rossiya"], "ru"), L([74, "markaziy"], "MARKAZIY BANK ZAXIRASI"), {"at": [74, "300"], "k": "counter", "to": 300, "prefix": "$", "suffix": " MLRD", "x": .5, "y": .3},
         ST([74, "muzlatildi"], "MUZLATILDI"), T([75, "yarmi"], "ZAXIRANING YARMI", True)])
beat([76, "Eng"], "object", props=[P([76, "SWIFT"], "prop_phone_cut", .25, .5, .42), P([77, "Visa"], "prop_card_x", .75, .5, .42)],
     ev=[T([76, "SWIFT"], "SWIFT'DAN UZILDI", x=.25, y=.82), T([77, "Visa"], "VISA VA MASTERCARD KETDI", True, x=.75, y=.82)])
beat([78, "Yevropa"], "scene", bg="bg_oil_field", ev=[F([78, "Yevropa"], "eu"), T([78, "to'xtatdi"], "YEVROPA NEFT OLMAYDI"), PR([78, "chegara"], SH, .8, .55, .35, part=0, nparts=4),
     T([78, "chegara"], "NARX CHEGARASI", True)])
beat([79, "Ko'pchilik"], "object", ev=[M([79, "Ko'pchilik"], 2), T([79, "qulaydi"], "BIR NECHA OYDA QULAYDI?", x=.36, y=.4), ST([80, "bunday"], "YO'Q")])
beat([81, "Rossiya"], "map", bg="map_world", zf=[.66, .36], ev=[AR([81, "Xitoy"], MOS, CN), F([81, "Xitoy"], "cn"), AR([81, "Hindistonga"], MOS, IN), F([81, "Hindistonga"], ["cn", "in"])])
beat([82, "To'lovlar"], "scene", bg="bg_china_port", ev=[T([82, "yo'llar"], "BOSHQA YO'LLAR"), T([82, "valyutalar"], "BOSHQA VALYUTALAR"), T([82, "vositachi"], "VOSITACHI DAVLATLAR", True),
     T([83, "qulamadi"], "QIYNALDI, LEKIN QULAMADI")])
beat([84, "Muzlatilgan"], "scene", bg="bg_brussels_vault", mood="curious",
     ev=[F([85, "Belgiyadagi"], "be"), L([85, "Euroclear"], "EUROCLEAR · BELGIYA"), {"at": [85, "200"], "k": "counter", "to": 200, "prefix": "€", "suffix": " MLRD", "x": .5, "y": .3},
         T([86, "sud"], "SUD JANJALLARI DAVOM ETMOQDA", True)])
beat([87, "Aytgancha"], "object", ev=[M([87, "Aytgancha"], 1), {"at": [87, "layk"], "k": "like", "x": .36, "y": .45}])
# ---------------- 5-qism: ishlaydimi ----------------
beat([89, "Xo'sh"], "chapter", num="5-QISM", title="ISHLAYDIMI?")
beat([90, "Olimlar"], "object", ev=[L([90, "yuzlab"], "YUZLAB HOLAT O'RGANILGAN"),
     {"at": [91, "uchtadan"], "k": "pie", "x": .35, "y": .55, "r": .25, "slices": [{"label": "MAQSADGA ERISHGAN", "value": 33}, {"label": "ERISHMAGAN", "value": 67}]}])
beat([92, "Ular"], "object", ev=[L([92, "ishlaydi"], "QACHON ISHLAYDI?"), T([92, "aniq"], "1. MAQSAD KICHIK VA ANIQ", x=.5, y=.4), T([92, "davlat"], "2. DAVLAT KICHIK", x=.5, y=.55),
     T([92, "boshqa"], "3. BOSHQA YO'L YO'Q", x=.5, y=.7)])
beat([93, "Masalan"], "scene", bg="bg_south_africa", ev=[F([93, "Janubiy"], "za"), L([93, "aparteid"], "JANUBIY AFRIKA · APARTEID"), T([93, "muhim"], "SANKSIYA YORDAM BERGAN")])
beat([94, "Kuba"], "scene", bg="bg_havana", crop="right", ev=[F([94, "Kuba"], "cu"), {"at": [94, "oltmish"], "k": "counter", "to": 60, "suffix": "+ YIL", "x": .5, "y": .3},
     ST([94, "o'zgarmadi"], "O'ZGARMADI")])
beat([95, "Sanksiyalarning"], "scene", bg="bg_shortage", mood="dramatic",
     ev=[T([96, "hokimiyatdagilar"], "HOKIMIYAT EMAS..."), T([96, "oddiy"], "...ODDIY ODAMLAR", True), T([97, "Narxlar"], "NARXLAR ↑"), T([97, "dori-darmon"], "DORI YO'Q"),
         ST([97, "qora"], "QORA BOZOR")])
beat([98, "Va"], "map", bg="map_world", zf=[.6, .38], ev=[L([98, "dollarsiz"], "DOLLARSIZ YO'LLAR"), F([99, "Xitoy"], ["cn", "ru"]), RG([99, "Xitoy"], CN), RG([99, "Rossiya"], MOS),
     T([99, "to'lov"], "O'Z TO'LOV TIZIMLARI", x=.5, y=.82)])
beat([100, "Ya'ni"], "object", props=[P([100, "dollar"], "prop_dollar", .5, .5, .5)],
     ev=[T([100, "ko'p"], "KUCHNI KO'P ISHLATSA...", x=.5, y=.2), T([100, "qochish"], "...DUNYO QOCHADI", True, x=.5, y=.82)])
# ---------------- 6-qism: O'zbekiston ----------------
beat([101, "Endi"], "chapter", num="6-QISM", title="O'ZBEKISTON")
beat([102, "O'zbekistonga"], "scene", bg="bg_tashkent_exchange", ev=[F([102, "O'zbekistonga"], "uz"), T([102, "qo'yilmagan"], "SANKSIYA YO'Q"),
     T([103, "ta'sir"], "LEKIN TA'SIRI BOR", True)])
beat([104, "2022-yil"], "scene", bg="bg_samarkand_bank", ev=[L([104, "2022-yil"], "23-SENTABR 2022"), T([104, "Mir"], "\"MIR\" TO'XTATILDI"), T([105, "texnik"], "RASMIY SABAB: \"TEXNIK\"", True)])
beat([106, "Lekin"], "map", bg="map_world", zf=[.6, .36], ev=[F([106, "Turkiya"], "tr"), PIN([106, "Turkiya"], TR), F([106, "Qozog'iston"], ["tr", "kz"]), PIN([106, "Qozog'iston"], KZ),
     F([106, "Armaniston"], ["tr", "kz", "am"]), PIN([106, "Armaniston"], AM), T([106, "ikkilamchi"], "IKKILAMCHI SANKSIYA QO'RQUVI", x=.5, y=.82)])
beat([107, "Bundan"], "scene", bg="bg_treasury", crop="left", ev=[F([107, "O'zbekistonda"], ["us", "uz"]), T([107, "kompaniyani"], "O'ZBEK KOMPANIYALARI"), ST([107, "ro'yxatiga"], "QORA RO'YXAT")])
beat([108, "Shuning"], "scene", bg="bg_bank_network", crop="right", ev=[T([108, "ehtiyotkorlik"], "BANKLAR EHTIYOTKOR", True)])
beat([109, "Esingizda"], "scene", bg="bg_migrant_work", ev=[F([109, "Rossiyadan"], "ru"),
     {"at": [109, "to'rtdan"], "k": "pie", "x": .56, "y": .55, "r": .2, "slices": [{"label": "ROSSIYADAN", "value": 75}, {"label": "BOSHQA", "value": 25}]}])
beat([110, "Demak"], "map", bg="map_world", zf=[.45, .33], ev=[AR([110, "Vashington"], DC, TAS), AR([110, "Bryusseldagi"], BE, TAS), PIN([110, "Toshkent"], TAS),
     T([110, "hamyoniga"], "SIZNING HAMYONINGIZ", True, x=.5, y=.82)])
# ---------------- Javob ----------------
beat([111, "Xo'sh"], "title", title="JAVOB", title2="SANKSIYALAR QANDAY ISHLAYDI?")
beat([113, "Ular"], "object", props=[P([113, "dollar"], "prop_dollar", .3, .5, .45)], ev=[T([113, "bank"], "DOLLAR + BANK TIZIMI", x=.7, y=.4),
     T([113, "majbur"], "MUHTOJ BO'LSANG, BO'YSUNASAN", True, x=.7, y=.58)])
beat([114, "Ular"], "object", ev=[M([114, "Ular"], 1), {"at": [115, "Ba'zan"], "k": "bigtext", "text": "BA'ZAN", "x": .36, "y": .45},
     T([116, "qiynashi"], "QIYNAYDI", x=.36, y=.62), T([116, "kamdan-kam"], "SIYOSATNI KAMDAN-KAM O'ZGARTIRADI", True, x=.36, y=.75)])
beat([117, "Va"], "map", bg="map_world", zf=[.5, .45], ev=[PR([117, "dollarsiz"], "prop_dollar", .5, .5, .3), C([117, "dollarsiz"], .5, .5, .2, .24), L([117, "yo'llar"], "DOLLARSIZ YO'LLAR")])
beat([118, "Sanksiyalar"], "title", title="SANKSIYALAR HAQIDA MEN HAM BILMAS EDIM", title2="ENDI ESA HAMMAMIZ BILAMIZ")
beat([120, "Ana"], "object", ev=[M([120, "Ana"], 0), T([120, "adolatli"], "ADOLATLI QUROLMI?", x=.36, y=.38), T([120, "jazolaydimi"], "YOKI ODDIY ODAMLARNI JAZOLAYDIMI?", True, x=.36, y=.55),
     T([121, "izohlarda"], "IZOHDA YOZING", x=.36, y=.72)])
beat([122, "Keyingi"], "scene", bg="bg_singapore", mood="curious", ev=[L([122, "Keyingi"], "KEYINGI QISM"), F([123, "Singapur"], "sg"), T([123, "Singapur"], "SINGAPUR"),
     T([123, "Li"], "LI KUAN YU", True)])
beat([124, "O'tkazib"], "end", pose=1, ev=[{"at": [124, "obuna"], "k": "subscribe", "x": .5, "y": .11, "dur": 3.4}, T([125, "Bilmasboy"], "BILMASBOY", True, x=.5, y=.9)])

cfg = {"layers": "layers", "music": {"curious": "../../assets/music/curious.mp3", "dramatic": "../../assets/music/dramatic.mp3", "calm": "../../assets/music/calm.mp3"},
       "mascot": {"img": "mascot_v2", "parts": 4, "full_body": True},
       "ui": {"subscribe": "OBUNA BO'LING", "subscribed": "OBUNA BO'LDINGIZ", "like": "LAYK", "next": "KEYINGI VIDEO"},
       "sentences": S, "beats": B,
       "shorts": [{"name": "hook", "from": [0, "Tasavvur"], "to": [11, "Va"], "hook": ""},
                  {"name": "types", "from": [30, "Xo'sh"], "to": [43, "Aynan"], "hook": "SANKSIYANING 4 TURI"},
                  {"name": "ofac", "from": [44, "Nega"], "to": [54, "Uning"], "hook": "NEGA AMERIKA SANKSIYASI BUNCHALIK KUCHLI?"},
                  {"name": "russia", "from": [72, "Endi"], "to": [86, "Ular"], "hook": "300 MLRD DOLLAR QANDAY MUZLATILDI?"},
                  {"name": "uzbekistan", "from": [101, "Endi"], "to": [110, "Demak"], "hook": "SANKSIYA O'ZBEKISTONGA QANDAY TA'SIR QILADI?"}],
       "series_label": "2-QISM: SANKSIYALAR", "handle": "@bilmasboy",
       "socials": [["youtube", "@bilmasboy"], ["instagram", "@bilmas.boy"], ["tiktok", "@bilmas.boy"], ["facebook", "@bilmas.boy"], ["telegram", "@bilmas_boy"]]}
json.dump(cfg, open("ep02_beats.json", "w"), ensure_ascii=False, indent=1)
print(len(B), "beats")
