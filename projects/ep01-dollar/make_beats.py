"""Builds ep01_beats.json (full episode) from the final script sentences + this beat plan."""
import json
S = json.load(open("ep01_sentences.json", encoding="utf-8"))["sentences"]
US, DC, UK, FR, DE, SA, TAS, MOS, IRN, JP, IN, KR, ME = (0.22, .37), (.27, .38), (.475, .29), (.49, .33), (.51, .30), (.60, .48), (.65, .38), (.57, .27), (.63, .43), (.86, .38), (.69, .50), (.82, .38), (.58, .44)
def L(at, t): return {"at": at, "k": "label", "text": t}
def T(at, t, red=False, **kw):
    d = {"at": at, "k": "tag", "text": t}; d.update(kw)
    if red: d["fg"] = "red"
    return d
def ST(at, t): return {"at": at, "k": "stamp", "text": t}
def AR(at, a, b, straight=False): return {"at": at, "k": "arrow", "from": list(a), "to": list(b), "straight": straight}
def PIN(at, p): return {"at": at, "k": "pin", "x": p[0], "y": p[1]}
def M(at, pose, side="right"): return {"at": at, "k": "mascot", "pose": pose, "side": side}
def PR(at, img, x, y, h, **kw):
    d = {"at": at, "k": "prop", "img": img, "x": x, "y": y, "h": h}; d.update(kw); return d
def P(at, img, x, y, h, **kw):
    d = {"img": img, "x": x, "y": y, "h": h, "at": at}; d.update(kw); return d
SH = "prop_sheet2"   # parts: 0 barrel, 1 bond, 2 scale, 3 yuan
B = []
def beat(at, typ, **kw):
    d = {"at": at, "type": typ}; d.update(kw); B.append(d)

# Hook
beat([0, "Bu"], "scene", bg="bg_bazaar", fig={"img": "fig_worker", "x": 0.3, "h": 0.78}, mood="curious",
     ev=[L([0, "Bu"], "TOSHKENT"), T([1, "Maoshini"], "MAOSH: SO'M"), T([2, "Umrida"], "AMERIKADA BO'LMAGAN", True)])
beat([3, "Lekin"], "object", props=[P([3, "telefon"], "prop_shopping", .2, .5, .42, part=0), P([4, "Mashina"], "prop_shopping", .5, .52, .32, part=1),
     P([5, "uni"], "prop_shopping", .8, .5, .42, part=2)],
     ev=[L([3, "dollarga"], "NARX = DOLLAR"), T([3, "dollarga"], "$", True, x=.2, y=.8), T([4, "dollarga"], "$", True, x=.5, y=.8), T([5, "dollarga"], "$", True, x=.8, y=.8)])
beat([6, "Minglab"], "object", props=[P([6, "Minglab"], "prop_dollar", .5, .52, .72, slam=True)],
     ev=[{"at": [6, "yashil"], "k": "circle", "x": .5, "y": .52, "rx": .3, "ry": .36}, L([6, "maoshi"], "YASHIL QOG'OZ")])
beat([7, "Qanday"], "map", bg="map_world", zf=[.75, .7],
     ev=[AR([7, "dollari"], US, TAS), PIN([7, "dunyo"], TAS), T([7, "dunyo"], "DUNYO PULI?", x=.5, y=.82), M([8, "Va"], 0)])
# Intro
beat([9, "Mening"], "intro", pose=3)
beat([11, "Bilganlarim"], "object", ev=[M([11, "Bilganlarim"], 3), T([11, "Bilganlarim"], "BILIM = BOYLIK", x=.32, y=.3),
     T([11, "so'rab"], "SO'RAYMAN", x=.32, y=.45), T([11, "izlab"], "IZLAYMAN", x=.32, y=.58), T([12, "ulashaman"], "ULASHAMAN", True, x=.32, y=.71)])
