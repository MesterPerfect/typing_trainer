import logging
from .base import BaseTTS

logger = logging.getLogger(__name__)

class WindowsTTS(BaseTTS):
    """ TTS implementation using UniversalSpeech (NVDA/JAWS). """

    def __init__(self):
        self.available = False
        self.speech = None

        try:
            from UniversalSpeech import UniversalSpeech
            self.speech = UniversalSpeech()
            self.available = True
            logger.info("UniversalSpeech initialized successfully")

        except Exception:
            logger.exception("Failed to initialize UniversalSpeech")

    def speak(self, text: str, interrupt: bool = True):
        if not self.available:
            logger.warning("TTS not available (Windows)")
            return

        try:
            self.speech.say(text, interrupt)
            logger.debug(f"Speaking text: {text}")

        except Exception:
            logger.exception("Error during speech output")

    def speak_char(self, char: str):
        if not self.available or not char:
            return

        try:
            # Handle special characters natively
            if char == " ":
                self.speech.say("space")
            elif char == "\n":
                self.speech.say("new line")
            elif ord(char) > 127:
                # Non-ASCII characters (like Arabic) require say()
                self.speech.say(char)
            else:
                # Standard ASCII characters
                self.speech.say_a(char)

            logger.debug(f"Speaking character: {repr(char)}")

        except Exception:
            logger.warning("say_a failed, falling back to speak()")
            self.speak(char)

    def stop(self):
        if not self.available:
            return

        try:
            self.speech.stop()
            logger.debug("Speech stopped")

        except Exception:
            logger.exception("Error stopping speech")
