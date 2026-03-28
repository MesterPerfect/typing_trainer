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

        # Safe exit system variables
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
        # Ensure it can capture all keyboard events
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
        }

        msg = f"{mode_names.get(mode, '')} activated. Press the escape key three times to exit."

        # Audio feedback for activation
        self.audio.play("correct")
        self.tts.speak(msg)

    def reset_escape_count(self):
        """Reset the count if the user pauses for too long."""
        self.escape_count = 0
        logger.debug("Escape sequence reset due to timeout.")

    def keyPressEvent(self, event):
        key = event.key()
        text = event.text()

        # Handle Safe Exit System (3x Escape)
        if key == Qt.Key.Key_Escape:
            self.escape_count += 1
            # Give the user 1.5 seconds to press Escape again
            self.escape_timer.start(1500)

            # Tactile click for escape presses
            self.audio.play("correct")

            if self.escape_count == 1:
                self.tts.speak("Press twice to exit")
            elif self.escape_count == 2:
                self.tts.speak("Press once to exit")
            elif self.escape_count >= 3:
                self.escape_timer.stop()
                self.reset_escape_count()

                # Completion sound upon exiting
                self.audio.play("complete")
                self.tts.speak("Exiting Explorer Mode")
                self.return_requested.emit()
            return

        # If user presses any other key, cancel the escape sequence
        self.escape_timer.stop()
        self.reset_escape_count()

        # Process standard keys
        if not self.engine or not text:
            return

        result = self.engine.process_char(text)

        if result and "message" in result and result["message"]:
            # Play a click for standard key presses, or error if the engine flags it as invalid for the mode
            is_valid = result.get("is_valid", True)
            if is_valid:
                self.audio.play("correct")
            else:
                self.audio.play("error")

            self.tts.speak(result["message"])
