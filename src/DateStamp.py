import os
import cv2
import argparse
import shutil
import stat
import platform
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import exifread
import piexif

def get_available_fonts():
    """Получение списка доступных шрифтов для текущей платформы"""
    system = platform.system()
    available_fonts = []
    
    if system == "Windows":
        # Windows шрифты
        font_candidates = [
            ("Arial", "C:/Windows/Fonts/arial.ttf"),
            ("Arial Bold", "C:/Windows/Fonts/arialbd.ttf"),
            ("Calibri", "C:/Windows/Fonts/calibri.ttf"),
            ("Calibri Bold", "C:/Windows/Fonts/calibrib.ttf"),
            ("Verdana", "C:/Windows/Fonts/verdana.ttf"),
            ("Verdana Bold", "C:/Windows/Fonts/verdanab.ttf"),
            ("Tahoma", "C:/Windows/Fonts/tahoma.ttf"),
            ("Tahoma Bold", "C:/Windows/Fonts/tahomabd.ttf"),
            ("Times New Roman", "C:/Windows/Fonts/times.ttf"),
            ("Times New Roman Bold", "C:/Windows/Fonts/timesbd.ttf"),
            ("Courier New", "C:/Windows/Fonts/cour.ttf"),
            ("Courier New Bold", "C:/Windows/Fonts/courbd.ttf")
        ]
    elif system == "Darwin":  # macOS
        # macOS шрифты
        font_candidates = [
            ("Arial", "/System/Library/Fonts/Arial.ttf"),
            ("Arial Bold", "/System/Library/Fonts/Arial Bold.ttf"),
            ("Helvetica", "/System/Library/Fonts/Helvetica.ttc"),
            ("Helvetica Bold", "/System/Library/Fonts/Helvetica Bold.ttf"),
            ("SF Pro Display", "/System/Library/Fonts/SF-Pro-Display-Regular.otf"),
            ("SF Pro Display Bold", "/System/Library/Fonts/SF-Pro-Display-Bold.otf"),
            ("Times", "/System/Library/Fonts/Times.ttc"),
            ("Times Bold", "/System/Library/Fonts/Times Bold.ttf"),
            ("Courier", "/System/Library/Fonts/Courier.ttc"),
            ("Courier Bold", "/System/Library/Fonts/Courier Bold.ttf")
        ]
    elif system == "Linux":
        # Linux шрифты
        font_candidates = [
            ("DejaVu Sans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
            ("DejaVu Sans Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
            ("Liberation Sans", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"),
            ("Liberation Sans Bold", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"),
            ("Ubuntu", "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf"),
            ("Ubuntu Bold", "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf")
        ]
    
    # Проверяем доступность шрифтов
    for font_name, font_path in font_candidates:
        if os.path.exists(font_path):
            available_fonts.append((font_name, font_path))
    
    # Добавляем встроенный шрифт как fallback
    available_fonts.append(("Встроенный (по умолчанию)", "default"))
    
    return available_fonts

def get_system_font(font_size, font_name=None):
    """Получение системного шрифта для текущей платформы"""
    if font_name is None or font_name == "Встроенный (по умолчанию)":
        # Используем старую логику для обратной совместимости
        system = platform.system()
        font_paths = []
        
        if system == "Windows":
            font_paths = [
                "C:/Windows/Fonts/arial.ttf",
                "C:/Windows/Fonts/calibri.ttf", 
                "C:/Windows/Fonts/calibrib.ttf",
                "C:/Windows/Fonts/verdana.ttf",
                "C:/Windows/Fonts/tahoma.ttf"
            ]
        elif system == "Darwin":
            font_paths = [
                "/System/Library/Fonts/Arial.ttf",
                "/System/Library/Fonts/Helvetica.ttc",
                "/System/Library/Fonts/SF-Pro-Display-Regular.otf",
                "/Library/Fonts/Arial.ttf"
            ]
        elif system == "Linux":
            font_paths = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                "/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf"
            ]
        
        for font_path in font_paths:
            try:
                if os.path.exists(font_path):
                    return ImageFont.truetype(font_path, font_size)
            except Exception:
                continue
        
        return ImageFont.load_default()
    
    # Ищем выбранный шрифт
    available_fonts = get_available_fonts()
    for name, path in available_fonts:
        if name == font_name:
            if path == "default":
                return ImageFont.load_default()
            try:
                return ImageFont.truetype(path, font_size)
            except Exception:
                continue
    
    # Fallback на встроенный шрифт
    return ImageFont.load_default()

def create_stamp_preview(font_size=60, font_name=None, position='center', margin_x=50, margin_y=30, 
                        text_color=(255, 255, 255), background_color=(0, 0, 0, 150), 
                        preview_width=400, preview_height=200):
    """Создание предварительного просмотра штампа с фиксированным размером поля"""
    from datetime import datetime
    
    # Получаем текущую дату и время
    current_time = datetime.now()
    dt_string = current_time.strftime('%Y-%m-%d %H:%M:%S')
    
    # Создаем изображение для предварительного просмотра с фиксированным размером
    preview_img = Image.new('RGB', (preview_width, preview_height), color=(240, 240, 240))
    draw = ImageDraw.Draw(preview_img, 'RGBA')
    
    # Вычисляем масштабированный размер шрифта для предварительного просмотра
    # Используем пропорцию 1:3 для более реалистичного отображения
    # Для фрейма 400x200px и максимального шрифта 100px: 100/3 ≈ 33px
    preview_font_size = max(8, font_size // 3)  # Минимум 8px для читаемости
    
    # Получаем шрифт с масштабированным размером
    font = get_system_font(preview_font_size, font_name)
    
    # Получаем размеры текста
    bbox = draw.textbbox((0, 0), dt_string, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Масштабируем отступы пропорционально размеру шрифта (1:3)
    preview_margin_x = max(2, margin_x // 3)
    preview_margin_y = max(2, margin_y // 3)
    
    # Определяем позицию текста
    if position == 'top-left':
        x, y = preview_margin_x, preview_margin_y
    elif position == 'top-right':
        x, y = preview_width - text_width - preview_margin_x, preview_margin_y
    elif position == 'bottom-left':
        x, y = preview_margin_x, preview_height - text_height - preview_margin_y
    elif position == 'center':
        x, y = (preview_width - text_width) // 2, (preview_height - text_height) // 2
    elif position == 'center-top':
        x, y = (preview_width - text_width) // 2, preview_margin_y
    elif position == 'center-bottom':
        x, y = (preview_width - text_width) // 2, preview_height - text_height - preview_margin_y
    else:  # bottom-right (по умолчанию)
        x, y = preview_width - text_width - preview_margin_x, preview_height - text_height - preview_margin_y
    
    # Рисуем полупрозрачный фон
    padding = max(2, 10 // 3)  # Масштабируем padding
    frame_y_offset = preview_font_size // 4  # Оптимальное соотношение 1/4
    draw.rectangle([x - padding, y - padding + frame_y_offset, 
                   x + text_width + padding, y + text_height + padding + frame_y_offset],
                  fill=background_color)
    
    # Рисуем текст
    draw.text((x, y), dt_string, font=font, fill=text_color)
    
    # Рисуем сетку зон для интерактивности (тонкие линии)
    grid_color = (200, 200, 200, 100)  # Светло-серый полупрозрачный
    
    # Вертикальные линии
    for i in range(1, 3):
        x_line = (preview_width * i) // 3
        draw.line([(x_line, 0), (x_line, preview_height)], fill=grid_color, width=1)
    
    # Горизонтальные линии
    for i in range(1, 3):
        y_line = (preview_height * i) // 3
        draw.line([(0, y_line), (preview_width, y_line)], fill=grid_color, width=1)
    
    return preview_img

def get_datetime_from_exif(image_path):
    """Получение даты и времени из EXIF данных"""
    try:
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f)
            if 'EXIF DateTimeOriginal' in tags:
                dt_str = str(tags['EXIF DateTimeOriginal'])
                return datetime.strptime(dt_str, '%Y:%m:%d %H:%M:%S')
    except:
        pass
    return None

def get_datetime_from_filename(filename):
    """Извлечение даты и времени из имени файла"""
    try:
        # Попробуем разные форматы имен файлoв
        base_name = os.path.splitext(filename)[0]
        
        # Формат: IMG_20230101_123456.jpg
        if base_name.startswith('IMG_') and len(base_name) >= 15:
            date_part = base_name[4:12]  # 20230101
            time_part = base_name[13:19]  # 123456
            dt_str = f"{date_part[:4]}:{date_part[4:6]}:{date_part[6:8]} {time_part[:2]}:{time_part[2:4]}:{time_part[4:6]}"
            return datetime.strptime(dt_str, '%Y:%m:%d %H:%M:%S')
        
        # Формат: 20230101_123456.jpg (только если начинается с цифр)
        if len(base_name) >= 15 and base_name[8] == '_' and base_name[:8].isdigit():
            date_part = base_name[:8]  # 20230101
            time_part = base_name[9:15]  # 123456
            dt_str = f"{date_part[:4]}:{date_part[4:6]}:{date_part[6:8]} {time_part[:2]}:{time_part[2:4]}:{time_part[4:6]}"
            return datetime.strptime(dt_str, '%Y:%m:%d %H:%M:%S')
        
        # Универсальный поиск паттерна даты в любом имени файла
        import re
        
        # Паттерн 1: camera13_DD-MM-YYYY_HHhMMmSSs (например: camera13_01-01-2024_22h16m08s163ms.jpg)
        pattern1 = r'camera\d+_(\d{1,2})-(\d{1,2})-(\d{4})_(\d{1,2})h(\d{1,2})m(\d{1,2})s'
        match1 = re.search(pattern1, base_name)
        if match1:
            day, month, year, hour, minute, second = match1.groups()
            date_str = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            time_str = f"{hour.zfill(2)}:{minute.zfill(2)}:{second.zfill(2)}"
            dt_str = f"{date_str} {time_str}"
            return datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
        
        
        # Паттерн 2: DD-MM-YYYY_HHhMMmSSs (например: Главная дорога_01-12-2024_08h36m46s683ms.jpg)
        pattern2 = r'(\d{1,2})-(\d{1,2})-(\d{4})_(\d{1,2})h(\d{1,2})m(\d{1,2})s'
        match2 = re.search(pattern2, base_name)
        if match2:
            day, month, year, hour, minute, second = match2.groups()
            date_str = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            time_str = f"{hour.zfill(2)}:{minute.zfill(2)}:{second.zfill(2)}"
            dt_str = f"{date_str} {time_str}"
            return datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
        
        # Паттерн 3: camera13_YYYY-Mon-DD_HH_MM_SS_ms (например: camera13_2023-Nov-21_13_36_19_680.jpg)
        pattern3 = r'camera\d+_(\d{4})-([A-Za-z]{3})-(\d{1,2})_(\d{1,2})_(\d{1,2})_(\d{1,2})_(\d{1,3})'
        match3 = re.search(pattern3, base_name)
        if match3:
            year, month_abbr, day, hour, minute, second, millisecond = match3.groups()
            # Словарь сокращений месяцев
            month_abbr_to_num = {
                'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
                'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
            }
            if month_abbr in month_abbr_to_num:
                date_str = f"{year}-{month_abbr_to_num[month_abbr]}-{day.zfill(2)}"
                time_str = f"{hour.zfill(2)}:{minute.zfill(2)}:{second.zfill(2)}"
                dt_str = f"{date_str} {time_str}"
                return datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
        
        # Паттерн 4: camera13_YYYY-ПолноеМесяц-DD_HH_MM_SS_ms (например: camera13_2023-Ноябрь-21_13_36_19_680.jpg)
        pattern4 = r'camera\d+_(\d{4})-([А-Яа-я]+)-(\d{1,2})_(\d{1,2})_(\d{1,2})_(\d{1,2})_(\d{1,3})'
        match4 = re.search(pattern4, base_name)
        if match4:
            year, month_ru, day, hour, minute, second, millisecond = match4.groups()
            # Словарь русских названий месяцев
            month_ru_to_num = {
                'Январь': '01', 'Февраль': '02', 'Март': '03', 'Апрель': '04', 'Май': '05', 'Июнь': '06',
                'Июль': '07', 'Август': '08', 'Сентябрь': '09', 'Октябрь': '10', 'Ноябрь': '11', 'Декабрь': '12'
            }
            if month_ru in month_ru_to_num:
                date_str = f"{year}-{month_ru_to_num[month_ru]}-{day.zfill(2)}"
                time_str = f"{hour.zfill(2)}:{minute.zfill(2)}:{second.zfill(2)}"
                dt_str = f"{date_str} {time_str}"
                return datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
        
        # Паттерн 5: camera13_YYYY-ПолноеМесяцEn-DD_HH_MM_SS_ms (например: camera13_2023-November-21_13_36_19_680.jpg)
        pattern5 = r'camera\d+_(\d{4})-([A-Za-z]+)-(\d{1,2})_(\d{1,2})_(\d{1,2})_(\d{1,2})_(\d{1,3})'
        match5 = re.search(pattern5, base_name)
        if match5:
            year, month_en, day, hour, minute, second, millisecond = match5.groups()
            # Словарь полных английских названий месяцев
            month_en_to_num = {
                'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06',
                'July': '07', 'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12'
            }
            if month_en in month_en_to_num:
                date_str = f"{year}-{month_en_to_num[month_en]}-{day.zfill(2)}"
                time_str = f"{hour.zfill(2)}:{minute.zfill(2)}:{second.zfill(2)}"
                dt_str = f"{date_str} {time_str}"
                return datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
            
    except Exception as e:
        print(f"Ошибка парсинга даты из имени файла '{filename}': {e}")
        pass
    return None

def get_file_creation_time(image_path):
    """Получение времени создания файла"""
    try:
        timestamp = os.path.getctime(image_path)
        return datetime.fromtimestamp(timestamp)
    except:
        return None

def preserve_file_metadata(source_path, dest_path):
    """Сохранение метаданных файла (дата создания, модификации, права доступа)"""
    try:
        # Получаем метаданные исходного файла
        stat_info = os.stat(source_path)
        
        # Устанавливаем время модификации и доступа
        os.utime(dest_path, (stat_info.st_atime, stat_info.st_mtime))
        
        # Попытка установить время создания через системную команду (только для macOS/Linux)
        import platform
        if platform.system() in ['Darwin', 'Linux']:  # macOS или Linux
            try:
                import subprocess
                # Форматируем время создания для команды touch
                creation_time = stat_info.st_birthtime
                formatted_time = datetime.fromtimestamp(creation_time).strftime('%Y%m%d%H%M.%S')
                
                # Выполняем команду touch для установки времени создания
                result = subprocess.run(['touch', '-t', formatted_time, dest_path], 
                                      check=True, capture_output=True, text=True)
                
            except (subprocess.CalledProcessError, FileNotFoundError, OSError) as e:
                print(f"Предупреждение: touch не сработал для {os.path.basename(dest_path)}: {e}")
                # Альтернативный способ - копируем файл с сохранением метаданных
                try:
                    import shutil
                    shutil.copystat(source_path, dest_path)
                except Exception as e2:
                    print(f"Предупреждение: copystat не сработал: {e2}")
        else:
            # Для Windows используем только стандартные методы Python
            try:
                import shutil
                shutil.copystat(source_path, dest_path)
            except Exception as e:
                print(f"Предупреждение: не удалось сохранить метаданные: {e}")
        
        # Устанавливаем права доступа (только если возможно)
        try:
            os.chmod(dest_path, stat_info.st_mode)
        except (OSError, PermissionError):
            pass  # Игнорируем ошибки прав доступа
            
    except (OSError, AttributeError) as e:
        print(f"Предупреждение: не удалось сохранить метаданные для {dest_path}: {e}")
        pass  # Игнорируем ошибки метаданных

def add_datetime_watermark(input_path, output_path, datetime_obj, font_size=30, 
                          position='bottom-right', opacity=0.7, text_color=(255, 255, 255),
                          background_color=(0, 0, 0, 150), margin_x=10, margin_y=10, font_name=None):
    """Добавление водяного знака с датой и временем"""
    
    # Открываем изображение напрямую
    if input_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        image = Image.open(input_path)
    else:
        # Для других форматов используем OpenCV
        img_cv = cv2.imread(input_path)
        image = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
    
    # Форматируем дату и время
    dt_string = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
    
    # Создаем объект для рисования
    draw = ImageDraw.Draw(image, 'RGBA')
    
    # Используем кроссплатформенную функцию выбора шрифта
    font = get_system_font(font_size, font_name)
    
    # Получаем размеры текста
    bbox = draw.textbbox((0, 0), dt_string, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Определяем позицию текста
    img_width, img_height = image.size
    
    if position == 'top-left':
        x, y = margin_x, margin_y
    elif position == 'top-right':
        x, y = img_width - text_width - margin_x, margin_y
    elif position == 'bottom-left':
        x, y = margin_x, img_height - text_height - margin_y
    elif position == 'center':
        x, y = (img_width - text_width) // 2, (img_height - text_height) // 2
    elif position == 'center-top':
        x, y = (img_width - text_width) // 2, margin_y
    elif position == 'center-bottom':
        x, y = (img_width - text_width) // 2, img_height - text_height - margin_y
    else:  # bottom-right (по умолчанию)
        x, y = img_width - text_width - margin_x, img_height - text_height - margin_y
    
    # Рисуем полупрозрачный фон
    padding = 10
    # Смещаем рамку вниз относительно текста - размер смещения пропорционален размеру шрифта
    frame_y_offset = font_size // 4  # 1/4 от размера шрифта для оптимального смещения
    draw.rectangle([x - padding, y - padding + frame_y_offset, 
                   x + text_width + padding, y + text_height + padding + frame_y_offset],
                  fill=background_color)
    
    # Рисуем текст
    draw.text((x, y), dt_string, font=font, fill=text_color)
    
    # Сохраняем изображение
    if output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
        image.save(output_path, 'JPEG', quality=95)
    else:
        image.save(output_path)
    
    # Сохраняем метаданные исходного файла
    preserve_file_metadata(input_path, output_path)

def process_images(input_folder, output_folder=None, overwrite=False, 
                  font_size=30, position='bottom-right'):
    """Обработка всех изображений в папке"""
    
    if output_folder is None:
        output_folder = input_folder
    elif not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif')
    
    processed_count = 0
    error_count = 0
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(supported_formats):
            input_path = os.path.join(input_folder, filename)
            
            if overwrite:
                output_path = input_path
            else:
                output_filename = f"watermarked_{filename}"
                output_path = os.path.join(output_folder, output_filename)
            
            # Получаем дату и время разными способами
            datetime_obj = None
            
            # 1. Пробуем получить из EXIF
            datetime_obj = get_datetime_from_exif(input_path)
            
            # 2. Если нет в EXIF, пробуем из имени файла
            if datetime_obj is None:
                datetime_obj = get_datetime_from_filename(filename)
            
            # 3. Если все еще нет, используем время создания файла
            if datetime_obj is None:
                datetime_obj = get_file_creation_time(input_path)
            
            if datetime_obj:
                try:
                    add_datetime_watermark(input_path, output_path, datetime_obj, 
                                          font_size, position)
                    print(f"Обработан: {filename} -> {datetime_obj}")
                    processed_count += 1
                except Exception as e:
                    print(f"Ошибка при обработке {filename}: {e}")
                    error_count += 1
            else:
                print(f"Не удалось определить дату для: {filename}")
                error_count += 1
    
    print(f"\nОбработка завершена!")
    print(f"Успешно: {processed_count}")
    print(f"С ошибками: {error_count}")

def process_images_with_structure(source_root, dest_root, font_size=30, position='bottom-right', margin_x=10, margin_y=10, font_name=None):
    """Обработка изображений с сохранением структуры папок"""
    
    if not os.path.exists(source_root):
        print(f"Ошибка: Исходная папка '{source_root}' не существует!")
        return
    
    # Создаем только корневую папку назначения
    os.makedirs(dest_root, exist_ok=True)
    
    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif')
    processed_count = 0
    error_count = 0
    
    # Рекурсивно обходим все папки
    for root, dirs, files in os.walk(source_root):
        # Вычисляем относительный путь от исходной папки
        rel_path = os.path.relpath(root, source_root)
        if rel_path == '.':
            dest_folder = dest_root
        else:
            dest_folder = os.path.join(dest_root, rel_path)
        
        # Обрабатываем файлы в текущей папке
        for filename in files:
            if filename.lower().endswith(supported_formats):
                source_path = os.path.join(root, filename)
                dest_path = os.path.join(dest_folder, filename)
                
                # Создаем папку назначения только при необходимости
                os.makedirs(dest_folder, exist_ok=True)
                
                # Получаем дату и время разными способами
                datetime_obj = None
                date_source = ""
                
                # 1. Пробуем получить из имени файла (ПРИОРИТЕТ)
                datetime_obj = get_datetime_from_filename(filename)
                if datetime_obj:
                    date_source = "имя файла"
                    print(f"  📅 Дата из имени файла: {datetime_obj}")
                
                # 2. Если нет в имени файла, пробуем из EXIF
                if datetime_obj is None:
                    datetime_obj = get_datetime_from_exif(source_path)
                    if datetime_obj:
                        date_source = "EXIF"
                        print(f"  📅 Дата из EXIF: {datetime_obj}")
                
                # 3. Если все еще нет, используем время создания файла
                if datetime_obj is None:
                    datetime_obj = get_file_creation_time(source_path)
                    if datetime_obj:
                        date_source = "время создания файла"
                        print(f"  📅 Дата из времени создания: {datetime_obj}")
                
                # Выводим информацию о том, какая дата будет использована
                if datetime_obj:
                    print(f"  ✅ Используется дата: {datetime_obj} (источник: {date_source})")
                else:
                    print(f"  ❌ Не удалось определить дату для файла")
                
                if datetime_obj:
                    try:
                        add_datetime_watermark(source_path, dest_path, datetime_obj, 
                                              font_size, position, margin_x=margin_x, margin_y=margin_y, font_name=font_name)
                        
                        # Выводим параметры штампа
                        print(f"  🎨 Параметры штампа: шрифт={font_size}px, позиция={position}, отступы={margin_x}x{margin_y}px")
                        print(f"Обработан: {os.path.join(rel_path, filename)} -> {datetime_obj} ({date_source})")
                        processed_count += 1
                    except Exception as e:
                        print(f"Ошибка при обработке {os.path.join(rel_path, filename)}: {e}")
                        error_count += 1
                else:
                    print(f"Не удалось определить дату для: {os.path.join(rel_path, filename)}")
                    error_count += 1
    
    print(f"\nОбработка с сохранением структуры завершена!")
    print(f"Успешно: {processed_count}")
    print(f"С ошибками: {error_count}")

def main():
    parser = argparse.ArgumentParser(description='Добавление меток даты и времени на снимки')
    parser.add_argument('input_folder', help='Папка с исходными изображениями')
    parser.add_argument('-o', '--output', help='Папка для сохранения результатов')
    parser.add_argument('--overwrite', action='store_true', 
                       help='Перезаписывать исходные файлы')
    parser.add_argument('--preserve-structure', action='store_true',
                       help='Сохранять структуру папок и метаданные файлов')
    parser.add_argument('--font-size', type=int, default=30, 
                       help='Размер шрифта (по умолчанию: 30)')
    parser.add_argument('--position', choices=['top-left', 'top-right', 
                                              'bottom-left', 'bottom-right', 'center',
                                              'center-top', 'center-bottom'],
                       default='bottom-right', 
                       help='Позиция водяного знака')
    parser.add_argument('--margin-x', type=int, default=10,
                       help='Отступ от краев по горизонтали (по умолчанию: 10)')
    parser.add_argument('--margin-y', type=int, default=10,
                       help='Отступ от краев по вертикали (по умолчанию: 10)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_folder):
        print(f"Ошибка: Папка '{args.input_folder}' не существует!")
        return
    
    if args.preserve_structure:
        if not args.output:
            print("Ошибка: Для режима сохранения структуры необходимо указать папку вывода (-o)")
            return
        process_images_with_structure(args.input_folder, args.output, 
                                    args.font_size, args.position, args.margin_x, args.margin_y)
    else:
        process_images(args.input_folder, args.output, args.overwrite, 
                      args.font_size, args.position)

if __name__ == "__main__":
    main()