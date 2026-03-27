import sys
import logging
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.constants import BASE_DIR

logger = logging.getLogger(__name__)

def run_app():
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
