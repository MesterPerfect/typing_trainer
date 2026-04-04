import re
import logging
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from core.modes import ExplorerMode
from utils.helpers import get_finger_instruction

logger = logging.getLogger(__name__)

class ExplorerEngine:
    """ Engine to handle discovery modes, including special keys and telemetry tracking. """
    
    def __init__(self, mode: ExplorerMode = ExplorerMode.FREE):
        self.mode = mode
        logger.info(f"ExplorerEngine initialized with mode: {self.mode.name}")
        self._track_activation()

    def _track_activation(self):
        """ Silently log that the user is utilizing the explorer mode feature. """
        app = QApplication.instance()
        if app and hasattr(app, "telemetry"):
            app.telemetry.track("explorer_mode_activated", {
                "type": self.mode.name
            })
            logger.debug("Telemetry: explorer_mode_activated event queued.")

    def process_input(self, key_code: int, char: str) -> dict:
        """ Processes either a standard character or a special hardware key. """
        
        # --- Keyboard Layout Explorer Mode ---
        if self.mode == ExplorerMode.KEYS:
            msg = self._get_key_info(key_code, char)
            return {"valid": True, "message": msg}

        # --- Standard Explorer Modes ---
        if not char or len(char) > 1:
            return {"valid": False, "message": ""}

        if self.mode == ExplorerMode.ARABIC:
            if not re.match(r'[\u0600-\u06FF\s]', char):
                return {"valid": False, "message": "Not an Arabic letter"}
                
        elif self.mode == ExplorerMode.ENGLISH:
            if not re.match(r'[a-zA-Z\s]', char):
                return {"valid": False, "message": "Not an English letter"}
                
        elif self.mode == ExplorerMode.NUMBERS:
            if not char.isdigit():
                return {"valid": False, "message": "Not a number"}

        char_name = "Space" if char == " " else char
        finger = get_finger_instruction(char)
        message = f"{char_name}, {finger}" if finger else char_name

        logger.debug(f"[EXPLORER] Processed '{char}' -> '{message}'")
        return {"valid": True, "message": message}

    def _get_key_info(self, key_code: int, char: str) -> str:
        """ Returns the descriptive name and type of a hardware key. """
        mapping = {
            Qt.Key.Key_Shift: "Shift, Modifier Key",
            Qt.Key.Key_Control: "Control, Modifier Key",
            Qt.Key.Key_Alt: "Alt, Modifier Key",
            Qt.Key.Key_Meta: "Windows, System Key",
            Qt.Key.Key_Return: "Enter, Action Key",
            Qt.Key.Key_Enter: "Enter, Action Key",
            Qt.Key.Key_Tab: "Tab, Functional Key",
            Qt.Key.Key_Backspace: "Backspace, Action Key",
            Qt.Key.Key_Space: "Spacebar",
            Qt.Key.Key_Escape: "Escape, System Key",
            Qt.Key.Key_CapsLock: "Caps Lock, Toggle Key",
            Qt.Key.Key_Delete: "Delete, Action Key",
            Qt.Key.Key_Up: "Up Arrow, Navigation",
            Qt.Key.Key_Down: "Down Arrow, Navigation",
            Qt.Key.Key_Left: "Left Arrow, Navigation",
            Qt.Key.Key_Right: "Right Arrow, Navigation",
            Qt.Key.Key_F1: "F1, Function Key",
            Qt.Key.Key_F2: "F2, Function Key",
            Qt.Key.Key_F3: "F3, Function Key",
        }
        
        if key_code in mapping:
            return mapping[key_code]
        if char:
            return f"Standard Key: {char}"
        return "Unknown Key"
