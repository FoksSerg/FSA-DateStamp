#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FSA-DateStamp - Универсальный скрипт сборки инсталляторов
Поддерживает Windows, macOS и Linux

Версия: 1.01.25.249 (6 сентября 2025)
Компания: AW-Software
Автор: Сергей Фокин @FoksSerg
Email: foks_serg@mail.ru

Система версионирования: X.YY.ZZ.DDD
- X - мажорная версия (1)
- YY - минорная версия (01)
- ZZ - год (25 = 2025)
- DDD - день года (249 = 6 сентября)
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

class InstallerBuilder:
    """Универсальный класс для сборки инсталляторов на всех ОС"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.installer_dir = Path(__file__).parent
        self.dist_dir = self.project_root / "Distrib" / "dist"
        self.current_os = platform.system().lower()
        self.version = self.get_version()
        
        print(f"🔧 FSA-DateStamp Installer Builder")
        print(f"📱 Текущая ОС: {platform.system()} ({self.current_os})")
        print(f"📦 Версия: {self.version}")
        print(f"📁 Корень проекта: {self.project_root}")
        print(f"📁 Папка инсталляторов: {self.installer_dir}")
        print("-" * 50)
    
    def get_version(self):
        """Получение версии из version.txt или по умолчанию"""
        try:
            # Сначала пытаемся прочитать из version.txt
            version_file = self.project_root / "version.txt"
            if version_file.exists():
                with open(version_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Ищем версию в version.txt
                    for line in content.split('\n'):
                        if 'prodvers=' in line or 'ProductVersion' in line:
                            # Извлекаем версию из строки типа prodvers=(1, 1, 25, 249)
                            if 'prodvers=' in line:
                                version_part = line.split('prodvers=')[1].split(')')[0]
                                version = version_part.replace('(', '').replace(')', '').replace(',', '.').replace(' ', '')
                                return version
                            # Или из строки типа StringStruct(u'ProductVersion', u'1.01.25.249')
                            elif 'ProductVersion' in line:
                                version_part = line.split("u'ProductVersion', u'")[1].split("')")[0]
                                return version_part
        except Exception as e:
            print(f"⚠️ Не удалось получить версию из version.txt: {e}")
        
        return "1.01.25.249"
    
    def build_installer(self, target_os=None):
        """Сборка инсталлятора для указанной ОС или текущей"""
        target_os = target_os or self.current_os
        
        print(f"🚀 Начинаем сборку инсталлятора для {target_os.upper()}")
        
        # Проверяем наличие собранного приложения
        if not self.check_built_application():
            print("❌ Сначала необходимо собрать приложение через Build.py")
            return False
        
        # Выбираем метод сборки в зависимости от ОС
        if target_os == "windows":
            return self.build_windows_installer()
        elif target_os == "darwin":  # macOS
            return self.build_macos_installer()
        elif target_os == "linux":
            return self.build_linux_installer()
        else:
            print(f"❌ Неподдерживаемая ОС: {target_os}")
            return False
    
    def check_built_application(self):
        """Проверка наличия собранного приложения"""
        if self.current_os == "windows":
            exe_path = self.project_root / "Distrib" / "Windows" / "FSA-DateStamp.exe"
            return exe_path.exists()
        elif self.current_os == "darwin":  # macOS
            app_path = self.project_root / "Distrib" / "MacOS" / "FSA-DateStamp.app"
            return app_path.exists()
        elif self.current_os == "linux":
            binary_path = self.project_root / "Distrib" / "Linux" / "FSA-DateStamp"
            return binary_path.exists()
        return False
    
    def build_windows_installer(self):
        """Сборка Windows инсталлятора через Inno Setup"""
        print("🪟 Сборка Windows инсталлятора...")
        
        # Создаем папку для Windows инсталлятора
        windows_dir = self.installer_dir / "Windows"
        windows_dir.mkdir(exist_ok=True)
        
        # Создаем Inno Setup скрипт
        iss_content = self.create_inno_setup_script()
        iss_file = windows_dir / "installer.iss"
        
        with open(iss_file, 'w', encoding='utf-8') as f:
            f.write(iss_content)
        
        print(f"📝 Создан Inno Setup скрипт: {iss_file}")
        
        # Проверяем наличие Inno Setup
        iscc_path = self.check_inno_setup()
        if not iscc_path:
            print("❌ Inno Setup не найден. Установите Inno Setup 6.0+")
            print("📥 Скачать: https://jrsoftware.org/isinfo.php")
            return False
        
        # Создаем папку для вывода
        output_dir = windows_dir / "installer_output"
        output_dir.mkdir(exist_ok=True)
        
        # Запускаем компиляцию
        try:
            print("🔨 Компилируем инсталлятор...")
            result = subprocess.run([
                iscc_path,  # Inno Setup Compiler
                str(iss_file)
            ], capture_output=True, text=True, cwd=str(windows_dir))
            
            if result.returncode == 0:
                print("✅ Windows инсталлятор успешно создан!")
                print(f"📦 Файл: {output_dir / 'FSA-DateStamp-Setup.exe'}")
                return True
            else:
                print(f"❌ Ошибка компиляции: {result.stderr}")
                return False
                
        except FileNotFoundError:
            print("❌ Inno Setup Compiler (iscc) не найден в PATH")
            return False
        except Exception as e:
            print(f"❌ Ошибка при сборке: {e}")
            return False
    
    def create_inno_setup_script(self):
        """Создание Inno Setup скрипта"""
        exe_path = self.project_root / "Distrib" / "Windows" / "FSA-DateStamp.exe"
        
        # Исправляем формат версии для Inno Setup (1.1.25.249 -> 1.01.25.249)
        version_parts = self.version.split('.')
        if len(version_parts) >= 2 and len(version_parts[1]) == 1:
            version_parts[1] = f"0{version_parts[1]}"
        fixed_version = '.'.join(version_parts)
        
        return f"""[Setup]
