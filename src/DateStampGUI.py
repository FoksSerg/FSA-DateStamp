#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FSA-DateStamp GUI - Графический интерфейс для добавления водяных знаков
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import configparser
from DateStamp import process_images_with_structure, get_available_fonts, create_stamp_preview

class DateStampGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FSA-DateStamp - Добавление водяных знаков")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        self.root.minsize(600, 500)  # Минимальный размер окна
        
        # Инициализируем переменные для всплывающей подсказки и управления процессом
        self.tooltip = None
        self.is_processing = False
        self.is_paused = False
        self.should_cancel = False
        self.processed_count = 0
        self.total_count = 0
        self.original_log_text = ""  # Сохраняем оригинальный текст лога
        
        # Определяем путь к файлу настроек рядом с исполняемым файлом
        if getattr(sys, 'frozen', False):
            # Если запущены через PyInstaller
            self.config_file = os.path.join(os.path.dirname(sys.executable), 'datestamp_settings.ini')
        else:
            # Если запущены обычным Python
            self.config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'datestamp_settings.ini')
        
        # Настройки по умолчанию
        self.settings = {
            'input_folder': '',
            'output_folder': '',
            'font_size': 60,
            'font_name': 'Встроенный (по умолчанию)',
            'position': 'center',
            'margin_x': 50,
            'margin_y': 30,
            'window_geometry': '600x500+100+100'
        }
        
        # Загружаем настройки
        self.load_settings()
        
        # Создаем интерфейс
        self.create_widgets()
        
        # Применяем загруженные настройки
        self.apply_settings()
    
    def create_widgets(self):
        """Создание элементов интерфейса"""
        
        # Создаем главный фрейм с вкладками
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Создаем вкладку настроек
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text="Настройки")
        
        # Создаем вкладку лога
        self.log_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.log_frame, text="Лог работы")
        
        # Создаем главный фрейм для настроек
        main_frame = ttk.Frame(self.settings_frame, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Настройка растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Заголовок с количеством изображений
        self.title_label = ttk.Label(main_frame, text="Найдено 0 изображений для обработки", 
                                    font=("Arial", 14, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Выбор исходной папки
        ttk.Label(main_frame, text="Исходная папка:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.input_var = tk.StringVar()
        self.input_entry = ttk.Entry(main_frame, textvariable=self.input_var, width=50)
        self.input_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=5)
        ttk.Button(main_frame, text="Обзор...", command=self.browse_input_folder).grid(row=1, column=2, pady=5)
        
        # Выбор финальной папки
        ttk.Label(main_frame, text="Папка результатов:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.output_var = tk.StringVar()
        self.output_entry = ttk.Entry(main_frame, textvariable=self.output_var, width=50)
        self.output_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=5)
        ttk.Button(main_frame, text="Обзор...", command=self.browse_output_folder).grid(row=2, column=2, pady=5)
        
        # Разделитель
        ttk.Separator(main_frame, orient='horizontal').grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)
        
        # Настройки штампа
        settings_label = ttk.Label(main_frame, text="Настройки штампа", 
                                  font=("Arial", 12, "bold"))
        settings_label.grid(row=4, column=0, columnspan=3, pady=(0, 10))
        
        # Размер шрифта
        ttk.Label(main_frame, text="Размер шрифта:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.font_size_var = tk.IntVar()
        self.font_size_scale = ttk.Scale(main_frame, from_=10, to=100, 
                                        variable=self.font_size_var, orient=tk.HORIZONTAL)
        self.font_size_scale.grid(row=5, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=5)
        self.font_size_label = ttk.Label(main_frame, text="60px")
        self.font_size_label.grid(row=5, column=2, pady=5)
        
        # Выбор шрифта
        ttk.Label(main_frame, text="Шрифт:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.font_name_var = tk.StringVar()
        self.font_combo = ttk.Combobox(main_frame, textvariable=self.font_name_var, 
                                      state="readonly", width=30)
        self.font_combo.grid(row=6, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=5)
        
        # Загружаем доступные шрифты
        self.load_available_fonts()
        
        # Предварительный просмотр штампа
        preview_label_text = ttk.Label(main_frame, text="Предварительный просмотр:")
        preview_label_text.grid(row=7, column=0, sticky=tk.W, pady=5)
        
        # Создаем фрейм для предварительного просмотра
        preview_frame = ttk.Frame(main_frame, relief="sunken", borderwidth=2)
        preview_frame.grid(row=7, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=5)
        
        # Создаем виджет для отображения изображения
        self.preview_label = ttk.Label(preview_frame)
        self.preview_label.pack(padx=5, pady=5)
        
        # Привязываем обработчик клика мыши для выбора позиции
        self.preview_label.bind("<Button-1>", self.on_preview_click)
        
        # Привязываем всплывающую подсказку при наведении
        self.preview_label.bind("<Enter>", self.show_tooltip)
        self.preview_label.bind("<Leave>", self.hide_tooltip)
        
        # Позиция и отступы на одной строке
        position_offset_frame = ttk.Frame(main_frame)
        position_offset_frame.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Позиция штампа
        ttk.Label(position_offset_frame, text="Позиция:").pack(side=tk.LEFT, padx=(0, 5))
        self.position_var = tk.StringVar()
        position_combo = ttk.Combobox(position_offset_frame, textvariable=self.position_var, 
                                     values=['top-left', 'top-right', 'bottom-left', 'bottom-right', 
                                            'center', 'center-top', 'center-bottom'],
                                     state="readonly", width=12)
        position_combo.pack(side=tk.LEFT, padx=(0, 20))
        
        # Отступы
        ttk.Label(position_offset_frame, text="Отступы:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Label(position_offset_frame, text="X:").pack(side=tk.LEFT, padx=(0, 2))
        self.margin_x_var = tk.IntVar()
        self.margin_x_spin = ttk.Spinbox(position_offset_frame, from_=0, to=100, 
                                        textvariable=self.margin_x_var, width=8)
        self.margin_x_spin.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(position_offset_frame, text="Y:").pack(side=tk.LEFT, padx=(0, 2))
        self.margin_y_var = tk.IntVar()
        self.margin_y_spin = ttk.Spinbox(position_offset_frame, from_=0, to=100, 
                                        textvariable=self.margin_y_var, width=8)
        self.margin_y_spin.pack(side=tk.LEFT)
        
        # Разделитель
        ttk.Separator(main_frame, orient='horizontal').grid(row=9, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)
        
        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=10, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="Обработать изображения", 
                  command=self.process_images, style="Accent.TButton").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Сохранить настройки", 
                  command=self.save_settings).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Выход", 
                  command=self.root.quit).pack(side=tk.LEFT)
        
        # Статус
        self.status_var = tk.StringVar(value="Готов к работе")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.grid(row=11, column=0, columnspan=3, pady=5)
        
        # Привязка событий
        self.font_size_scale.configure(command=self.update_font_size_label)
        
        # Привязка событий для обновления предварительного просмотра
        self.font_name_var.trace('w', lambda *args: self.update_preview())
        self.position_var.trace('w', lambda *args: self.update_preview())
        self.margin_x_var.trace('w', lambda *args: self.update_preview())
        self.margin_y_var.trace('w', lambda *args: self.update_preview())
        
        # Создаем предварительный просмотр после инициализации всех переменных
        self.update_preview()
        
        # Создаем лог работы
        self.create_log_widgets()
        
        # Создаем статус-бар
        self.status_var = tk.StringVar()
        self.status_var.set("Готов к работе")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Сохраняем настройки при закрытии окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_log_widgets(self):
        """Создание элементов лога работы"""
        # Заголовок лога
        ttk.Label(self.log_frame, text="Лог обработки изображений", font=("TkDefaultFont", 12, "bold")).pack(pady=10)
        
        # Текстовое поле для лога
        log_frame = ttk.Frame(self.log_frame)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Создаем Text виджет с прокруткой
        self.log_text = tk.Text(log_frame, height=20, width=80, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Фрейм для кнопок управления процессом
        control_frame = ttk.Frame(self.log_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Счетчик изображений
        self.count_label = ttk.Label(control_frame, text="Найдено изображений: 0")
        self.count_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Прогресс-бар
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(control_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 20))
        
        # Кнопки управления
        self.pause_button = ttk.Button(control_frame, text="Пауза", command=self.toggle_pause, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.cancel_button = ttk.Button(control_frame, text="Отмена", command=self.cancel_processing, state=tk.DISABLED)
        self.cancel_button.pack(side=tk.LEFT)
        
        # Фрейм для фильтрации логов
        filter_frame = ttk.Frame(self.log_frame)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Фильтр лога:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.log_filter_var = tk.StringVar(value="Все")
        self.log_filter_combo = ttk.Combobox(filter_frame, textvariable=self.log_filter_var, 
                                           values=["Все", "Обработано", "Пропущено", "Ошибки"], 
                                           state="readonly", width=15)
        self.log_filter_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.log_filter_combo.bind("<<ComboboxSelected>>", self.filter_log)
        
        ttk.Button(filter_frame, text="Очистить лог", command=self.clear_log).pack(side=tk.LEFT)
        
        # Обновляем счетчик при изменении папки
        self.input_var.trace('w', lambda *args: self.update_image_count())
    
    def load_available_fonts(self):
        """Загрузка доступных шрифтов в выпадающий список"""
        try:
            available_fonts = get_available_fonts()
            font_names = [name for name, path in available_fonts]
            self.font_combo['values'] = font_names
            if font_names:
                self.font_combo.set(font_names[0])  # Устанавливаем первый шрифт по умолчанию
        except Exception as e:
            print(f"Ошибка загрузки шрифтов: {e}")
            # Fallback на встроенный шрифт
            self.font_combo['values'] = ["Встроенный (по умолчанию)"]
            self.font_combo.set("Встроенный (по умолчанию)")

    def update_font_size_label(self, value):
        """Обновление метки размера шрифта"""
        self.font_size_label.config(text=f"{int(float(value))}px")
        # Обновляем предварительный просмотр при изменении размера шрифта
        self.update_preview()
    
    def on_preview_click(self, event):
        """Обработчик клика мыши на предварительном просмотре"""
        try:
            # Получаем размеры виджета предварительного просмотра
            widget_width = self.preview_label.winfo_width()
            widget_height = self.preview_label.winfo_height()
            
            if widget_width <= 0 or widget_height <= 0:
                return  # Виджет еще не отрисован
            
            # Координаты клика относительно виджета
            click_x = event.x
            click_y = event.y
            
            # Определяем позицию на основе координат клика
            # Разделяем область на 9 зон (3x3)
            zone_width = widget_width // 3
            zone_height = widget_height // 3
            
            # Определяем зону клика
            zone_x = click_x // zone_width
            zone_y = click_y // zone_height
            
            # Ограничиваем зоны (0, 1, 2)
            zone_x = min(2, max(0, zone_x))
            zone_y = min(2, max(0, zone_y))
            
            # Маппинг зон на позиции
            position_map = [
                ['top-left', 'center-top', 'top-right'],
                ['center-left', 'center', 'center-right'],
                ['bottom-left', 'center-bottom', 'bottom-right']
            ]
            
            new_position = position_map[zone_y][zone_x]
            
            # Обновляем выбранную позицию
            self.position_var.set(new_position)
            
            # Обновляем предварительный просмотр
            self.update_preview()
            
            self.log_message(f"Выбрана позиция: {new_position}")
            
        except Exception as e:
            print(f"Ошибка обработки клика: {e}")
    
    def show_tooltip(self, event):
        """Показать всплывающую подсказку"""
        try:
            # Создаем всплывающее окно
            self.tooltip = tk.Toplevel(self.root)
            self.tooltip.wm_overrideredirect(True)  # Убираем рамку окна
            self.tooltip.wm_attributes("-topmost", True)  # Поверх всех окон
            
            # Получаем координаты мыши
            x = self.root.winfo_pointerx() + 10
            y = self.root.winfo_pointery() + 10
            
            # Создаем виджет с текстом подсказки
            tooltip_label = tk.Label(self.tooltip, text="💡 Кликните для выбора позиции", 
                                   bg="yellow", fg="black", font=("TkDefaultFont", 9),
                                   padx=8, pady=4, relief="solid", borderwidth=1)
            tooltip_label.pack()
            
            # Размещаем подсказку
            self.tooltip.wm_geometry(f"+{x}+{y}")
            
            # Автоматически скрываем через 3 секунды
            self.root.after(3000, self.hide_tooltip)
            
        except Exception as e:
            print(f"Ошибка показа подсказки: {e}")
    
    def hide_tooltip(self, event=None):
        """Скрыть всплывающую подсказку"""
        try:
            if hasattr(self, 'tooltip') and self.tooltip:
                self.tooltip.destroy()
                self.tooltip = None
        except Exception as e:
            print(f"Ошибка скрытия подсказки: {e}")
    
    def log_message(self, message):
        """Добавление сообщения в лог"""
        try:
            from datetime import datetime
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_entry = f"[{timestamp}] {message}\n"
            
            # Добавляем в оригинальный текст
            self.original_log_text += log_entry
            
            # Если фильтр не активен, добавляем в отображение
            if hasattr(self, 'log_filter_var') and self.log_filter_var.get() == "Все":
                self.log_text.insert(tk.END, log_entry)
                self.log_text.see(tk.END)  # Прокрутка к концу
            elif hasattr(self, 'log_filter_var'):
                # Применяем текущий фильтр
                self._apply_filter()
            else:
                # Если фильтр еще не инициализирован, просто добавляем
                self.log_text.insert(tk.END, log_entry)
                self.log_text.see(tk.END)
            
            self.root.update_idletasks()  # Обновление интерфейса
            
        except Exception as e:
            print(f"Ошибка записи в лог: {e}")
    
    def update_image_count(self):
        """Обновление счетчика изображений"""
        try:
            input_folder = self.input_var.get()
            if input_folder and os.path.exists(input_folder):
                count = self.count_images(input_folder)
                self.total_count = count
                self.count_label.config(text=f"Найдено изображений: {count}")
                self.title_label.config(text=f"Найдено {count} изображений для обработки")
                self.log_message(f"Найдено {count} изображений для обработки")
            else:
                self.total_count = 0
                self.count_label.config(text="Найдено изображений: 0")
                self.title_label.config(text="Найдено 0 изображений для обработки")
        except Exception as e:
            self.log_message(f"Ошибка подсчета изображений: {e}")
            self.title_label.config(text="Ошибка подсчета изображений")
    
    def count_images(self, folder_path):
        """Подсчет количества изображений в папке"""
        count = 0
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif'}
        
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if os.path.splitext(file.lower())[1] in image_extensions:
                    count += 1
        return count
    
    def toggle_pause(self):
        """Переключение паузы/продолжения"""
        if self.is_paused:
            self.is_paused = False
            self.pause_button.config(text="Пауза")
            self.log_message("Обработка продолжена")
        else:
            self.is_paused = True
            self.pause_button.config(text="Продолжить")
            self.log_message("Обработка приостановлена")
    
    def cancel_processing(self):
        """Отмена обработки"""
        self.should_cancel = True
        self.log_message("Запрошена отмена обработки...")
        self.pause_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.DISABLED)
    
    def update_preview(self):
        """Обновление предварительного просмотра штампа"""
        try:
            # Проверяем, что все необходимые переменные инициализированы
            if not hasattr(self, 'font_size_var') or not hasattr(self, 'position_var'):
                return
            
            # Создаем предварительный просмотр
            preview_img = create_stamp_preview(
                font_size=self.font_size_var.get(),
                font_name=self.font_name_var.get() if hasattr(self, 'font_name_var') else 'Встроенный (по умолчанию)',
                position=self.position_var.get(),
                margin_x=self.margin_x_var.get() if hasattr(self, 'margin_x_var') else 50,
                margin_y=self.margin_y_var.get() if hasattr(self, 'margin_y_var') else 30
            )
            
            # Конвертируем PIL изображение в PhotoImage для tkinter
            from PIL import ImageTk
            photo = ImageTk.PhotoImage(preview_img)
            
            # Обновляем виджет
            self.preview_label.config(image=photo)
            self.preview_label.image = photo  # Сохраняем ссылку, чтобы изображение не удалилось
            
        except Exception as e:
            print(f"Ошибка обновления предварительного просмотра: {e}")
            # Показываем сообщение об ошибке
            if hasattr(self, 'preview_label'):
                self.preview_label.config(text="Ошибка предварительного просмотра", image="")
    
    def browse_input_folder(self):
        """Выбор исходной папки"""
        # Определяем начальную папку
        initial_dir = self.input_var.get() if self.input_var.get() and os.path.exists(self.input_var.get()) else os.path.expanduser("~")
        
        folder = filedialog.askdirectory(
            title="Выберите папку с исходными изображениями",
            initialdir=initial_dir
        )
        if folder:
            self.input_var.set(folder)
    
    def browse_output_folder(self):
        """Выбор папки результатов"""
        # Определяем начальную папку
        initial_dir = self.output_var.get() if self.output_var.get() and os.path.exists(self.output_var.get()) else os.path.expanduser("~")
        
        folder = filedialog.askdirectory(
            title="Выберите папку для сохранения результатов",
            initialdir=initial_dir
        )
        if folder:
            self.output_var.set(folder)
    
    def load_settings(self):
        """Загрузка настроек из файла"""
        if os.path.exists(self.config_file):
            config = configparser.ConfigParser()
            config.read(self.config_file, encoding='utf-8')
            
            if 'Settings' in config:
                section = config['Settings']
                self.settings['input_folder'] = section.get('input_folder', '')
                self.settings['output_folder'] = section.get('output_folder', '')
                self.settings['font_size'] = section.getint('font_size', 60)
                self.settings['font_name'] = section.get('font_name', 'Встроенный (по умолчанию)')
                self.settings['position'] = section.get('position', 'center')
                self.settings['margin_x'] = section.getint('margin_x', 50)
                self.settings['margin_y'] = section.getint('margin_y', 30)
                self.settings['window_geometry'] = section.get('window_geometry', '800x700+100+100')
                
                # Применяем геометрию окна сразу после загрузки
                self.root.geometry(self.settings['window_geometry'])
    
    def save_settings(self):
        """Сохранение настроек в файл"""
        # Сохраняем текущую геометрию окна
        self.settings['window_geometry'] = self.root.geometry()
        
        config = configparser.ConfigParser()
        config['Settings'] = {
            'input_folder': self.input_var.get(),
            'output_folder': self.output_var.get(),
            'font_size': str(self.font_size_var.get()),
            'font_name': self.font_name_var.get(),
            'position': self.position_var.get(),
            'margin_x': str(self.margin_x_var.get()),
            'margin_y': str(self.margin_y_var.get()),
            'window_geometry': self.settings['window_geometry']
        }
        
        # Создаем директорию если не существует
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            config.write(f)
        
        self.status_var.set("Настройки сохранены!")
        self.root.after(2000, lambda: self.status_var.set("Готов к работе"))
    
    def apply_settings(self):
        """Применение загруженных настроек"""
        self.input_var.set(self.settings['input_folder'])
        self.output_var.set(self.settings['output_folder'])
        self.font_size_var.set(self.settings['font_size'])
        self.font_name_var.set(self.settings['font_name'])
        self.position_var.set(self.settings['position'])
        self.margin_x_var.set(self.settings['margin_x'])
        self.margin_y_var.set(self.settings['margin_y'])
        self.update_font_size_label(self.settings['font_size'])
        
        # Включаем режим "поверх всех окон" на 3 секунды при запуске
        self.root.attributes('-topmost', True)
        # Отключаем режим "поверх всех окон" через 3 секунды
        self.root.after(3000, lambda: self.root.attributes('-topmost', False))
    
    def process_images(self):
        """Обработка изображений"""
        # Проверка входных данных
        if not self.input_var.get():
            messagebox.showerror("Ошибка", "Выберите исходную папку!")
            return
        
        if not self.output_var.get():
            messagebox.showerror("Ошибка", "Выберите папку результатов!")
            return
        
        if not os.path.exists(self.input_var.get()):
            messagebox.showerror("Ошибка", "Исходная папка не существует!")
            return
        
        # Создаем папку результатов если не существует
        os.makedirs(self.output_var.get(), exist_ok=True)
        
        # Инициализируем процесс
        self.is_processing = True
        self.is_paused = False
        self.should_cancel = False
        self.processed_count = 0
        
        # Активируем кнопки управления
        self.pause_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.NORMAL)
        
        # Переключаемся на вкладку лога
        self.notebook.select(1)
        
        # Запускаем обработку в отдельном потоке
        import threading
        self.processing_thread = threading.Thread(target=self._process_images_thread)
        self.processing_thread.daemon = True
        self.processing_thread.start()
    
    def _process_images_thread(self):
        """Поток обработки изображений"""
        try:
            self.log_message("Начало обработки изображений")
            self.status_var.set("Обработка изображений...")
            
            # Получаем список всех изображений
            image_files = self._get_image_files(self.input_var.get())
            total_files = len(image_files)
            
            if total_files == 0:
                self.log_message("Изображения не найдены")
                self._finish_processing(0, "Изображения не найдены")
                return
            
            self.log_message(f"Найдено {total_files} изображений для обработки")
            
            # Обрабатываем каждое изображение
            skipped_count = 0
            for i, image_path in enumerate(image_files):
                # Проверяем флаги управления
                while self.is_paused and not self.should_cancel:
                    self.root.after(100, lambda: None)  # Небольшая пауза
                
                if self.should_cancel:
                    self.log_message("Обработка отменена пользователем")
                    break
                
                try:
                    # Обрабатываем изображение
                    success = self._process_single_image(image_path)
                    
                    if success:
                        self.processed_count += 1
                        filename = os.path.basename(image_path)
                        self.log_message(f"Обработано: {filename} ({self.processed_count}/{total_files})")
                    else:
                        skipped_count += 1
                    
                    # Обновляем прогресс
                    progress = ((i + 1) / total_files) * 100
                    self.progress_var.set(progress)
                    
                except Exception as e:
                    filename = os.path.basename(image_path)
                    self.log_message(f"Ошибка обработки {filename}: {str(e)}")
                    skipped_count += 1
            
            # Завершаем обработку
            if self.should_cancel:
                self.log_message("Обработка отменена")
                self._finish_processing(self.processed_count, "Обработка отменена")
            else:
                self.log_message(f"Обработка завершена. Обработано: {self.processed_count}, пропущено: {skipped_count} из {total_files}")
                self._finish_processing(self.processed_count, f"Обработано {self.processed_count}, пропущено {skipped_count}")
                
        except Exception as e:
            self.log_message(f"Критическая ошибка: {str(e)}")
            self._finish_processing(0, f"Ошибка: {str(e)}")
    
    def _get_image_files(self, folder_path):
        """Получение списка всех изображений в папке"""
        image_files = []
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif'}
        
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if os.path.splitext(file.lower())[1] in image_extensions:
                    image_files.append(os.path.join(root, file))
        
        return image_files
    
    def _process_single_image(self, image_path):
        """Обработка одного изображения"""
        from DateStamp import add_datetime_watermark, get_datetime_from_exif, get_datetime_from_filename
        
        # Получаем дату и время из EXIF или имени файла
        datetime_obj = get_datetime_from_exif(image_path)
        if datetime_obj is None:
            datetime_obj = get_datetime_from_filename(os.path.basename(image_path))
        
        # Если не удалось получить дату/время, пропускаем изображение
        if datetime_obj is None:
            filename = os.path.basename(image_path)
            self.log_message(f"ПРОПУЩЕНО: {filename} - не удалось определить дату/время")
            return False
        
        # Определяем относительный путь для сохранения структуры
        rel_path = os.path.relpath(image_path, self.input_var.get())
        output_path = os.path.join(self.output_var.get(), rel_path)
        
        # Создаем папку назначения если не существует
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Добавляем водяной знак
        add_datetime_watermark(
            input_path=image_path,
            output_path=output_path,
            datetime_obj=datetime_obj,
            font_size=self.font_size_var.get(),
            font_name=self.font_name_var.get(),
            position=self.position_var.get(),
            margin_x=self.margin_x_var.get(),
            margin_y=self.margin_y_var.get()
        )
        return True
    
    def _finish_processing(self, processed_count, message):
        """Завершение обработки"""
        self.is_processing = False
        self.is_paused = False
        self.should_cancel = False
        
        # Деактивируем кнопки управления
        self.pause_button.config(state=tk.DISABLED, text="Пауза")
        self.cancel_button.config(state=tk.DISABLED)
        
        # Обновляем статус
        self.status_var.set(message)
        self.root.after(3000, lambda: self.status_var.set("Готов к работе"))
        
        # Сбрасываем прогресс
        self.progress_var.set(0)
    
    def filter_log(self, event=None):
        """Фильтрация лога по типу сообщений"""
        try:
            self._apply_filter()
        except Exception as e:
            print(f"Ошибка фильтрации лога: {e}")
    
    def _apply_filter(self):
        """Применение фильтра к логу"""
        try:
            filter_type = self.log_filter_var.get()
            
            # Получаем строки из оригинального текста
            lines = self.original_log_text.split('\n')
            
            # Фильтруем строки
            if filter_type == "Все":
                filtered_lines = lines
            elif filter_type == "Обработано":
                filtered_lines = [line for line in lines if "Обработано:" in line]
            elif filter_type == "Пропущено":
                filtered_lines = [line for line in lines if "ПРОПУЩЕНО:" in line]
            elif filter_type == "Ошибки":
                filtered_lines = [line for line in lines if "Ошибка" in line or "ошибка" in line]
            else:
                filtered_lines = lines
            
            # Очищаем и заполняем отфильтрованным текстом
            self.log_text.delete("1.0", tk.END)
            filtered_text = '\n'.join(filtered_lines)
            self.log_text.insert("1.0", filtered_text)
            
        except Exception as e:
            print(f"Ошибка применения фильтра: {e}")
    
    def clear_log(self):
        """Очистка лога"""
        try:
            self.log_text.delete("1.0", tk.END)
            self.original_log_text = ""
            self.log_message("Лог очищен")
        except Exception as e:
            print(f"Ошибка очистки лога: {e}")
    
    def on_closing(self):
        """Обработчик закрытия окна"""
        # Сохраняем настройки перед закрытием
        self.save_settings()
        self.root.destroy()

def main():
    """Главная функция"""
    root = tk.Tk()
    
    # Настройка стиля
    style = ttk.Style()
    style.theme_use('clam')
    
    # Создание приложения
    app = DateStampGUI(root)
    
    # Запуск главного цикла
    root.mainloop()

if __name__ == "__main__":
    main()
