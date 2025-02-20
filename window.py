from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt
from tray import Tray
from screen_utils import ScreenManager
from constants import SETTINGS_VALID, CURRENT_SETTINGS

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        initial_title = f"On Pause - EXT {CURRENT_SETTINGS.get('Agent', '')}" if SETTINGS_VALID else "On Pause - Please set your EXT number"
        self.screen_manager = ScreenManager()
        self.setWindowTitle(initial_title)
        self.setFixedSize(400, 150)
        self.move(1520, 0)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        
        self.tray = Tray()

        self.tray.settings.settings_updated.connect(self.on_settings_updated)

        if not SETTINGS_VALID:
            self.tray.settings.show()

    def on_settings_updated(self):
        self.setWindowTitle(f"On Pause - EXT {CURRENT_SETTINGS['Agent']}")