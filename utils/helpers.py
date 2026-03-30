def get_finger_instruction(char: str) -> str:
    """ Returns the finger instruction for a given character in English. """
    mapping = {
        # --- English Left Hand ---
        'a': 'Left Pinky', 'q': 'Top Left Pinky', 'z': 'Bottom Left Pinky',
        's': 'Left Ring', 'w': 'Top Left Ring', 'x': 'Bottom Left Ring',
        'd': 'Left Middle', 'e': 'Top Left Middle', 'c': 'Bottom Left Middle',
        'f': 'Left Index', 'r': 'Top Left Index', 'v': 'Bottom Left Index',
        'g': 'Right of Left Index', 't': 'Top Right of Left Index', 'b': 'Bottom Right of Left Index',
        
        # --- English Right Hand ---
        'j': 'Right Index', 'u': 'Top Right Index', 'm': 'Bottom Right Index',
        'h': 'Left of Right Index', 'y': 'Top Left of Right Index', 'n': 'Bottom Left of Right Index',
        'k': 'Right Middle', 'i': 'Top Right Middle', ',': 'Bottom Right Middle',
        'l': 'Right Ring', 'o': 'Top Right Ring', '.': 'Bottom Right Ring',
        ';': 'Right Pinky', 'p': 'Top Right Pinky', '/': 'Bottom Right Pinky',
        
        # --- Punctuation and Symbols (Shift cases mostly) ---
        ':': 'Right Pinky (with Shift)',
        '"': 'Right Pinky (with Shift)',
        "'": 'Right Pinky',
        '?': 'Bottom Right Pinky (with Shift)',
        '-': 'Top Right Pinky (reach up)',
        '_': 'Top Right Pinky (with Shift)',
        '!': 'Top Left Pinky (with Shift)',

        # --- Arabic Left Hand ---
        'ش': 'Left Pinky', 'ض': 'Top Left Pinky', 'ذ': 'Top Left of Left Pinky',
        'س': 'Left Ring', 'ص': 'Top Left Ring', 'ئ': 'Bottom Left Ring',
        'ي': 'Left Middle', 'ث': 'Top Left Middle', 'ء': 'Bottom Left Middle',
        'ب': 'Left Index', 'ق': 'Top Left Index', 'ؤ': 'Bottom Left Index',
        'ل': 'Right of Left Index', 'ف': 'Top Right of Left Index', 'ر': 'Bottom Right of Left Index',

        # --- Arabic Right Hand ---
        'ت': 'Right Index', 'ع': 'Top Right Index', 'ى': 'Bottom Right Index',
        'ا': 'Left of Right Index', 'غ': 'Top Left of Right Index', 'لا': 'Bottom Left of Right Index',
        'ن': 'Right Middle', 'ه': 'Top Right Middle', 'ة': 'Bottom Right Middle',
        'م': 'Right Ring', 'خ': 'Top Right Ring', 'و': 'Bottom Right Ring',
        'ك': 'Right Pinky', 'ح': 'Top Right Pinky', 'ز': 'Bottom Right Pinky',
        'ط': 'Right of Right Pinky', 'ج': 'Top Right of Right Pinky', 'ظ': 'Bottom Right of Right Pinky',
        'د': 'Far Right of Right Pinky',
        
        # --- Common ---
        ' ': 'Thumb'
    }
    return mapping.get(char.lower(), "")
