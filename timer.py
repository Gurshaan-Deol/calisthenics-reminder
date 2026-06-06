import history


READY_TEXT = "Ready when you are"


def format_time(seconds):
    m, s = divmod(seconds, 60)
    return f"{m:02d}:{s:02d}"


class Timer:
    def __init__(self, root, interval_seconds, snooze_seconds, on_ring, on_tick,
                 mode="fixed", on_rest_end=None):
        self._root = root
        self._interval = interval_seconds
        self._snooze = snooze_seconds
        self._remaining = interval_seconds
        self._on_ring = on_ring
        self._on_tick = on_tick
        # on_rest_end fires when log-mode rest countdown reaches zero; defaults to on_ring.
        self._on_rest_end = on_rest_end if on_rest_end is not None else on_ring
        self._mode = mode
        self._waiting = (mode == "log")
        self._tick()

    def set_mode(self, mode):
        """Switch between 'fixed' and 'log' modes, resetting the countdown state."""
        if mode == "fixed":
            self._mode = mode
            self._waiting = False
            self._remaining = self._interval
        elif mode == "log":
            self._mode = mode
            self._waiting = True
            self._remaining = self._interval
        else:
            raise ValueError(f"Unknown timer mode: {mode!r}")

    def snooze(self):
        self._remaining += self._snooze

    def reset(self):
        history.log_set()
        self._remaining = self._interval
        if self._mode == "log":
            self._waiting = False  # begin the rest countdown

    def _tick(self):
        if self._mode == "log" and self._waiting:
            self._on_tick(READY_TEXT)
        else:
            self._on_tick(format_time(self._remaining))
            if self._remaining > 0:
                self._remaining -= 1
            else:
                if self._mode == "log":
                    self._on_rest_end()
                    self._waiting = True
                else:
                    self._on_ring()
                self._remaining = self._interval
        self._root.after(1000, self._tick)
