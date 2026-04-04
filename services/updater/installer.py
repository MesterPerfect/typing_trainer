import sys
import os
import subprocess
import logging
from PySide6.QtWidgets import QApplication

# Import constants to get proper paths
from core.constants import BASE_DIR, USER_DATA_DIR

logger = logging.getLogger(__name__)

def trigger_update_installation(downloaded_file_path: str, target_version: str):
    """
    Launches the external apply_update.py script with proper arguments 
    and strictly shuts down the main application.
    """
    logger.info(f"Triggering update installation. File: {downloaded_file_path}")
    
    app = QApplication.instance()
    
    if app and hasattr(app, "telemetry"):
        app.telemetry.track("update_installation_started", {
            "target_version": target_version
        })
        app.telemetry._save_cache()

    try:
        updater_script = os.path.join(BASE_DIR, "apply_update.py")
        
        # In a built application (cx_Freeze), sys.executable is main.exe. 
        # In development, it is python.exe. We need to pass the correct exe name.
        if getattr(sys, 'frozen', False):
            exe_name = os.path.basename(sys.executable)
        else:
            exe_name = "main.py"  # Or sys.executable if running via python

        # Build the argument list expected by apply_update.py
        args = [
            sys.executable, 
            updater_script,
            "--archive", downloaded_file_path,
            "--target", str(BASE_DIR),
            "--exe", exe_name,
            "--userdata", str(USER_DATA_DIR)
        ]
        
        subprocess.Popen(args)
        logger.info("External updater launched successfully with full arguments. Exiting main application.")
        
    except Exception as e:
        logger.error(f"Failed to launch updater script: {e}")
        return

    if app:
        app.quit()
