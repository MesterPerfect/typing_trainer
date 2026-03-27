import subprocess
import logging
from .base import BaseTTS

logger = logging.getLogger(__name__)

class LinuxTTS(BaseTTS):
    """ 
    Linux TTS implementation supporting Orca v49+ DBus, Qt 6.8+ Accessibility, 
    and spd-say fallback. 
    """

    def __init__(self):
        self.qt_module = None
        self.backend = self._detect_backend()
        self.available = True

    def _detect_backend(self):
        """
        Detects the optimal TTS backend for the current Linux environment:
        1. Orca v49+ (DBus PresentMessage)
        2. Qt 6.8+ Accessibility (QAccessibleAnnouncementEvent)
        3. Fallback: Speech Dispatcher (spd-say)
        """
        if self._has_dbus_orca():
            logger.info("LinuxTTS: Using DBus backend (Orca v49+)")
            return "dbus"

        if self._has_qt_announcement():
            logger.info(f"LinuxTTS: Using Qt backend ({self.qt_module})")
            return "qt"

        logger.info("LinuxTTS: Using SPD fallback backend")
        return "spd"

    def _has_dbus_orca(self):
        """ Check if gdbus is available in the system. """
        try:
            subprocess.run(["which", "gdbus"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            return True
        except Exception:
            return False

    def _has_qt_announcement(self):
        """ Check if QAccessibleAnnouncementEvent is available in the installed Qt bindings. """
        try:
            from PyQt6.QtGui import QAccessible, QAccessibleAnnouncementEvent
            from PyQt6.QtWidgets import QApplication
            self.qt_module = "PyQt6"
            return True
        except ImportError:
            pass

        try:
            from PySide6.QtGui import QAccessible, QAccessibleAnnouncementEvent
            from PySide6.QtWidgets import QApplication
            self.qt_module = "PySide6"
            return True
        except ImportError:
            pass

        return False

    def speak(self, text: str, interrupt: bool = True):
        """ Route the speech request to the appropriate backend. """
        if not text:
            return

        if self.backend == "dbus":
            self._speak_dbus(text)
        elif self.backend == "qt":
            self._speak_qt(text, interrupt)
        else:
            self._speak_spd(text, interrupt)

    def speak_char(self, char: str):
        """ Handle individual character announcements safely. """
        if not char:
            return

        if char == " ":
            self.speak("space", interrupt=True)
        else:
            self.speak(char, interrupt=True)
            
        logger.debug(f"Speaking char: {repr(char)}")

    def stop(self):
        """ Attempt to stop ongoing speech (specifically for SPD backend). """
        if self.backend == "spd":
            try:
                subprocess.Popen(["spd-say", "-C"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e:
                logger.debug(f"Stop error: {e}")

    # =========================
    # Backend Implementations
    # =========================
    def _speak_dbus(self, text: str):
        try:
            subprocess.Popen([
                "gdbus", "call",
                "--session",
                "--dest", "org.gnome.Orca",
                "--object-path", "/org/gnome/Orca",
                "--method", "org.gnome.Orca.PresentMessage",
                text
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            logger.debug(f"DBus speak failed: {e}")

    def _speak_qt(self, text: str, interrupt: bool):
        try:
            if self.qt_module == "PyQt6":
                from PyQt6.QtGui import QAccessible, QAccessibleAnnouncementEvent
                from PyQt6.QtWidgets import QApplication
            else:
                from PySide6.QtGui import QAccessible, QAccessibleAnnouncementEvent
                from PySide6.QtWidgets import QApplication

            politeness = QAccessible.AnnouncementPoliteness.Assertive if interrupt else QAccessible.AnnouncementPoliteness.Polite

            widget = QApplication.activeWindow()
            if widget is None:
                return

            event = QAccessibleAnnouncementEvent(widget, text)
            event.setPoliteness(politeness)
            QAccessible.updateAccessibility(event)

        except Exception as e:
            logger.debug(f"Qt speak failed: {e}")

    def _speak_spd(self, text: str, interrupt: bool):
        try:
            if interrupt:
                subprocess.Popen(["spd-say", "-C"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.Popen(["spd-say", text], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            logger.debug(f"SPD speak failed: {e}")
