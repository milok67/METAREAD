<img width="1280" height="640" alt="metaread-social" src="https://github.com/user-attachments/assets/052fc2d7-9f3b-4cf1-a55e-34c14c3f8363" />
# METAREAD

Установка - pip install pillow
Запуск - python metaread.py

<img width="600" height="471" alt="image" src="https://github.com/user-attachments/assets/3d2b560d-5a38-409c-867b-28c0a669db3f" />

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

