"""Eldor Explains E01 Gold: builds ee01_beats.json from en/sentences.json + this beat plan. Run with CHANNEL=ee.
Scene pictures are shared with Bilmasboy E06 (../layers). New pictures (names starting e_ for the English-outfit
character, bg_fort_knox, bg_costco_gold, bg_boe_vault) are listed in en/picture_prompts.json.
Engagement rules: docs/master-episode.md (hook with 2 open loops, guess beat, re-hooks, three spoken asks)."""
import json
S = [s["text"] for s in json.load(open("sentences.json", encoding="utf-8"))]
US, DE, UK, PL, RU, CN, KZ, TR, BR = (.22, .37), (.51, .28), (.479, .265), (.536, .27), (.58, .25), (.757, .39), (.658, .30), (.575, .364), (.354, .70)
NY, PARIS = (.26, .33), (.485, .31)


def L(at, t): return {"at": at, "k": "label", "text": t}
def T(at, t, hl=False, **kw):
    d = {"at": at, "k": "tag", "text": t}; d.update(kw)
    if hl: d["fg"] = "red"            # 'red' = the channel accent (money green in Eldor Explains)
    return d
def ST(at, t, **kw):
    d = {"at": at, "k": "stamp", "text": t}; d.update(kw); return d
def AR(at, a, b, straight=False): return {"at": at, "k": "arrow", "from": list(a), "to": list(b), "straight": straight}
def PIN(at, p): return {"at": at, "k": "pin", "x": p[0], "y": p[1]}
def M(at, pose, side="right"): return {"at": at, "k": "mascot", "pose": pose, "side": side}
def F(at, code, **kw):
    d = {"at": at, "k": "flag", "code": code}; d.update(kw); return d
def P(at, img, x, y, h, **kw):
    d = {"img": img, "x": x, "y": y, "h": h, "at": at}; d.update(kw); return d
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

# ---------------- Hook: contrast + question + two open loops ----------------
beat([0, "In"], "object", mood="curious", ev=[L([0, "In"], "1 OUNCE OF GOLD"),
     BARS([0, "five"], [{"label": "JAN 2026", "value": 5590}, {"label": "NOV 2026", "value": 3900, "color": "red", "at": [1, "crashed"]}], prefix="$"),
     ST([1, "thirty"], "-30%", y=.2, x=.82)])
beat([2, "Any"], "scene", bg="bg_gold_trading", ev=[T([2, "panic"], "INVESTORS: SELL!"), T([3, "opposite"], "CENTRAL BANKS: BUY", True)], sfx=[[0.1, "whoosh"]])
beat([4, "In"], "object", props=[P([4, "In"], "prop_gold", .3, .5, .45)], ev=[L([4, "In"], "Q3 2026 · CENTRAL BANKS"),
     CNT([4, "twenty-one"], 321, suffix=" TONNES", x=.68, y=.45), T([4, "forty-two"], "+42% IN A YEAR", True, x=.68, y=.62)])
beat([5, "So"], "object", ev=[M([5, "So"], "e_magnifier"), T([5, "interest"], "NO INTEREST", x=.36, y=.32), T([5, "nothing"], "PRODUCES NOTHING", x=.36, y=.46),
     T([5, "hoarding"], "SO WHY HOARD IT?", True, x=.36, y=.62)])
beat([6, "Later"], "scene", bg="bg_uk_gold_sale", ev=[L([6, "Later"], "COMING UP"), T([6, "half"], "ONE COUNTRY SOLD HALF ITS GOLD", True),
     T([6, "worst"], "AT THE WORST MOMENT")], sfx=[[0, "swoosh"]])
