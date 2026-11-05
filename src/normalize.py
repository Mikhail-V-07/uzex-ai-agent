"""Normalisation helpers: canonical product families, brand/size/sort/type/class parsing,
Uzbek Cyrillic <-> Latin transliteration and phonetic keys for fuzzy entity search, region names."""
from __future__ import annotations

import re

# (latin as in deals/participants, Russian short, Russian as in contracts.csv)
REGIONS = [
    ("Toshkent shahri", "Ташкент (город)", "г. Ташкент"),
    ("Toshkent viloyati", "Ташкентская область", "Ташкентская область"),
    ("Samarqand viloyati", "Самаркандская область", "Самаркандская область"),
    ("Buxoro viloyati", "Бухарская область", "Бухарская область"),
    ("Qashqadaryo viloyati", "Кашкадарьинская область", "Кашкадарьинская область"),
    ("Namangan viloyati", "Наманганская область", "Наманганская область"),
    ("Andijon viloyati", "Андижанская область", "Андижанская область"),
    ("Surxondaryo viloyati", "Сурхандарьинская область", "Сурхандарьинская область"),
    ("Farg‘ona viloyati", "Ферганская область", "Ферганская область"),
    ("Navoiy viloyati", "Навоийская область", "Навоийская область"),
    ("Qoraqalpog‘iston Respublikasi", "Республика Каракалпакстан", "Республика Каракалпакстан"),
    ("Xorazm viloyati", "Хорезмская область", "Хорезмская область"),
    ("Jizzax viloyati", "Джизакская область", "Джизакская область"),
    ("Sirdaryo viloyati", "Сырдарьинская область", "Сырдарьинская область"),
]

# ordered rules: (predicate keywords (all must match), RU family, UZ family)
FAMILY_RULES = [
    (["хлоп", "сырец"], "Хлопок-сырец", "Paxta xomashyosi"),
    (["пряжа"], "Пряжа хлопчатобумажная", "Paxta ipi (kalava)"),
    (["шрот"], "Шрот хлопковый", "Paxta shroti"),
    (["масло", "хлопк"], "Масло хлопковое", "Paxta yog‘i"),
    (["подсолнеч"], "Масло подсолнечное", "Kungaboqar yog‘i"),
    (["мук"], "Мука пшеничная", "Bug‘doy uni"),
    (["пшениц"], "Пшеница", "Bug‘doy"),
    (["рис"], "Рис", "Guruch"),
    (["сахар"], "Сахар", "Shakar"),
    (["вод"], "Вода питьевая", "Ichimlik suvi"),
    (["комбикорм"], "Комбикорм", "Omuxta yem"),
    (["кормосмес"], "Комбикорм", "Omuxta yem"),
    (["соль"], "Соль пищевая", "Osh tuzi"),
    (["гипс"], "Гипс", "Gips"),
    (["извест"], "Известь", "Ohak"),
    (["цемент"], "Цемент", "Sement"),
    (["бензин"], "Бензин", "Benzin"),
    (["дизел"], "Дизельное топливо", "Dizel yoqilg‘isi"),
    (["мазут"], "Мазут", "Mazut"),
    (["аргон"], "Аргон", "Argon"),
    (["газ"], "Сжиженный газ", "Suyultirilgan gaz"),
    (["битум"], "Битум", "Bitum"),
    (["азот"], "Азот", "Azot"),
    (["серн"], "Серная кислота", "Sulfat kislota"),
    (["сода"], "Сода каустическая", "Kaustik soda"),
    (["карбамид"], "Карбамид", "Karbamid"),
    (["мочевин"], "Карбамид", "Karbamid"),
    (["селитр"], "Аммиачная селитра", "Ammiakli selitra"),
    (["эмаль"], "Эмаль", "Emal (bo‘yoq)"),
    (["труб"], "Трубы полиэтиленовые", "Polietilen quvurlar"),
    (["полиэтилен"], "Полиэтилен", "Polietilen"),
    (["полипропилен"], "Полипропилен", "Polipropilen"),
    (["поливинил"], "Поливинилхлорид", "Polivinilxlorid (PVX)"),
    (["пиломат"], "Пиломатериалы", "Yog‘och-taxta materiallari"),
    (["кирпич"], "Кирпич", "G‘isht"),
    (["стекло"], "Стекло", "Shisha (oyna)"),
    (["проволок"], "Проволока арматурная", "Armatura simi"),
    (["лист"], "Лист стальной", "Po‘lat list"),
    (["арматур"], "Арматура", "Armatura"),
    (["катод"], "Катод медный", "Mis katod"),
    (["алюмин"], "Алюминиевый профиль", "Alyuminiy profil"),
    (["подшипник"], "Подшипник", "Podshipnik"),
    (["кабель"], "Кабель силовой", "Kuch kabeli"),
]


