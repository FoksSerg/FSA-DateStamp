# FSA-DateStamp - Инсталляторы

**Версия:** 1.01.25.249 (6 сентября 2025)  
**Компания:** AW-Software  
**Автор:** Сергей Фокин @FoksSerg  
**Email:** foks_serg@mail.ru

Эта папка содержит инсталляторы для различных операционных систем.

## Система версионирования

Версия формируется по схеме: **X.YY.ZZ.DDD**
- **X** - мажорная версия (1)
- **YY** - минорная версия (01)
- **ZZ** - год (25 = 2025)
- **DDD** - день года (249 = 6 сентября)

Пример: `1.01.25.249` = версия 1.01, год 2025, 249-й день года (6 сентября)

## Структура

```
Installer/
├── build_installer.py          # Универсальный скрипт сборки
├── Windows/                    # Windows инсталляторы
│   ├── installer.iss          # Inno Setup скрипт
│   ├── installer_output/      # Готовые инсталляторы
│   └── resources/             # Дополнительные ресурсы
├── macOS/                      # macOS инсталляторы
│   ├── installer.pkg          # PKG инсталлятор
│   ├── installer.dmg          # DMG образ
│   └── installer_output/      # Готовые инсталляторы
├── Linux/                      # Linux инсталляторы
│   ├── installer.deb          # DEB пакет
│   ├── installer.rpm          # RPM пакет
│   ├── installer.AppImage     # AppImage
│   └── installer_output/      # Готовые инсталляторы
└── README.md                   # Этот файл
```

## Использование

### Сборка для текущей ОС
```bash
python build_installer.py
```

### Сборка для конкретной ОС
```bash
python build_installer.py --os windows
python build_installer.py --os macos
python build_installer.py --os linux
```

### Сборка для всех ОС
```bash
python build_installer.py --all
```

### Создание портативной версии
```bash
python build_installer.py --portable
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
- **macOS**: `macOS/installer_output/FSA-DateStamp.dmg`
- **Linux**: `Linux/installer_output/FSA-DateStamp.deb`

## Статус реализации

- ✅ **Windows**: Полностью реализован (Inno Setup)
- ⚠️ **macOS**: В разработке (PKG/DMG)
- ⚠️ **Linux**: В разработке (DEB/RPM/AppImage)

## Интеграция с Build.py

Скрипт автоматически интегрируется с основным Build.py:

```python
# В Build.py можно добавить:
def create_installer(os_name=None):
    installer_script = project_root / "Installer" / "build_installer.py"
    subprocess.run([sys.executable, str(installer_script), "--os", os_name])
```
