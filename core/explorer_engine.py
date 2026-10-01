import re
import logging
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from core.modes import ExplorerMode
from utils.helpers import get_finger_instruction
from ui.typing.verbalizer import get_pronunciation

logger = logging.getLogger(__name__)

class ExplorerEngine:
    """ Engine to handle discovery modes, including special keys and telemetry tracking. """
    
    def __init__(self, mode: ExplorerMode = ExplorerMode.FREE, lang: str = "en"):
        self.mode = mode
        self.lang = lang
        logger.info(f"ExplorerEngine initialized with mode: {self.mode.name}, lang: {self.lang}")
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
                return {"valid": False, "message": _("Not an Arabic letter")}
                
        elif self.mode == ExplorerMode.ENGLISH:
            if not re.match(r'[a-zA-Z\s]', char):
                return {"valid": False, "message": _("Not an English letter")}
                
        elif self.mode == ExplorerMode.NUMBERS:
            if not char.isdigit():
                return {"valid": False, "message": _("Not a number")}

        char_name = get_pronunciation(char, self.lang)
        finger = get_finger_instruction(char, self.lang)
        message = f"{char_name}, {finger}" if finger else char_name

        logger.debug(f"[EXPLORER] Processed '{char}' -> '{message}'")
        return {"valid": True, "message": message}

    def _get_key_info(self, key_code: int, char: str) -> str:
        """ Returns the descriptive name and type of a hardware key. """
        mapping = {
            Qt.Key.Key_Shift: _("Shift, Modifier Key"),
            Qt.Key.Key_Control: _("Control, Modifier Key"),
            Qt.Key.Key_Alt: _("Alt, Modifier Key"),
            Qt.Key.Key_Meta: _("Windows, System Key"),
            Qt.Key.Key_Return: _("Enter, Action Key"),
            Qt.Key.Key_Enter: _("Enter, Action Key"),
            Qt.Key.Key_Tab: _("Tab, Functional Key"),
            Qt.Key.Key_Backspace: _("Backspace, Action Key"),
            Qt.Key.Key_Space: _("Spacebar"),
            Qt.Key.Key_Escape: _("Escape, System Key"),
            Qt.Key.Key_CapsLock: _("Caps Lock, Toggle Key"),
            Qt.Key.Key_Delete: _("Delete, Action Key"),
            Qt.Key.Key_Insert: _("Insert, Action Key"),
            Qt.Key.Key_Home: _("Home, Navigation"),
            Qt.Key.Key_End: _("End, Navigation"),
            Qt.Key.Key_PageUp: _("Page Up, Navigation"),
            Qt.Key.Key_PageDown: _("Page Down, Navigation"),
            Qt.Key.Key_Up: _("Up Arrow, Navigation"),
            Qt.Key.Key_Down: _("Down Arrow, Navigation"),
            Qt.Key.Key_Left: _("Left Arrow, Navigation"),
            Qt.Key.Key_Right: _("Right Arrow, Navigation"),
            Qt.Key.Key_F1: _("F1, Function Key"),
            Qt.Key.Key_F2: _("F2, Function Key"),
            Qt.Key.Key_F3: _("F3, Function Key"),
            Qt.Key.Key_F4: _("F4, Function Key"),
            Qt.Key.Key_F5: _("F5, Function Key"),
            Qt.Key.Key_F6: _("F6, Function Key"),
            Qt.Key.Key_F7: _("F7, Function Key"),
            Qt.Key.Key_F8: _("F8, Function Key"),
            Qt.Key.Key_F9: _("F9, Function Key"),
            Qt.Key.Key_F10: _("F10, Function Key"),
            Qt.Key.Key_F11: _("F11, Function Key"),
            Qt.Key.Key_F12: _("F12, Function Key"),
        }
        
        if key_code in mapping:
            return mapping[key_code]
        if char:
            spoken_char = get_pronunciation(char, self.lang)
            return f"{_('Standard Key:')} {spoken_char}"
        return _("Unknown Key")
