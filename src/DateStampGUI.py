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
from DateStamp import process_images_with_structure

class DateStampGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FSA-DateStamp - Добавление водяных знаков")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
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
        
        # Главный фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="FSA-DateStamp", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
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
        self.font_size_scale = ttk.Scale(main_frame, from_=10, to=200, 
                                        variable=self.font_size_var, orient=tk.HORIZONTAL)
        self.font_size_scale.grid(row=5, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=5)
        self.font_size_label = ttk.Label(main_frame, text="60px")
        self.font_size_label.grid(row=5, column=2, pady=5)
        
        # Позиция штампа
        ttk.Label(main_frame, text="Позиция штампа:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.position_var = tk.StringVar()
        position_combo = ttk.Combobox(main_frame, textvariable=self.position_var, 
                                     values=['top-left', 'top-right', 'bottom-left', 'bottom-right', 
                                            'center', 'center-top', 'center-bottom'],
                                     state="readonly", width=20)
        position_combo.grid(row=6, column=1, sticky=tk.W, padx=(5, 5), pady=5)
        
        # Отступы
        ttk.Label(main_frame, text="Отступы (X, Y):").grid(row=7, column=0, sticky=tk.W, pady=5)
        
        # Отступ по X
        margin_frame = ttk.Frame(main_frame)
        margin_frame.grid(row=7, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=5)
        
        ttk.Label(margin_frame, text="X:").grid(row=0, column=0, padx=(0, 5))
        self.margin_x_var = tk.IntVar()
        self.margin_x_spin = ttk.Spinbox(margin_frame, from_=0, to=200, 
                                        textvariable=self.margin_x_var, width=8)
        self.margin_x_spin.grid(row=0, column=1, padx=(0, 10))
        
        ttk.Label(margin_frame, text="Y:").grid(row=0, column=2, padx=(0, 5))
        self.margin_y_var = tk.IntVar()
        self.margin_y_spin = ttk.Spinbox(margin_frame, from_=0, to=200, 
                                        textvariable=self.margin_y_var, width=8)
        self.margin_y_spin.grid(row=0, column=3)
        
        # Разделитель
        ttk.Separator(main_frame, orient='horizontal').grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)
        
        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=9, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="Обработать изображения", 
                  command=self.process_images, style="Accent.TButton").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Сохранить настройки", 
                  command=self.save_settings).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Выход", 
                  command=self.root.quit).pack(side=tk.LEFT)
        
        # Прогресс-бар
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=10, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Статус
        self.status_var = tk.StringVar(value="Готов к работе")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.grid(row=11, column=0, columnspan=3, pady=5)
        
        # Привязка событий
        self.font_size_scale.configure(command=self.update_font_size_label)
        
        # Сохраняем настройки при закрытии окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def update_font_size_label(self, value):
        """Обновление метки размера шрифта"""
        self.font_size_label.config(text=f"{int(float(value))}px")
    
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
                self.settings['position'] = section.get('position', 'center')
                self.settings['margin_x'] = section.getint('margin_x', 50)
                self.settings['margin_y'] = section.getint('margin_y', 30)
                self.settings['window_geometry'] = section.get('window_geometry', '600x500+100+100')
    
    def save_settings(self):
        """Сохранение настроек в файл"""
        # Сохраняем текущую геометрию окна
        self.settings['window_geometry'] = self.root.geometry()
        
        config = configparser.ConfigParser()
        config['Settings'] = {
            'input_folder': self.input_var.get(),
            'output_folder': self.output_var.get(),
            'font_size': str(self.font_size_var.get()),
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
        self.position_var.set(self.settings['position'])
        self.margin_x_var.set(self.settings['margin_x'])
        self.margin_y_var.set(self.settings['margin_y'])
        self.update_font_size_label(self.settings['font_size'])
        
        # Применяем геометрию окна
        self.root.geometry(self.settings['window_geometry'])
        
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
        
        try:
            # Запускаем прогресс-бар
            self.progress.start()
            self.status_var.set("Обработка изображений...")
            self.root.update()
            
            # Обрабатываем изображения
            process_images_with_structure(
                self.input_var.get(),
                self.output_var.get(),
                self.font_size_var.get(),
                self.position_var.get(),
                self.margin_x_var.get(),
                self.margin_y_var.get()
            )
            
            # Останавливаем прогресс-бар
            self.progress.stop()
            self.status_var.set("Обработка завершена успешно!")
            
            # Показываем сообщение об успехе
            messagebox.showinfo("Успех", "Изображения успешно обработаны!")
            
        except Exception as e:
            self.progress.stop()
            self.status_var.set("Ошибка при обработке!")
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
        
        finally:
            self.root.after(3000, lambda: self.status_var.set("Готов к работе"))
    
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