beat([13, "Tan"], "object", ev=[PR([13, "Tan"], "prop_dollar", .3, .5, .5), {"at": [13, "ko'p"], "k": "counter", "from": 0, "to": 1000, "prefix": "$", "x": .3, "y": .82},
     {"at": [14, "nega"], "k": "bigtext", "text": "?", "x": .62, "y": .45}, M([15, "Buni"], 2)])
beat([17, "Demak"], "title", title="BUGUNGI MAVZU", title2="AQSH DOLLARI")
beat([18, "Boshlashdan"], "object", ev=[M([18, "Boshlashdan"], 1), {"at": [18, "obuna"], "k": "subscribe", "x": .36, "y": .5, "dur": 3.4}])
# Boshlanish
beat([19, "Yuz"], "scene", bg="bg_london", ev=[T([19, "Yuz"], "100 YIL OLDIN"), T([19, "dollar"], "DOLLAR EMAS", True), L([21, "Britaniya"], "BRITANIYA FUNTI"),
     PR([21, "funti"], "prop_currencies", .2, .6, .42), T([22, "imperiya"], "ENG KATTA IMPERIYA"), T([23, "funtida"], "SAVDO = FUNTDA"), T([24, "London"], "LONDON: MOLIYA MARKAZI")])
beat([25, "Keyin"], "scene", bg="bg_war", mood="dramatic", ev=[L([25, "ikki"], "1914–1918 · 1939–1945")])
beat([26, "Urushlar"], "scene", bg="bg_london", tint=.55, ev=[T([26, "qimmatga"], "JUDA QIMMAT", True), T([27, "Qurol"], "QUROL"), T([27, "oziq-ovqat"], "OZIQ-OVQAT"),
     T([27, "askarlar"], "ASKARLAR"), ST([27, "qarz"], "QARZ")])
beat([27, "aynan"], "map", bg="map_world", ev=[AR([27, "Amerikadan"], DC, UK), PIN([27, "Amerikadan"], UK), L([27, "keldi"], "QARZ: AQSHDAN"), ST([28, "qarzdor"], "QARZDOR")])
beat([29, "Amerikada"], "scene", bg="bg_us_factory", mood="curious", ev=[L([29, "Amerikada"], "AQSH"), T([30, "Urush"], "URUSH YETIB KELMADI"), T([31, "Zavodlari"], "ZAVODLAR TO'LIQ ISHLARDI")])
beat([32, "Davlatlar"], "number", prop="prop_gold", value="2/3", sub="DUNYO OLTIN ZAXIRASI AQSHDA", show=[32, "uchdan"])
beat([33, "Shunday"], "object", ev=[L([33, "1944-yilda"], "1944"), M([33, "savol"], 2), T([33, "urush"], "URUSH TUGAGACH...", x=.32, y=.42), T([33, "qaysi"], "QAYSI PUL?", True, x=.32, y=.6)])
# 1-qism
beat([34, "1944-yil"], "chapter", num="1-QISM", title="KELISHUV")
beat([35, "Amerikadagi"], "scene", bg="bg_hotel", crop="left", ev=[L([35, "Bretton-Vuds"], "BRETTON-VUDS · 1944"), {"at": [36, "44"], "k": "counter", "to": 44, "suffix": " DAVLAT", "x": .5, "y": .5}])
beat([37, "Ular"], "scene", bg="bg_depression", mood="dramatic", ev=[L([37, "1930-yillarni"], "1930-YILLAR"), T([38, "arzonlashtirib"], "PULNI ARZONLASHTIRISH"),
     T([39, "Boshqalar"], "BOSHQALAR HAM"), ST([40, "Savdo"], "SAVDO QULADI"), T([41, "takrorlanishini"], "QAYTA TAKRORLANMASIN", True)])
beat([42, "Yig'ilgan"], "scene", bg="bg_conference", mood="curious", ev=[T([42, "uch"], "3 HAFTA BAHS")])
beat([43, "Britaniya"], "portrait", fig="fig_keynes", ev=[L([43, "Jon"], "JON MEYNARD KEYNS"), T([43, "iqtisodchisi"], "BRITANIYA"), T([44, "yangi"], "YANGI XALQARO VALYUTA?")])
beat([45, "Ammo"], "split", left="bg_vault", right="bg_us_factory", ev=[T([45, "oltin"], "OLTIN: AQSHDA", x=.25, y=.22), T([45, "kuch-qudrat"], "KUCH: AQSHDA", x=.75, y=.22),
     ST([46, "qoidani"], "QOIDANI AQSH YOZADI")])
