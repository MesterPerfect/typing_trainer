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

        # Auto-repeat prompt timer
        self.auto_repeat_timer = QTimer()
        self.auto_repeat_timer.timeout.connect(self._auto_repeat_prompt)

    def setup_session(self, engine, is_test: bool):
        self.engine = engine
        self.is_test = is_test
        self.current_word_spoken = ""
        self.prompt_timer.stop()
        self.auto_repeat_timer.stop()

    def speak_start(self):
        if self.is_test:
            self.tts.speak(_("Test started. Good luck."), interrupt=True)
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
        self.tts.speak(_("Backspace"), interrupt=True)
        self.speak_prompt(correct=True, is_first_prompt=False)

    def speak_pause(self, is_paused: bool):
        """Announce pause or resume status."""
        if is_paused:
            self.prompt_timer.stop()
            self.auto_repeat_timer.stop()
            self.tts.speak(_("Session paused. Press Ctrl+P to resume."), interrupt=True)
        else:
            self.tts.speak(_("Session resumed."), interrupt=True)
            self._restart_auto_repeat_if_needed()
            QTimer.singleShot(700, self.speak_repeat)

    def speak_repeat(self):
        """Manually re-announce the current character/word on demand (e.g. Ctrl+R)."""
        if not self.engine or self.engine.is_finished():
            return
        message, _ = build_prompt_message(
            self.engine,
            self.settings,
            self.is_test,
            correct=True,
            is_first_prompt=True,
            current_word_spoken=""
        )
        if message:
            self.tts.speak(message, interrupt=True)
            self._restart_auto_repeat_if_needed()

    def _auto_repeat_prompt(self):
        """Periodically repeated prompt when user is idle."""
        if not self.engine or self.engine.is_finished() or getattr(self.engine.stats, "is_paused", False):
            self.auto_repeat_timer.stop()
            return
        message, _ = build_prompt_message(
            self.engine,
            self.settings,
            self.is_test,
            correct=True,
            is_first_prompt=True,
            current_word_spoken=""
        )
        if message:
            self.tts.speak(message, interrupt=False)

    def _restart_auto_repeat_if_needed(self):
        """Start or restart the auto-repeat timer if enabled in settings."""
        if self.settings.get("auto_repeat_prompt", False) and not self.is_test:
            interval_sec = max(2, int(self.settings.get("auto_repeat_interval", 4)))
            self.auto_repeat_timer.start(interval_sec * 1000)
        else:
            self.auto_repeat_timer.stop()

    def speak_completion(self, stats: dict):
        self.prompt_timer.stop()
        self.auto_repeat_timer.stop()
        self.audio.play("complete")

        if self.is_test:
            template = _("Test completed. Speed: {wpm} WPM ({cpm} CPM). Accuracy: {accuracy}%. Errors: {errors}.")
            result_msg = template.format(
                wpm=stats.get('wpm', 0),
                cpm=stats.get('cpm', 0),
                accuracy=stats.get('accuracy', 0.0),
                errors=stats.get('errors', 0)
            )
            self.tts.speak(result_msg, interrupt=True)
        else:
            self.tts.speak(_("Lesson completed"), interrupt=True)

    def _speak_queued_prompt(self):
        if self.queued_prompt:
            self.tts.speak(self.queued_prompt, interrupt=False)
            self._restart_auto_repeat_if_needed()

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
                self._restart_auto_repeat_if_needed()
            else:
                self.prompt_timer.stop()
                self.queued_prompt = message
                self.prompt_timer.start(500)
