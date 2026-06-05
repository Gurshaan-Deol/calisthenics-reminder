import datetime
import json
import sys


# Returned by ExerciseCycler on days when no exercises are scheduled.
REST_DAY_EXERCISE = {"name": "No exercises today", "sets": 0, "reps": 0}


def _is_scheduled(exercise):
    """True if the exercise is scheduled for today's weekday (1=Mon … 7=Sun)."""
    days = exercise.get("days", "daily")
    if days == "daily":
        return True
    return datetime.date.today().isoweekday() in days


def _validate_days(days_val, exercise_name):
    if days_val == "daily":
        return
    if not isinstance(days_val, list) or not days_val:
        sys.exit(
            f"Error: '{exercise_name}' days must be \"daily\" or a non-empty list of integers."
        )
    for d in days_val:
        if not isinstance(d, int) or not (1 <= d <= 7):
            sys.exit(
                f"Error: '{exercise_name}' days list must contain integers between 1 and 7."
            )


def load_config(path="config.json"):
    try:
        with open(path, "r") as f:
            cfg = json.load(f)
    except FileNotFoundError:
        sys.exit(f"Error: '{path}' not found. Create it before running.")
    except json.JSONDecodeError as e:
        sys.exit(f"Error: '{path}' is not valid JSON — {e}")

    for key in ("interval_minutes", "snooze_minutes", "exercises"):
        if key not in cfg:
            sys.exit(f"Error: config.json is missing '{key}'.")
    if not cfg["exercises"]:
        sys.exit("Error: config.json must contain at least one exercise.")

    for ex in cfg["exercises"]:
        if "days" in ex:
            _validate_days(ex["days"], ex.get("name", "unnamed"))

    return cfg


class ExerciseCycler:
    def __init__(self, exercises):
        self._exercises = exercises
        self._index = self._first_scheduled()

    def _first_scheduled(self):
        """Return the index of the first exercise scheduled for today, or None."""
        for i, ex in enumerate(self._exercises):
            if _is_scheduled(ex):
                return i
        return None

    def has_today(self):
        """True if at least one exercise is scheduled for today."""
        return self._index is not None

    def current(self):
        if self._index is None:
            return REST_DAY_EXERCISE
        return self._exercises[self._index]

    def advance(self):
        if self._index is None:
            return REST_DAY_EXERCISE
        n = len(self._exercises)
        for step in range(1, n + 1):
            candidate = (self._index + step) % n
            if _is_scheduled(self._exercises[candidate]):
                self._index = candidate
                return self._exercises[self._index]
        # Every exercise became unscheduled mid-run (e.g. midnight crossed).
        self._index = None
        return REST_DAY_EXERCISE
