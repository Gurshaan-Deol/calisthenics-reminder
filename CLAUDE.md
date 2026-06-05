# Claude Code Instructions

This file tells Claude Code how to work on this project. Read it before making any changes.

## Project goals

A lightweight Windows calisthenics reminder app. The top priority after correctness is **low memory usage**. Every dependency and design decision should be justified against that constraint.

## Tech stack

- **Python 3.8+** — no newer syntax unless necessary
- **Tkinter** — built-in, used for the always-on-top panel (no external UI frameworks)
- **plyer** — desktop notifications
- **pystray** — system tray icon
- **Pillow** — required by pystray for the tray icon image
- **No other dependencies** — do not add new packages without flagging it first

## Architecture

Flat module layout:

```
main.py        # entry point, argparse (--autostart / --remove-autostart), CountdownApp wiring
exercises.py   # load_config(), ExerciseCycler (current/advance)
timer.py       # format_time(), Timer class (after() loop, snooze, reset)
tray.py        # TrayIcon class (pystray icon, Show/Hide/Quit menu)
ui.py          # Panel class (Tkinter window, labels, buttons, positioning)
config.json    # user config, loaded at startup
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

## V1 commit plan (follow this order)

1. `init: project scaffold, config.json, requirements.txt, README` ✅
2. `feat: always-on-top countdown window`
3. `feat: exercise cycling from config`
4. `feat: desktop notification + sound on timer end`
5. `feat: snooze and done buttons`
6. `feat: system tray icon`
7. `feat: windows autostart on login`

## Coding rules

- Keep functions short and single-purpose
- No global mutable state unless unavoidable (timer state is fine)
- Config is loaded once at startup from `config.json` — do not hot-reload in V1
- The countdown panel must always stay on top (`wm_attributes('-topmost', True)`)
- Sound must use a built-in Windows sound (e.g. `winsound`) — do not bundle audio files
- All user-facing strings should be easy to find (no strings buried deep in logic)
- Handle missing or malformed `config.json` gracefully with clear error messages

## Things to avoid

- Do not use threading unless necessary — use Tkinter's `after()` for the timer
- Do not use `time.sleep()` on the main thread
- Do not import anything not in the standard library or `requirements.txt`
- Do not add a database — any tracking in V2 uses a plain JSON file
- Do not use `subprocess` to spawn other processes
