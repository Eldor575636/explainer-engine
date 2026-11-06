#!/usr/bin/env python3
"""Turn a caption script into text a TTS voice reads correctly (Uzbek).

Captions keep the original spelling; only the text sent to the voice changes:
- numbers, years and dates are written out in Uzbek words (1944-yilda -> ming to'qqiz yuz qirq to'rtinchi yilda)
- abbreviations are expanded or spelled phonetically (AQSh dollari -> Amerika dollari the first time, then dollar)
- extra entries come from lexicon.json (word -> spoken form), shared across episodes

Usage: python3 voice_text.py <sentences.json> <out.json>   (writes {"voice": [...]} one entry per sentence)
"""
import json, re, sys
from pathlib import Path

ONES = ["", "bir", "ikki", "uch", "to'rt", "besh", "olti", "yetti", "sakkiz", "to'qqiz"]
TENS = ["", "o'n", "yigirma", "o'ttiz", "qirq", "ellik", "oltmish", "yetmish", "sakson", "to'qson"]


def words(n):
    if n == 0:
        return "nol"
    out = []
    for val, name in ((10 ** 9, "milliard"), (10 ** 6, "million"), (1000, "ming")):
        if n >= val:
            q, n = divmod(n, val)
            out += ([] if (q == 1 and name == "ming") else [words(q)]) + [name]
    if n >= 100:
        q, n = divmod(n, 100)
        out += ([ONES[q]] if q > 1 else []) + ["yuz"]
    if n >= 10:
        out.append(TENS[n // 10]); n %= 10
    if n:
        out.append(ONES[n])
    return " ".join(out)


def ordinal(n):
    w = words(n)
    if w.endswith("ellik"):                     # ellik -> elliginchi (k softens before a vowel)
        w = w[:-1] + "g"
    return w + ("nchi" if w[-1] in "aeiou" else "inchi")


LEX = json.loads((Path(__file__).parent / "lexicon.json").read_text(encoding="utf-8"))


def to_voice(sentences):
    seen = set()
    out = []
    for s in sentences:
        v = s
        # first-mention rules for AQSh
        def aqsh(m):
            suffix = m.group(1) or ""
            if m.group(2):                                  # "AQSh dollari"
                key = "dollar"
                full = "Amerika dollari" if key not in seen else "dollar"
                seen.add(key)
                return full + m.group(2)[len(" dollari"):]
            key = "aqsh"
            base = "Amerika Qo'shma Shtatlari" if key not in seen else "Amerika"
            seen.add(key)
            if suffix and base.endswith("i"):
                suffix = {"da": "da", "ning": "ning", "ga": "ga", "dan": "dan"}.get(suffix, suffix)
            return base + suffix
        v = re.sub(r"AQSh(da|ning|ga|dan)?( dollari\w*)?", aqsh, v)
        for k, w in LEX.items():
            v = re.sub(r"\b" + re.escape(k), w, v)
        # years / ordinals: 1944-yil, 1930-yillar, 15-avgust
        v = re.sub(r"(\d+)-(yil\w*|avgust|sentabr|iyul|yanvar|fevral|mart|aprel|may|iyun|oktabr|noyabr|dekabr)",
                   lambda m: ordinal(int(m.group(1))) + " " + m.group(2), v)
        v = re.sub(r"(\d+) (ta\w*)", lambda m: words(int(m.group(1))) + m.group(2), v)   # 9 tasining -> to'qqiztasining
        v = re.sub(r"\d[\d ]*\d|\d", lambda m: words(int(m.group(0).replace(" ", ""))), v)
        v = re.sub(r"\s*[—–]\s*", ", ", v)
        out.append(v[:1].upper() + v[1:])
    return out


if __name__ == "__main__":
    src = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    sents = src["sentences"] if isinstance(src, dict) else src
    json.dump({"voice": to_voice(sents)}, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
