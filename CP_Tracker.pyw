from datetime import datetime, timedelta
import os
import json                      # ★ 新增：懸浮畫筆用來把線條轉成文字存檔
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

DB_FILE = 'cp_tracker.db'


# ============================================================
# ★ 新增：懸浮畫筆（共用主程式的 root，資料存在同一個資料庫）
# ============================================================
DRAW_KEY = "#010203"   # 這個顏色會被當成「透明」
DRAW_COLORS = ["#ff3b30", "#007aff", "#ffcc00", "#34c759", "#ffffff"]
DRAW_FONT = ("Microsoft JhengHei", 11)


class FloatDraw:
    def __init__(self, root, db_file, show=True):
        self.root = root
        self.db_file = db_file
        self.strokes = []          # 每一筆畫的資料
        self.items = []            # 畫布上對應的線條編號
        self.current = None
        self.color_i = 0
        self.width = 4
        self.drawing_mode = False
        self.panel_visible = False
        self.btn_pos = (100, 100)
        self.cleared_backup = [] 

        self.init_table()
        self.load()

        # 第 1 層：墨水層（顯示畫的線，背景透明）
        self.ink = tk.Toplevel(root)
        self.ink.overrideredirect(True)
        self.ink.attributes("-topmost", True)
        self.ink.attributes("-transparentcolor", DRAW_KEY)
        self.canvas = tk.Canvas(self.ink, bg=DRAW_KEY, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.ink.withdraw()

        # 第 2 層：接滑鼠層（幾乎看不見，但能收到滑鼠動作）
        self.cap = tk.Toplevel(root)
        self.cap.overrideredirect(True)
        self.cap.attributes("-topmost", True)
        self.cap.attributes("-alpha", 0.01)
        self.cap.configure(bg="black", cursor="pencil")
        self.cap.bind("<ButtonPress-1>", self.start)
        self.cap.bind("<B1-Motion>", self.move)
        self.cap.bind("<ButtonRelease-1>", self.end)
        self.cap.bind("<Escape>", lambda e: self.toggle_draw())
        self.cap.bind("<Control-z>", lambda e: self.undo())
        self.cap.withdraw()

        self.fit_to_work_area()    # ★v2：兩層都只蓋住工作區，不蓋工作列

        self.build_panel()
        self.redraw()
        if show:
            self.show_panel()

    # ---------- ★v2：取得工作區（螢幕扣掉工作列） ----------
    def get_work_area(self):
        try:
            import ctypes
            from ctypes import wintypes
            rect = wintypes.RECT()
            SPI_GETWORKAREA = 0x0030
            ctypes.windll.user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0)
            w = rect.right - rect.left
            h = rect.bottom - rect.top
            if w > 0 and h > 0:
                return rect.left, rect.top, w, h
        except Exception:
            pass
        # 拿不到的話就退回整個螢幕
        return 0, 0, self.root.winfo_screenwidth(), self.root.winfo_screenheight()

    def fit_to_work_area(self):
        x, y, w, h = self.get_work_area()
        geo = f"{w}x{h}+{x}+{y}"
        self.ink.geometry(geo)
        self.cap.geometry(geo)

    # ---------- 資料庫 ----------
    def init_table(self):
        conn = sqlite3.connect(self.db_file)
        conn.execute("CREATE TABLE IF NOT EXISTS float_draw (key TEXT PRIMARY KEY, value TEXT)")
        conn.commit()
        conn.close()

    def save(self):
        data = json.dumps({"strokes": self.strokes,
                           "pos": self.btn_pos,
                           "color": self.color_i})
        conn = sqlite3.connect(self.db_file)
        conn.execute("INSERT OR REPLACE INTO float_draw (key, value) VALUES ('state', ?)", (data,))
        conn.commit()
        conn.close()

    def load(self):
        conn = sqlite3.connect(self.db_file)
        row = conn.execute("SELECT value FROM float_draw WHERE key='state'").fetchone()
        conn.close()
        if not row:
            return
        try:
            d = json.loads(row[0])
            self.strokes = d.get("strokes", [])
            self.btn_pos = tuple(d.get("pos", (100, 100)))
            self.color_i = d.get("color", 0) % len(DRAW_COLORS)
        except (json.JSONDecodeError, TypeError):
            pass

    # ---------- 浮動按鈕列 ----------
    def build_panel(self):
        p = self.panel = tk.Toplevel(self.root)
        p.overrideredirect(True)
        p.attributes("-topmost", True)
        p.geometry(f"+{self.btn_pos[0]}+{self.btn_pos[1]}")
        p.configure(bg="#333")
        style = dict(bg="#333", fg="white", font=DRAW_FONT, bd=0, padx=8, pady=4,
                     activebackground="#555", activeforeground="white")

        grip = tk.Label(p, text="≡", bg="#333", fg="#aaa", font=DRAW_FONT,
                        cursor="fleur", padx=6)
        grip.pack(side="left")
        grip.bind("<ButtonPress-1>", self.drag_start)
        grip.bind("<B1-Motion>", self.drag_move)

        self.pen_btn = tk.Button(p, text="✎ 畫", command=self.toggle_draw, **style)
        self.pen_btn.pack(side="left")
        self.color_btn = tk.Button(p, text="●", command=self.next_color,
                                   **{**style, "fg": DRAW_COLORS[self.color_i]})
        self.color_btn.pack(side="left")
        tk.Button(p, text="↶", command=self.undo, **style).pack(side="left")
        tk.Button(p, text="清除", command=self.clear, **style).pack(side="left")
        tk.Button(p, text="✕", command=self.hide_panel, **style).pack(side="left")
        p.withdraw()

    def show_panel(self):
        self.panel.deiconify()
        self.panel.lift()
        self.panel_visible = True

    def hide_panel(self):
        if self.drawing_mode:
            self.toggle_draw()
        self.panel.withdraw()
        self.panel_visible = False
        self.save()

    def toggle_panel(self):
        """給主程式的 ✎ 按鈕用：顯示 / 收起懸浮列"""
        if self.panel_visible:
            self.hide_panel()
        else:
            self.show_panel()

    def drag_start(self, e):
        self.dx = e.x_root - self.panel.winfo_x()
        self.dy = e.y_root - self.panel.winfo_y()

    def drag_move(self, e):
        x, y = e.x_root - self.dx, e.y_root - self.dy
        self.panel.geometry(f"+{x}+{y}")
        self.btn_pos = (x, y)

    def raise_panel(self):
        self.panel.attributes("-topmost", False)
        self.panel.attributes("-topmost", True)
        self.panel.lift()

    def toggle_draw(self):
        self.drawing_mode = not self.drawing_mode
        if self.drawing_mode:
            self.fit_to_work_area()
            self.ink.deiconify()
            self.cap.deiconify()
            self.ink.lift()
            self.cap.lift()
            self.cap.focus_force()
            self.root.after_idle(self.raise_panel)   # ★v3：焦點給完之後，再把懸浮列拉到最上面
            self.pen_btn.config(text="✎ 停", bg="#c0392b")
        else:
            self.cap.withdraw()
            self.ink.withdraw()
            self.pen_btn.config(text="✎ 畫", bg="#333")

    def next_color(self):
        self.color_i = (self.color_i + 1) % len(DRAW_COLORS)
        self.color_btn.config(fg=DRAW_COLORS[self.color_i])

    def start(self, e):
        self.cap.focus_force()
        self.root.after_idle(self.raise_panel)   # ★v3：搶完焦點後，懸浮列立刻回到最上面
        c = DRAW_COLORS[self.color_i]
        self.current = {"color": c, "width": self.width,
                        "points": [e.x, e.y, e.x, e.y]}
        self.cur_item = self.canvas.create_line(
            *self.current["points"], fill=c, width=self.width,
            capstyle="round", joinstyle="round", smooth=True)

    def move(self, e):
        if self.current:
            self.current["points"] += [e.x, e.y]
            self.canvas.coords(self.cur_item, *self.current["points"])

    def end(self, e):
        if self.current:
            self.strokes.append(self.current)
            self.items.append(self.cur_item)
            self.current = None
            self.save()            # 每畫完一筆就自動存進資料庫

    def redraw(self):
        self.canvas.delete("all")
        self.items = []
        for s in self.strokes:
            self.items.append(self.canvas.create_line(
                *s["points"], fill=s["color"], width=s["width"],
                capstyle="round", joinstyle="round", smooth=True))

    def undo(self):
        if self.strokes:
            self.strokes.pop()
            self.canvas.delete(self.items.pop())
            self.save()
        elif self.cleared_backup:            # ★v4：畫布是空的 → 把剛清掉的整批救回來
            self.strokes = self.cleared_backup
            self.cleared_backup = []
            self.redraw()
            self.save()

    def clear(self):
        if not self.strokes:
            return
        self.cleared_backup = self.strokes   # ★v4：先把整批畫收進備份
        self.strokes = []
        self.redraw()
        self.save()
