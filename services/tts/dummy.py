import logging
from .base import BaseTTS

logger = logging.getLogger(__name__)

class DummyTTS(BaseTTS):
    """ Safe fallback when no TTS is available. """

    def speak(self, text: str, interrupt: bool = True):
        logger.info(f"[TTS disabled] Speak: {text}")

    def speak_char(self, char: str):
        logger.info(f"[TTS disabled] Char: {char}")