AppName=FSA-DateStamp
AppVersion={fixed_version}
AppPublisher=AW-Software
AppPublisherURL=https://github.com/foksserg
AppSupportURL=https://github.com/foksserg
AppUpdatesURL=https://github.com/foksserg
DefaultDirName={{autopf}}\\AW-Software\\FSA-DateStamp
DefaultGroupName=AW-Software\\FSA-DateStamp
AllowNoIcons=yes
LicenseFile=
OutputDir=installer_output
OutputBaseFilename=FSA-DateStamp-Setup
SetupIconFile=
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\\Russian.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{{cm:CreateQuickLaunchIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked; OnlyBelowVersion: 6.1

[Files]
Source: "{exe_path}"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "{self.project_root}\\Distrib\\Windows\\*"; DestDir: "{{app}}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{{group}}\\FSA-DateStamp"; Filename: "{{app}}\\FSA-DateStamp.exe"
Name: "{{group}}\\{{cm:UninstallProgram,FSA-DateStamp}}"; Filename: "{{uninstallexe}}"
Name: "{{autodesktop}}\\FSA-DateStamp"; Filename: "{{app}}\\FSA-DateStamp.exe"; Tasks: desktopicon
Name: "{{userappdata}}\\Microsoft\\Internet Explorer\\Quick Launch\\FSA-DateStamp"; Filename: "{{app}}\\FSA-DateStamp.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{{app}}\\FSA-DateStamp.exe"; Description: "{{cm:LaunchProgram,FSA-DateStamp}}"; Flags: nowait postinstall skipifsilent
"""
    
    def check_inno_setup(self):
        """Проверка наличия Inno Setup"""
        # Проверяем стандартные пути установки Inno Setup
        possible_paths = [
            r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
            r"C:\Program Files\Inno Setup 6\ISCC.exe",
            r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
            r"C:\Program Files\Inno Setup 5\ISCC.exe"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # Проверяем в PATH
        try:
            result = subprocess.run(["ISCC.exe", "/?"], capture_output=True, text=True)
            return "ISCC.exe" if result.returncode == 0 else False
        except FileNotFoundError:
            return False
    
    def build_macos_installer(self):
        """Сборка macOS инсталлятора (заглушка)"""
        print("🍎 Сборка macOS инсталлятора...")
        print("⚠️ macOS инсталлятор пока не реализован")
        print("📋 Планируется: PKG, DMG, App Store")
        return False
    
    def build_linux_installer(self):
        """Сборка Linux инсталлятора (заглушка)"""
        print("🐧 Сборка Linux инсталлятора...")
        print("⚠️ Linux инсталлятор пока не реализован")
        print("📋 Планируется: DEB, RPM, AppImage, Snap")
        return False
    
    def create_portable_version(self):
        """Создание портативной версии"""
        print("📦 Создание портативной версии...")
        
        if self.current_os == "windows":
            return self.create_windows_portable()
        elif self.current_os == "darwin":
            return self.create_macos_portable()
        elif self.current_os == "linux":
            return self.create_linux_portable()
        else:
            print(f"❌ Портативная версия для {self.current_os} не поддерживается")
            return False
    
    def create_windows_portable(self):
        """Создание Windows портативной версии"""
        windows_dir = self.installer_dir / "Windows"
        output_dir = windows_dir / "installer_output"
        output_dir.mkdir(exist_ok=True)
        
        portable_zip = output_dir / "FSA-DateStamp-Portable.zip"
        source_dir = self.project_root / "Distrib" / "Windows"
        
        try:
            import zipfile
            with zipfile.ZipFile(portable_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in source_dir.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(source_dir)
                        zipf.write(file_path, arcname)
            
            print(f"✅ Портативная версия создана: {portable_zip}")
            return True
        except Exception as e:
            print(f"❌ Ошибка создания портативной версии: {e}")
            return False
    
    def create_macos_portable(self):
        """Создание macOS портативной версии (заглушка)"""
        print("⚠️ macOS портативная версия пока не реализована")
        return False
    
    def create_linux_portable(self):
        """Создание Linux портативной версии (заглушка)"""
        print("⚠️ Linux портативная версия пока не реализована")
        return False

def main():
    """Главная функция"""
    import argparse
    
    parser = argparse.ArgumentParser(description='FSA-DateStamp Installer Builder')
    parser.add_argument('--os', choices=['windows', 'macos', 'linux'], 
                       help='Целевая ОС (по умолчанию - текущая)')
    parser.add_argument('--portable', action='store_true', 
                       help='Создать портативную версию')
    parser.add_argument('--all', action='store_true', 
                       help='Создать инсталляторы для всех ОС')
    
    args = parser.parse_args()
    
    builder = InstallerBuilder()
    
    if args.all:
        # Сборка для всех ОС
        success = True
        for os_name in ['windows', 'macos', 'linux']:
            print(f"\n{'='*60}")
            print(f"Сборка для {os_name.upper()}")
            print(f"{'='*60}")
            if not builder.build_installer(os_name):
                success = False
        return 0 if success else 1
    
    elif args.portable:
        # Создание портативной версии
        return 0 if builder.create_portable_version() else 1
    
    else:
        # Сборка для указанной или текущей ОС
        return 0 if builder.build_installer(args.os) else 1

if __name__ == "__main__":
    sys.exit(main())
