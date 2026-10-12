import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta

DB_FILE = 'cp_tracker.db'

class CPTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RC Tracker")
        
        try:
            import os
            if os.name == 'nt':
                import ctypes
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("my_cp_tracker_app")
            
            self.icon_image = tk.PhotoImage(file='./AWARD/mess/CheckIn_py/rc_icon.png')
            self.root.iconphoto(False, self.icon_image)
        except Exception:
            pass

        window_width = 460
        window_height = 430
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = screen_width - window_width - 10
        y = screen_height - window_height - 80 
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.plat_map = {'C++': 'cpp', '課業': 'school', '資安': 'sec', '專案': 'project', '英文': 'eng', '躲水裡': 'water'}
        
        self.init_db()
        
        self.timer_running = False
        self.total_seconds = 0
        self.remaining_seconds = self.total_seconds
        self.alerted_checkpoints = set()
        
        self.cpp_done = tk.BooleanVar(value=False)
        self.school_done = tk.BooleanVar(value=False)
        self.sec_done = tk.BooleanVar(value=False) 
        self.project_done = tk.BooleanVar(value=False)
        self.eng_done = tk.BooleanVar(value=False)
        self.water_done = tk.BooleanVar(value=False)
        
        self.week_offset = 0
        self.study_week_offset = 0
        self.upd_win = None
        self.checkin_popup = None
        self.popup_timer = None
        self.ignore_next_click = False 
        
        # 時間軸選取管理
        self.selected_timeline_cells = set() # 格式: (day_type, hour)
        self.timeline_labels = {}           # 保存標籤元件: (day_type, merge_id) -> widget
        self.last_rendered_hour = None
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=2)
        
        self.build_tab_daily()
        self.build_tab_calendar()
        self.build_tab_study()  
        self.build_tab_stats()

        self.check_cross_day()
        self.load_daily_status()
        self.poll_timeline_update()
        
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
        cursor.execute("INSERT OR IGNORE INTO app_config VALUES ('timeline_shift_date', '2000-01-01')")
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS study_plan
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT, date TEXT, content TEXT, urgency TEXT, status INTEGER DEFAULT 0)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS subjects (name TEXT PRIMARY KEY)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS other_categories (name TEXT PRIMARY KEY)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS hourly_schedule (
                          day_type TEXT, 
                          hour INTEGER, 
                          merge_id INTEGER, 
                          text TEXT, 
                          PRIMARY KEY(day_type, hour))''')

        try: cursor.execute("ALTER TABLE streaks ADD COLUMN prev_checkin DATE DEFAULT '2000-01-01'")
        except: pass
        try: cursor.execute("ALTER TABLE contests ADD COLUMN probs TEXT DEFAULT ''")
        except: pass
        try: cursor.execute("ALTER TABLE contests ADD COLUMN up_done TEXT DEFAULT ''")
        except: pass
        try: cursor.execute("ALTER TABLE contests ADD COLUMN c_num TEXT DEFAULT ''")
        except: pass
        try: cursor.execute("ALTER TABLE study_plan ADD COLUMN status INTEGER DEFAULT 0")
        except: pass
        
        try: cursor.execute("UPDATE study_plan SET urgency='可以放棄的白色' WHERE urgency='可以放棄的灰色'")
        except: pass
        
        tw_year = datetime.now().year - 1911
        try: cursor.execute(f"UPDATE contests SET date = '{tw_year}-' || date WHERE length(date) = 5")
        except: pass
            
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
            
            if sch_s[0] > cpp_s[0]:
                cursor.execute("UPDATE streaks SET current_streak=?, last_checkin=?, prev_checkin=? WHERE platform='C++'", 
                               (max(cpp_s[0], sch_s[0]), max(cpp_s[1], sch_s[1]), max(cpp_s[2], sch_s[2])))
                cursor.execute("UPDATE time_stats SET daily_time=?, total_time=?, last_date=? WHERE platform='C++'", 
                               (max(cpp_t[0], sch_t[0]), cpp_t[1] + sch_t[1], max(cpp_t[2], sch_t[2])))
                cursor.execute("UPDATE streaks SET current_streak=0, last_checkin='2000-01-01', prev_checkin='2000-01-01' WHERE platform='課業'")
                cursor.execute("UPDATE time_stats SET daily_time=0, total_time=0, last_date='2000-01-01' WHERE platform='課業'")

        for plat in ['C++', '課業', '資安', '專案', '英文', '躲水裡']:
            cursor.execute("INSERT OR IGNORE INTO streaks (platform, current_streak, last_checkin, prev_checkin) VALUES (?, 0, '2000-01-01', '2000-01-01')", (plat,))
            cursor.execute("INSERT OR IGNORE INTO time_stats VALUES (?, 0, 0, '2000-01-01')", (plat,))
                
        conn.commit()
        conn.close()

    def show_center_alert(self, title, message):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.attributes("-topmost", True)
        
        w, h = 300, 150
        sw = popup.winfo_screenwidth()
        sh = popup.winfo_screenheight()
        cx = int((sw - w) / 2)
        cy = int((sh - h) / 2)
        popup.geometry(f"{w}x{h}+{cx}+{cy}")
        popup.resizable(False, False)

        frame = tk.Frame(popup, padx=15, pady=15)
        frame.pack(expand=True, fill="both")

        lbl = tk.Label(frame, text=message, font=("Arial", 11, "bold"), fg="#e74c3c", wraplength=260)
        lbl.pack(expand=True, pady=(10, 15))

        btn = tk.Button(frame, text="我知道了", command=popup.destroy, bg="#3498db", fg="white", width=10, relief="groove")
        btn.pack()
        
        popup.grab_set()
        popup.focus_force()

    def build_tab_daily(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="日常打卡")

        self.time_label = tk.Label(tab, text="00:00:00", font=("Helvetica", 28, "bold"), fg="#e74c3c")
        self.time_label.pack(pady=1)
        
        ctrl_frame = tk.Frame(tab)
        ctrl_frame.pack(pady=0)
        
        tk.Label(ctrl_frame, text=" ", font=("Arial", 9)).pack(side=tk.LEFT, padx=2)
        self.combo_target = ttk.Combobox(ctrl_frame, values=["C++", "課業", "資安", "專案", "英文", "躲水裡"], width=5, state="readonly")
        self.combo_target.pack(side=tk.LEFT, padx=2)
        
        tk.Button(ctrl_frame, text="+1小時", command=lambda: self.add_timer(3600), font=("Arial", 8)).pack(side=tk.LEFT, padx=2)
        tk.Button(ctrl_frame, text="+15分", command=lambda: self.add_timer(900), font=("Arial", 8)).pack(side=tk.LEFT, padx=2)
        tk.Button(ctrl_frame, text="+5分", command=lambda: self.add_timer(300), font=("Arial", 8)).pack(side=tk.LEFT, padx=2)
        
        tk.Button(ctrl_frame, text="開始", command=self.start_timer, bg="#2ecc71", fg="white", width=4).pack(side=tk.LEFT, padx=2)
        tk.Button(ctrl_frame, text="暫停", command=self.stop_timer, bg="#f39c12", fg="white", width=4).pack(side=tk.LEFT, padx=2)
        tk.Button(ctrl_frame, text="重置", command=self.reset_timer, bg="#34495e", fg="white", width=4).pack(side=tk.LEFT, padx=2)

        main_content = tk.Frame(tab)
        main_content.pack(fill="both", expand=True, padx=10, pady=2)

        check_frame = tk.LabelFrame(main_content, text="今日任務", font=("Arial", 9))
        check_frame.pack(side=tk.LEFT, fill="y", padx=(0, 10), pady=2)

        self.lbl_cpp_streak = tk.Label(check_frame, text="C++ cnt: 0 | 0.0 hr", font=("Arial", 9))
        self.lbl_cpp_streak.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.lbl_cpp_streak.bind('<Double-1>', lambda e: self.show_last_checkin(e, 'C++'))
        tk.Checkbutton(check_frame, text="", variable=self.cpp_done, command=lambda: self.handle_checkin('C++')).grid(row=0, column=1, sticky="w")

        self.lbl_school_streak = tk.Label(check_frame, text="課業 cnt: 0 | 0.0 hr", font=("Arial", 9))
        self.lbl_school_streak.grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.lbl_school_streak.bind('<Double-1>', lambda e: self.show_last_checkin(e, '課業'))
        tk.Checkbutton(check_frame, text="", variable=self.school_done, command=lambda: self.handle_checkin('課業')).grid(row=1, column=1, sticky="w")

        self.lbl_sec_streak = tk.Label(check_frame, text="資安 cnt: 0 | 0.0 hr", font=("Arial", 9))
        self.lbl_sec_streak.grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.lbl_sec_streak.bind('<Double-1>', lambda e: self.show_last_checkin(e, '資安'))
        tk.Checkbutton(check_frame, text="", variable=self.sec_done, command=lambda: self.handle_checkin('資安')).grid(row=2, column=1, sticky="w")
        
        self.lbl_project_streak = tk.Label(check_frame, text="專案 cnt: 0 | 0.0 hr", font=("Arial", 9))
        self.lbl_project_streak.grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.lbl_project_streak.bind('<Double-1>', lambda e: self.show_last_checkin(e, '專案'))
        tk.Checkbutton(check_frame, text="", variable=self.project_done, command=lambda: self.handle_checkin('專案')).grid(row=3, column=1, sticky="w")

        self.lbl_eng_streak = tk.Label(check_frame, text="英文 cnt: 0 | 0.0 hr", font=("Arial", 9))
        self.lbl_eng_streak.grid(row=4, column=0, sticky="w", padx=5, pady=2)
        self.lbl_eng_streak.bind('<Double-1>', lambda e: self.show_last_checkin(e, '英文'))
        tk.Checkbutton(check_frame, text="", variable=self.eng_done, command=lambda: self.handle_checkin('英文')).grid(row=4, column=1, sticky="w")
        
        self.lbl_water_streak = tk.Label(check_frame, text="躲水裡 cnt: 0 | 0.0 hr", font=("Arial", 9))
        self.lbl_water_streak.grid(row=5, column=0, sticky="w", padx=5, pady=2)
        self.lbl_water_streak.bind('<Double-1>', lambda e: self.show_last_checkin(e, '躲水裡'))
        tk.Checkbutton(check_frame, text="", variable=self.water_done, command=lambda: self.handle_checkin('躲水裡')).grid(row=5, column=1, sticky="w")

        self.timeline_frame = tk.LabelFrame(main_content, text="當下與明日安排 (單擊編輯 | Ctrl+單擊多選合併)", font=("Arial", 8))
        self.timeline_frame.pack(side=tk.LEFT, fill="both", expand=True, pady=2)

        action_bar = tk.Frame(self.timeline_frame)
        action_bar.pack(fill="x", padx=5, pady=1)
        tk.Button(action_bar, text="合併選取", font=("Arial", 8), command=self.merge_selected_timeline).pack(side=tk.LEFT, padx=2)
        tk.Button(action_bar, text="取消合併", font=("Arial", 8), command=self.unmerge_selected_timeline).pack(side=tk.LEFT, padx=2)

        self.timeline_grid_frame = tk.Frame(self.timeline_frame)
        self.timeline_grid_frame.pack(fill="both", expand=True, padx=2, pady=1)

        bottom_frame = tk.Frame(tab)
        bottom_frame.pack(fill="x", side=tk.BOTTOM, pady=2, padx=10)
        
        self.lbl_total_days = tk.Label(bottom_frame, text="🔥 總累積修煉: 0 天", font=("Arial", 10, "bold"), fg="#2980b9")
        self.lbl_total_days.pack(side=tk.LEFT)
        
        btn_info = tk.Button(bottom_frame, text=" ℹ ", font=("Arial", 10, "bold"), relief="flat", fg="gray", cursor="hand2", command=self.show_guide)
        btn_info.pack(side=tk.RIGHT)

        self.render_hourly_timeline()

    # --- 時間軸機制 ---
    def poll_timeline_update(self):
        self.check_night_shift()
        now_h = datetime.now().hour
        if self.last_rendered_hour != now_h:
            self.render_hourly_timeline()
        self.root.after(30000, self.poll_timeline_update)

    def check_night_shift(self):
        now = datetime.now()
        today = now.strftime('%Y-%m-%d')
        
        if now.hour >= 22:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM app_config WHERE key='timeline_shift_date'")
            row = cursor.fetchone()
            last_shift = row[0] if row else '2000-01-01'
            
            if last_shift != today:
                cursor.execute("DELETE FROM hourly_schedule WHERE day_type='today'")
                cursor.execute("UPDATE hourly_schedule SET day_type='today' WHERE day_type='tomorrow'")
                cursor.execute("INSERT OR REPLACE INTO app_config (key, value) VALUES ('timeline_shift_date', ?)", (today,))
                conn.commit()
                conn.close()
                self.render_hourly_timeline()
            else:
                conn.close()

    def render_hourly_timeline(self):
        for widget in self.timeline_grid_frame.winfo_children():
            widget.destroy()

        self.timeline_labels.clear()
        self.selected_timeline_cells.clear()
        
        now = datetime.now()
        cur_h = now.hour
        self.last_rendered_hour = cur_h

        today_hours = [h for h in range(cur_h, 23)] if cur_h < 23 else []
        tomorrow_hours = [h for h in range(6, 23)]

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT day_type, hour, merge_id, text FROM hourly_schedule")
        sched_data = {}
        for dt, h, mid, txt in cursor.fetchall():
            sched_data[(dt, h)] = (mid if mid is not None else h, txt or "")
        conn.close()

        canvas = tk.Canvas(self.timeline_grid_frame, highlightthickness=0, height=210)
        scrollbar = ttk.Scrollbar(self.timeline_grid_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        def _on_frame_configure(e):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scrollable_frame.bind("<Configure>", _on_frame_configure)
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        def _on_canvas_configure(e):
            canvas.itemconfig(canvas_window, width=e.width)

        canvas.bind("<Configure>", _on_canvas_configure)
        canvas.configure(yscrollcommand=scrollbar.set)

        def _on_mousewheel(event):
            if getattr(event, 'delta', 0) != 0:
                direction = -1 if event.delta > 0 else 1
                canvas.yview_scroll(direction, "units")
            elif getattr(event, 'num', 0) in (4, 5):
                direction = -1 if event.num == 4 else 1
                canvas.yview_scroll(direction, "units")

        def _bind_mouse(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            canvas.bind_all("<Button-4>", _on_mousewheel)
            canvas.bind_all("<Button-5>", _on_mousewheel)

        def _unbind_mouse(event):
            canvas.unbind_all("<MouseWheel>")
            canvas.unbind_all("<Button-4>")
            canvas.unbind_all("<Button-5>")

        canvas.bind("<Enter>", _bind_mouse)
        canvas.bind("<Leave>", _unbind_mouse)

        canvas.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        scrollable_frame.columnconfigure(1, weight=1)
        scrollable_frame.columnconfigure(4, weight=1)

        self._build_col(scrollable_frame, "今日剩餘", "today", today_hours, sched_data, 0)
        ttk.Separator(scrollable_frame, orient='vertical').grid(row=0, column=2, rowspan=30, sticky='ns', padx=6)
        self._build_col(scrollable_frame, "明日計畫", "tomorrow", tomorrow_hours, sched_data, 3)

    def _build_col(self, parent, title, day_type, hours, sched_data, col_offset):
        tk.Label(parent, text=title, font=("Arial", 9, "bold"), fg="#2c3e50").grid(row=0, column=col_offset, columnspan=2, pady=(0, 4))
        if not hours:
            msg = "時段已過22:00" if datetime.now().hour >= 22 else "今日時段已過完"
            tk.Label(parent, text=msg, font=("Arial", 8), fg="gray").grid(row=1, column=col_offset, columnspan=2)
            return

        groups = []
        cur_mid = None
        cur_group = []
        for h in hours:
            mid, txt = sched_data.get((day_type, h), (h, ""))
            if cur_mid is None:
                cur_mid = mid
                cur_group = [(h, txt)]
            elif mid == cur_mid:
                cur_group.append((h, txt))
            else:
                groups.append((cur_mid, cur_group))
                cur_mid = mid
                cur_group = [(h, txt)]
        if cur_group:
            groups.append((cur_mid, cur_group))

        row_idx = 1
        for mid, grp in groups:
            h_start = grp[0][0]
            h_end = grp[-1][0]
            txt = grp[0][1]

            label_str = f"{h_start:02d}:00" if h_start == h_end else f"{h_start:02d}~{h_end+1:02d}"

            time_lbl = tk.Label(parent, text=label_str, font=("Arial", 8), width=6, anchor="e", padx=2)
            time_lbl.grid(row=row_idx, column=col_offset, sticky="ns", pady=1)

            disp_text = txt if txt else ""
            content_lbl = tk.Label(parent, text=disp_text, font=("Arial", 8), bg="#e0e0e0", fg="#2c3e50",
                                   relief="solid", borderwidth=0, anchor="w", padx=3, height=1, width=14)
            content_lbl.grid(row=row_idx, column=col_offset+1, sticky="w", pady=1, padx=(0, 4))

            content_lbl.bind("<Button-1>", lambda e, dt=day_type, m=mid, l=content_lbl, p=parent, r=row_idx, c=col_offset+1: 
                             self.start_edit_cell(e, dt, m, l, p, r, c))

            for (h, _) in grp:
                time_lbl.bind("<Control-Button-1>", lambda e, dt=day_type, hr=h, l=time_lbl: self.toggle_cell_select(dt, hr, l))
                content_lbl.bind("<Control-Button-1>", lambda e, dt=day_type, hr=h, l=time_lbl: self.toggle_cell_select(dt, hr, l))

            self.timeline_labels[(day_type, mid)] = content_lbl
            row_idx += 1

    def start_edit_cell(self, event, day_type, merge_id, label_widget, parent, row, col):
        current_text = label_widget.cget("text")
        label_widget.grid_remove()

        entry = tk.Entry(parent, font=("Arial", 8), width=14, bg="#ffffff")
        entry.insert(0, current_text)
        entry.grid(row=row, column=col, sticky="w", pady=1, padx=(0, 4))
        entry.focus_set()

        def _finish_edit(e=None):
            val = entry.get().strip()
            entry.destroy()
            label_widget.config(text=val)
            label_widget.grid()
            
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            
            cursor.execute("SELECT hour FROM hourly_schedule WHERE day_type=? AND merge_id=?", (day_type, merge_id))
            rows = cursor.fetchall()

            if rows:
                cursor.execute("UPDATE hourly_schedule SET text=? WHERE day_type=? AND merge_id=?", (val, day_type, merge_id))
            else:
                cursor.execute('''INSERT INTO hourly_schedule (day_type, hour, merge_id, text)
                                  VALUES (?, ?, ?, ?)
                                  ON CONFLICT(day_type, hour) DO UPDATE SET text=excluded.text, merge_id=excluded.merge_id''',
                               (day_type, merge_id, merge_id, val))
                
            conn.commit()
            conn.close()

        entry.bind("<FocusOut>", _finish_edit)
        entry.bind("<Return>", _finish_edit)

    def toggle_cell_select(self, day_type, hour, label_widget):
        item = (day_type, hour)
        if item in self.selected_timeline_cells:
            self.selected_timeline_cells.remove(item)
            label_widget.config(bg=self.root.cget('bg'), fg='black')
        else:
            self.selected_timeline_cells.add(item)
            label_widget.config(bg="#3498db", fg="white")

    def merge_selected_timeline(self):
        if len(self.selected_timeline_cells) < 2:
            return

        days = {d for d, h in self.selected_timeline_cells}
        if len(days) > 1:
            messagebox.showwarning("警告", "無法跨天合併時段！")
            return

        day_type = list(days)[0]
        hours = sorted([h for d, h in self.selected_timeline_cells])

        for i in range(len(hours) - 1):
            if hours[i+1] != hours[i] + 1:
                messagebox.showwarning("警告", "選取的小時必須連續才能合併！")
                return

        new_mid = hours[0]
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT text FROM hourly_schedule WHERE day_type=? AND hour=?", (day_type, new_mid))
        row = cursor.fetchone()
        orig_text = row[0] if row else ""

        for h in hours:
            cursor.execute('''INSERT INTO hourly_schedule (day_type, hour, merge_id, text)
                              VALUES (?, ?, ?, ?)
                              ON CONFLICT(day_type, hour) DO UPDATE SET merge_id=?, text=?''',
                           (day_type, h, new_mid, orig_text, new_mid, orig_text))

        conn.commit()
        conn.close()
        self.render_hourly_timeline()

    def unmerge_selected_timeline(self):
        if not self.selected_timeline_cells:
            return

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        for day_type, h in self.selected_timeline_cells:
            cursor.execute("UPDATE hourly_schedule SET merge_id=? WHERE day_type=? AND hour=?", (h, day_type, h))
        conn.commit()
        conn.close()
        self.render_hourly_timeline()

    # --- 輔助選單/分類管理 ---
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

    # --- 賽事行事曆 ---
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

        paned_window = ttk.PanedWindow(tab, orient=tk.VERTICAL)
        paned_window.pack(fill="both", expand=True, padx=5, pady=2)

        canvas_frame = tk.Frame(paned_window)
        
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
        
        paned_window.add(canvas_frame, weight=3)

        del_frame = tk.Frame(paned_window)

        contest_cols = ('ID', '日期', '時間', '賽事', '編號', '分類')
        contest_disp = ('日期', '時間', '賽事', '編號', '分類')
        self.tree_contests = ttk.Treeview(del_frame, columns=contest_cols, displaycolumns=contest_disp, show='headings', height=2)

        c_widths = {'日期': 50, '時間': 50, '賽事': 45, '編號': 55, '分類': 100}
        for c in contest_disp:
            self.tree_contests.heading(c, text=c)
            self.tree_contests.column(c, width=c_widths.get(c, 50), anchor='center' if c != '分類' else 'w')

        c_scroll = ttk.Scrollbar(del_frame, orient="vertical", command=self.tree_contests.yview)
        self.tree_contests.configure(yscrollcommand=c_scroll.set)

        self.tree_contests.pack(side=tk.LEFT, fill="both", expand=True)
        c_scroll.pack(side=tk.LEFT, fill="y")
        tk.Button(del_frame, text="刪除", command=self.delete_contest, bg="#e74c3c", fg="white", width=4).pack(side=tk.RIGHT, padx=3, fill='y')

        self.tree_contests.bind('<Double-1>', self.on_contest_tree_double_click)

        paned_window.add(del_frame, weight=1)

        self.draw_calendar()

    def on_contest_tree_double_click(self, event):
        region = self.tree_contests.identify_region(event.x, event.y)
        if region != "cell":
            return
            
        row_id = self.tree_contests.identify_row(event.y)
        col_id = self.tree_contests.identify_column(event.x)
        if not row_id or not col_id:
            return

        col_idx = int(col_id.replace('#', '')) - 1
        disp_cols = ('日期', '時間', '賽事', '編號', '分類')
        if col_idx >= len(disp_cols):
            return
        field_name = disp_cols[col_idx]

        item_vals = self.tree_contests.item(row_id, 'values')
        if not item_vals:
            return

        cid = item_vals[0]
        cur_val = item_vals[col_idx + 1]

        x, y, w, h = self.tree_contests.bbox(row_id, col_id)

        if field_name == "賽事":
            edit_widget = ttk.Combobox(self.tree_contests, values=["CF", "LC", "CPE", "Other"], state="readonly", font=("Arial", 8))
            edit_widget.set(cur_val)
        else:
            edit_widget = tk.Entry(self.tree_contests, font=("Arial", 8))
            edit_widget.insert(0, cur_val)

        edit_widget.place(x=x, y=y, width=w, height=h)
        edit_widget.focus_set()

        def _save_contest_cell(e=None):
            new_val = edit_widget.get().strip()
            edit_widget.destroy()

            if new_val == cur_val:
                return

            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()

            if field_name == '日期':
                tw_year = datetime.now().year - 1911
                if len(new_val) == 4 and new_val.isdigit():
                    cdate = f"{tw_year}-{new_val[:2]}-{new_val[2:]}"
                elif len(new_val) == 5 and '-' in new_val:
                    cdate = f"{tw_year}-{new_val}"
                elif len(new_val) >= 8 and '-' in new_val:
                    cdate = new_val
                else:
                    messagebox.showerror("錯誤", "日期格式錯誤 (請輸入 MMDD，例: 0718)")
                    conn.close()
                    return
                cursor.execute("UPDATE contests SET date=? WHERE id=?", (cdate, cid))
            elif field_name == '時間':
                if len(new_val) == 4 and new_val.isdigit():
                    ctime = f"{new_val[:2]}:{new_val[2:]}"
                elif len(new_val) == 5 and ':' in new_val:
                    ctime = new_val
                elif new_val == "":
                    ctime = "00:00"
                else:
                    messagebox.showerror("錯誤", "時間格式錯誤 (請輸入 HHMM，例: 2235)")
                    conn.close()
                    return
                cursor.execute("UPDATE contests SET time=? WHERE id=?", (ctime, cid))
            elif field_name == '賽事':
                cursor.execute("UPDATE contests SET type=? WHERE id=?", (new_val, cid))
            elif field_name == '編號':
                cursor.execute("UPDATE contests SET c_num=? WHERE id=?", (new_val, cid))
            elif field_name == '分類':
                cursor.execute("UPDATE contests SET div=? WHERE id=?", (new_val, cid))
                cursor.execute("SELECT type FROM contests WHERE id=?", (cid,))
                ctype_row = cursor.fetchone()
                if ctype_row and ctype_row[0] == "Other" and new_val:
                    cursor.execute("INSERT OR IGNORE INTO other_categories (name) VALUES (?)", (new_val,))
                    self.load_other_categories()

            conn.commit()
            conn.close()
            self.draw_calendar()
            self.refresh_stats()

        edit_widget.bind("<Return>", _save_contest_cell)
        edit_widget.bind("<FocusOut>", _save_contest_cell)
        if field_name == "賽事":
            edit_widget.bind("<<ComboboxSelected>>", _save_contest_cell)

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
        else:
            self.lbl_div_type.config(text="Div:")
            self.lbl_div_type.grid(row=1, column=0, sticky="e")
            self.entry_div.grid(row=1, column=1, padx=2, pady=2)
            self.lbl_cnum.config(text="編號(4碼):")
            self.lbl_cnum.grid(row=1, column=2, sticky="e")
            self.entry_cnum.config(state="normal")
            self.entry_cnum.grid(row=1, column=3, padx=2)

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
        else:
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
        selected = self.tree_contests.selection()
        if not selected: return
        item_vals = self.tree_contests.item(selected[0], 'values')
        if not item_vals: return
        cid = item_vals[0]
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contests WHERE id=?", (cid,))
        conn.commit()
        conn.close()
        self.draw_calendar()
        self.refresh_stats()

    def draw_calendar(self):
        self.canvas.delete("all")
        for r in self.tree_contests.get_children():
            self.tree_contests.delete(r)
        
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
            cid = c[0]
            c_type = c[1]
            disp_date = c[2][-5:]
            ctime = c[3] or "00:00"
            c_div = c[4] or ""
            c_num = c[9] if len(c) > 9 else ""
            self.tree_contests.insert("", "end", values=(cid, disp_date, ctime, c_type, c_num, c_div))
                
        self.canvas.yview_moveto(0) 
        bbox = self.canvas.bbox("all")
        if bbox:
            self.canvas.config(scrollregion=(0, 0, bbox[2], max(90, bbox[3] + 10)))

    def change_week(self, delta):
        self.week_offset += delta
        self.draw_calendar()
        
    def reset_week_view(self, event=None):
        if self.week_offset != 0:
            self.week_offset = 0
            self.draw_calendar()

    # --- 課業安排 ---
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
        self.combo_urgency = ttk.Combobox(input_frame, values=["紅色緊急", "淺藍色不緊急", "可以放棄的白色"], width=13, state="readonly")
        self.combo_urgency.set("紅色緊急")
        self.combo_urgency.grid(row=1, column=4, padx=2)

        nav_frame = tk.Frame(tab)
        nav_frame.pack(fill="x", pady=0)
        tk.Button(nav_frame, text="◀", command=lambda: self.change_study_week(-1)).pack(side=tk.LEFT, padx=10)
        self.lbl_study_week = tk.Label(nav_frame, text="本週", font=("Arial", 9, "bold"), cursor="hand2")
        self.lbl_study_week.pack(side=tk.LEFT, expand=True)
        self.lbl_study_week.bind("<Button-1>", self.reset_study_week_view)
        tk.Button(nav_frame, text="▶", command=lambda: self.change_study_week(1)).pack(side=tk.RIGHT, padx=10)

        paned_window = ttk.PanedWindow(tab, orient=tk.VERTICAL)
        paned_window.pack(fill="both", expand=True, padx=5, pady=2)

        canvas_frame = tk.Frame(paned_window)
        self.study_canvas_scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical")
        self.study_canvas_scrollbar.pack(side=tk.RIGHT, fill="y")
        self.study_canvas = tk.Canvas(canvas_frame, height=110, bg="#1e1e1e", highlightthickness=0, yscrollcommand=self.study_canvas_scrollbar.set)
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
        self.study_canvas.tag_bind("study_item", "<Double-1>", self.on_study_item_double_click)

        paned_window.add(canvas_frame, weight=1)

        tree_container = tk.Frame(paned_window)
        
        study_cols = ('ID', '日期', '科目', '內容', '急迫性')
        study_disp = ('日期', '科目', '內容', '急迫性')
        self.tree_study = ttk.Treeview(tree_container, columns=study_cols, displaycolumns=study_disp, show='headings', height=4)
        
        col_widths = {'日期': 55, '科目': 75, '內容': 160, '急迫性': 90}
        for c in study_disp:
            self.tree_study.heading(c, text=c)
            self.tree_study.column(c, width=col_widths.get(c, 70), anchor='center' if c in ('日期', '急迫性') else 'w')
            
        tree_scroll = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree_study.yview)
        self.tree_study.configure(yscrollcommand=tree_scroll.set)
        
        self.tree_study.pack(side=tk.LEFT, fill="both", expand=True)
        tree_scroll.pack(side=tk.LEFT, fill="y")
        
        tk.Button(tree_container, text="刪除", command=self.delete_study_plan, bg="#e74c3c", fg="white", width=4).pack(side=tk.RIGHT, padx=3, fill='y')
        
        self.tree_study.bind('<Double-1>', self.on_study_tree_double_click)

        paned_window.add(tree_container, weight=1)
        self.draw_study_calendar()

    def on_study_tree_double_click(self, event):
        region = self.tree_study.identify_region(event.x, event.y)
        if region != "cell":
            return
            
        row_id = self.tree_study.identify_row(event.y)
        col_id = self.tree_study.identify_column(event.x)
        if not row_id or not col_id:
            return
            
        col_idx = int(col_id.replace('#', '')) - 1
        disp_cols = ('日期', '科目', '內容', '急迫性')
        if col_idx >= len(disp_cols):
            return
        field_name = disp_cols[col_idx]
        
        item_vals = self.tree_study.item(row_id, 'values')
        if not item_vals:
            return
            
        plan_id = item_vals[0]
        cur_val = item_vals[col_idx + 1]
        
        x, y, w, h = self.tree_study.bbox(row_id, col_id)
        
        if field_name == "急迫性":
            edit_widget = ttk.Combobox(self.tree_study, values=["紅色緊急", "淺藍色不緊急", "可以放棄的白色"], state="readonly", font=("Arial", 8))
            edit_widget.set(cur_val)
        else:
            edit_widget = tk.Entry(self.tree_study, font=("Arial", 8))
            edit_widget.insert(0, cur_val)
            
        edit_widget.place(x=x, y=y, width=w, height=h)
        edit_widget.focus_set()
        
        def _save_study_cell(e=None):
            new_val = edit_widget.get().strip()
            edit_widget.destroy()
            
            if not new_val or new_val == cur_val:
                return
                
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            
            if field_name == '日期':
                tw_year = datetime.now().year - 1911
                if len(new_val) == 4 and new_val.isdigit():
                    sdate = f"{tw_year}-{new_val[:2]}-{new_val[2:]}"
                elif len(new_val) == 5 and '-' in new_val:
                    sdate = f"{tw_year}-{new_val}"
                elif len(new_val) >= 8 and '-' in new_val:
                    sdate = new_val
                else:
                    messagebox.showerror("錯誤", "日期格式錯誤 (請輸入 MMDD，例: 0718)")
                    conn.close()
                    return
                cursor.execute("UPDATE study_plan SET date=? WHERE id=?", (sdate, plan_id))
            elif field_name == '科目':
                cursor.execute("UPDATE study_plan SET subject=? WHERE id=?", (new_val, plan_id))
                cursor.execute("INSERT OR IGNORE INTO subjects (name) VALUES (?)", (new_val,))
                self.load_subjects()
            elif field_name == '內容':
                cursor.execute("UPDATE study_plan SET content=? WHERE id=?", (new_val, plan_id))
            elif field_name == '急迫性':
                cursor.execute("UPDATE study_plan SET urgency=? WHERE id=?", (new_val, plan_id))
                
            conn.commit()
            conn.close()
            self.draw_study_calendar()
            
        edit_widget.bind("<Return>", _save_study_cell)
        edit_widget.bind("<FocusOut>", _save_study_cell)
        if field_name == "急迫性":
            edit_widget.bind("<<ComboboxSelected>>", _save_study_cell)

    def draw_study_calendar(self):
        self.study_canvas.delete("all")
        for r in self.tree_study.get_children():
            self.tree_study.delete(r)

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM study_plan ORDER BY date DESC")
        plans = cursor.fetchall()
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
                        
                    self.study_canvas.create_rectangle(x_center-col_width/2+2, y_offset, x_center+col_width/2-2, y_offset+28, fill="#2f3542", outline=box_col)
                    self.study_canvas.create_text(x_center, y_offset+14, text=text_disp, fill=box_col, font=("Arial", 7, "bold"), justify="center")
                    y_offset += 32

            day_plans = [p for p in plans if p[2][-5:] == day_str]
            def plan_priority(p):
                status = p[5] if len(p) > 5 else 0
                u = p[4]
                u_score = 0 if u == "紅色緊急" else (2 if u == "可以放棄的白色" else 1)
                return (status, u_score)
                
            day_plans.sort(key=plan_priority)

            for p in day_plans:
                u = p[4]
                status = p[5] if len(p) > 5 else 0
                if status == 1:
                    box_col = "#7f8fa6" 
                else:
                    if u == "紅色緊急": box_col = "#e74c3c"
                    elif u == "可以放棄的白色": box_col = "#ffffff"
                    else: box_col = "#3498db"

                subj_disp = p[1][:4]
                cont_disp = p[3][:4]
                text_disp = f"{subj_disp}\n{cont_disp}"

                self.study_canvas.create_rectangle(x_center-col_width/2+2, y_offset, x_center+col_width/2-2, y_offset+30, fill="#2f3542", outline=box_col, tags=("study_item", f"plan_{p[0]}"))
                self.study_canvas.create_text(x_center, y_offset+15, text=text_disp, fill=box_col, font=("", 8, ""), justify="center", tags=("study_item", f"plan_{p[0]}"))
                y_offset += 32

        for p in plans:
            status = p[5] if len(p) > 5 else 0
            if status != 1:
                disp_date = p[2][-5:]
                self.tree_study.insert("", "end", values=(p[0], disp_date, p[1], p[3], p[4]))

        self.study_canvas.yview_moveto(0)
        bbox = self.study_canvas.bbox("all")
        if bbox:
            self.study_canvas.config(scrollregion=(0, 0, bbox[2], max(90, bbox[3] + 10)))

    def on_study_item_double_click(self, event):
        item = self.study_canvas.find_withtag("current")
        if not item: return
        tags = self.study_canvas.gettags(item[0])
        plan_id = None
        for t in tags:
            if t.startswith("plan_"):
                plan_id = t.split("_")[1]
                break
        
        if plan_id:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT status FROM study_plan WHERE id=?", (plan_id,))
            row = cursor.fetchone()
            if row:
                new_status = 1 if row[0] == 0 else 0
                cursor.execute("UPDATE study_plan SET status=? WHERE id=?", (new_status, plan_id))
                conn.commit()
            conn.close()
            self.draw_study_calendar()

    def delete_study_plan(self):
        selected = self.tree_study.selection()
        if not selected: return
        item_vals = self.tree_study.item(selected[0], 'values')
        if not item_vals: return
        sid = item_vals[0]
        
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
        cursor.execute("INSERT INTO study_plan (subject, date, content, urgency, status) VALUES (?, ?, ?, ?, 0)", (subj, sdate, content, urgency))
        conn.commit()
        conn.close()

        self.entry_s_date.delete(0, 'end')
        self.entry_s_content.delete(0, 'end')
        self.load_subjects()
        self.draw_study_calendar()

    # --- 戰力與補題 ---
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

    def refresh_stats(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        for plat in ['C++', '課業', '資安', '專案', '英文', '躲水裡']:
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
                
                if missing: unsolved_str = "".join(missing)
                else: unsolved_str = "✔"

            disp_row = (c_id, event_str, c_date[-5:], c_probs or '-', sol_cnt or '-', unsolved_str)
            self.tree.insert("", "end", values=disp_row)
            
            tot_solved += sol_cnt
            tot_up += up_cnt
            
        self.tree.tag_configure('sep', background='#dcdde1')
        self.lbl_stats.config(text=f"🏆 CF {cf_cnt} | LC {lc_cnt} | CPE {cpe_cnt} | 另 {other_cnt}\n🔥 解出: {tot_solved} 項 | 🛠️ 賽後補題: {tot_up} 題")
        conn.close()

    def add_timer(self, seconds):
        self.total_seconds += seconds
        self.remaining_seconds += seconds
        self.alerted_checkpoints = {cp for cp in self.alerted_checkpoints if self.remaining_seconds < cp}
        mins, secs = divmod(self.remaining_seconds, 60)
        hours, mins = divmod(mins, 60)
        self.time_label.config(text=f"{hours:02d}:{mins:02d}:{secs:02d}")

    def reset_timer(self):
        self.timer_running = False
        self.total_seconds = 0
        self.remaining_seconds = self.total_seconds
        self.alerted_checkpoints.clear()
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
            
            if self.remaining_seconds == 900 and 900 not in self.alerted_checkpoints:
                self.alerted_checkpoints.add(900)
                self.show_center_alert("時間提醒", "⏰ 倒數剩餘 15 分鐘！")

            elif self.remaining_seconds == 300 and 300 not in self.alerted_checkpoints:
                self.alerted_checkpoints.add(300)
                self.show_center_alert("時間提醒", "⚠️ 倒數剩餘 5 分鐘！")

            elapsed = self.total_seconds - self.remaining_seconds
            if elapsed > 0 and elapsed % 60 == 0:
                self.record_time()

            self.remaining_seconds -= 1
            self.root.after(1000, self.update_timer)
        elif self.remaining_seconds <= 0:
            self.time_label.config(text="00:00:00")
            self.timer_running = False
            self.record_time()
            if 0 not in self.alerted_checkpoints:
                self.alerted_checkpoints.add(0)
                self.show_center_alert("計時結束", "🔔 倒數結束！請記得休息或打卡。")

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
                
        any_checked = self.cpp_done.get() or self.school_done.get() or self.sec_done.get() or self.project_done.get() or self.eng_done.get() or self.water_done.get()
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
        for plat in ['C++', '課業', '資安', '專案', '英文', '躲水裡']:
            cursor.execute("SELECT last_checkin FROM streaks WHERE platform=?", (plat,))
            if cursor.fetchone()[0] == today:
                getattr(self, f"{self.plat_map[plat]}_done").set(True)
                
        cursor.execute("SELECT id FROM contests WHERE type='CF' AND date=?", (today_tw,))
        if cursor.fetchone() and not self.cpp_done.get():
            self.cpp_done.set(True)
            self.handle_checkin('C++') 
            
        conn.close()
        self.update_target_default()

    def show_guide(self):
        guide_text = (
            "🏆 【每日指南】\n\n"
            "🔴 Part 1: C++\n"
            "• 解題、看 Tutorial。\n\n"
            "🔵 Part 2: 課業\n"
            "• 讀書與整理。\n"
            "• 課業與賽事條列處：支援上下拖拉分隔與雙擊獨立修改！\n\n"
            "📅 賽事與自動化\n"
            "• Other 類別可以自訂賽事/任務分類，並單獨篩選！\n"
            "• 雙擊戰力補題頁面比賽，可深入勾選各題進度！\n\n"
            "(本地 db 好耶!\n"
            "SINCE 115/07/16 RC"
        )
        messagebox.showinfo("每日生存證明", guide_text)

    def update_target_default(self):
        cpp = self.cpp_done.get()
        school = self.school_done.get()
        sec = self.sec_done.get()
        project = self.project_done.get()
        eng = self.eng_done.get()
        water = self.water_done.get()
        
        if not cpp: self.combo_target.set("C++")
        elif not school: self.combo_target.set("課業")
        elif not sec: self.combo_target.set("資安")
        elif not project: self.combo_target.set("專案") 
        elif not eng: self.combo_target.set("英文")
        else: self.combo_target.set("躲水裡")

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
            self.eng_done.set(False)
            self.water_done.set(False)
            
            cursor.execute("SELECT value FROM app_config WHERE key='timeline_shift_date'")
            row = cursor.fetchone()
            last_shift = row[0] if row else '2000-01-01'
            if last_shift != today:
                cursor.execute("DELETE FROM hourly_schedule WHERE day_type='today'")
                cursor.execute("UPDATE hourly_schedule SET day_type='today' WHERE day_type='tomorrow'")
                cursor.execute("INSERT OR REPLACE INTO app_config (key, value) VALUES ('timeline_shift_date', ?)", (today,))

            cursor.execute("UPDATE app_config SET value=? WHERE key='last_startup'", (today,))
            conn.commit()
            
            self.update_target_default()
            self.refresh_stats()
            self.render_hourly_timeline()
            
        conn.close()
        self.check_night_shift()
        self.root.after(60000, self.check_cross_day)

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
        prev_date = (prev_checkin if prev_checkin != '2000-01-01' else "無") if last_checkin == today else (last_checkin if last_checkin != '2000-01-01' else "無")
            
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
            try: self.checkin_popup.destroy()
            except Exception: pass
            self.checkin_popup = None
            
    def close_popup_on_click(self, event):
        if getattr(self, 'ignore_next_click', False): return
        if getattr(self, 'checkin_popup', None) and self.checkin_popup.winfo_exists():
            try:
                if event.widget == self.checkin_popup or event.widget.master == self.checkin_popup:
                    return
            except Exception: pass
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