beat([7, "And"], "scene", bg="bg_fort_knox", ev=[L([7, "And"], "COMING UP"), T([7, "trillion"], "$1 TRILLION OF GOLD..."), T([7, "eleven"], "...WORTH $11 BILLION ON PAPER?", True)])
# ---------------- Intro (logo sting after the hook) ----------------
beat([8, "I'm"], "intro")
beat([9, "One"], "object", ev=[M([9, "One"], "e_presenting"), T([9, "question"], "ONE MONEY QUESTION", x=.36, y=.42), T([9, "real"], "REAL NUMBERS", True, x=.36, y=.57)])
beat([10, "Today"], "title", title="TODAY'S QUESTION", title2="WHY IS THE WORLD GOING BACK TO GOLD?")
# ---------------- 1: why is gold expensive ----------------
beat([11, "First"], "chapter", num="PART 1", title="WHY IS GOLD SO EXPENSIVE?")
beat([12, "Reason"], "object", ev=[M([12, "Reason"], "e_pointer"), T([12, "Reason"], "3 REASONS", True, x=.36, y=.4), T([12, "little"], "1. THERE IS VERY LITTLE", x=.36, y=.56)])
beat([13, "Take"], "scene", bg="bg_gold_mine_shaft", ev=[L([13, "Take"], "TAKE A GUESS"), T([13, "melted"], "ALL GOLD EVER MINED, MELTED", True),
     T([14, "football"], "A. A FOOTBALL STADIUM?", x=.5, y=.62), T([15, "skyscraper"], "B. A SKYSCRAPER?", x=.5, y=.74)], sfx=[[0, "tick"]])
beat([16, "The"], "scene", bg="bg_gold_cube", ev=[T([16, "cube"], "A CUBE: 22 M (~70 FT) EACH SIDE", True)], sfx=[[0, "ding"]])
beat([17, "That's"], "scene", bg="bg_gold_cube", crop="right", ev=[T([17, "seven-story"], "= A 7-STORY BUILDING"), AR([17, "roughly"], (.42, .2), (.42, .82), True)])
beat([18, "That's"], "scene", bg="bg_gold_cube", crop="left", ev=[L([18, "pharaohs"], "FROM THE PHARAOHS TO TODAY"), BIG([18, "thousand"], "220,000 TONNES", y=.5)])
beat([19, "Split"], "scene", bg="bg_gold_people_world", ev=[T([19, "everyone"], "8 BILLION PEOPLE"), T([19, "twenty-seven"], "~27 GRAMS EACH", True)])
beat([20, "And"], "object", ev=[L([20, "And"], "ALL THE GOLD IN THE WORLD"),
     BARS([20, "worth"], [{"label": "ALL GOLD", "value": 27, "at": [20, "trillion"]}, {"label": "US ECONOMY / YEAR", "value": 30, "color": "mustard", "at": [20, "American"]}],
          suffix=" TRN $")])
beat([21, "Reason"], "scene", bg="bg_gold_ancient", crop="left", ev=[T([21, "Reason"], "2. NEVER RUSTS", True), T([21, "rots"], "NEVER ROTS")])
beat([22, "Gold"], "scene", bg="bg_gold_ancient", crop="right", ev=[T([22, "thousands"], "THOUSANDS OF YEARS UNDERGROUND"), T([22, "shining"], "STILL SHINES ✓", True)])
beat([23, "Reason"], "scene", bg="bg_printing_press", ev=[T([23, "print"], "3. NOBODY CAN PRINT IT", True)], sfx=[[0.2, "hit"]])
beat([24, "A"], "scene", bg="bg_printing_press", crop="left", ev=[T([24, "keystrokes"], "MONEY: A FEW KEYSTROKES")])
beat([25, "Gold"], "object", props=[P([25, "Gold"], "prop_gold", .3, .5, .45)], ev=[L([25, "Gold"], "MINED EVERY YEAR"),
     CNT([25, "mines"], 3700, suffix=" TONNES", x=.68, y=.42), T([25, "two"], "+2% A YEAR", True, x=.68, y=.6)])
