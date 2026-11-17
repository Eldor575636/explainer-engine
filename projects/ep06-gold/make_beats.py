"""Builds ep06_beats.json (Gold) from ep06_sentences.json + this beat plan.
New pictures in layers/ (Higgsfield, 2026-11-17, prompts in picture_prompts.json); mascot library, map_world,
fig_nixon, bg_conference, bg_tv_1971, vaults, bg_gold_bazaar, bg_uzbek_wedding etc. reused from E01-E05."""
import json
S = json.load(open("ep06_sentences.json", encoding="utf-8"))["sentences"]
# map_world coordinates (same map as E01-E05)
US, DE, UK, PL, RU, CN, KZ, TR, BR, UZ = (.22, .37), (.51, .28), (.479, .265), (.536, .27), (.58, .25), (.757, .39), (.658, .30), (.575, .364), (.354, .70), (.645, .35)
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
def PIE(at, slices, **kw):
    d = {"at": at, "k": "pie", "slices": slices}; d.update(kw); return d
def CNT(at, to, **kw):
    d = {"at": at, "k": "counter", "to": to, "x": .5, "y": .5}; d.update(kw); return d
B = []
def beat(at, typ, **kw):
    d = {"at": at, "type": typ}; d.update(kw); B.append(d)

# ---------------- Hook ----------------
beat([0, "2026-yil"], "scene", bg="bg_gold_trading", mood="curious", ev=[L([0, "2026-yil"], "2026 · YANVAR"), T([1, "5"], "1 UNSIYA > $5 000")])
beat([2, "28-yanvarda"], "number", prop="prop_gold", value="$5 590", sub="REKORD · 28-YANVAR", show=[2, "590"])
beat([3, "Noyabr"], "object", ev=[L([3, "Noyabr"], "1 UNSIYA OLTIN NARXI"),
     BARS([3, "Noyabr"], [{"label": "YANVAR", "value": 5590}, {"label": "NOYABR", "value": 3900, "color": "red", "at": [3, "3"]}], prefix="$"),
     ST([3, "30"], "-30%", y=.2, x=.82)])
beat([4, "Shunga"], "scene", bg="bg_gold_delivery", ev=[T([4, "markaziy"], "MARKAZIY BANKLAR"), T([4, "to'xtatmayapti"], "SOTIB OLISHDA DAVOM ETMOQDA", True)])
beat([5, "2026-yilning"], "object", props=[P([5, "2026-yilning"], "prop_gold", .3, .5, .45)], ev=[L([5, "2026-yilning"], "2026 · 3-CHORAK"),
     CNT([5, "321"], 321, suffix=" TONNA", x=.68, y=.45), T([5, "42"], "+42% / 1 YIL", True, x=.68, y=.62)])
beat([6, "Ular"], "object", ev=[F([6, "O'zbekiston"], "uz"), L([6, "zaxiralarining"], "O'ZBEKISTON ZAXIRALARI"),
     PIE([6, "91"], [{"label": "OLTIN", "value": 91}, {"label": "BOSHQA", "value": 9}], x=.5, y=.55, r=.22)])
beat([7, "Xo'sh"], "object", ev=[M([7, "Xo'sh"], "t_gold_magnifier"), T([7, "foiz"], "FOIZ BERMAYDI", x=.36, y=.3), T([7, "ishlab"], "HECH NARSA ISHLAB CHIQARMAYDI", x=.36, y=.45),
     T([7, "qadrli"], "NEGA BUNCHA QADRLI?", True, x=.36, y=.62)])
beat([8, "Va"], "scene", bg="s_kitchen", vfocus=.3, ev=[T([8, "hamyonimizga"], "BIZNING HAMYONIMIZGA TA'SIRI?", True)])
# ---------------- Intro ----------------
beat([9, "Mening"], "intro", pose=3)
beat([10, "Bilganlarim"], "object", ev=[M([10, "Bilganlarim"], "p_book"), T([10, "Bilganlarim"], "BILIM = BOYLIK", x=.32, y=.3),
     T([10, "savollar"], "SO'RAYMAN", x=.32, y=.45), T([10, "izlanaman"], "IZLANAMAN", x=.32, y=.58)])
