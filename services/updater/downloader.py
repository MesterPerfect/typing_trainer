import os
import tempfile
import urllib.request
import logging
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QApplication

logger = logging.getLogger(__name__)

class UpdateDownloader(QThread):
    """
    Asynchronously downloads the update file and reports progress.
    """
    progress_updated = Signal(int)
    download_complete = Signal(str)
    error_occurred = Signal(str)

    def __init__(self, download_url: str, target_version: str):
        super().__init__()
        self.download_url = download_url
        self.target_version = target_version
        
        filename = download_url.split("/")[-1]
        self.download_path = os.path.join(tempfile.gettempdir(), filename)
        self._is_cancelled = False

    def run(self):
        self._track_telemetry("update_download_started", {"target_version": self.target_version})
        try:
            logger.info(f"Starting update download from: {self.download_url}")
            req = urllib.request.Request(self.download_url, headers={'User-Agent': 'TypingTrainer-App'})
            
            with urllib.request.urlopen(req, timeout=15) as response:
                total_size = int(response.headers.get('content-length', 0))
                downloaded_size = 0
                chunk_size = 8192
                
                with open(self.download_path, 'wb') as file:
                    while True:
                        if self._is_cancelled:
                            logger.info("Update download cancelled.")
                            self._track_telemetry("update_download_cancelled", {"target_version": self.target_version})
                            return
                            
                        chunk = response.read(chunk_size)
                        if not chunk:
                            break
                            
                        file.write(chunk)
                        downloaded_size += len(chunk)
                        
                        if total_size > 0:
                            progress = int((downloaded_size / total_size) * 100)
                            self.progress_updated.emit(progress)
                            
            logger.info(f"Download complete: {self.download_path}")
            self._track_telemetry("update_download_completed", {"target_version": self.target_version})
            self.download_complete.emit(self.download_path)
            
        except Exception as e:
            logger.error(f"Download failed: {e}")
            self._track_telemetry("update_download_failed", {"error": str(e), "target_version": self.target_version})
            self.error_occurred.emit("Failed to download the update. Please try again later.")
            
    def cancel(self):
        self._is_cancelled = True

    def _track_telemetry(self, event_name: str, properties: dict):
        app = QApplication.instance()
        if app and hasattr(app, "telemetry"):
            app.telemetry.track(event_name, properties)
