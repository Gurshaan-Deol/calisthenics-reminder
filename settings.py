import tkinter as tk
from tkinter import ttk

import exercises

SETTINGS_TITLE = "Settings — Calisthenics"
LABEL_FONT = ("Segoe UI", 10)
BTN_FONT = ("Segoe UI", 10)


class SettingsWindow:
    """Settings dialog. Only one instance can be open at a time."""

    def __init__(self, root):
        self._root = root
        self._win = None

    def open(self):
        if self._win is not None and self._win.winfo_exists():
            self._win.focus_force()
            return
        self._win = tk.Toplevel(self._root)
        self._build(self._win)

    def _build(self, win):
        win.title(SETTINGS_TITLE)
        win.resizable(True, True)
        win.minsize(400, 300)
        win.protocol("WM_DELETE_WINDOW", win.destroy)

        notebook = ttk.Notebook(win)
        notebook.pack(fill="both", expand=True, padx=12, pady=(12, 0))

        timer_tab = ttk.Frame(notebook)
        notebook.add(timer_tab, text="Timer")
        tk.Label(timer_tab, text="Coming soon", font=LABEL_FONT).pack(
            padx=20, pady=40
        )

        exercises_tab = ttk.Frame(notebook)
        notebook.add(exercises_tab, text="Exercises")
        tk.Label(exercises_tab, text="Coming soon", font=LABEL_FONT).pack(
            padx=20, pady=40
        )

        btn_frame = tk.Frame(win)
        btn_frame.pack(fill="x", padx=12, pady=12)
        tk.Button(
            btn_frame, text="Save", font=BTN_FONT, command=self._on_save,
        ).pack(side="right")

    def _on_save(self):
        # Placeholder — will write config and call exercises.reload_config() when
        # Timer and Exercises tabs are implemented.
        pass