def family_of(name: str) -> tuple[str, str | None]:
    n = (name or "").lower()
    for keys, ru, uz in FAMILY_RULES:
        if all(k in n for k in keys):
            return ru, uz
    return (name or "").strip(), None


def _parse_grade_token(tok: str) -> str:
    t = tok.lower().strip()
    if t in ("в/с",) or t.startswith("высш"):
        return "высший"
    if t in ("1", "i") or t.startswith("перв"):
        return "1"
    if t in ("2", "ii") or t.startswith("втор"):
        return "2"
    if t in ("3", "iii") or t.startswith("трет"):
        return "3"
    if t in ("4", "iv") or t.startswith("четв"):
        return "4"
    return t


def sort_of(text: str | None, raw_sort: str | None = None, hs_code: str | int | None = None) -> str | None:
    if str(hs_code or "") == "280421":
        return None
    s = f"{raw_sort or ''} {text or ''}".lower()
    if "в/с" in s or "высш" in s:
        return "высший"
    m = re.search(r"(?<![а-яa-z0-9])(перв\w+|втор\w+|трет\w+|[123]|iii|ii|i)\s*[-–]?\s*сорт", s)
    if m:
        return _parse_grade_token(m.group(1))
    m = re.search(r"сорт\s*[-–:]?\s*(перв\w+|втор\w+|трет\w+|[123]|iii|ii|i)\b", s)
    if m:
        return _parse_grade_token(m.group(1))
    return None


def class_of(text: str | None, raw_class: str | None = None, hs_code: str | int | None = None) -> str | None:
    s = f"{raw_class or ''} {text or ''}"
    if re.search(r"А500С|A500C", s, re.I):
        return "А500С"
    sl = s.lower()
    m = re.search(r"(?<![а-яa-z0-9])(перв\w+|втор\w+|трет\w+|четв\w+|[1234]|iv|iii|ii|i)\s*[-–]?\s*класс", sl)
    if m:
        return _parse_grade_token(m.group(1))
    m = re.search(r"класс\s*[-–:]?\s*(перв\w+|втор\w+|трет\w+|четв\w+|[1234]|iv|iii|ii|i)\b", sl)
    if m:
        return _parse_grade_token(m.group(1))
    return None


def brand_of(text: str | None, raw_brand: str | None = None, hs_code: str | int | None = None) -> str | None:
    s = f"{raw_brand or ''} {text or ''}"
    su = s.upper()
    hs_str = str(hs_code or "")
    for b in ("М00К", "М0К"):
        if b in su:
            return "М00к" if b == "М00К" else "М0к"
    for b in (
        "АИ-80", "АИ-92", "АИ-95", "ДТ-Л-К5", "ДТ-З-К5", "ДТ-Е-К5",
        "М-100", "М-125", "М-150", "М-40", "ПБА", "ПБТ",
        "БНД 60/90", "БНД 70/100", "БНД 90/130",
        "Г-5", "Г-6", "КС-65", "КС-70", "ПФ-115",
        "LL-0218", "HD-5502", "HD-6018", "LD-1825", "PE-3015",
        "PP-0350", "PP-1102", "PP-2310", "SG-5", "SG-7",
        "6205", "6210", "6305", "6312", "ВВГ 3Х2,5", "ВВГ 3Х4",
    ):
        if b in su:
            return b.replace("3Х", "3х")
    if "NE 20/1" in su:
        return "Ne 20/1"
    if "NE 24/1" in su:
        return "Ne 24/1"
    if "СТ3СП" in su:
        return "Ст3сп"
    if "ВР-1" in su:
        return "Вр-1"
    if re.search(r"ЦЕМ\s*I\s*42[.,]5\s*Н", su):
        return "ЦЕМ I 42,5Н"
    if re.search(r"ЦЕМ\s*II/А-Ш\s*32[.,]5\s*Н", su):
        return "ЦЕМ II/А-Ш 32,5Н"
    if re.search(r"ЦЕМ\s*II/В-К\s*32[.,]5\s*Н", su):
        return "ЦЕМ II/В-К 32,5Н"
    if hs_str in ("310210", "310230") and (raw_brand == "Б" or re.search(r"\bМАРКА\s+Б\b", su) or hs_str in ("310210", "310230")):
        if raw_brand == "Б" or re.search(r"\bМАРКА\s+Б\b", su):
            return "Б"
    if hs_str == "280421" and (raw_brand or "высш" in s.lower()):
        return "высший"
    return (raw_brand or "").strip() or None


