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
            'Agent': '',
            'api': {
                'base_url': '',
                'endpoint': '/pause',
                'polling_interval': 60,
                'enabled': False
            }
        }
        self.current_settings, self.settings_valid = self._load_settings()

    def _load_settings(self):
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    current_settings = json.load(f)
                    for key, value in self.default_settings.items():
                        if key not in current_settings:
                            current_settings[key] = value
                        if key == 'api':
                            for api_key, api_value in value.items():
                                if api_key not in current_settings['api']:
                                    current_settings['api'][api_key] = api_value

                    settings_valid = self._validate_settings(current_settings)
            else:
                current_settings = self.default_settings.copy()
                settings_valid = False
        except Exception as e:
            print(f"Error loading settings: {e}")
            current_settings = self.default_settings.copy()
            settings_valid = False
        
        return current_settings, settings_valid

    def _validate_settings(self, settings):
        agent_valid = bool(settings.get('Agent', '').isdigit())
        try:
            api_settings = settings.get('api', {})
            api_valid = True
            
            if api_settings.get('enabled', False):
                base_url = api_settings.get('base_url', '').strip()
                if base_url and not (base_url.startswith('http://') or base_url.startswith('https://')):
                    api_valid = False
                
                polling_interval = api_settings.get('polling_interval', 0)
                if not isinstance(polling_interval, (int, float)) or polling_interval <= 0:
                    api_valid = False
                
                endpoint = api_settings.get('endpoint', '').strip()
                if not endpoint:
                    api_valid = False
        except Exception as e:
            print(f"API validation error: {e}")
            api_valid = False
        
        return agent_valid and (not api_settings.get('enabled', False) or api_valid)
   
   
   
    def save_settings(self, new_settings):
        try:
            if 'api' not in new_settings:
                new_settings['api'] = self.default_settings['api'].copy()
            if self._validate_settings(new_settings):
                os.makedirs(self.settings_path, exist_ok=True)
                with open(self.settings_file, 'w', encoding='utf-8') as f:
                    json.dump(new_settings, f)
                self.current_settings = new_settings
                self.settings_valid = True
            else:
                print("Settings validation failed")
                self.settings_valid = False
                
        except Exception as e:
            print(f"Error saving settings: {e}")
            self.settings_valid = False

settings = SettingsManager()