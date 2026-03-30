from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Signal, Qt, QTimer
import logging

from core.explorer_engine import ExplorerEngine
from core.modes import ExplorerMode

logger = logging.getLogger(__name__)


class ExplorerView(QWidget):
    return_requested = Signal()

    def __init__(self, tts, audio):
        super().__init__()
        self.tts = tts
        self.audio = audio
        self.engine = None

        self.escape_count = 0
        self.escape_timer = QTimer()
        self.escape_timer.setSingleShot(True)
        self.escape_timer.timeout.connect(self.reset_escape_count)

        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()
        self.label = QLabel(
            "Explorer Mode\n"
            "Press any key to identify it.\n"
            "To exit, press the Escape key three consecutive times."
        )
        font = self.label.font()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.setLayout(layout)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def start_explorer(self, mode: ExplorerMode = ExplorerMode.FREE):
        self.engine = ExplorerEngine(mode)
        self.reset_escape_count()
        self.setFocus()

        mode_names = {
            ExplorerMode.FREE: "Free Explorer",
            ExplorerMode.ARABIC: "Arabic Letters Explorer",
            ExplorerMode.ENGLISH: "English Letters Explorer",
            ExplorerMode.NUMBERS: "Numbers Explorer",
            ExplorerMode.KEYS: "Keyboard Layout Explorer",
        }

        msg = f"{mode_names.get(mode, '')} activated. Press the escape key three times to exit."

        self.audio.play("correct")
        self.tts.speak(msg)

    def reset_escape_count(self):
        self.escape_count = 0
        logger.debug("Escape sequence reset due to timeout.")

    def keyPressEvent(self, event):
        key = event.key()
        text = event.text()

        # Handle Safe Exit System (3x Escape)
        if key == Qt.Key.Key_Escape:
            self.escape_count += 1
            self.escape_timer.start(1500)
            self.audio.play("correct")

            if self.escape_count == 1:
                self.tts.speak("Press twice to exit")
            elif self.escape_count == 2:
                self.tts.speak("Press once to exit")
            elif self.escape_count >= 3:
                self.escape_timer.stop()
                self.reset_escape_count()
                self.audio.play("complete")
                self.tts.speak("Exiting Explorer Mode")
                self.return_requested.emit()
            
            # Allow the engine to announce Escape key if in Keys mode
            if self.engine and self.engine.mode == ExplorerMode.KEYS:
                result = self.engine.process_input(key, text)
                if result and result.get("valid"):
                    self.tts.speak(result["message"])
            return

        self.escape_timer.stop()
        self.reset_escape_count()

        if not self.engine:
            return

        # Process input (sending both key code and text)
        result = self.engine.process_input(key, text)

        if result and "message" in result and result["message"]:
            is_valid = result.get("valid", True)
            if is_valid:
                self.audio.play("correct")
            else:
                self.audio.play("error")

            self.tts.speak(result["message"])
