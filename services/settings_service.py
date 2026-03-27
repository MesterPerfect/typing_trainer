import json
import os
import logging
from typing import Any
from core.constants import SETTINGS_FILE

logger = logging.getLogger(__name__)

class SettingsService:
    def __init__(self, file_path=None):
        # Convert Path object to string for standard file operations
        self.file_path = str(file_path or SETTINGS_FILE)
        self.settings = self._load_settings()

    def _load_settings(self) -> dict:
        """
        Load settings from the JSON file.
        Returns default settings if the file does not exist or is corrupted.
        """
        default_settings = {
            "guided_mode": True,
            "tts_enabled": True,
            "sound_effects": True,
            "sound_volume": 70
        }

        if not os.path.exists(self.file_path):
            self._save_to_file(default_settings)
            return default_settings

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                loaded_settings = json.load(f)
                
                # Merge loaded settings with defaults to ensure all keys exist
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
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
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
        Update a specific setting and save to file.
        """
        self.settings[key] = value
        self._save_to_file(self.settings)
        logger.info(f"Setting '{key}' updated to: {value}")
