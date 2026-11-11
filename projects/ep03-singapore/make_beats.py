"""Builds ep03_beats.json (Singapore & Lee Kuan Yew) from ep03_sentences.json + this beat plan.
New pictures in layers/ (Higgsfield, 2026-11-10); bg_singapore, bg_ships, bg_china_port, bg_family_home,
bg_conference, bg_oil_field, bg_bank_network, bg_war, map_world, prop_dollar, prop_gold reused from E01/E02."""
import json
S = json.load(open("ep03_sentences.json", encoding="utf-8"))["sentences"]
# map_world coordinates (same map as E01/E02)
UK, SGW, JP, US, NL, TAS, KR, TW = (.475, .29), (.765, .58), (.85, .37), (.22, .37), (.49, .29), (.65, .38), (.82, .38), (.8, .45)
# map_malacca / map_central_asia coordinates
SGM, MYM, UZ = (.59, .71), (.47, .35), (.45, .55)
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
B = []
def beat(at, typ, **kw):
    d = {"at": at, "type": typ}; d.update(kw); B.append(d)

# ---------------- Hook ----------------
beat([0, "1965-yil"], "scene", bg="bg_tv_1965", mood="dramatic",
     ev=[L([0, "1965-yil"], "1965 · 9-AVGUST"), T([1, "televizorda"], "TELEVIZORDA MUROJAAT"), C([1, "yig'lab"], .41, .33, .1, .14),
         T([1, "yig'lab"], "RAHBAR YIG'LAYAPTI", True)])
beat([2, "Bu"], "scene", bg="bg_independence_1965", ev=[L([2, "mustaqil"], "MUSTAQILLIK KUNI"),
     T([3, "bayram"], "ODATDA: BAYRAM", x=.5, y=.72), ST([4, "xursand"], "XURSAND EMAS")])
beat([5, "Na"], "scene", bg="bg_oil_field", tint=.55,
     ev=[T([5, "neft"], "NEFT YO'Q", True, x=.25, y=.35), T([5, "gaz"], "GAZ YO'Q", True, x=.5, y=.35), T([5, "oltin"], "OLTIN YO'Q", True, x=.75, y=.35),
         ST([5, "suvi"], "SUV HAM YETMAYDI")])
beat([6, "Bu"], "map", bg="map_malacca", zf=[.59, .68], ev=[PIN([6, "orol"], SGM), RG([6, "kichik"], SGM),
     T([6, "Toshkent"], "MAYDONI ~2 TA TOSHKENT", x=.5, y=.85)])
beat([7, "Oradan"], "scene", bg="bg_singapore", mood="curious", ev=[T([7, "avlod"], "BIR AVLOD O'TIB..."), ST([7, "boy"], "ENG BOY DAVLATLARDAN")])
beat([8, "Bu"], "portrait", fig="lky_cut", vfocus=.2, ev=[F([8, "Singapur"], "sg"), L([8, "Singapur"], "SINGAPUR"), T([8, "Li"], "LI KUAN YU", True)])
beat([9, "Xo'sh"], "object", ev=[M([9, "Xo'sh"], 4), T([9, "resurssiz"], "RESURSSIZ OROL...", x=.36, y=.38), T([9, "boyib"], "QANDAY BOYIDI?", x=.36, y=.54),
     T([10, "narxi"], "NARXI QANCHA?", True, x=.36, y=.7)])
# ---------------- Intro ----------------
beat([11, "Mening"], "intro", pose=3)
beat([12, "Bilganlarim"], "object", ev=[M([12, "Bilganlarim"], 3), T([12, "Bilganlarim"], "BILIM = BOYLIK", x=.32, y=.3),
     T([12, "savollar"], "SO'RAYMAN", x=.32, y=.45), T([12, "izlanaman"], "IZLANAMAN", x=.32, y=.58), T([13, "ulashib"], "ULASHAMAN", True, x=.32, y=.71)])
beat([14, "O'tgan"], "object", props=[P([14, "sanksiyalar"], "prop_dollar", .3, .5, .45)],
     ev=[L([14, "O'tgan"], "2-QISM: SANKSIYALAR"), T([15, "yer"], "YER OSTIDAGI BOYLIK?", x=.7, y=.4), T([15, "qarorlar"], "YOKI TO'G'RI QARORLAR?", True, x=.7, y=.58)])
