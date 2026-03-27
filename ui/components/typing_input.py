from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, Qt
import logging

logger = logging.getLogger(__name__)

class TypingInput(QWidget):
    # Signals for keyboard interactions
    char_typed = pyqtSignal(str)
    backspace_pressed = pyqtSignal()
    escape_pressed = pyqtSignal()

    def __init__(self):
        super().__init__()
        # Ensure the widget can capture keyboard focus
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def keyPressEvent(self, event):
        """
        Capture key presses and emit corresponding signals.
        """
        key = event.key()
        text = event.text()

        logger.debug(f"Input captured: {repr(text)} (code={key})")

        if key == Qt.Key.Key_Escape:
            self.escape_pressed.emit()
            return

        if key == Qt.Key.Key_Backspace:
            self.backspace_pressed.emit()
            return

        # Emit the typed character if it is not empty
        if text:
            self.char_typed.emit(text)