beat([11, "Hamda"], "scene", bg="s_library", vfocus=.33, ev=[T([11, "topganlarimni"], "TOPGANLARIMNI"), T([11, "ulashib"], "SIZ BILAN ULASHAMAN", True)])
beat([12, "O'tgan"], "scene", bg="bg_wallet", ev=[L([12, "O'tgan"], "5-QISM: INFLYATSIYA"), T([12, "qadri"], "SO'MNING QADRI QAYERGA KETADI?", True)])
beat([13, "Bugun"], "scene", bg="bg_gold_ancient", ev=[T([13, "ming"], "MING YILLAR DAVOMIDA"), T([13, "yo'qotmagan"], "QADRINI YO'QOTMAGAN", True)])
beat([14, "Demak"], "title", title="BUGUNGI MAVZU", title2="OLTIN")
beat([14, "nega"], "scene", bg="s_vault", vfocus=.3, ev=[T([14, "nega"], "NEGA DUNYO OLTINGA QAYTMOQDA?", True)])
# ---------------- 1-qism: nega qimmat ----------------
beat([15, "Avval"], "chapter", num="1-QISM", title="OLTIN NEGA QIMMAT?")
beat([16, "Birinchi"], "object", ev=[M([16, "Birinchi"], "p_pointer"), T([16, "Birinchi"], "3 TA SABAB", True, x=.36, y=.4), T([16, "kam"], "1. JUDA KAM", x=.36, y=.56)])
beat([17, "Insoniyat"], "scene", bg="bg_gold_mine_shaft", ev=[L([17, "Insoniyat"], "BUTUN TARIX DAVOMIDA"), BIG([17, "220"], "220 000 TONNA", y=.5)])
beat([18, "Agar"], "scene", bg="bg_gold_cube", ev=[T([18, "22"], "KUB: 22 × 22 × 22 METR", True)])
beat([19, "Bu"], "scene", bg="bg_gold_cube", crop="right", ev=[T([19, "yetti"], "= 7 QAVATLI UY"), AR([19, "balandligi"], (.42, .2), (.42, .82), True)])
beat([20, "Agar"], "scene", bg="bg_gold_people_world", ev=[T([20, "barcha"], "8 MILLIARD ODAM"), T([20, "27"], "HAR BIRIGA ~27 GRAMM", True)])
beat([21, "Bugungi"], "object", ev=[L([21, "Bugungi"], "DUNYODAGI BARCHA OLTIN"),
     BARS([21, "Bugungi"], [{"label": "BARCHA OLTIN", "value": 27, "at": [21, "27"]}, {"label": "AQSH IQTISODI / 1 YIL", "value": 30, "color": "red", "at": [21, "Amerika"]}],
          suffix=" TRLN $", novalue=False)])
beat([22, "Ikkinchi"], "scene", bg="bg_gold_ancient", crop="left", ev=[T([22, "Ikkinchi"], "2. ZANGLAMAYDI", True), T([22, "chirimaydi"], "CHIRIMAYDI")])
beat([23, "Ming"], "scene", bg="bg_gold_ancient", crop="right", ev=[T([23, "Ming"], "MING YILLAR OLDIN"), T([23, "yangidek"], "BUGUN HAM YANGIDEK ✓", True)])
beat([24, "Uchinchi"], "scene", bg="bg_printing_press", ev=[T([24, "Uchinchi"], "3. BOSIB CHIQARIB BO'LMAYDI", True)])
beat([25, "Pulni"], "scene", bg="bg_gold_mine_shaft", crop="left", ev=[T([25, "Pulni"], "PUL: BIR KUNDA ✓"), T([25, "qazib"], "OLTIN: FAQAT QAZIB OLINADI", True)])
beat([26, "Butun"], "object", props=[P([26, "Butun"], "prop_gold", .3, .5, .45)], ev=[L([26, "Butun"], "BIR YILDA QAZIB OLINADI"),
     CNT([26, "700"], 3700, suffix=" TONNA", x=.68, y=.42), T([26, "2"], "+2% / YIL", True, x=.68, y=.6)])
beat([27, "Shuning"], "scene", bg="bg_gold_bazaar", ev=[T([27, "ishonib"], "MING YILLIK ISHONCH", True)])
beat([28, "Taxminan"], "scene", bg="bg_lydia_mint", mood="calm", ev=[L([28, "Taxminan"], "MIL. AVV. 6-ASR · LIDIYA"),
     T([28, "tangalardan"], "ILK TANGALARDAN BIRI", True), T([28, "kumush"], "OLTIN + KUMUSH")])
