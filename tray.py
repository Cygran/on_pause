from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QIcon

class Tray(QSystemTrayIcon):
    def __init__(self):
        super().__init__()
        self.setIcon(QIcon("assets/icon.png"))
        self.menu = QMenu()
        self.menu.addAction("Exit").triggered.connect(QApplication.instance().quit)
        self.setContextMenu(self.menu)
        self.setVisible(True)
    