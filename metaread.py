#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
METAREAD.PY — вытаскивает из фото ВСЕ метаданные: EXIF, GPS, IPTC, XMP.

Как пользоваться:
   1) Один раз установи Pillow:   python -m pip install pillow
   2) Перетащи фото прямо на файл metaread.py
      или из терминала:           python metaread.py photo.jpg
   3) Отчёт выведется на экран и сохранится рядом с фото:
      <имя_фото>_metadata.txt
"""

import os
import sys
from datetime import datetime

RULE = "=" * 66


def fail(msg):
    print()
    print("  ОШИБКА: " + msg)
    print()
    input("  Нажми Enter, чтобы выйти...")
    sys.exit(1)


def pick_file():
    if len(sys.argv) > 1 and sys.argv[1].strip():
        return sys.argv[1].strip().strip('"')
    print()
    print("  Перетащи файл в это окно и нажми Enter:")
    try:
        return input("  > ").strip().strip('"')
    except (EOFError, KeyboardInterrupt):
        sys.exit(0)


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


def main():
    try:
        from PIL import Image, ExifTags, IptcImagePlugin
    except ImportError:
        fail("Нужна библиотека Pillow. Установи её:  python -m pip install pillow")

    path = pick_file()
    if not path or not os.path.isfile(path):
        fail("Файл не найден: " + str(path))

    try:
        img = Image.open(path)
        img.load()
    except Exception as e:
        fail("Pillow не смог открыть файл: " + str(e))

    TAGS = ExifTags.TAGS
    GPSTAGS = ExifTags.GPSTAGS
    IFD = getattr(ExifTags, "IFD", None)  # появился в Pillow 9.1

    lines = []
    total = [0]

    def section(title, pairs):
        if not pairs:
            return
        total[0] += len(pairs)
        width = min(46, max(len(k) for k, _ in pairs))
        lines.append("")
        lines.append(("=== " + title + "  (" + str(len(pairs)) + ") ").ljust(66, "="))
        for k, v in pairs:
            lines.append("  " + k.ljust(width) + "  " + v)

    lines.append(RULE)
    lines.append("  METAREAD.PY -- ПОЛНЫЙ ДАМП МЕТАДАННЫХ")
    lines.append("  " + datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
    lines.append(RULE)

    st = os.stat(path)
    section("ФАЙЛ", [
        ("Имя", os.path.basename(path)),
        ("Путь", os.path.abspath(path)),
        ("Размер", "%s (%s байт)" % (human_size(st.st_size), format(st.st_size, ",").replace(",", " "))),
        ("Изменён", datetime.fromtimestamp(st.st_mtime).strftime("%d.%m.%Y %H:%M:%S")),
    ])

    w, h = img.size
    section("ИЗОБРАЖЕНИЕ", [
        ("Формат", str(img.format)),
        ("Разрешение", "%d × %d px" % (w, h)),
        ("Мегапиксели", "%.1f Мп" % (w * h / 1e6)),
        ("Цветовой режим", str(img.mode)),
        ("Кадров", str(getattr(img, "n_frames", 1))),
    ])

    gps_decimal = [None, None]

    # ------------------------------ EXIF ------------------------------
    try:
        exif = img.getexif()
        section("EXIF / IFD0 — камера и файл", decode_dict(exif, TAGS))

        if IFD is not None:
            subs = [
                (IFD.Exif, "EXIF SUB-IFD — параметры съёмки", TAGS),
                (IFD.GPSInfo, "GPS — геолокация", GPSTAGS),
                (IFD.Interop, "INTEROPERABILITY", TAGS),
                (IFD.Makernote, "MAKERNOTE — данные производителя", TAGS),
            ]
            ifd1 = getattr(IFD, "IFD1", None)
            if ifd1 is not None:
                subs.append((ifd1, "IFD1 — встроенное превью", TAGS))
            for ifd_code, title, tagmap in subs:
                try:
                    sub = exif.get_ifd(ifd_code)
                except Exception:
                    sub = None
                if not sub:
                    continue
                section(title, decode_dict(sub, tagmap))
                if title.startswith("GPS"):
                    gps_decimal[0] = dms_to_deg(sub.get(2), sub.get(1))
                    gps_decimal[1] = dms_to_deg(sub.get(4), sub.get(3))
        else:
            raw = getattr(img, "_getexif", lambda: None)() or {}
            gps_raw = raw.get(34853) or {}
            old = {k: v for k, v in raw.items() if k not in (34853, 34665, 40965)}
            section("EXIF — parameters (старый парсер)", decode_dict(old, TAGS))
            if gps_raw:
                section("GPS — геолокация", decode_dict(gps_raw, GPSTAGS))
                gps_decimal[0] = dms_to_deg(gps_raw.get(2), gps_raw.get(1))
                gps_decimal[1] = dms_to_deg(gps_raw.get(4), gps_raw.get(3))
    except Exception as e:
        section("EXIF — не удалось прочитать", [("Ошибка", str(e))])

    # ------------------------------ GPS ------------------------------
    if gps_decimal[0] is not None and gps_decimal[1] is not None:
        lat, lon = gps_decimal
        section("GPS — карта", [
            ("Широта", "%.6f" % lat),
            ("Долгота", "%.6f" % lon),
            ("Google Maps", "https://www.google.com/maps?q=%.6f,%.6f" % (lat, lon)),
            ("Яндекс Карта", "https://yandex.ru/maps/?pt=%.6f,%.6f&z=16&l=map" % (lon, lat)),
        ])
    else:
        lines.append("")
        lines.append("  GPS-метки не найдены (координаты не записаны или стёрты).")

    # ------------------------------ IPTC ------------------------------
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
        section("IPTC — описание и права", pairs)

    # ------------------------------ XMP ------------------------------
    xmp = img.info.get("XML:com.adobe.xmp")
    if xmp:
        if isinstance(xmp, bytes):
            xmp = xmp.decode("utf-8", "replace")
        xmp = str(xmp).strip()
        note = xmp if len(xmp) <= 4000 else (xmp[:4000] + "\n  ... [обрезано, всего %d символов]" % len(xmp))
        section("XMP — редактор и история (сырые данные)", [("XMP", note)])

    # ------------------------------ ICC ------------------------------
    icc = img.info.get("icc_profile")
    if icc:
        section("ICC — цветовой профиль", [("Профиль", "%d байт" % len(icc))])

    # ------------------------------ итог ------------------------------
    lines.append("")
    lines.append(RULE)
    lines.append("  Всего полей: %d   |   metaread.py" % total[0])
    lines.append(RULE)

    report = "\n".join(lines)
    print()
    print(report)

    base, _ = os.path.splitext(path)
    out_path = base + "_metadata.txt"
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(report + "\n")
        print()
        print("  Отчёт сохранён: " + out_path)
    except Exception as e:
        print("  Не удалось сохранить отчёт: " + str(e))

    print()
    input("  Нажми Enter, чтобы закрыть окно...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
