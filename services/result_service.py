import json
import logging
from pathlib import Path
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
        self.file_path = Path(file_path) if file_path else RESULTS_FILE
        self.cached_results = []
        self._ensure_file_exists()
        self._load_initial_data()

    def _ensure_file_exists(self):
        """ Ensure the results file and its directory exist. """
        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
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
            "cpm": result.cpm,
            "accuracy": result.accuracy,
            "errors": result.errors,
            "time_elapsed": result.time_elapsed,
            "timestamp": result.timestamp
        })

        self._save_data(self.cached_results)
        logger.info(f"Saved result for lesson {result.lesson_id} (WPM: {result.wpm}, CPM: {result.cpm})")

    def get_results_by_lesson(self, lesson_id: str) -> List[LessonResult]:
        """ Retrieve stored results for a specific lesson ID from the memory cache. """
        return [
            LessonResult(**item) for item in self.cached_results 
            if item.get("lesson_id") == lesson_id
        ]

    def clear_all_results(self) -> bool:
        """ Wipe all cached and saved results history. """
        self.cached_results = []
        self._save_data(self.cached_results)
        logger.info("Cleared all typing results history.")
        return True

    def get_lifetime_summary(self) -> dict:
        """ Compute aggregate statistics across all recorded sessions. """
        total_sessions = len(self.cached_results)
        if total_sessions == 0:
            return {
                "total_sessions": 0,
                "peak_wpm": 0,
                "peak_cpm": 0,
                "avg_wpm": 0.0,
                "avg_accuracy": 100.0,
                "total_time_seconds": 0.0
            }

        wpms = [item.get("wpm", 0) for item in self.cached_results]
        cpms = [item.get("cpm", 0) for item in self.cached_results]
        accuracies = [item.get("accuracy", 100.0) for item in self.cached_results]
        times = [item.get("time_elapsed", 0.0) for item in self.cached_results]

        return {
            "total_sessions": total_sessions,
            "peak_wpm": max(wpms, default=0),
            "peak_cpm": max(cpms, default=0),
            "avg_wpm": round(sum(wpms) / total_sessions, 1),
            "avg_accuracy": round(sum(accuracies) / total_sessions, 1),
            "total_time_seconds": round(sum(times), 1)
        }

    def export_to_csv(self, target_path: Path, lesson_titles: dict = None) -> bool:
        """ Export all results history to a CSV file. """
        import csv
        from datetime import datetime
        
        lesson_titles = lesson_titles or {}
        target_path = Path(target_path)
        try:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            with open(target_path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Date", "Lesson ID", "Lesson Title", "WPM", "CPM", "Accuracy (%)", "Errors", "Time (seconds)"])
                for item in self.cached_results:
                    ts = item.get("timestamp", 0)
                    date_str = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S") if ts else ""
                    lid = str(item.get("lesson_id", ""))
                    ltitle = lesson_titles.get(lid, lid)
                    writer.writerow([
                        ts,
                        date_str,
                        lid,
                        ltitle,
                        item.get("wpm", 0),
                        item.get("cpm", 0),
                        item.get("accuracy", 100.0),
                        item.get("errors", 0),
                        item.get("time_elapsed", 0.0)
                    ])
            logger.info(f"Exported results to CSV at {target_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to export CSV: {e}")
            return False
