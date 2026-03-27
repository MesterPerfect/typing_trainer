from dataclasses import dataclass

@dataclass
class Lesson:
    id: str
    title: str
    text: str
    difficulty: int
    language: str = "en"
    lesson_type: str = "lesson"
