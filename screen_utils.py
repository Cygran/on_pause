from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QScreen
from enum import Enum

screens = QApplication.screens()
primary_screen = QApplication.primaryScreen()
screen_count = len(screens)

class ScreenCorner(Enum):
    Top_Left = "top_left"
    Top_Right = "top_right"
    Bottom_Left = "bottom_left"
    BottomRight = "bottom_right"


class ScreenManager:
    def __init__(self):
        self.screens = QApplication.screens()
        self.primary_screen = QApplication.primaryScreen()
        QApplication.instance().screenAdded.connect(self.handle_screen_change)
        QApplication.instance().screenRemoved.connect(self.handle_screen_change)

    def handle_screen_change(self, screen: QScreen):
        self.screens = QApplication.screens()
        self.primary_screen = QApplication.primaryScreen()


    def get_safe_screen(screen_index=0) -> QScreen:
        if screen_index >= len(screens):
            return primary_screen
        return screens[screen_index]

    def get_corner_position(screen: QScreen, corner: ScreenCorner, window_width, window_height):
        available = screen.availableGeometry()
        geometry = screen.geometry()
        useable_width = available.width()
        useable_height = available.height()

        match corner:
            case ScreenCorner.Top_Left:
                return (available.left(), available.top())
            case ScreenCorner.Top_Right:
                return (available.right() - window_width, available.top())
            case ScreenCorner.Bottom_Left:
                return (available.left(), available.bottom() - window_height)
            case ScreenCorner.BottomRight:
                return (available.right() - window_width, available.bottom() - window_height)
            
    def get_screen_names(self) -> list[str]:
        return [f"Screen {i}" for i, screen in enumerate(self.screens)]
    
    def get_screen_count(self) -> int:
        return len(self.screens)