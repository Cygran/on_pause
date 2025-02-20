from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QScreen
from PySide6.QtCore import QObject, Signal
from enum import Enum

class ScreenCorner(Enum):
    Top_Left = "top_left"
    Top_Right = "top_right"
    Bottom_Left = "bottom_left"
    Bottom_Right = "bottom_right"

    @classmethod
    def from_string(cls, corner_str: str):
        """Convert string to enum value safely"""
        try:
            return cls(corner_str)
        except ValueError:
            return cls.Top_Right  # default

class ScreenManager(QObject):
    screens_changed = Signal()
    
    def __init__(self):
        super().__init__()
        self.screens = QApplication.screens()
        self.primary_screen = QApplication.primaryScreen()
        QApplication.instance().screenAdded.connect(self.handle_screen_change)
        QApplication.instance().screenRemoved.connect(self.handle_screen_change)

    def handle_screen_change(self, _):
        self.screens = QApplication.screens()
        self.primary_screen = QApplication.primaryScreen()
        self.screens_changed.emit()

    def get_screen_names(self):
        """Return list of screen names/identifiers"""
        return [f"Screen {i+1}" for i in range(len(self.screens))]

    def get_safe_screen(self, screen_index = 0) -> QScreen:
        if screen_index >= len(self.screens):
            return self.primary_screen
        return self.screens[screen_index]

    def position_window(self, window, screen_index: int, corner: ScreenCorner):
        screen = self.get_safe_screen(screen_index)
        available = screen.availableGeometry()
        window_width = window.width()
        window_height = window.height()
        
        if corner == ScreenCorner.Top_Left:
            x, y = available.left(), available.top()
        elif corner == ScreenCorner.Top_Right:
            x, y = available.right() - window_width, available.top()
        elif corner == ScreenCorner.Bottom_Left:
            x, y = available.left(), available.bottom() - window_height
        elif corner == ScreenCorner.Bottom_Right:
            x, y = available.right() - window_width, available.bottom() - window_height
        else:  # default to top right
            x, y = available.right() - window_width, available.top()
            
        window.move(x, y)