def size_of(text: str | None, raw_size: str | None = None, hs_code: str | int | None = None) -> str | None:
    s = f"{raw_size or ''} {text or ''}"
    su = s.upper()
    if "0,5" in su and "Л" in su:
        return "0,5л"
    if "1,5" in su and "Л" in su:
        return "1,5л"
    m = re.search(r"Ø\s*(\d+)\s*ММ", su)
    if m:
        return f"Ø{m.group(1)}мм"
    m = re.search(r"(\d+[ХX]\d+(?:[ХX]\d+)?)\s*ММ", su)
    if m:
        return m.group(1).lower().replace("x", "х") + "мм"
    m = re.search(r"\b([4568])\s*ММ\b", su)
    if m:
        return f"{m.group(1)}мм"
    return (raw_size or "").strip() or None


def type_of(text: str | None, raw_type: str | None = None, hs_code: str | int | None = None) -> str | None:
    s = f"{raw_type or ''} {text or ''}".lower()
    if "обогащ" in s:
        return "обогащенная витаминно-минеральной смесью"
    if "хлебопекар" in s:
        return "хлебопекарная"
    if "дезодорир" in s:
        return "рафинированное дезодорированное"
    if "рафинир" in s:
        return "рафинированное"
    if "тостир" in s:
        return "тостированный"
    if "йодир" in s:
        return "йодированная"
    if "дорожн" in s:
        return "дорожный"
    if "технич" in s:
        return "техническая"
    if "тверд" in s:
        return "твердая"
    if "суспенз" in s:
        return "суспензионный"
    if "хвойн" in s:
        return "обрезные хвойных пород"
    return (raw_type or "").strip().lower() or None


_CYR = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "yo", "ж": "j", "з": "z", "и": "i",
    "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t",
    "у": "u", "ф": "f", "х": "x", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "sh", "ъ": "", "ы": "i", "ь": "",
    "э": "e", "ю": "yu", "я": "ya", "ў": "o", "қ": "q", "ғ": "g", "ҳ": "h",
}
_LEGAL = (
    r"\b(mas\s*uliyati cheklangan jamiyati|masuliyati cheklangan jamiyati|mchj|xk|aj|qk|ok|ooo|chp|"
    r"xususiy korxona|aksiyadorlik jamiyati|oilaviy korxona|fermer xo\s*jaligi)\b"
)


def translit_key(text: str) -> str:
    s = (text or "").lower()
    s = "".join(_CYR.get(ch, ch) for ch in s)
    s = re.sub(r"[‘’'`ʻʼ]", "", s)
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    s = re.sub(_LEGAL, " ", s)
    return re.sub(r"\s+", " ", s).strip()


def phonetic_key(text: str) -> str:
    """Phonetic key unifying common Russian/Uzbek keyboard substitutions (q/k, h/x, u/o, ts/s)."""
    k = translit_key(text)
    k = k.replace("q", "k").replace("h", "x").replace("ts", "s").replace("u", "o")
    return k
