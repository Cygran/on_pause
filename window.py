from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt
from tray import Tray
from screen_utils import ScreenManager
from settings_manager import settings

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        initial_title = f"On Pause - EXT {settings.current_settings.get('Agent', '')}" if settings.settings_valid else "On Pause - Please set your EXT number"
        self.screen_manager = ScreenManager()
        self.setWindowTitle(initial_title)
        self.setFixedSize(400, 150)
        self.move(1520, 0)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        
        self.tray = Tray(screen_manager=self.screen_manager)

        self.tray.settings.settings_updated.connect(self.on_settings_updated)

        if not settings.settings_valid:
            self.tray.settings.show()

    def on_settings_updated(self):
        self.setWindowTitle(f"On Pause - EXT {settings.current_settings['Agent']}")