beat([26, "That's"], "scene", bg="bg_lydia_mint", mood="calm", ev=[L([26, "Lydia"], "6TH CENTURY BC · LYDIA"), T([26, "coins"], "ONE OF THE FIRST COINS", True), T([26, "silver"], "GOLD + SILVER")])
# ---------------- 2: gold and money ----------------
beat([27, "That"], "chapter", num="PART 2", title="WHEN MONEY WAS GOLD")
beat([28, "Under"], "scene", bg="bg_gold_standard", ev=[L([28, "standard"], "THE GOLD STANDARD"), T([28, "paper"], "PAPER NOTE →"), T([28, "swap"], "→ GOLD", True)])
beat([29, "After"], "scene", bg="bg_conference", ev=[L([29, "Second"], "1944 · BRETTON WOODS"), T([29, "currencies"], "CURRENCIES → DOLLAR"), T([29, "tied"], "DOLLAR → GOLD", True)])
beat([29, "thirty-five"], "number", prop="prop_gold", value="$35", sub="1 OUNCE · 1944", show=[29, "thirty-five"])
beat([30, "Today's"], "object", ev=[L([30, "Today's"], "1 OUNCE OF GOLD"),
     BARS([30, "Today's"], [{"label": "1944", "value": 35}, {"label": "TODAY", "value": 3900, "hl": True, "at": [30, "hundred"]}], prefix="$"),
     ST([30, "times"], "×110+", y=.2, x=.82)])
beat([31, "Then"], "portrait", fig="fig_nixon", ev=[F([31, "Nixon"], "us", x=.9, y=.15), L([31, "1971"], "1971 · RICHARD NIXON")])
beat([31, "television"], "scene", bg="bg_tv_1971", ev=[T([32, "swapped"], "DOLLAR → GOLD ✗", True)], sfx=[[0, "hit"]])
beat([33, "From"], "scene", bg="bg_wallet", ev=[T([33, "metal"], "NOT BACKED BY ANY METAL"), T([33, "trust"], "ONLY TRUST", True)])
beat([34, "And"], "object", ev=[M([34, "And"], "e_newspaper"), T([34, "relic"], "\"A RELIC\"", True, x=.36, y=.5)])
beat([35, "None"], "map", bg="map_world", zf=[.48, .27], ev=[F([35, "Britain"], "gb"), PIN([35, "Britain"], UK), L([36, "Between"], "1999-2002 · BRITAIN")])
beat([36, "the"], "scene", bg="bg_uk_gold_sale", crop="left", ev=[T([36, "ninety-five"], "395 TONNES SOLD", True), T([36, "half"], "HALF THE COUNTRY'S GOLD")])
beat([37, "And"], "scene", bg="bg_uk_gold_sale", ev=[ST([37, "advance"], "ANNOUNCED IN ADVANCE", y=.78)], sfx=[[0, "hit"]])
beat([38, "Traders"], "scene", bg="bg_gold_trading", crop="right", ev=[T([38, "seller"], "A HUGE SELLER IS COMING"), T([38, "twenty-year"], "PRICE: 20-YEAR LOW ↓", True)])
beat([39, "Britain"], "number", prop="prop_gold", value="$275", sub="AVERAGE PRICE · 1 OUNCE", show=[39, "seventy-five"])
beat([39, "raised"], "object", ev=[L([39, "raised"], "BRITAIN'S 395 TONNES, $ BILLION"),
     BARS([39, "raised"], [{"label": "SOLD FOR", "value": 3.5, "at": [39, "three"]}, {"label": "WORTH TODAY", "value": 50, "hl": True, "at": [40, "fifty"]}]),
     ST([41, "Fourteen"], "×14", y=.2, x=.82)])