beat([47, "Oxir-oqibat"], "object", props=[P([48, "Dollar"], "prop_dollar", .5, .5, .42), P([48, "oltinga"], "prop_gold", .82, .5, .42), P([49, "Boshqa"], "prop_currencies", .17, .5, .46)],
     ev=[AR([48, "oltinga"], (.62, .5), (.71, .5), True), {"at": [48, "35"], "k": "counter", "to": 35, "prefix": "$", "suffix": " = 1 UNSIYA", "x": .74, "y": .8},
         AR([49, "dollarga"], (.29, .5), (.38, .5), True)])
beat([50, "Dollari"], "map", bg="map_world", ev=[AR([50, "Amerikadan"], FR, DC), AR([50, "Amerikadan"], JP, (.3, .4)), AR([50, "haqiqiy"], UK, (.28, .36)),
     PIN([50, "Amerikadan"], DC), L([50, "almashtirib"], "DOLLARNI OLTINGA"), T([50, "istalgan"], "ISTALGAN VAQT"), M([50, "mumkin"], 3)])
beat([51, "Shu"], "object", props=[P([51, "AQSh"], "prop_dollar", .3, .5, .5), P([51, "oltin"], "prop_gold", .7, .5, .5)],
     ev=[{"at": [51, "teng"], "k": "bigtext", "text": "=", "x": .5, "y": .5}, L([51, "oltin"], "OLTIN BILAN TENG")])
beat([52, "Markaziy"], "scene", bg="bg_vault", ev=[L([52, "Markaziy"], "MARKAZIY BANKLAR"), T([53, "tashish"], "OSON TASHILADI"), T([53, "foiz"], "+ FOIZ DAROMAD")])
beat([54, "Shu"], "scene", bg="bg_conference", crop="right", ev=[T([54, "Xalqaro"], "XALQARO VALYUTA JAMG'ARMASI"), T([54, "Jahon"], "JAHON BANKI")])
beat([55, "Shu"], "map", bg="map_world", zf=[.5, .5], ev=[PR([55, "Shu"], "prop_dollar", .5, .5, .4, grow=True), {"at": [55, "markaziga"], "k": "rings", "x": .5, "y": .5},
     L([55, "markaziga"], "DOLLAR: DUNYO MARKAZIDA")])
# 2-qism
beat([56, "Tizim"], "chapter", num="2-QISM", title="BUZILGAN VA'DA")
beat([57, "Lekin"], "object", props=[P([58, "va'daga"], "prop_dollar", .3, .5, .5), P([58, "oltin"], "prop_gold", .7, .5, .5)],
     ev=[L([58, "va'daga"], "VA'DA"), {"at": [58, "har"], "k": "bigtext", "text": "=", "x": .5, "y": .5}])
beat([59, "1960-yillarda"], "scene", bg="bg_printing", ev=[L([59, "1960-yillarda"], "1960-YILLAR"), T([59, "Vetnam"], "VETNAM URUSHI"), T([59, "yangi"], "YANGI DASTURLAR"),
     T([59, "harbiy"], "HARBIY BAZALAR")])
beat([60, "Bularning"], "object", ev=[L([60, "dollar"], "TOBORA KO'P DOLLAR"),
     {"at": [61, "Tez"], "k": "bars", "novalue": True, "items": [{"label": "AQSHDAGI OLTIN", "value": 35, "color": "mustard"}, {"label": "DUNYODAGI DOLLAR", "value": 100, "color": "red", "hl": True}]}])
