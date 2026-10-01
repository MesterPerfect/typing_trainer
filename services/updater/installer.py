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
        is_frozen = getattr(sys, 'frozen', False)
        if is_frozen:
            target_dir = os.path.dirname(sys.executable)
            main_exe = os.path.basename(sys.executable)
            updater_exe = "apply_update.exe" if sys.platform == "win32" else "apply_update"
            updater_path = os.path.join(target_dir, updater_exe)
            
            if not os.path.exists(updater_path):
                logger.error(f"Updater binary not found at {updater_path}")
                return

            args = [
                updater_path,
                "--archive", downloaded_file_path,
                "--target", target_dir,
                "--exe", main_exe,
                "--userdata", str(USER_DATA_DIR)
            ]
            if sys.platform == "win32":
                subprocess.Popen(args, creationflags=subprocess.DETACHED_PROCESS)
            else:
                subprocess.Popen(args, start_new_session=True)
            logger.info("External standalone updater launched successfully. Exiting main application.")
        else:
            updater_script = os.path.join(BASE_DIR, "apply_update.py")
            args = [
                sys.executable,
                updater_script,
                "--archive", downloaded_file_path,
                "--target", str(BASE_DIR),
                "--exe", "main.py",
                "--userdata", str(USER_DATA_DIR)
            ]
            subprocess.Popen(args)
            logger.info("Dev mode: updater script launched via python interpreter. Exiting main application.")
            
    except Exception as e:
        logger.error(f"Failed to launch updater script: {e}")
        return

    if app:
        app.quit()