beat([42, "Britain"], "object", ev=[L([42, "Britain"], "GOLD PER PERSON"), BIG([42, "four"], "4.5 GRAMS", y=.5), T([42, "left"], "BRITAIN NOW: 310 TONNES", True, y=.7)])
beat([43, "Economists"], "scene", bg="bg_uk_gold_sale", crop="right", ev=[ST([43, "wrong"], "THE WRONG MOMENT", y=.78)])
beat([44, "If"], "object", sfx=[[0, "ding"]], ev=[M([44, "If"], "e_presenting"), {"at": [44, "subscribe"], "k": "subscribe", "x": .4, "y": .45, "dur": 3.4}])
# ---------------- 3: why buy again ----------------
beat([45, "So"], "chapter", num="PART 3", title="WHY ARE BANKS BUYING AGAIN?")
beat([46, "The"], "scene", bg="bg_moscow_vault", mood="dramatic", ev=[L([46, "2022"], "2022"), F([47, "Russia"], "ru")])
beat([47, "Western"], "scene", bg="bg_vault_empty", ev=[T([47, "froze"], "~$300 BILLION FROZEN", True), ST([47, "abroad"], "FROZEN", y=.78)], sfx=[[0, "hit"]])
beat([48, "Overnight"], "scene", bg="bg_treasury", ev=[T([48, "lesson"], "EVERY GOVERNMENT LEARNED A LESSON", True)])
beat([49, "Dollars"], "scene", bg="bg_treasury", crop="right", ev=[T([49, "someone"], "MONEY IN SOMEONE ELSE'S BANK"), T([49, "agrees"], "= THEIR DECISION", True)])
beat([50, "Gold"], "scene", bg="bg_vault", ev=[T([50, "own"], "GOLD IN YOUR OWN VAULT"), ST([50, "frozen"], "CAN'T BE FROZEN", y=.78)])
beat([51, "What"], "scene", bg="bg_gold_delivery", ev=[T([51, "spree"], "A BUYING SPREE", True)], sfx=[[0, "cash"]])
beat([52, "Central"], "object", ev=[L([52, "Central"], "CENTRAL BANK BUYING, TONNES / YEAR"),
     BARS([52, "Central"], [{"label": "2010-21", "value": 470, "at": [52, "decade"]}, {"label": "2022-24", "value": 1000, "hl": True, "at": [52, "thousand"]},
                            {"label": "2025", "value": 863, "at": [53, "sixty-three"]}])])
beat([54, "The"], "map", bg="map_world", zf=[.6, .3], ev=[PIN([54, "China"], CN), PIN([54, "Russia"], RU), T([54, "wasn't"], "BIGGEST BUYER?", True, x=.5, y=.85)])
beat([55, "It"], "scene", bg="bg_warsaw_gold", ev=[F([55, "Poland"], "pl"), L([55, "Poland"], "BIGGEST BUYER · POLAND"), T([55, "hundred"], "2025: 102 TONNES", True)], sfx=[[0, "ding"]])
beat([56, "Some"], "scene", bg="bg_gold_plane", ev=[T([56, "back"], "BRINGING THE GOLD HOME", True)])
beat([57, "Between"], "map", bg="map_world", zf=[.4, .3], ev=[F([57, "Germany"], "de"), L([57, "Between"], "2013-2017 · GERMANY"),
     AR([57, "York"], NY, DE), AR([57, "Paris"], PARIS, DE), PIN([57, "Frankfurt"], DE)])
beat([57, "six"], "scene", bg="bg_gold_plane", crop="right", ev=[T([57, "seventy-four"], "674 TONNES HOME", True), L([57, "Frankfurt"], "FRANKFURT")])
beat([58, "And"], "scene", bg="bg_central_bank", mood="calm", ev=[T([58, "shift"], "HOW BIG IS THE SHIFT?", True)], sfx=[[0, "swoosh"]])
beat([59, "According"], "object", ev=[L([59, "According"], "WORLD CENTRAL BANK RESERVES · END 2025"),
     BARS([59, "made"], [{"label": "GOLD", "value": 27, "hl": True, "at": [59, "twenty-seven"]}, {"label": "US TREASURIES", "value": 22, "at": [60, "twenty-two"]},
                         {"label": "EURO", "value": 15, "at": [60, "fifteen"]}], suffix="%", w=.6)])
beat([61, "Gold"], "scene", bg="bg_vault", crop="right", ev=[ST([61, "biggest"], "NO. 1", y=.3, x=.7)])
# ---------------- 4: America and Britain ----------------
beat([62, "But"], "chapter", num="PART 4", title="WHO HAS THE MOST GOLD?")
beat([63, "It"], "object", ev=[L([63, "It"], "BIGGEST GOLD RESERVES, TONNES"),
     BARS([63, "It"], [{"label": "USA", "value": 8133, "hl": True, "at": [63, "eight"]}, {"label": "GERMANY", "value": 3350}, {"label": "UK", "value": 310}])])
