import logging
from PySide6.QtCore import QTimer

from .verbalizer import get_pronunciation
from .prompt_builder import build_prompt_message

logger = logging.getLogger(__name__)

class TypingSpeechHandler:
    """
    Coordinates TTS engine, Audio service, and Timing for typing feedback.
    Delegates prompt creation to PromptBuilder and text mapping to Verbalizer.
    """

    def __init__(self, tts, settings, audio):
        self.tts = tts
        self.settings = settings
        self.audio = audio
        self.engine = None
        self.is_test = False
        self.current_word_spoken = ""
        
        self.prompt_timer = QTimer()
        self.prompt_timer.setSingleShot(True)
        self.prompt_timer.timeout.connect(self._speak_queued_prompt)
        self.queued_prompt = ""

    def setup_session(self, engine, is_test: bool):
        self.engine = engine
        self.is_test = is_test
        self.current_word_spoken = ""
        self.prompt_timer.stop()

    def speak_start(self):
        if self.is_test:
            self.tts.speak("Test started. Good luck.", interrupt=True)
            QTimer.singleShot(1500, lambda: self.speak_prompt(correct=True, is_first_prompt=True))
        else:
            self.speak_prompt(correct=True, is_first_prompt=True)

    def speak_char_feedback(self, char: str, correct: bool):
        if correct:
            self.audio.play("correct")
        else:
            self.audio.play("error")

        lang = self.settings.get("ui_language", "en")
        spoken_char = get_pronunciation(char, lang)

        if correct or self.is_test:
            self.tts.speak(spoken_char, interrupt=True)

        self.speak_prompt(correct=correct, is_first_prompt=False)

    def speak_backspace(self):
        self.tts.speak("Backspace", interrupt=True)
        self.speak_prompt(correct=True, is_first_prompt=False)

    def speak_completion(self, stats: dict):
        self.prompt_timer.stop()
        self.audio.play("complete")

        if self.is_test:
            result_msg = f"Test completed. Speed: {stats['wpm']} WPM. Accuracy: {stats['accuracy']}%. Errors: {stats['errors']}."
            self.tts.speak(result_msg, interrupt=True)
        else:
            self.tts.speak("Lesson completed", interrupt=True)

    def _speak_queued_prompt(self):
        if self.queued_prompt:
            self.tts.speak(self.queued_prompt, interrupt=False)

    def speak_prompt(self, correct=True, is_first_prompt=False):
        # Delegate prompt building to our pure function in prompt_builder.py
        message, updated_word = build_prompt_message(
            self.engine, 
            self.settings, 
            self.is_test, 
            correct, 
            is_first_prompt, 
            self.current_word_spoken
        )
        
        self.current_word_spoken = updated_word

        if message:
            if is_first_prompt:
                self.tts.speak(message, interrupt=True)
            else:
                self.prompt_timer.stop()
                self.queued_prompt = message
                self.prompt_timer.start(500)
