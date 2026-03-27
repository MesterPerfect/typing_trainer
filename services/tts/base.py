import logging

logger = logging.getLogger(__name__)

class BaseTTS:
    """ Base interface for all TTS engines. """

    def speak(self, text: str, interrupt: bool = True):
        raise NotImplementedError

    def speak_char(self, char: str):
        raise NotImplementedError

    def stop(self):
        pass
