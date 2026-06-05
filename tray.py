import threading

from PIL import Image
import pystray


_ICON_SIZE = 64
_ICON_COLOR = "#89b4fa"


def _make_tray_image():
    return Image.new("RGB", (_ICON_SIZE, _ICON_SIZE), color=_ICON_COLOR)


class TrayIcon:
    def __init__(self, title, on_toggle, on_quit):
        menu = pystray.Menu(
            pystray.MenuItem(
                "Show / Hide",
                lambda icon, item: on_toggle(),
            ),
            pystray.MenuItem("Quit", lambda icon, item: on_quit()),
        )
        self._icon = pystray.Icon("calisthenics", _make_tray_image(), title, menu)
        threading.Thread(target=self._icon.run, daemon=True).start()

    def stop(self):
        self._icon.stop()