beat([16, "Demak"], "title", title="BUGUNGI MAVZU", title2="SINGAPUR VA LI KUAN YU")
# ---------------- 1-qism: tarix ----------------
beat([17, "Avval"], "chapter", num="1-QISM", title="OROL TARIXI")
beat([18, "Singapur"], "map", bg="map_malacca", zf=[.5, .5], ev=[L([18, "Malakka"], "MALAKKA BO'G'OZI"), PIN([18, "Singapur"], SGM),
     T([18, "Hind"], "HIND OKEANI", x=.15, y=.75), T([18, "Tinch"], "TINCH OKEANI", x=.85, y=.2), T([18, "yo'lining"], "DUNYO SAVDO YO'LI", True, x=.5, y=.9)])
beat([19, "1819-yilda"], "scene", bg="bg_port_1819", mood="curious", ev=[L([19, "1819-yilda"], "1819"), F([19, "inglizlar"], "gb"), T([19, "savdo"], "INGLIZ SAVDO PORTI")])
beat([20, "Deyarli"], "scene", bg="bg_port_1819", crop="right", ev=[CT([20, "bir"], 146, suffix=" YIL", x=.5, y=.3), T([20, "mustamlakasi"], "BRITANIYA MUSTAMLAKASI", True)])
beat([21, "Ikkinchi"], "scene", bg="bg_ww2", mood="dramatic", ev=[L([21, "Ikkinchi"], "1942 · IKKINCHI JAHON URUSHI"), F([21, "Yaponiya"], "jp"),
     ST([21, "bosib"], "BOSIB OLINDI")])
beat([22, "Urushdan"], "scene", bg="bg_ships", mood="calm", ev=[T([22, "port"], "PORT TIKLANDI"), T([22, "qashshoqlikda"], "LEKIN QASHSHOQLIK", True)])
beat([23, "Odamlar"], "scene", bg="bg_kampong", ev=[T([23, "gavjum"], "GAVJUM KULBALAR"), T([23, "suvsiz"], "SUVSIZ"), T([23, "kanalizatsiyasiz"], "KANALIZATSIYASIZ", True)])
beat([24, "Ishsizlik"], "scene", bg="bg_kampong", crop="left", ev=[T([24, "Ishsizlik"], "ISHSIZLIK YUQORI", True), T([24, "jinoiy"], "JINOIY GURUHLAR")])
beat([25, "1959-yilda"], "scene", bg="lky_rally_1959", ev=[L([25, "1959-yilda"], "1959"), T([25, "boshqarish"], "O'ZINI O'ZI BOSHQARISH"),
     T([25, "bosh"], "LI KUAN YU · BOSH VAZIR", True), T([26, "Kembrijda"], "KEMBRIJ · HUQUQSHUNOS"), CT([26, "o'ttiz"], 35, suffix=" YOSH", x=.15, y=.8)])
beat([27, "Uning"], "scene", bg="lky_desk", ev=[T([27, "yolg'iz"], "KICHIK OROL YOLG'IZ YASHAY OLMAYDI", True)])
beat([28, "Shuning"], "map", bg="map_malacca", zf=[.5, .45], ev=[L([28, "1963-yilda"], "1963"), F([28, "Malayziya"], ["sg", "my"]), AR([28, "qo'shildi"], SGM, MYM),
     T([28, "federatsiyasiga"], "MALAYZIYA FEDERATSIYASI", x=.5, y=.85)])
beat([29, "Lekin"], "scene", bg="bg_riots_1964", mood="dramatic", ev=[T([29, "davom"], "UZOQ DAVOM ETMADI"), T([30, "to'qnashuvlar"], "TO'QNASHUVLAR", True)])
beat([31, "Ikki"], "scene", bg="bg_parliament_1965", ev=[L([31, "Ikki"], "1965"), ST([31, "chiqarishga"], "CHIQARILDI")])
beat([32, "Ya'ni"], "object", ev=[M([32, "Ya'ni"], 5), T([32, "so'rab"], "MUSTAQILLIKNI SO'RAMAGAN", x=.36, y=.38),
     T([32, "majbur"], "MAJBUR QILISHGAN", True, x=.36, y=.55), T([33, "ko'z"], "KO'Z YOSHLARI SHUNDAN", x=.36, y=.72)])
