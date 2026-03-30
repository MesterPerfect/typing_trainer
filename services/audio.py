import logging
from pathlib import Path
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtCore import QUrl
from core.constants import BASE_DIR

logger = logging.getLogger(__name__)


class AudioService:
    def __init__(self, settings):
        self.settings = settings
        self.sounds = {}

        # Use BASE_DIR for bulletproof path resolution
        self._load_sound("correct", BASE_DIR / "assets" / "sounds" / "correct.wav")
        self._load_sound("error", BASE_DIR / "assets" / "sounds" / "error.wav")
        self._load_sound("complete", BASE_DIR / "assets" / "sounds" / "complete.wav")

    def _load_sound(self, name: str, filepath: Path):
        if not filepath.exists():
            logger.warning(f"Sound file not found: {filepath}")
            return

        try:
            effect = QSoundEffect()
            # Resolve absolute path natively using pathlib
            effect.setSource(QUrl.fromLocalFile(str(filepath.resolve())))
            self.sounds[name] = effect
            logger.info(f"Loaded sound effect: {name}")
        except Exception as e:
            logger.error(f"Failed to load sound {name}: {e}")

    def play(self, name: str):
        is_enabled = self.settings.get("sound_effects", True)
        if not is_enabled:
            return

        if name in self.sounds:
            volume = self.settings.get("sound_volume", 70) / 100.0
            self.sounds[name].setVolume(volume)
            self.sounds[name].play()
            logger.debug(f"Playing sound: {name} at volume {volume}")
        else:
            logger.debug(f"Sound '{name}' not found or not loaded.")