beat([62, "Ko'pchilik"], "portrait", fig="fig_degaulle", ev=[T([63, "Fransiya"], "FRANSIYA"), L([63, "Sharl"], "SHARL DE GOLL"), T([63, "almashtira"], "DOLLARNI OLTINGA", True)])
beat([63, "oltinni"], "scene", bg="bg_gold_ships", ev=[T([63, "kemalar"], "KEMALARDA OLTIN")])
beat([64, "Boshqa"], "map", bg="map_world", ev=[AR([64, "Boshqa"], DC, FR), AR([64, "Fransiyaga"], DC, DE), AR([64, "ergashdi"], DC, UK), L([64, "ergashdi"], "OLTIN KETMOQDA")])
beat([65, "Amerika"], "scene", bg="bg_vault_empty", ev=[ST([65, "kamayib"], "OLTIN KAMAYMOQDA")])
beat([66, "1971-yil"], "scene", bg="bg_tv_1971", mood="dramatic", ev=[L([66, "1971-yil"], "1971 · 15-AVGUST")])
beat([66, "Prezident"], "portrait", fig="fig_nixon", ev=[L([66, "Richard"], "RICHARD NIKSON"), T([66, "almashtirmasligini"], "OLTINGA ALMASHTIRILMAYDI", True)])
beat([67, "Ayni"], "object", ev=[{"at": [67, "Ayni"], "k": "news", "text": "VA'DA TUGADI"}])
beat([68, "Ya'ni"], "object", props=[P([68, "Ya'ni"], "prop_dollar", .38, .5, .5, slam=True)],
     ev=[T([68, "oltin"], "ENDI OLTIN YO'Q", True, x=.38, y=.18), T([68, "ishoning"], "SHUNCHAKI ISHONING", x=.38, y=.84), M([69, "Hmm"], 0)])
beat([71, "Xullas"], "object", mood="curious", props=[P([71, "Xullas"], "prop_dollar", .5, .5, .5)],
     ev=[T([71, "yo'qotadi"], "DOLLAR TUSHADI?", x=.5, y=.18), ST([72, "qulamadi"], "QULAMADI")])
beat([73, "Aksincha"], "map", bg="map_world", trans="zoom", zf=[.58, .44], ev=[PIN([73, "voqea"], ME), {"at": [73, "voqea"], "k": "rings", "x": ME[0], "y": ME[1]}])
beat([74, "Bir"], "object", ev=[M([74, "Bir"], 1), {"at": [74, "layk"], "k": "like", "x": .36, "y": .42}, {"at": [74, "obuna"], "k": "subscribe", "x": .36, "y": .62, "dur": 3.4}])
# 3-qism
beat([77, "Demak"], "chapter", num="3-QISM", title="NEFT DOLLARNI QUTQARADI")
beat([78, "Arab"], "map", bg="map_world", mood="dramatic", ev=[PIN([78, "Arab"], ME), L([78, "neft"], "NEFT EMBARGOSI"), AR([78, "Amerika"], ME, DC), ST([78, "to'xtatdi"], "TO'XTATILDI")])
beat([79, "Bir"], "object", ev=[L([79, "neft"], "NEFT NARXI"), PR([79, "neft"], SH, .2, .55, .34, part=0, nparts=4),
     {"at": [79, "to'rt"], "k": "bars", "suffix": "x", "x": .6, "w": .5, "items": [{"label": "1973 BOSHI", "value": 1}, {"label": "1974", "value": 4, "color": "red", "hl": True}]}])
beat([80, "Amerika"], "scene", bg="bg_gas_queue", ev=[T([80, "uzun"], "UZUN NAVBATLAR", True)])
beat([81, "Dunyo"], "scene", bg="bg_oil_field", mood="curious", ev=[T([81, "neftga"], "DUNYO NEFTGA BOG'LIQ"), L([82, "Saudiya"], "SAUDIYA ARABISTONI")])
beat([83, "1974-yilda"], "map", bg="map_world", ev=[L([83, "1974-yilda"], "1974 · KELISHUV"), PIN([83, "Saudiya"], SA), AR([84, "dollarda"], SA, DC), T([84, "dollarda"], "NEFT DOLLARDA", x=.45, y=.8),
     AR([85, "Evaziga"], DC, SA), T([85, "harbiy"], "QUROL VA HIMOYA", x=.45, y=.9)])
