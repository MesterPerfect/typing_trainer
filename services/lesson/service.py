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
        """ Load all lessons from the JSON file. """
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
