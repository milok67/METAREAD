#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
METAREAD.PY — вытаскивает из фото ВСЕ метаданные: EXIF, GPS, IPTC, XMP.

Как пользоваться:
   1) Один раз установи Pillow:   python -m pip install pillow
   2) Перетащи один или несколько файлов на metaread.py
      или из терминала:           python metaread.py photo.jpg [photo2.jpg ...]
   3) Открывается окно-просмотрщик: Enter — дальше, p — назад, q — к итогу.
      Полный отчёт всё равно сохраняется рядом с фото:
      <имя_фото>_metadata.txt
   4) При желании можно сразу сохранить копию БЕЗ метаданных — удобно
      перед тем, как делиться фото (EXIF/GPS остаются только в отчёте).
"""

import json
import os
import re
import sys
from datetime import datetime

VERSION = "v0.9.0 Beta"
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "metaread_config.json")

BOX_W = 84          # общая ширина окна в символах
ROWS_PER_PAGE = 14  # строк данных на одной "странице" окна


# ══════════════════════════ ЦВЕТ / ОФОРМЛЕНИЕ ══════════════════════════
class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    GREEN = "\033[92m"
    GREY = "\033[90m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    RED = "\033[91m"


ANSI_RE = re.compile(r"\033\[[0-9;]*m")


def paint(text, *codes):
    return "".join(codes) + str(text) + C.RESET


def strip_ansi(text):
    return ANSI_RE.sub("", text)


def vis_len(s):
    return len(strip_ansi(s))


def pad(s, width):
    return s + " " * max(0, width - vis_len(s))


def enable_ansi():
    # включает обработку ANSI-кодов в cmd.exe / старом PowerShell
    if os.name == "nt":
        os.system("")


def trim_to(s, width):
    """Обрезает ОБЫЧНЫЙ (без ANSI-кодов) текст под видимую ширину."""
    if width <= 0:
        return ""
    if vis_len(s) <= width:
        return s
    return s[: max(0, width - 1)] + "…"


# ══════════════════════════ ОКНО ══════════════════════════
class Screen:
    """Рисует рамку целиком: очистка экрана → шапка (METAREAD v0.9.0 Beta
    строго в левом верхнем углу) → тело → подвал с подсказкой по клавишам.
    Каждый вызов page() — это одна "страница" окна, старое содержимое не
    остаётся над ней, поэтому в консоли не копится сплошной текст."""

    INNER = BOX_W - 4

    @staticmethod
    def clear():
        sys.stdout.write("\033[2J\033[3J\033[H")
        sys.stdout.flush()

    @classmethod
    def _row(cls, text=""):
        print("│ " + pad(trim_to(text, cls.INNER) if "\033[" not in text else text, cls.INNER) + " │")

    @classmethod
    def page(cls, subtitle, body, right=None, footer=None):
        cls.clear()
        w = BOX_W - 2
        print("╭" + "─" * w + "╮")

        brand_plain = "METAREAD " + VERSION  # эта часть никогда не обрезается
        inner = cls.INNER
        right_plain = right or ""
        subtitle_plain = subtitle or ""

        # 1) правая часть (файл/страница) — не больше того, что вообще осталось
        #    после бренда с минимум 2 пробелами-разделителями
        avail_right = inner - len(brand_plain) - 2
        right_plain = trim_to(right_plain, avail_right) if right_plain else ""

        # 2) подзаголовку (название секции) достаётся то, что осталось после
        #    бренда и уже посчитанной правой части
        reserved = len(brand_plain) + (5 if subtitle_plain else 0) + 2 + len(right_plain)
        avail_subtitle = inner - reserved
        subtitle_plain = trim_to(subtitle_plain, avail_subtitle) if avail_subtitle >= 3 else ""

        left = paint("METAREAD", C.GREEN, C.BOLD) + " " + paint(VERSION, C.GREY)
        if subtitle_plain:
            left += "  ·  " + paint(subtitle_plain, C.BOLD)
        right_s = paint(right_plain, C.GREY) if right_plain else ""
        gap = " " * max(1, inner - vis_len(left) - vis_len(right_s))
        cls._row(left + gap + right_s)
        print("├" + "─" * w + "┤")
        cls._row()
        for row in body:
            cls._row(row)
        cls._row()
        if footer:
            print("├" + "─" * w + "┤")
            for f in footer:
                cls._row(f)
        print("╰" + "─" * w + "╯")


def prompt(text):
    try:
        return input("  " + text).strip()
    except (EOFError, KeyboardInterrupt):
        sys.exit(0)


# ══════════════════════════ ЯЗЫК / ПЕРЕВОДЫ ══════════════════════════
TR = {
    "ru": {
        "err_title": "ОШИБКА",
        "press_enter_exit": "Нажми Enter, чтобы выйти...",
        "need_pillow": "Нужна библиотека Pillow. Установи её:  python -m pip install pillow",
        "drag_prompt": "Перетащи один или несколько файлов в это окно и нажми Enter:",
        "file_not_found": "Файл не найден: ",
        "open_failed": "Pillow не смог открыть файл: ",
        "lang_prompt": "Выбери язык:  [1] Русский   [2] English",
        "welcome_title": "добро пожаловать",
        "nav_hint": "Enter/n — дальше   p — назад   q — сразу к итогу",
        "of_file": "файл",
        "page_of": "стр.",
        "section_file": "ФАЙЛ",
        "section_image": "ИЗОБРАЖЕНИЕ",
        "section_exif_ifd0": "EXIF / IFD0 — камера и файл",
        "section_exif_sub": "EXIF SUB-IFD — параметры съёмки",
        "section_gps": "GPS — геолокация",
        "section_interop": "INTEROPERABILITY",
        "section_makernote": "MAKERNOTE — данные производителя",
        "section_ifd1": "IFD1 — встроенное превью",
        "section_exif_old": "EXIF — параметры (старый парсер)",
        "section_exif_failed": "EXIF — не удалось прочитать",
        "section_gps_map": "GPS — карта",
        "section_summary": "итог",
        "gps_not_found": "GPS-метки не найдены (координаты не записаны или стёрты).",
        "gps_privacy_warning": "⚠ В файле есть точные координаты съёмки — прежде чем делиться",
        "gps_privacy_warning2": "  фото, подумай, не раскрывает ли это твоё местоположение.",
        "section_iptc": "IPTC — описание и права",
        "section_xmp": "XMP — редактор и история (сырые данные)",
        "section_icc": "ICC — цветовой профиль",
        "field_name": "Имя",
        "field_path": "Путь",
        "field_size": "Размер",
        "field_modified": "Изменён",
        "field_format": "Формат",
        "field_resolution": "Разрешение",
        "field_megapixels": "Мегапиксели",
        "field_colormode": "Цветовой режим",
        "field_frames": "Кадров",
        "field_lat": "Широта",
        "field_lon": "Долгота",
        "field_gmaps": "Google Maps",
        "field_ymaps": "Яндекс Карта",
        "field_error": "Ошибка",
        "field_xmp": "XMP",
        "field_icc_profile": "Профиль",
        "total_fields": "Всего полей",
        "report_saved": "Отчёт сохранён: ",
        "report_save_failed": "Не удалось сохранить отчёт: ",
        "press_enter_close": "Нажми Enter, чтобы закрыть окно...",
        "strip_prompt": "Сохранить рядом копию БЕЗ метаданных (безопасно для публикации)? [y/N]: ",
        "strip_saved": "Чистая копия сохранена: ",
        "strip_failed": "Не удалось создать чистую копию: ",
        "no_data": "Метаданных не найдено.",
    },
    "en": {
        "err_title": "ERROR",
        "press_enter_exit": "Press Enter to exit...",
        "need_pillow": "Pillow library is required. Install it:  python -m pip install pillow",
        "drag_prompt": "Drag one or more files into this window and press Enter:",
        "file_not_found": "File not found: ",
        "open_failed": "Pillow failed to open the file: ",
        "lang_prompt": "Choose language:  [1] Русский   [2] English",
        "welcome_title": "welcome",
        "nav_hint": "Enter/n — next   p — back   q — jump to summary",
        "of_file": "file",
        "page_of": "page",
        "section_file": "FILE",
        "section_image": "IMAGE",
        "section_exif_ifd0": "EXIF / IFD0 — camera & file",
        "section_exif_sub": "EXIF SUB-IFD — shooting parameters",
        "section_gps": "GPS — location",
        "section_interop": "INTEROPERABILITY",
        "section_makernote": "MAKERNOTE — manufacturer data",
        "section_ifd1": "IFD1 — embedded thumbnail",
        "section_exif_old": "EXIF — parameters (legacy parser)",
        "section_exif_failed": "EXIF — failed to read",
        "section_gps_map": "GPS — map",
        "section_summary": "summary",
        "gps_not_found": "No GPS tags found (coordinates not recorded or already stripped).",
        "gps_privacy_warning": "⚠ This file has exact shooting coordinates — think twice before",
        "gps_privacy_warning2": "  sharing it, it can reveal your location.",
        "section_iptc": "IPTC — description & rights",
        "section_xmp": "XMP — editor & history (raw data)",
        "section_icc": "ICC — color profile",
        "field_name": "Name",
        "field_path": "Path",
        "field_size": "Size",
        "field_modified": "Modified",
        "field_format": "Format",
        "field_resolution": "Resolution",
        "field_megapixels": "Megapixels",
        "field_colormode": "Color mode",
        "field_frames": "Frames",
        "field_lat": "Latitude",
        "field_lon": "Longitude",
        "field_gmaps": "Google Maps",
        "field_ymaps": "Yandex Map",
        "field_error": "Error",
        "field_xmp": "XMP",
        "field_icc_profile": "Profile",
        "total_fields": "Total fields",
        "report_saved": "Report saved: ",
        "report_save_failed": "Failed to save report: ",
        "press_enter_close": "Press Enter to close window...",
        "strip_prompt": "Save a copy WITHOUT metadata nearby (safe to share)? [y/N]: ",
        "strip_saved": "Clean copy saved: ",
        "strip_failed": "Failed to create clean copy: ",
        "no_data": "No metadata found.",
    },
}

LANG = "ru"


def t(key):
    return TR.get(LANG, TR["ru"]).get(key, key)


def load_saved_lang():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            lang = json.load(f).get("lang")
        return lang if lang in TR else None
    except Exception:
        return None


def save_lang(lang):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump({"lang": lang}, f)
    except Exception:
        pass  # не критично, просто не запомнится выбор


def choose_language():
    saved = load_saved_lang()
    default_num = "2" if saved == "en" else "1"
    Screen.page(TR["ru"]["welcome_title"] + " / welcome", [
        "  " + TR["ru"]["lang_prompt"],
    ])
    choice = prompt("[%s] > " % default_num)
    if choice == "":
        lang = saved or "ru"
    else:
        lang = "en" if choice == "2" else "ru"
    save_lang(lang)
    return lang


# ══════════════════════════ ВЫБОР ФАЙЛОВ ══════════════════════════
def fail(msg):
    Screen.page(t("err_title"), [
        "  " + paint(msg, C.RED),
    ])
    prompt(t("press_enter_exit"))
    sys.exit(1)


def split_dragged_paths(raw):
    """Разбивает строку с одним или несколькими путями по пробелам, уважая
    кавычки, но НЕ трогая обратный слеш — в отличие от shlex.split, который
    на Windows-путях (C:\\Users\\...) съедает все "\\" как экранирование."""
    parts = []
    current = ""
    in_quotes = False
    for ch in raw:
        if ch == '"':
            in_quotes = not in_quotes
            continue
        if ch in (" ", "\t") and not in_quotes:
            if current:
                parts.append(current)
                current = ""
            continue
        current += ch
    if current:
        parts.append(current)
    return parts


def pick_files():
    if len(sys.argv) > 1:
        args = [a.strip().strip('"') for a in sys.argv[1:] if a.strip()]
        if args:
            return args
    Screen.page(t("welcome_title"), [
        "  " + t("drag_prompt"),
    ])
    raw = prompt("> ")
    return [p for p in split_dragged_paths(raw) if p]


# ══════════════════════════ ЧИСТАЯ ЛОГИКА ПАРСИНГА (без изменений) ══════════════════════════
def human_size(n):
    n = float(n)
    for unit in ("Б", "КБ", "МБ", "ГБ"):
        if n < 1024 or unit == "ГБ":
            return (str(int(n)) + " Б") if unit == "Б" else ("%.1f %s" % (n, unit))
        n /= 1024.0
    return str(n)


def fmt(v):
    """Любое значение EXIF -> читаемая строка (или None)."""
    if v is None:
        return None
    if isinstance(v, bytes):
        try:
            s = v.decode("utf-8", "replace").strip("\x00").strip()
            return s if s else ("<binary %d байт>" % len(v))
        except Exception:
            return "<binary %d байт>" % len(v)
    if isinstance(v, (list, tuple)):
        parts = [x for x in (fmt(i) for i in v) if x]
        return "; ".join(parts) if parts else None
    if isinstance(v, dict):
        parts = [("%s: %s" % (k, fmt(x))) for k, x in v.items() if fmt(x)]
        return "; ".join(parts) if parts else None
    s = str(v).strip()
    return s if s else None


def decode_dict(d, tagmap):
    out = []
    for k, v in d.items():
        name = tagmap.get(k, k) if isinstance(k, int) else k
        s = fmt(v)
        if s:
            out.append((str(name), s))
    return out


def to_float(x):
    try:
        return float(x)
    except Exception:
        try:
            return x.numerator / x.denominator
        except Exception:
            return 0.0


def dms_to_deg(dms, ref):
    try:
        d, m, s = dms
        val = to_float(d) + to_float(m) / 60.0 + to_float(s) / 3600.0
        return -val if ref in ("S", "W") else val
    except Exception:
        return None


IPTC_NAMES = {
    (2, 5): "ObjectName", (2, 25): "Keywords", (2, 40): "SpecialInstructions",
    (2, 55): "DateCreated", (2, 60): "TimeCreated", (2, 80): "By-line",
    (2, 85): "By-lineTitle", (2, 90): "City", (2, 95): "Province-State",
    (2, 101): "Country", (2, 103): "OriginalTransmissionReference",
    (2, 105): "Headline", (2, 110): "Credit", (2, 115): "Source",
    (2, 116): "CopyrightNotice", (2, 118): "Contact", (2, 120): "Caption-Abstract",
    (2, 122): "Writer-Editor",
}


def save_clean_copy(img, path):
    """Пересохраняет фото без EXIF/IPTC/XMP, сохранив видимый поворот кадра
    (иначе после удаления тега Orientation фото может 'лечь на бок')."""
    from PIL import Image, ImageOps

    fixed = ImageOps.exif_transpose(img) or img
    clean = Image.new(fixed.mode, fixed.size)
    if hasattr(fixed, "get_flattened_data"):
        clean.putdata(fixed.get_flattened_data())  # Pillow ≥ 12
    else:
        clean.putdata(list(fixed.getdata()))       # старые версии Pillow

    base, ext = os.path.splitext(path)
    out_path = base + "_clean" + ext
    save_kwargs = {}
    if (img.format or "").upper() in ("JPEG", "JPG"):
        save_kwargs["quality"] = 95
    clean.save(out_path, format=img.format, **save_kwargs)
    return out_path


# ══════════════════════════ СБОР ДАННЫХ ФАЙЛА ══════════════════════════
def collect_sections(path, ExifTags, IptcImagePlugin, Image):
    """Открывает файл и возвращает (img, meta_rows, sections, gps_decimal, error).
    sections — список (title, [(label, value), ...]), без какого-либо
    форматирования под экран — то же самое, что раньше шло в общий дамп."""
    try:
        img = Image.open(path)
        img.load()
    except Exception as e:
        return None, None, None, None, t("open_failed") + str(e)

    TAGS = ExifTags.TAGS
    GPSTAGS = ExifTags.GPSTAGS
    IFD = getattr(ExifTags, "IFD", None)  # появился в Pillow 9.1

    sections = []

    def section(title, pairs):
        if pairs:
            sections.append((title, pairs))

    st = os.stat(path)
    meta_rows = [
        (t("field_name"), os.path.basename(path)),
        (t("field_path"), os.path.abspath(path)),
        (t("field_size"), "%s (%s байт)" % (human_size(st.st_size), format(st.st_size, ",").replace(",", " "))),
        (t("field_modified"), datetime.fromtimestamp(st.st_mtime).strftime("%d.%m.%Y %H:%M:%S")),
    ]
    w, h = img.size
    meta_rows_image = [
        (t("field_format"), str(img.format)),
        (t("field_resolution"), "%d × %d px" % (w, h)),
        (t("field_megapixels"), "%.1f Мп" % (w * h / 1e6)),
        (t("field_colormode"), str(img.mode)),
        (t("field_frames"), str(getattr(img, "n_frames", 1))),
    ]
    section(t("section_file"), meta_rows)
    section(t("section_image"), meta_rows_image)

    gps_decimal = [None, None]

    try:
        exif = img.getexif()
        section(t("section_exif_ifd0"), decode_dict(exif, TAGS))

        if IFD is not None:
            subs = [
                (IFD.Exif, t("section_exif_sub"), TAGS),
                (IFD.GPSInfo, t("section_gps"), GPSTAGS),
                (IFD.Interop, t("section_interop"), TAGS),
                (IFD.Makernote, t("section_makernote"), TAGS),
            ]
            ifd1 = getattr(IFD, "IFD1", None)
            if ifd1 is not None:
                subs.append((ifd1, t("section_ifd1"), TAGS))
            for ifd_code, title, tagmap in subs:
                try:
                    sub = exif.get_ifd(ifd_code)
                except Exception:
                    sub = None
                if not sub:
                    continue
                section(title, decode_dict(sub, tagmap))
                if title == t("section_gps"):
                    gps_decimal[0] = dms_to_deg(sub.get(2), sub.get(1))
                    gps_decimal[1] = dms_to_deg(sub.get(4), sub.get(3))
        else:
            raw = getattr(img, "_getexif", lambda: None)() or {}
            gps_raw = raw.get(34853) or {}
            old = {k: v for k, v in raw.items() if k not in (34853, 34665, 40965)}
            section(t("section_exif_old"), decode_dict(old, TAGS))
            if gps_raw:
                section(t("section_gps"), decode_dict(gps_raw, GPSTAGS))
                gps_decimal[0] = dms_to_deg(gps_raw.get(2), gps_raw.get(1))
                gps_decimal[1] = dms_to_deg(gps_raw.get(4), gps_raw.get(3))
    except Exception as e:
        section(t("section_exif_failed"), [(t("field_error"), str(e))])

    if gps_decimal[0] is not None and gps_decimal[1] is not None:
        lat, lon = gps_decimal
        section(t("section_gps_map"), [
            (t("field_lat"), "%.6f" % lat),
            (t("field_lon"), "%.6f" % lon),
            (t("field_gmaps"), "https://www.google.com/maps?q=%.6f,%.6f" % (lat, lon)),
            (t("field_ymaps"), "https://yandex.ru/maps/?pt=%.6f,%.6f&z=16&l=map" % (lon, lat)),
        ])

    try:
        iptc = IptcImagePlugin.getiptcinfo(img)
    except Exception:
        iptc = None
    if iptc:
        pairs = []
        for key, val in iptc.items():
            name = IPTC_NAMES.get(key, "IPTC %s" % str(key))
            s = fmt(val)
            if s:
                pairs.append((str(name), s))
        section(t("section_iptc"), pairs)

    xmp = img.info.get("XML:com.adobe.xmp")
    if xmp:
        if isinstance(xmp, bytes):
            xmp = xmp.decode("utf-8", "replace")
        xmp = str(xmp).strip()
        note = xmp if len(xmp) <= 4000 else (xmp[:4000] + "\n  ... [обрезано, всего %d символов]" % len(xmp))
        section(t("section_xmp"), [(t("field_xmp"), note)])

    icc = img.info.get("icc_profile")
    if icc:
        section(t("section_icc"), [(t("field_icc_profile"), "%d байт" % len(icc))])

    return img, meta_rows, sections, gps_decimal, None


def build_plain_report(path, sections, total_fields):
    """Полный текстовый отчёт без цвета/рамок — как раньше, для .txt файла."""
    RULE = "=" * 66
    lines = [RULE,
             "  METAREAD.PY -- " + os.path.basename(path),
             "  " + datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
             RULE]
    for title, pairs in sections:
        width = min(46, max(len(k) for k, _ in pairs))
        lines.append("")
        lines.append(("=== " + title + "  (" + str(len(pairs)) + ") ").ljust(66, "="))
        for k, v in pairs:
            lines.append("  " + k.ljust(width) + "  " + v)
    lines += ["", RULE, "  %s: %d   |   metaread.py %s" % (t("total_fields"), total_fields, VERSION), RULE]
    return "\n".join(lines)


def build_page_deck(sections, inner_width):
    """Разбивает секции на 'страницы' окна (с обрезкой длинных значений
    и чанкованием больших секций), готовые для показа через Screen.page()."""
    label_w = 0
    for _, pairs in sections:
        for k, _ in pairs:
            label_w = max(label_w, len(k))
    label_w = min(label_w, 28)

    deck = []
    for title, pairs in sections:
        chunks = [pairs[i:i + ROWS_PER_PAGE] for i in range(0, len(pairs), ROWS_PER_PAGE)]
        for ci, chunk in enumerate(chunks, 1):
            page_title = title if len(chunks) == 1 else ("%s (%d/%d)" % (title, ci, len(chunks)))
            body = []
            for k, v in chunk:
                prefix = "  " + k.ljust(label_w) + "  "
                avail = max(4, inner_width - vis_len(prefix))
                body.append(paint(prefix, C.GREY) + trim_to(v, avail))
            deck.append((page_title, body))
    return deck


def browse_deck(deck, file_label):
    if not deck:
        Screen.page(t("section_summary"), ["  " + t("no_data")], right=file_label)
        prompt("Enter")
        return
    idx = 0
    while True:
        title, body = deck[idx]
        footer = [paint("  " + t("nav_hint"), C.GREY)]
        Screen.page(title, body, right="%s · %s %d/%d" % (file_label, t("page_of"), idx + 1, len(deck)),
                    footer=footer)
        ch = prompt("> ").lower()
        if ch == "q":
            return
        if ch in ("p", "prev", "b", "назад"):
            idx = max(0, idx - 1)
        else:  # Enter / n / что угодно ещё = дальше
            if idx + 1 >= len(deck):
                return
            idx += 1


def final_screen(path, img, total_fields, gps_present, out_path, save_ok):
    file_label = os.path.basename(path)
    body = ["  %s: %d" % (t("total_fields"), total_fields)]
    if gps_present:
        body += ["", paint("  " + t("gps_privacy_warning"), C.YELLOW, C.BOLD),
                  paint(t("gps_privacy_warning2"), C.YELLOW, C.BOLD)]
    body.append("")
    if save_ok:
        body.append(paint("  " + t("report_saved") + out_path, C.GREEN))
    else:
        body.append(paint("  " + t("report_save_failed") + out_path, C.RED))
    Screen.page(t("section_summary"), body, right=file_label)

    answer = prompt(t("strip_prompt")).lower()
    if answer in ("y", "yes", "д", "да"):
        try:
            clean_path = save_clean_copy(img, path)
            body.append("")
            body.append(paint("  " + t("strip_saved") + clean_path, C.GREEN))
        except Exception as e:
            body.append("")
            body.append(paint("  " + t("strip_failed") + str(e), C.RED))
        Screen.page(t("section_summary"), body, right=file_label)


# ══════════════════════════ ОБРАБОТКА ОДНОГО ФАЙЛА ══════════════════════════
def process_file(path, ExifTags, IptcImagePlugin, Image, file_label):
    if not path or not os.path.isfile(path):
        Screen.page(t("err_title"), ["  " + paint(t("file_not_found") + str(path), C.RED)], right=file_label)
        prompt(t("press_enter_exit"))
        return

    img, meta_rows, sections, gps_decimal, error = collect_sections(path, ExifTags, IptcImagePlugin, Image)
    if error:
        Screen.page(t("err_title"), ["  " + paint(error, C.RED)], right=file_label)
        prompt(t("press_enter_exit"))
        return

    total_fields = sum(len(pairs) for _, pairs in sections)
    deck = build_page_deck(sections, Screen.INNER)
    browse_deck(deck, file_label)

    plain_report = build_plain_report(path, sections, total_fields)
    base, _ = os.path.splitext(path)
    out_path = base + "_metadata.txt"
    save_ok = True
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(plain_report + "\n")
    except Exception as e:
        save_ok = False
        out_path = str(e)

    gps_present = gps_decimal[0] is not None and gps_decimal[1] is not None
    final_screen(path, img, total_fields, gps_present, out_path, save_ok)


def main():
    enable_ansi()

    global LANG
    LANG = choose_language()

    try:
        from PIL import Image, ExifTags, IptcImagePlugin
    except ImportError:
        fail(t("need_pillow"))

    paths = pick_files()
    if not paths:
        fail(t("file_not_found") + "-")

    for i, path in enumerate(paths, 1):
        file_label = ("%s %d/%d: %s" % (t("of_file"), i, len(paths), os.path.basename(path)))
        process_file(path, ExifTags, IptcImagePlugin, Image, file_label)

    Screen.page(t("welcome_title"), ["  " + t("press_enter_close")])
    prompt("")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
