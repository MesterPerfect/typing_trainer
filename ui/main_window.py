import sys
import logging
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QMessageBox
from PySide6.QtGui import QIcon, QShortcut, QKeySequence
from PySide6.QtCore import Qt, QTimer

from ui.lesson_editor_view import LessonEditorView
from services.tts import create_tts
from services.settings_service import SettingsService
from services.updater import UpdateChecker
from services.result_service import ResultService
from services.audio import AudioService
from ui.lesson_view import LessonView
from ui.typing.view import TypingView
from ui.settings.settings_view import SettingsView
from ui.results_view import ResultsView
from ui.explorer_view import ExplorerView
from ui.components.update_dialog import UpdateDialog
from ui.components.app_menu import AppMenu
from core.modes import ExplorerMode
from core.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, APP_VERSION, 
    ICON_FILE_ICO, ICON_FILE_PNG
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
        # UI, Menu & Shortcuts Setup
        # ===============================
        self._setup_ui()
        
        # Inject the custom Menu Bar
        self.setMenuBar(AppMenu(self))
        
        self._setup_shortcuts()

        # ===============================
        # Startup Tasks
        # ===============================
        if self.settings.get("auto_update", True):
            QTimer.singleShot(2000, lambda: self.check_for_updates(silent=True))

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

        self.lesson_view = LessonView(self.tts)
        self.lesson_view.lesson_selected.connect(self.start_lesson)
        self.lesson_view.explorer_requested.connect(self.start_explorer)
        self.stacked_widget.addWidget(self.lesson_view)

        self.typing_view = TypingView(self.tts, self.settings, self.result_service, self.audio)
        self.typing_view.return_requested.connect(self.show_lessons)
        self.stacked_widget.addWidget(self.typing_view)

        self.settings_view = SettingsView(self.settings, self.tts)
        self.settings_view.return_requested.connect(self.show_lessons)
        self.stacked_widget.addWidget(self.settings_view)

        self.results_view = ResultsView(self.result_service, self.tts)
        self.results_view.return_requested.connect(self.show_lessons)
        self.stacked_widget.addWidget(self.results_view)

        self.explorer_view = ExplorerView(self.tts, self.audio)
        self.explorer_view.return_requested.connect(self.show_lessons)
        self.stacked_widget.addWidget(self.explorer_view)

        self.editor_view = LessonEditorView(self.tts)
        self.editor_view.return_requested.connect(self.show_lessons)
        self.stacked_widget.addWidget(self.editor_view)

    # ===============================
    # Global Shortcuts Registration
    # ===============================
    def _setup_shortcuts(self):
        # F2: Toggle Guided Mode
        QShortcut(QKeySequence(Qt.Key.Key_F2), self, self._toggle_guided_mode)
        
        # F5 - F8: Explorer Modes
        QShortcut(QKeySequence(Qt.Key.Key_F5), self, lambda: self.start_explorer(ExplorerMode.FREE))
        QShortcut(QKeySequence(Qt.Key.Key_F6), self, lambda: self.start_explorer(ExplorerMode.ARABIC))
        QShortcut(QKeySequence(Qt.Key.Key_F7), self, lambda: self.start_explorer(ExplorerMode.ENGLISH))
        QShortcut(QKeySequence(Qt.Key.Key_F8), self, lambda: self.start_explorer(ExplorerMode.NUMBERS))

    def _toggle_guided_mode(self):
        current_mode = self.settings.get("guided_mode", True)
        new_mode = not current_mode
        self.settings.set("guided_mode", new_mode)
        status = "Enabled" if new_mode else "Disabled"
        self.tts.speak(f"Guided mode {status}")

    # ===============================
    # Navigation Methods (Routing)
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
        self.settings_view.tree_widget.setFocus()
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
    def check_for_updates(self, silent=True):
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
    # Window Lifecycle Events
    # ===============================
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
