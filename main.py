import argparse
import os
import sys
import tkinter as tk
import winreg
import winsound

from plyer import notification

from exercises import load_config, ExerciseCycler
from settings import SettingsWindow
from timer import Timer
from tray import TrayIcon
from ui import Panel, WINDOW_TITLE


AUTOSTART_NAME = "CalisthenicsReminder"
AUTOSTART_KEY = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
NOTIFICATION_TIMEOUT = 8


def _get_pythonw():
    """Return pythonw.exe path when available so autostart doesn't open a console window."""
    exe = sys.executable
    if exe.lower().endswith("python.exe"):
        candidate = exe[:-len("python.exe")] + "pythonw.exe"
        if os.path.exists(candidate):
            return candidate
    return exe


def add_autostart():
    script = os.path.abspath(__file__)
    cmd = f'"{_get_pythonw()}" "{script}"'
    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER, AUTOSTART_KEY, 0, winreg.KEY_SET_VALUE
    ) as key:
        winreg.SetValueEx(key, AUTOSTART_NAME, 0, winreg.REG_SZ, cmd)
    print(f"Autostart added: {cmd}")


def remove_autostart():
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, AUTOSTART_KEY, 0, winreg.KEY_SET_VALUE
        ) as key:
            winreg.DeleteValue(key, AUTOSTART_NAME)
        print("Autostart removed.")
    except FileNotFoundError:
        print("Autostart entry not found — nothing to remove.")


class CountdownApp:
    def __init__(self, root, cfg):
        self.root = root
        self._cycler = ExerciseCycler(cfg["exercises"])
        interval = int(cfg["interval_minutes"] * 60)
        snooze = int(cfg["snooze_minutes"] * 60)

        self._panel = Panel(
            root,
            initial_exercise=self._cycler.current(),
            on_done=self._on_done,
            on_snooze=self._on_snooze,
        )
        self._timer = Timer(
            root,
            interval_seconds=interval,
            snooze_seconds=snooze,
            on_ring=self._on_ring,
            on_tick=self._panel.set_time,
            on_rest_end=self._on_rest_end,
        )
        self._settings = SettingsWindow(
            root,
            on_timer_update=lambda i, s: self._timer.apply_config(i, s),
            on_exercises_update=self._on_exercises_update,
        )
        self._tray = TrayIcon(
            WINDOW_TITLE,
            on_toggle=lambda: root.after(0, self._panel.toggle),
            on_quit=self._quit,
            on_mode_switch=lambda mode: root.after(0, lambda: self._on_mode_switch(mode)),
            on_settings=lambda: root.after(0, self._settings.open),
        )

    def _on_done(self):
        ex = self._cycler.advance()
        self._panel.set_exercise(ex["name"], ex["sets"], ex["reps"])
        self._timer.reset()

    def _on_snooze(self):
        self._timer.snooze()

    def _on_ring(self):
        ex = self._cycler.advance()
        self._panel.set_exercise(ex["name"], ex["sets"], ex["reps"])
        notification.notify(
            title="Time to move!",
            message=f"{ex['name']} — {ex['sets']} sets × {ex['reps']} reps",
            app_name=WINDOW_TITLE,
            timeout=NOTIFICATION_TIMEOUT,
        )
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)

    def _on_exercises_update(self):
        ex = self._cycler.current()
        self._panel.set_exercise(ex["name"], ex["sets"], ex["reps"])

    def _on_mode_switch(self, mode):
        self._timer.set_mode(mode)
        self._panel.set_mode_label(mode)

    def _on_rest_end(self):
        ex = self._cycler.current()
        notification.notify(
            title="Rest over!",
            message=f"Ready for {ex['name']} — {ex['sets']} sets × {ex['reps']} reps",
            app_name=WINDOW_TITLE,
            timeout=NOTIFICATION_TIMEOUT,
        )
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)

    def _quit(self):
        self._tray.stop()
        self.root.after(0, self.root.destroy)


def main():
    parser = argparse.ArgumentParser(description=WINDOW_TITLE)
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--autostart", action="store_true",
        help="Register app to run on Windows login",
    )
    group.add_argument(
        "--remove-autostart", action="store_true",
        help="Remove app from Windows login startup",
    )
    args = parser.parse_args()

    if args.autostart:
        add_autostart()
        return
    if args.remove_autostart:
        remove_autostart()
        return

    cfg = load_config()
    root = tk.Tk()
    CountdownApp(root, cfg)
    root.mainloop()


if __name__ == "__main__":
    main()
