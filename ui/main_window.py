import sys
import logging
import platform

from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6.QtGui import QGuiApplication, QIcon
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from ui.lesson_editor_view import LessonEditorView
from services.tts import create_tts
from services.lesson import LessonService
from services.settings_service import SettingsService
from utils.logger import setup_logger
from services.result_service import ResultService
from services.audio import AudioService
from ui.lesson_view import LessonView
from ui.typing import TypingView
from ui.settings_view import SettingsView
from ui.results_view import ResultsView
from ui.explorer_view import ExplorerView
from core.modes import ExplorerMode
from core.constants import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, ICON_FILE_ICO, ICON_FILE_PNG

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self, args=None):
        super().__init__()
        
        self.setWindowTitle(WINDOW_TITLE)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Apply the application icon dynamically based on the platform
        self._apply_window_icon()

        self.settings = SettingsService()
        self.result_service = ResultService()

        # Apply CLI language setting if provided
        if args and args.lang:
            self.settings.set("ui_language", args.lang)
            logger.info(f"UI Language set to {args.lang} via CLI")

        # Initialize TTS with CLI override
        disable_tts = args.no_tts if args else False
        self.tts = create_tts(disable_tts=disable_tts)

        self.audio = AudioService(self.settings)
        
        # Initialize the user interface
        self._setup_ui()

    def _apply_window_icon(self):
        """ Applies the suitable icon file to the main window based on the OS. """
        try:
            if sys.platform == "win32" and ICON_FILE_ICO.exists():
                self.setWindowIcon(QIcon(str(ICON_FILE_ICO)))
            elif sys.platform == "linux" and ICON_FILE_PNG.exists():
                self.setWindowIcon(QIcon(str(ICON_FILE_PNG)))
            else:
                logger.debug("Window icon not applied: file not found or unsupported platform.")
        except Exception as e:
            logger.warning(f"Failed to set window icon: {e}")

    def center_on_screen(self):
        screen_geometry = self.screen().availableGeometry()
        window_geometry = self.frameGeometry()
        
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())        

    def _setup_ui(self):
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # 1. Lesson Selection View
        self.lesson_view = LessonView(self.tts)
        self.lesson_view.lesson_selected.connect(self.start_lesson)
        self.lesson_view.explorer_requested.connect(self.start_explorer)
        self.lesson_view.settings_requested.connect(self.show_settings)
        self.lesson_view.results_requested.connect(self.show_results)
        self.lesson_view.editor_requested.connect(self.show_editor)
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
        self.settings_view.guided_mode_cb.setFocus()
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
    # Global Shortcuts
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
        if hasattr(self, 'tts') and self.tts:
            try:
                self.tts.stop()
            except Exception as e:
                logger.error(f"Error stopping TTS during shutdown: {e}")
        event.accept()
