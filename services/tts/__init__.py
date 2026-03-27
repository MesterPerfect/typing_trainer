import platform
import logging

from .dummy import DummyTTS

logger = logging.getLogger(__name__)

def create_tts():
    """ Factory function to create the appropriate TTS engine. """
    system = platform.system()
    logger.info(f"Detected platform: {system}")

    if system == "Windows":
        from .windows import WindowsTTS
        tts = WindowsTTS()
        if tts.available:
            return tts
            
        logger.warning("Falling back to Dummy TTS (Windows)")
        return DummyTTS()

    elif system == "Linux":
        from .linux import LinuxTTS
        tts = LinuxTTS()
        if tts.available:
            return tts
            
        logger.warning("Falling back to Dummy TTS (Linux)")
        return DummyTTS()

    else:
        logger.warning(f"Unsupported platform: {system}")
        return DummyTTS()
