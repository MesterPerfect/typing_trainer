from core.modes import TypingMode
from utils.helpers import get_finger_instruction
from .verbalizer import get_pronunciation

def build_prompt_message(engine, settings, is_test: bool, correct: bool, is_first_prompt: bool, current_word_spoken: str) -> tuple[str, str]:
    """ 
    Constructs the instructional message based on the current mode and state.
    Returns a tuple of (The Message String, The Updated Current Word).
    """
    if not settings.get("guided_mode", True) or not engine:
        return "", current_word_spoken

    current_char = engine.get_current_char()
    if not current_char:
        return "", current_word_spoken

    mode = engine.mode
    lang = settings.get("ui_language", "en")
    
    char_name = get_pronunciation(current_char, lang)
    finger = get_finger_instruction(current_char)
    message = ""

    # Localization mapping
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

    char_instruction = f"{char_name}, {finger}" if finger else char_name

    # --- Exam Mode ---
    if is_test:
        if is_first_prompt:
            if mode == TypingMode.CHARACTER:
                message = f"{type_str} {char_name}"
            elif mode == TypingMode.WORD:
                current_word_spoken = engine.get_current_word()
                message = f"{word_str} {current_word_spoken}"
            elif mode == TypingMode.SENTENCE:
                message = f"{sentence_str} {engine.text}"
        else:
            if mode == TypingMode.CHARACTER:
                message = f"{type_str} {char_name}"
            elif mode == TypingMode.WORD:
                word = engine.get_current_word()
                if word and word != current_word_spoken:
                    current_word_spoken = word
                    message = f"{next_word_str} {word}"

    # --- Training Mode ---
    else:
        if mode == TypingMode.CHARACTER:
            message = f"{type_str} {char_instruction}" if is_first_prompt else char_instruction
            
        elif mode == TypingMode.WORD:
            word = engine.get_current_word()
            if is_first_prompt or word != current_word_spoken:
                current_word_spoken = word
                message = f"{word_str} {word}"
            else:
                message = char_instruction
                
        elif mode == TypingMode.SENTENCE:
            message = f"{sentence_str} {engine.text}" if is_first_prompt else char_instruction

    return message, current_word_spoken
