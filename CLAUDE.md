# Claude Code Instructions

This file tells Claude Code how to work on this project. Read it before making any changes.

## Project goals

A lightweight Windows calisthenics reminder app. The top priority after correctness is **low memory usage**. Every dependency and design decision should be justified against that constraint.

## Tech stack

- **Python 3.8+** — no newer syntax unless necessary
- **Tkinter** — built-in, used for the always-on-top panel and the settings window (no external UI frameworks)
- **plyer** — desktop notifications
- **pystray** — system tray icon
- **Pillow** — required by pystray for the tray icon image
- **No other dependencies** — do not add new packages without flagging it first

## Architecture

Flat module layout:

```
main.py        # entry point, argparse (--autostart / --remove-autostart), CountdownApp wiring
exercises.py   # load_config(), get_config(), reload_config(), save_config(), ExerciseCycler
timer.py       # format_time(), Timer class (after() loop, snooze, reset, apply_config)
tray.py        # TrayIcon class (pystray icon, Show/Hide/Settings/mode-switch/Quit menu)
ui.py          # Panel class (Tkinter window, labels, buttons, history section, positioning)
settings.py    # SettingsWindow class (Toplevel, ttk.Notebook tabs, Timer + Exercises tabs, Save)
history.py     # log_set(), get_today(), staging slot for Done-button coordination
config.json    # user config, loaded at startup and reloaded on settings save
history.json   # per-day set log, created automatically on first Done click
requirements.txt
README.md
ROADMAP.md
CLAUDE.md      # this file
```

Do not create subfolders or add further modules without a clear reason.

## Commit discipline

- One logical change per commit
- Commit messages follow this format: `type: short description`
- Types: `init`, `feat`, `fix`, `refactor`, `docs`, `chore`
- Do not bundle unrelated changes into a single commit
- Do not commit broken or half-working code

## Coding rules

- Keep functions short and single-purpose
- No global mutable state unless unavoidable — `_config` and `_cycler` in exercises.py and `_staged` in history.py are the accepted exceptions
- Config is loaded at startup from `config.json` and reloaded live when the user saves in the settings window; all modules read config via `exercises.get_config()` at the time they need it rather than caching at startup
- The countdown panel must always stay on top (`wm_attributes('-topmost', True)`)
- The settings window is a normal Toplevel — NOT always-on-top, IS resizable
- Sound must use a built-in Windows sound (`winsound`) — do not bundle audio files
- All user-facing strings should be easy to find (no strings buried deep in logic)
- Handle missing or malformed `config.json` gracefully — `load_config()` calls `sys.exit()` with a clear error message; settings validation prevents writing invalid config
- `history.json` errors are always silently recovered — log and display functions catch `FileNotFoundError` and `json.JSONDecodeError` and return safe defaults

## Things to avoid

- Do not use threading unless necessary — use Tkinter's `after()` for the timer
- Do not use `time.sleep()` on the main thread
- Do not import anything not in the standard library or `requirements.txt`
- Do not add a database — tracking uses `history.json` (plain JSON)
- Do not use `subprocess` to spawn other processes
- Do not call `sys.exit()` from anywhere except startup validation in `load_config()`

## Timer modes

Two modes are supported and switchable from the tray menu:

- **Fixed mode** — counts down a fixed interval; rings and advances exercise on zero
- **Log mode** — waits for "Done" to log the set; then counts down a rest period; rings on rest end without advancing exercise

## Config format

```json
{
  "interval_minutes": 45,
  "snooze_minutes": 5,
  "exercises": [
    { "name": "Pull-ups", "sets": 3, "reps": 8,  "days": "daily" },
    { "name": "Push-ups", "sets": 3, "reps": 15, "days": [1, 3, 5] }
  ]
}
```

`"days"` is either the string `"daily"` or a list of ISO weekday integers (1=Mon … 7=Sun). If omitted, `"daily"` is assumed.

## Live reload flow

When the user saves in the settings window:

1. `exercises.save_config(cfg)` — writes to `config.json`
2. `exercises.reload_config()` — re-reads and updates the in-memory config
3. `exercises.reset_cycler()` — calls `ExerciseCycler.reset()` with the new exercise list, restarting from the first scheduled exercise
4. `on_exercises_update` callback — updates the panel's displayed exercise
5. `on_timer_update` callback — calls `Timer.apply_config()` with new interval/snooze seconds

## Autostart

`python main.py --autostart` registers the app under `HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run`. Uses `pythonw.exe` if available to suppress the console window. `--remove-autostart` removes the entry.
