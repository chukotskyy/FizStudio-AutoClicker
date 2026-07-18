import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import threading
import win32api
import win32con
import keyboard
import json
import os

class AutoClicker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FizStudio AutoClicker")
        self.root.geometry("380x500")
        self.root.minsize(350, 450)
        self.root.attributes('-topmost', True)
        
        self.clicking = False
        self.click_thread = None
        self.target_x = None
        self.target_y = None
        self.click_count = 0
        self.current_theme = "dark"
        self.current_lang = "ru"
        
        # Тексты на разных языках
        self.texts = {
            "ru": {
                "brand": "AutoClicker",
                "by": "by FizStudio",
                "main_tab": "Главная",
                "settings_tab": "Настройки",
                "position": "📍 Позиция клика",
                "not_selected": "Не выбрана",
                "select_btn": "🎯 Выбрать точку",
                "select_hint": "Нажмите кнопку и кликните в нужном месте",
                "stats": "📊 Статистика",
                "clicks": "кликов",
                "clicks_per_sec": "кликов/сек",
                "start": "▶  СТАРТ",
                "stop": "⏹  СТОП",
                "cps_mode": "🎯 Клики в секунду",
                "cps": "CPS",
                "advanced_mode": "🔧 Продвинутые настройки",
                "delay": "Задержка",
                "sec": "сек",
                "spread_time": "Разброс времени",
                "spread_coord": "Разброс координат",
                "px": "px",
                "hotkeys": "⌨ Горячие клавиши",
                "start_stop_key": "Старт/Стоп:",
                "select_key_label": "Выбор точки:",
                "key_hint": "Нажмите на кнопку клавиши для изменения",
                "reset": "🔄 Сбросить настройки",
                "ready": "Готов к работе",
                "select_point_first": "❌ Сначала выберите точку для клика",
                "running": "🟢 Кликер запущен",
                "stopped": "⏸ Остановлен | Всего кликов: "
            },
            "en": {
                "brand": "AutoClicker",
                "by": "by FizStudio",
                "main_tab": "Main",
                "settings_tab": "Settings",
                "position": "📍 Click Position",
                "not_selected": "Not selected",
                "select_btn": "🎯 Select Point",
                "select_hint": "Click button and then click on screen",
                "stats": "📊 Statistics",
                "clicks": "clicks",
                "clicks_per_sec": "clicks/sec",
                "start": "▶  START",
                "stop": "⏹  STOP",
                "cps_mode": "🎯 Clicks Per Second",
                "cps": "CPS",
                "advanced_mode": "🔧 Advanced Settings",
                "delay": "Delay",
                "sec": "sec",
                "spread_time": "Time Spread",
                "spread_coord": "Coordinate Spread",
                "px": "px",
                "hotkeys": "⌨ Hotkeys",
                "start_stop_key": "Start/Stop:",
                "select_key_label": "Select Point:",
                "key_hint": "Click key button to change",
                "reset": "🔄 Reset Settings",
                "ready": "Ready",
                "select_point_first": "❌ Select click point first",
                "running": "🟢 Clicker running",
                "stopped": "⏸ Stopped | Total clicks: "
            }
        }
        
        # Цветовые схемы
        self.themes = {
            "dark": {
                'bg': '#1e1e1e',
                'frame_bg': '#2d2d2d',
                'text': '#ffffff',
                'subtext': '#888888',
                'accent': '#0078d4',
                'success': '#4caf50',
                'danger': '#f44336',
                'warning': '#ff9800'
            },
            "light": {
                'bg': '#ffffff',
                'frame_bg': '#f5f5f5',
                'text': '#1e1e1e',
                'subtext': '#666666',
                'accent': '#0078d4',
                'success': '#4caf50',
                'danger': '#f44336',
                'warning': '#ff9800'
            }
        }
        
        self.colors = self.themes[self.current_theme]
        
        self.config_file = "autoclicker_config.json"
        self.load_config()
        self.setup_styles()
        self.setup_ui()
    
    def load_config(self):
        default_config = {
            "start_key": "f6",
            "select_key": "f8",
            "delay": 0.1,
            "spread": 0.05,
            "coord_spread": 3,
            "cps": 10,
            "use_cps": True,
            "target_x": None,
            "target_y": None,
            "theme": "dark",
            "language": "ru"
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                for key in default_config:
                    if key in config:
                        default_config[key] = config[key]
            except:
                pass
        
        self.config = default_config
        self.target_x = self.config["target_x"]
        self.target_y = self.config["target_y"]
        self.current_theme = self.config.get("theme", "dark")
        self.current_lang = self.config.get("language", "ru")
        self.colors = self.themes[self.current_theme]
    
    def t(self, key):
        """Получить перевод"""
        return self.texts[self.current_lang].get(key, key)
    
    def save_config(self):
        if hasattr(self, 'delay_var'):
            self.config["delay"] = self.delay_var.get()
        if hasattr(self, 'spread_var'):
            self.config["spread"] = self.spread_var.get()
        if hasattr(self, 'coord_var'):
            self.config["coord_spread"] = self.coord_var.get()
        if hasattr(self, 'cps_var'):
            self.config["cps"] = self.cps_var.get()
        if hasattr(self, 'use_cps_var'):
            self.config["use_cps"] = self.use_cps_var.get()
        self.config["target_x"] = self.target_x
        self.config["target_y"] = self.target_y
        self.config["theme"] = self.current_theme
        self.config["language"] = self.current_lang
        
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TNotebook', background=self.colors['bg'], borderwidth=0)
        style.configure('TNotebook.Tab', background=self.colors['frame_bg'], 
                       foreground=self.colors['subtext'], padding=[20, 8],
                       font=('Segoe UI', 10))
        style.map('TNotebook.Tab', background=[('selected', self.colors['accent'])],
                 foreground=[('selected', self.colors['text'])])
        
        style.configure('TFrame', background=self.colors['bg'])
        style.configure('TLabelframe', background=self.colors['bg'], 
                       foreground=self.colors['text'])
        style.configure('TLabelframe.Label', background=self.colors['bg'], 
                       foreground=self.colors['text'], font=('Segoe UI', 9, 'bold'))
    
    def create_label(self, parent, text, font_size=10, color=None, bold=False, **kwargs):
        if color is None:
            color = self.colors['text']
        font_weight = 'bold' if bold else 'normal'
        return tk.Label(parent, text=text, font=('Segoe UI', font_size, font_weight),
                       fg=color, bg=self.colors['bg'], **kwargs)
    
    def create_button(self, parent, text, command, color=None, font_size=11, **kwargs):
        if color is None:
            color = self.colors['accent']
        return tk.Button(parent, text=text, command=command,
                        font=('Segoe UI', font_size, 'bold'),
                        bg=color, fg='white', relief='flat',
                        activebackground=color, activeforeground='white',
                        cursor='hand2', bd=0, padx=20, pady=8, **kwargs)
    
    def toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.colors = self.themes[self.current_theme]
        self.save_config()
        self.root.destroy()
        self.__init__()
        self.run()
    
    def toggle_language(self):
        self.current_lang = "en" if self.current_lang == "ru" else "ru"
        self.save_config()
        self.root.destroy()
        self.__init__()
        self.run()
    
    def setup_ui(self):
        self.root.configure(bg=self.colors['bg'])
        
        # Верхняя панель
        header = tk.Frame(self.root, bg=self.colors['bg'], height=50)
        header.pack(fill="x", pady=(15, 5))
        header.pack_propagate(False)
        
        # Левая часть - бренд
        left_header = tk.Frame(header, bg=self.colors['bg'])
        left_header.pack(side="left", padx=(20, 0))
        
        tk.Label(left_header, text="⚡", font=('Segoe UI', 16), bg=self.colors['bg'], 
                fg=self.colors['accent']).pack(side="left", padx=(0, 5))
        
        brand_frame = tk.Frame(left_header, bg=self.colors['bg'])
        brand_frame.pack(side="left")
        
        tk.Label(brand_frame, text=self.t("brand"), font=('Segoe UI', 16, 'bold'),
                bg=self.colors['bg'], fg=self.colors['text']).pack(anchor="w")
        tk.Label(brand_frame, text=self.t("by"), font=('Segoe UI', 9),
                bg=self.colors['bg'], fg=self.colors['subtext']).pack(anchor="w")
        
        # Правая часть - переключатели
        right_header = tk.Frame(header, bg=self.colors['bg'])
        right_header.pack(side="right", padx=20)
        
        # Переключатель темы
        theme_btn = tk.Button(right_header, text="🌙" if self.current_theme == "dark" else "☀️",
                            command=self.toggle_theme,
                            font=('Segoe UI', 14), bg=self.colors['bg'], 
                            fg=self.colors['text'], relief='flat',
                            cursor='hand2', bd=0, padx=5)
        theme_btn.pack(side="left", padx=2)
        
        # Переключатель языка с флагами
        flag_text = "🇷🇺" if self.current_lang == "ru" else "🇺🇸"
        lang_btn = tk.Button(right_header, text=flag_text,
                            command=self.toggle_language,
                            font=('Segoe UI', 14), bg=self.colors['bg'], 
                            fg=self.colors['text'], relief='flat',
                            cursor='hand2', bd=0, padx=5)
        lang_btn.pack(side="left", padx=2)
        
        # Создаем вкладки
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, padx=15, fill="both", expand=True)
        
        # Вкладка "Главная"
        self.main_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.main_frame, text=f"  {self.t('main_tab')}  ")
        self.setup_main_tab()
        
        # Вкладка "Настройки"
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text=f"  {self.t('settings_tab')}  ")
        self.setup_settings_tab()
        
        # Статус-бар
        self.status_bar = tk.Label(self.root, text=self.t("ready"), 
                                   font=('Segoe UI', 9), fg=self.colors['subtext'],
                                   bg=self.colors['frame_bg'], anchor="w", padx=15, pady=5)
        self.status_bar.pack(fill="x", side="bottom")
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind_hotkeys()
    
    def setup_main_tab(self):
        parent = self.main_frame
        
        # Позиция клика
        pos_frame = tk.LabelFrame(parent, text=self.t("position"), padx=15, pady=10,
                                  bg=self.colors['bg'], fg=self.colors['text'])
        pos_frame.pack(pady=10, padx=10, fill="x")
        
        if self.target_x is not None and self.target_y is not None:
            pos_text = f"X: {self.target_x}  |  Y: {self.target_y}"
            pos_color = self.colors['success']
        else:
            pos_text = self.t("not_selected")
            pos_color = self.colors['danger']
        
        self.pos_label = self.create_label(pos_frame, pos_text, font_size=12, 
                                          color=pos_color, bold=True)
        self.pos_label.pack(pady=5)
        
        self.select_btn = self.create_button(pos_frame, self.t("select_btn"), 
                                            self.start_position_selection,
                                            color=self.colors['accent'])
        self.select_btn.pack(pady=10)
        
        self.create_label(pos_frame, self.t("select_hint"),
                         font_size=9, color=self.colors['subtext']).pack()
        
        # Статистика
        stats_frame = tk.LabelFrame(parent, text=self.t("stats"), padx=15, pady=10,
                                    bg=self.colors['bg'], fg=self.colors['text'])
        stats_frame.pack(pady=10, padx=10, fill="x")
        
        stats_inner = tk.Frame(stats_frame, bg=self.colors['bg'])
        stats_inner.pack()
        
        self.counter_label = self.create_label(stats_inner, "0", font_size=32, 
                                              color=self.colors['accent'], bold=True)
        self.counter_label.pack()
        self.create_label(stats_inner, self.t("clicks"), font_size=10, 
                         color=self.colors['subtext']).pack()
        
        self.speed_label = self.create_label(stats_inner, f"0 {self.t('clicks_per_sec')}", 
                                            font_size=10, color=self.colors['subtext'])
        self.speed_label.pack(pady=(5, 0))
        
        # Кнопка Старт/Стоп
        self.start_btn = self.create_button(parent, self.t("start"), self.toggle_clicking,
                                           color=self.colors['success'], font_size=14,
                                           height=2)
        self.start_btn.pack(pady=15, padx=15, fill="x")
    
    def setup_settings_tab(self):
        parent = self.settings_frame
        
        # Режим CPS
        cps_frame = tk.LabelFrame(parent, text=self.t("cps_mode"), padx=15, pady=10,
                                  bg=self.colors['bg'], fg=self.colors['text'])
        cps_frame.pack(pady=10, padx=10, fill="x")
        
        # Переключатель режима CPS/Продвинутый
        mode_frame = tk.Frame(cps_frame, bg=self.colors['bg'])
        mode_frame.pack(fill="x", pady=5)
        
        self.use_cps_var = tk.BooleanVar(value=self.config.get("use_cps", True))
        
        cps_radio = tk.Radiobutton(mode_frame, text=f"CPS ({self.t('cps')})", 
                                   variable=self.use_cps_var, value=True,
                                   command=self.toggle_mode,
                                   bg=self.colors['bg'], fg=self.colors['text'],
                                   selectcolor=self.colors['bg'],
                                   activebackground=self.colors['bg'],
                                   activeforeground=self.colors['accent'],
                                   font=('Segoe UI', 10))
        cps_radio.pack(side="left", padx=5)
        
        advanced_radio = tk.Radiobutton(mode_frame, text=self.t("advanced_mode"), 
                                        variable=self.use_cps_var, value=False,
                                        command=self.toggle_mode,
                                        bg=self.colors['bg'], fg=self.colors['text'],
                                        selectcolor=self.colors['bg'],
                                        activebackground=self.colors['bg'],
                                        activeforeground=self.colors['accent'],
                                        font=('Segoe UI', 10))
        advanced_radio.pack(side="left", padx=5)
        
        # Слайдер CPS
        self.cps_container = tk.Frame(cps_frame, bg=self.colors['bg'])
        self.cps_container.pack(fill="x", pady=5)
        
        cps_slider_frame = tk.Frame(self.cps_container, bg=self.colors['bg'])
        cps_slider_frame.pack(fill="x")
        
        self.cps_var = tk.IntVar(value=self.config.get("cps", 10))
        self.cps_label = self.create_label(cps_slider_frame, 
                                          f"{self.config.get('cps', 10)} {self.t('cps')}", 
                                          font_size=11)
        self.cps_label.pack(side="right")
        
        self.cps_scale = tk.Scale(cps_slider_frame, from_=1, to=50, resolution=1,
                                 variable=self.cps_var, orient="horizontal",
                                 bg=self.colors['bg'], fg=self.colors['text'],
                                 highlightbackground=self.colors['bg'],
                                 troughcolor=self.colors['frame_bg'],
                                 activebackground=self.colors['accent'],
                                 length=200)
        self.cps_scale.pack(side="left", fill="x", expand=True)
        self.cps_scale.config(command=lambda v: self.cps_label.config(
            text=f"{int(float(v))} {self.t('cps')}"))
        
        # Продвинутые настройки (контейнер)
        self.advanced_container = tk.Frame(parent, bg=self.colors['bg'])
        
        # Продвинутые настройки
        self.advanced_frame = tk.LabelFrame(self.advanced_container, text=self.t("advanced_mode"), 
                                           padx=15, pady=10,
                                           bg=self.colors['bg'], fg=self.colors['text'])
        self.advanced_frame.pack(fill="x")
        
        # Задержка
        tk.Label(self.advanced_frame, text=self.t("delay"), 
                bg=self.colors['bg'], fg=self.colors['subtext'],
                font=('Segoe UI', 9)).pack(anchor="w", pady=(0, 5))
        
        delay_row = tk.Frame(self.advanced_frame, bg=self.colors['bg'])
        delay_row.pack(fill="x")
        
        self.delay_var = tk.DoubleVar(value=self.config["delay"])
        self.delay_label = self.create_label(delay_row, 
                                            f"{self.config['delay']:.2f} {self.t('sec')}", 
                                            font_size=11)
        self.delay_label.pack(side="right")
        
        self.delay_scale = tk.Scale(delay_row, from_=0.01, to=2.0, resolution=0.01,
                                  variable=self.delay_var, orient="horizontal",
                                  bg=self.colors['bg'], fg=self.colors['text'],
                                  highlightbackground=self.colors['bg'],
                                  troughcolor=self.colors['frame_bg'],
                                  activebackground=self.colors['accent'],
                                  length=200)
        self.delay_scale.pack(side="left", fill="x", expand=True)
        self.delay_scale.config(command=lambda v: self.delay_label.config(
            text=f"{float(v):.2f} {self.t('sec')}"))
        
        # Разброс времени
        tk.Label(self.advanced_frame, text=self.t("spread_time"), 
                bg=self.colors['bg'], fg=self.colors['subtext'],
                font=('Segoe UI', 9)).pack(anchor="w", pady=(10, 5))
        
        spread_slider_row = tk.Frame(self.advanced_frame, bg=self.colors['bg'])
        spread_slider_row.pack(fill="x")
        
        self.spread_var = tk.DoubleVar(value=self.config["spread"])
        self.spread_label = self.create_label(spread_slider_row, 
                                             f"±{self.config['spread']:.2f} {self.t('sec')}", 
                                             font_size=11)
        self.spread_label.pack(side="right")
        
        self.spread_scale = tk.Scale(spread_slider_row, from_=0, to=1.0, resolution=0.01,
                                   variable=self.spread_var, orient="horizontal",
                                   bg=self.colors['bg'], fg=self.colors['text'],
                                   highlightbackground=self.colors['bg'],
                                   troughcolor=self.colors['frame_bg'],
                                   activebackground=self.colors['accent'],
                                   length=200)
        self.spread_scale.pack(side="left", fill="x", expand=True)
        self.spread_scale.config(command=lambda v: self.spread_label.config(
            text=f"±{float(v):.2f} {self.t('sec')}"))
        
        # Разброс координат
        tk.Label(self.advanced_frame, text=self.t("spread_coord"), 
                bg=self.colors['bg'], fg=self.colors['subtext'],
                font=('Segoe UI', 9)).pack(anchor="w", pady=(10, 5))
        
        coord_slider_row = tk.Frame(self.advanced_frame, bg=self.colors['bg'])
        coord_slider_row.pack(fill="x")
        
        self.coord_var = tk.IntVar(value=self.config["coord_spread"])
        self.coord_label = self.create_label(coord_slider_row, 
                                            f"±{self.config['coord_spread']} {self.t('px')}", 
                                            font_size=11)
        self.coord_label.pack(side="right")
        
        self.coord_scale = tk.Scale(coord_slider_row, from_=0, to=50, resolution=1,
                                  variable=self.coord_var, orient="horizontal",
                                  bg=self.colors['bg'], fg=self.colors['text'],
                                  highlightbackground=self.colors['bg'],
                                  troughcolor=self.colors['frame_bg'],
                                  activebackground=self.colors['accent'],
                                  length=200)
        self.coord_scale.pack(side="left", fill="x", expand=True)
        self.coord_scale.config(command=lambda v: self.coord_label.config(
            text=f"±{int(float(v))} {self.t('px')}"))
        
        # Горячие клавиши
        self.hotkey_frame = tk.LabelFrame(parent, text=self.t("hotkeys"), padx=15, pady=10,
                                     bg=self.colors['bg'], fg=self.colors['text'])
        self.hotkey_frame.pack(pady=10, padx=10, fill="x")
        
        hotkey_row1 = tk.Frame(self.hotkey_frame, bg=self.colors['bg'])
        hotkey_row1.pack(fill="x", pady=5)
        
        self.create_label(hotkey_row1, self.t("start_stop_key"), font_size=10, 
                         color=self.colors['subtext']).pack(side="left")
        
        self.start_key_var = tk.StringVar(value=self.config["start_key"].upper())
        start_key_btn = tk.Button(hotkey_row1, textvariable=self.start_key_var,
                                 command=lambda: self.change_key("start"),
                                 font=('Segoe UI', 10, 'bold'),
                                 bg=self.colors['frame_bg'], fg=self.colors['text'],
                                 relief='flat', cursor='hand2', width=8)
        start_key_btn.pack(side="right")
        
        hotkey_row2 = tk.Frame(self.hotkey_frame, bg=self.colors['bg'])
        hotkey_row2.pack(fill="x", pady=5)
        
        self.create_label(hotkey_row2, self.t("select_key_label"), font_size=10, 
                         color=self.colors['subtext']).pack(side="left")
        
        self.select_key_var = tk.StringVar(value=self.config["select_key"].upper())
        select_key_btn = tk.Button(hotkey_row2, textvariable=self.select_key_var,
                                  command=lambda: self.change_key("select"),
                                  font=('Segoe UI', 10, 'bold'),
                                  bg=self.colors['frame_bg'], fg=self.colors['text'],
                                  relief='flat', cursor='hand2', width=8)
        select_key_btn.pack(side="right")
        
        self.create_label(self.hotkey_frame, self.t("key_hint"),
                         font_size=8, color=self.colors['subtext']).pack(pady=(5,0))
        
        # Кнопка сброса
        reset_btn = self.create_button(parent, self.t("reset"), 
                                      self.reset_settings,
                                      color=self.colors['frame_bg'])
        reset_btn.pack(pady=15)
        
        # Применяем начальное состояние режима
        self.toggle_mode()
    
    def toggle_mode(self):
        """Переключение между режимом CPS и продвинутыми настройками"""
        if self.use_cps_var.get():
            # Режим CPS - скрываем продвинутые настройки
            self.advanced_container.pack_forget()
        else:
            # Продвинутый режим - показываем перед горячими клавишами
            self.advanced_container.pack(pady=10, padx=10, fill="x", before=self.hotkey_frame)
    
    def change_key(self, key_type):
        dialog = tk.Toplevel(self.root)
        dialog.title("Новая клавиша" if self.current_lang == "ru" else "New Key")
        dialog.geometry("300x150")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 300) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 150) // 2
        dialog.geometry(f"+{x}+{y}")
        
        self.create_label(dialog, 
                         "Нажмите нужную клавишу..." if self.current_lang == "ru" else "Press a key...", 
                         font_size=12).pack(pady=20)
        key_label = self.create_label(dialog, "", font_size=24, 
                                     color=self.colors['accent'], bold=True)
        key_label.pack()
        
        def on_key(event):
            key_name = event.keysym
            if not key_name or key_name == '??':
                return
            
            key_name = key_name.lower()
            
            if key_type == "start":
                if key_name == self.select_key_var.get().lower():
                    messagebox.showwarning(
                        "Конфликт" if self.current_lang == "ru" else "Conflict", 
                        "Эта клавиша уже используется для выбора точки!" if self.current_lang == "ru" else "This key is already used for point selection!")
                    return
                self.config["start_key"] = key_name
                self.start_key_var.set(key_name.upper())
            else:
                if key_name == self.start_key_var.get().lower():
                    messagebox.showwarning(
                        "Конфликт" if self.current_lang == "ru" else "Conflict", 
                        "Эта клавиша уже используется для старта!" if self.current_lang == "ru" else "This key is already used for start!")
                    return
                self.config["select_key"] = key_name
                self.select_key_var.set(key_name.upper())
            
            self.bind_hotkeys()
            dialog.destroy()
        
        dialog.bind('<KeyRelease>', on_key)
        dialog.focus_set()
    
    def bind_hotkeys(self):
        try:
            keyboard.unhook_all()
        except:
            pass
        
        try:
            keyboard.add_hotkey(self.config["start_key"], self.toggle_clicking)
            keyboard.add_hotkey(self.config["select_key"], self.start_position_selection)
        except Exception as e:
            print(f"Ошибка привязки клавиш: {e}")
    
    def reset_settings(self):
        if messagebox.askyesno(
            "Сброс" if self.current_lang == "ru" else "Reset", 
            "Сбросить все настройки?" if self.current_lang == "ru" else "Reset all settings?"):
            
            self.config["delay"] = 0.1
            self.config["spread"] = 0.05
            self.config["coord_spread"] = 3
            self.config["cps"] = 10
            self.config["use_cps"] = True
            
            self.delay_var.set(0.1)
            self.spread_var.set(0.05)
            self.coord_var.set(3)
            self.cps_var.set(10)
            self.use_cps_var.set(True)
            
            self.toggle_mode()
            self.save_config()
            self.update_status("Настройки сброшены" if self.current_lang == "ru" else "Settings reset")
    
    def click_at(self, x, y):
        current_x, current_y = win32api.GetCursorPos()
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        win32api.SetCursorPos((current_x, current_y))
    
    def start_position_selection(self):
        if self.clicking:
            self.toggle_clicking()
        
        self.root.iconify()
        time.sleep(0.3)
        
        select_window = tk.Toplevel(self.root)
        select_window.attributes('-fullscreen', True)
        select_window.attributes('-alpha', 0.4)
        select_window.configure(bg='black')
        
        canvas = tk.Canvas(select_window, bg='black', highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        select_text = "🎯 Кликните в нужном месте\n\nEsc - отмена" if self.current_lang == "ru" else "🎯 Click on the target\n\nEsc - cancel"
        canvas.create_text(select_window.winfo_screenwidth()//2, 
                          select_window.winfo_screenheight()//2 - 50,
                          text=select_text,
                          font=('Segoe UI', 18, 'bold'), fill='white', 
                          justify="center")
        
        def on_click(event):
            self.target_x = event.x_root
            self.target_y = event.y_root
            self.pos_label.config(text=f"X: {self.target_x}  |  Y: {self.target_y}",
                                 fg=self.colors['success'])
            self.save_config()
            select_window.destroy()
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            self.update_status(f"Точка выбрана: X={self.target_x}, Y={self.target_y}" if self.current_lang == "ru" else f"Point selected: X={self.target_x}, Y={self.target_y}")
        
        def on_escape(event):
            select_window.destroy()
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
        
        select_window.bind('<Button-1>', on_click)
        select_window.bind('<Escape>', on_escape)
        select_window.focus_set()
    
    def toggle_clicking(self):
        if self.target_x is None or self.target_y is None:
            self.update_status(self.t("select_point_first"))
            return
        
        self.clicking = not self.clicking
        
        if self.clicking:
            self.start_btn.config(text=self.t("stop"), bg=self.colors['danger'],
                                 activebackground=self.colors['danger'])
            self.select_btn.config(state="disabled", bg=self.colors['frame_bg'])
            self.click_count = 0
            self.update_status(self.t("running"))
            self.click_thread = threading.Thread(target=self.click_loop, daemon=True)
            self.click_thread.start()
        else:
            self.stop_clicking()
    
    def stop_clicking(self):
        self.clicking = False
        self.start_btn.config(text=self.t("start"), bg=self.colors['success'],
                             activebackground=self.colors['success'])
        self.select_btn.config(state="normal", bg=self.colors['accent'])
        self.update_status(f"{self.t('stopped')}{self.click_count}")
    
    def click_loop(self):
        last_time = time.time()
        clicks_in_second = 0
        
        while self.clicking:
            spread = self.coord_var.get()
            x = self.target_x + random.randint(-spread, spread)
            y = self.target_y + random.randint(-spread, spread)
            
            self.click_at(x, y)
            self.click_count += 1
            clicks_in_second += 1
            
            self.root.after(0, lambda: self.counter_label.config(text=str(self.click_count)))
            
            current_time = time.time()
            if current_time - last_time >= 1.0:
                speed = clicks_in_second / (current_time - last_time)
                self.root.after(0, lambda s=speed: self.speed_label.config(
                    text=f"{s:.1f} {self.t('clicks_per_sec')}"))
                clicks_in_second = 0
                last_time = current_time
            
            if self.use_cps_var.get():
                cps = self.cps_var.get()
                base_delay = 1.0 / cps
                delay_spread = base_delay * 0.1
                actual_delay = base_delay + random.uniform(-delay_spread, delay_spread)
            else:
                delay = self.delay_var.get()
                delay_spread = self.spread_var.get()
                actual_delay = delay + random.uniform(-delay_spread, delay_spread)
            
            actual_delay = max(0.01, actual_delay)
            time.sleep(actual_delay)
    
    def update_status(self, message):
        self.status_bar.config(text=message)
    
    def run(self):
        self.root.mainloop()
    
    def on_closing(self):
        self.clicking = False
        self.save_config()
        try:
            keyboard.unhook_all()
        except:
            pass
        self.root.destroy()

if __name__ == "__main__":
    app = AutoClicker()
    app.run()