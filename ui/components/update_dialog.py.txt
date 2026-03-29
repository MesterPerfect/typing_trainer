import os
import sys
import logging
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QTextEdit, QPushButton, QProgressBar, QMessageBox
)
from PySide6.QtCore import Qt

from services.updater import UpdateDownloader

logger = logging.getLogger(__name__)

class UpdateDialog(QDialog):
    """
    Dialog to notify the user of an update, display release notes,
    and handle the downloading process with a progress bar.
    """
    def __init__(self, new_version: str, release_notes: str, download_url: str, tts_engine, parent=None):
        super().__init__(parent)
        self.new_version = new_version
        self.release_notes = release_notes
        self.download_url = download_url
        self.tts = tts_engine
        
        self.downloader = None
        self.last_announced_progress = 0

        self._setup_ui()
        self._announce_update()

    def _setup_ui(self):
        self.setWindowTitle("Update Available")
        self.setMinimumWidth(450)
        self.setMinimumHeight(300)
        self.setModal(True)

        layout = QVBoxLayout(self)

        # Title Label
        self.title_label = QLabel(f"<b>A new version is available: v{self.new_version}</b>")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)

        # Release Notes Text Area (Read-only)
        self.notes_edit = QTextEdit()
        self.notes_edit.setReadOnly(True)
        self.notes_edit.setPlainText(self.release_notes)
        # Accessible description for screen readers
        self.notes_edit.setAccessibleName("Release Notes") 
        layout.addWidget(self.notes_edit)

        # Progress Bar (Hidden initially)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        # Buttons Layout
        self.buttons_layout = QHBoxLayout()
        
        self.btn_update = QPushButton("Update Now")
        self.btn_update.clicked.connect(self._start_download)
        
        self.btn_later = QPushButton("Later")
        self.btn_later.clicked.connect(self.reject)  # Closes the dialog safely
        
        self.buttons_layout.addWidget(self.btn_update)
        self.buttons_layout.addWidget(self.btn_later)
        
        layout.addLayout(self.buttons_layout)

    def _announce_update(self):
        """ Announce the update availability to screen reader users. """
        msg = f"Update available. Version {self.new_version}. Press Tab to read release notes or update."
        if self.tts:
            self.tts.speak(msg)

    def _start_download(self):
        """ Initiates the background download process. """
        # Update UI state
        self.btn_update.hide()
        self.btn_later.setText("Cancel")
        self.btn_later.clicked.disconnect()
        self.btn_later.clicked.connect(self._cancel_download)
        self.progress_bar.show()
        
        if self.tts:
            self.tts.speak("Starting download. Please wait.")

        # Initialize and start the background downloader thread
        self.downloader = UpdateDownloader(self.download_url)
        self.downloader.progress_updated.connect(self._on_progress_updated)
        self.downloader.download_complete.connect(self._on_download_complete)
        self.downloader.error_occurred.connect(self._on_download_error)
        self.downloader.start()

    def _on_progress_updated(self, value: int):
        """ Updates the progress bar and announces every 25% for accessibility. """
        self.progress_bar.setValue(value)
        
        # Announce progress at 25%, 50%, 75% to avoid spamming the screen reader
        if value - self.last_announced_progress >= 25:
            self.last_announced_progress = value
            if self.tts:
                self.tts.speak(f"{value} percent")

    def _on_download_complete(self, file_path: str):
        """ Handles the successful completion of the download. """
        if self.tts:
            self.tts.speak("Download complete. Closing application to apply update.")
            
        logger.info(f"Update downloaded to: {file_path}")
        
        # Inform the user before closing
        QMessageBox.information(
            self, "Download Complete", 
            "The update has been downloaded. The application will now close to apply the update."
        )
        
        # Launch the downloaded file (Works for Windows .zip/.exe or Linux/Mac archives)
        self._launch_update_file(file_path)
        
        # Close the dialog and trigger app shutdown
        self.accept()
        sys.exit(0)

    def _on_download_error(self, error_msg: str):
        """ Handles download failures. """
        if self.tts:
            self.tts.speak("Download failed.")
            
        QMessageBox.critical(self, "Update Error", error_msg)
        
        # Restore UI state
        self.progress_bar.hide()
        self.btn_update.show()
        self.btn_later.setText("Later")
        self.btn_later.clicked.disconnect()
        self.btn_later.clicked.connect(self.reject)

    def _cancel_download(self):
        """ Safely aborts the download if the user clicks Cancel. """
        if self.downloader and self.downloader.isRunning():
            self.downloader.cancel()
            self.downloader.wait() # Wait for thread to finish safely
            
        if self.tts:
            self.tts.speak("Download cancelled.")
        self.reject()

    def _launch_update_file(self, file_path: str):
        """ Attempts to open the downloaded file using the OS default handler. """
        try:
            if sys.platform == "win32":
                os.startfile(file_path)
            elif sys.platform == "darwin":
                import subprocess
                subprocess.call(["open", file_path])
            else:
                import subprocess
                subprocess.call(["xdg-open", file_path])
        except Exception as e:
            logger.error(f"Failed to launch update file: {e}")
