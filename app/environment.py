import os
import logging
import platform
import subprocess
from PySide6.QtCore import qVersion

logger = logging.getLogger(__name__)

def _get_linux_distro_name() -> str:
    """Read the standard os-release file to get the exact Linux distribution name."""
    try:
        with open("/etc/os-release", "r") as f:
            for line in f:
                if line.startswith("PRETTY_NAME="):
                    return line.split("=")[1].strip().strip('"')
    except Exception:
        pass
    return "Unknown Linux Distribution"

def log_system_environment():
    """Log comprehensive and clean details about the OS, Audio, and Screen Reader environment."""
    logger.info("=" * 40)
    logger.info("SYSTEM ENVIRONMENT INFO")
    logger.info("=" * 40)

    if platform.system() == "Linux":
        os_name = _get_linux_distro_name()
        logger.info(f"OS Platform : {os_name}")
        logger.info(f"Kernel      : {platform.release()}")
    else:
        logger.info(f"OS Platform : {platform.system()} {platform.release()}")
        logger.info(f"OS Version  : {platform.version()}")

    logger.info(f"Python      : {platform.python_version()}")
    logger.info(f"PySide6     : {qVersion()}")

    if platform.system() == "Linux":
        try:
            desktop = os.environ.get("XDG_CURRENT_DESKTOP", "Unknown")
            session_type = os.environ.get("XDG_SESSION_TYPE", "Unknown")
            logger.info(f"Desktop     : {desktop} ({session_type})")

            orca_out = subprocess.check_output(["orca", "--version"], text=True).strip()
            logger.info(f"ScreenReader: {orca_out}")
        except Exception:
            logger.info("ScreenReader: Orca not detected")

    logger.info("=" * 40)

def detect_screen_reader() -> str:
    """Accurately detects the active screen reader for telemetry purposes."""
    sys_plat = platform.system()
    if sys_plat == "Linux":
        try:
            return subprocess.check_output(["orca", "--version"], text=True).strip()
        except Exception:
            return "Orca not detected"
    elif sys_plat == "Windows":
        try:
            from UniversalSpeech import UniversalSpeech
            temp_speech = UniversalSpeech()
            return temp_speech.engine_used
        except Exception:
            return "UniversalSpeech failed/Missing DLLs"
    elif sys_plat == "Darwin":
        return "VoiceOver"
    
    return "Unknown"
