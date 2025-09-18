# FSA-DateStamp - Дистрибутив

**Версия:** 1.02.25.261 (18 сентября 2025)  
**Компания:** AW-Software  
**Автор:** Сергей Фокин @FoksSerg  
**Email:** foks_serg@mail.ru

## Описание

FSA-DateStamp - это приложение для добавления временных меток на изображения с поддержкой различных форматов и настроек. Поддерживает Windows, macOS и Linux.

## Структура дистрибутива

```
Distrib/
├── Build.py                    # Основной скрипт сборки
├── MacOS/                      # macOS приложение
│   └── FSA-DateStamp.app/      # macOS приложение (.app)
├── Windows7/                   # Windows 7 исполняемый файл
│   └── FSA-DateStamp.exe
├── Windows11/                  # Windows 11 исполняемый файл
│   └── FSA-DateStamp.exe
├── Icons/                      # Иконки приложения
│   ├── app.ico                 # Windows иконка
│   ├── app.icns                # macOS иконка
│   └── app.png                 # PNG иконка
├── Build_Config*.json          # Конфигурации сборки
└── README.md                   # Этот файл
```

## Системные требования

### Windows
- Windows 7/8/10/11 (x86/x64)
- Python 3.8+ (встроен в исполняемый файл)
- 100 МБ свободного места на диске

### macOS
- macOS 10.14+ (Mojave и выше)
- 100 МБ свободного места на диске

### Linux
- Ubuntu 18.04+ / CentOS 7+ / Fedora 30+
- Python 3.8+
- 100 МБ свободного места на диске

## Сборка

### Сборка приложения
```bash
python3 Build.py
```

Скрипт автоматически определяет операционную систему и собирает приложение для неё:
- **Windows** → создает исполняемый файл в `Windows7/` или `Windows11/`
- **macOS** → создает приложение в `MacOS/FSA-DateStamp.app/`
- **Linux** → создает исполняемый файл в `Linux/`

## Установка

### Windows
1. Скачайте `FSA-DateStamp.exe` из папки `Windows7/` или `Windows11/`
2. Запустите файл двойным кликом

### macOS
1. Скачайте `FSA-DateStamp.app` из папки `MacOS/`
2. Перетащите в папку Applications
3. Запустите из Launchpad или Applications

### Linux
1. Установите зависимости: `pip install -r requirements.txt`
2. Запустите: `python3 start_gui.py`

## Поддерживаемые форматы

- JPEG (.jpg, .jpeg)
- PNG (.png)
- TIFF (.tiff, .tif)
- BMP (.bmp)
- WEBP (.webp)

## Версия

**Версия:** 1.02.25.261  
**Дата сборки:** 18 сентября 2025

## Поддержка

При возникновении проблем обращайтесь к разработчику.