beat([34, "Endi"], "scene", bg="bg_kampong", mood="calm", ev=[L([34, "tasavvur"], "1965-YILDAGI SINGAPUR"),
     CT([35, "ikki"], 2, suffix=" MLN AHOLI", x=.5, y=.25), T([35, "xitoylar"], "XITOYLAR"), T([35, "malaylar"], "MALAYLAR"), T([35, "hindlar"], "HINDLAR")])
beat([36, "Bir"], "scene", bg="bg_riots_1964", crop="right", mood="dramatic", ev=[L([36, "Bir"], "1964"), T([36, "qonli"], "QONLI TO'QNASHUVLAR", True), ST([37, "Armiya"], "ARMIYA YO'Q")])
beat([38, "Ichimlik"], "scene", bg="bg_water_pipe", ev=[F([38, "Malayziyadan"], "my"), T([38, "quvur"], "SUV MALAYZIYADAN QUVUR ORQALI", True)])
beat([39, "Aholi"], "number", prop="prop_dollar", value="$500", sub="AHOLI JON BOSHIGA DAROMAD (YILIGA)", show=[39, "besh"])
beat([40, "Ko'pchilik"], "object", ev=[M([40, "Ko'pchilik"], 8), T([40, "uzoq"], "UZOQ YASHAMAYDI...", True, x=.36, y=.45)])
beat([41, "Bir"], "object", ev=[M([41, "Bir"], 11), {"at": [41, "obuna"], "k": "subscribe", "x": .36, "y": .5, "dur": 3.4}])
# ---------------- 2-qism: 4 qaror ----------------
beat([43, "Li"], "chapter", num="2-QISM", title="TO'RT QAROR")
beat([44, "Birinchi"], "scene", bg="bg_china_port", ev=[L([44, "Birinchi"], "1. ESHIKNI OCHISH")])
beat([45, "O'sha"], "scene", bg="bg_nationalize", ev=[T([45, "qo'rqardi"], "KO'PCHILIK XORIJIY KOMPANIYADAN QO'RQARDI"), ST([46, "milliylashtirar"], "MILLIYLASHTIRISH")])
beat([47, "Singapur"], "object", ev=[M([47, "Singapur"], 7), {"at": [47, "teskarisini"], "k": "bigtext", "text": "TESKARISI", "x": .36, "y": .45}])
beat([48, "Ular"], "scene", bg="bg_welcome_investors", ev=[T([48, "Kelinglar"], "\"KELINGLAR, ZAVODINGIZNI SHU YERDA QURING\"", True)])
beat([49, "Buning"], "scene", bg="bg_conference", ev=[L([49, "Iqtisodiy"], "IQTISODIY RIVOJLANISH KENGASHI"), T([50, "Sanoat"], "SANOAT HUDUDLARI"),
     T([50, "soliqlar"], "SOLIQLAR ↓"), T([50, "ruxsatnomalar"], "RUXSATNOMA TEZ", True)])
beat([51, "Golland"], "scene", bg="bg_conference", crop="right", ev=[F([51, "Golland"], "nl"), T([51, "Vinsemius"], "ALBERT VINSEMIUS"), T([51, "maslahatchi"], "MASLAHATCHI", True)])
beat([52, "Avval"], "scene", bg="bg_factories", mood="curious", ev=[T([52, "kiyim"], "KIYIM"), T([52, "elektronika"], "ELEKTRONIKA"), T([52, "neftni"], "NEFTNI QAYTA ISHLASH"),
     T([52, "banklar"], "BANKLAR", True)])
beat([53, "Ish"], "scene", bg="bg_factories", crop="left",
     ev=[{"at": [53, "ishsizlik"], "k": "bars", "novalue": True, "x": .5, "w": .4, "items": [{"label": "OLDIN", "value": 100, "color": "red"}, {"label": "KEYIN", "value": 25, "hl": True}]},
         T([53, "ishsizlik"], "ISHSIZLIK TEZ KAMAYDI", True)])
