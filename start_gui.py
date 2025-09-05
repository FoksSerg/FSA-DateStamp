#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FSA-DateStamp GUI Launcher
Запуск графического интерфейса для добавления водяных знаков
"""

import sys
import os

# Добавляем папку src в путь Python
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')

if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Импортируем и запускаем GUI
try:
    from DateStampGUI import main
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print(f"Пути Python: {sys.path}")
    print(f"Текущая директория: {os.getcwd()}")
    print(f"Путь к src: {src_dir}")
    print(f"Существует ли src: {os.path.exists(src_dir)}")
    if os.path.exists(src_dir):
        print(f"Содержимое src: {os.listdir(src_dir)}")
    sys.exit(1)

if __name__ == "__main__":
    main()
