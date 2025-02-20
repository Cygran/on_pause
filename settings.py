from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox
from PySide6.QtCore import Signal
import os
import json
from constants import SETTINGS_PATH, SETTINGS_FILE, CURRENT_SETTINGS

class SettingsWindow(QDialog):
    settings_updated = Signal()
    
    def __init__(self):
        super().__init__()
        self.settings_data = {}
        self.setWindowTitle("Settings")
        self.setFixedSize(200, 100)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.label = QLabel("Agent Number:")
        layout.addWidget(self.label)
        
        self.input = QLineEdit()
        layout.addWidget(self.input)
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save)
        layout.addWidget(self.save_button)

        if CURRENT_SETTINGS.get("Agent"):
            self.input.setText(CURRENT_SETTINGS["Agent"])

    def save(self):
        self.settings_data = {
            "Agent": self.input.text()
        }
        try:
            os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.settings_data, f, ensure_ascii=False, indent=4)
            
            global CURRENT_SETTINGS, SETTINGS_VALID
            CURRENT_SETTINGS.update(self.settings_data)
            SETTINGS_VALID = bool(self.input.text() and self.input.text().isdigit())
            
            self.settings_updated.emit()
            self.close()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to save settings: {str(e)}"
            )