beat([54, "Ikkinchi"], "scene", bg="bg_anticorruption", mood="dramatic", ev=[L([54, "Ikkinchi"], "2. KORRUPSIYAGA QARSHI"), T([55, "yemiradi"], "KORRUPSIYA ICHIDAN YEMIRADI", True)])
beat([56, "Korrupsiyani"], "scene", bg="bg_anticorruption", crop="right", ev=[T([56, "byuro"], "KORRUPSIYA BYUROSI"), T([57, "daromadidan"], "DAROMADDAN ORTIQ BOYLIK = DALIL", True)])
beat([58, "Hatto"], "scene", bg="bg_minister", mood="dramatic", ev=[ST([58, "vazirlar"], "VAZIRLAR HAM")])
beat([59, "Shu"], "object", props=[P([59, "Shu"], "prop_gold", .3, .5, .42)], ev=[T([59, "maosh"], "YUQORI MAOSH", x=.3, y=.82),
     T([60, "halol"], "HALOLGA: YAXSHI HAQ", x=.7, y=.4), T([60, "jazola"], "PORAXO'RGA: QATTIQ JAZO", True, x=.7, y=.58)])
beat([61, "Bugungacha"], "scene", bg="bg_singapore", crop="right", ev=[F([61, "Singapur"], "sg"), T([61, "kam"], "ENG KAM KORRUPSIYALI DAVLATLAR QATORIDA")])
beat([62, "Uchinchi"], "scene", bg="bg_hdb", mood="calm", ev=[L([62, "Uchinchi"], "3. UY-JOY"), T([63, "kengashi"], "1960 · UY-JOY KENGASHI"),
     T([64, "ko'p"], "MINGLAB KO'P QAVATLI UYLAR")])
beat([65, "Eng"], "object", props=[P([65, "Eng"], "prop_key", .3, .5, .5, slam=True)], ev=[T([65, "ijaraga"], "IJARA EMAS", x=.7, y=.4),
     T([65, "sotib"], "SOTIB OLISH", True, x=.7, y=.58)])
beat([66, "Buning"], "object", props=[P([66, "Buning"], "prop_gold", .25, .5, .38)], ev=[T([66, "majburiy"], "MAJBURIY JAMG'ARMA", x=.25, y=.82),
     AR([67, "hisobidan"], (.4, .5), (.62, .5), True), PR([67, "uyini"], "prop_key", .78, .5, .38)])
beat([68, "Bugun"], "scene", bg="bg_hdb", crop="right",
     ev=[{"at": [68, "sakkiztasi"], "k": "pie", "x": .3, "y": .55, "r": .22, "slices": [{"label": "DAVLAT UYLARIDA", "value": 80}, {"label": "BOSHQA", "value": 20}]},
         T([69, "egasi"], "KO'PCHILIGI UY EGASI", True, x=.7, y=.5)])
beat([70, "Li"], "scene", bg="lky_hdb", ev=[T([70, "uyi"], "UYI BOR ODAM..."), T([70, "himoya"], "...DAVLATINI HIMOYA QILADI", True)])
beat([71, "To'rtinchi"], "scene", bg="bg_classroom", mood="curious", ev=[L([71, "To'rtinchi"], "4. TIL VA TA'LIM"), CT([72, "to'rtta"], 4, suffix=" RASMIY TIL", x=.5, y=.25),
     T([72, "ingliz"], "INGLIZ"), T([72, "xitoy"], "XITOY"), T([72, "malay"], "MALAY"), T([72, "tamil"], "TAMIL")])
beat([73, "Li"], "scene", bg="bg_office_world", ev=[F([73, "ingliz"], "gb"), T([73, "ish"], "INGLIZ TILI = ISH TILI", True), T([74, "ustun"], "HECH KIM USTUN EMAS"),
     T([74, "savdo"], "DUNYO BILAN SAVDO")])
