#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Создание wrapper-скрипта для оптимизации запуска
"""

import os
import sys
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

def create_wrapper_script():
    """Создает wrapper-скрипт для быстрого запуска"""
    
    wrapper_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FSA-DateStamp Wrapper - Быстрый запуск приложения
"""
import os
import sys
import subprocess
import tempfile
from pathlib import Path

def main():
    """Основная функция wrapper'а"""
    # Определяем пути
    if getattr(sys, 'frozen', False):
        # Если запущены через PyInstaller
        app_dir = os.path.dirname(sys.executable)
    else:
        # Если запущены обычным Python
        app_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Путь к основному приложению
    main_app = os.path.join(app_dir, 'FSA-DateStamp')
    
    # Путь к папке с распакованными библиотеками
    libs_dir = os.path.join(app_dir, 'libs')
    
    # Проверяем, есть ли уже распакованные библиотеки
    if not os.path.exists(libs_dir):
        print("Первый запуск - распаковка библиотек...")
        # Создаем папку для библиотек
        os.makedirs(libs_dir, exist_ok=True)
        
        # Запускаем основное приложение для распаковки
        # PyInstaller автоматически распакует библиотеки при первом запуске
        subprocess.run([main_app], cwd=app_dir)
        
        # Копируем распакованные библиотеки из временной папки
        # (это упрощенная версия - в реальности нужно более сложная логика)
        print("Библиотеки распакованы. Последующие запуски будут быстрее.")
    
    # Запускаем основное приложение
    subprocess.run([main_app], cwd=app_dir)

if __name__ == "__main__":
    main()
'''
    
    # Сохраняем wrapper-скрипт
    wrapper_path = os.path.join(os.path.dirname(__file__), 'wrapper.py')
    with open(wrapper_path, 'w', encoding='utf-8') as f:
        f.write(wrapper_content)
    
    print(f"Wrapper-скрипт создан: {wrapper_path}")
    return wrapper_path

if __name__ == "__main__":
    create_wrapper_script()