beat([64, "About"], "scene", bg="bg_fort_knox", ev=[L([64, "Knox"], "FORT KNOX · KENTUCKY"), T([64, "half"], "≈ HALF OF AMERICA'S GOLD", True)])
beat([65, "No"], "scene", bg="bg_fort_knox", crop="right", ev=[ST([65, "visitors"], "NO VISITORS", y=.78)])
beat([66, "At"], "number", prop="prop_gold", value="$1 TRILLION", sub="US GOLD AT TODAY'S PRICE", show=[66, "trillion"])
beat([67, "But"], "object", ev=[M([67, "But"], "e_surprised"), T([67, "strange"], "THE STRANGE PART", True, x=.36, y=.5)], sfx=[[0, "hit"]])
beat([68, "On"], "scene", bg="bg_treasury", ev=[L([68, "1973"], "SET BY LAW · 1973"), T([68, "forty-two"], "$42.22 AN OUNCE", True)])
beat([69, "At"], "object", ev=[L([69, "At"], "US GOLD, $ BILLION"),
     BARS([69, "At"], [{"label": "REAL VALUE", "value": 1020}, {"label": "ON THE BOOKS", "value": 11, "color": "red", "at": [69, "eleven"]}])])
beat([70, "Shared"], "object", ev=[L([70, "Shared"], "GOLD PER PERSON, GRAMS"),
     BARS([70, "Shared"], [{"label": "USA", "value": 24, "hl": True, "at": [70, "twenty-four"]}, {"label": "UK", "value": 4.5, "at": [70, "British"]}])])
beat([71, "And"], "scene", bg="bg_boe_vault", ev=[L([71, "London"], "BANK OF ENGLAND · LONDON"), T([71, "thousand"], "400,000+ BARS", True), T([71, "million"], "EACH ≈ $1.5 MILLION")])
beat([72, "Most"], "scene", bg="bg_boe_vault", crop="right", ev=[T([72, "other"], "MOSTLY OTHER COUNTRIES' GOLD", True)])
# ---------------- 5: gold and you ----------------
beat([73, "But"], "chapter", num="PART 5", title="SHOULD ORDINARY PEOPLE CARE?")
beat([74, "In"], "scene", bg="bg_costco_gold", ev=[L([74, "Costco"], "COSTCO · 2024"), T([74, "hundred"], "$100-200 MILLION A MONTH", True),
     T([74, "toilet"], "NEXT TO THE TOILET PAPER")], sfx=[[0.5, "cash"]])
beat([75, "So"], "object", ev=[M([75, "So"], "e_pointer"), T([75, "facts"], "3 FACTS", True, x=.36, y=.42), T([75, "ads"], "THE ADS SKIP", x=.36, y=.57)])
beat([76, "Fact"], "object", ev=[M([76, "Fact"], "e_piggy"), T([76, "nothing"], "1. GOLD PAYS NOTHING", True, x=.36, y=.35),
     T([77, "interest"], "SAVINGS: INTEREST ✓", x=.36, y=.5), T([77, "only"], "GOLD: ONLY IF PRICE ↑", x=.36, y=.62)])