# ---------------- 2-qism: oltin va pul ----------------
beat([29, "Aynan"], "chapter", num="2-QISM", title="OLTIN VA PUL")
beat([29, "pulning"], "scene", bg="bg_gold_standard", crop="left", ev=[T([29, "pulning"], "PUL = OLTINGA BOG'LANGAN", True)])
beat([30, "Buni"], "scene", bg="bg_gold_standard", ev=[L([30, "standarti"], "OLTIN STANDARTI"), T([30, "qog'oz"], "QOG'OZ PUL →"), T([30, "almashtirish"], "→ OLTIN", True)])
beat([31, "Birinchi"], "scene", bg="bg_conference", ev=[L([31, "Ikkinchi"], "1944 · BRETTON-VUDS"), T([31, "dollarga"], "VALYUTALAR → DOLLAR"), T([31, "oltinga"], "DOLLAR → OLTIN", True)])
beat([32, "O'shanda"], "number", prop="prop_gold", value="$35", sub="1 UNSIYA · 1944", show=[32, "35"])
beat([33, "Bugungi"], "object", ev=[L([33, "Bugungi"], "1 UNSIYA OLTIN"),
     BARS([33, "Bugungi"], [{"label": "1944", "value": 35}, {"label": "BUGUN", "value": 3900, "hl": True, "at": [33, "110"]}], prefix="$"),
     ST([33, "110"], "×110+", y=.2, x=.82)])
beat([34, "Lekin"], "portrait", fig="fig_nixon", ev=[F([34, "AQSh"], "us", x=.9, y=.15), L([34, "1971-yilda"], "1971 · RICHARD NIKSON")])
beat([34, "dollarni"], "scene", bg="bg_tv_1971", ev=[T([34, "almashtirishni"], "DOLLAR → OLTIN ✗", True)])
beat([35, "Shundan"], "scene", bg="bg_wallet", crop="left", ev=[T([35, "metallga"], "METALLGA BOG'LANMAGAN"), T([35, "ishonchga"], "FAQAT ISHONCH", True)])
beat([36, "Keyingi"], "object", ev=[M([36, "Keyingi"], "p_newspaper"), T([36, "eski"], "\"ESKI ZAMON QOLDIG'I\"", True, x=.36, y=.5)])
beat([37, "Masalan"], "map", bg="map_world", zf=[.48, .27], ev=[F([37, "Britaniya"], "gb"), PIN([37, "Britaniya"], UK), L([37, "1999"], "1999-2002 · BRITANIYA"),
     T([37, "Britaniya"], "OLTINNING YARMI SOTILDI", True, x=.5, y=.85)])
beat([37, "oltinining"], "scene", bg="bg_uk_gold_sale", crop="left", ev=[T([37, "yarmini"], "QARIYB YARMI"), T([37, "395"], "395 TONNA SOTILDI", True)])
beat([38, "O'shanda"], "scene", bg="bg_uk_gold_sale", ev=[T([38, "275"], "1 UNSIYA ≈ $275")])
beat([39, "Bugun"], "object", ev=[L([39, "Bugun"], "1 UNSIYA OLTIN"),
     BARS([39, "Bugun"], [{"label": "1999-2002", "value": 275}, {"label": "BUGUN", "value": 3900, "hl": True, "at": [39, "o'n"]}], prefix="$"),
     ST([39, "barobar"], "×14", y=.2, x=.82)])
beat([40, "Bugun"], "object", ev=[L([40, "Bugun"], "OLTIN ZAXIRASI, TONNA"),
     BARS([40, "Bugun"], [{"label": "BRITANIYA", "value": 310, "at": [40, "310"]}, {"label": "O'ZBEKISTON", "value": 453, "hl": True, "at": [40, "O'zbekiston"]}])])
beat([41, "Britaniyaning"], "scene", bg="bg_uk_gold_sale", crop="right", ev=[ST([41, "xatosi"], "NOTO'G'RI VAQT", y=.78)])
beat([42, "Shu"], "object", sfx=[[0, "ding"]], ev=[M([42, "Shu"], 7), {"at": [42, "obuna"], "k": "subscribe", "x": .4, "y": .45, "dur": 3.4}])
# ---------------- 3-qism: nega yana ----------------
beat([44, "Xo'sh"], "chapter", num="3-QISM", title="NEGA YANA OLTIN?")
beat([44, "markaziy"], "scene", bg="bg_gold_delivery", ev=[T([44, "eski"], "\"ESKI ZAMON QOLDIG'I\"?"), T([44, "sotib"], "NEGA YANA SOTIB OLISHMOQDA?", True)])
beat([45, "2022-yilda"], "scene", bg="bg_moscow_vault", mood="dramatic", ev=[L([45, "2022-yilda"], "2022"), F([45, "Rossiya"], "ru"),
     T([45, "Ukrainaga"], "BOSTIRIB KIRISH")])
