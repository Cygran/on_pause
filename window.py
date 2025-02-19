from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt
from tray import Tray

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Queue Status")
        self.setFixedSize(400, 150)
        self.move(1520, 0)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        
        self.tray = Tray()

    