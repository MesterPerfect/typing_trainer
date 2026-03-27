import json
import os
import logging
from typing import List
from models.result_model import LessonResult
from core.constants import RESULTS_FILE

logger = logging.getLogger(__name__)

class ResultService:
    """
    Service to handle saving and retrieving typing results using an in-memory cache
    to minimize disk I/O operations.
    """
    def __init__(self, file_path=None):
        self.file_path = str(file_path or RESULTS_FILE)
        self.cached_results = []
        self._ensure_file_exists()
        self._load_initial_data()

    def _ensure_file_exists(self):
        """ Ensure the results file and its directory exist. """
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            self._save_data([])

    def _load_initial_data(self):
        """ Load data into memory cache once at startup. """
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.cached_results = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.cached_results = []
            self._save_data(self.cached_results)

    def _save_data(self, data: list):
        """ Write raw list data to the JSON file. """
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save results: {e}")

    def save_result(self, result: LessonResult):
        """ Append a new LessonResult to the cache and save to disk. """
        self.cached_results.append({
            "lesson_id": result.lesson_id,
            "wpm": result.wpm,
            "accuracy": result.accuracy,
            "errors": result.errors,
            "time_elapsed": result.time_elapsed,
            "timestamp": result.timestamp
        })

        self._save_data(self.cached_results)
        logger.info(f"Saved result for lesson {result.lesson_id} (WPM: {result.wpm})")

    def get_results_by_lesson(self, lesson_id: str) -> List[LessonResult]:
        """ Retrieve stored results for a specific lesson ID from the memory cache. """
        return [
            LessonResult(**item) for item in self.cached_results 
            if item.get("lesson_id") == lesson_id
        ]