beat([45, "G'arb"], "scene", bg="bg_vault_empty", ev=[T([45, "300"], "~$300 MLRD MUZLATILDI", True), ST([45, "muzlatib"], "MUZLATILDI", y=.78)])
beat([46, "Ikkinchi"], "scene", bg="bg_brussels_vault", ev=[L([46, "Ikkinchi"], "2-QISM: SANKSIYALAR")])
beat([47, "Ko'rishga"], "object", ev=[M([47, "Ko'rishga"], 5), T([47, "sanksiyalarga"], "2-QISMNI KO'RING", True, x=.36, y=.45),
     {"at": [47, "YouTube"], "k": "like", "x": .82, "y": .2}])
beat([48, "Aynan"], "scene", bg="bg_treasury", ev=[T([48, "dollar"], "CHET ELDAGI DOLLAR / YEVRO"), T([48, "qaroriga"], "= BOSHQA DAVLAT QARORI", True)])
beat([48, "chet"], "scene", bg="bg_treasury", crop="right", ev=[T([48, "qaroriga"], "BOSHQA DAVLATNING QARORI", True)])
beat([49, "O'z"], "scene", bg="bg_vault", ev=[T([49, "omboringizda"], "O'Z OMBORINGIZDAGI OLTIN"), ST([49, "muzlatib"], "MUZLATIB BO'LMAYDI", y=.78)])
beat([50, "Shundan"], "scene", bg="bg_gold_delivery", crop="left", ev=[T([50, "uch"], "3 YIL KETMA-KET"), T([50, "ming"], "> 1 000 TONNA / YIL", True)])
beat([51, "Bu"], "object", ev=[L([51, "Bu"], "MARKAZIY BANKLAR XARIDI, TONNA"),
     BARS([51, "Bu"], [{"label": "2010-21", "value": 470}, {"label": "2022-24", "value": 1000, "hl": True, "at": [51, "ikki"]},
                       {"label": "2025", "value": 863, "at": [52, "863"]}])])
beat([53, "Eng"], "scene", bg="bg_warsaw_gold", ev=[F([53, "Polsha"], "pl"), L([53, "Polsha"], "ENG KATTA XARIDOR · POLSHA"), T([53, "102"], "2025: 102 TONNA", True)])
beat([54, "Xitoy"], "map", bg="map_world", zf=[.55, .4], ev=[PIN([54, "Xitoy"], CN), PIN([54, "Qozog'iston"], KZ), PIN([54, "Turkiya"], TR), PIN([54, "Braziliya"], BR),
     F([54, "Xitoy"], ["cn", "kz", "tr", "br"])])
beat([55, "Ba'zi"], "scene", bg="bg_gold_plane", ev=[T([55, "uyga"], "OLTINNI UYGA QAYTARISH", True)])
beat([56, "Masalan"], "map", bg="map_world", zf=[.4, .3], ev=[F([56, "Germaniya"], "de"), L([56, "2013"], "2013-2017 · GERMANIYA"),
     AR([56, "Nyu-York"], (.26, .33), DE), AR([56, "Parijda"], (.485, .31), DE), PIN([56, "Frankfurtga"], DE)])
beat([56, "674"], "scene", bg="bg_gold_plane", crop="right", ev=[T([56, "674"], "674 TONNA UYGA", True), L([56, "Frankfurtga"], "FRANKFURT")])
beat([57, "Bugun"], "object", ev=[L([57, "Bugun"], "ENG KO'P OLTIN, TONNA"),
     BARS([57, "Bugun"], [{"label": "AQSH", "value": 8133, "hl": True, "at": [58, "8"]}, {"label": "GERMANIYA", "value": 3350, "at": [57, "3"]},
                          {"label": "O'ZBEKISTON", "value": 453, "at": [57, "Bugun"]}])])
beat([59, "Bu"], "scene", bg="bg_central_bank", mood="calm", ev=[T([59, "o'zgarish"], "KATTA O'ZGARISH", True)])
beat([60, "Yevropa"], "scene", bg="bg_central_bank", crop="right", ev=[L([60, "Yevropa"], "YEVROPA MARKAZIY BANKI"), T([60, "2025-yil"], "2025-YIL OXIRI")])
beat([60, "dunyo"], "object", ev=[L([60, "dunyo"], "MARKAZIY BANKLAR ZAXIRASI · 2025"),
     BARS([60, "dunyo"], [{"label": "OLTIN", "value": 27, "hl": True, "at": [60, "27"]}, {"label": "AQSH OBLIG.", "value": 22, "at": [61, "22"]},
                            {"label": "YEVRO", "value": 15, "at": [61, "15"]}], suffix="%", w=.6)])
