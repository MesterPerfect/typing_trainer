import sys
import os
from pathlib import Path

# =========================================================
# Application Info
# =========================================================

APP_NAME = "typing_trainer"
APP_DISPLAY_NAME = "Typing Trainer"
APP_AUTHOR = "tecwindow"
APP_VERSION = "1.0.0"

# Detect if the application is running as a frozen executable (cx_Freeze / PyInstaller)
IS_FROZEN = getattr(sys, 'frozen', False)

if IS_FROZEN:
    BASE_DIR = Path(os.path.dirname(sys.executable))
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

IS_PORTABLE = (BASE_DIR / ".portable").exists()

def get_user_data_dir() -> Path:
    """
    Returns the user data and settings directory:
    - Windows: %APPDATA%/tecwindow/typing_trainer
    - Linux: ~/.config/tecwindow/typing_trainer (or $XDG_CONFIG_HOME/tecwindow/typing_trainer)
    - macOS: ~/Library/Application Support/tecwindow/typing_trainer
    """
    if IS_PORTABLE:
        return BASE_DIR / "user_data"

    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA")
        if appdata:
            base = Path(appdata)
        else:
            base = Path.home() / "AppData" / "Roaming"
        return base / APP_AUTHOR / APP_NAME
    elif sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / APP_AUTHOR / APP_NAME
    else:
        xdg_config = os.environ.get("XDG_CONFIG_HOME")
        if xdg_config:
            base = Path(xdg_config)
        else:
            base = Path.home() / ".config"
        return base / APP_AUTHOR / APP_NAME

def get_user_log_dir() -> Path:
    """
    Returns the user logs directory:
    - Windows: %LOCALAPPDATA%/tecwindow/typing_trainer/Logs
    - Linux: ~/.local/state/tecwindow/typing_trainer/logs (or $XDG_STATE_HOME/tecwindow/typing_trainer/logs)
    - macOS: ~/Library/Logs/tecwindow/typing_trainer
    """
    if IS_PORTABLE:
        return BASE_DIR / "logs"

    if sys.platform == "win32":
        localappdata = os.environ.get("LOCALAPPDATA")
        if localappdata:
            base = Path(localappdata)
        else:
            base = Path.home() / "AppData" / "Local"
        return base / APP_AUTHOR / APP_NAME / "Logs"
    elif sys.platform == "darwin":
        return Path.home() / "Library" / "Logs" / APP_AUTHOR / APP_NAME
    else:
        xdg_state = os.environ.get("XDG_STATE_HOME")
        if xdg_state:
            base = Path(xdg_state)
        else:
            base = Path.home() / ".local" / "state"
        return base / APP_AUTHOR / APP_NAME / "logs"

USER_DATA_DIR = get_user_data_dir()
LOG_DIR = get_user_log_dir()

USER_DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Assets Directory
ASSETS_DIR = BASE_DIR / "assets"

# Icon file paths for different platforms
ICON_FILE_ICO = ASSETS_DIR / "icon.ico"
ICON_FILE_PNG = ASSETS_DIR / "icon.png"

# JSON File Paths
SETTINGS_FILE = USER_DATA_DIR / "settings.json"
RESULTS_FILE = USER_DATA_DIR / "results.json"
LESSONS_FILE = USER_DATA_DIR / "lessons.json"

# Logs
LOG_FILE = LOG_DIR / "app.log"

# =========================================================
# Window Configuration
# =========================================================

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 650
WINDOW_TITLE = "Typing Trainer (Accessible)"
