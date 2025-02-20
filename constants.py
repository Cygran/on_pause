from platformdirs import user_data_dir
from settings import SettingsWindow
import os



SETTINGS_PATH = user_data_dir("On Pause", "Cygran")
SETTINGS_FILE = os.path.join(SETTINGS_PATH, "user_settings.json")
CURRENT_SETTINGS, SETTINGS_VALID = SettingsWindow.load_settings()