beat([62, "Ya'ni"], "scene", bg="s_vault", vfocus=.3, ev=[ST([62, "eng"], "1-O'RINDA", y=.3, x=.7)])
# ---------------- 4-qism: O'zbekiston ----------------
beat([63, "Xo'sh"], "chapter", num="4-QISM", title="O'ZBEKISTON VA OLTIN")
beat([64, "O'zbekiston"], "map", bg="map_central_asia", ev=[F([64, "O'zbekiston"], "uz"), T([64, "tomoshabin"], "ODDIY TOMOSHABIN EMAS", True, x=.5, y=.85)])
beat([65, "Navoiy"], "scene", bg="bg_muruntau", ev=[L([65, "Navoiy"], "NAVOIY · MURUNTOV"), T([65, "eng"], "DUNYODAGI ENG KATTA OCHIQ KON", True)])
beat([66, "Uning"], "scene", bg="bg_muruntau", crop="right", ev=[T([66, "600"], "CHUQURLIGI: 600+ M"), T([66, "3"], "KENGLIGI: 3+ KM", True)])
beat([67, "Bu"], "scene", bg="bg_pit_vs_tower", ev=[T([67, "375"], "TELEMINORA: 375 M"), T([67, "bir"], "KON: ×1,5 CHUQUR", True)])
beat([68, "2025-yilda"], "number", prop="prop_gold", value="83 TONNA", sub="MURUNTOV · 2025 · DUNYODA 2-O'RIN", show=[68, "83"])
beat([68, "dunyodagi"], "scene", bg="bg_muruntau", crop="left", ev=[T([68, "ikkinchi"], "DUNYODA 2-O'RIN", True)])
beat([69, "Mamlakatda"], "scene", bg="bg_refinery", ev=[T([69, "Markaziy"], "QAZIB OLINGAN OLTIN → MARKAZIY BANK", True)])
beat([70, "Shuning"], "scene", bg="bg_tashkent_cb", ev=[L([70, "Jahon"], "JAHON OLTIN KENGASHI"), T([70, "faol"], "ENG FAOL XARIDORLARDAN", True)])
beat([71, "2026-yilning"], "object", ev=[L([71, "2026-yilning"], "2026 · OLTIN QO'SHILDI"),
     BARS([71, "avgust"], [{"label": "AVGUST", "value": 8}, {"label": "SENTABR", "value": 7}, {"label": "OKTABR", "value": 8, "hl": True}], suffix=" T")])
beat([72, "Oktabr"], "number", prop="prop_gold", value="453 TONNA", sub="O'ZBEKISTON · REKORD", show=[72, "453"])
beat([73, "Bu"], "object", ev=[L([73, "Bu"], "ZAXIRALARDA OLTIN ULUSHI"), PIE([73, "91"], [{"label": "OLTIN", "value": 91}, {"label": "BOSHQA", "value": 9}], x=.5, y=.55, r=.22)])
beat([74, "Agar"], "number", prop="prop_gold", value="≈ 12 GRAMM", sub="HAR BIR FUQAROGA · 38 MLN AHOLI", show=[74, "12"])
beat([75, "Taqqoslash"], "object", ev=[L([75, "Taqqoslash"], "ZAXIRALARDA OLTIN ULUSHI"),
     BARS([75, "Taqqoslash"], [{"label": "O'ZBEKISTON", "value": 91, "hl": True}, {"label": "DUNYO O'RTACHA", "value": 27, "at": [75, "27"]}], suffix="%")])
beat([76, "Bunday"], "scene", bg="bg_tashkent_cb", crop="left", ev=[T([76, "oshsa"], "OLTIN ↑ → ZAXIRA ↑ ✓", True)])
beat([77, "Lekin"], "scene", bg="bg_reserves_fall", mood="dramatic", ev=[T([77, "teskari"], "TESKARI TOMONI", True)])
beat([78, "2026-yil"], "object", ev=[L([78, "2026-yil"], "O'ZBEKISTON ZAXIRALARI, MLRD $"),
     BARS([78, "2026-yil"], [{"label": "1-SENTABR", "value": 72.1}, {"label": "1-OKTABR", "value": 66.6, "at": [78, "oktabr"]},
                             {"label": "1-NOYABR", "value": 63.6, "color": "red", "at": [78, "8"]}]), ST([78, "kamaydi"], "-$8,5 MLRD", y=.42, x=.86)])
