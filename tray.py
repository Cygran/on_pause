from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QIcon
from settings_window import SettingsWindow
from api_client import APIClient

class Tray(QSystemTrayIcon):
    def __init__(self, screen_manager, api_client: APIClient):
        super().__init__()
        self.api_client = api_client
        self.setIcon(QIcon("assets/offline_or_connection_failed.png"))
        self.menu = QMenu()
        self.settings = SettingsWindow(screen_manager)
        self.menu.addAction("Exit").triggered.connect(QApplication.instance().quit)
        self.menu.addAction("Settings").triggered.connect(self.settings.show)
        self.setContextMenu(self.menu)
        self.setVisible(True)
        self.api_client.status_changed.connect(self._handle_status_change)
        self.api_client.poll_error.connect(self._handle_poll_error)

    def _handle_status_change(self, is_paused: bool):
        if is_paused:
            self.setIcon(QIcon("assets/paused.png"))
            self.setToolTip("Agent: Paused")
        else:
            self.setIcon(QIcon("assets/unpaused.png"))
            self.setToolTip("Agent: Active")

    def _handle_poll_error(self, error: str):
        self.setIcon(QIcon("assets/offline_or_connection_failed.png"))
        self.setToolTip(f"Error: {error}")