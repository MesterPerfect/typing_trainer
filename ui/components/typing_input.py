from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal, Qt
import logging

logger = logging.getLogger(__name__)


class TypingInput(QWidget):
    # Signals for keyboard interactions
    char_typed = Signal(str)
    backspace_pressed = Signal()
    escape_pressed = Signal()
    pause_requested = Signal()
    repeat_requested = Signal()

    def __init__(self):
        super().__init__()
        # Ensure the widget can capture keyboard focus
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def keyPressEvent(self, event):
        """
        Capture key presses and emit corresponding signals.
        """
        key = event.key()
        modifiers = event.modifiers()
        text = event.text()

        logger.debug(f"Input captured: {repr(text)} (code={key})")

        if key == Qt.Key.Key_Escape:
            self.escape_pressed.emit()
            return

        if key == Qt.Key.Key_Pause or (modifiers & Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_P):
            self.pause_requested.emit()
            return

        if modifiers & Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_R:
            self.repeat_requested.emit()
            return

        if key == Qt.Key.Key_Backspace:
            self.backspace_pressed.emit()
            return

        # Emit the typed character if it is not empty
        if text:
            self.char_typed.emit(text)