beat([75, "Shu"], "scene", bg="bg_mother_tongue", ev=[T([75, "ona"], "+ ONA TILI", True)])
beat([76, "Maktablarda"], "scene", bg="bg_classroom", crop="right", ev=[T([76, "matematika"], "MATEMATIKA VA FANLAR"), ST([77, "birinchi"], "1-O'RIN")])
# ---------------- 3-qism: natija ----------------
beat([78, "Natijasi"], "chapter", num="3-QISM", title="NATIJA")
beat([79, "Aholi"], "object", ev=[L([79, "Aholi"], "AHOLI JON BOSHIGA DAROMAD"),
     {"at": [79, "sakson"], "k": "bars", "x": .5, "w": .5, "items": [{"label": "1965", "value": 500, "color": "red"}, {"label": "BUGUN", "value": 80000, "hl": True}], "suffix": "$"},
     ])
beat([80, "Bu"], "map", bg="map_world", zf=[.5, .45], ev=[F([80, "Amerikadan"], ["sg", "us"]), PIN([80, "Singapur"], SGW), PIN([80, "Amerikadan"], US),
     T([80, "oldinda"], "AMERIKADAN HAM OLDINDA", True, x=.5, y=.85)])
beat([81, "Singapur"], "scene", bg="bg_ships", ev=[T([81, "porti"], "SINGAPUR PORTI"), ST([81, "gavjum"], "ENG GAVJUMLARDAN")])
beat([82, "Orol"], "scene", bg="bg_reclamation", mood="curious", ev=[T([82, "to'ldirish"], "DENGIZNI TO'LDIRISH"), CT([82, "chorak"], 25, prefix="+", suffix="% YER", x=.3, y=.3)])
beat([83, "Suv"], "scene", bg="bg_reclamation", crop="left", ev=[T([83, "yomg'ir"], "YOMG'IR SUVI"), T([83, "chuchuklashtirish"], "DENGIZ SUVI"), T([83, "oqova"], "QAYTA TOZALASH", True)])
beat([84, "Li"], "portrait", fig="lky_cut", vfocus=.2, ev=[L([84, "kitobida"], "LI KUAN YU KITOBI"), T([84, "Uchinchi"], "\"UCHINCHI DUNYODAN\""),
     T([84, "birinchi"], "\"BIRINCHI DUNYOGA\"", True)])
# ---------------- 4-qism: narx ----------------
beat([85, "Lekin"], "chapter", num="4-QISM", title="NARXI")
beat([87, "Li"], "scene", bg="bg_conference", tint=.5, mood="dramatic", ev=[L([87, "1959-yildan"], "1959-YILDAN BERI"), T([87, "hokimiyatda"], "BIR PARTIYA HOKIMIYATDA"),
     ST([87, "yutqazmagan"], "HECH QACHON YUTQAZMAGAN")])
beat([88, "Muxolifat"], "scene", bg="bg_courtroom", mood="dramatic", ev=[T([88, "tuhmat"], "TUHMAT DA'VOLARI"), T([88, "jarimalar"], "KATTA JARIMALAR", True)])
beat([89, "Ba'zi"], "scene", bg="bg_cell", ev=[T([89, "sudsiz"], "SUDSIZ QAMOQ", True), T([89, "yillar"], "YILLAR DAVOMIDA")])
beat([90, "Gazeta"], "scene", bg="bg_censor", ev=[T([90, "Gazeta"], "GAZETA VA TV"), ST([90, "nazoratida"], "NAZORATDA")])
beat([91, "Qonunlar"], "scene", bg="bg_clean_street", ev=[L([91, "qattiq"], "QATTIQ QONUNLAR"), T([91, "axlat"], "AXLAT = KATTA JARIMA"), T([91, "kaltak"], "KALTAK JAZOSI", True)])
beat([92, "1992-yildan"], "object", props=[P([92, "saqich"], "prop_gum_x", .3, .5, .5, slam=True)], ev=[L([92, "1992-yildan"], "1992"), T([92, "saqich"], "SAQICH TAQIQLANGAN", x=.3, y=.85),
     T([93, "o'lim"], "GIYOHVAND SAVDOSI: O'LIM JAZOSI", True, x=.7, y=.5)])
