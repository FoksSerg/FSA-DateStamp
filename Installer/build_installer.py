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
    
    def build_installer(self):
        """Сборка инсталлятора для текущей ОС"""
        print(f"🚀 Начинаем сборку инсталлятора для {self.current_os.upper()}")
        
        # Проверяем наличие собранного приложения
        if not self.check_built_application():
            print("❌ Сначала необходимо собрать приложение через Build.py")
            return False
        
        # Выбираем метод сборки в зависимости от текущей ОС
        if self.current_os == "windows":
            return self.build_windows_installer()
        elif self.current_os == "darwin":  # macOS
            return self.build_macos_installer()
        elif self.current_os == "linux":
            return self.build_linux_installer()
        else:
            print(f"❌ Неподдерживаемая ОС: {self.current_os}")
            return False
    
    def check_built_application(self):
        """Проверка наличия собранного приложения"""
        if self.current_os == "windows":
            # Проверяем наличие всех версий Windows дистрибутивов
            windows_versions = ['Windows7', 'Windows8', 'Windows10', 'Windows11']
            available_versions = []
            
            for version in windows_versions:
                exe_path = self.project_root / "Distrib" / version / "FSA-DateStamp.exe"
                if exe_path.exists():
                    available_versions.append(version)
            
            if available_versions:
                print(f"✅ Найдены дистрибутивы для Windows: {', '.join(available_versions)}")
                return True
            else:
                print("❌ Не найдено ни одного Windows дистрибутива")
                return False
                
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
        """Создание универсального Inno Setup скрипта для существующих версий Windows"""
        
        # Исправляем формат версии для Inno Setup (1.1.25.249 -> 1.01.25.249)
        version_parts = self.version.split('.')
        if len(version_parts) >= 2 and len(version_parts[1]) == 1:
            version_parts[1] = f"0{version_parts[1]}"
        fixed_version = '.'.join(version_parts)
        
        # Получаем пути к дистрибутивам и проверяем их существование
        distrib_path = self.project_root / "Distrib"
        available_versions = {}
        
        # Проверяем каждую версию Windows
        versions_to_check = [
            ('Windows7', 'Windows 7'),
            ('Windows8', 'Windows 8/8.1'),
            ('Windows10', 'Windows 10'),
            ('Windows11', 'Windows 11')
        ]
        
        for folder_name, display_name in versions_to_check:
            exe_path = distrib_path / folder_name / "FSA-DateStamp.exe"
            if exe_path.exists():
                available_versions[folder_name] = {
                    'path': exe_path,
                    'display_name': display_name,
                    'exe_name': f"FSA-DateStamp-{folder_name}.exe"
                }
                print(f"✅ Найден дистрибутив: {display_name}")
            else:
                print(f"⚠️ Дистрибутив не найден: {display_name}")
        
        if not available_versions:
            raise FileNotFoundError("Не найдено ни одного Windows дистрибутива!")
        
        # Определяем fallback версию (приоритет: Windows10 > Windows11 > Windows8 > Windows7)
        fallback_version = None
        for preferred in ['Windows10', 'Windows11', 'Windows8', 'Windows7']:
            if preferred in available_versions:
                fallback_version = preferred
                break
        
        # Генерируем секцию [Files] только для существующих версий
        files_section = ""
        for version_name, version_info in available_versions.items():
            check_function = f"Is{version_name}"
            files_section += f'; {version_info["display_name"]} версия\n'
            files_section += f'Source: "{version_info["path"]}"; DestDir: "{{app}}"; DestName: "{version_info["exe_name"]}"; Flags: ignoreversion; Check: {check_function}\n'
        
        # Генерируем ВСЕ функции проверки версий (используем простой подход)
        version_checks = """function IsWindows7: Boolean;
var
  Version: TWindowsVersion;
begin
  GetWindowsVersionEx(Version);
  Result := (Version.Major = 6) and (Version.Minor = 1);
end;

function IsWindows8: Boolean;
var
  Version: TWindowsVersion;
begin
  GetWindowsVersionEx(Version);
  Result := (Version.Major = 6) and ((Version.Minor = 2) or (Version.Minor = 3));
end;

function IsWindows10: Boolean;
var
  Version: TWindowsVersion;
begin
  GetWindowsVersionEx(Version);
  Result := (Version.Major = 10) and (Version.Minor = 0) and (Version.Build < 22000);
end;

function IsWindows11: Boolean;
var
  Version: TWindowsVersion;
begin
  GetWindowsVersionEx(Version);
  Result := (Version.Major = 10) and (Version.Minor = 0) and (Version.Build >= 22000);
end;

"""
        
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
OutputBaseFilename=FSA-DateStamp-Universal-Setup
SetupIconFile=
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
MinVersion=6.1

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\\Russian.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{{cm:CreateQuickLaunchIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked; OnlyBelowVersion: 6.1

[Files]
{files_section}

[Icons]
Name: "{{group}}\\FSA-DateStamp"; Filename: "{{app}}\\FSA-DateStamp.exe"
Name: "{{group}}\\{{cm:UninstallProgram,FSA-DateStamp}}"; Filename: "{{uninstallexe}}"
Name: "{{autodesktop}}\\FSA-DateStamp"; Filename: "{{app}}\\FSA-DateStamp.exe"; Tasks: desktopicon
Name: "{{userappdata}}\\Microsoft\\Internet Explorer\\Quick Launch\\FSA-DateStamp"; Filename: "{{app}}\\FSA-DateStamp.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{{app}}\\FSA-DateStamp.exe"; Description: "{{cm:LaunchProgram,FSA-DateStamp}}"; Flags: nowait postinstall skipifsilent

[Code]
{version_checks}

procedure CurStepChanged(CurStep: TSetupStep);
var
  SourceFile, DestFile: AnsiString;
begin
  if CurStep = ssPostInstall then
  begin
    // Выбираем нужный исполняемый файл на основе версии Windows
    SourceFile := '';
    DestFile := ExpandConstant('{{app}}\\FSA-DateStamp.exe');
    
    // Выбираем версию по принципу совместимости
    if IsWindows7 then
    begin
      // На Windows 7 - только Windows 7 сборка
      if FileExists(ExpandConstant('{{app}}\\FSA-DateStamp-Windows7.exe')) then
        SourceFile := ExpandConstant('{{app}}\\FSA-DateStamp-Windows7.exe')
      else
      begin
        MsgBox('Ошибка: Для Windows 7 требуется специальная сборка FSA-DateStamp-Windows7.exe, которая не найдена в пакете установки.', mbError, MB_OK);
        Abort;
      end;
    end
    else if IsWindows8 then
    begin
      // На Windows 8 - ищем Windows 8, затем Windows 10, затем Windows 11
      if FileExists(ExpandConstant('{{app}}\\FSA-DateStamp-Windows8.exe')) then
        SourceFile := ExpandConstant('{{app}}\\FSA-DateStamp-Windows8.exe')
      else if FileExists(ExpandConstant('{{app}}\\FSA-DateStamp-Windows10.exe')) then
        SourceFile := ExpandConstant('{{app}}\\FSA-DateStamp-Windows10.exe')
      else if FileExists(ExpandConstant('{{app}}\\FSA-DateStamp-Windows11.exe')) then
        SourceFile := ExpandConstant('{{app}}\\FSA-DateStamp-Windows11.exe')
      else
      begin
        MsgBox('Ошибка: Не найдено ни одной совместимой сборки для Windows 8.', mbError, MB_OK);
        Abort;
      end;
    end
    else if IsWindows10 then
    begin
      // На Windows 10 - ищем Windows 10, затем Windows 11, затем Windows 8
      if FileExists(ExpandConstant('{{app}}\\FSA-DateStamp-Windows10.exe')) then
        SourceFile := ExpandConstant('{{app}}\\FSA-DateStamp-Windows10.exe')
      else if FileExists(ExpandConstant('{{app}}\\FSA-DateStamp-Windows11.exe')) then
        SourceFile := ExpandConstant('{{app}}\\FSA-DateStamp-Windows11.exe')
      else if FileExists(ExpandConstant('{{app}}\\FSA-DateStamp-Windows8.exe')) then
        SourceFile := ExpandConstant('{{app}}\\FSA-DateStamp-Windows8.exe')
      else
      begin
        MsgBox('Ошибка: Не найдено ни одной совместимой сборки для Windows 10.', mbError, MB_OK);
        Abort;
      end;
    end
    else if IsWindows11 then
    begin
      // На Windows 11 - ищем Windows 11, затем Windows 10, затем Windows 8
      if FileExists(ExpandConstant('{{app}}\\FSA-DateStamp-Windows11.exe')) then
        SourceFile := ExpandConstant('{{app}}\\FSA-DateStamp-Windows11.exe')
      else if FileExists(ExpandConstant('{{app}}\\FSA-DateStamp-Windows10.exe')) then
        SourceFile := ExpandConstant('{{app}}\\FSA-DateStamp-Windows10.exe')
      else if FileExists(ExpandConstant('{{app}}\\FSA-DateStamp-Windows8.exe')) then
        SourceFile := ExpandConstant('{{app}}\\FSA-DateStamp-Windows8.exe')
      else
      begin
        MsgBox('Ошибка: Не найдено ни одной совместимой сборки для Windows 11.', mbError, MB_OK);
        Abort;
      end;
    end
    else
    begin
      MsgBox('Ошибка: Неподдерживаемая версия Windows.', mbError, MB_OK);
      Abort;
    end;
    
    // Копируем выбранный файл как основной
    if SourceFile <> '' then
    begin
      FileCopy(SourceFile, DestFile, False);
      // Удаляем временные файлы версий
      DeleteFile(ExpandConstant('{{app}}\\FSA-DateStamp-Windows7.exe'));
      DeleteFile(ExpandConstant('{{app}}\\FSA-DateStamp-Windows8.exe'));
      DeleteFile(ExpandConstant('{{app}}\\FSA-DateStamp-Windows10.exe'));
      DeleteFile(ExpandConstant('{{app}}\\FSA-DateStamp-Windows11.exe'));
    end;
  end;
end;
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
    parser.add_argument('--portable', action='store_true', 
                       help='Создать портативную версию')
    
    args = parser.parse_args()
    
    builder = InstallerBuilder()
    
    if args.portable:
        # Создание портативной версии
        return 0 if builder.create_portable_version() else 1
    
    else:
        # Сборка инсталлятора для текущей ОС
        return 0 if builder.build_installer() else 1

if __name__ == "__main__":
    sys.exit(main())
