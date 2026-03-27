from dataclasses import dataclass, field
import time

@dataclass
class LessonResult:
    """
    Data model representing the result of a completed typing lesson.
    """
    lesson_id: str
    wpm: int
    accuracy: float
    errors: int
    time_elapsed: float
    timestamp: float = field(default_factory=time.time)
