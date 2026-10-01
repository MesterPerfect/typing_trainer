import json
import platform
import urllib.request
import logging
import time
from core.constants import IS_PORTABLE
from packaging.version import parse as parse_version
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QApplication

logger = logging.getLogger(__name__)

UPDATE_JSON_URL = "https://raw.githubusercontent.com/MesterPerfect/typing_trainer/main/update.json"

class UpdateChecker(QThread):
    """
    Asynchronously checks a remote JSON manifest for the latest application version.
    """
    update_available = Signal(str, str, str)
    no_update = Signal()
    error_occurred = Signal(str)

    def __init__(self, current_version: str, current_language: str = "en", update_channel: str = "stable"):
        super().__init__()
        self.current_version = current_version
        self.current_language = current_language
        self.update_channel = update_channel

    def run(self):
        try:
            logger.info(f"Checking for updates from: {UPDATE_JSON_URL} on channel: {self.update_channel}")
            
            url_with_nocache = f"{UPDATE_JSON_URL}?t={int(time.time())}"
            req = urllib.request.Request(url_with_nocache, headers={'User-Agent': 'TypingTrainer-App'})
            
            with urllib.request.urlopen(req, timeout=10) as response:
                master_data = json.loads(response.read().decode())
            
            channel_data = master_data.get(self.update_channel)
            if not channel_data:
                logger.error(f"Channel '{self.update_channel}' not found.")
                self.error_occurred.emit(f"Update channel '{self.update_channel}' is not available.")
                return

            latest_version = channel_data.get("version", "")
            
            if self._is_newer(latest_version, self.current_version):
                notes_dict = channel_data.get("release_notes", {})
                localized_notes = notes_dict.get(self.current_language, notes_dict.get("en", "No release notes provided."))
                
                current_os = platform.system().lower() # 'windows', 'darwin', or 'linux'
                os_downloads = channel_data.get("downloads", {}).get(current_os, "")
                
                if isinstance(os_downloads, dict):
                    if IS_PORTABLE:
                        download_url = os_downloads.get("portable", "")
                    else:
                        download_url = os_downloads.get("installed", "")
                else:
                    download_url = str(os_downloads)
                
                if download_url:
                    self.update_available.emit(latest_version, localized_notes, download_url)
                else:
                    self.error_occurred.emit("No suitable update file found for this operating system.")
            else:
                self.no_update.emit()
                
        except Exception as e:
            logger.error(f"Update check failed: {e}")
            self.error_occurred.emit("Could not check for updates. Please check your internet connection.")
            self._track_telemetry("update_check_failed", {"error": str(e)})

    def _is_newer(self, latest: str, current: str) -> bool:
        try:
            return parse_version(latest) > parse_version(current)
        except Exception as e:
            logger.error(f"Version parsing error: {e}")
            return False

    def _track_telemetry(self, event_name: str, properties: dict):
        """ Silently tracks update events. """
        app = QApplication.instance()
        if app and hasattr(app, "telemetry"):
            app.telemetry.track(event_name, properties)
