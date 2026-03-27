import sys
import os
import logging
import platform
import subprocess
from PyQt6.QtCore import qVersion
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.constants import BASE_DIR

logger = logging.getLogger(__name__)

def log_system_environment():
    """ Log comprehensive details about the OS, Audio, and Screen Reader environment. """
    logger.info("="*40)
    logger.info("SYSTEM ENVIRONMENT INFO")
    logger.info("="*40)
    logger.info(f"OS Platform : {platform.system()} {platform.release()}")
    logger.info(f"OS Version  : {platform.version()}")
    logger.info(f"Python      : {platform.python_version()}")
    logger.info(f"PyQt6       : {qVersion()}")
    
    if platform.system() == "Linux":
        try:
            desktop = os.environ.get("XDG_CURRENT_DESKTOP", "Unknown")
            session_type = os.environ.get("XDG_SESSION_TYPE", "Unknown")
            logger.info(f"Desktop     : {desktop} ({session_type})")
            
            orca_out = subprocess.check_output(["orca", "--version"], text=True).strip()
            logger.info(f"ScreenReader: {orca_out}")
        except Exception:
            logger.info("ScreenReader: Orca not detected")
    logger.info("="*40)


def run_app():
    # Log the environment details right at startup
    log_system_environment()
    
    app = QApplication(sys.argv)
    
    # Use BASE_DIR for absolute, bulletproof path resolution
    style_path = BASE_DIR / "assets" / "styles.qss"
    
    if style_path.exists():
        try:
            with open(style_path, "r", encoding="utf-8") as style_file:
                app.setStyleSheet(style_file.read())
            logger.info("Stylesheet loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load stylesheet: {e}")
    else:
        logger.warning(f"Stylesheet not found at {style_path}")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
