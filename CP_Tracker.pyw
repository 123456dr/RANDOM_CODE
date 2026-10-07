import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta

DB_FILE = 'cp_tracker.db'

class CPTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CP & CTF Tracker")
        
        try:
            import os
            if os.name == 'nt':
                import ctypes
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("my_cp_tracker_app")
            
            self.icon_image = tk.PhotoImage(file='./AWARD/mess/CheckIn_py/rc_icon.png')
            self.root.iconphoto(False, self.icon_image)
        except Exception as e:
            pass

        window_width = 460 
        window_height = 320 
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = screen_width - window_width - 10
        y = screen_height - window_height - 80 
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.plat_map = {'C++': 'cpp', '課業': 'school', '資安': 'sec', '專案': 'project'}
        
        self.init_db()
        
        self.timer_running = False
        self.total_seconds = 10800
        self.remaining_seconds = self.total_seconds
        
        self.cpp_done = tk.BooleanVar(value=False)
        self.school_done = tk.BooleanVar(value=False)
        self.sec_done = tk.BooleanVar(value=False) 
        self.project_done = tk.BooleanVar(value=False)
        
        self.week_offset = 0
        self.study_week_offset = 0
        self.upd_win = None
        self.contest_ids = []
        self.study_ids = []
        self.checkin_popup = None
        self.popup_timer = None
        self.ignore_next_click = False 
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=2)
        
        self.build_tab_daily()
        self.build_tab_calendar()
        self.build_tab_study()  
        self.build_tab_stats()

        self.check_cross_day()
        self.load_daily_status()
        
        self.root.bind_all("<Button-1>", self.close_popup_on_click, add="+")

    def init_db(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS streaks 
                          (platform TEXT PRIMARY KEY, current_streak INTEGER, last_checkin DATE)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS time_stats 
                          (platform TEXT PRIMARY KEY, daily_time INTEGER, total_time INTEGER, last_date DATE)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS contests 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, date TEXT, time TEXT, 
                           div TEXT, solved TEXT, upsolved TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS activity_log 
                          (date TEXT PRIMARY KEY)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS app_config 
                          (key TEXT PRIMARY KEY, value TEXT)''')
        cursor.execute("INSERT OR IGNORE INTO app_config VALUES ('last_startup', '2000-01-01')")
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS study_plan
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT, date TEXT, content TEXT, urgency TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS subjects (name TEXT PRIMARY KEY)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS other_categories (name TEXT PRIMARY KEY)''')

        try: cursor.execute("ALTER TABLE streaks ADD COLUMN prev_checkin DATE DEFAULT '2000-01-01'")
        except: pass
        try: cursor.execute("ALTER TABLE contests ADD COLUMN probs TEXT DEFAULT ''")
        except: pass
        try: cursor.execute("ALTER TABLE contests ADD COLUMN up_done TEXT DEFAULT ''")
        except: pass
        try: cursor.execute("ALTER TABLE contests ADD COLUMN c_num TEXT DEFAULT ''")
        except: pass
        
        tw_year = datetime.now().year - 1911
        try: cursor.execute(f"UPDATE contests SET date = '{tw_year}-' || date WHERE length(date) = 5")
        except: pass
            
        # ================= 無痛資料庫轉移與修復邏輯 =================
        # 1. 處理未遷移過的舊資料
        cursor.execute("SELECT count(*) FROM streaks WHERE platform='CF'")
        if cursor.fetchone()[0] > 0:
            cursor.execute("SELECT current_streak, last_checkin, prev_checkin FROM streaks WHERE platform='CF'")
            cf_s = cursor.fetchone() or (0, '2000-01-01', '2000-01-01')
            cursor.execute("SELECT current_streak, last_checkin, prev_checkin FROM streaks WHERE platform='CSES'")
            cses_s = cursor.fetchone() or (0, '2000-01-01', '2000-01-01')
            
            cpp_streak = max(cf_s[0], cses_s[0])
            cpp_last = max(cf_s[1], cses_s[1])
            cpp_prev = max(cf_s[2], cses_s[2])
            
            cursor.execute("SELECT current_streak, last_checkin, prev_checkin FROM streaks WHERE platform='picoCTF'")
            pico_s = cursor.fetchone() or (0, '2000-01-01', '2000-01-01')
            cursor.execute("SELECT current_streak, last_checkin, prev_checkin FROM streaks WHERE platform='Project'")
            proj_s = cursor.fetchone() or (0, '2000-01-01', '2000-01-01')

            cursor.execute("INSERT OR REPLACE INTO streaks VALUES (?, ?, ?, ?)", ('C++', cpp_streak, cpp_last, cpp_prev))
            cursor.execute("INSERT OR REPLACE INTO streaks VALUES (?, ?, ?, ?)", ('資安', pico_s[0], pico_s[1], pico_s[2]))
            cursor.execute("INSERT OR REPLACE INTO streaks VALUES (?, ?, ?, ?)", ('專案', proj_s[0], proj_s[1], proj_s[2]))
            cursor.execute("DELETE FROM streaks WHERE platform IN ('CF', 'CSES', 'picoCTF', 'Project')")

            cursor.execute("SELECT daily_time, total_time, last_date FROM time_stats WHERE platform='CF'")
            cf_t = cursor.fetchone() or (0, 0, '2000-01-01')
            cursor.execute("SELECT daily_time, total_time, last_date FROM time_stats WHERE platform='CSES'")
            cses_t = cursor.fetchone() or (0, 0, '2000-01-01')

            cpp_t_daily = cf_t[0] + cses_t[0]
            cpp_t_total = cf_t[1] + cses_t[1]
            cpp_t_last = max(cf_t[2], cses_t[2])

            cursor.execute("INSERT OR REPLACE INTO time_stats VALUES (?, ?, ?, ?)", ('C++', cpp_t_daily, cpp_t_total, cpp_t_last))
            cursor.execute("DELETE FROM time_stats WHERE platform IN ('CF', 'CSES', 'picoCTF', 'Project')")

        # 2. 自動修復：如果「課業」已經有大於 0 的舊 CSES 資料，將其合併給 C++ 並將課業歸零
        cursor.execute("SELECT current_streak FROM streaks WHERE platform='課業'")
        school_s_val = cursor.fetchone()
        cursor.execute("SELECT total_time FROM time_stats WHERE platform='課業'")
        school_t_val = cursor.fetchone()
        
        if (school_s_val and school_s_val[0] > 0) or (school_t_val and school_t_val[0] > 0):
            cursor.execute("SELECT current_streak, last_checkin, prev_checkin FROM streaks WHERE platform='課業'")
            sch_s = cursor.fetchone() or (0, '2000-01-01', '2000-01-01')
            cursor.execute("SELECT daily_time, total_time, last_date FROM time_stats WHERE platform='課業'")
            sch_t = cursor.fetchone() or (0, 0, '2000-01-01')
            
            cursor.execute("SELECT current_streak, last_checkin, prev_checkin FROM streaks WHERE platform='C++'")
            cpp_s = cursor.fetchone() or (0, '2000-01-01', '2000-01-01')
            cursor.execute("SELECT daily_time, total_time, last_date FROM time_stats WHERE platform='C++'")
            cpp_t = cursor.fetchone() or (0, 0, '2000-01-01')
            
            cursor.execute("UPDATE streaks SET current_streak=?, last_checkin=?, prev_checkin=? WHERE platform='C++'", 
                           (max(cpp_s[0], sch_s[0]), max(cpp_s[1], sch_s[1]), max(cpp_s[2], sch_s[2])))
            cursor.execute("UPDATE time_stats SET daily_time=?, total_time=?, last_date=? WHERE platform='C++'",
                           (max(cpp_t[0], sch_t[0]), cpp_t[1] + sch_t[1], max(cpp_t[2], sch_t[2])))
            
            cursor.execute("UPDATE streaks SET current_streak=0, last_checkin='2000-01-01', prev_checkin='2000-01-01' WHERE platform='課業'")
            cursor.execute("UPDATE time_stats SET daily_time=0, total_time=0, last_date='2000-01-01' WHERE platform='課業'")

        for plat in ['C++', '課業', '資安', '專案']:
            cursor.execute("INSERT OR IGNORE INTO streaks (platform, current_streak, last_checkin, prev_checkin) VALUES (?, 0, '2000-01-01', '2000-01-01')", (plat,))
            cursor.execute("INSERT OR IGNORE INTO time_stats VALUES (?, 0, 0, '2000-01-01')", (plat,))
                
        conn.commit()
        conn.close()

    def build_tab_daily(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="日常打卡")

        self.time_label = tk.Label(tab, text="03:00:00", font=("Helvetica", 32, "bold"), fg="#e74c3c")
        self.time_label.pack(pady=2)
        
        ctrl_frame = tk.Frame(tab)
        ctrl_frame.pack(pady=0)
        
        tk.Label(ctrl_frame, text=" ", font=("Arial", 9)).pack(side=tk.LEFT, padx=2)
        self.combo_target = ttk.Combobox(ctrl_frame, values=["C++", "課業", "資安", "專案"], width=5, state="readonly")
        self.combo_target.pack(side=tk.LEFT, padx=2)
        
        tk.Label(ctrl_frame, text="時間:", font=("Arial", 9)).pack(side=tk.LEFT, padx=2)
        self.combo_time = ttk.Combobox(ctrl_frame, values=["1 小時", "2 小時", "3 小時"], width=6, state="readonly")
        self.combo_time.set("3 小時")
        self.combo_time.pack(side=tk.LEFT, padx=2)
        self.combo_time.bind("<<ComboboxSelected>>", self.on_time_select)
        
        tk.Button(ctrl_frame, text="開始", command=self.start_timer, bg="#2ecc71", fg="white", width=4).pack(side=tk.LEFT, padx=2)
        tk.Button(ctrl_frame, text="暫停", command=self.stop_timer, bg="#f39c12", fg="white", width=4).pack(side=tk.LEFT, padx=2)
        tk.Button(ctrl_frame, text="重置", command=self.reset_timer, bg="#34495e", fg="white", width=4).pack(side=tk.LEFT, padx=2)

        check_frame = tk.LabelFrame(tab, text="今日任務", font=("Arial", 9))
        check_frame.pack(fill="x", padx=10, pady=2)

        self.lbl_cpp_streak = tk.Label(check_frame, text="C++ cnt: 0 | 0.0 hr", font=("Arial", 9))
        self.lbl_cpp_streak.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.lbl_cpp_streak.bind('<Double-1>', lambda e: self.show_last_checkin(e, 'C++'))
        tk.Checkbutton(check_frame, text="C++ 打卡", variable=self.cpp_done, command=lambda: self.handle_checkin('C++')).grid(row=0, column=1, sticky="w")

        self.lbl_school_streak = tk.Label(check_frame, text="課業 cnt: 0 | 0.0 hr", font=("Arial", 9))
        self.lbl_school_streak.grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.lbl_school_streak.bind('<Double-1>', lambda e: self.show_last_checkin(e, '課業'))
        tk.Checkbutton(check_frame, text="課業 打卡", variable=self.school_done, command=lambda: self.handle_checkin('課業')).grid(row=1, column=1, sticky="w")

        self.lbl_sec_streak = tk.Label(check_frame, text="資安 cnt: 0 | 0.0 hr", font=("Arial", 9))
        self.lbl_sec_streak.grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.lbl_sec_streak.bind('<Double-1>', lambda e: self.show_last_checkin(e, '資安'))
        tk.Checkbutton(check_frame, text="資安 打卡", variable=self.sec_done, command=lambda: self.handle_checkin('資安')).grid(row=2, column=1, sticky="w")
        
        self.lbl_project_streak = tk.Label(check_frame, text="專案 cnt: 0 | 0.0 hr", font=("Arial", 9))
        self.lbl_project_streak.grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.lbl_project_streak.bind('<Double-1>', lambda e: self.show_last_checkin(e, '專案'))
        tk.Checkbutton(check_frame, text="專案 打卡", variable=self.project_done, command=lambda: self.handle_checkin('專案')).grid(row=3, column=1, sticky="w")

        bottom_frame = tk.Frame(tab)
        bottom_frame.pack(fill="x", side=tk.BOTTOM, pady=2, padx=10)
        
        self.lbl_total_days = tk.Label(bottom_frame, text="🔥 總累積修煉: 0 天", font=("Arial", 10, "bold"), fg="#2980b9")
        self.lbl_total_days.pack(side=tk.LEFT)
        
        btn_info = tk.Button(bottom_frame, text=" ℹ ", font=("Arial", 10, "bold"), relief="flat", fg="gray", cursor="hand2", command=self.show_guide)
        btn_info.pack(side=tk.RIGHT)

    def build_tab_calendar(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="賽事行事曆")

        self.input_frame = tk.Frame(tab)
        self.input_frame.pack(fill="x", padx=2, pady=0)
        
        tk.Label(self.input_frame, text="賽事:", font=("Arial", 8)).grid(row=0, column=0, sticky="e")
        self.entry_type = ttk.Combobox(self.input_frame, values=["CF", "LC", "CPE", "Other"], width=4, state="readonly")
        self.entry_type.grid(row=0, column=1, padx=2, pady=2)
        self.entry_type.set("CF")
        
        tk.Label(self.input_frame, text="日期(MMDD):", font=("Arial", 8)).grid(row=0, column=2, sticky="e")
        self.entry_date = tk.Entry(self.input_frame, width=5)
        self.entry_date.grid(row=0, column=3, padx=2)
        
        tk.Label(self.input_frame, text="時間(HHMM):", font=("Arial", 8)).grid(row=0, column=4, sticky="e")
        self.entry_time = tk.Entry(self.input_frame, width=5)
        self.entry_time.grid(row=0, column=5, padx=2)
        
        self.lbl_div_type = tk.Label(self.input_frame, text="Div:", font=("Arial", 8))
        self.entry_div = tk.Entry(self.input_frame, width=6)
        
        self.combo_lc_type = ttk.Combobox(self.input_frame, values=["Weekly", "Biweekly"], width=6, state="readonly")
        self.combo_lc_type.set("Weekly")
        
        self.lbl_other = tk.Label(self.input_frame, text="自訂:", font=("Arial", 8))
        self.combo_other = ttk.Combobox(self.input_frame, width=8)
        self.btn_del_other = tk.Button(self.input_frame, text="x", command=self.delete_other_category, fg="red", relief="flat", font=("Arial", 8, "bold"))
        self.load_other_categories()

        self.lbl_cnum = tk.Label(self.input_frame, text="編號(4碼):", font=("Arial", 8))
        self.entry_cnum = tk.Entry(self.input_frame, width=5)

        self.entry_type.bind("<<ComboboxSelected>>", self.on_type_change)
        
        self.lbl_div_type.grid(row=1, column=0, sticky="e")
        self.entry_div.grid(row=1, column=1, padx=2, pady=2)
        self.lbl_cnum.grid(row=1, column=2, sticky="e")
        self.entry_cnum.grid(row=1, column=3, padx=2)

        tk.Button(self.input_frame, text="新增", command=self.add_contest, bg="#3498db", fg="white", height=1).grid(row=1, column=4, columnspan=2, padx=5, sticky="we")

        nav_frame = tk.Frame(tab)
        nav_frame.pack(fill="x", pady=0)
        tk.Button(nav_frame, text="◀", command=lambda: self.change_week(-1)).pack(side=tk.LEFT, padx=10)
        self.lbl_week = tk.Label(nav_frame, text="本週", font=("Arial", 9, "bold"), cursor="hand2")
        self.lbl_week.pack(side=tk.LEFT, expand=True)
        self.lbl_week.bind("<Button-1>", self.reset_week_view)
        tk.Button(nav_frame, text="▶", command=lambda: self.change_week(1)).pack(side=tk.RIGHT, padx=10)

        canvas_frame = tk.Frame(tab)
        canvas_frame.pack(fill="x", pady=2)
        
        self.canvas_scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical")
        self.canvas_scrollbar.pack(side=tk.RIGHT, fill="y")
        self.canvas = tk.Canvas(canvas_frame, height=90, bg="#1e1e1e", highlightthickness=0, yscrollcommand=self.canvas_scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill="both", expand=True)
        self.canvas_scrollbar.config(command=self.canvas.yview)

        def _on_mousewheel(event):
            if getattr(event, 'delta', 0) != 0:
                direction = -1 if event.delta > 0 else 1
                self.canvas.yview_scroll(direction, "units")
            elif getattr(event, 'num', 0) in (4, 5):
                direction = -1 if event.num == 4 else 1
                self.canvas.yview_scroll(direction, "units")

        def _bind_mouse(event):
            self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
            self.canvas.bind_all("<Button-4>", _on_mousewheel)
            self.canvas.bind_all("<Button-5>", _on_mousewheel)

        def _unbind_mouse(event):
            self.canvas.unbind_all("<MouseWheel>")
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")

        self.canvas.bind("<Enter>", _bind_mouse)
        self.canvas.bind("<Leave>", _unbind_mouse)
        
        del_frame = tk.Frame(tab)
        del_frame.pack(fill="both", expand=True, padx=5, pady=0)
        self.list_contests = tk.Listbox(del_frame, height=3, font=("Arial", 8))
        self.list_contests.pack(side=tk.LEFT, fill="both", expand=True)
        tk.Button(del_frame, text="刪除", command=self.delete_contest, bg="#e74c3c", fg="white").pack(side=tk.RIGHT, padx=2)

        self.draw_calendar()

    def load_other_categories(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM other_categories")
        cats = [r[0] for r in cursor.fetchall()]
        conn.close()
        self.combo_other['values'] = cats

    def delete_other_category(self):
        cat = self.combo_other.get().strip()
        if not cat: return
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM other_categories WHERE name=?", (cat,))
        conn.commit()
        conn.close()
        self.combo_other.set('')
        self.load_other_categories()

    def on_type_change(self, event=None):
        self.lbl_div_type.grid_remove()
        self.entry_div.grid_remove()
        self.combo_lc_type.grid_remove()
        self.lbl_other.grid_remove()
        self.combo_other.grid_remove()
        self.btn_del_other.grid_remove()
        self.lbl_cnum.grid_remove()
        self.entry_cnum.grid_remove()
        
        self.entry_time.config(state="normal") 
        ctype = self.entry_type.get()
        
        if ctype == "LC":
            self.lbl_div_type.config(text="類型:")
            self.lbl_div_type.grid(row=1, column=0, sticky="e")
            self.combo_lc_type.grid(row=1, column=1, padx=2, pady=2)
            
            self.lbl_cnum.config(text="編號(4碼):")
            self.lbl_cnum.grid(row=1, column=2, sticky="e")
            self.entry_cnum.config(state="normal")
            self.entry_cnum.grid(row=1, column=3, padx=2)
            
        elif ctype == "Other":
            self.lbl_other.grid(row=1, column=0, sticky="e")
            self.combo_other.grid(row=1, column=1, padx=2, pady=2)
            self.btn_del_other.grid(row=1, column=2, sticky="w")
            
        elif ctype == "CPE":
            self.entry_time.delete(0, 'end')
            self.entry_time.config(state="disabled") 
            self.lbl_cnum.config(text="民國年:")
            self.lbl_cnum.grid(row=1, column=0, sticky="e")
            self.entry_cnum.config(state="normal")
            self.entry_cnum.grid(row=1, column=1, padx=2, pady=2)
            
        else: # CF
            self.lbl_div_type.config(text="Div:")
            self.lbl_div_type.grid(row=1, column=0, sticky="e")
            self.entry_div.grid(row=1, column=1, padx=2, pady=2)
            
            self.lbl_cnum.config(text="編號(4碼):")
            self.lbl_cnum.grid(row=1, column=2, sticky="e")
            self.entry_cnum.config(state="normal")
            self.entry_cnum.grid(row=1, column=3, padx=2)

    def build_tab_study(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="課業安排")

        input_frame = tk.Frame(tab)
        input_frame.pack(fill="x", padx=2, pady=2)

        tk.Label(input_frame, text="科目:", font=("Arial", 8)).grid(row=0, column=0, sticky="e")
        
        self.combo_subject = ttk.Combobox(input_frame, width=9)
        self.combo_subject.grid(row=0, column=1, padx=2, pady=2)
        self.load_subjects()
        
        btn_del_subj = tk.Button(input_frame, text="x", command=self.delete_subject_from_menu, fg="red", relief="flat", font=("Arial", 8, "bold"))
        btn_del_subj.grid(row=0, column=2, padx=0)

        tk.Label(input_frame, text="日期(MMDD):", font=("Arial", 8)).grid(row=0, column=3, sticky="e")
        self.entry_s_date = tk.Entry(input_frame, width=5)
        self.entry_s_date.grid(row=0, column=4, padx=2)

        tk.Button(input_frame, text="新增", command=self.add_study_plan, bg="#3498db", fg="white", height=1).grid(row=0, column=5, rowspan=2, padx=5, sticky="nsew")

        tk.Label(input_frame, text="內容:", font=("Arial", 8)).grid(row=1, column=0, sticky="e")
        self.entry_s_content = tk.Entry(input_frame, width=12)
        self.entry_s_content.grid(row=1, column=1, columnspan=2, sticky="w", padx=2)

        tk.Label(input_frame, text="急迫性:", font=("Arial", 8)).grid(row=1, column=3, sticky="e")
        self.combo_urgency = ttk.Combobox(input_frame, values=["紅色緊急", "淺藍色不緊急", "可以放棄的灰色"], width=13, state="readonly")
        self.combo_urgency.set("紅色緊急")
        self.combo_urgency.grid(row=1, column=4, padx=2)

        nav_frame = tk.Frame(tab)
        nav_frame.pack(fill="x", pady=0)
        tk.Button(nav_frame, text="◀", command=lambda: self.change_study_week(-1)).pack(side=tk.LEFT, padx=10)
        self.lbl_study_week = tk.Label(nav_frame, text="本週", font=("Arial", 9, "bold"), cursor="hand2")
        self.lbl_study_week.pack(side=tk.LEFT, expand=True)
        self.lbl_study_week.bind("<Button-1>", self.reset_study_week_view)
        tk.Button(nav_frame, text="▶", command=lambda: self.change_study_week(1)).pack(side=tk.RIGHT, padx=10)

        canvas_frame = tk.Frame(tab)
        canvas_frame.pack(fill="x", pady=2)
        
        self.study_canvas_scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical")
        self.study_canvas_scrollbar.pack(side=tk.RIGHT, fill="y")
        self.study_canvas = tk.Canvas(canvas_frame, height=90, bg="#1e1e1e", highlightthickness=0, yscrollcommand=self.study_canvas_scrollbar.set)
        self.study_canvas.pack(side=tk.LEFT, fill="both", expand=True)
        self.study_canvas_scrollbar.config(command=self.study_canvas.yview)

        def _on_s_mousewheel(event):
            if getattr(event, 'delta', 0) != 0:
                direction = -1 if event.delta > 0 else 1
                self.study_canvas.yview_scroll(direction, "units")
            elif getattr(event, 'num', 0) in (4, 5):
                direction = -1 if event.num == 4 else 1
                self.study_canvas.yview_scroll(direction, "units")

        def _s_bind_mouse(event):
            self.study_canvas.bind_all("<MouseWheel>", _on_s_mousewheel)
            self.study_canvas.bind_all("<Button-4>", _on_s_mousewheel)
            self.study_canvas.bind_all("<Button-5>", _on_s_mousewheel)

        def _s_unbind_mouse(event):
            self.study_canvas.unbind_all("<MouseWheel>")
            self.study_canvas.unbind_all("<Button-4>")
            self.study_canvas.unbind_all("<Button-5>")

        self.study_canvas.bind("<Enter>", _s_bind_mouse)
        self.study_canvas.bind("<Leave>", _s_unbind_mouse)

        del_frame = tk.Frame(tab)
        del_frame.pack(fill="both", expand=True, padx=5, pady=0)
        self.list_study = tk.Listbox(del_frame, height=3, font=("Arial", 8))
        self.list_study.pack(side=tk.LEFT, fill="both", expand=True)
        tk.Button(del_frame, text="刪除", command=self.delete_study_plan, bg="#e74c3c", fg="white").pack(side=tk.RIGHT, padx=2)

        self.draw_study_calendar()

    def build_tab_stats(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="戰力與補題")
        
        self.stat_frame = tk.Frame(tab, bg="#f5f6fa")
        self.stat_frame.pack(fill="x", pady=2, padx=5)
        self.lbl_stats = tk.Label(self.stat_frame, text="資料載入中...", justify=tk.LEFT, bg="#f5f6fa", font=("Arial", 9))
        self.lbl_stats.pack(anchor="w", pady=2, padx=5)

        header_frame = tk.Frame(tab)
        header_frame.pack(fill="x", padx=5)
        
        tk.Label(header_frame, text="雙擊下方賽事修改進度", font=("Arial", 8, "bold"), fg="gray").pack(side=tk.LEFT)
        
        self.filter_cf = tk.BooleanVar(value=False)
        self.filter_lc = tk.BooleanVar(value=False)
        self.filter_cpe = tk.BooleanVar(value=True) 
        self.filter_other = tk.BooleanVar(value=False)

        tk.Checkbutton(header_frame, text="Other", variable=self.filter_other, command=self.refresh_stats).pack(side=tk.RIGHT)
        tk.Checkbutton(header_frame, text="CPE", variable=self.filter_cpe, command=self.refresh_stats).pack(side=tk.RIGHT)
        tk.Checkbutton(header_frame, text="LC", variable=self.filter_lc, command=self.refresh_stats).pack(side=tk.RIGHT)
        tk.Checkbutton(header_frame, text="CF", variable=self.filter_cf, command=self.refresh_stats).pack(side=tk.RIGHT)
        tk.Label(header_frame, text="篩選:", font=("Arial", 8, "bold")).pack(side=tk.RIGHT, padx=2)

        cols = ('ID', '賽事', '日期', '題目', '賽中', '未補')
        disp_cols = ('賽事', '日期', '題目', '賽中', '未補')
        
        self.tree = ttk.Treeview(tab, columns=cols, displaycolumns=disp_cols, show='headings', height=5)
        for c, w in zip(disp_cols, [75, 50, 60, 45, 45]):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w, anchor='center')
            
        self.tree.pack(fill='both', expand=True, padx=5, pady=2)
        self.tree.bind('<Double-1>', self.on_tree_double_click)
        
        self.refresh_stats()

    # ================= 課業安排相關邏輯 =================
    def load_subjects(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM subjects")
        subs = [r[0] for r in cursor.fetchall()]
        conn.close()
        self.combo_subject['values'] = subs

    def delete_subject_from_menu(self):
        subj = self.combo_subject.get().strip()
        if not subj: return
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM subjects WHERE name=?", (subj,))
        conn.commit()
        conn.close()
        self.combo_subject.set('')
        self.load_subjects()

    def add_study_plan(self):
        subj = self.combo_subject.get().strip()
        raw_date = self.entry_s_date.get().strip()
        content = self.entry_s_content.get().strip()
        urgency = self.combo_urgency.get()

        if not subj or not content:
            messagebox.showerror("錯誤", "科目與內容不可為空")
            return
        if len(raw_date) != 4 or not raw_date.isdigit():
            messagebox.showerror("錯誤", "日期格式錯誤 (例: 0718)")
            return

        tw_year = datetime.now().year - 1911
        sdate = f"{tw_year}-{raw_date[:2]}-{raw_date[2:]}"

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO subjects (name) VALUES (?)", (subj,))
        cursor.execute("INSERT INTO study_plan (subject, date, content, urgency) VALUES (?, ?, ?, ?)", (subj, sdate, content, urgency))
        conn.commit()
        conn.close()

        self.entry_s_date.delete(0, 'end')
        self.entry_s_content.delete(0, 'end')
        self.load_subjects()
        self.draw_study_calendar()

    def delete_study_plan(self):
        selected = self.list_study.curselection()
        if not selected: return
        idx = selected[0]
        sid = self.study_ids[idx]
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM study_plan WHERE id=?", (sid,))
        conn.commit()
        conn.close()
        self.draw_study_calendar()

    def change_study_week(self, delta):
        self.study_week_offset += delta
        self.draw_study_calendar()
        
    def reset_study_week_view(self, event=None):
        if self.study_week_offset != 0:
            self.study_week_offset = 0
            self.draw_study_calendar()

    def draw_study_calendar(self):
        self.study_canvas.delete("all")
        self.list_study.delete(0, tk.END)
        self.study_ids.clear()

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM study_plan ORDER BY date DESC")
        plans = cursor.fetchall()
        
        # 讀取賽事，疊加顯示在課業行事曆上
        cursor.execute("SELECT * FROM contests ORDER BY date DESC, time DESC")
        contests = cursor.fetchall()
        conn.close()

        today = datetime.now().date()
        idx = (today.weekday() + 1) % 7
        sunday = today - timedelta(days=idx)
        start_date = sunday + timedelta(weeks=self.study_week_offset)

        if self.study_week_offset == 0:
            self.lbl_study_week.config(text="本週", fg="#f39c12")
        else:
            mid_week = start_date + timedelta(days=3)
            self.lbl_study_week.config(text=f"{mid_week.month} 月", fg="#3498db")

        days_zh = ["日", "一", "二", "三", "四", "五", "六"]
        col_width = 350 / 7

        for i in range(7):
            d = start_date + timedelta(days=i)
            x_center = i * col_width + (col_width / 2) + 5
            is_today = (d == today)
            bg_color = "#ff4757" if is_today else "#1e1e1e"

            self.study_canvas.create_text(x_center, 8, text=days_zh[i], fill="#7f8fa6", font=("Arial", 8))
            if is_today:
                self.study_canvas.create_oval(x_center-12, 16, x_center+12, 40, fill=bg_color, outline="")
            self.study_canvas.create_text(x_center, 28, text=d.strftime("%d"), fill="white" if is_today else "gray", font=("Arial", 9, "bold"))

            day_str = d.strftime("%m-%d")
            y_offset = 46

            # 先畫上賽事，純視覺顯示
            for c in contests:
                if c[2][-5:] == day_str:
                    c_type = c[1]
                    c_div = c[4]
                    c_num = c[9] if len(c) > 9 else ""
                    
                    if c_type == "LC":
                        text_disp = f"LC {c_num}\n{c_div}"
                        box_col = "#e67e22"
                    elif c_type == "Other":
                        text_disp = f"{c_div[:8]}"
                        box_col = "#9b59b6" 
                    elif c_type == "CPE":
                        text_disp = f"CPE {c_num}"
                        box_col = "#27ae60"
                    else:
                        text_disp = f"CF {c_num}\n{c_div}"
                        box_col = "#3498db"
                        
                    self.study_canvas.create_rectangle(x_center-col_width/2+2, y_offset, x_center+col_width/2-2, y_offset+25, fill="#2f3542", outline=box_col)
                    self.study_canvas.create_text(x_center, y_offset+12, text=text_disp, fill=box_col, font=("Arial", 6))
                    y_offset += 28

            # 再畫上課業
            for p in plans:
                if p[2][-5:] == day_str:
                    u = p[4]
                    if u == "紅色緊急": box_col = "#e74c3c"
                    elif u == "可以放棄的灰色": box_col = "#7f8fa6"
                    else: box_col = "#3498db"

                    text_disp = f"{p[1][:5]}\n{p[3][:5]}"

                    self.study_canvas.create_rectangle(x_center-col_width/2+2, y_offset, x_center+col_width/2-2, y_offset+25, fill="#2f3542", outline=box_col)
                    self.study_canvas.create_text(x_center, y_offset+12, text=text_disp, fill=box_col, font=("Arial", 6))
                    y_offset += 28

        # 這裡僅將課業安排存入刪除列表，避免誤刪賽事
        for p in plans:
            self.study_ids.append(p[0])
            disp_date = p[2][-5:]
            self.list_study.insert(tk.END, f"{disp_date} | {p[1]} - {p[3]} ({p[4]})")

        self.study_canvas.yview_moveto(0)
        bbox = self.study_canvas.bbox("all")
        if bbox:
            self.study_canvas.config(scrollregion=(0, 0, bbox[2], max(90, bbox[3] + 10)))

    # ================= 核心邏輯 =================
    def show_guide(self):
        guide_text = (
            "🏆 【每日指南】\n\n"
            "🔴 Part 1: C++\n"
            "• 解題、看 Tutorial。\n\n"
            "🔵 Part 2: 課業\n"
            "• 讀書與整理。\n\n"
            "📅 賽事與自動化\n"
            "• Other 類別可以自訂賽事/任務分類，並單獨篩選！\n"
            "• 雙擊補題頁面的比賽，再次雙擊「編號/分類」即可原地修改！\n\n"
            "(本地 db 好耶!\n"
            "SINCE 115/07/16 RC"
        )
        messagebox.showinfo("每日生存證明", guide_text)

    def on_time_select(self, event=None):
        val = self.combo_time.get()
        if "1" in val: self.total_seconds = 3600
        elif "2" in val: self.total_seconds = 7200
        else: self.total_seconds = 10800
        self.reset_timer()

    def update_target_default(self):
        cpp = self.cpp_done.get()
        school = self.school_done.get()
        sec = self.sec_done.get()
        if not cpp:
            self.combo_target.set("C++")
        elif not school:
            self.combo_target.set("課業")
        elif not sec:
            self.combo_target.set("資安")
        else:
            self.combo_target.set("專案") 

    def check_cross_day(self):
        today = datetime.now().strftime('%Y-%m-%d')
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute("SELECT value FROM app_config WHERE key='last_startup'")
        last_startup = cursor.fetchone()[0]
        
        if last_startup != today:
            self.cpp_done.set(False)
            self.school_done.set(False)
            self.sec_done.set(False)
            self.project_done.set(False)
            
            cursor.execute("UPDATE app_config SET value=? WHERE key='last_startup'", (today,))
            conn.commit()
            
            self.update_target_default()
            self.refresh_stats()
            
        conn.close()
        self.root.after(60000, self.check_cross_day)

    def change_week(self, delta):
        self.week_offset += delta
        self.draw_calendar()
        
    def reset_week_view(self, event=None):
        if self.week_offset != 0:
            self.week_offset = 0
            self.draw_calendar()

    def reset_timer(self):
        self.timer_running = False
        self.remaining_seconds = self.total_seconds
        mins, secs = divmod(self.remaining_seconds, 60)
        hours, mins = divmod(mins, 60)
        self.time_label.config(text=f"{hours:02d}:{mins:02d}:{secs:02d}")

    def start_timer(self):
        target = self.combo_target.get()
        if not target:
            messagebox.showwarning("警告", "請先在下拉選單選擇計時對象！")
            return
            
        if not self.timer_running and self.remaining_seconds > 0:
            self.timer_running = True
            self.update_timer()

    def stop_timer(self):
        self.timer_running = False

    def update_timer(self):
        if self.timer_running and self.remaining_seconds > 0:
            mins, secs = divmod(self.remaining_seconds, 60)
            hours, mins = divmod(mins, 60)
            self.time_label.config(text=f"{hours:02d}:{mins:02d}:{secs:02d}")
            
            elapsed = self.total_seconds - self.remaining_seconds
            if elapsed > 0 and elapsed % 60 == 0:
                self.record_time()

            self.remaining_seconds -= 1
            self.root.after(1000, self.update_timer)
        elif self.remaining_seconds <= 0:
            self.time_label.config(text="00:00:00")
            self.timer_running = False
            self.record_time()

    def record_time(self):
        today = datetime.now().strftime('%Y-%m-%d')
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        target = self.combo_target.get()
        if not target: 
            conn.close()
            return
            
        cursor.execute("SELECT daily_time, total_time, last_date FROM time_stats WHERE platform=?", (target,))
        row = cursor.fetchone()
        
        if row:
            daily_time, total_time, last_date = row[0], row[1], row[2]
        else:
            daily_time, total_time, last_date = 0, 0, '2000-01-01'
        
        if last_date != today: daily_time = 0 
        cursor.execute("UPDATE time_stats SET daily_time=?, total_time=?, last_date=? WHERE platform=?", 
                       (daily_time + 60, total_time + 60, today, target))
        conn.commit()
        conn.close()
        self.refresh_stats()

    def handle_checkin(self, platform):
        var_name = self.plat_map[platform]
        is_checked = getattr(self, f"{var_name}_done").get()
        today = datetime.now().strftime('%Y-%m-%d')
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute("SELECT current_streak, last_checkin, prev_checkin FROM streaks WHERE platform=?", (platform,))
        streak, last_date, prev_date = cursor.fetchone()
        
        if is_checked:
            if last_date != today:
                streak = streak + 1 
                cursor.execute("UPDATE streaks SET current_streak=?, last_checkin=?, prev_checkin=? WHERE platform=?", (streak, today, last_date, platform))
        else:
            if last_date == today:
                streak = max(0, streak - 1)
                cursor.execute("UPDATE streaks SET current_streak=?, last_checkin=? WHERE platform=?", (streak, prev_date, platform))
                
        any_checked = self.cpp_done.get() or self.school_done.get() or self.sec_done.get() or self.project_done.get()
        if any_checked:
            cursor.execute("INSERT OR IGNORE INTO activity_log (date) VALUES (?)", (today,))
        else:
            cursor.execute("DELETE FROM activity_log WHERE date=?", (today,))
            
        conn.commit()
        conn.close()
        
        self.update_target_default()
        self.refresh_stats()

    def load_daily_status(self):
        today = datetime.now().strftime('%Y-%m-%d')
        today_md = datetime.now().strftime('%m-%d')
        tw_year = datetime.now().year - 1911
        today_tw = f"{tw_year}-{today_md}"
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        for plat in ['C++', '課業', '資安', '專案']:
            cursor.execute("SELECT last_checkin FROM streaks WHERE platform=?", (plat,))
            if cursor.fetchone()[0] == today:
                getattr(self, f"{self.plat_map[plat]}_done").set(True)
                
        cursor.execute("SELECT id FROM contests WHERE type='CF' AND date=?", (today_tw,))
        if cursor.fetchone() and not self.cpp_done.get():
            self.cpp_done.set(True)
            self.handle_checkin('C++') 
            
        conn.close()
        self.update_target_default()

    def add_contest(self):
        ctype = self.entry_type.get()
        raw_date = self.entry_date.get()
        raw_time = self.entry_time.get()
        cdiv = ""
        cnum = ""
        
        if ctype == "LC":
            cdiv = self.combo_lc_type.get()
            cnum = self.entry_cnum.get().strip()
        elif ctype == "Other":
            cdiv = self.combo_other.get().strip()
        elif ctype == "CF":
            cdiv = self.entry_div.get().strip()
            cnum = self.entry_cnum.get().strip()
        elif ctype == "CPE":
            cnum = self.entry_cnum.get().strip()
            raw_time = "0000"
            
        if ctype not in ["Other", "CPE"]:
            if len(raw_date) != 4 or not raw_date.isdigit() or len(raw_time) != 4 or not raw_time.isdigit():
                messagebox.showerror("錯誤", "格式錯誤，請輸入 4 碼 (例: 0718)")
                return
        elif ctype == "CPE":
            if len(raw_date) != 4 or not raw_date.isdigit():
                messagebox.showerror("錯誤", "日期格式錯誤 (例: 0718)")
                return
        else: # Other
            if len(raw_date) != 4 or not raw_date.isdigit():
                messagebox.showerror("錯誤", "日期格式錯誤 (例: 0718)")
                return
            if len(raw_time) != 4 and raw_time != "":
                 if not raw_time.isdigit():
                    messagebox.showerror("錯誤", "時間請留空或輸入 4 碼")
                    return
            elif raw_time == "": raw_time = "0000"
            
        tw_year = datetime.now().year - 1911
        cdate = f"{tw_year}-{raw_date[:2]}-{raw_date[2:]}"
        ctime = f"{raw_time[:2]}:{raw_time[2:]}"
        
        if ctype == "CF" and cdiv:
            if not cdiv.lower().startswith("div"):
                cdiv = f"Div {cdiv}"
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        if ctype == "Other" and cdiv:
            cursor.execute("INSERT OR IGNORE INTO other_categories (name) VALUES (?)", (cdiv,))
            self.load_other_categories()

        cursor.execute('''INSERT INTO contests 
                          (type, date, time, div, solved, upsolved, probs, up_done, c_num) 
                          VALUES (?, ?, ?, ?, '', '', '', '', ?)''', 
                       (ctype, cdate, ctime, cdiv, cnum))
        conn.commit()
        conn.close()
        
        self.entry_date.delete(0, 'end')
        self.entry_time.delete(0, 'end')
        if ctype != "Other":
            self.entry_cnum.delete(0, 'end')
            
        self.draw_calendar()
        self.refresh_stats()

    def delete_contest(self):
        selected = self.list_contests.curselection()
        if not selected: return
        
        idx = selected[0]
        cid = self.contest_ids[idx]
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contests WHERE id=?", (cid,))
        conn.commit()
        conn.close()
        self.draw_calendar()
        self.refresh_stats()

    def draw_calendar(self):
        self.canvas.delete("all")
        self.list_contests.delete(0, tk.END)
        self.contest_ids.clear()
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contests ORDER BY date DESC, time DESC")
        contests = cursor.fetchall()
        conn.close()
        
        today = datetime.now().date()
        idx = (today.weekday() + 1) % 7
        sunday = today - timedelta(days=idx)
        start_date = sunday + timedelta(weeks=self.week_offset)
        
        if self.week_offset == 0:
            self.lbl_week.config(text="本週", fg="#f39c12") 
        else:
            mid_week = start_date + timedelta(days=3)
            self.lbl_week.config(text=f"{mid_week.month} 月", fg="#3498db")
        
        days_zh = ["日", "一", "二", "三", "四", "五", "六"]
        col_width = 350 / 7  
        
        for i in range(7):
            d = start_date + timedelta(days=i)
            x_center = i * col_width + (col_width / 2) + 5
            
            is_today = (d == today)
            bg_color = "#ff4757" if is_today else "#1e1e1e"
            
            self.canvas.create_text(x_center, 8, text=days_zh[i], fill="#7f8fa6", font=("Arial", 8))
            if is_today:
                self.canvas.create_oval(x_center-12, 16, x_center+12, 40, fill=bg_color, outline="")
            self.canvas.create_text(x_center, 28, text=d.strftime("%d"), fill="white" if is_today else "gray", font=("Arial", 9, "bold"))
            
            day_str = d.strftime("%m-%d")
            y_offset = 46
            for c in contests:
                if c[2][-5:] == day_str:
                    c_type = c[1]
                    c_div = c[4]
                    c_num = c[9] if len(c) > 9 else ""
                    
                    if c_type == "LC":
                        text_disp = f"LC {c_num}\n{c_div}"
                        box_col = "#e67e22"
                    elif c_type == "Other":
                        text_disp = f"{c_div[:8]}"
                        box_col = "#9b59b6" 
                    elif c_type == "CPE":
                        text_disp = f"CPE {c_num}"
                        box_col = "#27ae60"
                    else:
                        text_disp = f"CF {c_num}\n{c_div}"
                        box_col = "#3498db"
                        
                    self.canvas.create_rectangle(x_center-col_width/2+2, y_offset, x_center+col_width/2-2, y_offset+25, fill="#2f3542", outline=box_col)
                    self.canvas.create_text(x_center, y_offset+12, text=text_disp, fill=box_col, font=("Arial", 6))
                    y_offset += 28

        for c in contests:
            self.contest_ids.append(c[0]) 
            c_type = c[1]
            c_num = c[9] if len(c) > 9 else ""
            c_div = c[4]
            disp_date = c[2][-5:]
            if c_type == "Other":
                self.list_contests.insert(tk.END, f"{disp_date} | {c_div}")
            elif c_type == "CPE":
                self.list_contests.insert(tk.END, f"{disp_date} | CPE {c_num}年")
            else:
                self.list_contests.insert(tk.END, f"{disp_date} {c[3]} | {c_type} {c_num} ({c_div})")
                
        self.canvas.yview_moveto(0) 
        bbox = self.canvas.bbox("all")
        if bbox:
            self.canvas.config(scrollregion=(0, 0, bbox[2], max(90, bbox[3] + 10)))

    def refresh_stats(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        for plat in ['C++', '課業', '資安', '專案']:
            cursor.execute("SELECT current_streak FROM streaks WHERE platform=?", (plat,))
            streak = cursor.fetchone()[0] if cursor.rowcount != 0 else 0
            
            cursor.execute("SELECT total_time FROM time_stats WHERE platform=?", (plat,))
            t_row = cursor.fetchone()
            total_hours = (t_row[0] / 3600) if t_row else 0
            time_str = f" | {total_hours:.1f} hr"
            
            lbl = getattr(self, f"lbl_{self.plat_map[plat]}_streak")
            lbl.config(text=f"{plat} D-{streak} {time_str}")
            
        cursor.execute("SELECT COUNT(*) FROM activity_log")
        total_days = cursor.fetchone()[0]
        self.lbl_total_days.config(text=f"🔥 總累積修煉: {total_days} 天")
            
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        filters = []
        if self.filter_cf.get(): filters.append("'CF'")
        if self.filter_lc.get(): filters.append("'LC'")
        if self.filter_cpe.get(): filters.append("'CPE'")
        if self.filter_other.get(): filters.append("'Other'")
            
        if not filters:
            cursor.execute("SELECT id, type, date, div, probs, solved, up_done, c_num FROM contests WHERE 1=0")
        else:
            query = f"SELECT id, type, date, div, probs, solved, up_done, c_num FROM contests WHERE type IN ({','.join(filters)}) ORDER BY date DESC, time DESC"
            cursor.execute(query)
            
        cf_cnt, lc_cnt, cpe_cnt, other_cnt = 0, 0, 0, 0
        tot_solved, tot_up = 0, 0
        last_month = None
        
        for row in cursor.fetchall():
            c_id, c_type, c_date, c_div, c_probs, c_solved, c_up, c_num = row
            
            current_month = c_date[-5:-3] 
            if current_month != last_month:
                self.tree.insert("", "end", values=('', f'--- {int(current_month)} 月 ---', '', '', '', ''), tags=('sep',))
                last_month = current_month
            
            c_solved_clean = (c_solved or "").upper().replace(" ", "").replace(",", "")
            c_up_clean = (c_up or "").upper().replace(" ", "").replace(",", "")
            
            sol_cnt = len(c_solved_clean)
            up_cnt = len(c_up_clean)
            
            if c_type == "CF":
                event_str = f"CF {c_num}"
                cf_cnt += 1
            elif c_type == "LC":
                event_str = f"LC {c_num}"
                lc_cnt += 1
            elif c_type == "CPE":
                event_str = f"CPE {c_num}"
                cpe_cnt += 1
            elif c_type == "Other":
                event_str = f"{c_div}"
                other_cnt += 1

            unsolved_str = "-"
            if c_probs:
                p_str = c_probs.upper().replace("~", "-")
                all_probs = []
                if '-' in p_str:
                    parts = p_str.split('-')
                    if len(parts) == 2:
                        start, end = parts[0], parts[1]
                        if start.isdigit() and end.isdigit():
                            all_probs = [str(i) for i in range(int(start), int(end)+1)]
                        elif start.isalpha() and end.isalpha():
                            all_probs = [chr(i) for i in range(ord(start), ord(end)+1)]
                
                if not all_probs:
                    all_probs = list(p_str)
                
                done_list = list(c_solved_clean + c_up_clean)
                missing = [p for p in all_probs if p not in done_list]
                
                if missing:
                    unsolved_str = "".join(missing)
                else:
                    unsolved_str = "✔"

            disp_row = (c_id, event_str, c_date[-5:], c_probs or '-', sol_cnt or '-', unsolved_str)
            self.tree.insert("", "end", values=disp_row)
            
            tot_solved += sol_cnt
            tot_up += up_cnt
            
        self.tree.tag_configure('sep', background='#dcdde1')
            
        self.lbl_stats.config(text=f"🏆 CF {cf_cnt} | LC {lc_cnt} | CPE {cpe_cnt} | 另 {other_cnt}\n🔥 解出: {tot_solved} 項 | 🛠️ 賽後補題: {tot_up} 題")
        conn.close()

    def show_last_checkin(self, event, platform):
        self.close_popup()
        
        self.ignore_next_click = True
        self.root.after(200, lambda: setattr(self, 'ignore_next_click', False))
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT last_checkin, current_streak, prev_checkin FROM streaks WHERE platform=?", (platform,))
        row = cursor.fetchone()
        conn.close()
        
        if not row: return
        last_checkin, streak, prev_checkin = row
        today = datetime.now().strftime('%Y-%m-%d')
        
        if last_checkin == today:
            prev_date = prev_checkin if prev_checkin != '2000-01-01' else "無"
        else:
            prev_date = last_checkin if last_checkin != '2000-01-01' else "無"
            
        self.checkin_popup = tk.Toplevel(self.root)
        self.checkin_popup.wm_overrideredirect(True) 
        self.checkin_popup.attributes("-topmost", True)
        
        x = event.x_root + 15
        y = event.y_root + 15
        self.checkin_popup.geometry(f"+{x}+{y}")
        
        lbl = tk.Label(self.checkin_popup, text=f"上次打卡: {prev_date}", 
                       bg="#fffae6", fg="#d35400", borderwidth=1, relief="solid", 
                       font=("Arial", 9), padx=5, pady=2)
        lbl.pack()
        
        self.popup_timer = self.root.after(1000, self.close_popup)

    def close_popup(self, event=None):
        if getattr(self, 'popup_timer', None):
            self.root.after_cancel(self.popup_timer)
            self.popup_timer = None
            
        if getattr(self, 'checkin_popup', None):
            try:
                self.checkin_popup.destroy()
            except Exception:
                pass
            self.checkin_popup = None
            
    def close_popup_on_click(self, event):
        if getattr(self, 'ignore_next_click', False):
            return
            
        if getattr(self, 'checkin_popup', None) and self.checkin_popup.winfo_exists():
            try:
                if event.widget == self.checkin_popup or event.widget.master == self.checkin_popup:
                    return
            except Exception:
                pass
            
            self.close_popup()

    def on_tree_double_click(self, event):
        selected = self.tree.selection()
        if not selected: return
        
        item = self.tree.item(selected[0])
        cid = item['values'][0]
        
        if not str(cid).strip(): return
        
        if self.upd_win and self.upd_win.winfo_exists():
            self.upd_win.lift()
            return
            
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT type, probs, solved, up_done, c_num, div, date FROM contests WHERE id=?", (cid,))
        row = cursor.fetchone()
        conn.close()
        
        ctype, cur_probs, cur_solved, cur_up_done, cur_cnum, cur_div, full_date = row
        is_lc = (ctype == "LC")
        is_cpe = (ctype == "CPE")
        is_cf = (ctype == "CF")
        is_other = (ctype == "Other")
        
        if not cur_probs:
            if is_lc: cur_probs = "1-4"
            elif is_cpe: cur_probs = "1-7"
            elif is_cf: cur_probs = "A-F"
            else: cur_probs = ""
            
        cur_solved = cur_solved if cur_solved else ""
        cur_up_done = cur_up_done if cur_up_done else ""

        self.upd_win = tk.Toplevel(self.root)
        self.upd_win.title("更新進度")
        x = self.root.winfo_x() - 50
        y = self.root.winfo_y() + 50
        self.upd_win.geometry(f"250x260+{x}+{y}")
        self.upd_win.attributes('-topmost', True)
        
        header_frame = tk.Frame(self.upd_win)
        header_frame.pack(pady=5)
        
        tk.Label(header_frame, text=f"{ctype} ", font=("Arial", 10, "bold")).grid(row=0, column=0)
        
        if is_other:
            lbl_cnum = tk.Label(header_frame, text=cur_div if cur_div else "(未填)", font=("Arial", 10, "bold", "underline"), fg="#3498db", cursor="hand2")
            lbl_cnum.grid(row=0, column=1)
            ent_cnum = tk.Entry(header_frame, width=8, font=("Arial", 10))
            ent_cnum.insert(0, cur_div)
        else:
            lbl_cnum = tk.Label(header_frame, text=cur_cnum if cur_cnum else "(未填)", font=("Arial", 10, "bold", "underline"), fg="#3498db", cursor="hand2")
            lbl_cnum.grid(row=0, column=1)
            ent_cnum = tk.Entry(header_frame, width=5, font=("Arial", 10))
            ent_cnum.insert(0, cur_cnum)
        
        tk.Label(header_frame, text=" (", font=("Arial", 10, "bold")).grid(row=0, column=2)
        lbl_date = tk.Label(header_frame, text=full_date, font=("Arial", 10, "bold", "underline"), fg="#3498db", cursor="hand2")
        lbl_date.grid(row=0, column=3)
        tk.Label(header_frame, text=")", font=("Arial", 10, "bold")).grid(row=0, column=4)
        
        ent_date = tk.Entry(header_frame, width=8, font=("Arial", 10))
        ent_date.insert(0, full_date)
        
        def on_date_double_click(e):
            lbl_date.grid_forget()
            ent_date.grid(row=0, column=3)
            ent_date.focus_set()
            
        def on_date_focus_out(e):
            ent_date.grid_forget()
            new_val = ent_date.get().strip()
            lbl_date.config(text=new_val if new_val else full_date)
            lbl_date.grid(row=0, column=3)

        lbl_date.bind("<Double-1>", on_date_double_click)
        ent_date.bind("<FocusOut>", on_date_focus_out)
        ent_date.bind("<Return>", on_date_focus_out)

        def on_cnum_double_click(e):
            lbl_cnum.grid_forget()
            ent_cnum.grid(row=0, column=1)
            ent_cnum.focus_set()
            
        def on_cnum_focus_out(e):
            ent_cnum.grid_forget()
            new_val = ent_cnum.get().strip()
            lbl_cnum.config(text=new_val if new_val else "(未填)")
            lbl_cnum.grid(row=0, column=1)
            
        lbl_cnum.bind("<Double-1>", on_cnum_double_click)
        ent_cnum.bind("<FocusOut>", on_cnum_focus_out)
        ent_cnum.bind("<Return>", on_cnum_focus_out)

        lbl_p_text = "題目範圍 (例 1-7):" if is_cpe else ("題目範圍 (例 1-4):" if is_lc else "題目範圍 (例 A-F):")
        tk.Label(self.upd_win, text=lbl_p_text, font=("Arial", 8)).pack()
        ent_probs = tk.Entry(self.upd_win, width=12)
        ent_probs.insert(0, cur_probs)
        ent_probs.pack()
        
        lbl_s_text = "賽中解出 (例 124):" if (is_lc or is_cpe) else "賽中解出 (例 ACD):"
        tk.Label(self.upd_win, text=lbl_s_text, font=("Arial", 8)).pack()
        ent_solved = tk.Entry(self.upd_win, width=12)
        ent_solved.insert(0, cur_solved)
        ent_solved.pack()
        
        chk_frame = tk.Frame(self.upd_win)
        chk_frame.pack(pady=5)
        
        chk_vars = {}
        
        def generate_boxes(*args):
            for widget in chk_frame.winfo_children():
                widget.destroy()
            chk_vars.clear()
            
            p_str = ent_probs.get().upper().replace("~", "-")
            s_str = ent_solved.get().upper().replace(" ", "").replace(",", "")
            
            all_probs = []
            if '-' in p_str:
                parts = p_str.split('-')
                if len(parts) == 2:
                    start, end = parts[0], parts[1]
                    if start.isdigit() and end.isdigit():
                        all_probs = [str(i) for i in range(int(start), int(end)+1)]
                    elif start.isalpha() and end.isalpha():
                        all_probs = [chr(i) for i in range(ord(start), ord(end)+1)]
            
            if not all_probs and p_str:
                all_probs = list(p_str)
                
            solved_list = list(s_str)
            missing = [p for p in all_probs if p not in solved_list]
            
            for p in missing:
                var = tk.BooleanVar(value=(p in cur_up_done))
                chk_vars[p] = var
                tk.Checkbutton(chk_frame, text=f"題 {p}", variable=var).pack(anchor="w")

        ent_probs.bind('<KeyRelease>', generate_boxes)
        ent_solved.bind('<KeyRelease>', generate_boxes)
        generate_boxes()
        
        def save_update():
            p_val = ent_probs.get().upper().replace("~", "-")
            s_val = ent_solved.get().upper().replace(" ", "").replace(",", "")
            u_val = "".join([p for p, var in chk_vars.items() if var.get()])
            new_date = ent_date.get().strip() 
            
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            
            if is_other:
                new_div = ent_cnum.get().strip()
                cursor.execute("UPDATE contests SET probs=?, solved=?, up_done=?, div=?, date=? WHERE id=?", 
                               (p_val, s_val, u_val, new_div, new_date, cid))
                if new_div:
                    cursor.execute("INSERT OR IGNORE INTO other_categories (name) VALUES (?)", (new_div,))
            else:
                new_cnum = ent_cnum.get().strip()
                cursor.execute("UPDATE contests SET probs=?, solved=?, up_done=?, c_num=?, date=? WHERE id=?", 
                               (p_val, s_val, u_val, new_cnum, new_date, cid))
                
            conn.commit()
            conn.close()
            self.refresh_stats()
            self.draw_calendar()
            self.upd_win.destroy()
            
        tk.Button(self.upd_win, text="儲存", command=save_update, bg="#2ecc71", fg="white").pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = CPTrackerApp(root)
    root.mainloop()