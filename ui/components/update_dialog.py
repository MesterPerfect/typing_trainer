import os
import sys
import logging
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QTextEdit, QPushButton, QProgressBar, QMessageBox,
    QApplication  # أضفنا QApplication هنا للوصول إلى الحافظة (Clipboard)
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
        self.setMinimumWidth(500)  # قمنا بزيادة العرض قليلاً ليستوعب 3 أزرار
        self.setMinimumHeight(350)
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
        
        # 1. زر نسخ المستجدات
        self.btn_copy = QPushButton("Copy Notes")
        self.btn_copy.clicked.connect(self._copy_release_notes)
        self.buttons_layout.addWidget(self.btn_copy)
        
        # مسافة مرنة لفصل زر النسخ عن أزرار التحديث والإغلاق
        self.buttons_layout.addStretch()
        
        # 2. زر التحديث
        self.btn_update = QPushButton("Update Now")
        self.btn_update.clicked.connect(self._start_download)
        self.buttons_layout.addWidget(self.btn_update)
        
        # 3. زر الإلغاء/التأجيل
        self.btn_later = QPushButton("Later")
        self.btn_later.clicked.connect(self.reject)  # Closes the dialog safely
        self.buttons_layout.addWidget(self.btn_later)
        
        layout.addLayout(self.buttons_layout)

    def _copy_release_notes(self):
        """ Copies the release notes to the system clipboard and announces it. """
        clipboard = QApplication.clipboard()
        clipboard.setText(self.release_notes)
        
        if self.tts:
            self.tts.speak("Release notes copied to clipboard.")
        
        logger.info("Release notes copied to clipboard.")

    def _announce_update(self):
        """ Announce the update availability to screen reader users. """
        msg = f"Update available. Version {self.new_version}. Press Tab to read release notes, copy them, or update."
        if self.tts:
            self.tts.speak(msg)

    def _start_download(self):
        """ Initiates the background download process. """
        # Update UI state
        self.btn_update.hide()
        self.btn_copy.hide()  # إخفاء زر النسخ أثناء التحميل لتنظيف الواجهة
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
        
        # Launch the downloaded file
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
        self.btn_copy.show()  # إعادة إظهار زر النسخ في حال فشل التحميل
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
        """ Triggers the background updater and kills the main app to allow file replacement. """
        import subprocess
        
        # Check if the app is compiled (frozen) or running from source
        if getattr(sys, 'frozen', False):
            # Compiled portable app mode
            target_dir = os.path.dirname(sys.executable)
            main_exe = os.path.basename(sys.executable)
            updater_exe = "apply_update.exe" if sys.platform == "win32" else "apply_update"
            updater_path = os.path.join(target_dir, updater_exe)
            
            if os.path.exists(updater_path):
                # Spawn the updater as a detached process
                args = [
                    updater_path, 
                    "--archive", file_path, 
                    "--target", target_dir, 
                    "--exe", main_exe
                ]
                
                if sys.platform == "win32":
                    subprocess.Popen(args, creationflags=subprocess.DETACHED_PROCESS)
                else:
                    subprocess.Popen(args, start_new_session=True)
            else:
                logger.error("Updater executable not found. Unable to self-update.")
                QMessageBox.warning(self, "Update Error", "The updater module is missing.")
        else:
            # Running from source code (Developer Mode) - Just open the folder
            QMessageBox.information(
                self, "Developer Mode", 
                f"Update downloaded to:\n{file_path}\n\nSince you are running from source, the self-updater will not run."
            )
            # Open the containing folder for the developer
            folder = os.path.dirname(file_path)
            if sys.platform == "win32":
                os.startfile(folder)
            elif sys.platform == "darwin":
                subprocess.call(["open", folder])
            else:
                subprocess.call(["xdg-open", folder])
