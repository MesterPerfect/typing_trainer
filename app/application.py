import sys
import os
import logging
import platform
import subprocess
from PySide6.QtCore import qVersion
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.constants import BASE_DIR
from utils.i18n import setup_translations
from services.settings_service import SettingsService

logger = logging.getLogger(__name__)


def _get_linux_distro_name() -> str:
    """Read the standard os-release file to get the exact Linux distribution name."""
    try:
        with open("/etc/os-release", "r") as f:
            for line in f:
                if line.startswith("PRETTY_NAME="):
                    # Extract the value and remove quotes
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
    logger.info(f"PySide6       : {qVersion()}")

    if platform.system() == "Linux":
        try:
            desktop = os.environ.get("XDG_CURRENT_DESKTOP", "Unknown")
            session_type = os.environ.get("XDG_SESSION_TYPE", "Unknown")
            logger.info(f"Desktop     : {desktop} ({session_type})")

            # Fetch Orca version using subprocess
            orca_out = subprocess.check_output(["orca", "--version"], text=True).strip()
            logger.info(f"ScreenReader: {orca_out}")
        except Exception:
            logger.info("ScreenReader: Orca not detected")

    logger.info("=" * 40)


def run_app(args=None):
    # Log the environment details right at startup
    log_system_environment()

    if args:
        logger.info(f"Launched with CLI Arguments: {vars(args)}")

    # 1. Determine Language (CLI overrides saved settings)
    settings = SettingsService()
    lang_code = args.lang if (args and args.lang) else settings.get("ui_language", "en")

    # 2. Initialize global translation function _()
    setup_translations(lang_code)

    app = QApplication(sys.argv)

    if lang_code == "ar":
        app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    else:
        app.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

    # 3. Dynamic Theme Loading Logic
    # Default to 'dark_theme' if no setting is found
    theme_name = settings.get("theme", "dark_theme") 
    theme_path = BASE_DIR / "assets" / "themes" / f"{theme_name}.qss"

    if theme_path.exists():
        try:
            with open(theme_path, "r", encoding="utf-8") as style_file:
                app.setStyleSheet(style_file.read())
            logger.info(f"Theme '{theme_name}' loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load theme {theme_name}: {e}")
    else:
        logger.warning(f"Theme file not found at {theme_path}")

    window = MainWindow(args=args)
    window.show()
    sys.exit(app.exec())