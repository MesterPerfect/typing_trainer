import sys
import os
from pathlib import Path

# =========================================================
# Application Info
# =========================================================

APP_VERSION = "1.0.0-beta3"

# =========================================================
# Paths & Directories
# =========================================================

# Detect if the application is running as a frozen executable (cx_Freeze / PyInstaller)
if getattr(sys, 'frozen', False):
    # If frozen, the root is the directory containing the executable
    BASE_DIR = Path(os.path.dirname(sys.executable))
else:
    # Base directory of the project (2 levels up from this file)
    BASE_DIR = Path(__file__).resolve().parent.parent

# Assets Directory
ASSETS_DIR = BASE_DIR / "assets"

# Icon file paths for different platforms
ICON_FILE_ICO = ASSETS_DIR / "icon.ico"
ICON_FILE_PNG = ASSETS_DIR / "icon.png"

# We create a specific folder for user data to avoid mixing with the 'data' python package
USER_DATA_DIR = BASE_DIR / "user_data"

# JSON File Paths
SETTINGS_FILE = USER_DATA_DIR / "settings.json"
RESULTS_FILE = USER_DATA_DIR / "results.json"
LESSONS_FILE = USER_DATA_DIR / "lessons.json"

# Logs
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "app.log"

# =========================================================
# Window Configuration
# =========================================================

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 650
WINDOW_TITLE = "Typing Trainer (Accessible)"
