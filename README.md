
<img width="1960" height="520" alt="metaread-horizontal" src="https://github.com/user-attachments/assets/727fc6e5-f8bd-46ea-b221-2f69683f8e8c" />

> [!IMPORTANT]
> ## TONFORGE v0.9.0 Beta
<img width="681" height="227" alt="image" src="https://github.com/user-attachments/assets/c56b921d-9ec2-44c9-8111-c5ae9956534a" />

**1️⃣ First Improvements**

Added colored console UI and METAREAD v0.9.0 Beta branding.
Added RU/EN language selection with saved preference.
Added batch processing for multiple images.
Added a GPS privacy warning when exact coordinates are detected.
Added one-click creation of a metadata-free copy while preserving the correct image orientation.
Fixed compatibility with upcoming Pillow versions.
Tested everything on a real JPEG with EXIF + GPS metadata.

**2️⃣ Windowed Interface**

Reworked the output into paginated terminal windows.
Added navigation with Enter / n / p / q.
Large metadata sections are automatically split across multiple pages.
Full .txt reports are still saved without pagination or ANSI codes.
Added automatic frame-width validation and fixed an overflow bug caused by long headers.

**3️⃣ Fixes After Real-World Testing**

Fixed Windows path handling — paths like C:\Users\... are no longer corrupted.
Replaced shlex.split() with a custom argument parser that preserves backslashes.
Improved handling of paths with spaces, quotes, and multiple files.
Language selection is now shown on every launch.
The previously selected language is used as the default when pressing Enter


> [!IMPORTANT]
> ## TONFORGE v0.8.0 Beta
<img width="600" height="471" alt="image" src="https://github.com/user-attachments/assets/3d2b560d-5a38-409c-867b-28c0a669db3f" />

Установка - pip install pillow
Запуск - python metaread.py

# METAREAD — Анализатор метаданных изображений
**METAREAD** — это Python-инструмент для извлечения и анализа метаданных из изображений. Программа позволяет получить подробную информацию о файле, изображении и встроенных метаданных, включая EXIF, GPS, IPTC, XMP и ICC.
Проект может быть полезен для анализа фотографий, проверки информации о файлах, цифровой криминалистики и изучения метаданных изображений.

## ✨ Возможности
* 📷 Чтение EXIF-метаданных
* 📍 Извлечение GPS-координат
* 🗺️ Преобразование GPS в широту и долготу
* 🔗 Генерация ссылок на Google Maps и Яндекс Карты
* 📝 Чтение IPTC-данных
* 🔍 Извлечение XMP-информации
* 🎨 Определение ICC цветового профиля
* 📁 Информация о файле и его размере
* 🖼️ Разрешение, формат, цветовой режим и количество кадров
* 📊 Подсчёт общего количества найденных полей
* 📄 Автоматическое сохранение результата в `.txt`
* 🖱️ Поддержка передачи файла через аргумент командной строки
* 📂 Возможность перетащить изображение в терминал

## 📋 Какие данные можно получить
В зависимости от изображения программа может обнаружить:

* Производителя и модель камеры
* Дату и время съёмки
* Параметры камеры
* GPS-координаты
* Информацию об авторе
* Copyright
* Город и страну
* Описание изображения
* Ключевые слова
* Информацию о редакторе
* XMP-данные
* Цветовой профиль
* Технические параметры изображения

## 📦 Установка
Установите библиотеку Pillow:

```bash
python -m pip install pillow
```

## 🚀 Использование
Запуск с указанием файла:

```bash
python metaread.py photo.jpg
```

Также можно просто перетащить изображение в окно программы.

После анализа рядом с исходным файлом автоматически создаётся отчёт:

```text
photo_metadata.txt
```

## 🛠️ Требования
* Python 3.x
* Pillow

## ⚠️ Примечание
Количество доступных метаданных зависит от самого изображения. Многие социальные сети, редакторы фотографий и мессенджеры удаляют EXIF, GPS и другие метаданные при обработке или загрузке изображения.

**METAREAD не восстанавливает удалённые метаданные — он извлекает только те данные, которые фактически присутствуют в файле.**

## 📄 Назначение
Проект предназначен для образовательного использования, анализа изображений, цифровой криминалистики и проверки метаданных собственных файлов.


# METAREAD — Image Metadata Reader
**METAREAD** is a Python tool for extracting and analyzing metadata from image files. It provides detailed information about the file and embedded metadata, including EXIF, GPS, IPTC, XMP, and ICC profiles.
The project can be useful for image analysis, file inspection, digital forensics, and learning how image metadata is stored and processed.

## ✨ Features
* 📷 EXIF metadata extraction
* 📍 GPS coordinate extraction
* 🗺️ GPS coordinates converted to decimal format
* 🔗 Google Maps and Yandex Maps links
* 📝 IPTC metadata extraction
* 🔍 XMP data extraction
* 🎨 ICC color profile detection
* 📁 File information and file size
* 🖼️ Image format, resolution, color mode, and frame count
* 📊 Total metadata field count
* 📄 Automatic `.txt` report generation
* 🖱️ Command-line file input
* 📂 Drag-and-drop file support

## 📋 Extracted Information
Depending on the image, METAREAD may detect:

* Camera manufacturer and model
* Date and time
* Camera settings
* GPS coordinates
* Author information
* Copyright information
* City and country
* Image description
* Keywords
* Editing software information
* XMP metadata
* ICC color profile
* Technical image information

## 📦 Installation
Install the required Pillow library:

```bash
python -m pip install pillow
```

## 🚀 Usage
Run the tool with an image:

```bash
python metaread.py photo.jpg
```

You can also drag an image file into the terminal when prompted.

After processing, the report is automatically saved next to the original image:

```text
photo_metadata.txt
```

## 🛠️ Requirements
* Python 3.x
* Pillow

## ⚠️ Note
The amount of available metadata depends on the image itself. Social networks, image editors, and messaging applications often remove EXIF, GPS, and other metadata during processing or upload.

**METAREAD does not recover deleted metadata — it only extracts information that is actually present in the file.**

## 📄 Purpose
METAREAD is intended for educational use, image analysis, digital forensics, and inspecting metadata in files you own or are authorized to analyze.