beat([94, "Li"], "portrait", fig="lky_cut", vfocus=.2, ev=[T([94, "tartib"], "1. TARTIB VA RIVOJLANISH"), T([94, "erkinlik"], "2. KEYIN ERKINLIK", True)])
beat([95, "Shu"], "scene", bg="bg_debate_scale", ev=[L([95, "bahs"], "BAHS DAVOM ETADI"), T([96, "natija"], "\"NATIJA HAMMASINI OQLAYDI\"", x=.27, y=.75),
     T([97, "shart"], "\"ERKINLIKDAN VOZ KECHISH SHART EMAS\"", True, x=.73, y=.75)])
beat([98, "Misol"], "scene", bg="bg_korea_taiwan", ev=[F([98, "Koreya"], "kr"), F([98, "Tayvan"], ["kr", "tw"]), T([98, "boyidi"], "TEZ BOYIDI"),
     T([98, "demokratiyalarga"], "KEYIN DEMOKRATIYA", True)])
beat([99, "Yana"], "map", bg="map_malacca", zf=[.55, .6], ev=[PIN([99, "kichik"], SGM), RG([99, "o'rtasida"], SGM), T([99, "kichik"], "JUDA KICHIK", x=.5, y=.85)])
beat([100, "Katta"], "map", bg="map_world", zf=[.7, .42], ev=[T([100, "Katta"], "KATTA DAVLATDA HAM ISHLAYDIMI?", True, x=.5, y=.85)])
# ---------------- 5-qism: biz uchun ----------------
beat([101, "Xo'sh"], "chapter", num="5-QISM", title="BIZ UCHUN SABOQ")
beat([102, "Ko'plab"], "map", bg="map_central_asia", zf=[.45, .5], ev=[T([102, "Markaziy"], "MARKAZIY OSIYO HAM O'RGANADI", x=.5, y=.12)])
beat([103, "Lekin"], "object", ev=[M([103, "Lekin"], 10), ST([103, "emas"], "YER OSTIDA EMAS", x=.36)])
beat([104, "Ular"], "scene", bg="bg_four_pillars", ev=[T([104, "qonunning"], "QONUN HAMMAGA BIR XIL", x=.2, y=.85), T([104, "korrupsiyaga"], "KORRUPSIYAGA QARSHI", x=.4, y=.78),
     T([104, "ta'limga"], "TA'LIMGA SARMOYA", x=.6, y=.85), T([104, "investorga"], "INVESTORGA ISHONCH", True, x=.8, y=.78)])
beat([105, "Masalan"], "map", bg="map_central_asia", zf=[.45, .55], ev=[F([105, "O'zbekistonning"], "uz"), PIN([105, "O'zbekistonning"], UZ),
     T([105, "ikki"], "IKKI KARRA DENGIZSIZ", True, x=.5, y=.85)])
beat([106, "Demak"], "scene", bg="bg_tashkent_far", ev=[ST([106, "nusxa"], "NUSXA EMAS"), T([106, "moslash"], "O'Z SHAROITIGA MOSLASH", True, x=.5, y=.75)])
# ---------------- Javob ----------------
beat([107, "Xo'sh"], "title", title="JAVOB", title2="RESURSSIZ OROL QANDAY BOYIDI?")
beat([108, "Yer"], "object", ev=[M([108, "Yer"], 7), {"at": [108, "qarorlar"], "k": "bigtext", "text": "QARORLAR", "x": .36, "y": .3},
     T([109, "eshikni"], "1. ESHIKNI OCHDI", x=.36, y=.48), T([109, "korrupsiyaga"], "2. KORRUPSIYAGA QARSHI", x=.36, y=.6),
     T([109, "uy"], "3. UY EGASI QILDI", x=.36, y=.72), T([109, "ta'limga"], "4. TA'LIM", x=.36, y=.84)])
beat([110, "Lekin"], "portrait", fig="lky_cut", vfocus=.2, ev=[T([110, "erkinlikning"], "NARXI: CHEKLANGAN ERKINLIK", True),
     L([111, "1990-yilgacha"], "1959–1990 · BOSH VAZIR"), T([111, "vafot"], "2015 · 91 YOSHDA VAFOT ETDI")])
