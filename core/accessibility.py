import logging
import builtins
from PySide6.QtCore import QObject, QEvent
from PySide6.QtWidgets import QWidget, QPushButton, QLabel

logger = logging.getLogger(__name__)

# Fallback for gettext translation function if not already installed in builtins
if not hasattr(builtins, "_"):
    builtins._ = lambda s: s

class SelfVoicingFilter(QObject):
    def __init__(self, tts):
        super().__init__()
        self.tts = tts
        self.last_spoken = ""

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.FocusIn:
            if isinstance(obj, QWidget):
                text_to_speak = self._extract_text(obj)
                if text_to_speak and text_to_speak != self.last_spoken:
                    self.tts.speak(text_to_speak, interrupt=True)
                    self.last_spoken = text_to_speak
        elif event.type() == QEvent.Type.FocusOut:
            self.last_spoken = ""

        return super().eventFilter(obj, event)

    def _extract_text(self, widget: QWidget) -> str:
        name = widget.accessibleName()
        if name:
            return name

        raw_text = ""
        if isinstance(widget, QPushButton):
            btn_text = widget.text().replace("&", "")
            return f"{_('Button,')} {btn_text}"
        elif hasattr(widget, "text") and callable(widget.text):
            raw_text = widget.text()
        elif hasattr(widget, "title") and callable(widget.title):
            raw_text = widget.title()

        if raw_text:
            # Strip ampersands used for keyboard shortcuts in Qt
            return raw_text.replace("&", "")

        return ""
