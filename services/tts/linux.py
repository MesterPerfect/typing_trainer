import logging
from .base import BaseTTS

logger = logging.getLogger(__name__)

class LinuxTTS(BaseTTS):

    def __init__(self):
        try:
            import speechd
            self.client = speechd.SSIPClient('typing-trainer')
            
            self._set_best_module()
            
            self.available = True
            logger.info("speechd module initialized successfully")
        except Exception as e:
            self.available = False
            logger.error(f"speechd initialization failed: {e}")

    def _set_best_module(self):
        try:
            available_modules = self.client.list_output_modules()
            preferred_modules = ['voxin', 'espeak-ng', 'espeak']
            
            for mod in preferred_modules:
                if mod in available_modules:
                    self.client.set_output_module(mod)
                    logger.info(f"Speech module set to: {mod}")
                    break
        except Exception as e:
            logger.error(f"Module selection error: {e}")

    def speak(self, text: str, interrupt: bool = True):
        if not getattr(self, 'available', False) or not text:
            return

        try:
            if interrupt:
                self.client.cancel()
            self.client.speak(text)
            logger.debug(f"Speaking: {text}")
        except Exception as e:
            logger.error(f"Speak error: {e}")

    def speak_char(self, char: str):
        if not getattr(self, 'available', False) or not char:
            return
            
        try:
            if char == " ":
                self.speak("space", interrupt=True)
            else:
                self.speak(char, interrupt=True)
            logger.debug(f"Speaking char: {repr(char)}")
        except Exception as e:
            logger.error(f"Speak char error: {e}")

    def set_rate(self, rate: int):
        if getattr(self, 'available', False):
            try:
                self.client.set_rate(rate)
                logger.info(f"Speech rate set to: {rate}")
            except Exception as e:
                logger.error(f"Set rate error: {e}")

    def set_pitch(self, pitch: int):
        if getattr(self, 'available', False):
            try:
                self.client.set_pitch(pitch)
                logger.info(f"Speech pitch set to: {pitch}")
            except Exception as e:
                logger.error(f"Set pitch error: {e}")

    def stop(self):
        if getattr(self, 'available', False):
            try:
                self.client.cancel()
            except Exception as e:
                logger.error(f"Stop error: {e}")
