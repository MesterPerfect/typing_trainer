import subprocess
import logging
import shutil
import threading
import queue
from typing import Callable, Dict, Optional, Tuple

from .base import BaseTTS

logger = logging.getLogger(__name__)


class LinuxTTS(BaseTTS):
    """
    Linux TTS with:
    - DBus (Orca v49+)
    - Qt Accessibility
    - SPD fallback
    - Speech Queue system
    """

    def __init__(self):
        self.qt_module: Optional[str] = None
        self.QAccessible = None
        self.QAccessibleAnnouncementEvent = None
        self.QApplication = None

        self.backend = self._detect_backend()

        self._backends: Dict[str, Callable] = {
            "dbus": self._speak_dbus,
            "qt": self._speak_qt,
            "spd": self._speak_spd,
        }

        # =========================
        # Queue System
        # =========================
        self._queue: queue.Queue[Tuple[str, bool]] = queue.Queue()
        self._stop_event = threading.Event()
        self._worker_thread = threading.Thread(target=self._worker, daemon=True)
        self._worker_thread.start()

        logger.info(f"LinuxTTS initialized with backend: {self.backend}")

    # =========================
    # Backend Detection
    # =========================
    def _detect_backend(self) -> str:
        if self._has_dbus_orca():
            logger.info("LinuxTTS: Using DBus backend (Orca v49+)")
            return "dbus"

        if self._has_qt_announcement():
            logger.info(f"LinuxTTS: Using Qt backend ({self.qt_module})")
            return "qt"

        logger.info("LinuxTTS: Using SPD fallback backend")
        return "spd"

    def _has_dbus_orca(self) -> bool:
        import re

        if not shutil.which("gdbus"):
            return False

        try:
            out = subprocess.check_output(
                ["orca", "--version"], text=True, stderr=subprocess.DEVNULL
            ).strip()

            match = re.search(r"(\d+)", out)
            if match and int(match.group(1)) >= 49:
                return True

        except Exception as e:
            logger.debug(f"Orca detection failed: {e}")

        return False

    def _has_qt_announcement(self) -> bool:
        try:
            from PySide6.QtGui import QAccessible, QAccessibleAnnouncementEvent
            from PySide6.QtWidgets import QApplication

            self.qt_module = "PySide6"
        except ImportError:
            try:
                from PySide6.QtGui import QAccessible, QAccessibleAnnouncementEvent
                from PySide6.QtWidgets import QApplication

                self.qt_module = "PySide6"
            except ImportError:
                return False

        self.QAccessible = QAccessible
        self.QAccessibleAnnouncementEvent = QAccessibleAnnouncementEvent
        self.QApplication = QApplication

        return True

    # =========================
    # Public API
    # =========================
    def speak(self, text: str, interrupt: bool = True):
        if not text:
            return

        logger.debug(f"Speak request: {text} (interrupt={interrupt})")

        # CRITICAL: Qt GUI operations must run on the main thread, NOT the worker thread.
        if self.backend == "qt":
            if interrupt:
                self.stop()
            self._speak_qt(text, interrupt)
            return

        # For non-GUI backends (dbus, spd), use the background queue
        if interrupt:
            self._clear_queue()
            self.stop()

        self._queue.put((text, interrupt))

    def speak_char(self, char: str):
        if not char:
            return

        if char == " ":
            self.speak("space", interrupt=True)
        else:
            self.speak(char, interrupt=True)

    def stop(self):
        """Stop current speech and clear queue."""
        self._clear_queue()

        if self.backend == "spd":
            try:
                subprocess.Popen(
                    ["spd-say", "-C"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except Exception as e:
                logger.debug(f"Stop error: {e}")

    def shutdown(self):
        """Clean shutdown of worker thread."""
        self._stop_event.set()
        self._queue.put(("__STOP__", True))
        self._worker_thread.join(timeout=1)

    # =========================
    # Queue Worker
    # =========================
    def _worker(self):
        while not self._stop_event.is_set():
            try:
                text, interrupt = self._queue.get()

                if text == "__STOP__":
                    break

                backend_func = self._backends.get(self.backend)
                if backend_func:
                    backend_func(text, interrupt)

            except Exception as e:
                logger.error(f"TTS worker error: {e}")

    def _clear_queue(self):
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
            except queue.Empty:
                break

    # =========================
    # Backends
    # =========================
    def _speak_dbus(self, text: str, interrupt: bool = True):
        try:
            # Format text as a strict GVariant string to prevent gdbus silent failures
            safe_text = text.replace("'", "\\'")
            gvariant_str = f"'{safe_text}'"

            subprocess.Popen(
                [
                    "gdbus",
                    "call",
                    "--session",
                    "--dest",
                    "org.gnome.Orca",
                    "--object-path",
                    "/org/gnome/Orca",
                    "--method",
                    "org.gnome.Orca.PresentMessage",
                    gvariant_str,
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception as e:
            logger.debug(f"DBus speak failed: {e}")

    def _speak_qt(self, text: str, interrupt: bool = True):
        try:
            politeness = (
                self.QAccessible.AnnouncementPoliteness.Assertive
                if interrupt
                else self.QAccessible.AnnouncementPoliteness.Polite
            )

            app = self.QApplication.instance()
            if not app:
                return

            widget = app.activeWindow() or app.focusWidget()
            if widget is None:
                return

            event = self.QAccessibleAnnouncementEvent(widget, text)
            event.setPoliteness(politeness)

            self.QAccessible.updateAccessibility(event)

        except Exception as e:
            logger.debug(f"Qt speak failed: {e}")

    def _speak_spd(self, text: str, interrupt: bool = True):
        try:
            # We skip "-C" here because the queue processes sequentially
            # Interruption is handled by clearing the queue in the `speak` method
            subprocess.Popen(
                ["spd-say", text], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        except Exception as e:
            logger.debug(f"SPD speak failed: {e}")
