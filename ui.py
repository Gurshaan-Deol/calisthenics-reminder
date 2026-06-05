import tkinter as tk


WINDOW_TITLE = "Calisthenics"
TIMER_FONT = ("Segoe UI", 36, "bold")
LABEL_FONT = ("Segoe UI", 10)
EXERCISE_FONT = ("Segoe UI", 12, "bold")
DETAIL_FONT = ("Segoe UI", 10)
BG_COLOR = "#1e1e2e"
FG_COLOR = "#cdd6f4"
ACCENT_COLOR = "#89b4fa"
DIM_COLOR = "#a6adc8"
MARGIN_RIGHT = 20
MARGIN_BOTTOM = 60


class Panel:
    def __init__(self, root, initial_exercise, on_done, on_snooze):
        self.root = root
        self._visible = True
        self._on_done = on_done
        self._on_snooze = on_snooze
        self._build_window(initial_exercise)
        self._position_window()

    def _build_window(self, exercise):
        self.root.title(WINDOW_TITLE)
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)
        self.root.wm_attributes("-topmost", True)
        self.root.protocol("WM_DELETE_WINDOW", self.hide)

        tk.Label(
            self.root, text="Next break in", font=LABEL_FONT,
            bg=BG_COLOR, fg=DIM_COLOR
        ).pack(padx=20, pady=(12, 0))

        self.label_time = tk.Label(
            self.root, text="", font=TIMER_FONT,
            bg=BG_COLOR, fg=ACCENT_COLOR
        )
        self.label_time.pack(padx=20, pady=(2, 10))

        tk.Frame(self.root, bg=DIM_COLOR, height=1).pack(fill="x", padx=16)

        self.label_exercise = tk.Label(
            self.root, text=exercise["name"], font=EXERCISE_FONT,
            bg=BG_COLOR, fg=FG_COLOR
        )
        self.label_exercise.pack(padx=20, pady=(8, 2))

        detail = f"{exercise['sets']} sets  ×  {exercise['reps']} reps"
        self.label_detail = tk.Label(
            self.root, text=detail, font=DETAIL_FONT,
            bg=BG_COLOR, fg=DIM_COLOR
        )
        self.label_detail.pack(padx=20, pady=(0, 10))

        btn_frame = tk.Frame(self.root, bg=BG_COLOR)
        btn_frame.pack(padx=16, pady=(0, 14), fill="x")

        btn_style = dict(
            font=LABEL_FONT, relief="flat", cursor="hand2",
            activeforeground=BG_COLOR, bd=0, padx=10, pady=4,
        )
        tk.Button(
            btn_frame, text="Done",
            bg=ACCENT_COLOR, fg=BG_COLOR, activebackground=ACCENT_COLOR,
            command=self._on_done, **btn_style
        ).pack(side="left", expand=True, fill="x", padx=(0, 4))
        tk.Button(
            btn_frame, text="Snooze",
            bg=DIM_COLOR, fg=BG_COLOR, activebackground=DIM_COLOR,
            command=self._on_snooze, **btn_style
        ).pack(side="left", expand=True, fill="x", padx=(4, 0))

    def _position_window(self):
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = sw - w - MARGIN_RIGHT
        y = sh - h - MARGIN_BOTTOM
        self.root.geometry(f"+{x}+{y}")

    def set_time(self, text):
        self.label_time.config(text=text)

    def set_exercise(self, name, sets, reps):
        self.label_exercise.config(text=name)
        self.label_detail.config(text=f"{sets} sets  ×  {reps} reps")

    def hide(self):
        self.root.withdraw()
        self._visible = False

    def toggle(self):
        if self._visible:
            self.root.withdraw()
            self._visible = False
        else:
            self.root.deiconify()
            self._visible = True
