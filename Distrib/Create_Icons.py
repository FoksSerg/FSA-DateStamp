#!/usr/bin/env python3
"""
Скрипт для создания иконок приложения для разных платформ
"""

import os
from PIL import Image

def create_icon(size=(256, 256), color=(34, 139, 34)):
    """Создание базового изображения иконки для FSA-DateStamp"""
    img = Image.new('RGB', size, color)
    
    # Добавляем простой текст "DS" белым цветом
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(img)
    
    # Рассчитываем размер шрифта как 40% от размера изображения
    font_size = int(min(size) * 0.4)
    try:
        font = ImageFont.truetype("Arial", font_size)
    except:
        font = ImageFont.load_default()
        
    text = "DS"
    # Получаем размеры текста
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Центрируем текст
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Рисуем текст
    draw.text((x, y), text, fill="white", font=font)
    
    return img

def create_windows_ico(img, output_path):
    """Создание .ico файла для Windows"""
    # Создаем набор изображений разных размеров
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    icons = []
    
    for size in sizes:
        icons.append(img.resize(size, Image.Resampling.LANCZOS))
        
    # Сохраняем как .ico
    icons[0].save(
        output_path,
        format='ICO',
        sizes=[(i.width, i.height) for i in icons],
        append_images=icons[1:]
    )

def create_macos_icns(img, output_path):
    """Создание .icns файла для macOS"""
    import tempfile
    import subprocess
    import platform
    
    if platform.system() != 'Darwin':
        print("ВНИМАНИЕ: Создание .icns возможно только на macOS!")
        return False
        
    try:
        subprocess.run(['which', 'iconutil'], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("ВНИМАНИЕ: Утилита iconutil не найдена!")
        return False
    
    with tempfile.TemporaryDirectory() as iconset:
        iconset_name = iconset + '.iconset'
        os.makedirs(iconset_name)
        
        # Создаем иконки разных размеров
        scales = [
            (16, '16x16'), (32, '16x16@2x'),
            (32, '32x32'), (64, '32x32@2x'),
            (128, '128x128'), (256, '128x128@2x'),
            (256, '256x256'), (512, '256x256@2x'),
            (512, '512x512'), (1024, '512x512@2x')
        ]
        
        for size, name in scales:
            resized = img.resize((size, size), Image.Resampling.LANCZOS)
            resized.save(os.path.join(iconset_name, f'icon_{name}.png'))
            
        # Конвертируем iconset в .icns
        subprocess.run(['iconutil', '-c', 'icns', iconset_name, '-o', output_path], check=True)
        return True

def create_linux_png(img, output_path):
    """Создание .png файла для Linux"""
    img.save(output_path, format='PNG')

def main():
    """Основная функция"""
    # Определяем директорию Icons
    icons_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Icons')
    if not os.path.exists(icons_dir):
        os.makedirs(icons_dir)
        
    # Создаем базовую иконку
    icon = create_icon(size=(1024, 1024))
    
    # Создаем иконки для разных платформ
    create_windows_ico(icon, os.path.join(icons_dir, 'app.ico'))
    if create_macos_icns(icon, os.path.join(icons_dir, 'app.icns')):
        print("macOS иконка создана успешно")
    create_linux_png(icon, os.path.join(icons_dir, 'app.png'))
    
    print(f"Иконки успешно созданы в директории {icons_dir}")

if __name__ == "__main__":
    main() 