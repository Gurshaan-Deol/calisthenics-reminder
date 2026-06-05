import datetime
import json


_HISTORY_FILE = "history.json"

# Staging slot: exercises.py writes the about-to-be-completed exercise name here
# before advancing; timer.py consumes it inside reset() (Done-button path only).
_staged = None


def _stage(exercise_name):
    """Called by ExerciseCycler.advance() to record which exercise is being completed."""
    global _staged
    _staged = exercise_name


def log_set(exercise_name=None):
    """Append a completed set to history.json.

    If exercise_name is omitted, uses the value staged by _stage().
    Creates history.json if it does not exist. Never raises on missing or corrupt file.
    """
    global _staged
    name = exercise_name if exercise_name is not None else _staged
    _staged = None
    if not name:
        return

    today = datetime.date.today().isoformat()
    timestamp = datetime.datetime.now().isoformat(timespec="seconds")

    try:
        with open(_HISTORY_FILE, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    if today not in data:
        data[today] = []
    data[today].append({"exercise": name, "timestamp": timestamp})

    with open(_HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_today():
    """Return all set records logged today, or [] if none / file missing."""
    today = datetime.date.today().isoformat()
    try:
        with open(_HISTORY_FILE, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    return data.get(today, [])
