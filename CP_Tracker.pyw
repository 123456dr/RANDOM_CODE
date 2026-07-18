import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta

DB_FILE = 'cp_tracker.db'

class CPTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CP & CTF Tracker")
        
        # --- 精準設定視窗大小與位置 ---
        window_width = 380
        window_height = 280
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = screen_width - window_width - 10
        y = screen_height - window_height - 80 
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.init_db()
        
        self.timer_running = False
        self.total_seconds = 10800
        self.remaining_seconds = self.total_seconds
        
        self.cf_done = tk.BooleanVar(value=False)
        self.cses_done = tk.BooleanVar(value=False)
        self.picoctf_done = tk.BooleanVar(value=False) 
        self.project_done = tk.BooleanVar(value=False)
        
        self.week_offset = 0
        self.upd_win = None
        self.contest_ids = []
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=2)
        
        self.build_tab_daily()
        self.build_tab_calendar()
        self.build_tab_stats()

        self.check_startup_date()
        
        self.load_daily_status()

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
        
        try: cursor.execute("ALTER TABLE contests ADD COLUMN probs TEXT DEFAULT ''")
        except: pass
        try: cursor.execute("ALTER TABLE contests ADD COLUMN up_done TEXT DEFAULT ''")
        except: pass
        try: cursor.execute("ALTER TABLE contests ADD COLUMN c_num TEXT DEFAULT ''")
        except: pass
            
        for plat in ['CF', 'CSES', 'picoCTF', 'Project']:
            cursor.execute("INSERT OR IGNORE INTO streaks VALUES (?, 0, '2000-01-01')", (plat,))
            if plat not in ['picoCTF', 'Project']:
                cursor.execute("INSERT OR IGNORE INTO time_stats VALUES (?, 0, 0, '2000-01-01')", (plat,))
        conn.commit()
        conn.close()

    # ================= UI 建構 =================
    def build_tab_daily(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="日常打卡")

        self.time_label = tk.Label(tab, text="03:00:00", font=("Helvetica", 32, "bold"), fg="#e74c3c")
        self.time_label.pack(pady=2)
        
        ctrl_frame = tk.Frame(tab)
        ctrl_frame.pack(pady=0)
        
        tk.Label(ctrl_frame, text="時間:", font=("Arial", 9)).pack(side=tk.LEFT, padx=2)
        self.combo_time = ttk.Combobox(ctrl_frame, values=["1 小時", "2 小時", "3 小時"], width=6, state="readonly")
        self.combo_time.set("3 小時")
        self.combo_time.pack(side=tk.LEFT, padx=5)
        self.combo_time.bind("<<ComboboxSelected>>", self.on_time_select)
        
        tk.Button(ctrl_frame, text="開始", command=self.start_timer, bg="#2ecc71", fg="white", width=4).pack(side=tk.LEFT, padx=2)
        tk.Button(ctrl_frame, text="暫停", command=self.stop_timer, bg="#f39c12", fg="white", width=4).pack(side=tk.LEFT, padx=2)
        tk.Button(ctrl_frame, text="重置", command=self.reset_timer, bg="#34495e", fg="white", width=4).pack(side=tk.LEFT, padx=2)

        check_frame = tk.LabelFrame(tab, text="今日任務", font=("Arial", 9))
        check_frame.pack(fill="x", padx=10, pady=2)

        self.lbl_cf_streak = tk.Label(check_frame, text="CF cnt: 0 | 0.0 hr", font=("Arial", 9))
        self.lbl_cf_streak.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        tk.Checkbutton(check_frame, text="CF 打卡", variable=self.cf_done, command=lambda: self.handle_checkin('CF')).grid(row=0, column=1, sticky="w")

        self.lbl_cses_streak = tk.Label(check_frame, text="CSES cnt: 0 | 0.0 hr", font=("Arial", 9))
        self.lbl_cses_streak.grid(row=1, column=0, sticky="w", padx=5, pady=2)
        tk.Checkbutton(check_frame, text="CSES 打卡", variable=self.cses_done, command=lambda: self.handle_checkin('CSES')).grid(row=1, column=1, sticky="w")

        self.lbl_picoctf_streak = tk.Label(check_frame, text="picoCTF cnt: 0", font=("Arial", 9))
        self.lbl_picoctf_streak.grid(row=2, column=0, sticky="w", padx=5, pady=2)
        tk.Checkbutton(check_frame, text="picoCTF 打卡", variable=self.picoctf_done, command=lambda: self.handle_checkin('picoCTF')).grid(row=2, column=1, sticky="w")
        
        self.lbl_project_streak = tk.Label(check_frame, text="專案 cnt: 0", font=("Arial", 9))
        self.lbl_project_streak.grid(row=3, column=0, sticky="w", padx=5, pady=2)
        tk.Checkbutton(check_frame, text="專案 打卡", variable=self.project_done, command=lambda: self.handle_checkin('Project')).grid(row=3, column=1, sticky="w")

        bottom_frame = tk.Frame(tab)
        bottom_frame.pack(fill="x", side=tk.BOTTOM, pady=2, padx=10)
        
        self.lbl_total_days = tk.Label(bottom_frame, text="🔥 總累積修煉: 0 天", font=("Arial", 10, "bold"), fg="#2980b9")
        self.lbl_total_days.pack(side=tk.LEFT)
        
        btn_info = tk.Button(bottom_frame, text=" ℹ ", font=("Arial", 10, "bold"), relief="flat", fg="gray", cursor="hand2", command=self.show_guide)
        btn_info.pack(side=tk.RIGHT)

    def build_tab_calendar(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="賽事行事曆")

        input_frame = tk.Frame(tab)
        input_frame.pack(fill="x", padx=2, pady=0)
        
        tk.Label(input_frame, text="賽事:", font=("Arial", 8)).grid(row=0, column=0, sticky="e")
        # 增加 CPE
        self.entry_type = ttk.Combobox(input_frame, values=["CF", "LC", "CPE", "Other"], width=4, state="readonly")
        self.entry_type.grid(row=0, column=1, padx=2, pady=2)
        self.entry_type.set("CF")
        
        tk.Label(input_frame, text="日期(MMDD):", font=("Arial", 8)).grid(row=0, column=2, sticky="e")
        self.entry_date = tk.Entry(input_frame, width=5)
        self.entry_date.grid(row=0, column=3, padx=2)
        
        tk.Label(input_frame, text="時間(HHMM):", font=("Arial", 8)).grid(row=0, column=4, sticky="e")
        self.entry_time = tk.Entry(input_frame, width=5)
        self.entry_time.grid(row=0, column=5, padx=2)
        
        self.lbl_div_type = tk.Label(input_frame, text="Div:", font=("Arial", 8))
        self.lbl_div_type.grid(row=1, column=0, sticky="e")
        
        self.entry_div = tk.Entry(input_frame, width=6)
        self.entry_div.grid(row=1, column=1, padx=2, pady=2)
        
        self.lbl_cnum = tk.Label(input_frame, text="編號(4碼):", font=("Arial", 8))
        self.lbl_cnum.grid(row=1, column=2, sticky="e")
        
        self.entry_cnum = tk.Entry(input_frame, width=5)
        self.entry_cnum.grid(row=1, column=3, padx=2)

        def on_type_change(event):
            self.entry_div.destroy()
            self.entry_time.config(state="normal") # 重置時間欄位狀態
            
            ctype = self.entry_type.get()
            if ctype == "LC":
                self.lbl_div_type.config(text="類型:")
                self.entry_div = ttk.Combobox(input_frame, values=["Weekly", "Biweekly"], width=6, state="readonly")
                self.entry_div.set("Weekly")
                self.lbl_cnum.config(text="編號(4碼):")
                self.entry_cnum.config(state="normal")
            elif ctype == "Other":
                self.lbl_div_type.config(text="Task:")
                self.entry_div = tk.Entry(input_frame, width=12) 
                self.lbl_cnum.config(text="")
                self.entry_cnum.delete(0, 'end')
                self.entry_cnum.config(state="disabled") 
            elif ctype == "CPE":
                self.lbl_div_type.config(text="")
                self.entry_div = tk.Entry(input_frame, width=6)
                self.entry_div.insert(0, "")
                self.entry_div.config(state="disabled") # CPE 不需要 Div
                self.entry_time.delete(0, 'end')
                self.entry_time.config(state="disabled") # 隱藏/停用時間
                self.lbl_cnum.config(text="民國年:")
                self.entry_cnum.config(state="normal")
            else:
                self.lbl_div_type.config(text="Div:")
                self.entry_div = tk.Entry(input_frame, width=6)
                self.lbl_cnum.config(text="編號(4碼):")
                self.entry_cnum.config(state="normal")
            
            if ctype == "Other":
                self.entry_div.grid(row=1, column=1, columnspan=3, sticky="w", padx=2, pady=2)
            else:
                self.entry_div.grid(row=1, column=1, padx=2, pady=2)
                
        self.entry_type.bind("<<ComboboxSelected>>", on_type_change)
        
        tk.Button(input_frame, text="新增", command=self.add_contest, bg="#3498db", fg="white", height=1).grid(row=1, column=4, columnspan=2, padx=5, sticky="we")

        nav_frame = tk.Frame(tab)
        nav_frame.pack(fill="x", pady=0)
        tk.Button(nav_frame, text="◀", command=lambda: self.change_week(-1)).pack(side=tk.LEFT, padx=10)
        
        self.lbl_week = tk.Label(nav_frame, text="本週", font=("Arial", 9, "bold"), cursor="hand2")
        self.lbl_week.pack(side=tk.LEFT, expand=True)
        self.lbl_week.bind("<Button-1>", self.reset_week_view)
        
        tk.Button(nav_frame, text="▶", command=lambda: self.change_week(1)).pack(side=tk.RIGHT, padx=10)

        self.canvas = tk.Canvas(tab, height=90, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack(fill="x", pady=2)
        
        del_frame = tk.Frame(tab)
        del_frame.pack(fill="both", expand=True, padx=5, pady=0)
        self.list_contests = tk.Listbox(del_frame, height=3, font=("Arial", 8))
        self.list_contests.pack(side=tk.LEFT, fill="both", expand=True)
        tk.Button(del_frame, text="刪除", command=self.delete_contest, bg="#e74c3c", fg="white").pack(side=tk.RIGHT, padx=2)

        self.draw_calendar()

    def build_tab_stats(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="戰力與補題")
        
        self.stat_frame = tk.Frame(tab, bg="#f5f6fa")
        self.stat_frame.pack(fill="x", pady=2, padx=5)
        self.lbl_stats = tk.Label(self.stat_frame, text="資料載入中...", justify=tk.LEFT, bg="#f5f6fa", font=("Arial", 9))
        self.lbl_stats.pack(anchor="w", pady=2, padx=5)

        tk.Label(tab, text="雙擊下方賽事修改進度 (顯示 CF/LC/CPE)", font=("Arial", 8, "bold"), fg="gray").pack(anchor="w", padx=5)

        cols = ('ID', '賽事', '日期', '題目', '進度', '未補')
        disp_cols = ('賽事', '日期', '題目', '進度', '未補')
        
        self.tree = ttk.Treeview(tab, columns=cols, displaycolumns=disp_cols, show='headings', height=5)
        for c, w in zip(disp_cols, [65, 55, 60, 50, 50]):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w, anchor='center')
            
        self.tree.pack(fill='both', expand=True, padx=5, pady=2)
        self.tree.bind('<Double-1>', self.on_tree_double_click)
        
        self.refresh_stats()

    # ================= 核心邏輯 =================
    def show_guide(self):
        guide_text = (
            "🏆 【每日指南】\n\n"
            "🔴 Part 1: CF (2 hr)\n"
            "• 先解 1 題 CF 1100+。\n"
            "• 卡 1 小時，看解答打 AC。\n\n"
            "🔵 Part 2: CSES (1 hr)\n"
            "• CF 解完剩時刷 CSES。\n"
            "• 時間到未寫完，留註解當明天開胃菜。\n\n"
            "📅 賽事與自動化\n"
            "• 點擊行事曆上方標籤可快速跳回「本週」。\n"
            "• 雙擊補題頁面的比賽，再次雙擊「編號」即可原地修改！\n\n"
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

    def check_startup_date(self):
        """比對上次啟動日期，若跨日則重置打卡勾選"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute("SELECT value FROM app_config WHERE key='last_startup'")
        last_startup = cursor.fetchone()[0]
        
        if last_startup != today:
            # 日期不同：單純取消 UI 的勾選狀態，不會觸發 handle_checkin 影響舊紀錄
            self.cf_done.set(False)
            self.cses_done.set(False)
            self.picoctf_done.set(False)
            self.project_done.set(False)
            
            # 更新資料庫中的最後啟動日期為今天
            cursor.execute("UPDATE app_config SET value=? WHERE key='last_startup'", (today,))
            conn.commit()
            
        conn.close()

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
            if elapsed == 3600 and not self.cf_done.get() and self.total_seconds > 3600:
                messagebox.showinfo("CF 提醒", "一小時了，卡住記得看 Tutorial！")
            elif elapsed == 7200 and not self.cf_done.get() and self.total_seconds > 7200:
                messagebox.showinfo("CF 警告", "兩小時了！準備進入 CSES！")

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
        target = 'CSES' if self.cf_done.get() else 'CF'
        cursor.execute("SELECT daily_time, total_time, last_date FROM time_stats WHERE platform=?", (target,))
        row = cursor.fetchone()
        daily_time, total_time, last_date = row[0], row[1], row[2]
        
        if last_date != today: daily_time = 0 
        cursor.execute("UPDATE time_stats SET daily_time=?, total_time=?, last_date=? WHERE platform=?", 
                       (daily_time + 60, total_time + 60, today, target))
        conn.commit()
        conn.close()
        self.refresh_stats()

    def handle_checkin(self, platform):
        is_checked = getattr(self, f"{platform.lower()}_done").get()
        today = datetime.now().strftime('%Y-%m-%d')
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute("SELECT current_streak, last_checkin FROM streaks WHERE platform=?", (platform,))
        streak, last_date = cursor.fetchone()
        
        if is_checked:
            if last_date != today:
                streak = streak + 1 #streak + 1 if last_date == yesterday else 1
                cursor.execute("UPDATE streaks SET current_streak=?, last_checkin=? WHERE platform=?", (streak, today, platform))
        else:
            if last_date == today:
                streak = max(0, streak - 1)
                cursor.execute("UPDATE streaks SET current_streak=?, last_checkin=? WHERE platform=?", (streak, yesterday, platform))
                
        any_checked = self.cf_done.get() or self.cses_done.get() or self.picoctf_done.get() or self.project_done.get()
        if any_checked:
            cursor.execute("INSERT OR IGNORE INTO activity_log (date) VALUES (?)", (today,))
        else:
            cursor.execute("DELETE FROM activity_log WHERE date=?", (today,))
            
        conn.commit()
        conn.close()
        self.refresh_stats()

    def load_daily_status(self):
        today = datetime.now().strftime('%Y-%m-%d')
        today_md = datetime.now().strftime('%m-%d')
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        for plat in ['CF', 'CSES', 'picoCTF', 'Project']:
            cursor.execute("SELECT last_checkin FROM streaks WHERE platform=?", (plat,))
            if cursor.fetchone()[0] == today:
                getattr(self, f"{plat.lower()}_done").set(True)
                
        cursor.execute("SELECT id FROM contests WHERE type='CF' AND date=?", (today_md,))
        if cursor.fetchone() and not self.cf_done.get():
            self.cf_done.set(True)
            self.handle_checkin('CF') 
            
        conn.close()

    def add_contest(self):
        ctype = self.entry_type.get()
        raw_date = self.entry_date.get()
        raw_time = self.entry_time.get()
        cdiv = self.entry_div.get().strip()
        cnum = self.entry_cnum.get().strip() if ctype != "Other" else ""
        
        if ctype not in ["Other", "CPE"]:
            if len(raw_date) != 4 or not raw_date.isdigit() or len(raw_time) != 4 or not raw_time.isdigit():
                messagebox.showerror("錯誤", "格式錯誤，請輸入 4 碼 (例: 0718)")
                return
        elif ctype == "CPE":
            if len(raw_date) != 4 or not raw_date.isdigit():
                messagebox.showerror("錯誤", "日期格式錯誤 (例: 0718)")
                return
            raw_time = "0000" # CPE 不記錄時間
        else:
            if len(raw_date) != 4 or not raw_date.isdigit():
                messagebox.showerror("錯誤", "日期格式錯誤 (例: 0718)")
                return
            if len(raw_time) != 4 and raw_time != "":
                 if not raw_time.isdigit():
                    messagebox.showerror("錯誤", "時間請留空或輸入 4 碼")
                    return
            elif raw_time == "": raw_time = "0000"
            
        cdate = f"{raw_date[:2]}-{raw_date[2:]}"
        ctime = f"{raw_time[:2]}:{raw_time[2:]}"
        
        if ctype == "CF" and cdiv:
            if not cdiv.lower().startswith("div"):
                cdiv = f"Div {cdiv}"
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
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
        col_width = 370 / 7
        
        for i in range(7):
            d = start_date + timedelta(days=i)
            x_center = i * col_width + (col_width / 2) + 5
            
            is_today = (d == today)
            color = "#ff4757" if is_today else "white"
            bg_color = "#ff4757" if is_today else "#1e1e1e"
            
            self.canvas.create_text(x_center, 8, text=days_zh[i], fill="#7f8fa6", font=("Arial", 8))
            if is_today:
                self.canvas.create_oval(x_center-12, 16, x_center+12, 40, fill=bg_color, outline="")
            self.canvas.create_text(x_center, 28, text=d.strftime("%d"), fill="white" if is_today else "gray", font=("Arial", 9, "bold"))
            
            day_str = d.strftime("%m-%d")
            y_offset = 46
            for c in contests:
                if c[2] == day_str:
                    c_type = c[1]
                    c_div = c[4]
                    c_num = c[9] if len(c) > 9 else ""
                    
                    if c_type == "LC":
                        text_disp = f"LC {c_num}\n{c_div}"
                        box_col = "#e67e22"
                    elif c_type == "Other":
                        text_disp = f"Task\n{c_div[:8]}"
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
            if c_type == "Other":
                self.list_contests.insert(tk.END, f"{c[2]} {c[3]} | Task: {c_div}")
            elif c_type == "CPE":
                self.list_contests.insert(tk.END, f"{c[2]} | CPE {c_num}年")
            else:
                self.list_contests.insert(tk.END, f"{c[2]} {c[3]} | {c_type} {c_num} ({c_div})")

    def refresh_stats(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        for plat in ['CF', 'CSES', 'picoCTF', 'Project']:
            cursor.execute("SELECT current_streak FROM streaks WHERE platform=?", (plat,))
            streak = cursor.fetchone()[0] if cursor.rowcount != 0 else 0
            time_str = ""
            if plat not in ['picoCTF', 'Project']:
                cursor.execute("SELECT total_time FROM time_stats WHERE platform=?", (plat,))
                t_row = cursor.fetchone()
                total_hours = (t_row[0] / 3600) if t_row else 0
                time_str = f" | {total_hours:.1f} hr"
            
            getattr(self, f"lbl_{plat.lower()}_streak").config(text=f"{plat} 連勝: {streak} {time_str}")
            
        cursor.execute("SELECT COUNT(*) FROM activity_log")
        total_days = cursor.fetchone()[0]
        self.lbl_total_days.config(text=f"🔥 總累積修煉: {total_days} 天")
            
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        # 僅選取 CF, LC, CPE 進入補題列表
        cursor.execute("SELECT id, type, date, div, probs, solved, up_done, c_num FROM contests WHERE type IN ('CF', 'LC', 'CPE') ORDER BY date DESC, time DESC")
        cf_cnt, lc_cnt, cpe_cnt = 0, 0, 0
        tot_solved, tot_up = 0, 0
        
        for row in cursor.fetchall():
            c_id, c_type, c_date, c_div, c_probs, c_solved, c_up, c_num = row
            
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

            disp_row = (c_id, event_str, c_date, c_probs or '-', sol_cnt or '-', unsolved_str)
            self.tree.insert("", "end", values=disp_row)
            
            tot_solved += sol_cnt
            tot_up += up_cnt
            
        self.lbl_stats.config(text=f"🏆 賽事: CF {cf_cnt} | LC {lc_cnt} | CPE {cpe_cnt}\n🔥 完成進度: {tot_solved} 項 | 🛠️ 賽後補題: {tot_up} 題")
        conn.close()

    def on_tree_double_click(self, event):
        selected = self.tree.selection()
        if not selected: return
        
        if self.upd_win and self.upd_win.winfo_exists():
            self.upd_win.lift()
            return
            
        item = self.tree.item(selected[0])
        cid = item['values'][0]
        cdate = item['values'][2]
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT type, probs, solved, up_done, c_num, div FROM contests WHERE id=?", (cid,))
        row = cursor.fetchone()
        conn.close()
        
        ctype, cur_probs, cur_solved, cur_up_done, cur_cnum, cur_div = row
        is_lc = (ctype == "LC")
        is_cpe = (ctype == "CPE")
        is_cf = (ctype == "CF")
        
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
        self.upd_win.geometry(f"200x260+{x}+{y}")
        self.upd_win.attributes('-topmost', True)
        
        header_frame = tk.Frame(self.upd_win)
        header_frame.pack(pady=5)
        
        tk.Label(header_frame, text=f"{ctype} ", font=("Arial", 10, "bold")).grid(row=0, column=0)
        
        lbl_cnum = tk.Label(header_frame, text=cur_cnum if cur_cnum else "(未填)", font=("Arial", 10, "bold", "underline"), fg="#3498db", cursor="hand2")
        lbl_cnum.grid(row=0, column=1)
        
        ent_cnum = tk.Entry(header_frame, width=5, font=("Arial", 10))
        ent_cnum.insert(0, cur_cnum)
        
        tk.Label(header_frame, text=f" ({cdate})", font=("Arial", 10, "bold")).grid(row=0, column=2)
        
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
            new_cnum = ent_cnum.get().strip()
            
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("UPDATE contests SET probs=?, solved=?, up_done=?, c_num=? WHERE id=?", 
                           (p_val, s_val, u_val, new_cnum, cid))
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