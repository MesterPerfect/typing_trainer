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
    Linux TTS with prioritized backends:
    1. Direct python-speechd library (Most robust for general Linux)
    2. DBus (Orca v49+ specific)
    3. Qt Accessibility (GUI framework integration)
    4. SPD CLI fallback (spd-say)
    Uses a background queue to ensure smooth UI performance.
    """

    def __init__(self):
        self.qt_module: Optional[str] = None
        self.QAccessible = None
        self.QAccessibleAnnouncementEvent = None
        self.QApplication = None

        # Variables for direct speechd
        self._speechd_client = None
        self._speechd_is_speaking = False

        self._backends: Dict[str, Callable] = {
            "python_speechd": self._speak_python_speechd,
            "dbus": self._speak_dbus,
            "qt": self._speak_qt,
            "spd": self._speak_spd,
        }

        self.backend = self._detect_backend()

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
        # 1. Try direct python-speechd module first
        if self._init_python_speechd():
            logger.info("LinuxTTS: Using direct python-speechd backend")
            return "python_speechd"

        # 2. Try Orca DBus
        if self._has_dbus_orca():
            logger.info("LinuxTTS: Using DBus backend (Orca v49+)")
            return "dbus"

        # 3. Try Qt Accessibility
        if self._has_qt_announcement():
            logger.info(f"LinuxTTS: Using Qt backend ({self.qt_module})")
            return "qt"

        # 4. Fallback to CLI
        logger.info("LinuxTTS: Using SPD CLI fallback backend")
        return "spd"

    def _init_python_speechd(self) -> bool:
        """Attempts to initialize the direct speechd python client."""
        try:
            import speechd
            self.speechd_module = speechd
            # CRITICAL: Client name must NOT contain spaces for the SSIP protocol
            self._speechd_client = speechd.SSIPClient("typing_trainer")
            return True
        except ImportError:
            logger.debug("python3-speechd module not installed.")
            return False
        except Exception as e:
            logger.debug(f"Failed to connect to speechd SSIP server: {e}")
            return False

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

        # CRITICAL: Qt GUI operations must run on the main thread
        if self.backend == "qt":
            if interrupt:
                self.stop()
            self._speak_qt(text, interrupt)
            return

        # For non-GUI backends, use the background queue
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

        if self.backend == "python_speechd" and self._speechd_client:
            try:
                self._speechd_client.cancel()
            except Exception as e:
                logger.debug(f"python_speechd stop error: {e}")
                
        elif self.backend == "spd":
            try:
                subprocess.Popen(
                    ["spd-say", "-C"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except Exception as e:
                logger.debug(f"SPD CLI stop error: {e}")

    def shutdown(self):
        """Clean shutdown of worker thread and clients."""
        self._stop_event.set()
        self._queue.put(("__STOP__", True))
        self._worker_thread.join(timeout=1)
        
        if self._speechd_client:
            try:
                self._speechd_client.close()
            except Exception:
                pass

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
    # Backends Implementations
    # =========================
    def _speechd_callback(self, callback_type):
        if callback_type == self.speechd_module.CallbackType.BEGIN:
            self._speechd_is_speaking = True
        elif callback_type in (self.speechd_module.CallbackType.END, self.speechd_module.CallbackType.CANCEL):
            self._speechd_is_speaking = False

    def _speak_python_speechd(self, text: str, interrupt: bool = True):
        if not self._speechd_client:
            return
        try:
            self._speechd_client.speak(
                text, 
                callback=self._speechd_callback,
                event_types=(
                    self.speechd_module.CallbackType.BEGIN,
                    self.speechd_module.CallbackType.CANCEL,
                    self.speechd_module.CallbackType.END
                )
            )
        except Exception as e:
            logger.debug(f"python_speechd speak failed: {e}")

    def _speak_dbus(self, text: str, interrupt: bool = True):
        try:
            safe_text = text.replace("'", "\\'")
            gvariant_str = f"'{safe_text}'"
            subprocess.Popen(
                [
                    "gdbus", "call", "--session", "--dest", "org.gnome.Orca",
                    "--object-path", "/org/gnome/Orca", "--method", "org.gnome.Orca.PresentMessage",
                    gvariant_str,
                ],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
        except Exception as e:
            logger.debug(f"DBus speak failed: {e}")

    def _speak_qt(self, text: str, interrupt: bool = True):
        try:
            politeness = (
                self.QAccessible.AnnouncementPoliteness.Assertive
                if interrupt else self.QAccessible.AnnouncementPoliteness.Polite
            )
            app = self.QApplication.instance()
            if not app: return
            widget = app.activeWindow() or app.focusWidget()
            if widget is None: return

            event = self.QAccessibleAnnouncementEvent(widget, text)
            event.setPoliteness(politeness)
            self.QAccessible.updateAccessibility(event)
        except Exception as e:
            logger.debug(f"Qt speak failed: {e}")

    def _speak_spd(self, text: str, interrupt: bool = True):
        try:
            subprocess.Popen(["spd-say", text], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            logger.debug(f"SPD CLI speak failed: {e}")
