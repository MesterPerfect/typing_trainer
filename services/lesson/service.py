import json
import logging
from pathlib import Path
from typing import List

from models.lesson_model import Lesson
from core.constants import LESSONS_FILE
from .default_data import DEFAULT_LESSONS

logger = logging.getLogger(__name__)

class LessonService:
    """ Service to handle loading, saving, and managing typing lessons. """
    
    def __init__(self, file_path=None):
        self.file_path = Path(file_path) if file_path else LESSONS_FILE
        self._ensure_default_lessons()

    def _ensure_default_lessons(self):
        """ Create a default lessons JSON file if it does not exist. """
        if not self.file_path.exists():
            logger.info(f"Lessons file not found at {self.file_path}. Creating default.")
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                with open(self.file_path, "w", encoding="utf-8") as f:
                    json.dump(DEFAULT_LESSONS, f, indent=4, ensure_ascii=False)
                logger.info("Default lessons file created successfully.")
            except Exception as e:
                logger.error(f"Failed to create default lessons file: {e}")

    def load_all_lessons(self) -> List[Lesson]:
        """ Load all lessons from the lessons JSON file. """
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            lessons = []
            for item in data:
                lesson = Lesson(
                    id=item.get("id", ""),
                    title=item.get("title", "Untitled"),
                    text=item.get("text", ""),
                    difficulty=item.get("difficulty", 1),
                    language=item.get("language", "en"),
                    lesson_type=item.get("lesson_type", "lesson")
                )
                lessons.append(lesson)
            
            logger.info(f"Successfully loaded {len(lessons)} lessons.")
            return lessons
            
        except Exception as e:
            logger.error(f"Failed to load lessons: {e}")
            return []

    def save_all_lessons(self, lessons: List[Lesson]) -> bool:
        """ Save a list of Lesson objects back to the JSON file. """
        try:
            data = []
            for lesson in lessons:
                data.append({
                    "id": lesson.id,
                    "title": lesson.title,
                    "text": lesson.text,
                    "difficulty": lesson.difficulty,
                    "language": lesson.language,
                    "lesson_type": lesson.lesson_type
                })
                
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                
            logger.info("Lessons saved successfully.")
            return True
        except Exception as e:
            logger.error(f"Failed to save lessons: {e}")
            return False

    def export_package(self, target_path: Path, lessons: List[Lesson]) -> bool:
        """ Export lessons to an external JSON package file. """
        target_path = Path(target_path)
        try:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            data = [
                {
                    "id": l.id,
                    "title": l.title,
                    "text": l.text,
                    "difficulty": l.difficulty,
                    "language": l.language,
                    "lesson_type": l.lesson_type
                }
                for l in lessons
            ]
            with open(target_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logger.info(f"Exported {len(lessons)} lessons to {target_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to export lesson package: {e}")
            return False

    def import_package(self, source_path: Path) -> List[Lesson]:
        """ Read lessons from an external JSON package file. """
        source_path = Path(source_path)
        try:
            with open(source_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                logger.error("Invalid package format: expected a list of lessons.")
                return []
            lessons = []
            for item in data:
                if isinstance(item, dict) and "text" in item and "title" in item:
                    lessons.append(Lesson(
                        id=item.get("id", ""),
                        title=item.get("title", "Untitled"),
                        text=item.get("text", ""),
                        difficulty=int(item.get("difficulty", 1)),
                        language=item.get("language", "en"),
                        lesson_type=item.get("lesson_type", "lesson")
                    ))
            logger.info(f"Successfully imported {len(lessons)} lessons from {source_path}")
            return lessons
        except Exception as e:
            logger.error(f"Failed to import lesson package: {e}")
            return []