beat([79, "Holbuki"], "scene", bg="bg_reserves_fall", crop="right", ev=[T([79, "ko'paygan"], "OLTIN MIQDORI ↑", True), T([79, "Holbuki"], "QIYMATI ↓")])
beat([80, "Shuning"], "scene", bg="bg_debate_scale", ev=[L([80, "iqtisodchilar"], "IQTISODCHILAR"), T([80, "xavfli"], "1-FIKR: BITTA AKTIV XAVFLI", True)])
beat([81, "Boshqalar"], "scene", bg="bg_debate_scale", crop="right", ev=[T([81, "tabiiy"], "2-FIKR: QAZIB OLUVCHIGA TABIIY")])
# ---------------- 5-qism: oddiy odam ----------------
beat([82, "Aslida"], "chapter", num="5-QISM", title="OLTIN VA BIZ")
beat([83, "O'zbek"], "scene", bg="bg_home_gold", ev=[T([83, "jamg'arma"], "OILAVIY JAMG'ARMA", True)])
beat([84, "To'ylarda"], "scene", bg="bg_uzbek_wedding", ev=[T([84, "kelinga"], "KELINGA OLTIN TAQINCHOQ")])
beat([84, "ko'pchilik"], "scene", bg="bg_gold_bazaar", crop="left", ev=[T([84, "buyumlarga"], "PUL → OLTIN BUYUM", True)])
beat([85, "Bugun"], "scene", bg="bg_bank_gold_bars", ev=[L([85, "Markaziy"], "TIJORAT BANKLARIDA"), T([85, "5"], "5 GRAMMDAN 100 GRAMMGACHA", True)])
beat([86, "Lekin"], "object", ev=[M([86, "Lekin"], "p_pointer"), T([86, "uchta"], "SOTIB OLISHDAN OLDIN", x=.36, y=.42), T([86, "bilish"], "3 TA NARSA", True, x=.36, y=.57)])
beat([87, "Birinchidan"], "object", ev=[M([87, "Birinchidan"], "p_piggy"), T([87, "foiz"], "1. FOIZ BERMAYDI", True, x=.36, y=.35),
     T([88, "omonat"], "OMONAT: FOIZ ✓", x=.36, y=.5), T([88, "oltin"], "OLTIN: FAQAT NARX ↑", x=.36, y=.62)])
