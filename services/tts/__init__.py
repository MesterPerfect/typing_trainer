import platform
import logging

from .dummy import DummyTTS

logger = logging.getLogger(__name__)

def create_tts(disable_tts=False):
    """ Factory function to create the appropriate TTS engine. """
    if disable_tts:
        logger.info("TTS explicitly disabled via CLI.")
        return DummyTTS()
        
    system = platform.system()
    logger.info(f"Detected platform: {system}")

    if system == "Windows":
        from .windows import WindowsTTS
        tts = WindowsTTS()
        if getattr(tts, 'available', True):
            return tts
            
        logger.warning("Falling back to Dummy TTS (Windows)")
        return DummyTTS()

    elif system == "Linux":
        from .linux import LinuxTTS
        tts = LinuxTTS()
        if getattr(tts, 'available', True):
            return tts
            
        logger.warning("Falling back to Dummy TTS (Linux)")
        return DummyTTS()

    elif system == "Darwin":
        from .macos import MacOSTTS
        tts = MacOSTTS()
        if getattr(tts, 'available', True):
            return tts
            
        logger.warning("Falling back to Dummy TTS (macOS)")
        return DummyTTS()

    else:
        logger.warning(f"Unsupported platform: {system}")
        return DummyTTS()
