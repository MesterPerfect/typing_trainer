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
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def keyPressEvent(self, event):
        """
        Capture key presses, filter out control characters, and emit clean signals.
        """
        key = event.key()
        modifiers = event.modifiers()
        text = event.text()

        logger.debug(f"Input captured: {repr(text)} (code={key}, modifiers={modifiers})")

        # 1. Escape key
        if key == Qt.Key.Key_Escape:
            self.escape_pressed.emit()
            return

        # 2. Pause / Resume (Pause key or Ctrl+P)
        if key == Qt.Key.Key_Pause or (modifiers & Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_P):
            self.pause_requested.emit()
            return

        # 3. Repeat Prompt (Ctrl+R)
        if modifiers & Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_R:
            self.repeat_requested.emit()
            return

        # 4. Backspace
        if key == Qt.Key.Key_Backspace:
            self.backspace_pressed.emit()
            return

        # 5. Return / Enter key normalization
        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.char_typed.emit("\n")
            return

        # 6. Ignore special navigation / function keys
        ignored_keys = (
            Qt.Key.Key_Tab, Qt.Key.Key_Insert, Qt.Key.Key_Delete,
            Qt.Key.Key_Home, Qt.Key.Key_End, Qt.Key.Key_PageUp, Qt.Key.Key_PageDown,
            Qt.Key.Key_Left, Qt.Key.Key_Right, Qt.Key.Key_Up, Qt.Key.Key_Down,
            Qt.Key.Key_CapsLock, Qt.Key.Key_NumLock, Qt.Key.Key_ScrollLock,
            Qt.Key.Key_Print, Qt.Key.Key_SysReq, Qt.Key.Key_Menu
        )
        if key in ignored_keys or (Qt.Key.Key_F1 <= key <= Qt.Key.Key_F12):
            return

        # 7. Ignore modifier-heavy combinations (Ctrl+C, Ctrl+V, Alt+...)
        if modifiers & (Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.AltModifier | Qt.KeyboardModifier.MetaModifier):
            return

        # 8. Filter non-printable ASCII control characters (0-31 except \n and \t)
        if text:
            filtered_chars = [
                c for c in text 
                if ord(c) >= 32 or c in ('\n', '\t')
            ]
            if filtered_chars:
                self.char_typed.emit("".join(filtered_chars))