# ============================================================
# ★ 懸浮畫筆結束
# ============================================================


class CPTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RC Tracker")
        
        try:
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
        self.task_order = ['英文', 'C++', '專案', '課業', '資安']   # 每日打卡順序
        
        self.init_db()
        
        # ===== 計時器狀態 =====
        self.WARMUP_SEC = 300        # 開始時先倒數 5 分鐘
        self.FOCUS_CYCLE_SEC = 1500  # 碼表每 25 分鐘提醒休息
        self.BREAK_SEC = 300         # 休息 5 分鐘
        self.timer_phase = 'idle'    # idle / warmup / focus / break
        self.timer_running = False
        self.phase_remaining = self.WARMUP_SEC
        self.focus_elapsed = 0       # 碼表顯示的總時間
        self.cycle_elapsed = 0       # 這一輪番茄已經數了多久
        self.pomodoro_count = 0
        self.session_work_sec = 0    # 這次總共專注幾秒（不含休息）
        self.unrecorded = 0          # 還沒寫進資料庫的秒數
        self.current_timer_target = None
        self._timer_job = None
        self.timer_popup = None
        
        self.cpp_done = tk.BooleanVar(value=False)
        self.school_done = tk.BooleanVar(value=False)
        self.sec_done = tk.BooleanVar(value=False) 
        self.project_done = tk.BooleanVar(value=False)
        self.eng_done = tk.BooleanVar(value=False)
        self.water_done = tk.BooleanVar(value=False)

        self.task_labels = {}        # 目前畫面上的打卡標籤
        self.show_others = False     # 是否展開其他項目
        self.plan_entries = {}       # (day_type, slot) -> Entry
        
        self.week_offset = 0
        self.study_week_offset = 0
        self.upd_win = None
        self.checkin_popup = None
        self.popup_timer = None
        self.ignore_next_click = False 
        
        # ===== 時間軸 =====
        self.DAY_START_HOUR = 6      # 一天從早上 6 點開始
        self.DAY_LAST_DEFAULT = 22   # 預設只顯示到 22 點
        # 深夜時段：23, 0, 1, 2, 3, 4, 5（要從「＋時段」勾選才顯示）
        self.NIGHT_HOURS = [h % 24 for h in range(self.DAY_LAST_DEFAULT + 1, self.DAY_START_HOUR + 24)]
        self.timeline_labels = {}
        self.last_rendered_hour = None
        self.editable_hours = set()
        self.cur_idx = 0             # 現在是一天中的第幾個小時（6點=0）
        self._extra_vars = {}        # 「＋時段」選單的勾選狀態
        
        # 赤榜拖曳管理變數
        self.drag_item = None
        self.is_dragging = False

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=2)
        
        self.build_tab_daily()
        self.build_tab_calendar()
        self.build_tab_study()  
        self.build_tab_stats()
        self.build_tab_redlist() # 猛的赤榜

        self.check_cross_day()
        self.load_daily_status()
        self.poll_timeline_update()
        self.update_today_accum_label()
        
        self.root.bind_all("<Button-1>", self.close_popup_on_click, add="+")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # ★ 新增：建立懸浮畫筆（show=False 可改成開啟時不自動跳出）
        self.float_draw = FloatDraw(self.root, DB_FILE, show=True)

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

        # 赤榜資料表
        cursor.execute('''CREATE TABLE IF NOT EXISTS red_list (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          dream TEXT,
                          difficulty TEXT,
                          time_cost TEXT,
                          status INTEGER DEFAULT 0,
                          sort_order INTEGER DEFAULT 0)''')

        # 今日 / 明日計畫（各 4 格）
        cursor.execute('''CREATE TABLE IF NOT EXISTS plan_slots (
                          day_type TEXT,
                          slot INTEGER,
                          text TEXT,
                          PRIMARY KEY(day_type, slot))''')

        # 手動加入「今日剩餘」的深夜時段，date 存的是「邏輯日」（6 點換日）
        cursor.execute('''CREATE TABLE IF NOT EXISTS extra_hours (
                          date TEXT,
                          hour INTEGER,
                          PRIMARY KEY(date, hour))''')

        try: cursor.execute("ALTER TABLE red_list ADD COLUMN sort_order INTEGER DEFAULT 0")
        except: pass
        try: cursor.execute("ALTER TABLE streaks ADD COLUMN prev_checkin DATE DEFAULT '2000-01-01'")
        except: pass
        try: cursor.execute("ALTER TABLE streaks ADD COLUMN manually_unchecked_date DATE DEFAULT '2000-01-01'")
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

            cursor.execute("INSERT OR REPLACE INTO streaks (platform, current_streak, last_checkin, prev_checkin) VALUES (?, ?, ?, ?)", ('C++', cpp_streak, cpp_last, cpp_prev))
            cursor.execute("INSERT OR REPLACE INTO streaks (platform, current_streak, last_checkin, prev_checkin) VALUES (?, ?, ?, ?)", ('資安', pico_s[0], pico_s[1], pico_s[2]))
            cursor.execute("INSERT OR REPLACE INTO streaks (platform, current_streak, last_checkin, prev_checkin) VALUES (?, ?, ?, ?)", ('專案', proj_s[0], proj_s[1], proj_s[2]))
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
            cursor.execute("INSERT OR IGNORE INTO streaks (platform, current_streak, last_checkin, prev_checkin, manually_unchecked_date) VALUES (?, 0, '2000-01-01', '2000-01-01', '2000-01-01')", (plat,))
            cursor.execute("INSERT OR IGNORE INTO time_stats VALUES (?, 0, 0, '2000-01-01')", (plat,))
                
        conn.commit()
        conn.close()

    def get_today_total_study_seconds(self):
        today = datetime.now().strftime('%Y-%m-%d')
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(daily_time) FROM time_stats WHERE last_date=?", (today,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row and row[0] else 0

    def update_today_accum_label(self):
        if not hasattr(self, 'lbl_today_accum'):
            return
        total_sec = self.get_today_total_study_seconds()
        hrs = total_sec // 3600
        mins = (total_sec % 3600) // 60
        self.lbl_today_accum.config(text=f"今日累積: {hrs}h {mins}m")

    def build_tab_daily(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="日常打卡")

        timer_container = tk.Frame(tab)
        timer_container.pack(pady=(1, 0), fill="x")

        self.time_label = tk.Label(timer_container, text="00:05:00", font=("Helvetica", 28, "bold"), fg="#e74c3c")
        self.time_label.pack()

        self.lbl_today_accum = tk.Label(timer_container, text="今日累積: 0h 0m", font=("Arial", 8), fg="#7f8c8d")
        self.lbl_today_accum.place(relx=1.0, rely=1.0, anchor="se", x=-18, y=-2)

        self.lbl_phase = tk.Label(timer_container, text="", font=("Arial", 8), fg="#7f8c8d")
        self.lbl_phase.place(relx=0.0, rely=1.0, anchor="sw", x=18, y=-2)
        
        ctrl_frame = tk.Frame(tab)
        ctrl_frame.pack(pady=0)
        
        tk.Label(ctrl_frame, text=" ", font=("Arial", 9)).pack(side=tk.LEFT, padx=2)
        self.combo_target = ttk.Combobox(ctrl_frame, values=self.task_order, width=5, state="readonly")
        self.combo_target.pack(side=tk.LEFT, padx=2)
        self.combo_target.bind("<<ComboboxSelected>>", self.on_target_changed)
        
        self.btn_start_pause = tk.Button(ctrl_frame, text="開始", command=self.toggle_timer, bg="#2ecc71", fg="white", width=4)
        self.btn_start_pause.pack(side=tk.LEFT, padx=2)
        tk.Button(ctrl_frame, text="結束", command=self.end_timer, bg="#34495e", fg="white", width=4).pack(side=tk.LEFT, padx=2)

        main_content = tk.Frame(tab)
        main_content.pack(fill="both", expand=True, padx=10, pady=2)

        self.check_frame = tk.LabelFrame(main_content, text="今日任務", font=("Arial", 9))
        self.check_frame.pack(side=tk.LEFT, fill="y", padx=(0, 10), pady=2)
        self.check_frame.columnconfigure(0, minsize=140)

        self.timeline_frame = tk.LabelFrame(main_content, text="當下與今明計畫 (單擊編輯當前兩小時)", font=("Arial", 8))
        self.timeline_frame.pack(side=tk.LEFT, fill="both", expand=True, pady=2)

        self.timeline_grid_frame = tk.Frame(self.timeline_frame)
        self.timeline_grid_frame.pack(fill="both", expand=True, padx=2, pady=1)

        # 右：今日 / 明日計畫；左：今日剩餘時程
        self.plan_area = tk.Frame(self.timeline_grid_frame)
        self.plan_area.pack(side=tk.RIGHT, fill="y", padx=(0, 2))
        ttk.Separator(self.timeline_grid_frame, orient='vertical').pack(side=tk.RIGHT, fill='y', padx=6)
        self.hours_area = tk.Frame(self.timeline_grid_frame)
        self.hours_area.pack(side=tk.LEFT, fill="both", expand=True)

        bottom_frame = tk.Frame(tab)
        bottom_frame.pack(fill="x", side=tk.BOTTOM, pady=2, padx=10)
        
        self.lbl_total_days = tk.Label(bottom_frame, text="🔥 總累積修煉: 0 天", font=("Arial", 10, "bold"), fg="#2980b9")
        self.lbl_total_days.pack(side=tk.LEFT)
        
        btn_info = tk.Button(bottom_frame, text=" ℹ ", font=("Arial", 10, "bold"), relief="flat", fg="gray", cursor="hand2", command=self.show_guide)
        btn_info.pack(side=tk.RIGHT)

        # ★ 新增：叫出 / 收起懸浮畫筆（用 lambda 是因為這時 float_draw 還沒建立）
        tk.Button(bottom_frame, text=" ✎ ", font=("Arial", 10, "bold"), relief="flat", fg="gray",
                  cursor="hand2", command=lambda: self.float_draw.toggle_panel()).pack(side=tk.RIGHT)

        self.build_plan_area()
        self.render_hourly_timeline()
        self.render_checkin_panel()
        self._show_time()

    # --- 每日打卡（一次一項） ---
    def done_var(self, plat):
        return getattr(self, f"{self.plat_map[plat]}_done")

    def task_label_text(self, plat):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT current_streak FROM streaks WHERE platform=?", (plat,))
        s_row = cursor.fetchone()
        cursor.execute("SELECT total_time FROM time_stats WHERE platform=?", (plat,))
        t_row = cursor.fetchone()
        conn.close()
        streak = s_row[0] if s_row else 0
        hours = (t_row[0] / 3600) if t_row else 0
        return f"{plat} D-{streak} | {hours:.1f} hr"

    def render_checkin_panel(self):
        for w in self.check_frame.winfo_children():
            w.destroy()
        self.task_labels.clear()

        current = next((p for p in self.task_order if not self.done_var(p).get()), None)
        row = 0

        if current:
            tk.Label(self.check_frame, text="現在輪到：", font=("Arial", 8), fg="gray").grid(row=row, column=0, columnspan=2, sticky="w", padx=5, pady=(2, 0))
            row += 1
            self._make_task_row(current, row, big=True)
            row += 1
        else:
            tk.Label(self.check_frame, text="🎉 今日任務全部完成！", font=("Arial", 9, "bold"), fg="#27ae60").grid(row=row, column=0, columnspan=2, sticky="w", padx=5, pady=6)
            row += 1

        arrow = "▲ 收起" if self.show_others else "▼ 其他項目"
        tk.Button(self.check_frame, text=arrow, relief="flat", font=("Arial", 8), fg="gray", cursor="hand2",
                  command=self.toggle_others).grid(row=row, column=0, columnspan=2, sticky="w", padx=2)
        row += 1

        if self.show_others:
            for p in self.task_order:
                if p != current:
                    self._make_task_row(p, row)
                    row += 1

    def _make_task_row(self, plat, row, big=False):
        done = self.done_var(plat).get()
        font = ("Arial", 10, "bold") if big else ("Arial", 9)
        lbl = tk.Label(self.check_frame, text=self.task_label_text(plat), font=font,
                       fg="#95a5a6" if done else "#2c3e50")
        lbl.grid(row=row, column=0, sticky="w", padx=5, pady=4 if big else 2)
        lbl.bind('<Double-1>', lambda e, p=plat: self.show_last_checkin(e, p))
        tk.Checkbutton(self.check_frame, text="", variable=self.done_var(plat),
                       command=lambda p=plat: self.handle_checkin(p)).grid(row=row, column=1, sticky="w")
        self.task_labels[plat] = lbl

    def toggle_others(self):
        self.show_others = not self.show_others
        self.render_checkin_panel()

    # --- 今日 / 明日計畫（各 4 格） ---
    def build_plan_area(self):
        for w in self.plan_area.winfo_children():
            w.destroy()
        self.plan_entries.clear()

        row = 0
        for day_type, title in (('today', '今日計畫'), ('tomorrow', '明日計畫')):
            if day_type == 'tomorrow':
                ttk.Separator(self.plan_area, orient='horizontal').grid(row=row, column=0, sticky='ew', pady=6)
                row += 1
            tk.Label(self.plan_area, text=title, font=("Arial", 9, "bold"), fg="#2c3e50").grid(row=row, column=0, pady=(0, 4))
            row += 1
            for slot in range(4):
                key = (day_type, slot)
                ent = tk.Entry(self.plan_area, font=("Arial", 8), width=16, bg="#e0e0e0", relief="flat")
                ent.grid(row=row, column=0, sticky="ew", pady=1, ipady=1)
                ent.bind("<FocusOut>", lambda e, k=key: self.save_plan_slot(k))
                ent.bind("<Return>", lambda e, k=key: self._on_plan_return(k))
                self.plan_entries[key] = ent
                row += 1

        self.load_plan_entries()

    def _on_plan_return(self, key):
        self.save_plan_slot(key)
        self.root.focus_set()   # 按 Enter 後離開輸入框

    def load_plan_entries(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT day_type, slot, text FROM plan_slots")
        data = {(dt, s): (t or "") for dt, s, t in cursor.fetchall()}
        conn.close()
        for key, ent in self.plan_entries.items():
            ent.delete(0, 'end')
            ent.insert(0, data.get(key, ""))

    def save_plan_slot(self, key):
        ent = self.plan_entries.get(key)
        if not ent:
            return
        text = ent.get().strip()
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO plan_slots (day_type, slot, text) VALUES (?, ?, ?)",
                       (key[0], key[1], text))
        conn.commit()
        conn.close()

    # --- 時間軸機制（以早上 6 點為一天的開始） ---
    def logical_today(self):
        """6 點前都算前一天：把現在往回推 6 小時再取日期"""
        return (datetime.now() - timedelta(hours=self.DAY_START_HOUR)).strftime('%Y-%m-%d')

    def _day_idx(self, h):
        """小時在『一天』裡的順序：6點=0、22點=16、23點=17、0點=18 … 5點=23"""
        return (h - self.DAY_START_HOUR) % 24

    def shift_timeline_if_needed(self):
        """到了早上 6 點：明日時程/計畫 → 今日，舊的今日清掉"""
        day = self.logical_today()
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM app_config WHERE key='timeline_shift_date'")
        row = cursor.fetchone()
        last_shift = row[0] if row else '2000-01-01'
        shifted = False
        if last_shift != day:
            cursor.execute("DELETE FROM hourly_schedule WHERE day_type='today'")
            cursor.execute("UPDATE hourly_schedule SET day_type='today' WHERE day_type='tomorrow'")
            cursor.execute("DELETE FROM plan_slots WHERE day_type='today'")
            cursor.execute("UPDATE plan_slots SET day_type='today' WHERE day_type='tomorrow'")
            cursor.execute("INSERT OR REPLACE INTO app_config (key, value) VALUES ('timeline_shift_date', ?)", (day,))
            conn.commit()
            shifted = True
        conn.close()
        if shifted and self.plan_entries:
            self.load_plan_entries()
        return shifted

    def get_extra_hours(self):
        """撈出這個邏輯日手動加入、而且還沒過去的深夜時段"""
        day = self.logical_today()
        cur_idx = self._day_idx(datetime.now().hour)
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM extra_hours WHERE date<>?", (day,))   # 順手清掉舊日期
        cursor.execute("SELECT hour FROM extra_hours WHERE date=?", (day,))
        hours = {r[0] for r in cursor.fetchall() if self._day_idx(r[0]) >= cur_idx}
        conn.commit()
        conn.close()
        return hours

    def toggle_extra_hour(self, hour, var):
        day = self.logical_today()
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        if var.get():
            cursor.execute("INSERT OR IGNORE INTO extra_hours (date, hour) VALUES (?, ?)", (day, hour))
        else:
            cursor.execute("DELETE FROM extra_hours WHERE date=? AND hour=?", (day, hour))
        conn.commit()
        conn.close()
        self.render_hourly_timeline()

    def show_extra_hours_menu(self, btn):
        cur_idx = self._day_idx(datetime.now().hour)
        # 候選 = 深夜時段中還沒過去的
        candidates = [h for h in self.NIGHT_HOURS if self._day_idx(h) >= cur_idx]
        shown = self.get_extra_hours()

        menu = tk.Menu(self.root, tearoff=0)
        self._extra_vars = {}   # 存起來，避免 BooleanVar 被回收導致勾勾消失
        if not candidates:
            menu.add_command(label="今晚沒有可加入的時段", state="disabled")
        for h in candidates:
            var = tk.BooleanVar(value=(h in shown))
            self._extra_vars[h] = var
            menu.add_checkbutton(label=f"{h:02d}:00", variable=var,
                                 command=lambda h=h, v=var: self.toggle_extra_hour(h, v))
        menu.tk_popup(btn.winfo_rootx(), btn.winfo_rooty() + btn.winfo_height())

    def poll_timeline_update(self):
        now_h = datetime.now().hour
        if self.last_rendered_hour != now_h:
            self.render_hourly_timeline()
        self.root.after(30000, self.poll_timeline_update)

    def render_hourly_timeline(self):
        self.shift_timeline_if_needed()   # 畫之前先確認要不要換日

        for widget in self.hours_area.winfo_children():
            widget.destroy()
        self.timeline_labels.clear()

        cur_h = datetime.now().hour
        self.last_rendered_hour = cur_h
        self.cur_idx = self._day_idx(cur_h)
        self.editable_hours = {cur_h, (cur_h + 1) % 24}

        # 今日：預設 6~22 加上勾選的深夜時段，只留還沒過去的，再依「一天中的順序」排序
        pool = set(range(self.DAY_START_HOUR, self.DAY_LAST_DEFAULT + 1)) | self.get_extra_hours()
        today_hours = sorted((h for h in pool if self._day_idx(h) >= self.cur_idx), key=self._day_idx)
        # 明日：6~22（預覽用）
        tomorrow_hours = list(range(self.DAY_START_HOUR, self.DAY_LAST_DEFAULT + 1))

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT day_type, hour, merge_id, text FROM hourly_schedule")
        sched = {'today': {}, 'tomorrow': {}}
        for dt, h, mid, txt in cursor.fetchall():
            if dt in sched:
                sched[dt][h] = (mid if mid is not None else h, txt or "")
        conn.close()

        # 左下角小按鈕：一定要比 canvas 先 pack，才會固定在底部
        bar = tk.Frame(self.hours_area)
        bar.pack(side=tk.BOTTOM, fill="x")
        btn_more = tk.Button(bar, text="＋時段", font=("Arial", 7), relief="flat",
                             fg="gray", cursor="hand2", padx=1, pady=0)
        btn_more.config(command=lambda: self.show_extra_hours_menu(btn_more))
        btn_more.pack(side=tk.LEFT)

        canvas = tk.Canvas(self.hours_area, highlightthickness=0, height=190)
        scrollbar = ttk.Scrollbar(self.hours_area, orient="vertical", command=canvas.yview)
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
        self._build_today_col(scrollable_frame, today_hours, sched['today'],
                              tomorrow_hours, sched['tomorrow'])

    def _group_hours(self, hours, sched_data):
        """把 merge_id 相同、而且時間連續的小時合成一組（23→0 也算連續）"""
        groups = []
        prev_h = None
        for h in hours:
            mid, txt = sched_data.get(h, (h, ""))
            if groups and groups[-1][0] == mid and prev_h is not None and h == (prev_h + 1) % 24:
                groups[-1][1].append((h, txt))
            else:
                groups.append((mid, [(h, txt)]))
            prev_h = h
        return groups

    def _render_groups(self, parent, day_type, groups, row_idx, offset):
        """offset：今日 = 0，明日 = 24（明日 6 點 = 第 24 個小時）"""
        for mid, grp in groups:
            grp_hours = [h for h, _ in grp]
            h_start, h_end = grp_hours[0], grp_hours[-1]
            txt = grp[0][1]
            # 只有「當前兩小時」可以編輯（凌晨 5 點時，明日 6 點也算）
            editable = any((offset + self._day_idx(h)) in (self.cur_idx, self.cur_idx + 1) for h in grp_hours)

            label_str = f"{h_start:02d}:00" if h_start == h_end else f"{h_start:02d}~{(h_end + 1) % 24:02d}"

            time_lbl = tk.Label(parent, text=label_str, font=("Arial", 8), width=6, anchor="e", padx=2,
                                fg="#2c3e50" if editable else "#bdc3c7")
            time_lbl.grid(row=row_idx, column=0, sticky="ns", pady=1)

            content_lbl = tk.Label(parent, text=txt, font=("Arial", 8),
                                   bg="#e0e0e0" if editable else "#f4f4f4",
                                   fg="#2c3e50" if editable else "#bdc3c7",
                                   relief="solid", borderwidth=0, anchor="w", padx=3, height=1, width=14,
                                   cursor="hand2" if editable else "")
            content_lbl.grid(row=row_idx, column=1, sticky="w", pady=1, padx=(0, 4))

            if editable:
                content_lbl.bind("<Button-1>", lambda e, d=day_type, m=mid, l=content_lbl, p=parent, r=row_idx:
                                 self.start_edit_cell(e, d, m, l, p, r, 1))

            self.timeline_labels[(day_type, mid)] = content_lbl
            row_idx += 1
        return row_idx

    def _build_today_col(self, parent, today_hours, today_sched, tomorrow_hours, tomorrow_sched):
        tk.Label(parent, text="今日剩餘", font=("Arial", 9, "bold"), fg="#2c3e50").grid(row=0, column=0, columnspan=2, pady=(0, 4))
        row_idx = 1

        if today_hours:
            row_idx = self._render_groups(parent, 'today', self._group_hours(today_hours, today_sched), row_idx, 0)
        else:
            tk.Label(parent, text="今日時段已過完", font=("Arial", 8), fg="gray").grid(row=row_idx, column=0, columnspan=2)
            row_idx += 1

        tk.Label(parent, text="── 明日 ──", font=("Arial", 8, "bold"), fg="#2980b9").grid(row=row_idx, column=0, columnspan=2, pady=(6, 2))
        row_idx += 1
        self._render_groups(parent, 'tomorrow', self._group_hours(tomorrow_hours, tomorrow_sched), row_idx, 24)

    def start_edit_cell(self, event, day_type, merge_id, label_widget, parent, row, col):
        current_text = label_widget.cget("text")
        label_widget.grid_remove()

        entry = tk.Entry(parent, font=("Arial", 8), width=14, bg="#ffffff")
        entry.insert(0, current_text)
        entry.grid(row=row, column=col, sticky="w", pady=1, padx=(0, 4))
        entry.focus_set()

        finished = False

        def _finish_edit(e=None):
            nonlocal finished
            if finished:   # Enter 和 FocusOut 可能都觸發，只存一次
                return
            finished = True
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
            first, last = self.canvas.yview()
            if first <= 0 and last >= 1:   # 內容沒超出畫面，不用捲
                return
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
        self.canvas.bind("<Configure>", lambda e: self._fit_scrollregion(self.canvas))
        
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

    def _fit_scrollregion(self, canvas):
        """讓捲動範圍至少跟畫面一樣高，內容不夠高時就固定在最上面"""
        bbox = canvas.bbox("all")
        visible_h = max(canvas.winfo_height(), 1)
        content_h = (bbox[3] + 10) if bbox else 0
        width = bbox[2] if bbox else canvas.winfo_width()
        canvas.config(scrollregion=(0, 0, width, max(visible_h, content_h)))
        if content_h <= visible_h:
            canvas.yview_moveto(0)

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
        self._fit_scrollregion(self.canvas)

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
        self.entry_s_date.insert(0, datetime.now().strftime("%m%d"))

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
        self.tree_study = ttk.Treeview(tree_container, columns=study_cols, displaycolumns=study_disp, show='headings', height=2)
        
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
        cursor.execute("SELECT * FROM study_plan ORDER BY date ASC")
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
        self.entry_s_date.insert(0, datetime.now().strftime("%m%d"))
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
        # 更新打卡面板上目前看得到的標籤
        for plat, lbl in list(self.task_labels.items()):
            try:
                lbl.config(text=self.task_label_text(plat))
            except tk.TclError:
                pass

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
            
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

    # --- 猛的赤榜 ---
    def build_tab_redlist(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="猛的赤榜")

        input_frame = tk.Frame(tab)
        input_frame.pack(fill="x", padx=4, pady=3)

        tk.Label(input_frame, text="夢:", font=("Arial", 8)).grid(row=0, column=0, sticky="e")
        self.entry_red_dream = tk.Entry(input_frame, width=15)
        self.entry_red_dream.grid(row=0, column=1, padx=2, pady=2, sticky="w")

        tk.Label(input_frame, text="難度:", font=("Arial", 8)).grid(row=0, column=2, sticky="e")
        self.combo_red_diff = ttk.Combobox(input_frame, values=["高", "中", "低", ""], width=4, state="readonly")
        self.combo_red_diff.set("中")
        self.combo_red_diff.grid(row=0, column=3, padx=2, pady=2)

        tk.Label(input_frame, text="耗時:", font=("Arial", 8)).grid(row=0, column=4, sticky="e")
        self.combo_red_time = ttk.Combobox(input_frame, values=["大", "中", "少", ""], width=4, state="readonly")
        self.combo_red_time.set("中")
        self.combo_red_time.grid(row=0, column=5, padx=2, pady=2)

        tk.Button(input_frame, text="新增", command=self.add_red_item, bg="#e74c3c", fg="white", font=("Arial", 8, "bold"), width=5).grid(row=0, column=6, padx=4)

        tk.Label(tab, text="💡 提示：可按住項目上下拖移排序；點擊狀態可切換完成", font=("Arial", 8), fg="gray").pack(anchor="w", padx=6, pady=1)

        table_frame = tk.Frame(tab)
        table_frame.pack(fill="both", expand=True, padx=4, pady=2)

        cols = ('ID', '狀態', '夢想清單', '難度', '耗時')
        disp_cols = ('狀態', '夢想清單', '難度', '耗時')
        self.tree_red = ttk.Treeview(table_frame, columns=cols, displaycolumns=disp_cols, show='headings', selectmode='browse')
        
        widths = {'狀態': 55, '夢想清單': 210, '難度': 45, '耗時': 50}
        for c in disp_cols:
            self.tree_red.heading(c, text=c, anchor='center')
            self.tree_red.column(c, width=widths.get(c, 60), anchor='center')

        red_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_red.yview)
        self.tree_red.configure(yscrollcommand=red_scroll.set)

        self.tree_red.pack(side=tk.LEFT, fill="both", expand=True)
        red_scroll.pack(side=tk.LEFT, fill="y")

        btn_frame = tk.Frame(table_frame)
        btn_frame.pack(side=tk.RIGHT, fill="y", padx=2)
        tk.Button(btn_frame, text="刪除", command=self.delete_red_item, bg="#e74c3c", fg="white", font=("Arial", 8), width=4).pack(pady=2, fill="x")
        
        btn_red_info = tk.Button(btn_frame, text=" ℹ ", font=("Arial", 9, "bold"), relief="flat", fg="gray", cursor="hand2", command=self.show_red_guide)
        btn_red_info.pack(side=tk.BOTTOM, pady=2)

        self.tree_red.bind('<Button-1>', self.on_red_tree_press)
        self.tree_red.bind('<B1-Motion>', self.on_red_tree_drag)
        self.tree_red.bind('<ButtonRelease-1>', self.on_red_tree_release)
        self.tree_red.bind('<Double-1>', self.on_red_tree_double_click)

        self.tree_red.tag_configure('done', foreground='#95a5a6')
        self.tree_red.tag_configure('todo', foreground='#2c3e50')

        self.load_red_items()

    def show_red_guide(self):
        guide_text = (
            "🚩 【猛的赤榜指南】\n\n"
            "• 記錄一直想做但尚未實現的願望清單。\n"
            "• 長按項目上下拖移即可直接調整先後排序。\n"
            "• 雙擊內容格子可隨時進行編輯與修改。\n\n"
            "THIS PAGE SINCE 115/07/16 RC"
        )
        messagebox.showinfo("猛的赤榜", guide_text)

    def add_red_item(self):
        dream = self.entry_red_dream.get().strip()
        diff = self.combo_red_diff.get().strip()
        t_cost = self.combo_red_time.get().strip()

        if not dream:
            messagebox.showerror("錯誤", "夢想項目不可為空！")
            return

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT MIN(sort_order) FROM red_list")
        min_order = cursor.fetchone()[0]
        new_order = (min_order - 1) if (min_order is not None) else 0

        cursor.execute("INSERT INTO red_list (dream, difficulty, time_cost, status, sort_order) VALUES (?, ?, ?, 0, ?)",
                       (dream, diff, t_cost, new_order))
        conn.commit()
        conn.close()

        self.entry_red_dream.delete(0, 'end')
        self.load_red_items()

    def load_red_items(self):
        for r in self.tree_red.get_children():
            self.tree_red.delete(r)

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, status, dream, difficulty, time_cost FROM red_list ORDER BY sort_order ASC, id DESC")
        rows = cursor.fetchall()
        conn.close()

        for r in rows:
            rid, status, dream, diff, t_cost = r
            status_icon = "✔" if status == 1 else "⬜"
            tag = 'done' if status == 1 else 'todo'
            self.tree_red.insert("", "end", values=(rid, status_icon, dream, diff or "-", t_cost or "-"), tags=(tag,))

    def on_red_tree_press(self, event):
        region = self.tree_red.identify_region(event.x, event.y)
        if region != "cell":
            return
            
        col_id = self.tree_red.identify_column(event.x)
        row_id = self.tree_red.identify_row(event.y)

        if col_id == '#1' and row_id:
            vals = self.tree_red.item(row_id, 'values')
            if vals:
                rid = vals[0]
                new_status = 0 if vals[1] == "✔" else 1

                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                cursor.execute("UPDATE red_list SET status=? WHERE id=?", (new_status, rid))
                conn.commit()
                conn.close()
                self.load_red_items()
                return "break"

        if row_id:
            self.drag_item = row_id
            self.is_dragging = False

    def on_red_tree_drag(self, event):
        if not self.drag_item:
            return
            
        self.is_dragging = True
        target_row = self.tree_red.identify_row(event.y)
        
        if target_row and target_row != self.drag_item:
            children = list(self.tree_red.get_children())
            target_idx = children.index(target_row)
            
            self.tree_red.move(self.drag_item, '', target_idx)
            self.tree_red.selection_set(self.drag_item)

    def on_red_tree_release(self, event):
        if self.is_dragging and self.drag_item:
            self.save_red_item_order()
            
        self.drag_item = None
        self.is_dragging = False

    def save_red_item_order(self):
        items = self.tree_red.get_children()
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        for idx, item in enumerate(items):
            rid = self.tree_red.item(item, 'values')[0]
            cursor.execute("UPDATE red_list SET sort_order=? WHERE id=?", (idx, rid))
            
        conn.commit()
        conn.close()

    def on_red_tree_double_click(self, event):
        region = self.tree_red.identify_region(event.x, event.y)
        if region != "cell": return
        row_id = self.tree_red.identify_row(event.y)
        col_id = self.tree_red.identify_column(event.x)
        if not row_id or not col_id: return

        if col_id == '#1':
            return

        col_idx = int(col_id.replace('#', '')) - 1
        disp_cols = ('狀態', '夢想清單', '難度', '耗時')
        if col_idx >= len(disp_cols): return
        field_name = disp_cols[col_idx]

        item_vals = self.tree_red.item(row_id, 'values')
        if not item_vals: return
        rid = item_vals[0]
        cur_val = item_vals[col_idx + 1]

        x, y, w, h = self.tree_red.bbox(row_id, col_id)

        if field_name == "難度":
            edit_widget = ttk.Combobox(self.tree_red, values=["高", "中", "低", ""], state="readonly", font=("Arial", 8), justify="center")
            edit_widget.set(cur_val if cur_val != "-" else "")
        elif field_name == "耗時":
            edit_widget = ttk.Combobox(self.tree_red, values=["大", "中", "少", ""], state="readonly", font=("Arial", 8), justify="center")
            edit_widget.set(cur_val if cur_val != "-" else "")
        else:
            edit_widget = tk.Entry(self.tree_red, font=("Arial", 8), justify="center")
            edit_widget.insert(0, cur_val)

        edit_widget.place(x=x, y=y, width=w, height=h)
        edit_widget.focus_set()

        def _save_cell(e=None):
            new_val = edit_widget.get().strip()
            edit_widget.destroy()
            if new_val == cur_val: return

            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            if field_name == "夢想清單":
                if not new_val:
                    messagebox.showerror("錯誤", "夢想名稱不能為空！")
                    conn.close()
                    return
                cursor.execute("UPDATE red_list SET dream=? WHERE id=?", (new_val, rid))
            elif field_name == "難度":
                cursor.execute("UPDATE red_list SET difficulty=? WHERE id=?", (new_val, rid))
            elif field_name == "耗時":
                cursor.execute("UPDATE red_list SET time_cost=? WHERE id=?", (new_val, rid))

            conn.commit()
            conn.close()
            self.load_red_items()

        edit_widget.bind("<Return>", _save_cell)
        edit_widget.bind("<FocusOut>", _save_cell)
        if field_name in ("難度", "耗時"):
            edit_widget.bind("<<ComboboxSelected>>", _save_cell)

    def delete_red_item(self):
        selected = self.tree_red.selection()
        if not selected: return
        vals = self.tree_red.item(selected[0], 'values')
        if not vals: return
        rid = vals[0]

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM red_list WHERE id=?", (rid,))
        conn.commit()
        conn.close()
        self.load_red_items()

    # --- 計時器：暖身 5 分鐘 → 碼表 + 番茄鐘循環 ---
    def _fmt(self, s):
        h, rem = divmod(max(0, s), 3600)
        m, sec = divmod(rem, 60)
        return f"{h:02d}:{m:02d}:{sec:02d}"

    def _show_time(self):
        p = self.timer_phase
        if p == 'idle':
            text, color, status = self._fmt(self.WARMUP_SEC), "#e74c3c", "暖身 5 分鐘"
        elif p == 'warmup':
            text, color, status = self._fmt(self.phase_remaining), "#e74c3c", "🔥 暖身倒數"
        elif p == 'focus':
            left = self.FOCUS_CYCLE_SEC - self.cycle_elapsed
            text, color = self._fmt(self.focus_elapsed), "#27ae60"
            status = f"🍅 專注｜{left // 60:02d}:{left % 60:02d}後休息"
        else:
            text, color, status = self._fmt(self.phase_remaining), "#3498db", "☕ 休息倒數"
        if p != 'idle' and not self.timer_running:
            status += "（暫停）"
        self.time_label.config(text=text, fg=color)
        self.lbl_phase.config(text=status)
        # 按鈕的文字和顏色跟著計時狀態走
        if hasattr(self, 'btn_start_pause'):
            if self.timer_running:
                self.btn_start_pause.config(text="暫停", bg="#f39c12")
            elif p != 'idle':
                self.btn_start_pause.config(text="繼續", bg="#2ecc71")
            else:
                self.btn_start_pause.config(text="開始", bg="#2ecc71")

    def show_timer_popup(self, title, message):
        if self.timer_popup is not None and self.timer_popup.winfo_exists():
            self.timer_popup.destroy()
        self.root.bell()

        pop = tk.Toplevel(self.root)
        pop.title(title)
        pop.attributes("-topmost", True)
        w, h = 300, 170
        cx = int((pop.winfo_screenwidth() - w) / 2)
        cy = int((pop.winfo_screenheight() - h) / 2)
        pop.geometry(f"{w}x{h}+{cx}+{cy}")
        pop.resizable(False, False)

        frame = tk.Frame(pop, padx=15, pady=10)
        frame.pack(expand=True, fill="both")
        tk.Label(frame, text=title, font=("Arial", 12, "bold"), fg="#2c3e50").pack(pady=(4, 4))
        tk.Label(frame, text=message, font=("Arial", 10), wraplength=260, justify="center").pack(pady=(0, 10))
        tk.Button(frame, text="好", command=pop.destroy, bg="#3498db", fg="white", width=10, relief="groove").pack()
        self.timer_popup = pop

    def _cancel_timer_job(self):
        if self._timer_job:
            try: self.root.after_cancel(self._timer_job)
            except Exception: pass
            self._timer_job = None

    def toggle_timer(self):
        if self.timer_running:
            self.stop_timer()
        else:
            self.start_timer()

    def start_timer(self):
        target = self.combo_target.get()
        if not target:
            messagebox.showwarning("警告", "請先在下拉選單選擇計時對象！")
            return
        if self.timer_running:
            return

        # 按下開始就自動幫目前選的項目打勾
        # auto_jump=False：打勾後下拉選單不跳到下一項，計時對象保持不變
        if target in self.plat_map and not self.done_var(target).get():
            self.done_var(target).set(True)
            self.handle_checkin(target, auto_jump=False)

        if self.timer_phase == 'idle':   # 全新開始
            self.current_timer_target = target
            self.timer_phase = 'warmup'
            self.phase_remaining = self.WARMUP_SEC
            self.focus_elapsed = 0
            self.cycle_elapsed = 0
            self.pomodoro_count = 0
            self.session_work_sec = 0
            self.unrecorded = 0

        self.timer_running = True
        self._show_time()
        self._cancel_timer_job()
        self._timer_job = self.root.after(1000, self._tick)

    def stop_timer(self):
        if not self.timer_running:
            return
        self._cancel_timer_job()
        self.timer_running = False
        self.flush_record()
        self._show_time()

    def end_timer(self):
        self._cancel_timer_job()
        was_active = self.timer_phase != 'idle'
        self.flush_record()
        work_min = self.session_work_sec // 60
        tomatoes = self.pomodoro_count

        self.timer_running = False
        self.timer_phase = 'idle'
        self.phase_remaining = self.WARMUP_SEC
        self.focus_elapsed = 0
        self.cycle_elapsed = 0
        self.pomodoro_count = 0
        self.session_work_sec = 0
        self.unrecorded = 0
        self._show_time()

        if was_active and work_min > 0:
            self.show_timer_popup("本次結束", f"這次一共專注了 {work_min} 分鐘\n完成 {tomatoes} 顆番茄 🍅\n辛苦了！")

    def _tick(self):
        if not self.timer_running:
            return

        # 暖身和專注的時間才算進統計，休息不算
        if self.timer_phase in ('warmup', 'focus'):
            self.session_work_sec += 1
            self.unrecorded += 1
            if self.unrecorded >= 60:
                self.flush_record()

        if self.timer_phase == 'warmup':
            self.phase_remaining -= 1
            if self.phase_remaining <= 0:
                self.timer_phase = 'focus'
                self.focus_elapsed = self.WARMUP_SEC   # 碼表接著暖身的 5 分鐘往上數
                self.cycle_elapsed = 0
                self.show_timer_popup("✅ 暖身 5 分鐘完成！", "接下來改成碼表計時，\n每 25 分鐘會提醒你休息 5 分鐘。")

        elif self.timer_phase == 'focus':
            self.focus_elapsed += 1
            self.cycle_elapsed += 1
            if self.cycle_elapsed >= self.FOCUS_CYCLE_SEC:
                self.pomodoro_count += 1
                self.timer_phase = 'break'
                self.phase_remaining = self.BREAK_SEC
                self.show_timer_popup(f"🍅 完成第 {self.pomodoro_count} 顆番茄！", "休息 5 分鐘，\n起來走走、喝口水。")

        elif self.timer_phase == 'break':
            self.phase_remaining -= 1
            if self.phase_remaining <= 0:
                self.timer_phase = 'focus'
                self.cycle_elapsed = 0
                self.show_timer_popup("☀️ 休息結束", "碼表繼續計時，回來吧！")

        self._show_time()
        self._timer_job = self.root.after(1000, self._tick)

    def on_target_changed(self, event=None):
        new = self.combo_target.get()
        if new == self.current_timer_target:
            return
        if self.timer_phase != 'idle':
            self.flush_record()   # 還沒記的秒數先算給舊項目，計時繼續不中斷
        self.current_timer_target = new

    def flush_record(self):
        if self.unrecorded > 0:
            self.record_time(self.unrecorded)
        self.unrecorded = 0

    def record_time(self, seconds):
        target = self.current_timer_target or self.combo_target.get()
        if not target or target not in self.plat_map:
            return

        today = datetime.now().strftime('%Y-%m-%d')
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT daily_time, total_time, last_date FROM time_stats WHERE platform=?", (target,))
        row = cursor.fetchone()
        
        if row:
            daily_time, total_time, last_date = row[0], row[1], row[2]
        else:
            daily_time, total_time, last_date = 0, 0, '2000-01-01'
        
        if last_date != today: daily_time = 0 
        cursor.execute("UPDATE time_stats SET daily_time=?, total_time=?, last_date=? WHERE platform=?", 
                       (daily_time + seconds, total_time + seconds, today, target))
        conn.commit()
        conn.close()

        self.refresh_stats()
        self.update_today_accum_label()

    def on_close(self):
        try: self.flush_record()
        except Exception: pass
        try: self.float_draw.save()        # ★ 新增：關閉前把畫的內容存起來
        except Exception: pass
        self.root.destroy()

    # --- 打卡邏輯 ---
    def handle_checkin(self, platform, auto_jump=True):
        is_checked = self.done_var(platform).get()
        today = datetime.now().strftime('%Y-%m-%d')
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT current_streak, last_checkin, prev_checkin FROM streaks WHERE platform=?", (platform,))
        streak, last_date, prev_date = cursor.fetchone()
        
        if is_checked:
            if last_date != today:
                streak = streak + 1 
                cursor.execute("UPDATE streaks SET current_streak=?, last_checkin=?, prev_checkin=?, manually_unchecked_date='2000-01-01' WHERE platform=?", (streak, today, last_date, platform))
            else:
                cursor.execute("UPDATE streaks SET manually_unchecked_date='2000-01-01' WHERE platform=?", (platform,))
        else:
            if last_date == today:
                streak = max(0, streak - 1)
                cursor.execute("UPDATE streaks SET current_streak=?, last_checkin=?, manually_unchecked_date=? WHERE platform=?", (streak, prev_date, today, platform))
            else:
                cursor.execute("UPDATE streaks SET manually_unchecked_date=? WHERE platform=?", (today, platform))
                
        any_checked = any(self.done_var(p).get() for p in self.plat_map)
        if any_checked:
            cursor.execute("INSERT OR IGNORE INTO activity_log (date) VALUES (?)", (today,))
        else:
            cursor.execute("DELETE FROM activity_log WHERE date=?", (today,))
            
        conn.commit()
        conn.close()

        # 畫面在這次點擊處理完之後才重畫，避免刪掉正在被點的勾選框
        self.root.after_idle(self.render_checkin_panel)

        # 勾掉的是「正在計時的項目」→ 自動切到下一項，計時接續
        if auto_jump and is_checked and self.combo_target.get() == platform:
            self.update_target_default()
        self.refresh_stats()

    def load_daily_status(self):
        today = datetime.now().strftime('%Y-%m-%d')
        today_md = datetime.now().strftime('%m-%d')
        tw_year = datetime.now().year - 1911
        today_tw = f"{tw_year}-{today_md}"
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        for plat in self.plat_map:
            cursor.execute("SELECT last_checkin FROM streaks WHERE platform=?", (plat,))
            row = cursor.fetchone()
            if row and row[0] == today:
                self.done_var(plat).set(True)
                
        cursor.execute("SELECT manually_unchecked_date FROM streaks WHERE platform='C++'")
        cpp_m_row = cursor.fetchone()
        cpp_manually_unchecked = cpp_m_row[0] if cpp_m_row else '2000-01-01'

        if cpp_manually_unchecked != today:
            cursor.execute("SELECT id FROM contests WHERE type='CF' AND date=?", (today_tw,))
            if cursor.fetchone() and not self.cpp_done.get():
                self.cpp_done.set(True)
                self.handle_checkin('C++', auto_jump=False) 
            
        conn.close()
        self.render_checkin_panel()
        self.update_target_default()

    def show_guide(self):
        guide_text = (
            "🏆 【每日指南】\n\n"
            "✅ 今日任務\n"
            "• 一次只顯示一項，打勾後才出現下一項。\n"
            "• 順序：英文 → C++ → 專案 → 課業 → 資安\n"
            "• 點「▼ 其他項目」可以手動勾選任何一項。\n\n"
            "⏱️ 計時器\n"
            "• 開始：先倒數 5 分鐘暖身。\n"
            "• 暖身完自動變碼表，每 25 分鐘休息 5 分鐘，循環到按「結束」。\n"
            "• 中途切換項目不會中斷，時間接續記到新項目。\n\n"
            "🕐 時程與計畫\n"
            "• 一天從早上 6 點開始，預設顯示到 22 點。\n"
            "• 深夜 23~05 點從左下「＋時段」勾選才顯示，過了自動消失。\n"
            "• 不論今明，都只能編輯當前兩小時。\n"
            "• 早上 6 點時，明日時程與計畫會變成今日。\n\n"
            "📅 賽事與自動化\n"
            "• Other 類別可以自訂賽事/任務分類，並單獨篩選！\n"
            "• 雙擊戰力補題頁面比賽，可深入勾選各題進度！\n\n"
            "🚩 猛的赤榜\n"
            "• 記錄一直想做但尚未實現的願望，長按項目可拖移排序！\n\n"
            # ★ 新增：懸浮畫筆說明
            "✎ 懸浮畫筆\n"
            "• 右下 ✎ 可叫出 / 收起懸浮列，按住 ≡ 可拖動。\n"
            "• 「畫」開始在螢幕上畫，Esc 或「停」結束，Ctrl+Z 復原。\n"
            "• 畫的內容會自動保存，下次開啟還在。\n\n"
            "(本地 db 好耶!\n"
            "SINCE 115/07/16 RC"
        )
        messagebox.showinfo("每日生存證明", guide_text)

    def update_target_default(self):
        nxt = next((p for p in self.task_order if not self.done_var(p).get()), None)
        if nxt is None:   # 全部完成：保留目前選擇
            if not self.combo_target.get():
                self.combo_target.set(self.task_order[0])
                self.on_target_changed()
            return
        if self.combo_target.get() != nxt:
            self.combo_target.set(nxt)
            self.on_target_changed()

    def check_cross_day(self):
        # 打卡：午夜 0 點換日
        today = datetime.now().strftime('%Y-%m-%d')
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM app_config WHERE key='last_startup'")
        last_startup = cursor.fetchone()[0]
        
        if last_startup != today:
            for plat in self.plat_map:
                self.done_var(plat).set(False)
            cursor.execute("UPDATE app_config SET value=? WHERE key='last_startup'", (today,))
            conn.commit()
            
            self.render_checkin_panel()
            self.update_target_default()
            self.refresh_stats()
            self.update_today_accum_label()
            
        conn.close()

        # 時間軸與計畫：早上 6 點換日
        if self.shift_timeline_if_needed():
            self.render_hourly_timeline()

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