import history


def format_time(seconds):
    m, s = divmod(seconds, 60)
    return f"{m:02d}:{s:02d}"


class Timer:
    def __init__(self, root, interval_seconds, snooze_seconds, on_ring, on_tick):
        self._root = root
        self._interval = interval_seconds
        self._snooze = snooze_seconds
        self._remaining = interval_seconds
        self._on_ring = on_ring
        self._on_tick = on_tick
        self._tick()

    def snooze(self):
        self._remaining += self._snooze

    def reset(self):
        history.log_set()
        self._remaining = self._interval

    def _tick(self):
        self._on_tick(format_time(self._remaining))
        if self._remaining > 0:
            self._remaining -= 1
        else:
            self._on_ring()
            self._remaining = self._interval
        self._root.after(1000, self._tick)