beat([89, "Ikkinchidan"], "scene", bg="bg_gold_trading", crop="right", ev=[T([89, "keskin"], "2. NARX KESKIN O'ZGARADI", True), T([90, "30"], "2026: -30%")])
beat([91, "Tarixda"], "scene", bg="bg_gold_1980", ev=[L([91, "1980-yilning"], "1980 · YANVAR"), T([91, "850"], "1 UNSIYA = $850")])
beat([92, "Shundan"], "object", ev=[M([92, "Shundan"], "p_calculator"), BIG([92, "28"], "28 YIL", x=.36, y=.42), T([92, "qaytish"], "SHU NARXGA QAYTISH UCHUN", True, x=.36, y=.62)])
beat([93, "Uchinchidan"], "scene", bg="bg_gold_spread", ev=[T([93, "farq"], "3. OLISH VA SOTISH NARXI FARQI", True)])
beat([94, "Kichik"], "scene", bg="bg_gold_spread", crop="right", ev=[T([94, "necha"], "FARQ: BIR NECHA %"), ST([94, "yo'qotasiz"], "PULNING BIR QISMI KETADI", y=.78)])
beat([95, "Shu"], "object", ev=[M([95, "Shu"], "p_gold"), T([95, "qisqa"], "QISQA MUDDAT ✗", x=.36, y=.42), T([95, "himoya"], "UZOQ MUDDATLI HIMOYA ✓", True, x=.36, y=.57)])
# ---------------- Bahs ----------------
beat([96, "Iqtisodchilar"], "scene", bg="bg_debate_scale", mood="calm", ev=[L([96, "bahs"], "OLTIN HAQIDA BAHS")])
beat([97, "Bir"], "scene", bg="bg_crisis_gold", ev=[T([97, "Bir"], "1-FIKR: INQIROZDA ENG ISHONCHLI", True)])
beat([97, "urush"], "scene", bg="bg_war", ev=[T([97, "urush"], "URUSH · SANKSIYA · INFLYATSIYA"), T([97, "oltinga"], "ODAMLAR OLTINGA YUGURADI", True)])
beat([98, "Boshqa"], "object", ev=[M([98, "Boshqa"], "p_scale"), T([98, "ishlab"], "2-FIKR: HECH NARSA ISHLAB CHIQARMAYDI", True, x=.36, y=.5)])
beat([99, "Mashhur"], "portrait", fig="buffett_cut", ev=[F([99, "Uorren"], "us", x=.9, y=.15), L([99, "Uorren"], "UORREN BAFFET"), T([99, "2011-yilda"], "2011 · MAKTUB", x=.3, y=.85)])
beat([100, "O'sha"], "number", prop="prop_gold", value="$9,6 TRLN", sub="DUNYODAGI BARCHA OLTIN · 2011", show=[100, "9"])
beat([101, "Baffetning"], "scene", bg="bg_buffett_compare", ev=[T([101, "ekin"], "AQSHDAGI BARCHA EKIN YERLARI"), ])
beat([101, "Exxon"], "scene", bg="bg_buffett_compare", crop="right", ev=[T([101, "16"], "+ 16 TA EXXON MOBIL"), T([101, "1"], "+ $1 TRLN ORTADI", True)])
beat([102, "Uning"], "scene", bg="bg_buffett_compare", crop="left", ev=[T([102, "yer"], "YER, KOMPANIYA = DAROMAD ✓"), T([102, "omborda"], "OLTIN = OMBORDA YOTADI ✗", True)])
beat([103, "Aslida"], "scene", bg="bg_debate_scale", crop="right", ev=[T([103, "ikkala"], "IKKALA TOMON HAM HAQ")])
beat([104, "Oltin"], "object", ev=[M([104, "Oltin"], "p_gold"), T([104, "ko'paytirish"], "KO'PAYTIRISH ✗", x=.36, y=.42), T([104, "saqlab"], "SAQLAB QOLISH ✓", True, x=.36, y=.57)])
# ---------------- Biz uchun ----------------
beat([105, "Xo'sh"], "chapter", num="BIZ UCHUN", title="NIMA UCHUN MUHIM?")
beat([106, "Birinchidan"], "scene", bg="s_exchange", vfocus=.3, ev=[T([106, "Birinchidan"], "1. OLTIN NARXI → SO'M", True), T([106, "zaxiralarimizning"], "ZAXIRANING 91% OLTINDA")])
beat([107, "Ikkinchidan"], "scene", bg="bg_gold_export", ev=[T([107, "eksporti"], "2. ENG KATTA EKSPORT", True)])
beat([108, "2025-yilda"], "object", ev=[L([108, "2025-yilda"], "O'ZBEKISTON EKSPORTI · 2025"),
     PIE([108, "30"], [{"label": "OLTIN $9,9 MLRD", "value": 29}, {"label": "BOSHQA", "value": 71}], x=.5, y=.55, r=.22)])
beat([109, "Uchinchidan"], "object", ev=[M([109, "Uchinchidan"], "t_gold_tower"), T([109, "jamg'armangizni"], "3. JAMG'ARMA OLTINDA?", True, x=.36, y=.42),
     T([109, "tushishi"], "NARX TUSHISHI MUMKIN", x=.36, y=.57)])
beat([110, "Bu"], "scene", bg="s_bank", vfocus=.3, ev=[T([110, "maslahat"], "MOLIYAVIY MASLAHAT EMAS"), T([110, "bilish"], "LEKIN BILISH SHART", True)])
# ---------------- Javob ----------------
beat([111, "Demak"], "title", title="JAVOB", title2="NEGA BANKLAR OLTIN OLMOQDA?")
beat([111, "markaziy"], "scene", bg="s_vault", vfocus=.3, ev=[T([111, "markaziy"], "NEGA YANA OLTIN?", True)])
beat([112, "Chunki"], "scene", bg="bg_crisis_gold", crop="left", ev=[T([112, "notinch"], "DUNYO NOTINCH"), T([112, "qarzdor"], "HECH KIMGA QARZDOR EMAS", True)])
beat([113, "Uni"], "scene", bg="bg_vault", ev=[T([113, "muzlatib"], "MUZLATIB BO'LMAYDI"), T([113, "bosib"], "BOSIB BO'LMAYDI"), T([113, "ming"], "MING YILLIK QADR", True)])
beat([114, "Lekin"], "scene", bg="bg_gold_trading", crop="left", ev=[T([114, "xatarsiz"], "LEKIN XATARSIZ EMAS", True), T([114, "ko'tariladi"], "NARX ↑↓")])
beat([115, "Demak"], "object", ev=[M([115, "Demak"], "t_gold_hug"), T([115, "qisqa"], "TEZ DAROMAD ✗", x=.36, y=.42), T([115, "asrash"], "BOYLIKNI ASRASH ✓", True, x=.36, y=.57)])
beat([116, "Oltin"], "title", title="OLTIN HAQIDA MEN HAM BILMAS EDIM", title2="ENDI ESA HAMMAMIZ BILAMIZ")
beat([118, "Ana"], "object", ev=[M([118, "Ana"], "p_scale"), T([118, "oltinda"], "OLTINDAMI...", x=.36, y=.38),
     T([118, "so'mda"], "...YOKI SO'MDAMI?", True, x=.36, y=.55), T([119, "izohlarda"], "IZOHDA YOZING", x=.36, y=.72),
     {"at": [118, "sizningcha"], "k": "like", "x": .82, "y": .2}])
