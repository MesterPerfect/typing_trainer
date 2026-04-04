import sys
import logging
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow
from core.constants import USER_DATA_DIR, APP_VERSION
from utils.i18n import setup_translations
from services.settings_service import SettingsService
from services.telemetry import TelemetryService

# Import from our newly created modular package
from .environment import log_system_environment, detect_screen_reader
from .exceptions import setup_exception_handler
from .theme import setup_theme

logger = logging.getLogger(__name__)

def run_app(args=None):
    """ Main application entry point orchestrating the startup sequence. """
    
    # 1. Log the environment details right at startup
    log_system_environment()

    if args:
        logger.info(f"Launched with CLI Arguments: {vars(args)}")

    # 2. Determine Language
    settings = SettingsService()
    lang_code = args.lang if (args and args.lang) else settings.get("ui_language", "en")

    # 3. Initialize Telemetry Service & Error Handling
    screen_reader_info = detect_screen_reader()
    telemetry_enabled = settings.get("telemetry_enabled", True)
    
    telemetry_instance = TelemetryService(
        user_data_dir=str(USER_DATA_DIR), 
        app_version=APP_VERSION,
        language=lang_code,
        screen_reader=screen_reader_info,
        enabled=telemetry_enabled
    )
    telemetry_instance.start_session()
    
    # Register the global exception handler and pass telemetry to it
    setup_exception_handler(telemetry_instance)

    # 4. Initialize Translations
    setup_translations(lang_code)

    # 5. Setup QApplication
    app = QApplication(sys.argv)
    app.telemetry = telemetry_instance
    
    app.setApplicationName("Typing Trainer")
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName("MesterPerfect")

    if lang_code == "ar":
        app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    else:
        app.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

    # 6. Apply Theme
    theme_name = settings.get("theme", "dark_theme") 
    setup_theme(app, theme_name)

    # 7. Launch UI
    window = MainWindow(args=args)
    window.show()
    
    # 8. Run Event Loop
    exit_code = app.exec()
    
    # 9. Clean Exit
    telemetry_instance.end_session()
    sys.exit(exit_code)
