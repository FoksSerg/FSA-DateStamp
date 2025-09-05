#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FSA-DateStamp GUI Launcher
Запуск графического интерфейса для добавления водяных знаков
"""

import sys
import os

# Добавляем папку src в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Импортируем и запускаем GUI
from DateStampGUI import main

if __name__ == "__main__":
    main()
