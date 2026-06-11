import tkinter as tk
from tkinter import ttk

import exercises

SETTINGS_TITLE = "Settings — Calisthenics"
LABEL_FONT = ("Segoe UI", 10)
BTN_FONT = ("Segoe UI", 10)
ENTRY_ERROR_BG = "#ffe0e0"
ERROR_FG = "#cc0000"

# Character widths for exercise table columns.
_NAME_W = 20
_NUM_W = 5

# Day-toggle button constants.
_DAY_LABELS = ("M", "T", "W", "T", "F", "S", "S")
_DAY_BTN_FONT = ("Segoe UI", 8)
_DAY_ACTIVE_BG = "#89b4fa"
_DAY_INACTIVE_BG = "SystemButtonFace"


class SettingsWindow:
    """Settings dialog. Only one instance can be open at a time."""

    def __init__(self, root, on_timer_update=None, on_exercises_update=None):
        self._root = root
        self._win = None
        self._on_timer_update = on_timer_update
        self._on_exercises_update = on_exercises_update
        # Timer tab widget refs — set by _build_timer_tab, read by _on_save.
        self._entry_interval = None
        self._entry_snooze = None
        self._err_interval = None
        self._err_snooze = None
        self._normal_entry_bg = None
        # Exercises tab state — set by _build_exercises_tab.
        self._rows = []        # list of row dicts (see _add_exercise_row)
        self._inner_frame = None
        self._ex_canvas = None

    # ------------------------------------------------------------------
    # Window lifecycle
    # ------------------------------------------------------------------

    def open(self):
        if self._win is not None and self._win.winfo_exists():
            self._win.focus_force()
            return
        self._win = tk.Toplevel(self._root)
        self._build(self._win)

    def _build(self, win):
        win.title(SETTINGS_TITLE)
        win.resizable(True, True)
        win.minsize(580, 380)
        win.protocol("WM_DELETE_WINDOW", win.destroy)

        notebook = ttk.Notebook(win)
        notebook.pack(fill="both", expand=True, padx=12, pady=(12, 0))

        timer_tab = ttk.Frame(notebook)
        notebook.add(timer_tab, text="Timer")
        self._build_timer_tab(timer_tab)

        exercises_tab = ttk.Frame(notebook)
        notebook.add(exercises_tab, text="Exercises")
        self._build_exercises_tab(exercises_tab)

        btn_frame = tk.Frame(win)
        btn_frame.pack(fill="x", padx=12, pady=12)
        tk.Button(
            btn_frame, text="Save", font=BTN_FONT, command=self._on_save,
        ).pack(side="right")

    # ------------------------------------------------------------------
    # Timer tab
    # ------------------------------------------------------------------

    def _build_timer_tab(self, parent):
        cfg = exercises.get_config()

        frame = tk.Frame(parent)
        frame.pack(fill="both", padx=20, pady=20)

        tk.Label(frame, text="Reminder interval (minutes):", font=LABEL_FONT).grid(
            row=0, column=0, sticky="w", pady=(0, 8)
        )
        self._entry_interval = tk.Entry(frame, font=LABEL_FONT, width=8)
        self._entry_interval.insert(0, str(cfg["interval_minutes"]))
        self._entry_interval.grid(row=0, column=1, sticky="w", padx=(8, 0), pady=(0, 8))
        self._err_interval = tk.Label(frame, text="", font=LABEL_FONT, fg=ERROR_FG)
        self._err_interval.grid(row=0, column=2, sticky="w", padx=(8, 0), pady=(0, 8))

        tk.Label(frame, text="Snooze duration (minutes):", font=LABEL_FONT).grid(
            row=1, column=0, sticky="w"
        )
        self._entry_snooze = tk.Entry(frame, font=LABEL_FONT, width=8)
        self._entry_snooze.insert(0, str(cfg["snooze_minutes"]))
        self._entry_snooze.grid(row=1, column=1, sticky="w", padx=(8, 0))
        self._err_snooze = tk.Label(frame, text="", font=LABEL_FONT, fg=ERROR_FG)
        self._err_snooze.grid(row=1, column=2, sticky="w", padx=(8, 0))

        # Capture default Entry background once; used by all validation helpers.
        self._normal_entry_bg = self._entry_interval.cget("background")

    # ------------------------------------------------------------------
    # Exercises tab
    # ------------------------------------------------------------------

    def _build_exercises_tab(self, parent):
        self._rows = []

        # Toolbar: Add Exercise button above the list.
        toolbar = tk.Frame(parent)
        toolbar.pack(fill="x", padx=8, pady=(8, 0))
        tk.Button(
            toolbar, text="Add Exercise", font=BTN_FONT,
            command=self._add_blank_row,
        ).pack(side="left")

        # Column headers — fixed outside the scroll area.
        header = tk.Frame(parent)
        header.pack(fill="x", padx=8, pady=(6, 0))
        tk.Label(header, text="Name", font=LABEL_FONT, width=_NAME_W, anchor="w").pack(side="left")
        tk.Label(header, text="Sets", font=LABEL_FONT, width=_NUM_W, anchor="w").pack(
            side="left", padx=(4, 0)
        )
        tk.Label(header, text="Reps", font=LABEL_FONT, width=_NUM_W, anchor="w").pack(
            side="left", padx=(4, 0)
        )
        tk.Label(header, text="Days", font=LABEL_FONT, anchor="w").pack(
            side="left", padx=(8, 0)
        )

        # Scroll container.
        container = tk.Frame(parent)
        container.pack(fill="both", expand=True, padx=8, pady=(2, 8))

        scrollbar = tk.Scrollbar(container, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self._ex_canvas = tk.Canvas(
            container, yscrollcommand=scrollbar.set, highlightthickness=0
        )
        self._ex_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self._ex_canvas.yview)
        self._ex_canvas.bind("<MouseWheel>", self._on_mousewheel)

        self._inner_frame = tk.Frame(self._ex_canvas)
        self._inner_frame.bind("<MouseWheel>", self._on_mousewheel)
        win_id = self._ex_canvas.create_window((0, 0), window=self._inner_frame, anchor="nw")

        self._inner_frame.bind(
            "<Configure>",
            lambda _e: self._ex_canvas.configure(
                scrollregion=self._ex_canvas.bbox("all")
            ),
        )
        self._ex_canvas.bind(
            "<Configure>",
            lambda e: self._ex_canvas.itemconfig(win_id, width=e.width),
        )

        for ex in exercises.get_config()["exercises"]:
            self._add_exercise_row(
                ex["name"], ex["sets"], ex["reps"],
                days=ex.get("days", "daily"),
                original=ex,
            )

    def _add_exercise_row(self, name="", sets="", reps="", days="daily", original=None):
        row_frame = tk.Frame(self._inner_frame)
        row_frame.pack(fill="x", pady=2)

        e_name = tk.Entry(row_frame, font=LABEL_FONT, width=_NAME_W)
        e_name.insert(0, str(name))
        e_name.pack(side="left")

        e_sets = tk.Entry(row_frame, font=LABEL_FONT, width=_NUM_W)
        e_sets.insert(0, str(sets))
        e_sets.pack(side="left", padx=(4, 0))

        e_reps = tk.Entry(row_frame, font=LABEL_FONT, width=_NUM_W)
        e_reps.insert(0, str(reps))
        e_reps.pack(side="left", padx=(4, 0))

        # Day-toggle buttons.
        day_frame = tk.Frame(row_frame)
        day_frame.pack(side="left", padx=(8, 0))
        initial_states = _days_to_states(days)
        day_btns = []
        for label in _DAY_LABELS:
            btn = tk.Button(
                day_frame, text=label, font=_DAY_BTN_FONT,
                width=2, bd=1, padx=0, pady=1,
            )
            btn.pack(side="left", padx=1)
            day_btns.append(btn)

        row = {
            "frame": row_frame,
            "name": e_name,
            "sets": e_sets,
            "reps": e_reps,
            "_original": original,
            "day_btns": day_btns,
            "day_vars": initial_states,
        }

        # Configure button commands and initial appearance now that row dict exists.
        for idx, btn in enumerate(day_btns):
            btn.config(command=lambda i=idx, r=row: self._toggle_day(r, i))
            self._update_day_btn(btn, initial_states[idx])
            btn.bind("<MouseWheel>", self._on_mousewheel)

        btn_remove = tk.Button(
            row_frame, text="Remove", font=LABEL_FONT,
            command=lambda r=row: self._remove_row(r),
        )
        btn_remove.pack(side="left", padx=(8, 0))
        self._rows.append(row)

        for widget in (row_frame, e_name, e_sets, e_reps, day_frame, btn_remove):
            widget.bind("<MouseWheel>", self._on_mousewheel)

    def _add_blank_row(self):
        self._add_exercise_row()

    def _remove_row(self, row):
        row["frame"].destroy()
        self._rows.remove(row)

    # ------------------------------------------------------------------
    # Day-toggle helpers
    # ------------------------------------------------------------------

    def _toggle_day(self, row, day_idx):
        """Toggle a day button; blocks deselecting the last active day."""
        states = row["day_vars"]
        if states[day_idx] and sum(states) == 1:
            return  # would leave no days — block it
        states[day_idx] = not states[day_idx]
        self._update_day_btn(row["day_btns"][day_idx], states[day_idx])

    def _update_day_btn(self, btn, active):
        if active:
            btn.config(bg=_DAY_ACTIVE_BG, relief="sunken")
        else:
            btn.config(bg=_DAY_INACTIVE_BG, relief="raised")

    def _days_value_from_row(self, row):
        """Return 'daily' if all days are selected, else a sorted list of isoweekday ints."""
        states = row["day_vars"]
        if all(states):
            return "daily"
        return [i + 1 for i, active in enumerate(states) if active]

    # ------------------------------------------------------------------
    # Scroll
    # ------------------------------------------------------------------

    def _on_mousewheel(self, event):
        if self._ex_canvas is not None:
            self._ex_canvas.yview_scroll(-1 * (event.delta // 120), "units")

    # ------------------------------------------------------------------
    # Validation helpers
    # ------------------------------------------------------------------

    def _validate_field(self, entry, err_label=None):
        """Parse entry as a positive integer. Returns the int on success, None on failure."""
        val = entry.get().strip()
        try:
            n = int(val)
            if n <= 0:
                raise ValueError
        except ValueError:
            entry.config(background=ENTRY_ERROR_BG)
            if err_label is not None:
                err_label.config(text="Must be a positive integer")
            return None
        entry.config(background=self._normal_entry_bg)
        if err_label is not None:
            err_label.config(text="")
        return n

    def _validate_name_field(self, entry):
        """Validate entry as a non-empty string. Returns stripped value or None."""
        val = entry.get().strip()
        if not val:
            entry.config(background=ENTRY_ERROR_BG)
            return None
        entry.config(background=self._normal_entry_bg)
        return val

    def _validate_exercises(self):
        """Validate all exercise rows. Returns list of exercise dicts or None if any are invalid."""
        if not self._rows:
            return None
        ok = True
        result = []
        for row in self._rows:
            name = self._validate_name_field(row["name"])
            sets_val = self._validate_field(row["sets"])
            reps_val = self._validate_field(row["reps"])
            days = self._days_value_from_row(row)
            # Sanity check: toggle logic guarantees at least one day, but verify.
            days_ok = days == "daily" or bool(days)
            if name is None or sets_val is None or reps_val is None or not days_ok:
                ok = False
            else:
                # Preserve any unknown fields from the original; overwrite known ones.
                ex = dict(row["_original"]) if row["_original"] else {}
                ex["name"] = name
                ex["sets"] = sets_val
                ex["reps"] = reps_val
                ex["days"] = days
                result.append(ex)
        return result if ok else None

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------

    def _on_save(self):
        # Validate both tabs before writing anything.
        interval = self._validate_field(self._entry_interval, self._err_interval)
        snooze = self._validate_field(self._entry_snooze, self._err_snooze)
        new_exercises = self._validate_exercises()

        if interval is None or snooze is None or new_exercises is None:
            return

        cfg = dict(exercises.get_config())
        cfg["interval_minutes"] = interval
        cfg["snooze_minutes"] = snooze
        cfg["exercises"] = new_exercises
        try:
            exercises.save_config(cfg)
            exercises.reload_config()
            exercises.reset_cycler()
        except OSError:
            return  # disk error — leave in-memory state unchanged

        if self._on_exercises_update:
            self._on_exercises_update()
        if self._on_timer_update:
            self._on_timer_update(interval * 60, snooze * 60)


# ------------------------------------------------------------------
# Module-level helpers (no UI state)
# ------------------------------------------------------------------

def _days_to_states(days):
    """Convert a days value ('daily' or list of isoweekday ints) to a list of 7 booleans."""
    if days == "daily":
        return [True] * 7
    return [(i + 1) in days for i in range(7)]
