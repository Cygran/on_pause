from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon
import sys

app = QApplication(sys.argv)
tray = QSystemTrayIcon()
tray.setIcon(QIcon("assets/icon.png"))

menu = QMenu()
menu.addAction("Exit").triggered.connect(app.quit)
tray.setContextMenu(menu)

tray.setVisible(True)
sys.exit(app.exec())