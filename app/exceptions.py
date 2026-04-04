import sys
import logging

logger = logging.getLogger(__name__)

def setup_exception_handler(telemetry_instance=None):
    """
    Registers a global exception handler to catch all unhandled exceptions,
    log them, and send a crash report via telemetry before the app dies.
    """
    def _global_exception_handler(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
            
        # Track the crash immediately before the application dies
        if telemetry_instance:
            telemetry_instance.track("app_crashed", {
                "error_type": exc_type.__name__,
                "error_msg": str(exc_value)
            })
            telemetry_instance._save_cache() # Force synchronous save on crash
            
        logger.critical("Unhandled exception in the application:", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = _global_exception_handler
