# FSA-DateStamp

Система для автоматического добавления водяных знаков с датой и временем на изображения с сохранением структуры папок и метаданных файлов.

## Возможности

- ✅ Добавление водяных знаков с датой и временем
- ✅ Сохранение структуры исходных папок
- ✅ Сохранение дат создания и модификации файлов
- ✅ Поддержка множества форматов изображений (JPG, PNG, BMP, TIFF)
- ✅ Извлечение даты из EXIF, имени файла или времени создания
- ✅ Настраиваемые параметры (размер шрифта, позиция, цвета)

## Структура проекта

```
FSA-DateStamp/
├── src/
│   ├── DateStamp.py          # Основной модуль обработки
│   ├── PacketFolder.py       # Пакетная обработка папок
│   └── TestFotoProcessor.py  # Специальный процессор для TestFoto
├── TestFotoInput/            # Папка с исходными изображениями
├── TestFotoStamp/            # Папка с результатами обработки
└── README.md
```

## Использование

### 1. Обработка TestFoto (рекомендуемый способ)

```bash
cd src
python TestFotoProcessor.py
```

Этот скрипт автоматически:
- Обрабатывает все изображения из `TestFotoInput/`
- Сохраняет результаты в `TestFotoStamp/` с сохранением структуры
- Сохраняет метаданные исходных файлов

### 2. Обычная обработка с сохранением структуры

```bash
cd src
python DateStamp.py /путь/к/исходной/папке -o /путь/к/результату --preserve-structure
```

### 3. Пакетная обработка папок

```bash
cd src
python PacketFolder.py /корневая/папка /папка/результатов --preserve-structure
```

## Параметры командной строки

### DateStamp.py

- `input_folder` - Папка с исходными изображениями (обязательно)
- `-o, --output` - Папка для сохранения результатов
- `--preserve-structure` - Сохранять структуру папок и метаданные
- `--overwrite` - Перезаписывать исходные файлы
- `--font-size` - Размер шрифта (по умолчанию: 30)
- `--position` - Позиция водяного знака (top-left, top-right, bottom-left, bottom-right)

### PacketFolder.py

- `input_root` - Корневая папка с исходными изображениями
- `output_root` - Папка для результатов
- `--preserve-structure` - Режим сохранения структуры

## Поддерживаемые форматы

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff, .tif)

## Извлечение даты и времени

Система пытается получить дату и время в следующем порядке:

1. **EXIF-данные** - из метаданных изображения
2. **Имя файла** - парсинг форматов:
   - `IMG_20230101_123456.jpg`
   - `20230101_123456.jpg`
3. **Время создания файла** - как fallback

## Примеры использования

### Обработка одной папки
```bash
python DateStamp.py ./photos -o ./watermarked --preserve-structure --font-size 40
```

### Пакетная обработка с сохранением структуры
```bash
python PacketFolder.py ./input_photos ./output_photos --preserve-structure
```

### Обработка TestFoto
```bash
# Поместите изображения в TestFotoInput/
python TestFotoProcessor.py
# Результаты появятся в TestFotoStamp/
```

## Требования

- Python 3.6+
- Pillow (PIL)
- OpenCV
- exifread
- piexif

## Установка зависимостей

```bash
pip install Pillow opencv-python exifread piexif
```
