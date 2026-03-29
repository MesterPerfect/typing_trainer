import sys
import os
import subprocess
import webbrowser
import logging

from PySide6.QtWidgets import (
    QMainWindow, QStackedWidget, QMessageBox
)
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt, QTimer

from ui.lesson_editor_view import LessonEditorView
from services.tts import create_tts
from services.lesson import LessonService
from services.settings_service import SettingsService
from services.updater import UpdateChecker
from utils.logger import setup_logger
from services.result_service import ResultService
from services.audio import AudioService
from ui.lesson_view import LessonView
from ui.typing import TypingView
from ui.settings_view import SettingsView
from ui.results_view import ResultsView
from ui.explorer_view import ExplorerView
from ui.components.update_dialog import UpdateDialog
from core.modes import ExplorerMode
from core.constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    APP_VERSION,
    ICON_FILE_ICO,
    ICON_FILE_PNG,
    LOG_FILE
)

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self, args=None):
        super().__init__()

        self.setWindowTitle(WINDOW_TITLE)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self._apply_window_icon()

        # ===============================
        # Services Initialization
        # ===============================
        self.settings = SettingsService()
        self.result_service = ResultService()

        if args and args.lang:
            self.settings.set("ui_language", args.lang)
            logger.info(f"UI Language set to {args.lang} via CLI")

        disable_tts = args.no_tts if args else False
        self.tts = create_tts(disable_tts=disable_tts)
        self.audio = AudioService(self.settings)

        # ===============================
        # UI & Menu Setup
        # ===============================
        self._setup_ui()
        self._setup_menu()

        # ===============================
        # Startup Tasks
        # ===============================
        if self.settings.get("auto_update", True):
            QTimer.singleShot(2000, lambda: self._check_for_updates(silent=True))

    def _apply_window_icon(self):
        try:
            if sys.platform == "win32" and ICON_FILE_ICO.exists():
                self.setWindowIcon(QIcon(str(ICON_FILE_ICO)))
            elif sys.platform == "linux" and ICON_FILE_PNG.exists():
                self.setWindowIcon(QIcon(str(ICON_FILE_PNG)))
        except Exception as e:
            logger.warning(f"Failed to set window icon: {e}")

    def center_on_screen(self):
        screen_geometry = self.screen().availableGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

    # ===============================
    # Setup Views (Stacked Widget)
    # ===============================
    def _setup_ui(self):
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # 1. Lesson Selection View
        self.lesson_view = LessonView(self.tts)
        self.lesson_view.lesson_selected.connect(self.start_lesson)
        self.lesson_view.explorer_requested.connect(self.start_explorer)
        self.stacked_widget.addWidget(self.lesson_view)

        # 2. Typing Interface View
        self.typing_view = TypingView(self.tts, self.settings, self.result_service, self.audio)
        self.typing_view.return_requested.connect(self.show_lessons)
        self.stacked_widget.addWidget(self.typing_view)

        # 3. Settings View
        self.settings_view = SettingsView(self.settings, self.tts)
        self.settings_view.return_requested.connect(self.show_lessons)
        self.stacked_widget.addWidget(self.settings_view)

        # 4. Results View
        self.results_view = ResultsView(self.result_service, self.tts)
        self.results_view.return_requested.connect(self.show_lessons)
        self.stacked_widget.addWidget(self.results_view)

        # 5. Explorer View
        self.explorer_view = ExplorerView(self.tts, self.audio)
        self.explorer_view.return_requested.connect(self.show_lessons)
        self.stacked_widget.addWidget(self.explorer_view)

        # 6. Lesson Editor View
        self.editor_view = LessonEditorView(self.tts)
        self.editor_view.return_requested.connect(self.show_lessons)
        self.stacked_widget.addWidget(self.editor_view)

    # ===============================
    # Menu Bar Setup
    # ===============================
    def _setup_menu(self):
        menubar = self.menuBar()

        # --- File Menu ---
        file_menu = menubar.addMenu("File")
        
        action_settings = QAction("Settings", self)
        action_settings.setShortcut("F3")
        action_settings.triggered.connect(self.show_settings)
        file_menu.addAction(action_settings)

        action_open_log = QAction("Open Log File", self)
        action_open_log.triggered.connect(self._open_log_file)
        file_menu.addAction(action_open_log)

        file_menu.addSeparator()

        action_exit = QAction("Exit", self)
        action_exit.setShortcut("Alt+F4")
        action_exit.triggered.connect(self.close)
        file_menu.addAction(action_exit)

        # --- Tools Menu ---
        tools_menu = menubar.addMenu("Tools")
        
        action_editor = QAction("Lesson Manager", self)
        action_editor.setShortcut("F9")
        action_editor.triggered.connect(self.show_editor)
        tools_menu.addAction(action_editor)

        action_results = QAction("Results & Stats", self)
        action_results.setShortcut("F4")
        action_results.triggered.connect(self.show_results)
        tools_menu.addAction(action_results)

        # --- Help Menu ---
        help_menu = menubar.addMenu("Help")
        
        action_update = QAction("Check for Updates", self)
        action_update.triggered.connect(lambda: self._check_for_updates(silent=False))
        help_menu.addAction(action_update)

        action_contact = QAction("Contact Developer", self)
        action_contact.triggered.connect(self._contact_developer)
        help_menu.addAction(action_contact)

        action_about = QAction("About Typing Trainer", self)
        action_about.triggered.connect(self._show_about)
        help_menu.addAction(action_about)

    # ===============================
    # Menu Actions Implementations
    # ===============================
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
            QMessageBox.warning(self, "Error", "Could not open the log file.")

    def _contact_developer(self):
        webbrowser.open("https://github.com/MesterPerfect/typing_trainer/issues")

    def _show_about(self):
        QMessageBox.about(
            self, 
            "About Typing Trainer", 
            f"<b>Typing Trainer</b><br>Version: {APP_VERSION}<br><br>An accessible typing tutor designed for screen reader users.<br>Developed by MesterPerfect."
        )

    # ===============================
    # Navigation Methods
    # ===============================
    def start_lesson(self, lesson):
        self.stacked_widget.setCurrentWidget(self.typing_view)
        self.typing_view.start_lesson(lesson)

    def show_lessons(self):
        self.lesson_view.refresh_lessons()
        self.stacked_widget.setCurrentWidget(self.lesson_view)
        self.tts.speak("Main Menu")

    def show_editor(self):
        self.editor_view.load_data()
        self.stacked_widget.setCurrentWidget(self.editor_view)
        self.tts.speak("Lesson Editor Screen")

    def show_settings(self):
        self.settings_view.load_current_settings()
        self.stacked_widget.setCurrentWidget(self.settings_view)
        self.settings_view.auto_update_cb.setFocus()
        self.tts.speak("Settings Screen")

    def show_results(self):
        self.results_view.load_results()
        self.stacked_widget.setCurrentWidget(self.results_view)
        self.results_view.table.setFocus()
        self.tts.speak("Results Screen")

    def start_explorer(self, mode: ExplorerMode):
        self.stacked_widget.setCurrentWidget(self.explorer_view)
        self.explorer_view.start_explorer(mode)

    # ===============================
    # Update Logic
    # ===============================
    def _check_for_updates(self, silent=True):
        current_lang = self.settings.get("ui_language", "en")
        self.updater_thread = UpdateChecker(APP_VERSION, current_lang)
        self.updater_thread.update_available.connect(self._show_update_dialog)
        
        if not silent:
            self.updater_thread.no_update.connect(
                lambda: QMessageBox.information(self, "Up to Date", "You are using the latest version of Typing Trainer.")
            )
            self.updater_thread.error_occurred.connect(
                lambda err: QMessageBox.warning(self, "Update Error", err)
            )
            
        self.updater_thread.start()

    def _show_update_dialog(self, latest_version, release_notes, download_url):
        self.update_dialog = UpdateDialog(latest_version, release_notes, download_url, self.tts, self)
        self.update_dialog.show()

    # ===============================
    # Global Shortcuts & App Events
    # ===============================
    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key.Key_F2:
            current_mode = self.settings.get("guided_mode", True)
            new_mode = not current_mode
            self.settings.set("guided_mode", new_mode)
            status = "Enabled" if new_mode else "Disabled"
            self.tts.speak(f"Guided mode {status}")
            return

        if key == Qt.Key.Key_F3:
            if self.stacked_widget.currentWidget() != self.settings_view:
                self.show_settings()
            return

        if key == Qt.Key.Key_F4:
            if self.stacked_widget.currentWidget() != self.results_view:
                self.show_results()
            return

        if key == Qt.Key.Key_F5:
            self.start_explorer(ExplorerMode.FREE)
            return
        if key == Qt.Key.Key_F6:
            self.start_explorer(ExplorerMode.ARABIC)
            return
        if key == Qt.Key.Key_F7:
            self.start_explorer(ExplorerMode.ENGLISH)
            return
        if key == Qt.Key.Key_F8:
            self.start_explorer(ExplorerMode.NUMBERS)
            return
        if key == Qt.Key.Key_F9:
            if self.stacked_widget.currentWidget() != self.editor_view:
                self.show_editor()
            return

        super().keyPressEvent(event)

    def showEvent(self, event):
        self.center_on_screen()
        super().showEvent(event)

    def closeEvent(self, event):
        logger.info("Application is closing. Cleaning up resources...")
        if hasattr(self, "tts") and self.tts:
            try:
                self.tts.stop()
                if hasattr(self.tts, "shutdown"):
                    self.tts.shutdown()
                    logger.debug("TTS background threads shut down successfully.")
            except Exception as e:
                logger.error(f"Error stopping TTS during shutdown: {e}")
        event.accept()