beat([78, "Fact"], "scene", bg="bg_gold_trading", crop="right", ev=[T([78, "fall"], "2. IT CAN FALL HARD", True), T([78, "stay"], "AND STAY DOWN")])
beat([79, "In"], "scene", bg="bg_gold_1980", ev=[L([79, "1980"], "JANUARY 1980"), T([79, "fifty"], "1 OUNCE = $850")])
beat([80, "It"], "object", ev=[M([80, "It"], "e_calculator"), BIG([80, "twenty-eight"], "28 YEARS", x=.36, y=.42), T([81, "2008"], "BREAK EVEN: 2008", True, x=.36, y=.62)])
beat([82, "Fact"], "scene", bg="bg_gold_spread", ev=[T([82, "gap"], "3. BUY PRICE ≠ SELL PRICE", True)])
beat([83, "On"], "scene", bg="bg_gold_spread", crop="right", ev=[T([83, "several"], "GAP: SEVERAL %"), ST([83, "less"], "YOU WALK AWAY WITH LESS", y=.78)])
beat([84, "That's"], "object", ev=[M([84, "That's"], "e_gold"), T([84, "quickly"], "GET RICH QUICK ✗", x=.36, y=.42), T([84, "protection"], "LONG-TERM PROTECTION ✓", True, x=.36, y=.57)])
# ---------------- The debate ----------------
beat([85, "And"], "scene", bg="bg_debate_scale", mood="calm", ev=[L([85, "camps"], "TWO CAMPS")])
beat([86, "Camp"], "scene", bg="bg_war", ev=[T([86, "reliable"], "CAMP 1: SAFEST STORE OF WEALTH", True), T([86, "war"], "WAR · SANCTIONS · INFLATION")])
beat([87, "Camp"], "object", ev=[M([87, "Camp"], "e_scale"), T([87, "rock"], "CAMP 2: \"A ROCK THAT SITS THERE\"", True, x=.36, y=.5)])
beat([88, "Its"], "portrait", fig="buffett_cut", ev=[F([88, "Warren"], "us", x=.9, y=.15), L([88, "Warren"], "WARREN BUFFETT"), T([89, "2011"], "2011 · SHAREHOLDER LETTER", x=.3, y=.85)])
beat([90, "Back"], "number", prop="prop_gold", value="$9.6 TRILLION", sub="ALL THE WORLD'S GOLD · 2011", show=[90, "nine"])
beat([91, "With"], "scene", bg="bg_buffett_compare", ev=[T([91, "farmland"], "ALL US FARMLAND")])
beat([91, "sixteen"], "scene", bg="bg_buffett_compare", crop="right", ev=[T([91, "sixteen"], "+ 16 EXXON MOBILS"), T([92, "trillion"], "+ $1 TRILLION LEFT OVER", True)])
beat([93, "The"], "scene", bg="bg_buffett_compare", crop="left", ev=[T([93, "farms"], "LAND, COMPANIES = INCOME ✓"), T([93, "nothing"], "GOLD = NOTHING ✗", True)])
beat([94, "So"], "scene", bg="bg_debate_scale", crop="right", ev=[T([94, "right"], "WHO'S RIGHT?", True), T([95, "both"], "IN A WAY, BOTH")], sfx=[[0, "tick"]])
beat([96, "Gold"], "object", ev=[M([96, "Gold"], "e_gold"), T([96, "machine"], "WEALTH MACHINE ✗", x=.36, y=.42), T([96, "safe"], "A SAFE ✓", True, x=.36, y=.57)])
# ---------------- What it means for you ----------------
beat([97, "So"], "chapter", num="YOUR MONEY", title="WHAT DOES THIS MEAN FOR YOU?")
beat([98, "First"], "scene", bg="bg_crisis_gold", ev=[T([98, "gauge"], "1. GOLD = A FEAR GAUGE", True), T([98, "wars"], "WARS · DEBT · INFLATION")])
beat([99, "Second"], "scene", bg="bg_treasury", crop="left", ev=[T([99, "instead"], "2. GOLD INSTEAD OF US BONDS", True), T([99, "confidence"], "LESS CONFIDENCE IN THE DOLLAR")])
beat([99, "currency"], "scene", bg="bg_wallet", crop="right", ev=[T([99, "pay"], "YOUR PAY · RENT · SAVINGS")])
beat([100, "Third"], "object", ev=[M([100, "Third"], "e_magnifier"), T([100, "advertised"], "3. \"SAFE\" IN ADS?", True, x=.36, y=.4),
     T([100, "1980"], "REMEMBER 1980", x=.36, y=.55), T([100, "drop"], "AND -30% THIS YEAR", x=.36, y=.68)])
