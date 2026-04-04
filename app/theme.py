import logging
from PySide6.QtWidgets import QApplication
from core.constants import BASE_DIR

logger = logging.getLogger(__name__)

def setup_theme(app: QApplication, theme_name: str):
    """ Loads and applies the QSS stylesheet to the main application. """
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
