import sys
import os
import subprocess
import webbrowser
import logging
from PySide6.QtWidgets import QMenuBar, QMessageBox
from PySide6.QtGui import QAction

from core.constants import APP_VERSION, LOG_FILE

logger = logging.getLogger(__name__)

class AppMenu(QMenuBar):
    def __init__(self, parent_window):
        super().__init__(parent_window)
        self.window = parent_window
        self._setup_menu()

    def _setup_menu(self):
        # --- File Menu ---
        file_menu = self.addMenu(_("File"))
        
        action_settings = QAction(_("Settings"), self.window)
        action_settings.setShortcut("F3")
        action_settings.triggered.connect(self.window.show_settings)
        file_menu.addAction(action_settings)

        action_open_log = QAction(_("Open Log File"), self.window)
        action_open_log.triggered.connect(self._open_log_file)
        file_menu.addAction(action_open_log)

        file_menu.addSeparator()

        action_exit = QAction(_("Exit"), self.window)
        action_exit.setShortcut("Alt+F4")
        action_exit.triggered.connect(self.window.close)
        file_menu.addAction(action_exit)

        # --- Tools Menu ---
        tools_menu = self.addMenu(_("Tools"))
        
        action_editor = QAction(_("Lesson Manager"), self.window)
        action_editor.setShortcut("Ctrl+L")
        action_editor.triggered.connect(self.window.show_editor)
        tools_menu.addAction(action_editor)

        action_results = QAction(_("Results & Stats"), self.window)
        action_results.setShortcut("F4")
        action_results.triggered.connect(self.window.show_results)
        tools_menu.addAction(action_results)

        # --- Help Menu ---
        help_menu = self.addMenu(_("Help"))
        
        action_update = QAction(_("Check for Updates"), self.window)
        action_update.triggered.connect(lambda: self.window.check_for_updates(silent=False))
        help_menu.addAction(action_update)

        action_contact = QAction(_("Contact Developer"), self.window)
        action_contact.triggered.connect(self._contact_developer)
        help_menu.addAction(action_contact)

        action_about = QAction(_("About Typing Trainer"), self.window)
        action_about.triggered.connect(self._show_about)
        help_menu.addAction(action_about)

    def _open_log_file(self):
        try:
            if sys.platform == "win32":
                os.startfile(str(LOG_FILE))
            elif sys.platform == "darwin":
                subprocess.call(["open", str(LOG_FILE)])
            else:
                subprocess.call(["xdg-open", str(LOG_FILE)])
        except Exception as e:
            logger.error(f"Failed to open log file: {e}")
            QMessageBox.warning(self.window, _("Error"), _("Could not open the log file."))

    def _contact_developer(self):
        webbrowser.open("https://github.com/MesterPerfect/typing_trainer/issues")

    def _show_about(self):
        QMessageBox.about(
            self.window, 
            _("About Typing Trainer"), 
            f"<b>Typing Trainer</b><br>{_('Version:')} {APP_VERSION}<br><br>{_('An accessible typing tutor designed for screen reader users.')}<br>{_('Developed by MesterPerfect.')}"
        )