beat([86, "Saudiya"], "object", props=[P([86, "Saudiya"], SH, .5, .5, .55, part=1, nparts=4)], ev=[T([86, "obligatsiyalariga"], "AQSH DAVLAT OBLIGATSIYALARI", x=.5, y=.84)])
beat([87, "Boshqa"], "map", bg="map_world", ev=[{"at": [87, "Boshqa"], "k": "rings", "x": ME[0], "y": ME[1]}, L([87, "dollarda"], "NEFT = DOLLAR")])
beat([88, "O'ylab"], "object", props=[P([89, "neft"], SH, .22, .5, .38, part=0, nparts=4), P([90, "dollar"], "prop_dollar", .52, .5, .42)],
     ev=[M([88, "O'ylab"], 0), AR([90, "Agar"], (.31, .5), (.4, .5), True)])
beat([91, "Yaponiya"], "map", bg="map_world", ev=[PIN([91, "Yaponiya"], JP), PIN([91, "Germaniya"], DE), PIN([91, "Hindiston"], IN), T([91, "dollar"], "HAMMAGA DOLLAR KERAK", x=.5, y=.85)])
beat([92, "Ayni"], "map", bg="map_world", ev=[AR([93, "qaytarib"], ME, DC), PIN([93, "Amerikaga"], DC), T([93, "banklariga"], "AQSH BANKLARI", x=.3, y=.6)])
beat([94, "Bu"], "object", ev=[{"at": [94, "Bu"], "k": "news", "text": "PETRODOLLAR"}])
beat([95, "Shunday"], "object", props=[P([95, "oltin"], "prop_gold", .2, .5, .36), P([95, "strategik"], "prop_dollar", .5, .5, .36), P([95, "mahsulot"], SH, .8, .5, .36, part=0, nparts=4)],
     ev=[ST([95, "yo'qotganiga"], "OLTIN EMAS"), T([95, "yangi"], "YANGI TAYANCH: NEFT", True, x=.5, y=.84)])
# 4-qism
beat([96, "Bugun"], "chapter", num="4-QISM", title="BUGUNGI KUCH")
beat([96, "saqlaydigan"], "object", ev=[L([96, "saqlaydigan"], "ZAXIRA VALYUTALARI"),
     {"at": [96, "57"], "k": "pie", "slices": [{"label": "DOLLAR", "value": 57}, {"label": "YEVRO", "value": 20}, {"label": "YUAN", "value": 2}, {"label": "BOSHQA", "value": 21}]}])
beat([99, "Dunyoda"], "number", prop="prop_dollar", value="9/10", sub="VALYUTA BITIMLARIDA DOLLAR BOR", show=[99, "9"])
beat([100, "O'zbekistondagi"], "map", bg="map_world", ev=[PIN([100, "O'zbekistondagi"], TAS), PIN([100, "Koreyadan"], KR), AR([100, "dollar"], TAS, DC), AR([100, "o'tadi"], DC, KR),
     T([100, "Amerika"], "IKKALASI HAM AQSH EMAS", True, x=.5, y=.85)])
beat([101, "Bu"], "object", ev=[M([101, "Bu"], 3), L([101, "ikki"], "IKKI USTUNLIK"), T([102, "arzon"], "1. ARZON QARZ", x=.32, y=.4)])
beat([103, "Butun"], "object", ev=[L([103, "Butun"], "ARZON QARZ"), PR([103, "obligatsiyalarini"], SH, .2, .55, .36, part=1, nparts=4), M([104, "men"], 2),
     {"at": [104, "foiz"], "k": "bars", "novalue": True, "x": .5, "w": .4, "items": [{"label": "AQSH FOIZI", "value": 30}, {"label": "MENING FOIZIM", "value": 90, "color": "red", "hl": True}]}])