beat([101, "This"], "scene", bg="bg_bank_desk", ev=[T([101, "advice"], "NOT FINANCIAL ADVICE"), T([101, "numbers"], "JUST THE NUMBERS", True)])
# ---------------- The answer ----------------
beat([102, "So"], "title", title="THE ANSWER", title2="WHY ARE BANKS BUYING GOLD?")
beat([103, "Because"], "scene", bg="bg_crisis_gold", crop="left", ev=[T([103, "safe"], "THE WORLD FEELS LESS SAFE"), T([103, "promise"], "NOBODY ELSE'S PROMISE", True)])
beat([104, "It"], "scene", bg="bg_vault", ev=[T([104, "frozen"], "CAN'T BE FROZEN"), T([104, "printed"], "CAN'T BE PRINTED"), T([104, "thousands"], "THOUSANDS OF YEARS", True)])
beat([105, "But"], "scene", bg="bg_gold_trading", crop="left", ev=[T([105, "risk-free"], "BUT NOT RISK-FREE", True), T([105, "rises"], "PRICE ↑↓")])
beat([106, "Gold"], "object", ev=[M([106, "Gold"], "e_gold"), T([106, "quickly"], "RICH QUICK ✗", x=.36, y=.42), T([106, "safe"], "WEALTH KEPT SAFE ✓", True, x=.36, y=.57)])
beat([107, "That's"], "title", title="THAT'S THE STORY OF GOLD", title2="AND NOW YOU KNOW THE NUMBERS")
beat([109, "So"], "object", ev=[M([109, "So"], "e_scale"), T([109, "gold"], "TEAM GOLD...", x=.36, y=.38),
     T([109, "Buffett"], "...OR TEAM BUFFETT?", True, x=.36, y=.55), T([110, "comments"], "TELL ME IN THE COMMENTS", x=.36, y=.72),
     {"at": [109, "camp"], "k": "like", "x": .82, "y": .2}])
beat([111, "Next"], "scene", bg="bg_wallet", ev=[T([111, "Next"], "NEXT TIME"), T([111, "prices"], "WHY PRICES NEVER COME DOWN", True)])
beat([112, "Subscribe"], "end", pose="e_presenting", ev=[{"at": [112, "Subscribe"], "k": "subscribe", "x": .47, "y": .35, "dur": 3.4}])

VF = {(17, "That's"): {"vfocus": [0.3, 0.72]}}
for _d in B:
    if _d["type"] in ("scene", "portrait", "map"):
        _d.update(VF.get(tuple(_d["at"]), {}))

cfg = {"layers": "layers", "lang": "en",
       "auto_skip": ["Buffett", "Exxon", "Fargo", "Costco", "Knox"],
       "music": {"curious": "../../../assets/music/curious.mp3", "dramatic": "../../../assets/music/dramatic.mp3", "calm": "../../../assets/music/calm.mp3"},
       "mascot": {"img": "e_presenting", "parts": 1, "full_body": True},
       "ui": {"subscribe": "SUBSCRIBE", "subscribed": "SUBSCRIBED", "like": "LIKE", "next": "WATCH NEXT"},
       "sentences": S, "beats": B,
       "shorts": [{"name": "crash", "from": [0, "In"], "to": [5, "So"], "hook": "GOLD CRASHED. BANKS BOUGHT MORE"},
                  {"name": "cube", "from": [12, "Reason"], "to": [20, "And"], "hook": "ALL THE GOLD EVER MINED"},
                  {"name": "britain", "from": [35, "None"], "to": [43, "Economists"], "hook": "THE WORST GOLD SALE IN HISTORY"},
                  {"name": "freeze", "from": [46, "The"], "to": [55, "It"], "hook": "WHY BANKS ARE HOARDING GOLD"},
                  {"name": "fortknox", "from": [62, "But"], "to": [69, "At"], "hook": "$1 TRILLION, BOOKED AT $11 BILLION"},
                  {"name": "costco", "from": [74, "In"], "to": [84, "That's"], "hook": "BEFORE YOU BUY GOLD"},
                  {"name": "buffett", "from": [87, "Camp"], "to": [96, "Gold"], "hook": "WHY BUFFETT HATES GOLD"}],
       "end_hold": 9, "pauses": {"15": 1.5, "44": 1.0, "45": 1.0}, "end_slots": 2, "end_next": "WHY PRICES NEVER COME DOWN",
       "series_label": "EP 1: GOLD", "handle": "@EldorExplains",
       "socials": [["youtube", "@EldorExplains"], ["instagram", "@EldorExplains"], ["tiktok", "@EldorExplains"], ["facebook", "@EldorExplains"], ["telegram", "@EldorExplains"]]}
json.dump(cfg, open("ee01_beats.json", "w"), ensure_ascii=False, indent=1)
print(len(B), "beats")
