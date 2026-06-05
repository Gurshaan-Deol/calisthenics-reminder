import json
import sys


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

    return cfg


class ExerciseCycler:
    def __init__(self, exercises):
        self._exercises = exercises
        self._index = 0

    def current(self):
        return self._exercises[self._index]

    def advance(self):
        self._index = (self._index + 1) % len(self._exercises)
        return self.current()
