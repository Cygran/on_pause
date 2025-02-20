import logging
import requests
from PySide6.QtCore import QTimer, QObject, Signal

class APIClient(QObject):
    status_changed = Signal(bool)

    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_status)
        self.last_status = None
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def update_settings(self, new_settings):
        self.settings = new_settings
        if self.timer.isActive():
            self.stop_polling()
            self.start_polling()
            self.logger.info("Settings updated, polling restarted")

    def start_polling(self):
        if self.settings["api"]["enabled"]:
            interval = self.settings["api"]["polling_interval"] * 1000 
            self.timer.start(interval)
            
    def stop_polling(self):
        self.timer.stop()
        
    def check_status(self):
        try:
            base_url = self.settings['api']['base_url']
            endpoint = self.settings['api']['endpoint']
            agent = self.settings['api']['agent']
            
            url = f"{base_url}{endpoint}?agent={agent}"
            self.logger.info(f"Checking status at: {url}")
            
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            new_status = data.get('status', False)
            
            if new_status != self.last_status:
                self.last_status = new_status
                self.status_changed.emit(new_status)
                self.logger.info(f"Status changed to: {new_status}")
                
        except requests.RequestException as e:
            self.logger.error(f"API request failed: {str(e)}")
        except ValueError as e:
            self.logger.error(f"Failed to parse JSON response: {str(e)}")
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")