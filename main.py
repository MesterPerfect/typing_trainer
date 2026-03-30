import logging
from utils.cli import parse_arguments
from utils.logger import setup_logger
from app.application import run_app
from services.settings_service import SettingsService

# We initialize a very basic logger just in case SettingsService fails before our main logger is up
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    # 1. Parse CLI arguments first
    args = parse_arguments()
    
    # 2. Load settings from JSON to resolve logging preferences
    settings = SettingsService()
    
    # 3. Resolve Log Level (CLI takes precedence over JSON)
    final_log_level = args.log_level if args.log_level else settings.get("log_level", "INFO")
    
    # 4. Resolve Timestamp (CLI takes precedence over JSON)
    # If args.no_log_time is True, use it. Otherwise, fallback to the JSON setting.
    final_no_log_time = True if args.no_log_time else settings.get("no_log_time", False)
    
    # 5. Setup logger with the merged settings (This overrides the basicConfig above)
    setup_logger(cli_level=final_log_level, no_log_time=final_no_log_time)
    
    # 6. Launch the application passing the arguments
    run_app(args)
