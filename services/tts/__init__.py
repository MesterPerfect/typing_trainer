import platform
import logging
from PySide6.QtWidgets import QApplication

from .dummy import DummyTTS

logger = logging.getLogger(__name__)

def _track_fallback(system: str, reason: str):
    """ Helper to track critical TTS failures before returning DummyTTS. """
    app = QApplication.instance()
    if app and hasattr(app, "telemetry"):
        app.telemetry.track("tts_critical_failure", {
            "platform": system,
            "reason": reason
        })

def create_tts(disable_tts=False):
    """ Factory function to create the appropriate TTS engine. """
    if disable_tts:
        logger.info("TTS explicitly disabled via CLI.")
        return DummyTTS()
        
    system = platform.system()
    logger.info(f"Detected platform: {system}")

    try:
        if system == "Windows":
            from .windows import WindowsTTS
            tts = WindowsTTS()
            if getattr(tts, 'available', True):
                return tts
            logger.warning("Falling back to Dummy TTS (Windows)")
            _track_fallback(system, "unavailable_or_missing_dll")
            return DummyTTS()

        elif system == "Linux":
            from .linux import LinuxTTS
            tts = LinuxTTS()
            if getattr(tts, 'available', True):
                return tts
            logger.warning("Falling back to Dummy TTS (Linux)")
            _track_fallback(system, "all_backends_failed")
            return DummyTTS()

        elif system == "Darwin":
            from .macos import MacOSTTS
            tts = MacOSTTS()
            if getattr(tts, 'available', True):
                return tts
            logger.warning("Falling back to Dummy TTS (macOS)")
            _track_fallback(system, "unavailable")
            return DummyTTS()

        else:
            logger.warning(f"Unsupported platform: {system}")
            _track_fallback(system, "unsupported_platform")
            return DummyTTS()
            
    except Exception as e:
        logger.error(f"Failed to initialize TTS engine for {system}: {e}")
        _track_fallback(system, str(e))
        return DummyTTS()
