from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox, QComboBox
from PySide6.QtCore import Signal
from screen_utils import ScreenManager
from settings_manager import settings

class SettingsWindow(QDialog):
    settings_updated = Signal()
    
    def __init__(self, screen_manager: ScreenManager):
        super().__init__()
        self.screen_manager = screen_manager
        self.settings_data = {}
        self.setWindowTitle("Settings")
        self.setFixedSize(300, 200)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.label = QLabel("EXT Number:")
        layout.addWidget(self.label)
        
        self.input = QLineEdit()
        layout.addWidget(self.input)

        self.screen_label = QLabel("Select Screen:")
        layout.addWidget(self.screen_label)

        self.screen_combo = QComboBox()
        self.update_screen_list()
        layout.addWidget(self.screen_combo)
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save)
        layout.addWidget(self.save_button)

        if settings.current_settings.get("Agent"):
            self.input.setText(settings.current_settings["Agent"])
        if settings.current_settings.get("Screen"):
            self.screen_combo.setCurrentIndex(settings.current_settings["Screen"])

    def update_screen_list(self):
        self.screen_combo.clear()
        screen_names = self.screen_manager.get_screen_names()
        self.screen_combo.addItems(screen_names)

    def save(self):
        self.settings_data = {
            "Agent": self.input.text(),
            "Screen": self.screen_combo.currentIndex()
        }
        
        if len(self.settings_data["Agent"]) == 0:
            QMessageBox.critical(
                self,
                "Error",
                "Please enter an EXT number"
            )
        elif not self.settings_data["Agent"].isdigit():
            QMessageBox.critical(
                self,
                "Error",
                "Invalid Characters in EXT number"
            )
        elif self.settings_data["Agent"].isdigit() and len(self.settings_data["Agent"]) == 3:
            try:
                settings.save_settings(self.settings_data)
                self.settings_updated.emit()
                self.close()

            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to save settings: {str(e)}"
                )
        else:
            QMessageBox.critical(
                self,
                "Error",
                "EXT number must be a 3-digit number"
            )