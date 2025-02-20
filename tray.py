from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QIcon
from settings_window import SettingsWindow
from api_client import APIClient
from settings_manager import settings
import logging

class Tray(QSystemTrayIcon):
    def __init__(self, screen_manager, api_client: APIClient):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.api_client = api_client
        self.setIcon(QIcon("assets/offline_or_connection_failed.png"))
        self.menu = QMenu()
        self.settings = SettingsWindow(screen_manager)
        self.settings.settings_updated.connect(self.on_settings_updated)
        self.settings.settings_updated.connect(self.api_client.on_settings_updated)
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

    def on_settings_updated(self):
        # Use the settings_manager instead of SettingsWindow
        api_enabled = settings.current_settings['api']['enabled']

        if not api_enabled:
            self.api_client.stop_polling()
            self.logger.info("API disabled in settings")
            return

        was_polling = self.api_client.timer.isActive()
        if was_polling:
            self.api_client.stop_polling()
            self.api_client.start_polling()
            self.logger.info("Settings updated, polling restarted with new interval")