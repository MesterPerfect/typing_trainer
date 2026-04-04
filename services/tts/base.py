import logging
from PySide6.QtWidgets import QApplication

logger = logging.getLogger(__name__)

class BaseTTS:
    """ Base interface for all TTS engines. """

    def speak(self, text: str, interrupt: bool = True):
        raise NotImplementedError

    def speak_char(self, char: str):
        raise NotImplementedError

    def stop(self):
        pass

    def _track_event(self, event_name: str, properties: dict = None):
        """ Helper method to safely record telemetry events for any TTS engine. """
        app = QApplication.instance()
        if app and hasattr(app, "telemetry"):
            app.telemetry.track(event_name, properties)