beat([112, "Singapur"], "title", title="SINGAPUR HAQIDA MEN HAM BILMAS EDIM", title2="ENDI ESA HAMMAMIZ BILAMIZ")
beat([114, "Ana"], "object", ev=[M([114, "Ana"], 4), T([114, "rivojlanish"], "TEZ RIVOJLANISH UCHUN...", x=.36, y=.38),
     T([114, "erkinlikning"], "...ERKINLIKDAN VOZ KECHISH TO'G'RIMI?", True, x=.36, y=.55), T([115, "izohlarda"], "IZOHDA YOZING", x=.36, y=.72),
     {"at": [114, "sizningcha"], "k": "like", "x": .82, "y": .2}])
beat([116, "Keyingi"], "scene", bg="bg_diamond", mood="curious", ev=[L([116, "Keyingi"], "KEYINGI QISM"), T([117, "olmoslar"], "OLMOSLAR", True),
     T([117, "reklama"], "ENG MUVAFFAQIYATLI REKLAMA")])
beat([118, "O'tkazib"], "end", pose=1, ev=[{"at": [118, "obuna"], "k": "subscribe", "x": .5, "y": .23, "dur": 3.4}])

cfg = {"layers": "layers", "music": {"curious": "../../assets/music/curious.mp3", "dramatic": "../../assets/music/dramatic.mp3", "calm": "../../assets/music/calm.mp3"},
       "mascot": {"img": "mascot_v2", "parts": 4, "full_body": True,      # poses 0-3: thinking, pointing, surprised, presenting
                  # 4 chin-think, 5 shocked, 6 laughing, 7 finger up, 8 shrug, 9 magnifier, 10 arms crossed, 11 thumbs up
                  "more": [{"img": f"mascot_v3{s_}_{i_}", "parts": 1} for s_ in "ab" for i_ in range(4)]},
       "ui": {"subscribe": "OBUNA BO'LING", "subscribed": "OBUNA BO'LDINGIZ", "like": "LAYK", "next": "KEYINGI VIDEO"},
       "sentences": S, "beats": B,
       "shorts": [{"name": "hook", "from": [0, "1965-yil"], "to": [10, "Va"], "hook": ""},
                  {"name": "independence", "from": [27, "Uning"], "to": [33, "Li"], "hook": "MUSTAQILLIKKA MAJBUR QILINGAN DAVLAT"},
                  {"name": "doors", "from": [44, "Birinchi"], "to": [53, "Ish"], "hook": "SINGAPUR SARMOYANI QANDAY JALB QILDI?"},
                  {"name": "corruption", "from": [54, "Ikkinchi"], "to": [61, "Bugungacha"], "hook": "KORRUPSIYAGA QARSHI SINGAPUR USULI"},
                  {"name": "housing", "from": [62, "Uchinchi"], "to": [70, "Li"], "hook": "10 KISHIDAN 8 TASI DAVLAT UYIDA"},
                  {"name": "price", "from": [85, "Lekin"], "to": [94, "Li"], "hook": "SINGAPUR MUVAFFAQIYATINING NARXI"},
                  {"name": "lesson", "from": [101, "Xo'sh"], "to": [106, "Demak"], "hook": "SINGAPUR VA O'ZBEKISTON"}],
       "series_label": "3-QISM: SINGAPUR", "partners": "Hamkorlarimiz: californiauzbek.com va bysmillah.com loyihalari.",
       "partner_logos": [{"img": "assets/partners/californiauzbek.png", "anim": "assets/partners/californiauzbek_anim.webm", "site": "californiauzbek.com"},
                         {"img": "assets/partners/bysmillah.png", "anim": "assets/partners/bysmillah_anim.mp4", "loop": True, "site": "bysmillah.com", "round": True}], "handle": "@bilmasboy",
       "socials": [["youtube", "@bilmasboy"], ["instagram", "@bilmas.boy"], ["tiktok", "@bilmas.boy"], ["facebook", "@bilmas.boy"], ["telegram", "@bilmas_boy"]]}
json.dump(cfg, open("ep03_beats.json", "w"), ensure_ascii=False, indent=1)
print(len(B), "beats")
