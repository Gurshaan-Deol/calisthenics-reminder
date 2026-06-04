import json
import sys
import tkinter as tk
import winsound

from plyer import notification

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


def load_config(path="config.json"):
    try:
        with open(path, "r") as f:
            cfg = json.load(f)
    except FileNotFoundError:
        sys.exit(f"Error: '{path}' not found. Create it before running.")
    except json.JSONDecodeError as e:
        sys.exit(f"Error: '{path}' is not valid JSON — {e}")

    if "interval_minutes" not in cfg:
        sys.exit("Error: config.json is missing 'interval_minutes'.")
    if not cfg.get("exercises"):
        sys.exit("Error: config.json must contain at least one exercise.")

    return cfg


def format_time(seconds):
    m, s = divmod(seconds, 60)
    return f"{m:02d}:{s:02d}"


class CountdownApp:
    def __init__(self, root, cfg):
        self.root = root
        self.cfg = cfg
        self.interval = int(cfg["interval_minutes"] * 60)
        self.remaining = self.interval
        self.exercise_index = 0
        self.exercise = cfg["exercises"][0]
        self._build_window()
        self._position_window()
        self._tick()

    def _build_window(self):
        self.root.title(WINDOW_TITLE)
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)
        self.root.wm_attributes("-topmost", True)

        tk.Label(
            self.root, text="Next break in", font=LABEL_FONT,
            bg=BG_COLOR, fg=DIM_COLOR
        ).pack(padx=20, pady=(12, 0))

        self.label_time = tk.Label(
            self.root, text=format_time(self.remaining), font=TIMER_FONT,
            bg=BG_COLOR, fg=ACCENT_COLOR
        )
        self.label_time.pack(padx=20, pady=(2, 10))

        tk.Frame(self.root, bg=DIM_COLOR, height=1).pack(fill="x", padx=16)

        self.label_exercise = tk.Label(
            self.root, text=self.exercise["name"], font=EXERCISE_FONT,
            bg=BG_COLOR, fg=FG_COLOR
        )
        self.label_exercise.pack(padx=20, pady=(8, 2))

        detail = f"{self.exercise['sets']} sets  ×  {self.exercise['reps']} reps"
        self.label_detail = tk.Label(
            self.root, text=detail, font=DETAIL_FONT,
            bg=BG_COLOR, fg=DIM_COLOR
        )
        self.label_detail.pack(padx=20, pady=(0, 10))

        btn_frame = tk.Frame(self.root, bg=BG_COLOR)
        btn_frame.pack(padx=16, pady=(0, 14), fill="x")

        btn_style = dict(font=LABEL_FONT, relief="flat", cursor="hand2",
                         activeforeground=BG_COLOR, bd=0, padx=10, pady=4)

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

    def _on_done(self):
        self._advance_exercise()
        self.remaining = self.interval

    def _on_snooze(self):
        self.remaining += int(self.cfg["snooze_minutes"] * 60)

    def _notify(self):
        ex = self.exercise
        notification.notify(
            title="Time to move!",
            message=f"{ex['name']} — {ex['sets']} sets × {ex['reps']} reps",
            app_name=WINDOW_TITLE,
            timeout=8,
        )
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)

    def _advance_exercise(self):
        exercises = self.cfg["exercises"]
        self.exercise_index = (self.exercise_index + 1) % len(exercises)
        self.exercise = exercises[self.exercise_index]
        self.label_exercise.config(text=self.exercise["name"])
        detail = f"{self.exercise['sets']} sets  ×  {self.exercise['reps']} reps"
        self.label_detail.config(text=detail)

    def _position_window(self):
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = sw - w - MARGIN_RIGHT
        y = sh - h - MARGIN_BOTTOM
        self.root.geometry(f"+{x}+{y}")

    def _tick(self):
        self.label_time.config(text=format_time(self.remaining))
        if self.remaining > 0:
            self.remaining -= 1
        else:
            self._notify()
            self._advance_exercise()
            self.remaining = self.interval
        self.root.after(1000, self._tick)


def main():
    cfg = load_config()
    root = tk.Tk()
    CountdownApp(root, cfg)
    root.mainloop()


if __name__ == "__main__":
    main()
