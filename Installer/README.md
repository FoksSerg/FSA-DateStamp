# FSA-DateStamp - Инсталляторы

**Версия:** 1.02.25.261 (18 сентября 2025)  
**Компания:** AW-Software  
**Автор:** Сергей Фокин @FoksSerg  
**Email:** foks_serg@mail.ru

Эта папка содержит инсталляторы для различных операционных систем.

## Система версионирования

Версия формируется по схеме: **X.YY.ZZ.DDD**
- **X** - мажорная версия (1)
- **YY** - минорная версия (02)
- **ZZ** - год (25 = 2025)
- **DDD** - день года (261 = 18 сентября)

Пример: `1.02.25.261` = версия 1.02, год 2025, 261-й день года (18 сентября)

## Структура

```
Installer/
├── build_installer.py          # Универсальный скрипт сборки
├── Windows/                    # Windows инсталляторы
│   ├── installer.iss          # Inno Setup скрипт
│   └── installer_output/      # Готовые инсталляторы
│       └── FSA-DateStamp-Setup.exe
├── macOS/                      # macOS инсталляторы
│   └── installer_output/      # Готовые инсталляторы
│       ├── FSA-DateStamp.pkg  # PKG инсталлятор
│       ├── FSA-DateStamp.dmg  # DMG образ
│       └── FSA-DateStamp-Portable.zip
└── README.md                   # Этот файл
```

## Использование

### Сборка для текущей ОС
```bash
python3 build_installer.py
```

### Создание портативной версии
```bash
python3 build_installer.py --portable
```

## Требования

### Windows
- Inno Setup 6.0+ (https://jrsoftware.org/isinfo.php)
- Собранное приложение в `../Distrib/dist/`

### macOS
- Xcode Command Line Tools
- Собранное приложение в `../Distrib/dist/`

### Linux
- dpkg-deb (для DEB)
- rpmbuild (для RPM)
- appimagetool (для AppImage)
- Собранное приложение в `../Distrib/dist/`

## Результаты сборки

После успешной сборки инсталляторы будут находиться в:
- **Windows**: `Windows/installer_output/FSA-DateStamp-Setup.exe`
- **macOS**: `macOS/installer_output/FSA-DateStamp.pkg` и `FSA-DateStamp.dmg`
- **macOS Portable**: `macOS/installer_output/FSA-DateStamp-Portable.zip`

## Статус реализации

- ✅ **Windows**: Полностью реализован (Inno Setup)
- ✅ **macOS**: Полностью реализован (PKG/DMG/Portable)
- ⚠️ **Linux**: В разработке (DEB/RPM/AppImage)

## Интеграция с Build.py

Скрипт автоматически интегрируется с основным Build.py:

```python
# В Build.py можно добавить:
def create_installer(os_name=None):
    installer_script = project_root / "Installer" / "build_installer.py"
    subprocess.run([sys.executable, str(installer_script), "--os", os_name])
```