beat([105, "Ikkinchisi"], "scene", bg="bg_bank_network", mood="dramatic", ev=[L([105, "kuch"], "2. KUCH"), T([106, "banklari"], "TO'LOVLAR AQSH ORQALI"), T([108, "SWIFT"], "SWIFT"),
     ST([108, "uzib"], "UZILDI")])
beat([109, "Masalan"], "map", bg="map_world", ev=[PIN([109, "Eron"], IRN), T([109, "Eron"], "ERON", x=IRN[0], y=IRN[1] + .1), PIN([110, "Rossiya"], MOS),
     T([110, "2022-yildan"], "ROSSIYA · 2022", x=MOS[0], y=MOS[1] - .1)])
beat([111, "Shu"], "object", ev=[M([111, "Shu"], 2), T([111, "dollardan"], "DOLLARDAN UZILISH", x=.36, y=.4), T([111, "jahon"], "= JAHONDAN UZILISH", True, x=.36, y=.58)])
# 5-qism
beat([112, "Endi"], "chapter", num="5-QISM", title="O'ZBEKISTON UCHUN", mood="curious")
beat([113, "O'zbekiston"], "scene", bg="bg_bazaar", fig={"img": "fig_worker", "x": 0.3, "h": 0.78}, ev=[T([113, "mashinalar"], "MASHINALAR"), T([113, "telefonlar"], "TELEFONLAR"),
     T([113, "dori-darmonlar"], "DORI-DARMON"), T([113, "bug'doy"], "BUG'DOY VA UN")])
beat([114, "Bu"], "object", props=[P([114, "Bu"], "prop_dollar", .3, .5, .5)], ev=[L([114, "dollarda"], "IMPORT = DOLLAR"), T([115, "Dollar"], "DOLLAR QIMMATLASHSA", x=.68, y=.4),
     T([115, "qimmatlashadi"], "NARXLAR OSHADI", True, x=.68, y=.58)])
beat([116, "2017-yil"], "scene", bg="bg_tashkent_exchange", ev=[L([116, "2017-yil"], "2017 · SENTABR"), T([116, "erkin"], "VALYUTA ERKIN")])
beat([117, "O'sha"], "object", ev=[L([117, "kurs"], "1 DOLLAR NARXI"),
     {"at": [117, "taxminan"], "k": "bars", "suffix": " SO'M", "x": .5, "w": .5, "items": [{"label": "OLDIN", "value": 4200}, {"label": "KEYIN", "value": 8100, "color": "red", "hl": True}]}])
beat([118, "Shu"], "scene", bg="bg_bazaar", crop="right", ev=[ST([118, "keskin"], "NARXLAR SAKRADI")])
beat([119, "Pul"], "scene", bg="bg_migrant_work", ev=[T([119, "teskari"], "PUL QAYTIB KELADI"), T([120, "Millionlab"], "MILLIONLAB ISHCHI")])
beat([121, "2025-yilda"], "number", prop="prop_dollar", value="$19 MLRD", sub="2025: PUL O'TKAZMALARI", show=[121, "19"])
beat([121, "uning"], "map", bg="map_world", ev=[AR([121, "Rossiyadan"], MOS, TAS), PIN([121, "Rossiyadan"], TAS), T([121, "uch"], "QARIYB 3/4 ROSSIYADAN", x=.5, y=.85)])
beat([122, "Shuning"], "scene", bg="bg_family_home", ev=[T([122, "dollarda"], "JAMG'ARMA: DOLLARDA"), T([123, "qadrsizlangan"], "SO'M QADRSIZLANGAN"), T([124, "dollarda"], "UY, MASHINA: DOLLARDA")])
beat([125, "Demak"], "split", left="bg_fed", right="bg_bazaar", ev=[T([125, "Vashingtondagi"], "VASHINGTON", x=.25, y=.22), L([125, "foiz"], "FOIZ STAVKASI"),
     T([125, "Toshkentdagi"], "TOSHKENT", x=.75, y=.22), AR([125, "yetib"], (.3, .55), (.7, .55))])
