#!/usr/bin/env python3
"""
Скрипт сборки приложения для всех поддерживаемых платформ

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
import json
import shutil
import platform
import subprocess
import logging
import traceback
from datetime import datetime

# Импорт winreg только на Windows
if platform.system() == 'Windows':
    import winreg

# Настройка логирования
def setup_logging():
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, f'build_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    
    # Формат для файла
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # Формат для консоли
    console_formatter = logging.Formatter('%(message)s')
    
    # Настройка файлового логгера
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)
    
    # Настройка консольного логгера
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)
    
    # Создаем логгер
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logging()

def print_header(text):
    """Печать заголовка в консоль"""
    print("\n" + "=" * 80)
    print(f" {text} ".center(80, "="))
    print("=" * 80 + "\n")

def print_step(text):
    """Печать шага в консоль"""
    print(f"\n>>> {text}")

def print_success(text):
    """Печать успешного завершения в консоль"""
    print(f"\n✓ {text}")

def print_error(text):
    """Печать ошибки в консоль"""
    print(f"\n✗ {text}")

def print_warning(text):
    """Печать предупреждения в консоль"""
    print(f"\n! {text}")

def get_windows_version():
    """Определение версии Windows для выбора стратегии сборки"""
    try:
        if platform.system() != 'Windows':
            return 'unknown'
        
        # Сначала проверяем platform.platform() - это самый надежный способ
        platform_info = platform.platform()
        release = platform.release()
        
        logger.info(f"Platform: {platform_info}, Release: {release}")
        
        # Приоритет: platform.platform() для Windows 11
        if 'Windows-11' in platform_info or 'windows-11' in platform_info.lower():
            logger.info("Определено как Windows 11 по platform.platform()")
            return 'windows11'
        
        # Получаем версию Windows из реестра для остальных случаев
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                               r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
            version, _ = winreg.QueryValueEx(key, "CurrentVersion")
            build_number, _ = winreg.QueryValueEx(key, "CurrentBuild")
            product_name, _ = winreg.QueryValueEx(key, "ProductName")
            winreg.CloseKey(key)
            
            logger.info(f"Registry: version={version}, build={build_number}, product={product_name}")
            
            # Определяем версию по номеру и build number
            if version.startswith('6.1'):
                return 'windows7'
            elif version.startswith('6.2'):
                return 'windows8'
            elif version.startswith('6.3'):
                return 'windows8_1'
            elif version.startswith('10.0'):
                # Windows 10 vs Windows 11 по build number и названию продукта
                try:
                    build = int(build_number)
                    product_lower = product_name.lower()
                    
                    # Проверяем название продукта для Windows 11
                    if 'windows 11' in product_lower or build >= 22000:
                        return 'windows11'
                    else:  # Windows 10
                        return 'windows10'
                except ValueError:
                    return 'windows10'  # Fallback
            else:
                return 'windows11'
                
        except Exception as e:
            logger.warning(f"Ошибка чтения реестра: {str(e)}")
            # Fallback - используем platform.release()
            if release == '7':
                return 'windows7'
            elif release == '8':
                return 'windows8'
            elif release == '8.1':
                return 'windows8_1'
            elif release == '10':
                return 'windows10'
            else:
                return 'windows11'
                
    except Exception as e:
        logger.warning(f"Не удалось определить версию Windows: {str(e)}")
        return 'unknown'

def _get_target_dir_name(windows_version):
    """Получение имени целевой директории на основе версии Windows"""
    if windows_version == 'windows7':
        return 'Windows7'
    elif windows_version in ['windows8', 'windows8_1']:
        return 'Windows8'
    elif windows_version == 'windows10':
        return 'Windows10'
    elif windows_version == 'windows11':
        return 'Windows11'
    else:
        return 'Universal'

class BuildConfig:
    """Конфигурация сборки"""
    
    def __init__(self):
        try:
            self.system = platform.system()
            self.machine = platform.machine()
            logger.info(f"Инициализация сборки для {self.system} {self.machine}")
            
            # Определяем платформу
            self.is_windows = self.system == 'Windows'
            self.is_macos = self.system == 'Darwin'
            self.is_linux = self.system == 'Linux'
            
            # Пути к ресурсам
            self.base_dir = os.path.dirname(os.path.abspath(__file__))
            self.project_root = os.path.dirname(self.base_dir)
            self.icons_dir = os.path.join(self.base_dir, 'Icons')
            
            # Определяем версию Windows для версионных сборок
            self.windows_version = get_windows_version() if self.is_windows else None
            
            # Определяем платформо-специфичные директории
            if self.is_windows:
                # Создаем только нужную директорию для текущей версии Windows
                target_dir_name = _get_target_dir_name(self.windows_version)
                self.platform_dirs = {target_dir_name: os.path.join(self.base_dir, target_dir_name)}
            elif self.is_macos:
                self.platform_dirs = {'MacOS': os.path.join(self.base_dir, 'MacOS')}
            else:
                self.platform_dirs = {'Linux': os.path.join(self.base_dir, 'Linux')}
            
            # Загружаем конфигурацию сборки
            self.config_path = os.path.join(self.base_dir, 'build_config.json')
            self.load_config()
            
            # Проверяем и создаем иконки если нужно
            self._ensure_icons()
            
            # Создаем необходимые директории
            self._create_directories()
            
        except Exception as e:
            logger.error(f"Ошибка инициализации конфигурации: {str(e)}")
            logger.error(traceback.format_exc())
            raise
            
    def _ensure_icons(self):
        """Проверка наличия иконок и их создание при необходимости"""
        try:
            required_icons = {
                'Windows': 'app.ico',
                'Darwin': 'app.icns',
                'Linux': 'app.png'
            }
            
            # Проверяем нужны ли иконки
            if not os.path.exists(self.icons_dir):
                logger.info("Директория иконок не найдена, создаем иконки")
                self._create_icons()
            else:
                # Проверяем наличие нужной иконки для текущей платформы
                required_icon = required_icons.get(self.system)
                if required_icon and not os.path.exists(os.path.join(self.icons_dir, required_icon)):
                    logger.info(f"Иконка {required_icon} не найдена, создаем иконки")
                    self._create_icons()
                    
        except Exception as e:
            logger.error(f"Ошибка при проверке иконок: {str(e)}")
            logger.error(traceback.format_exc())
            raise
                
    def _create_icons(self):
        """Создание иконок с помощью Create_Icons.py"""
        try:
            create_icons_path = os.path.join(self.base_dir, 'Create_Icons.py')
            if os.path.exists(create_icons_path):
                logger.info("Запуск создания иконок")
                result = subprocess.run([sys.executable, create_icons_path], 
                                     check=True, 
                                     capture_output=True, 
                                     text=True)
                logger.info(result.stdout)
                if result.stderr:
                    logger.warning(result.stderr)
                logger.info("Иконки успешно созданы")
            else:
                error_msg = "ВНИМАНИЕ: Create_Icons.py не найден!"
                logger.error(error_msg)
                raise FileNotFoundError(error_msg)
                
        except subprocess.CalledProcessError as e:
            logger.error(f"Ошибка при создании иконок: {str(e)}")
            logger.error(f"Вывод: {e.stdout}\nОшибка: {e.stderr}")
            raise
        except Exception as e:
            logger.error(f"Неожиданная ошибка при создании иконок: {str(e)}")
            logger.error(traceback.format_exc())
            raise
        
    def load_config(self):
        """Загрузка конфигурации сборки"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    self.build_config = json.load(f)
                logger.info("Конфигурация сборки успешно загружена")
            else:
                logger.warning(f"Файл конфигурации {self.config_path} не найден, используются значения по умолчанию")
                self.build_config = {
                    "include_files": ["src/**/*.py", "resources/*"],
                    "exclude_files": ["**/__pycache__", "*.log", "*.db", "logs/*", "*.pyc"]
                }
                
        except Exception as e:
            logger.error(f"Ошибка загрузки конфигурации: {str(e)}")
            logger.error(traceback.format_exc())
            raise
            
    def _create_directories(self):
        """Создание необходимых директорий"""
        try:
            # Создаем платформо-специфичные директории
            for platform_name, platform_dir in self.platform_dirs.items():
                if not os.path.exists(platform_dir):
                    logger.info(f"Создание директории для {platform_name}: {platform_dir}")
                    os.makedirs(platform_dir)
                    
        except Exception as e:
            logger.error(f"Ошибка при создании директорий: {str(e)}")
            logger.error(traceback.format_exc())
            raise
                
    def get_target_directory(self):
        """Получение целевой директории для сборки на основе версии Windows"""
        try:
            if self.is_windows:
                # Возвращаем единственную созданную директорию
                return list(self.platform_dirs.values())[0]
            elif self.is_macos:
                return self.platform_dirs['MacOS']
            else:
                return self.platform_dirs['Linux']
                
        except Exception as e:
            logger.error(f"Ошибка при определении целевой директории: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def clean_target_directory(self):
        """Очистка целевой директории перед сборкой"""
        try:
            target_dir = self.get_target_directory()
                
            if os.path.exists(target_dir):
                logger.info(f"Очистка целевой директории: {target_dir}")
                for item in os.listdir(target_dir):
                    item_path = os.path.join(target_dir, item)
                    try:
                        if os.path.isfile(item_path):
                            os.unlink(item_path)
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                    except Exception as e:
                        logger.error(f"Ошибка при удалении {item_path}: {str(e)}")
                        
        except Exception as e:
            logger.error(f"Ошибка при очистке целевой директории: {str(e)}")
            logger.error(traceback.format_exc())
            raise
                    
    def clean_temp_files(self, exclude_dist=False):
        """Очистка временных файлов сборки"""
        temp_files = [
            'build',
            'FSA-DateStamp.spec',
            'FSA-DateStamp-Windows.zip',
            'FSA-DateStamp-MacOS.zip',
            'FSA-DateStamp-Linux.tar'
        ]
        
        # Добавляем dist только если не исключаем его
        if not exclude_dist:
            temp_files.append('dist')
        
        logger.info("Начало очистки временных файлов")
        # Очищаем в директории сборки
        for item in temp_files:
            item_path = os.path.join(self.base_dir, item)
            try:
                if os.path.exists(item_path):
                    logger.info(f"Удаление {item_path}")
                    if os.path.isfile(item_path):
                        os.unlink(item_path)
                    else:
                        shutil.rmtree(item_path)
            except Exception as e:
                logger.error(f"Ошибка при удалении {item_path}: {str(e)}")
                logger.error(traceback.format_exc())
                
    def _create_version_file(self, version_file):
        """Создание файла version.txt с учетом версии Windows"""
        try:
            # Определяем OS код для версии Windows
            if self.windows_version == 'windows7':
                os_code = '0x40001'  # Windows 7
                description = 'FSA-DateStamp - Версия для Windows 7'
            elif self.windows_version in ['windows8', 'windows8_1']:
                os_code = '0x40002'  # Windows 8
                description = 'FSA-DateStamp - Версия для Windows 8/8.1'
            elif self.windows_version == 'windows10':
                os_code = '0x40004'  # Windows 10
                description = 'FSA-DateStamp - Версия для Windows 10'
            elif self.windows_version == 'windows11':
                os_code = '0x40004'  # Windows 11 (использует тот же код)
                description = 'FSA-DateStamp - Версия для Windows 11'
            else:
                os_code = '0x40004'  # Fallback
                description = 'FSA-DateStamp - Универсальная версия'
            
            version_content = f"""VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 1, 25, 249),
    prodvers=(1, 1, 25, 249),
    mask=0x3f,
    flags=0x0,
    OS={os_code},
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'AW-Software'),
        StringStruct(u'FileDescription', u'{description}'),
        StringStruct(u'FileVersion', u'1.01.25.249'),
        StringStruct(u'InternalName', u'FSA-DateStamp'),
        StringStruct(u'LegalCopyright', u'Copyright (c) 2025 AW-Software'),
        StringStruct(u'OriginalFilename', u'FSA-DateStamp.exe'),
        StringStruct(u'ProductName', u'FSA-DateStamp'),
        StringStruct(u'ProductVersion', u'1.01.25.249')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)"""
            
            with open(version_file, 'w', encoding='utf-8') as f:
                f.write(version_content)
            logger.info(f"Создан файл version.txt для {self.windows_version}")
            
        except Exception as e:
            logger.error(f"Ошибка при создании version.txt: {str(e)}")
            raise

    def get_build_params(self):
        """Получение параметров сборки для текущей платформы"""
        try:
            # Базовые параметры
            params = [
                '--noconfirm',
                '--onefile',
                '--windowed',
                '--name', 'FSA-DateStamp',
                '--add-data', f'{self.icons_dir}{os.pathsep}icons',
                '--specpath', self.base_dir,
                '--workpath', os.path.join(self.base_dir, 'build'),
                '--distpath', os.path.join(self.base_dir, 'dist')
            ]
            
            # Специфичные параметры для Windows (версионные сборки)
            if self.is_windows:
                icon_path = os.path.join(self.icons_dir, 'app.ico')
                if os.path.exists(icon_path):
                    params.extend(['--icon', icon_path])
                
                # Создаем version.txt с учетом версии Windows
                version_file = os.path.join(self.project_root, 'version.txt')
                self._create_version_file(version_file)
                
                # Базовые параметры для всех версий Windows
                params.extend([
                    '--version-file', version_file,
                    '--uac-admin',
                    '--clean',
                    '--noconsole'
                ])
                
                # Специфичные параметры в зависимости от версии Windows
                if self.windows_version == 'windows7':
                    # Windows 7 - максимальная совместимость
                    params.extend([
                        '--target-arch', 'x86',  # x86 для максимальной совместимости
                        '--win-private-assemblies',
                        '--win-no-prefer-redirects'
                    ])
                    logger.info("Сборка для Windows 7 - режим максимальной совместимости")
                else:
                    # Windows 8+ - современные параметры
                    params.extend([
                        '--target-arch', 'x64'  # x64 для современных версий
                    ])
                    logger.info(f"Сборка для {self.windows_version} - современный режим")
                
                # Добавляем скрытые импорты для FSA-DateStamp (универсальная совместимость)
                # Основные модули приложения
                params.extend(['--hidden-import', 'DateStampGUI'])
                params.extend(['--hidden-import', 'DateStamp'])
                params.extend(['--hidden-import', 'PacketFolder'])
                
                # PIL и его модули
                params.extend(['--hidden-import', 'PIL'])
                params.extend(['--hidden-import', 'PIL.Image'])
                params.extend(['--hidden-import', 'PIL.ImageDraw'])
                params.extend(['--hidden-import', 'PIL.ImageFont'])
                params.extend(['--hidden-import', 'PIL.ImageFilter'])
                params.extend(['--hidden-import', 'PIL.ImageOps'])
                params.extend(['--hidden-import', 'PIL.ImageEnhance'])
                
                # OpenCV
                # cv2 импортируется условно в коде
                
                # EXIF библиотеки
                params.extend(['--hidden-import', 'exifread'])
                params.extend(['--hidden-import', 'piexif'])
                
                # tkinter и его модули
                params.extend(['--hidden-import', 'tkinter'])
                params.extend(['--hidden-import', 'tkinter.filedialog'])
                params.extend(['--hidden-import', 'tkinter.ttk'])
                params.extend(['--hidden-import', 'tkinter.messagebox'])
                params.extend(['--hidden-import', 'tkinter.simpledialog'])
                params.extend(['--hidden-import', 'tkinter.colorchooser'])
                
                # Стандартные библиотеки Python
                params.extend(['--hidden-import', 'configparser'])
                params.extend(['--hidden-import', 'argparse'])
                params.extend(['--hidden-import', 'shutil'])
                params.extend(['--hidden-import', 'stat'])
                params.extend(['--hidden-import', 'subprocess'])
                params.extend(['--hidden-import', 'datetime'])
                params.extend(['--hidden-import', 'os'])
                params.extend(['--hidden-import', 'sys'])
                params.extend(['--hidden-import', 'json'])
                params.extend(['--hidden-import', 'logging'])
                params.extend(['--hidden-import', 'traceback'])
                
                # Дополнительные модули для совместимости
                params.extend(['--hidden-import', 'numpy'])
                params.extend(['--hidden-import', 'numpy.core'])
                params.extend(['--hidden-import', 'numpy.core._methods'])
                params.extend(['--hidden-import', 'numpy.lib.format'])
                
                # Windows-специфичные модули
                params.extend(['--hidden-import', 'win32api'])
                params.extend(['--hidden-import', 'win32con'])
                params.extend(['--hidden-import', 'win32gui'])
                params.extend(['--hidden-import', 'win32process'])
                params.extend(['--hidden-import', 'pywintypes'])
                
            # Специфичные параметры для macOS
            elif self.is_macos:
                icon_path = os.path.join(self.icons_dir, 'app.icns')
                if os.path.exists(icon_path):
                    params.extend(['--icon', icon_path])
                params.extend([
                    '--osx-bundle-identifier', 'com.fsa.datestamp'
                ])
                
            # Специфичные параметры для Linux
            elif self.is_linux:
                icon_path = os.path.join(self.icons_dir, 'app.png')
                if os.path.exists(icon_path):
                    params.extend(['--icon', icon_path])
                params.extend([
                    '--clean'
                ])
                
            # Добавляем скрытые импорты для всех модулей (только для не-Windows платформ)
            if not self.is_windows:
                params.extend(['--hidden-import', 'DateStampGUI'])
                params.extend(['--hidden-import', 'DateStamp'])
                params.extend(['--hidden-import', 'PacketFolder'])
                
                # tkinter и его модули
                params.extend(['--hidden-import', 'tkinter'])
                params.extend(['--hidden-import', 'tkinter.filedialog'])
                params.extend(['--hidden-import', 'tkinter.ttk'])
                params.extend(['--hidden-import', 'tkinter.messagebox'])
                
                # PIL и его модули
                params.extend(['--hidden-import', 'PIL'])
                params.extend(['--hidden-import', 'PIL.Image'])
                params.extend(['--hidden-import', 'PIL.ImageDraw'])
                params.extend(['--hidden-import', 'PIL.ImageFont'])
                
                # OpenCV
                # cv2 импортируется условно в коде
                
                # EXIF библиотеки
                params.extend(['--hidden-import', 'exifread'])
                params.extend(['--hidden-import', 'piexif'])
                
                # Стандартные библиотеки
                params.extend(['--hidden-import', 'configparser'])
                params.extend(['--hidden-import', 'argparse'])
                params.extend(['--hidden-import', 'shutil'])
                params.extend(['--hidden-import', 'stat'])
                params.extend(['--hidden-import', 'subprocess'])
                params.extend(['--hidden-import', 'datetime'])
            
            # Добавляем папку src как данные
            src_path = os.path.join(self.project_root, 'src')
            if os.path.exists(src_path):
                # Используем правильный разделитель для PyInstaller на macOS/Unix
                params.extend(['--add-data', f'{src_path}{os.pathsep}src'])
            
            # Добавляем путь к основному скрипту (GUI версия)
            script_path = os.path.join(self.project_root, 'src', 'start_gui.py')
            params.append(script_path)
            
            logger.info(f"Параметры сборки: {params}")
            return params
            
        except Exception as e:
            logger.error(f"Ошибка при формировании параметров сборки: {str(e)}")
            logger.error(traceback.format_exc())
            raise
            
    def get_output_path(self):
        """Получение пути к собранному приложению"""
        try:
            if self.is_windows:
                target_dir = self.get_target_directory()
                return os.path.join(target_dir, 'FSA-DateStamp.exe')
            elif self.is_macos:
                return os.path.join(self.platform_dirs['MacOS'], 'FSA-DateStamp.app')
            else:  # Linux
                return os.path.join(self.platform_dirs['Linux'], 'FSA-DateStamp')
                
        except Exception as e:
            logger.error(f"Ошибка при определении пути вывода: {str(e)}")
            logger.error(traceback.format_exc())
            raise

def build():
    """Сборка приложения"""
    config = None
    try:
        print_header("НАЧАЛО СБОРКИ ПРИЛОЖЕНИЯ")
        
        # Инициализация конфигурации
        print_step("Инициализация конфигурации сборки")
        config = BuildConfig()
        
        # Проверяем платформу
        if config.is_windows and not platform.system() == 'Windows':
            error_msg = "ВНИМАНИЕ: Сборка Windows-версии возможна только на Windows!"
            print_error(error_msg)
            logger.error(error_msg)
            raise RuntimeError(error_msg)
            
        # Очищаем целевую директорию
        print_step("Очистка целевой директории")
        config.clean_target_directory()
            
        # Получаем параметры сборки
        print_step("Подготовка параметров сборки")
        build_params = config.get_build_params()
        
        # Собираем команду
        cmd = ['pyinstaller'] + build_params
        
        # Запускаем сборку
        print_step("Запуск сборки")
        print(f"Команда: {' '.join(cmd)}")
        # Запускаем PyInstaller из корня проекта для правильного поиска файлов
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, cwd=config.project_root)
        logger.info(result.stdout)
        if result.stderr:
            logger.warning(result.stderr)
        
        # Перемещаем собранное приложение в соответствующую директорию
        print_step("Перемещение собранного приложения")
        move_success = False
        
        if config.is_windows:
            source_file = os.path.join(config.base_dir, 'dist', 'FSA-DateStamp.exe')
            if os.path.exists(source_file):
                target_dir = config.get_target_directory()
                print(f"Перемещение Windows-версии для {config.windows_version}")
                try:
                    # Очищаем целевую директорию перед копированием
                    if os.path.exists(target_dir):
                        shutil.rmtree(target_dir)
                    os.makedirs(target_dir, exist_ok=True)
                    
                    # Копируем исполняемый файл
                    target_file = os.path.join(target_dir, 'FSA-DateStamp.exe')
                    shutil.copy2(source_file, target_file)
                    move_success = True
                    logger.info(f"Windows-версия для {config.windows_version} успешно перемещена в {target_dir}")
                except Exception as e:
                    logger.error(f"Ошибка при перемещении Windows-версии: {str(e)}")
                    raise
            else:
                logger.error(f"Файл {source_file} не найден!")
                raise FileNotFoundError(f"Собранное приложение не найдено: {source_file}")
                
        elif config.is_macos:
            app_path = os.path.join(config.base_dir, 'dist', 'FSA-DateStamp.app')
            if os.path.exists(app_path):
                print("Перемещение macOS-версии")
                target_path = os.path.join(config.platform_dirs['MacOS'], 'FSA-DateStamp.app')
                try:
                    if os.path.exists(target_path):
                        shutil.rmtree(target_path)
                    shutil.copytree(app_path, target_path)
                    move_success = True
                    logger.info(f"macOS-версия успешно перемещена в {config.platform_dirs['MacOS']}")
                except Exception as e:
                    logger.error(f"Ошибка при перемещении macOS-версии: {str(e)}")
                    raise
            else:
                logger.error(f"Приложение {app_path} не найдено!")
                raise FileNotFoundError(f"Собранное приложение не найдено: {app_path}")
                
        else:  # Linux
            source_path = os.path.join(config.base_dir, 'dist', 'FSA-DateStamp')
            if os.path.exists(source_path):
                print("Перемещение Linux-версии")
                try:
                    shutil.move(source_path, config.platform_dirs['Linux'])
                    move_success = True
                    logger.info(f"Linux-версия успешно перемещена в {config.platform_dirs['Linux']}")
                except Exception as e:
                    logger.error(f"Ошибка при перемещении Linux-версии: {str(e)}")
                    raise
            else:
                logger.error(f"Файл {source_path} не найден!")
                raise FileNotFoundError(f"Собранное приложение не найдено: {source_path}")
            
        print_success("Сборка завершена успешно!")
        print("Результаты сборки находятся в:")
        if config.is_windows:
            target_dir = config.get_target_directory()
            print(f"- Windows {config.windows_version}: {target_dir}")
        elif config.is_macos:
            print(f"- MacOS: {config.platform_dirs['MacOS']}")
        else:
            print(f"- Linux: {config.platform_dirs['Linux']}")
            
        # ОБЯЗАТЕЛЬНАЯ очистка временных файлов после успешной сборки
        print_step("Очистка временных файлов сборки")
        config.clean_temp_files(exclude_dist=False)
        print_success("Временные файлы успешно удалены")
            
    except subprocess.CalledProcessError as e:
        print_error(f"Ошибка выполнения команды: {str(e)}")
        logger.error(f"Ошибка выполнения команды: {str(e)}")
        logger.error(f"Вывод: {e.stdout}\nОшибка: {e.stderr}")
    except Exception as e:
        print_error(f"Ошибка сборки: {str(e)}")
        logger.error(f"Ошибка сборки: {str(e)}")
        logger.error(traceback.format_exc())
    finally:
        # Очищаем временные файлы только при ошибке
        if config and 'move_success' not in locals():
            try:
                print_step("Очистка временных файлов после ошибки")
                config.clean_temp_files(exclude_dist=False)
                print_success("Временные файлы успешно удалены")
            except Exception as e:
                print_error(f"Ошибка при очистке временных файлов: {str(e)}")
                logger.error(f"Ошибка при очистке временных файлов: {str(e)}")
                logger.error(traceback.format_exc())

if __name__ == "__main__":
    build() 