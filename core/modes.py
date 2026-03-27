from enum import Enum

class TypingMode(Enum):
    CHARACTER = "character"
    WORD = "word"
    SENTENCE = "sentence"

class ExplorerMode(Enum):
    FREE = "free"
    ARABIC = "arabic"
    ENGLISH = "english"
    NUMBERS = "numbers"
