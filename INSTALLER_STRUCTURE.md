# Структура инсталлятора FSA-DateStamp

**Версия:** 1.02.25.261 (18 сентября 2025)  
**Компания:** AW-Software  
**Автор:** Сергей Фокин @FoksSerg  
**Email:** foks_serg@mail.ru

## Обзор
Проект FSA-DateStamp поддерживает создание инсталляторов для различных операционных систем. Все инсталляторы размещаются в папке `Installer/` с подпапками для каждой ОС.

## Система версионирования

Версия формируется по схеме: **X.YY.ZZ.DDD**
- **X** - мажорная версия (1)
- **YY** - минорная версия (02) 
- **ZZ** - год (25 = 2025)
- **DDD** - день года (261 = 18 сентября)

Пример: `1.02.25.261` = версия 1.02, год 2025, 261-й день года (18 сентября)

## Структура папок

```
FSA-DateStamp/
├── src/                               # Исходный код приложения
├── Distrib/                           # Сборка и дистрибутивы
│   ├── Build.py                      # Основной скрипт сборки
│   └── dist/                         # Собранные исполняемые файлы
├── Installer/                         # 🆕 Папка инсталляторов
│   ├── Windows/                       # Инсталляторы для Windows
│   ├── macOS/                         # Инсталляторы для macOS
│   ├── Linux/                         # Инсталляторы для Linux
│   └── README.md                      # Общая документация
└── requirements.txt
```

## Детальная структура по ОС

### Windows (Installer/Windows/)
```
Windows/
├── installer.iss                     # Основной скрипт Inno Setup
└── installer_output/                 # Готовые инсталляторы
    └── FSA-DateStamp-Setup.exe      # Основной инсталлятор
```

### macOS (Installer/macOS/)
```
macOS/
└── installer_output/                 # Готовые инсталляторы
    ├── FSA-DateStamp.pkg            # PKG инсталлятор
    ├── FSA-DateStamp.dmg            # DMG образ
    └── FSA-DateStamp-Portable.zip   # Портативная версия
```

### Linux (Installer/Linux/)
```
Linux/
├── installer.deb                     # DEB пакет для Ubuntu/Debian
├── installer.rpm                     # RPM пакет для Red Hat/Fedora
├── installer.AppImage                # AppImage для всех дистрибутивов
├── installer.snap                    # Snap пакет
├── resources/
│   ├── fonts/
│   ├── images/
│   └── configs/
├── build_installer.py                # Скрипт сборки
└── installer_output/
    ├── FSA-DateStamp.deb
    ├── FSA-DateStamp.rpm
    ├── FSA-DateStamp.AppImage
    └── FSA-DateStamp.snap
```

## Функциональность инсталляторов

### Windows (Inno Setup)
- **Установка в Program Files** с правами администратора
- **Создание ярлыков** на рабочем столе и в меню Пуск
- **Регистрация в системе** для ассоциации файлов
- **Проверка зависимостей** (Python, библиотеки)
- **Сохранение настроек** при обновлении
- **Создание папки логов** в AppData
- **Портативная версия** для запуска без установки

### macOS (PKG/DMG)
- **Установка в Applications** с правами пользователя
- **Создание ярлыка** в Dock
- **Регистрация в Launch Services** для ассоциации файлов
- **Проверка Gatekeeper** и подпись кода
- **Создание папки логов** в ~/Library/Logs
- **App Store версия** с Sandbox

### Linux (DEB/RPM/AppImage)
- **Установка через пакетный менеджер** с зависимостями
- **Создание ярлыков** в меню приложений
- **Регистрация MIME типов** для ассоциации файлов
- **Создание папки логов** в ~/.local/share
- **AppImage** для запуска без установки
- **Snap** для изолированной установки

## Интеграция с Build.py

### Новые функции в Build.py:
```python
def create_installer(os_name, version):
    """Создание инсталлятора для указанной ОС"""
    if os_name == "windows":
        return create_windows_installer(version)
    elif os_name == "macos":
        return create_macos_installer(version)
    elif os_name == "linux":
        return create_linux_installer(version)

def create_windows_installer(version):
    """Создание Windows инсталлятора через Inno Setup"""
    # Вызов installer/Windows/build_installer.py
    
def create_macos_installer(version):
    """Создание macOS инсталлятора"""
    # Вызов installer/macOS/build_installer.py
    
def create_linux_installer(version):
    """Создание Linux инсталлятора"""
    # Вызов installer/Linux/build_installer.py
```

## Автоматизация сборки

### CI/CD Pipeline:
1. **Сборка исполняемых файлов** через `Build.py`
2. **Создание инсталляторов** для всех ОС
3. **Тестирование инсталляторов** на виртуальных машинах
4. **Публикация релизов** на GitHub/GitLab
5. **Уведомления** о готовности релизов

### Локальная сборка:
```bash
# Сборка приложения (автоматически определяет ОС)
python3 Distrib/Build.py

# Создание установщиков
python3 Installer/build_installer.py
```

## Требования к инсталляторам

### Общие требования:
- **Минимальный размер** - оптимизация ресурсов
- **Быстрая установка** - не более 30 секунд
- **Простой интерфейс** - минимум диалогов
- **Откат изменений** - возможность удаления
- **Логирование** - запись процесса установки

### Специфичные требования:
- **Windows**: Поддержка Windows 10/11, .NET Framework
- **macOS**: Поддержка macOS 10.15+, кодовая подпись
- **Linux**: Поддержка Ubuntu 18.04+, CentOS 7+, AppImage

## Будущие возможности

### Планируемые функции:
- **Автоматические обновления** через встроенный механизм
- **Многоязычная поддержка** интерфейса инсталлятора
- **Портативные версии** для всех ОС
- **Интеграция с облаком** для синхронизации настроек
- **Плагинная архитектура** для расширения функциональности

### Дополнительные форматы:
- **Windows**: MSI, NSIS, WiX
- **macOS**: DMG с drag&drop, App Store
- **Linux**: Flatpak, Snap, AppImage, DEB, RPM

## Заключение

Структура инсталлятора FSA-DateStamp обеспечивает:
- **Кроссплатформенность** - поддержка всех основных ОС
- **Масштабируемость** - легко добавлять новые ОС
- **Автоматизацию** - интеграция с CI/CD
- **Профессиональность** - качественные инсталляторы
- **Удобство** - простота установки для пользователей
