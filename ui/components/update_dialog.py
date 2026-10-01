import os
import sys
import logging
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QTextEdit, QPushButton, QProgressBar, QMessageBox,
    QApplication
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
        self.setWindowTitle(_("Update Available"))
        self.setMinimumWidth(500)
        self.setMinimumHeight(350)
        self.setModal(True)

        layout = QVBoxLayout(self)

        # Title Label
        title_text = f"<b>{_('A new version is available:')} v{self.new_version}</b>"
        self.title_label = QLabel(title_text)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)

        # Release Notes Text Area (Read-only)
        self.notes_edit = QTextEdit()
        self.notes_edit.setReadOnly(True)
        self.notes_edit.setPlainText(self.release_notes)
        self.notes_edit.setAccessibleName(_("Release Notes")) 
        layout.addWidget(self.notes_edit)

        # Progress Bar (Hidden initially)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        # Buttons Layout
        self.buttons_layout = QHBoxLayout()
        
        # 1. Copy Notes Button
        self.btn_copy = QPushButton(_("Copy Notes"))
        self.btn_copy.clicked.connect(self._copy_release_notes)
        self.buttons_layout.addWidget(self.btn_copy)
        
        self.buttons_layout.addStretch()
        
        # 2. Update Now Button
        self.btn_update = QPushButton(_("Update Now"))
        self.btn_update.clicked.connect(self._start_download)
        self.buttons_layout.addWidget(self.btn_update)
        
        # 3. Later / Cancel Button
        self.btn_later = QPushButton(_("Later"))
        self.btn_later.clicked.connect(self.reject)
        self.buttons_layout.addWidget(self.btn_later)
        
        layout.addLayout(self.buttons_layout)

    def _copy_release_notes(self):
        """ Copies the release notes to the system clipboard and announces it. """
        clipboard = QApplication.clipboard()
        clipboard.setText(self.release_notes)
        
        if self.tts:
            self.tts.speak(_("Release notes copied to clipboard."))
        
        logger.info("Release notes copied to clipboard.")

    def _announce_update(self):
        """ Announce the update availability to screen reader users. """
        msg = f"{_('Update available.')} {_('Version')} {self.new_version}. {_('Press Tab to read release notes, copy them, or update.')}"
        if self.tts:
            self.tts.speak(msg)

    def _start_download(self):
        """ Initiates the background download process. """
        self.btn_update.hide()
        self.btn_copy.hide()
        self.btn_later.setText(_("Cancel"))
        self.btn_later.clicked.disconnect()
        self.btn_later.clicked.connect(self._cancel_download)
        self.progress_bar.show()
        
        if self.tts:
            self.tts.speak(_("Starting download. Please wait."))

        self.downloader = UpdateDownloader(self.download_url, self.new_version)
        self.downloader.progress_updated.connect(self._on_progress_updated)
        self.downloader.download_complete.connect(self._on_download_complete)
        self.downloader.error_occurred.connect(self._on_download_error)
        self.downloader.start()

    def _on_progress_updated(self, value: int):
        """ Updates the progress bar and announces every 25% for accessibility. """
        self.progress_bar.setValue(value)
        
        if value - self.last_announced_progress >= 25:
            self.last_announced_progress = value
            if self.tts:
                self.tts.speak(f"{value} {_('percent')}")

    def _on_download_complete(self, file_path: str):
        """ Handles the successful completion of the download. """
        if self.tts:
            self.tts.speak(_("Download complete. Closing application to apply update."))
            
        logger.info(f"Update downloaded to: {file_path}")
        
        QMessageBox.information(
            self, _("Download Complete"), 
            _("The update has been downloaded. The application will now close to apply the update.")
        )
        
        self._launch_update_file(file_path)
        self.accept()
        sys.exit(0)

    def _on_download_error(self, error_msg: str):
        """ Handles download failures. """
        if self.tts:
            self.tts.speak(_("Download failed."))
            
        QMessageBox.critical(self, _("Update Error"), _(error_msg))
        
        self.progress_bar.hide()
        self.btn_update.show()
        self.btn_copy.show()
        self.btn_later.setText(_("Later"))
        self.btn_later.clicked.disconnect()
        self.btn_later.clicked.connect(self.reject)

    def _cancel_download(self):
        """ Safely aborts the download if the user clicks Cancel. """
        if self.downloader and self.downloader.isRunning():
            self.downloader.cancel()
            self.downloader.wait()
            
        if self.tts:
            self.tts.speak(_("Download cancelled."))
        self.reject()

    def _launch_update_file(self, file_path: str):
        """ Triggers the background updater and kills the main app to allow file replacement. """
        from services.updater.installer import trigger_update_installation
        trigger_update_installation(file_path, self.new_version)
