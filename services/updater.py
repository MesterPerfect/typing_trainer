import json
import os
import platform
import tempfile
import urllib.request
import logging
from packaging.version import parse as parse_version

from PySide6.QtCore import QThread, Signal

logger = logging.getLogger(__name__)

# URL to the raw JSON file on your GitHub repository
# Ensure this points to the master update file that contains ALL channels
UPDATE_JSON_URL = "https://raw.githubusercontent.com/MesterPerfect/typing_trainer/main/update.json"

class UpdateChecker(QThread):
    """
    Asynchronously checks a remote JSON manifest for the latest application version 
    based on the user's preferred update channel (stable/beta).
    """
    # Signals: latest_version, localized_release_notes, download_url
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
            
            # Prevent caching by adding a dummy query parameter
            import time
            url_with_nocache = f"{UPDATE_JSON_URL}?t={int(time.time())}"
            
            req = urllib.request.Request(url_with_nocache, headers={'User-Agent': 'TypingTrainer-App'})
            
            with urllib.request.urlopen(req, timeout=10) as response:
                master_data = json.loads(response.read().decode())
            
            # 1. Extract data for the selected channel
            channel_data = master_data.get(self.update_channel)
            
            if not channel_data:
                logger.error(f"Channel '{self.update_channel}' not found in update manifest.")
                self.error_occurred.emit(f"Update channel '{self.update_channel}' is not available.")
                return

            latest_version = channel_data.get("version", "")
            
            # 2. Smart Version Comparison (Supports SemVer like 1.1.0-beta)
            if self._is_newer(latest_version, self.current_version):
                # 3. Get localized notes, fallback to English, then to a default string
                notes_dict = channel_data.get("release_notes", {})
                localized_notes = notes_dict.get(self.current_language, notes_dict.get("en", "No release notes provided."))
                
                # 4. Get the correct download URL for the current OS (windows, linux, darwin)
                current_os = platform.system().lower()
                download_url = channel_data.get("downloads", {}).get(current_os, "")
                
                if download_url:
                    self.update_available.emit(latest_version, localized_notes, download_url)
                else:
                    self.error_occurred.emit("No suitable update file found for this operating system.")
            else:
                self.no_update.emit()
                
        except Exception as e:
            logger.error(f"Update check failed: {e}")
            self.error_occurred.emit("Could not check for updates. Please check your internet connection.")

    def _is_newer(self, latest: str, current: str) -> bool:
        """ 
        Compares semantic versions using standard packaging library.
        Correctly handles pre-releases (e.g. 1.1.0 > 1.1.0-beta > 1.0.0).
        """
        try:
            return parse_version(latest) > parse_version(current)
        except Exception as e:
            logger.error(f"Version parsing error: {e}")
            return False

class UpdateDownloader(QThread):
    """
    Asynchronously downloads the update file and reports progress.
    """
    progress_updated = Signal(int)
    download_complete = Signal(str)  # Returns the path to the downloaded file
    error_occurred = Signal(str)

    def __init__(self, download_url: str):
        super().__init__()
        self.download_url = download_url
        
        # Save the file to the system's temporary directory
        filename = download_url.split("/")[-1]
        self.download_path = os.path.join(tempfile.gettempdir(), filename)
        
        self._is_cancelled = False

    def run(self):
        try:
            logger.info(f"Starting update download from: {self.download_url}")
            req = urllib.request.Request(self.download_url, headers={'User-Agent': 'TypingTrainer-App'})
            
            with urllib.request.urlopen(req, timeout=15) as response:
                total_size = int(response.headers.get('content-length', 0))
                downloaded_size = 0
                chunk_size = 8192  # 8KB chunks
                
                with open(self.download_path, 'wb') as file:
                    while True:
                        if self._is_cancelled:
                            logger.info("Update download was cancelled by the user.")
                            return
                            
                        chunk = response.read(chunk_size)
                        if not chunk:
                            break
                            
                        file.write(chunk)
                        downloaded_size += len(chunk)
                        
                        # Calculate and emit progress percentage
                        if total_size > 0:
                            progress = int((downloaded_size / total_size) * 100)
                            self.progress_updated.emit(progress)
                            
            logger.info(f"Download complete: {self.download_path}")
            self.download_complete.emit(self.download_path)
            
        except Exception as e:
            logger.error(f"Download failed: {e}")
            self.error_occurred.emit("Failed to download the update. Please try again later.")
            
    def cancel(self):
        """ Safely aborts the ongoing download. """
        self._is_cancelled = True
