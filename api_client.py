import logging
import requests
from PySide6.QtCore import QTimer, QObject, Signal
from settings_manager import SettingsManager
from settings_window import SettingsWindow

class APIClient(QObject):
    status_changed = Signal(bool)
    poll_error = Signal(str)
    break_ended = Signal()
    break_time_updated = Signal(int, int)
    break_started = Signal()

    def __init__(self, settings: SettingsManager):
        super().__init__()
        self.settings = settings
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_status)
        self.last_status = None
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.break_timer = QTimer()
        self.break_timer.setSingleShot(True)
        self.break_timer.timeout.connect(self.end_break)
        self.display_timer = QTimer()
        self.display_timer.setInterval(1000)
        self.display_timer.timeout.connect(self.update_countdown)
        self.on_break = False

    def start_break(self, duration_minutes):
        if not 1 <= duration_minutes <= 60:
            raise ValueError("Break duration must be between 1 and 60 minutes")
        
        milliseconds = duration_minutes * 60 * 1000
        self.on_break = True
        self.break_timer.start(milliseconds)
        self.display_timer.start()
        self.break_started.emit()
        self.logger.info(f"Break started for {duration_minutes} minutes ({milliseconds}ms)")

    def end_break(self):
        self.on_break = False
        self.break_timer.stop()
        self.display_timer.stop()
        self.break_ended.emit()
        self.logger.info("Break ended automatically via timer")

    def is_on_break(self):
        return self.on_break

    def on_settings_updated(self):
        api_enabled = self.settings.current_settings['api']['enabled']
        if not api_enabled:
            self.stop_polling()
            self.logger.info("API disabled in settings")
            return
        was_polling = self.timer.isActive()
        if was_polling:
            self.stop_polling()
        if was_polling:
            self.start_polling()
            self.logger.info("Settings updated, polling restarted with new interval")

    def start_polling(self):
        if self.settings.current_settings['api']['enabled']:
            interval = self.settings.current_settings['api']['polling_interval'] * 1000
            self.timer.start(interval)
            
    def stop_polling(self):
        self.timer.stop()
        
    def check_status(self):
        if self.is_on_break():
            return self.on_break
        
        
        try:
            base_url = self.settings.current_settings['api']['base_url']
            endpoint = self.settings.current_settings['api']['endpoint']
            agent = self.settings.current_settings['Agent'] 
            
            url = f"{base_url}{endpoint}/?agent={agent}"
            self.logger.info(f"Checking status at: {url}")
            
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            self.logger.info(f"Received response: {data}")
            
            if data and isinstance(data, list) and len(data) > 0:
                status_str = data[0].get('status')
                new_status = status_str == "PAUSED"  # True if PAUSED, False if UNPAUSED
                
                if new_status != self.last_status:
                    self.last_status = new_status
                    self.status_changed.emit(new_status)
                    self.logger.info(f"Status changed to: {'PAUSED' if new_status else 'UNPAUSED'}")
                    
        except requests.RequestException as e:
            self.logger.error(f"API request failed: {str(e)}")
        except ValueError as e:
            self.logger.error(f"Failed to parse JSON response: {str(e)}")
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            
    def update_countdown(self):
        if not self.on_break:
            return
            
        remaining = self.break_timer.remainingTime()
        minutes = remaining // 60000  # Convert ms to minutes
        seconds = (remaining % 60000) // 1000  # Convert remainder to seconds
        self.break_time_updated.emit(int(minutes), int(seconds))

    def is_queue_paused(self):
        return self.last_status