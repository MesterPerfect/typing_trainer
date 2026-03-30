from core.modes import TypingMode
from core.statistics import TypingStatistics
import logging

logger = logging.getLogger(__name__)

class TypingResult:
    """
    Represents the result of a single key press.
    """
    def __init__(self, expected: str, actual: str, correct: bool, index: int):
        self.expected = expected
        self.actual = actual
        self.correct = correct
        self.index = index

class TypingEngine:
    """
    Typing engine with:
    - Lock-step typing
    - Backspace support
    - Modes (character / word / sentence)
    - Integrated statistics tracking
    """
    def __init__(self, text: str, mode: TypingMode = TypingMode.CHARACTER):
        self.text = text
        self.mode = mode

        self.current_index = 0
        self.typed = []
        
        # Initialize statistics tracker
        self.stats = TypingStatistics()

        logger.info(f"TypingEngine initialized (mode={mode.name})")

    def start(self):
        self.stats.start()
        logger.info("Typing session started")

    def process_char(self, char: str) -> TypingResult:
        # Check for completion before doing anything to prevent phantom timer starts
        if self.is_finished():
            logger.debug("Typing already finished, ignoring input")
            return None

        # Start timer on the very first valid keystroke
        if not self.stats.is_running:
            self.start()

        expected = self.text[self.current_index]
        correct = char == expected

        # Record keystroke for statistics
        self.stats.record_keystroke(correct)

        if correct:
            self.typed.append(char)
            self.current_index += 1

        logger.debug(f"[CHAR] '{char}' | Expected: '{expected}' | Correct: {correct}")

        return TypingResult(expected, char, correct, self.current_index)

    def backspace(self):
        if not self.typed:
            logger.debug("Backspace ignored (nothing to delete)")
            return

        removed = self.typed.pop()
        self.current_index -= 1
        logger.debug(f"[BACKSPACE] Removed '{removed}'")

    def is_finished(self) -> bool:
        return self.current_index >= len(self.text)

    def get_current_char(self) -> str:
        if self.is_finished():
            return ""
        return self.text[self.current_index]

    def progress(self) -> float:
        if not self.text:
            return 0.0
        return (self.current_index / len(self.text)) * 100

    def get_display_parts(self):
        correct_part = "".join(self.typed)
        current_char = self.get_current_char()
        remaining = self.text[self.current_index + 1:]
        return correct_part, current_char, remaining

    def get_stats(self):
        # Merge progress with the statistics dictionary
        stats_dict = self.stats.get_current_stats()
        stats_dict["progress"] = self.progress()
        return stats_dict

    def get_current_word(self) -> str:
        if self.is_finished():
            return ""

        words = self.text.split(" ")
        char_count = 0

        for word in words:
            if self.current_index < char_count + len(word):
                return word
            char_count += len(word) + 1

        return ""

    def get_prompt_unit(self) -> str:
        if self.mode == TypingMode.CHARACTER:
            return self.get_current_char()
        elif self.mode == TypingMode.WORD:
            return self.get_current_word()
        elif self.mode == TypingMode.SENTENCE:
            return self.text
        return ""
