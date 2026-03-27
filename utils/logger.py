import logging
import os
import json
from logging.handlers import RotatingFileHandler
from core.constants import SETTINGS_FILE, LOG_FILE, LOG_DIR


def _get_configured_level() -> str:
    """ Read log level directly from settings JSON to avoid circular imports. """
    settings_path = str(SETTINGS_FILE)
    try:
        if os.path.exists(settings_path):
            with open(settings_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("log_level", "DEBUG").upper()
    except Exception:
        pass
    return "DEBUG"

def setup_logger():
    """ Configure application-wide logging using constants. """
    # Use the constants defined in core/constants.py
    os.makedirs(str(LOG_DIR), exist_ok=True)

    logger = logging.getLogger()
    
    # Apply level from settings (or fallback to DEBUG)
    level_str = _get_configured_level()
    level = getattr(logging, level_str, logging.DEBUG)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    # Use the specific log file constant
    file_handler = RotatingFileHandler(
        str(LOG_FILE), maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    file_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(file_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
