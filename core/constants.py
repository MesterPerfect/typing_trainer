import sys
import os
from pathlib import Path

try:
    from platformdirs import user_data_dir, user_log_dir
except ImportError:
    # Graceful fallback if platformdirs is not yet installed (e.g. CI / setup stages)
    def user_data_dir(appname: str, appauthor: str = None) -> str:
        if sys.platform == "win32":
            base = os.environ.get("APPDATA", os.path.expanduser("~"))
        elif sys.platform == "darwin":
            base = os.path.expanduser("~/Library/Application Support")
        else:
            base = os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))
        return os.path.join(base, appname)

    def user_log_dir(appname: str, appauthor: str = None) -> str:
        if sys.platform == "win32":
            base = os.environ.get("LOCALAPPDATA", os.path.expanduser("~"))
            return os.path.join(base, appname, "Logs")
        elif sys.platform == "darwin":
            return os.path.expanduser(f"~/Library/Logs/{appname}")
        else:
            base = os.environ.get("XDG_STATE_HOME", os.path.expanduser("~/.local/state"))
            return os.path.join(base, appname, "logs")

# =========================================================
# Application Info
# =========================================================

APP_NAME = "TypingTrainer"
APP_AUTHOR = "MesterPerfect"
APP_VERSION = "1.0.0"

# Detect if the application is running as a frozen executable (cx_Freeze / PyInstaller)
IS_FROZEN = getattr(sys, 'frozen', False)

if IS_FROZEN:
    # If frozen, the root is the directory containing the executable
    BASE_DIR = Path(os.path.dirname(sys.executable))
    IS_PORTABLE = (BASE_DIR / ".portable").exists()
    
    if IS_PORTABLE:
        # In portable mode, data and logs reside within the application folder
        USER_DATA_DIR = BASE_DIR / "user_data"
        LOG_DIR = BASE_DIR / "logs"
    else:
        # Standard user directory to guarantee write permissions on all operating systems
        USER_DATA_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR))
        LOG_DIR = Path(user_log_dir(APP_NAME, APP_AUTHOR))
else:
    # Base directory of the project (2 levels up from this file)
    BASE_DIR = Path(__file__).resolve().parent.parent
    IS_PORTABLE = False
    USER_DATA_DIR = BASE_DIR / "user_data"
    LOG_DIR = BASE_DIR / "logs"

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
