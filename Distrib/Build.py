#!/usr/bin/env python3
"""
Скрипт сборки приложения для всех поддерживаемых платформ
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
            
            # Определяем только текущую платформу для сборки
            if self.is_windows:
                self.platform_dirs = {'Windows': os.path.join(self.base_dir, 'Windows')}
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
                
    def clean_target_directory(self):
        """Очистка целевой директории перед сборкой"""
        try:
            if self.is_windows:
                target_dir = self.platform_dirs['Windows']
            elif self.is_macos:
                target_dir = self.platform_dirs['MacOS']
            else:
                target_dir = self.platform_dirs['Linux']
                
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
                    
    def clean_temp_files(self):
        """Очистка временных файлов сборки"""
        temp_files = [
            'build',
            'dist',
            'FSA-DateStamp.spec',
            'FSA-DateStamp-Windows.zip',
            'FSA-DateStamp-MacOS.zip',
            'FSA-DateStamp-Linux.tar'
        ]
        
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
                
    def get_build_params(self):
        """Получение параметров сборки для текущей платформы"""
        try:
            # Базовые параметры
            params = [
                '--noconfirm',
                '--onedir',
                '--windowed',
                '--name', 'FSA-DateStamp',
                '--add-data', f'{self.icons_dir}:icons',
                '--specpath', self.base_dir,
                '--workpath', os.path.join(self.base_dir, 'build'),
                '--distpath', os.path.join(self.base_dir, 'dist')
            ]
            
            # Специфичные параметры для Windows
            if self.is_windows:
                icon_path = os.path.join(self.icons_dir, 'app.ico')
                if os.path.exists(icon_path):
                    params.extend(['--icon', icon_path])
                
                # Проверяем/создаем version.txt
                version_file = os.path.join(self.project_root, 'version.txt')
                if not os.path.exists(version_file):
                    logger.info("Создаем файл version.txt")
                    with open(version_file, 'w', encoding='utf-8') as f:
                        f.write("""VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'FSA'),
        StringStruct(u'FileDescription', u'FSA-DateStamp - Добавление водяных знаков с датой'),
        StringStruct(u'FileVersion', u'1.0.0'),
        StringStruct(u'InternalName', u'FSA-DateStamp'),
        StringStruct(u'LegalCopyright', u'Copyright (c) 2024'),
        StringStruct(u'OriginalFilename', u'FSA-DateStamp.exe'),
        StringStruct(u'ProductName', u'FSA-DateStamp'),
        StringStruct(u'ProductVersion', u'1.0.0')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)""")
                
                params.extend([
                    '--version-file', version_file,
                    '--uac-admin',
                    '--clean',
                    '--target-arch', 'x64',
                    '--noconsole'
                ])
                
                # Добавляем скрытые импорты для FSA-DateStamp
                params.extend(['--hidden-import', 'PIL'])
                params.extend(['--hidden-import', 'PIL.Image'])
                params.extend(['--hidden-import', 'PIL.ImageDraw'])
                params.extend(['--hidden-import', 'PIL.ImageFont'])
                params.extend(['--hidden-import', 'cv2'])
                params.extend(['--hidden-import', 'exifread'])
                params.extend(['--hidden-import', 'piexif'])
                params.extend(['--hidden-import', 'tkinter'])
                params.extend(['--hidden-import', 'tkinter.filedialog'])
                params.extend(['--hidden-import', 'tkinter.ttk'])
                params.extend(['--hidden-import', 'configparser'])
                
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
                
            # Добавляем скрытые импорты для всех модулей
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
            params.extend(['--hidden-import', 'cv2'])
            
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
                # Используем правильный разделитель для PyInstaller
                params.extend(['--add-data', f'{src_path}:src'])
            
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
                return os.path.join(self.platform_dirs['Windows'], 'FSA-DateStamp.exe')
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
        if config.is_windows:
            if os.path.exists(os.path.join(config.base_dir, 'dist', 'FSA-DateStamp.exe')):
                print("Перемещение Windows-версии")
                shutil.move(
                    os.path.join(config.base_dir, 'dist', 'FSA-DateStamp.exe'),
                    config.platform_dirs['Windows']
                )
        elif config.is_macos:
            app_path = os.path.join(config.base_dir, 'dist', 'FSA-DateStamp.app')
            if os.path.exists(app_path):
                print("Перемещение macOS-версии")
                target_path = os.path.join(config.platform_dirs['MacOS'], 'FSA-DateStamp.app')
                if os.path.exists(target_path):
                    shutil.rmtree(target_path)
                shutil.copytree(app_path, target_path)
        else:  # Linux
            if os.path.exists(os.path.join(config.base_dir, 'dist', 'FSA-DateStamp')):
                print("Перемещение Linux-версии")
                shutil.move(
                    os.path.join(config.base_dir, 'dist', 'FSA-DateStamp'),
                    config.platform_dirs['Linux']
                )
            
        print_success("Сборка завершена успешно!")
        print("Результаты сборки находятся в:")
        if config.is_windows:
            print(f"- Windows: {config.platform_dirs['Windows']}")
        elif config.is_macos:
            print(f"- MacOS: {config.platform_dirs['MacOS']}")
        else:
            print(f"- Linux: {config.platform_dirs['Linux']}")
            
    except subprocess.CalledProcessError as e:
        print_error(f"Ошибка выполнения команды: {str(e)}")
        logger.error(f"Ошибка выполнения команды: {str(e)}")
        logger.error(f"Вывод: {e.stdout}\nОшибка: {e.stderr}")
    except Exception as e:
        print_error(f"Ошибка сборки: {str(e)}")
        logger.error(f"Ошибка сборки: {str(e)}")
        logger.error(traceback.format_exc())
    finally:
        # Очищаем временные файлы в любом случае
        if config:
            try:
                print_step("Очистка временных файлов")
                config.clean_temp_files()
                print_success("Временные файлы успешно удалены")
            except Exception as e:
                print_error(f"Ошибка при очистке временных файлов: {str(e)}")
                logger.error(f"Ошибка при очистке временных файлов: {str(e)}")
                logger.error(traceback.format_exc())

if __name__ == "__main__":
    build() 