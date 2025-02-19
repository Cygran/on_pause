from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QIcon
from settings import SettingsWindow

class Tray(QSystemTrayIcon):
    def __init__(self):
        super().__init__()
        self.setIcon(QIcon("assets/icon.png"))
        self.menu = QMenu()
        self.settings = SettingsWindow()
        self.menu.addAction("Exit").triggered.connect(QApplication.instance().quit)
        self.menu.addAction("Settings").triggered.connect(self.settings.show)
        self.setContextMenu(self.menu)
        self.setVisible(True)
