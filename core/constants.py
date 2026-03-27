from pathlib import Path

# =========================================================
# Paths & Directories
# =========================================================

# Base directory of the project (2 levels up from this file)
BASE_DIR = Path(__file__).resolve().parent.parent

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
