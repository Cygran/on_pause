from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox, QComboBox, QFrame, QCheckBox, QSpinBox
from PySide6.QtCore import Signal
from screen_utils import ScreenManager, ScreenCorner
from settings_manager import settings

class SettingsWindow(QDialog):
    settings_updated = Signal()
    
    def __init__(self, screen_manager: ScreenManager):
        super().__init__()
        self.screen_manager = screen_manager
        self.screen_manager.screens_changed.connect(self.update_screen_list)
        self.settings_data = {}
        self.setWindowTitle("Settings")
        self.setFixedSize(300, 400)
        
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
        
        self.corner_label = QLabel("Select Corner:")
        layout.addWidget(self.corner_label)

        self.corner_combo = QComboBox()
        self.corner_combo.addItems(['top_right', 'top_left', 'bottom_right', 'bottom_left'])
        layout.addWidget(self.corner_combo)
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save)
        layout.addWidget(self.save_button)

        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(self.separator)

        self.api_settings_label = QLabel("API Settings")
        self.api_settings_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.api_settings_label)

        self.api_enabled = QCheckBox("Enable API")
        layout.addWidget(self.api_enabled)

        self.base_url_label = QLabel("Base URL:")
        layout.addWidget(self.base_url_label)
        self.base_url_input = QLineEdit()
        layout.addWidget(self.base_url_input)

        self.endpoint_label = QLabel("Endpoint:")
        layout.addWidget(self.endpoint_label)
        self.endpoint_input = QLineEdit()
        layout.addWidget(self.endpoint_input)

        self.polling_label = QLabel("Polling Interval (seconds):")
        layout.addWidget(self.polling_label)
        self.polling_input = QSpinBox()
        self.polling_input.setRange(1, 3600)
        layout.addWidget(self.polling_input)

        if settings.current_settings.get("Agent"):
            self.input.setText(settings.current_settings["Agent"])
        if settings.current_settings.get("Screen"):
            self.screen_combo.setCurrentIndex(settings.current_settings["Screen"])
        if settings.current_settings.get("Corner"):
            self.corner_combo.setCurrentText(settings.current_settings["Corner"])
        if settings.current_settings.get("api"):
            self.api_enabled.setChecked(settings.current_settings["api"].get("enabled", False))
            self.base_url_input.setText(settings.current_settings["api"].get("base_url", ""))
            self.endpoint_input.setText(settings.current_settings["api"].get("endpoint", ""))
            self.polling_input.setValue(settings.current_settings["api"].get("polling_interval", 60))

    def showEvent(self, event):
        """Center settings window when shown"""
        super().showEvent(event)
        frame_geometry = self.frameGeometry()
        screen_center = self.screen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

    def update_screen_list(self):
        self.screen_combo.clear()
        screen_names = self.screen_manager.get_screen_names()
        self.screen_combo.addItems(screen_names)

    def save(self):
        self.settings_data = {
            "Agent": self.input.text(),
            "Screen": self.screen_combo.currentIndex(),
            "Corner": self.corner_combo.currentText(),
            "api": {
                "enabled": self.api_enabled.isChecked(),
                "base_url": self.base_url_input.text(),
                "endpoint": self.endpoint_input.text(),
                "polling_interval": self.polling_input.value()
            }
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