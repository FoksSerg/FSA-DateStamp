#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FSA-DateStamp GUI Launcher
Запуск графического интерфейса для добавления водяных знаков
"""

import sys
import os

# Определяем, запущены ли мы через PyInstaller
if getattr(sys, 'frozen', False):
    # Если запущены через PyInstaller, используем путь к исполняемому файлу
    application_path = os.path.dirname(sys.executable)
    src_path = os.path.join(application_path, 'src')
else:
    # Если запущены обычным Python, используем путь к скрипту
    src_path = os.path.join(os.path.dirname(__file__), 'src')

# Добавляем папку src в путь
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Импортируем и запускаем GUI
try:
    from DateStampGUI import main
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print(f"Пути Python: {sys.path}")
    print(f"Текущая директория: {os.getcwd()}")
    print(f"Путь к src: {src_path}")
    print(f"Существует ли src: {os.path.exists(src_path)}")
    if os.path.exists(src_path):
        print(f"Содержимое src: {os.listdir(src_path)}")
    sys.exit(1)

if __name__ == "__main__":
    main()
