import json
import logging
from pathlib import Path
from typing import Any
from core.constants import SETTINGS_FILE

logger = logging.getLogger(__name__)

class SettingsService:
    def __init__(self, file_path=None):
        # Use pathlib natively instead of casting to string
        self.file_path = Path(file_path) if file_path else SETTINGS_FILE
        self.settings = self._load_settings()

    def _load_settings(self) -> dict:
        """
        Load settings from the JSON file.
        Returns a comprehensive default settings dictionary if the file is missing or corrupted.
        """
        # Master list of all application defaults
        default_settings = {
            "ui_language": "en",
            "theme": "dark_theme",
            "auto_update": True,
            "guided_mode": True,
            "tts_enabled": True,
            "sound_effects": True,
            "sound_volume": 70,
            "show_virtual_keyboard": True,
            "enable_logging": True,
            "log_level": "INFO",
            "no_log_time": False
        }

        if not self.file_path.exists():
            self._save_to_file(default_settings)
            return default_settings

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                loaded_settings = json.load(f)
                
            # Merge loaded settings with defaults to ensure no missing keys
            for key, value in default_settings.items():
                if key not in loaded_settings:
                    loaded_settings[key] = value
                    
            return loaded_settings
        except Exception as e:
            logger.error(f"Failed to load settings: {e}")
            return default_settings

    def _save_to_file(self, data: dict):
        """
        Save the provided dictionary to the JSON file.
        """
        # Create parent directories if they don't exist using pathlib
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a specific setting.
        """
        return self.settings.get(key, default)

    def set(self, key: str, value: Any):
        """
        Update a specific setting and save to file only if the value has changed.
        """
        # Prevent redundant Disk I/O operations if the value is identical
        if self.settings.get(key) == value:
            return

        self.settings[key] = value
        self._save_to_file(self.settings)
        logger.info(f"Setting '{key}' updated to: {value}")
        
    def update_many(self, new_settings: dict):
        """
        Batch update multiple settings and trigger a single file write.
        (Useful for bulk saves from the Settings UI)
        """
        changed = False
        for key, value in new_settings.items():
            if self.settings.get(key) != value:
                self.settings[key] = value
                changed = True
                logger.info(f"Setting '{key}' updated to: {value}")
        
        if changed:
            self._save_to_file(self.settings)