beat([120, "Keyingi"], "scene", bg="bg_migrant_work", ev=[T([120, "Keyingi"], "KEYINGI QISMDA"), T([120, "o'tkazmalari"], "PUL O'TKAZMALARI", True)])
beat([121, "O'tkazib"], "end", pose=1, ev=[{"at": [121, "obuna"], "k": "subscribe", "x": .47, "y": .35, "dur": 3.4}])

VF = {(67, "Bu"): {"vfocus": [0.3, 0.72]}}
for _d in B:
    if _d['type'] in ('scene', 'portrait', 'map'):
        _d.update(VF.get(tuple(_d['at']), {}))

cfg = {"layers": "layers", "auto_skip": ["Baffet", "Exxon", "2025-yil", "2026-yil"],
       "music": {"curious": "../../assets/music/curious.mp3", "dramatic": "../../assets/music/dramatic.mp3", "calm": "../../assets/music/calm.mp3"},
       "mascot": {"img": "mascot_v2", "parts": 4, "full_body": True,
                  "more": [{"img": f"mascot_v3{s_}_{i_}", "parts": 1} for s_ in "ab" for i_ in range(4)]},
       "ui": {"subscribe": "OBUNA BO'LING", "subscribed": "OBUNA BO'LDINGIZ", "like": "LAYK", "next": "KEYINGI VIDEO"},
       "sentences": S, "beats": B,
       "shorts": [{"name": "hook", "from": [0, "2026-yil"], "to": [8, "Va"], "hook": ""},
                  {"name": "cube", "from": [16, "Birinchi"], "to": [21, "Bugungi"], "hook": "BARCHA OLTIN = 22 METRLI KUB"},
                  {"name": "britain", "from": [36, "Keyingi"], "to": [41, "Britaniyaning"], "hook": "TARIXDAGI ENG YOMON SAVDO"},
                  {"name": "freeze", "from": [45, "2022-yilda"], "to": [53, "Eng"], "hook": "NEGA BANKLAR OLTIN OLMOQDA?"},
                  {"name": "muruntau", "from": [65, "Navoiy"], "to": [74, "Agar"], "hook": "O'ZBEKISTONNING OLTINI"},
                  {"name": "buy", "from": [86, "Lekin"], "to": [95, "Shu"], "hook": "OLTIN OLISHDAN OLDIN BILING"},
                  {"name": "buffett", "from": [98, "Boshqa"], "to": [104, "Oltin"], "hook": "BAFFET NEGA OLTINNI YOQTIRMAYDI?"}],
       "end_hold": 9, "pauses": {"42": 1.2, "44": 1.1}, "end_slots": 2, "end_next": "PUL O'TKAZMALARI", "series_label": "6-QISM: OLTIN",
       "partners": "Hamkorlarimiz: californiauzbek.com va bysmillah.com loyihalari.",
       "partner_logos": [{"img": "assets/partners/californiauzbek.png", "anim": "assets/partners/californiauzbek_anim.webm", "site": "californiauzbek.com"},
                         {"img": "assets/partners/bysmillah.png", "anim": "assets/partners/bysmillah_anim.mp4", "loop": True, "site": "bysmillah.com", "round": True}], "handle": "@bilmasboy",
       "socials": [["youtube", "@bilmasboy"], ["instagram", "@bilmas.boy"], ["tiktok", "@bilmas.boy"], ["facebook", "@bilmas.boy"], ["telegram", "@bilmas_boy"]]}
json.dump(cfg, open("ep06_beats.json", "w"), ensure_ascii=False, indent=1)
print(len(B), "beats")
