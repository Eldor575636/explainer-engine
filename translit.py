"""Cyrillic (Uzbek/Kazakh-style) to Uzbek Latin. Whisper sometimes answers Uzbek audio in Cyrillic."""
M = {'а': 'a', 'ә': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'ғ': "g'", 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'j', 'з': 'z',
     'и': 'i', 'й': 'y', 'к': 'k', 'қ': 'q', 'л': 'l', 'м': 'm', 'н': 'n', 'ң': 'ng', 'о': 'o', 'ө': "o'", 'п': 'p',
     'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ұ': 'u', 'ү': 'u', 'ў': "o'", 'ф': 'f', 'х': 'x', 'һ': 'h', 'ц': 'ts',
     'ч': 'ch', 'ш': 'sh', 'щ': 'sh', 'ъ': "'", 'ы': 'i', 'і': 'i', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'}


def to_latin(s):
    return "".join(M.get(c.lower(), c) for c in s)
