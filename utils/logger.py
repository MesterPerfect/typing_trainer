import logging
import json
from logging.handlers import RotatingFileHandler
from core.constants import SETTINGS_FILE, LOG_FILE, LOG_DIR

def _get_configured_level() -> str:
    """ Read log level directly from settings JSON to avoid circular imports. """
    try:
        if SETTINGS_FILE.exists():
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("log_level", "DEBUG").upper()
    except Exception:
        pass
    return "DEBUG"

def setup_logger(cli_level=None, no_log_time=False):
    """ Configure application-wide logging with CLI overrides. """
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger()
    
    # Apply level from CLI (highest priority) or settings
    level_str = cli_level if cli_level else _get_configured_level()
    level = getattr(logging, level_str, logging.DEBUG)
    logger.setLevel(level)

    # Remove any existing handlers (like the one created by basicConfig in main.py)
    # to ensure our custom format and file handler are applied correctly.
    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = RotatingFileHandler(
        str(LOG_FILE), maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    
    # Adjust format based on CLI flag
    if no_log_time:
        format_str = "%(levelname)s - %(name)s - %(message)s"
    else:
        format_str = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        
    formatter = logging.Formatter(format_str)
    
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
