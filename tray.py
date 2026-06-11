import threading

from PIL import Image
import pystray


_ICON_SIZE = 64
_ICON_COLOR = "#89b4fa"


def _make_tray_image():
    return Image.new("RGB", (_ICON_SIZE, _ICON_SIZE), color=_ICON_COLOR)


class TrayIcon:
    def __init__(self, title, on_toggle, on_quit, on_mode_switch=None, on_settings=None):
        self._mode = "fixed"
        self._on_mode_switch = on_mode_switch

        menu = pystray.Menu(
            pystray.MenuItem("Show / Hide", lambda icon, item: on_toggle()),
            pystray.MenuItem(
                lambda item: (
                    "Switch to Log Mode" if self._mode == "fixed"
                    else "Switch to Fixed Mode"
                ),
                self._handle_mode_switch,
            ),
            pystray.MenuItem("Settings", lambda icon, item: on_settings() if on_settings else None),
            pystray.MenuItem("Quit", lambda icon, item: on_quit()),
        )
        self._icon = pystray.Icon("calisthenics", _make_tray_image(), title, menu)
        threading.Thread(target=self._icon.run, daemon=True).start()

    def _handle_mode_switch(self, icon, item):
        new_mode = "log" if self._mode == "fixed" else "fixed"
        self._mode = new_mode
        if self._on_mode_switch:
            self._on_mode_switch(new_mode)

    def stop(self):
        self._icon.stop()
