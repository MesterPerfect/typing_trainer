import re
import logging
from PySide6.QtCore import Qt
from core.modes import ExplorerMode
from utils.helpers import get_finger_instruction

logger = logging.getLogger(__name__)

class ExplorerEngine:
    """ Engine to handle discovery modes, including special keys. """
    
    def __init__(self, mode: ExplorerMode = ExplorerMode.FREE):
        self.mode = mode
        logger.info(f"ExplorerEngine initialized with mode: {self.mode.name}")

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
            Qt.Key.Key_Shift: "Shift, Modifier Key, مفتاح تعديل",
            Qt.Key.Key_Control: "Control, Modifier Key, مفتاح تعديل",
            Qt.Key.Key_Alt: "Alt, Modifier Key, مفتاح تعديل",
            Qt.Key.Key_Meta: "Windows, System Key, مفتاح نظام",
            Qt.Key.Key_Return: "Enter, Action Key, مفتاح إجرائي",
            Qt.Key.Key_Enter: "Enter, Action Key, مفتاح إجرائي",
            Qt.Key.Key_Tab: "Tab, Functional Key, مفتاح وظيفي",
            Qt.Key.Key_Backspace: "Backspace, Action Key, مفتاح مسح",
            Qt.Key.Key_Space: "Spacebar, مسافة",
            Qt.Key.Key_Escape: "Escape, System Key, مفتاح خروج",
            Qt.Key.Key_CapsLock: "Caps Lock, Toggle Key, مفتاح تبديل",
            Qt.Key.Key_Delete: "Delete, Action Key, مفتاح مسح",
            Qt.Key.Key_Up: "Up Arrow, Navigation, سهم لأعلى",
            Qt.Key.Key_Down: "Down Arrow, Navigation, سهم لأسفل",
            Qt.Key.Key_Left: "Left Arrow, Navigation, سهم لليسار",
            Qt.Key.Key_Right: "Right Arrow, Navigation, سهم لليمين",
            Qt.Key.Key_F1: "F1, Function Key",
            Qt.Key.Key_F2: "F2, Function Key",
            Qt.Key.Key_F3: "F3, Function Key",
        }
        
        if key_code in mapping:
            return mapping[key_code]
        if char:
            return f"Standard Key, مفتاح قياسي: {char}"
        return "Unknown Key, مفتاح غير معروف"
