#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TestFotoProcessor.py - Специальный процессор для работы с TestFotoInput/ и TestFotoStamp/
"""

import os
import sys
from DateStamp import process_images_with_structure

def process_test_foto():
    """Обработка папок TestFotoInput -> TestFotoStamp с сохранением структуры"""
    
    # Определяем пути относительно текущей папки
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    input_folder = os.path.join(project_root, "TestFotoInput")
    output_folder = os.path.join(project_root, "TestFotoStamp")
    
    print("=" * 60)
    print("FSA-DateStamp: Обработка TestFoto")
    print("=" * 60)
    print(f"Исходная папка: {input_folder}")
    print(f"Папка назначения: {output_folder}")
    print("=" * 60)
    
    # Проверяем существование исходной папки
    if not os.path.exists(input_folder):
        print(f"ОШИБКА: Папка '{input_folder}' не существует!")
        print("Создайте папку TestFotoInput в корне проекта и поместите туда изображения.")
        return False
    
    # Создаем папку назначения если не существует
    os.makedirs(output_folder, exist_ok=True)
    
    # Обрабатываем изображения с сохранением структуры
    try:
        process_images_with_structure(
            source_root=input_folder,
            dest_root=output_folder,
            font_size=35,
            position='bottom-right'
        )
        
        print("=" * 60)
        print("Обработка завершена успешно!")
        print(f"Результаты сохранены в: {output_folder}")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"ОШИБКА при обработке: {e}")
        return False

def main():
    """Главная функция"""
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("TestFotoProcessor - Обработка TestFotoInput -> TestFotoStamp")
        print("")
        print("Использование:")
        print("  python TestFotoProcessor.py")
        print("")
        print("Функции:")
        print("  - Обрабатывает все изображения из папки TestFotoInput/")
        print("  - Сохраняет результаты в TestFotoStamp/ с сохранением структуры папок")
        print("  - Сохраняет даты создания исходных файлов")
        print("  - Добавляет водяные знаки с датой и временем")
        return
    
    success = process_test_foto()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
