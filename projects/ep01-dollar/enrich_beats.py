"""Adds country flags on every country mention and two extra scenes (ships, Chinese port) to ep01_beats.json
-> ep01_beats_enriched.json. Flags are screen-layer cards that pop in on the spoken word."""
import json, copy
from pathlib import Path
here = Path(__file__).parent
b = json.load(open(here / "ep01_beats.json", encoding="utf-8"))
S = b["sentences"]


def widx(at):
    si, pre = at
    ws = S[si].split()
    return next((i for i, w in enumerate(ws) if w.lower().strip("«»\"'.,:;?!").startswith(pre.lower())), 0)


def key(at):
    return (at[0], widx(at))


def insert_beat(nb, move_from=None):
    """Insert a beat; events of the previous beat at/after its start move into it."""
    k = key(nb["at"])
    i = max(j for j, x in enumerate(b["beats"]) if key(x["at"]) <= k)
    prev = b["beats"][i]
    moved = [e for e in prev.get("ev", []) if key(e["at"]) >= k]
    prev["ev"] = [e for e in prev.get("ev", []) if key(e["at"]) < k]
    nb.setdefault("ev", []); nb["ev"] = moved + nb["ev"]
    b["beats"].insert(i + 1, nb)


insert_beat({"at": [23, "Uning"], "type": "scene", "bg": "bg_ships", "mood": "curious"})
insert_beat({"at": [128, "Xitoy"], "type": "scene", "bg": "bg_china_port", "mood": "curious"})
insert_beat({"at": [130, "Markaziy"], "type": "object", "mood": "curious"})

FLAGS = [  # (sentence, word prefix, codes, x, y)
    (2, "Amerikaga", "us"), (21, "Britaniya", "gb"), (26, "Britaniyaga", "gb"), (29, "Amerikada", "us"),
    (43, "Britaniya", "gb"), (59, "Vetnam", "vn"), (63, "Fransiya", "fr"), (82, "Saudiya", "sa"),
    (83, "Saudiya", ["us", "sa"]), (91, "Yaponiya", "jp"), (91, "Germaniya", ["jp", "de"]),
    (91, "Hindiston", ["jp", "de", "in"]), (97, "yevro", "eu"), (98, "Xitoy", "cn"),
    (100, "O'zbekistondagi", "uz"), (100, "Koreyadan", ["uz", "kr"]), (109, "Eron", "ir"), (110, "Rossiya", "ru"),
    (113, "O'zbekiston", "uz"), (116, "O'zbekiston", "uz"), (121, "Rossiyadan", "ru"), (125, "Vashingtondagi", "us"),
    (128, "Xitoy", "cn"), (129, "BRIKS", ["br", "ru", "in", "cn", "za"]), (131, "O'zbekiston", "uz"),
]
for si, pre, codes in FLAGS:
    at = [si, pre]
    k = key(at)
    beat = max((x for x in b["beats"] if key(x["at"]) <= k), key=lambda x: key(x["at"]))
    ev = {"at": at, "k": "flag", "code": codes}
    if beat["type"] == "map":                      # maps: flags low-left, away from pins and arrows
        ev["y"] = 0.80
    if beat["type"] == "portrait":
        ev.update(x=0.86, y=0.2)
    if len(ev["code"]) == 5 if isinstance(ev["code"], list) else False:   # BRIKS row: wide, centred low
        ev.update(x=0.5, y=0.76)
    beat.setdefault("ev", []).append(ev)

# no empty moments: a keyword on "O'zgarish belgilari bor", gold bars right on "Markaziy banklar"
for x in b["beats"]:
    if x["at"][0] == 127:
        x.setdefault("ev", []).append({"at": [127, "O'zgarish"], "k": "label", "text": "O'ZGARISH BELGILARI"})
    for e in x.get("ev", []):
        if e["k"] == "prop" and e.get("img") == "prop_gold" and e["at"][0] == 130:
            e["at"] = [130, "Markaziy"]
json.dump(b, open(here / "ep01_beats_enriched.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(b["beats"]), "beats,", sum(1 for x in b["beats"] for e in x.get("ev", []) if e["k"] == "flag"), "flags")
