import logging
import builtins
from core.modes import TypingMode
from utils.helpers import get_finger_instruction

logger = logging.getLogger(__name__)

class TypingSpeechHandler:
    """Handles all TTS logic and prompt generation for the typing session."""

    def __init__(self, tts, settings, audio):
        self.tts = tts
        self.settings = settings
        self.audio = audio
        self.engine = None
        self.is_test = False
        self.current_word_spoken = ""

    def setup_session(self, engine, is_test: bool):
        """Initialize the handler for a new typing session."""
        self.engine = engine
        self.is_test = is_test
        self.current_word_spoken = ""

    def _get_pronunciation(self, char: str) -> str:
        """ Maps specific single characters (like Arabic diacritics) to readable words. """
        lang = self.settings.get("ui_language", "en")
        mapping = {
            'َ': 'فتحة' if lang == 'ar' else 'Fatha',
            'ً': 'تنوين بالفتح' if lang == 'ar' else 'Tanween Fath',
            'ُ': 'ضمة' if lang == 'ar' else 'Damma',
            'ٌ': 'تنوين بالضم' if lang == 'ar' else 'Tanween Damm',
            'ِ': 'كسرة' if lang == 'ar' else 'Kasra',
            'ٍ': 'تنوين بالكسر' if lang == 'ar' else 'Tanween Kasr',
            'ْ': 'سكون' if lang == 'ar' else 'Sukun',
            'ّ': 'شدة' if lang == 'ar' else 'Shadda',
            ' ': 'مسافة' if lang == 'ar' else 'Space',
            '\n': 'سطر جديد' if lang == 'ar' else 'Enter'
        }
        return mapping.get(char, char)

    def speak_start(self):
        """Announce the start of the session."""
        if self.is_test:
            self.tts.speak("Test started. Good luck.", interrupt=True)
            self.speak_prompt(correct=True, is_first_prompt=True)
        else:
            self.speak_prompt(correct=True, is_first_prompt=True)

    def speak_char_feedback(self, char: str, correct: bool):
        """Provide feedback after a character is typed."""
        if correct:
            self.audio.play("correct")
        else:
            self.audio.play("error")

        spoken_char = self._get_pronunciation(char)

        # Instantly interrupt and speak the typed character
        if correct or self.is_test:
            self.tts.speak(spoken_char, interrupt=True)

        # Queue the next instruction prompt WITHOUT interrupting the character
        self.speak_prompt(correct=correct, is_first_prompt=False)

    def speak_backspace(self):
        """Acknowledge backspace usage."""
        self.tts.speak("Backspace", interrupt=True)
        self.speak_prompt(correct=True, is_first_prompt=False)

    def speak_completion(self, stats: dict):
        """Announce the final results when the session is over."""
        self.audio.play("complete")

        if self.is_test:
            result_msg = f"Test completed. Speed: {stats['wpm']} WPM. Accuracy: {stats['accuracy']}%. Errors: {stats['errors']}."
            self.tts.speak(result_msg, interrupt=True)
        else:
            self.tts.speak("Lesson completed", interrupt=True)

    def speak_prompt(self, correct=True, is_first_prompt=False):
        """Generate and speak the dynamic instruction prompt based on the mode."""
        if not self.settings.get("guided_mode", True) or not self.engine:
            return

        current_char = self.engine.get_current_char()
        if not current_char:
            return

        mode = self.engine.mode
        char_name = self._get_pronunciation(current_char)
        finger = get_finger_instruction(current_char)
        message = ""

        # Using localization for UI words
        try:
            type_str = _("Type")
            word_str = _("Word:")
            sentence_str = _("Sentence:")
            next_word_str = _("Next word:")
        except NameError:
            type_str = "Type"
            word_str = "Word:"
            sentence_str = "Sentence:"
            next_word_str = "Next word:"

        # ==========================================
        # Exam Mode Prompts
        # ==========================================
        if self.is_test:
            if is_first_prompt:
                if mode == TypingMode.CHARACTER:
                    message = f"{type_str} {char_name}"
                elif mode == TypingMode.WORD:
                    self.current_word_spoken = self.engine.get_current_word()
                    message = f"{word_str} {self.current_word_spoken}"
                elif mode == TypingMode.SENTENCE:
                    message = f"{sentence_str} {self.engine.text}"
            else:
                if mode == TypingMode.CHARACTER:
                    message = f"{type_str} {char_name}"
                elif mode == TypingMode.WORD:
                    word = self.engine.get_current_word()
                    if word and word != self.current_word_spoken:
                        self.current_word_spoken = word
                        message = f"{next_word_str} {word}"

        # ==========================================
        # Training Mode Prompts
        # ==========================================
        else:
            if mode == TypingMode.CHARACTER:
                if is_first_prompt:
                    message = f"{type_str} {char_name}, {finger}" if finger else f"{type_str} {char_name}"
                else:
                    message = f"{char_name}, {finger}" if finger else char_name
            elif mode == TypingMode.WORD:
                word = self.engine.get_current_word()
                if is_first_prompt or word != self.current_word_spoken:
                    self.current_word_spoken = word
                    message = f"{word_str} {word}"
                else:
                    if not correct:
                        message = f"{char_name}, {finger}" if finger else char_name
            elif mode == TypingMode.SENTENCE:
                if is_first_prompt:
                    message = f"{sentence_str} {self.engine.text}"
                elif not correct:
                    message = f"{char_name}, {finger}" if finger else char_name

        if message:
            # Crucial Fix: interrupt=False puts the instruction in the queue!
            # It will wait for the typed character to finish speaking before starting.
            self.tts.speak(message, interrupt=False)
