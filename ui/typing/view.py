from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import QTimer, pyqtSignal
import logging

from core.typing_engine import TypingEngine
from core.modes import TypingMode
from ui.components.stats_panel import StatsPanel
from ui.components.text_display import TextDisplay
from ui.components.typing_input import TypingInput
from models.result_model import LessonResult
from .speech_handler import TypingSpeechHandler

logger = logging.getLogger(__name__)

class TypingView(QWidget):
    return_requested = pyqtSignal()

    def __init__(self, tts, settings, result_service, audio):
        super().__init__()
        self.result_service = result_service
        self.audio = audio
        
        self.engine = None
        self.current_lesson_id = None
        self.is_test = False
        
        # Initialize the speech handler and pass audio service to it
        self.speech_handler = TypingSpeechHandler(tts, settings, audio)
        
        self._setup_ui()
        self._setup_timers()

    def _setup_ui(self):
        layout = QVBoxLayout()
        self.stats_panel = StatsPanel()
        self.text_display = TextDisplay()
        self.typing_input = TypingInput()
        
        self.typing_input.char_typed.connect(self.handle_char_typed)
        self.typing_input.backspace_pressed.connect(self.handle_backspace)
        self.typing_input.escape_pressed.connect(self.trigger_return)

        layout.addWidget(self.stats_panel)
        layout.addWidget(self.text_display)
        layout.addWidget(self.typing_input)
        layout.addStretch()
        self.setLayout(layout)

    def _setup_timers(self):
        self.stats_timer = QTimer(self)
        self.stats_timer.timeout.connect(self.update_stats_display)

    def start_lesson(self, lesson):
        logger.info(f"TypingView: Starting lesson: {lesson.title}")
        self.current_lesson_id = lesson.id
        self.is_test = getattr(lesson, "lesson_type", "lesson") == "test"

        if lesson.difficulty == 1:
            mode = TypingMode.CHARACTER
        elif lesson.difficulty == 2:
            mode = TypingMode.WORD
        else:
            mode = TypingMode.SENTENCE

        self.engine = TypingEngine(lesson.text, mode=mode)
        
        # Pass session info to speech handler
        self.speech_handler.setup_session(self.engine, self.is_test)

        self.stats_panel.update_stats({
            "wpm": 0, "accuracy": 100.0, "errors": 0, "time": 0.0
        })

        self.typing_input.setFocus()
        self.update_display_and_stats()
        self.stats_timer.start(500)

        # Trigger initial start message
        self.speech_handler.speak_start()

    def update_stats_display(self):
        if self.engine and self.engine.stats.is_running:
            self.stats_panel.update_stats(self.engine.get_stats())

    def update_display_and_stats(self):
        parts = self.engine.get_display_parts()
        self.text_display.update_display(self.engine.text, *parts)
        self.update_stats_display()

    def handle_char_typed(self, char: str):
        if not self.engine: 
            return
            
        result = self.engine.process_char(char)
        if result is None: 
            return

        # Delegate audio and TTS feedback to speech handler
        self.speech_handler.speak_char_feedback(char, result.correct)
        self.update_display_and_stats()

        if self.engine.is_finished():
            self.handle_completion()

    def handle_backspace(self):
        if self.engine:
            self.engine.backspace()
            self.update_display_and_stats()
            self.speech_handler.speak_backspace()

    def handle_completion(self):
        logger.info("Typing completed")
        self.engine.stats.stop()
        self.stats_timer.stop()
        
        stats = self.engine.get_stats()
        self.stats_panel.update_stats(stats)
        
        if self.current_lesson_id:
            result = LessonResult(
                lesson_id=self.current_lesson_id, wpm=stats["wpm"],
                accuracy=stats["accuracy"], errors=stats["errors"],
                time_elapsed=stats["time"]
            )
            self.result_service.save_result(result)

        # Delegate completion announcement and sound to speech handler
        self.speech_handler.speak_completion(stats)
        
        QTimer.singleShot(4000, self.trigger_return)

    def trigger_return(self):
        self.stats_timer.stop()
        self.engine = None
        self.return_requested.emit()
