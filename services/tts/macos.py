import subprocess
import logging
import threading
import queue
from typing import Tuple

from .base import BaseTTS

logger = logging.getLogger(__name__)

class MacOSTTS(BaseTTS):
    """
    macOS TTS implementation using the native 'say' command.
    Implements a background queue to ensure the GUI never freezes.
    """

    def __init__(self):
        self.available = True
        
        # Initialize background queue system
        self._queue: queue.Queue[Tuple[str, bool]] = queue.Queue()
        self._stop_event = threading.Event()
        self._worker_thread = threading.Thread(
            target=self._worker,
            daemon=True
        )
        self._worker_thread.start()
        
        logger.info("MacOSTTS initialized using native 'say' command.")

    def speak(self, text: str, interrupt: bool = True):
        if not text:
            return

        logger.debug(f"Queue macOS speak: {text} (interrupt={interrupt})")

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
        """ Stop the currently speaking phrase and clear the queue. """
        self._clear_queue()
        try:
            # killall forcefully stops the native 'say' process
            subprocess.run(["killall", "say"], stderr=subprocess.DEVNULL)
        except Exception as e:
            logger.debug(f"Error stopping macOS speech: {e}")

    def shutdown(self):
        """ Cleanly terminate the background worker thread. """
        self._stop_event.set()
        self._queue.put(("__STOP__", True))
        self._worker_thread.join(timeout=1)

    def _worker(self):
        """ Background thread loop for processing the speech queue. """
        while not self._stop_event.is_set():
            try:
                text, interrupt = self._queue.get()

                if text == "__STOP__":
                    break

                # The 'say' command runs synchronously here, 
                # but it's safe because we are in a background thread.
                subprocess.run(["say", text], stderr=subprocess.DEVNULL)

            except Exception as e:
                logger.error(f"MacOSTTS worker error: {e}")

    def _clear_queue(self):
        """ Empty the speech queue. """
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
            except queue.Empty:
                break
