import logging
from PyQt6.QtCore import QTimer
from core.modes import TypingMode
from utils.helpers import get_finger_instruction

logger = logging.getLogger(__name__)

class TypingSpeechHandler:
    """ Handles all TTS logic and prompt generation for the typing session. """
    
    def __init__(self, tts, settings, audio):
        self.tts = tts
        self.settings = settings
        self.audio = audio
        self.engine = None
        self.is_test = False
        self.current_word_spoken = ""

    def setup_session(self, engine, is_test: bool):
        """ Initialize the handler for a new typing session. """
        self.engine = engine
        self.is_test = is_test
        self.current_word_spoken = ""

    def speak_start(self):
        """ Announce the start of the session. """
        if self.is_test:
            self.tts.speak("Test started. Good luck.")
            QTimer.singleShot(1500, lambda: self.speak_prompt(correct=True, is_first_prompt=True))
        else:
            self.speak_prompt(correct=True, is_first_prompt=True)

    def speak_char_feedback(self, char: str, correct: bool):
        """ Provide feedback after a character is typed. """
        if correct:
            self.audio.play("correct")
        else:
            self.audio.play("error")

        if self.is_test:
            self.tts.speak_char(char)
            self.speak_prompt(correct=correct, is_first_prompt=False)
        else:
            if correct:
                self.tts.speak_char(char)
            self.speak_prompt(correct=correct, is_first_prompt=False)

    def speak_backspace(self):
        """ Acknowledge backspace usage. """
        self.tts.speak("Backspace")
        self.speak_prompt(correct=True, is_first_prompt=False)

    def speak_completion(self, stats: dict):
        """ Announce the final results when the session is over. """
        self.audio.play("complete")
        
        if self.is_test:
            result_msg = f"Test completed. Your speed is {stats['wpm']} words per minute, with {stats['accuracy']} percent accuracy. You made {stats['errors']} errors."
            self.tts.speak(result_msg)
        else:
            self.tts.speak("Lesson completed")

    def speak_prompt(self, correct=True, is_first_prompt=False):
        """ Generate and speak the dynamic instruction prompt based on the mode. """
        if not self.settings.get("guided_mode", True) or not self.engine:
            return

        current_char = self.engine.get_current_char()
        if not current_char: 
            return

        mode = self.engine.mode
        char_name = "Space" if current_char == " " else current_char
        finger = get_finger_instruction(current_char)
        message = ""

        # ==========================================
        # Exam Mode Prompts
        # ==========================================
        if self.is_test:
            if is_first_prompt:
                if mode == TypingMode.CHARACTER:
                    message = f"Type {char_name}"
                elif mode == TypingMode.WORD:
                    self.current_word_spoken = self.engine.get_current_word()
                    message = f"Word: {self.current_word_spoken}"
                elif mode == TypingMode.SENTENCE:
                    message = f"Sentence: {self.engine.text}"
            else:
                if mode == TypingMode.CHARACTER:
                    message = f"Type {char_name}"
                elif mode == TypingMode.WORD:
                    word = self.engine.get_current_word()
                    if word and word != self.current_word_spoken:
                        self.current_word_spoken = word
                        message = f"Next word: {word}"
                        
        # ==========================================
        # Training Mode Prompts
        # ==========================================
        else:
            if mode == TypingMode.CHARACTER:
                message = f"Type {char_name}, {finger}" if is_first_prompt else f"{char_name}, {finger}"
            elif mode == TypingMode.WORD:
                word = self.engine.get_current_word()
                if is_first_prompt or word != self.current_word_spoken:
                    self.current_word_spoken = word
                    message = f"Word: {word}"
                else:
                    if not correct:
                        message = f"{char_name}, {finger}"
            elif mode == TypingMode.SENTENCE:
                if is_first_prompt:
                    message = f"Sentence: {self.engine.text}"
                elif not correct:
                    message = f"{char_name}, {finger}"

        if message:
            # Shortened delay to 200ms to feel more responsive alongside audio cues
            QTimer.singleShot(200, lambda: self.tts.speak(message))
