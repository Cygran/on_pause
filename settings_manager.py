import os
import json
from platformdirs import user_data_dir

class SettingsManager:
    def __init__(self):
        self.settings_path = user_data_dir("On Pause", "Cygran")
        self.settings_file = os.path.join(self.settings_path, "user_settings.json")
        self.default_settings = {
            'Screen': 0,
            'Corner': 'top_right',
            'Agent': ''
        }
        self.current_settings, self.settings_valid = self._load_settings()

    def _load_settings(self):
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    current_settings = json.load(f)
                    # Merge with defaults for any missing settings
                    for key, value in self.default_settings.items():
                        if key not in current_settings:
                            current_settings[key] = value
                    settings_valid = bool(current_settings.get('Agent', '').isdigit())
            else:
                current_settings = self.default_settings.copy()
                settings_valid = False
        except Exception as e:
            print(f"Error loading settings: {e}")
            current_settings = self.default_settings.copy()
            settings_valid = False
        
        return current_settings, settings_valid

    def save_settings(self, new_settings):
        os.makedirs(self.settings_path, exist_ok=True)
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump(new_settings, f)
        self.current_settings = new_settings
        self.settings_valid = bool(new_settings.get('Agent', '').isdigit())

settings = SettingsManager()