# Yakun
beat([126, "Ana"], "title", title="SO'NGGI SAVOL:", title2="DOLLAR TUGAYAPTIMI?")
beat([127, "O'zgarish"], "object", ev=[PR([128, "yuanni"], SH, .2, .45, .36, part=3, nparts=4), T([129, "BRIKS"], "BRIKS", x=.5, y=.3), PR([130, "oltin"], "prop_gold", .8, .45, .36),
     T([131, "O'zbekiston"], "O'ZBEKISTON HAM OLTIN OLMOQDA", True, x=.5, y=.8)])
beat([132, "Lekin"], "object", props=[P([132, "Lekin"], SH, .3, .52, .6, part=2, nparts=4)], ev=[T([133, "Ishonch"], "ISHONCH", x=.7, y=.3), T([133, "ochiq"], "OCHIQ BOZOR", x=.7, y=.45),
     T([133, "erkin"], "ERKIN PUL", x=.7, y=.6), ST([134, "taklif"], "RAQIB YO'Q")])
beat([135, "Savolga"], "object", mood="calm", ev=[M([135, "Savolga"], 3), T([135, "yo'qotib"], "ASTA-SEKIN ZAIFLASHMOQDA", x=.36, y=.4), T([135, "o'rinbosar"], "O'RINBOSAR HOZIRCHA YO'Q", True, x=.36, y=.58)])
beat([136, "Bu"], "title", title="BU HAQIDA MEN HAM BILMAS EDIM", title2="ENDI HAMMAMIZ BILAMIZ")
beat([137, "Ana"], "object", props=[P([137, "so'mdami"], "prop_currencies", .2, .5, .42), P([137, "dollardami"], "prop_dollar", .5, .5, .38), P([137, "oltindami"], "prop_gold", .8, .5, .38)],
     ev=[L([137, "sizga"], "SIZ-CHI?")])
beat([138, "Keyingi"], "object", ev=[M([138, "Keyingi"], 1), T([138, "izohlarda"], "IZOHDA YOZING", x=.36, y=.4), {"at": [139, "layk"], "k": "like", "x": .36, "y": .6}])
beat([140, "Keyingi"], "end", pose=1, ev=[{"at": [141, "obuna"], "k": "subscribe", "x": .5, "y": .11, "dur": 3.4},
     T([142, "Loyihamiz"], "HAMKORLAR: CALIFORNIA UZBEK · BYSMILLAH", x=.5, y=.1), T([144, "Bilmasboy"], "BILMASBOY", True, x=.5, y=.9)])

cfg = {"layers": "layers", "music": {"curious": "../../assets/music/curious.mp3", "dramatic": "../../assets/music/dramatic.mp3", "calm": "../../assets/music/calm.mp3"},
       "mascot": {"img": "mascot_v2", "parts": 4, "full_body": True},
       "ui": {"subscribe": "OBUNA BO'LING", "subscribed": "OBUNA BO'LDINGIZ", "like": "LAYK", "next": "KEYINGI VIDEO"},
       "sentences": S, "beats": B,
       "shorts": [{"name": "hook", "from": [0, "Bu"], "to": [8, "Va"], "hook": ""},
                  {"name": "bretton_woods", "from": [34, "1944-yil"], "to": [55, "Shu"], "hook": "1944: DOLLAR QANDAY SHOH BO'LDI?"},
                  {"name": "petrodollar", "from": [77, "Demak"], "to": [95, "Shunday"], "hook": "NEFT DOLLARNI QANDAY QUTQARDI?"},
                  {"name": "power", "from": [99, "Dunyoda"], "to": [111, "Shu"], "hook": "AQSH DAVLATNI DOLLARDAN QANDAY UZADI?"},
                  {"name": "uzbekistan", "from": [112, "Endi"], "to": [125, "Demak"], "hook": "SO'M NEGA DOLLARGA BOG'LIQ?"}]}
json.dump(cfg, open("ep01_beats.json", "w"), ensure_ascii=False, indent=1)
print(len(B), "beats")
