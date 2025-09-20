# FSA-DateStamp - Руководство по сборке дистрибутивов

**Версия:** 1.02.25.261 (18 сентября 2025)  
**Компания:** AW-Software  
**Автор:** Сергей Фокин @FoksSerg  
**Email:** foks_serg@mail.ru

## Обзор

Это руководство содержит пошаговые инструкции по установке всех необходимых зависимостей и сборке дистрибутивов FSA-DateStamp на различных операционных системах.

## Содержание

- [Windows](#windows)
- [macOS](#macos)
- [Linux](#linux)
- [Сборка дистрибутивов](#сборка-дистрибутивов)
- [Создание установщиков](#создание-установщиков)
- [Устранение неполадок](#устранение-неполадок)

---

## Windows

### Системные требования
- Windows 7/8/10/11 (x64)
- 4 ГБ RAM
- 2 ГБ свободного места на диске
- Интернет-соединение

### Шаг 1: Установка Python

#### Вариант A: Официальный установщик (рекомендуется)
1. Перейдите на [python.org](https://www.python.org/downloads/)
2. Скачайте Python 3.8+ (рекомендуется 3.11)
3. Запустите установщик
4. **ВАЖНО**: Отметьте "Add Python to PATH"
5. Выберите "Install Now"

#### Вариант B: Microsoft Store
1. Откройте Microsoft Store
2. Найдите "Python 3.11"
3. Нажмите "Получить"

#### Проверка установки
```cmd
python --version
pip --version
```

### Шаг 2: Установка зависимостей проекта
```cmd
# Переходим в папку с проектом (если у вас уже есть исходный код)
cd FSA-DateStamp

# Устанавливаем зависимости
pip install -r requirements.txt

# Устанавливаем PyInstaller
pip install pyinstaller
```

**Примечание**: Если у вас нет исходного кода проекта, скачайте архив с GitHub или используйте Git для клонирования репозитория.

### Шаг 4: Установка инструментов для Windows установщика

#### Inno Setup (для создания .exe установщика)
1. Перейдите на [jrsoftware.org](https://jrsoftware.org/isinfo.php)
2. Скачайте Inno Setup 6.0+
3. Установите с настройками по умолчанию
4. Добавьте путь к `iscc.exe` в PATH (обычно `C:\Program Files (x86)\Inno Setup 6\`)

#### Проверка установки
```cmd
iscc
```

---

## macOS

### Системные требования
- macOS 10.14+ (Mojave и выше)
- 4 ГБ RAM
- 2 ГБ свободного места на диске
- Интернет-соединение

### Шаг 1: Установка Xcode Command Line Tools
```bash
xcode-select --install
```

### Шаг 2: Установка Homebrew (рекомендуется)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Шаг 3: Установка Python
```bash
# Через Homebrew (рекомендуется)
brew install python@3.11

# Или через официальный установщик
# Скачайте с python.org и установите
```

#### Проверка установки
```bash
python3 --version
pip3 --version
```

### Шаг 4: Установка зависимостей проекта
```bash
# Переходим в папку с проектом (если у вас уже есть исходный код)
cd FSA-DateStamp

# Устанавливаем зависимости
pip3 install -r requirements.txt

# Устанавливаем PyInstaller
pip3 install pyinstaller
```

**Примечание**: Если у вас нет исходного кода проекта, скачайте архив с GitHub или используйте Git для клонирования репозитория.

### Шаг 6: Установка инструментов для macOS установщика

#### hdiutil (встроен в macOS)
```bash
# Проверяем наличие
hdiutil --help
```

#### pkgbuild и productbuild (встроены в macOS)
```bash
# Проверяем наличие
pkgbuild --help
productbuild --help
```

---

## Linux

### Системные требования
- Ubuntu 18.04+ / Debian 10+ / CentOS 7+ / Fedora 30+
- 4 ГБ RAM
- 2 ГБ свободного места на диске
- Интернет-соединение

### Ubuntu/Debian

#### Шаг 1: Обновление системы
```bash
sudo apt update
sudo apt upgrade -y
```

#### Шаг 2: Установка Python и зависимостей
```bash
# Установка Python 3.8+
sudo apt install python3 python3-pip python3-venv python3-dev

# Установка инструментов сборки
sudo apt install build-essential git

# Установка системных зависимостей для Pillow и OpenCV
sudo apt install libjpeg-dev zlib1g-dev libpng-dev libtiff-dev
sudo apt install libavcodec-dev libavformat-dev libswscale-dev
sudo apt install libgtk-3-dev libatlas-base-dev gfortran
```

#### Шаг 3: Установка зависимостей проекта
```bash
# Переходим в папку с проектом (если у вас уже есть исходный код)
cd FSA-DateStamp

# Создаем виртуальное окружение (рекомендуется)
python3 -m venv venv
source venv/bin/activate

# Устанавливаем зависимости
pip install -r requirements.txt

# Устанавливаем PyInstaller
pip install pyinstaller
```

**Примечание**: Если у вас нет исходного кода проекта, скачайте архив с GitHub или используйте Git для клонирования репозитория.

#### Шаг 4: Установка инструментов для Linux пакетов

##### DEB пакеты
```bash
sudo apt install dpkg-dev debhelper
```

##### RPM пакеты
```bash
sudo apt install rpm
```

##### AppImage
```bash
# Скачиваем appimagetool
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool
```

### CentOS/RHEL/Fedora

#### Шаг 1: Обновление системы
```bash
# CentOS/RHEL
sudo yum update -y

# Fedora
sudo dnf update -y
```

#### Шаг 2: Установка Python и зависимостей
```bash
# CentOS/RHEL
sudo yum install python3 python3-pip python3-devel gcc git

# Fedora
sudo dnf install python3 python3-pip python3-devel gcc git

# Установка системных зависимостей
sudo yum install libjpeg-devel zlib-devel libpng-devel libtiff-devel
# или для Fedora
sudo dnf install libjpeg-devel zlib-devel libpng-devel libtiff-devel
```

#### Шаг 3: Установка зависимостей проекта
```bash
# Переходим в папку с проектом (если у вас уже есть исходный код)
cd FSA-DateStamp

# Создаем виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Устанавливаем зависимости
pip install -r requirements.txt
pip install pyinstaller
```

**Примечание**: Если у вас нет исходного кода проекта, скачайте архив с GitHub или используйте Git для клонирования репозитория.

---

## Сборка дистрибутивов

### Общий процесс
```bash
# Переходим в папку Distrib
cd Distrib

# Запускаем сборку (автоматически определяет ОС)
python3 Build.py
```

### Результаты сборки
- **Windows**: `Windows7/FSA-DateStamp.exe` или `Windows11/FSA-DateStamp.exe`
- **macOS**: `MacOS/FSA-DateStamp.app/`
- **Linux**: `Linux/FSA-DateStamp`

### Особенности сборки по ОС

#### Windows
- Создается исполняемый файл с встроенным Python
- Поддерживает Windows 7+ (x86/x64)
- Автоматически выбирает версию по совместимости

#### macOS
- Создается .app bundle
- Поддерживает Intel и Apple Silicon (Universal Binary)
- Включает все необходимые библиотеки

#### Linux
- Создается исполняемый файл без расширения
- Статически линкованные библиотеки
- Работает на большинстве дистрибутивов

---

## Создание установщиков

### Общий процесс
```bash
# Переходим в папку Installer
cd Installer

# Создаем установщик для текущей ОС
python3 build_installer.py

# Создаем портативную версию
python3 build_installer.py --portable
```

### Результаты установщиков

#### Windows
- **Inno Setup**: `Windows/installer_output/FSA-DateStamp-Setup.exe`
- **Портативная**: `Windows/installer_output/FSA-DateStamp-Portable.zip`

#### macOS
- **PKG**: `macOS/installer_output/FSA-DateStamp.pkg`
- **DMG**: `macOS/installer_output/FSA-DateStamp.dmg`
- **Портативная**: `macOS/installer_output/FSA-DateStamp-Portable.zip`

#### Linux
- **DEB**: `Linux/installer_output/FSA-DateStamp.deb` (в разработке)
- **RPM**: `Linux/installer_output/FSA-DateStamp.rpm` (в разработке)
- **AppImage**: `Linux/installer_output/FSA-DateStamp.AppImage` (в разработке)

---

## Устранение неполадок

### Общие проблемы

#### Python не найден
```bash
# Windows
python --version

# macOS/Linux
python3 --version
```

#### pip не найден
```bash
# Windows
python -m pip --version

# macOS/Linux
python3 -m pip --version
```

#### PyInstaller не найден
```bash
pip install pyinstaller
# или
pip3 install pyinstaller
```

### Проблемы сборки

#### Ошибки импорта модулей
```bash
# Убедитесь, что все зависимости установлены
pip install -r requirements.txt
```

#### Ошибки с библиотеками изображений
```bash
# Ubuntu/Debian
sudo apt install libjpeg-dev zlib1g-dev libpng-dev

# CentOS/RHEL
sudo yum install libjpeg-devel zlib-devel libpng-devel
```

#### Ошибки с OpenCV
```bash
# Установите системные зависимости
sudo apt install libopencv-dev python3-opencv
```

### Проблемы установщиков

#### Windows: Inno Setup не найден
- Убедитесь, что Inno Setup установлен
- Проверьте PATH: `iscc` должен работать из командной строки

#### macOS: hdiutil не работает
- Убедитесь, что Xcode Command Line Tools установлены
- Запустите: `xcode-select --install`

#### Linux: dpkg-deb не найден
```bash
sudo apt install dpkg-dev debhelper
```

---

## Дополнительные ресурсы

- [Официальная документация Python](https://docs.python.org/3/)
- [PyInstaller документация](https://pyinstaller.readthedocs.io/)
- [Inno Setup документация](https://jrsoftware.org/ishelp/)
- [AppImage документация](https://docs.appimage.org/)

---

## Поддержка

При возникновении проблем:
1. Проверьте раздел "Устранение неполадок"
2. Убедитесь, что все зависимости установлены
3. Проверьте версии Python и pip
4. Обратитесь к разработчику: foks_serg@mail.ru
