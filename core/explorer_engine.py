import re
import logging
from core.modes import ExplorerMode
from utils.helpers import get_finger_instruction

logger = logging.getLogger(__name__)

class ExplorerEngine:
    """ Engine to handle discovery mode, returning character info in English. """
    
    def __init__(self, mode: ExplorerMode = ExplorerMode.FREE):
        self.mode = mode
        logger.info(f"ExplorerEngine initialized with mode: {self.mode.name}")

    def process_char(self, char: str) -> dict:
        if not char or len(char) > 1:
            return {"valid": False, "message": ""}

        # --- Filters based on mode ---
        if self.mode == ExplorerMode.ARABIC:
            if not re.match(r'[\u0600-\u06FF\s]', char):
                return {"valid": False, "message": "Not an Arabic letter"}
                
        elif self.mode == ExplorerMode.ENGLISH:
            if not re.match(r'[a-zA-Z\s]', char):
                return {"valid": False, "message": "Not an English letter"}
                
        elif self.mode == ExplorerMode.NUMBERS:
            if not char.isdigit():
                return {"valid": False, "message": "Not a number"}

        # --- Process valid character ---
        char_name = "Space" if char == " " else char
        finger = get_finger_instruction(char)
        
        message = f"{char_name}, {finger}" if finger else char_name

        logger.debug(f"[EXPLORER] Processed '{char}' -> '{message}'")
        return {"valid": True, "message": message}
