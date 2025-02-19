from platformdirs import user_data_dir
import os
import json

SETTINGS_PATH = user_data_dir("On Pause", "Cygran")
SETTINGS_FILE = os.path.join(SETTINGS_PATH, "user_settings.json")

def load_settings():
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                # Check if Agent exists and is a valid number
                if settings.get("Agent") and settings["Agent"].isdigit():
                    return settings, True
        return {"Agent": ""}, False
    except Exception:
        return {"Agent": ""}, False

CURRENT_SETTINGS, SETTINGS_VALID = load_settings()
