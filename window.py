from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt
from tray import Tray
from screen_utils import ScreenManager, ScreenCorner
from settings_manager import settings
from api_client import APIClient

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        initial_title = f"On Pause - EXT {settings.current_settings.get('Agent', '')}" if settings.settings_valid else "On Pause - Please set your EXT number"
        self.screen_manager = ScreenManager()
        self.api_client = APIClient(settings)
        self.setWindowTitle(initial_title)
        self.setFixedSize(400, 150)
        self.position_window()
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        
        self.tray = Tray(screen_manager=self.screen_manager)
        self.tray.settings.settings_updated.connect(self.on_settings_updated)
        self.screen_manager.screens_changed.connect(self.handle_screen_change)
        self.api_client.status_changed.connect(self.handle_status_change)
        self.api_client.break_started.connect(self.handle_break_started)
        self.api_client.break_ended.connect(self.handle_break_ended)
        self.api_client.start_polling()
        if not settings.settings_valid:
            self.tray.settings.show()

    def on_settings_updated(self):
        self.setWindowTitle(f"On Pause - EXT {settings.current_settings['Agent']}")
        self.position_window()
    
    def position_window(self):
        selected_screen_index = settings.current_settings.get('Screen', 0)
        selected_corner = ScreenCorner(settings.current_settings.get('Corner', 'top_right'))  # Convert string to enum
        print(f"Moving window to screen {selected_screen_index} and corner {selected_corner}")  # Debug print
        self.screen_manager.position_window(self, selected_screen_index, selected_corner)

    def handle_screen_change(self):
        preferred_screen = settings.current_settings.get("Screen", 0)
        preferred_corner = settings.current_settings.get("Corner", "top_right")
        
        if preferred_screen < len(self.screen_manager.screens):
            self.screen_manager.position_window(
                self, 
                preferred_screen, 
                ScreenCorner.from_string(preferred_corner)
            )
    
    def handle_status_change(self, is_paused):
        if is_paused:
            self.show()
        elif not self.api_client.is_on_break():
            self.hide()
    
    def handle_break_started(self):
        self.show()

    def handle_break_ended(self):
        if not self.api_client.is_queue_paused():
            self.hide()