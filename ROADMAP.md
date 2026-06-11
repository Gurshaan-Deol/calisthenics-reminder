# Roadmap

## V1 — Core ✅

- [x] `init: project scaffold, config.json, requirements.txt, README`
- [x] `feat: always-on-top countdown window`
- [x] `feat: exercise cycling from config`
- [x] `feat: desktop notification + sound on timer end`
- [x] `feat: snooze and done buttons`
- [x] `feat: system tray icon`
- [x] `feat: windows autostart on login`

## V2 — Scheduling + Tracking ✅

- [x] `feat: day scheduling per exercise in config and exercises.py`
- [x] `feat: daily set tracking saved to history.json`
- [x] `feat: history summary expanded in panel`
- [x] `feat: log-a-set timer mode`
- [x] `feat: switch timer mode from tray menu`

## V3 — Settings ✅

- [x] `feat: settings window scaffold opened from tray menu`
- [x] `feat: timer settings (interval and snooze) editable in settings window`
- [x] `feat: exercise list editable in settings window (add, edit, remove)`
- [x] `feat: day scheduling editable per exercise in settings window`
- [x] `chore: final polish pass — edge cases, live reload, panel cleanup`

## Known Limitations

These are intentionally out of scope and will not be addressed in the current version:

- **No per-exercise day editing from the panel** — the days field is only editable in the Settings window, not from the main panel.
- **History is not editable** — past sets logged to `history.json` can only be cleared by deleting or editing the file manually.
- **Timer does not persist across restarts** — closing and reopening the app resets the countdown to the full interval.
- **Single-monitor / taskbar-at-bottom assumption** — the panel positions itself relative to the bottom-right corner using fixed margins; taskbars docked to other edges may overlap the panel.
- **Log mode rest-end sound is the same as the ring sound** — there is no distinct audio cue to differentiate "time to work out" from "rest is over".
- **No import/export for history** — `history.json` is a plain file in the app directory; portability is the user's responsibility.
