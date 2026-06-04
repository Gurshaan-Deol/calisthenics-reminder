# Calisthenics Reminder

A lightweight Windows desktop app that reminds you to do calisthenics exercises throughout the day. Built with Python and Tkinter — minimal memory footprint, no browser, no Electron.

## Features (V1)

- Always-on-top countdown panel showing time to next set
- Desktop notification + sound when the timer hits zero
- Snooze (+5 min) and Done buttons to control the timer
- Exercises cycle in order from config
- System tray icon — show/hide the panel or quit from the tray
- Launches automatically on Windows startup

## Planned (V2+)

- Per-exercise day scheduling (daily / specific days)
- Log-a-set mode: timer starts after you mark a set done
- Daily set tracking and history view
- In-app settings UI

## Requirements

- Windows 10 or 11
- Python 3.8+
- See `requirements.txt` for Python dependencies

## Setup

1. Clone the repo:
   ```
   git clone https://github.com/YOUR_USERNAME/calisthenics-reminder.git
   cd calisthenics-reminder
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Edit `config.json` to set your exercises and interval (see Configuration below).

4. Run the app:
   ```
   python main.py
   ```

5. To enable autostart on login, run:
   ```
   python main.py --autostart
   ```
   To disable:
   ```
   python main.py --remove-autostart
   ```

## Configuration

Edit `config.json` to customise your workout:

```json
{
  "interval_minutes": 45,
  "snooze_minutes": 5,
  "exercises": [
    { "name": "Pull-ups", "sets": 3, "reps": 8 },
    { "name": "Push-ups", "sets": 3, "reps": 15 },
    { "name": "Dips",     "sets": 3, "reps": 10 }
  ]
}
```

| Field              | Description                                      |
|--------------------|--------------------------------------------------|
| `interval_minutes` | How often to be reminded (in minutes)            |
| `snooze_minutes`   | How long the snooze button delays the next alert |
| `exercises`        | List of exercises to cycle through in order      |
| `name`             | Exercise name shown in the panel                 |
| `sets`             | Number of sets shown in the panel                |
| `reps`             | Number of reps shown in the panel                |

## Usage

- The panel sits in the corner of your screen showing a countdown to the next set.
- When the timer hits zero, a desktop notification and sound will fire.
- Click **Done** to log the set and reset the timer.
- Click **Snooze** to delay the next reminder by `snooze_minutes`.
- Right-click the system tray icon to show/hide the panel or quit.

## Project Structure

```
calisthenics-reminder/
├── main.py          # Entry point
├── config.json      # User configuration
├── requirements.txt # Python dependencies
└── README.md        # This file
```

## Contributing

This is a personal tool but PRs are welcome. Keep it lightweight — no new dependencies without a good reason.

## License

MIT
