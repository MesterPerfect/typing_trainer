def get_finger_instruction(char: str, lang: str = "en") -> str:
    """ Returns the finger instruction for a given character in the appropriate language. """
    en_mapping = {
        # --- English Left Hand ---
        'a': 'Left Pinky', 'q': 'Top Left Pinky', 'z': 'Bottom Left Pinky',
        's': 'Left Ring', 'w': 'Top Left Ring', 'x': 'Bottom Left Ring',
        'd': 'Left Middle', 'e': 'Top Left Middle', 'c': 'Bottom Left Middle',
        'f': 'Left Index', 'r': 'Top Left Index', 'v': 'Bottom Left Index',
        'g': 'Right of Left Index', 't': 'Top Right of Left Index', 'b': 'Bottom Right of Left Index',
        
        # --- Numbers Row ---
        '1': 'Top Left Pinky (Number Row)', '2': 'Top Left Ring (Number Row)',
        '3': 'Top Left Middle (Number Row)', '4': 'Top Left Index (Number Row)', '5': 'Top Left Index (Number Row)',
        '6': 'Top Right Index (Number Row)', '7': 'Top Right Index (Number Row)', '8': 'Top Right Middle (Number Row)',
        '9': 'Top Right Ring (Number Row)', '0': 'Top Right Pinky (Number Row)',
        
        # --- English Right Hand ---
        'j': 'Right Index', 'u': 'Top Right Index', 'm': 'Bottom Right Index',
        'h': 'Left of Right Index', 'y': 'Top Left of Right Index', 'n': 'Bottom Left of Right Index',
        'k': 'Right Middle', 'i': 'Top Right Middle', ',': 'Bottom Right Middle',
        'l': 'Right Ring', 'o': 'Top Right Ring', '.': 'Bottom Right Ring',
        ';': 'Right Pinky', 'p': 'Top Right Pinky', '/': 'Bottom Right Pinky',
        
        # --- Punctuation and Symbols ---
        ':': 'Right Pinky (with Shift)', '"': 'Right Pinky (with Shift)', "'": 'Right Pinky',
        '?': 'Bottom Right Pinky (with Shift)', '-': 'Top Right Pinky', '_': 'Top Right Pinky (with Shift)',
        '!': 'Top Left Pinky (with Shift)',
        
        # --- Arabic Left Hand ---
        'ش': 'Left Pinky', 'ض': 'Top Left Pinky', 'ذ': 'Far Top Left Pinky',
        'س': 'Left Ring', 'ص': 'Top Left Ring', 'ئ': 'Bottom Left Ring',
        'ي': 'Left Middle', 'ث': 'Top Left Middle', 'ء': 'Bottom Left Middle',
        'ب': 'Left Index', 'ق': 'Top Left Index', 'ؤ': 'Bottom Left Index',
        'ل': 'Right of Left Index', 'ف': 'Top Right of Left Index', 'ر': 'Bottom Right of Left Index',
        
        # --- Arabic Right Hand ---
        'ت': 'Right Index', 'ع': 'Top Right Index', 'ى': 'Bottom Right Index',
        'ا': 'Left of Right Index', 'غ': 'Top Left of Right Index',
        'ن': 'Right Middle', 'ه': 'Top Right Middle', 'ة': 'Bottom Right Middle',
        'م': 'Right Ring', 'خ': 'Top Right Ring', 'و': 'Bottom Right Ring',
        'ك': 'Right Pinky', 'ح': 'Top Right Pinky', 'ز': 'Bottom Right Pinky',
        'ط': 'Right of Right Pinky', 'ج': 'Top Right of Right Pinky', 'ظ': 'Bottom Right of Right Pinky',
        'د': 'Far Right of Right Pinky',
        
        # --- Arabic Diacritics ---
        'َ': 'Top Left Pinky (with Shift)', 'ً': 'Top Left Ring (with Shift)',
        'ُ': 'Top Left Middle (with Shift)', 'ٌ': 'Top Left Index (with Shift)',
        'ِ': 'Left Pinky (with Shift)', 'ٍ': 'Left Ring (with Shift)',
        'ْ': 'Bottom Left Ring (with Shift)', 'ّ': 'Far Top Left Pinky (with Shift)',
        
        # --- Common ---
        ' ': 'Thumb'
    }

    ar_mapping = {
        # --- الإنجليزية واليسرى ---
        'a': 'خنصر اليد اليسرى', 'q': 'خنصر اليد اليسرى أعلى', 'z': 'خنصر اليد اليسرى أسفل',
        's': 'بنصر اليد اليسرى', 'w': 'بنصر اليد اليسرى أعلى', 'x': 'بنصر اليد اليسرى أسفل',
        'd': 'وسطى اليد اليسرى', 'e': 'وسطى اليد اليسرى أعلى', 'c': 'وسطى اليد اليسرى أسفل',
        'f': 'سبابة اليد اليسرى', 'r': 'سبابة اليد اليسرى أعلى', 'v': 'سبابة اليد اليسرى أسفل',
        'g': 'سبابة اليد اليسرى يميناً', 't': 'سبابة اليد اليسرى أعلى يميناً', 'b': 'سبابة اليد اليسرى أسفل يميناً',
        
        # --- صف الأرقام ---
        '1': 'خنصر اليد اليسرى في صف الأرقام', '2': 'بنصر اليد اليسرى في صف الأرقام',
        '3': 'وسطى اليد اليسرى في صف الأرقام', '4': 'سبابة اليد اليسرى في صف الأرقام', '5': 'سبابة اليد اليسرى في صف الأرقام',
        '6': 'سبابة اليد اليمنى في صف الأرقام', '7': 'سبابة اليد اليمنى في صف الأرقام', '8': 'وسطى اليد اليمنى في صف الأرقام',
        '9': 'بنصر اليد اليمنى في صف الأرقام', '0': 'خنصر اليد اليمنى في صف الأرقام',
        
        # --- الإنجليزية واليمنى ---
        'j': 'سبابة اليد اليمنى', 'u': 'سبابة اليد اليمنى أعلى', 'm': 'سبابة اليد اليمنى أسفل',
        'h': 'سبابة اليد اليمنى يساراً', 'y': 'سبابة اليد اليمنى أعلى يساراً', 'n': 'سبابة اليد اليمنى أسفل يساراً',
        'k': 'وسطى اليد اليمنى', 'i': 'وسطى اليد اليمنى أعلى', ',': 'وسطى اليد اليمنى أسفل',
        'l': 'بنصر اليد اليمنى', 'o': 'بنصر اليد اليمنى أعلى', '.': 'بنصر اليد اليمنى أسفل',
        ';': 'خنصر اليد اليمنى', 'p': 'خنصر اليد اليمنى أعلى', '/': 'خنصر اليد اليمنى أسفل',
        
        # --- الرموز ---
        ':': 'خنصر اليد اليمنى مع شفت', '"': 'خنصر اليد اليمنى مع شفت', "'": 'خنصر اليد اليمنى',
        '?': 'خنصر اليد اليمنى أسفل مع شفت', '-': 'خنصر اليد اليمنى أعلى', '_': 'خنصر اليد اليمنى أعلى مع شفت',
        '!': 'خنصر اليد اليسرى مع شفت',
        
        # --- العربية اليد اليسرى ---
        'ش': 'خنصر اليد اليسرى', 'ض': 'خنصر اليد اليسرى أعلى', 'ذ': 'خنصر اليد اليسرى أقصى اليسار أعلى',
        'س': 'بنصر اليد اليسرى', 'ص': 'بنصر اليد اليسرى أعلى', 'ئ': 'بنصر اليد اليسرى أسفل',
        'ي': 'وسطى اليد اليسرى', 'ث': 'وسطى اليد اليسرى أعلى', 'ء': 'وسطى اليد اليسرى أسفل',
        'ب': 'سبابة اليد اليسرى', 'ق': 'سبابة اليد اليسرى أعلى', 'ؤ': 'سبابة اليد اليسرى أسفل',
        'ل': 'سبابة اليد اليسرى يميناً', 'ف': 'سبابة اليد اليسرى أعلى يميناً', 'ر': 'سبابة اليد اليسرى أسفل يميناً',
        
        # --- العربية اليد اليمنى ---
        'ت': 'سبابة اليد اليمنى', 'ع': 'سبابة اليد اليمنى أعلى', 'ى': 'سبابة اليد اليمنى أسفل',
        'ا': 'سبابة اليد اليمنى يساراً', 'غ': 'سبابة اليد اليمنى أعلى يساراً',
        'ن': 'وسطى اليد اليمنى', 'ه': 'وسطى اليد اليمنى أعلى', 'ة': 'وسطى اليد اليمنى أسفل',
        'م': 'بنصر اليد اليمنى', 'خ': 'بنصر اليد اليمنى أعلى', 'و': 'بنصر اليد اليمنى أسفل',
        'ك': 'خنصر اليد اليمنى', 'ح': 'خنصر اليد اليمنى أعلى', 'ز': 'خنصر اليد اليمنى أسفل',
        'ط': 'خنصر اليد اليمنى يميناً', 'ج': 'خنصر اليد اليمنى أعلى يميناً', 'ظ': 'خنصر اليد اليمنى أسفل يميناً',
        'د': 'خنصر اليد اليمنى أقصى اليمين',
        
        # --- التشكيل العربي ---
        'َ': 'خنصر اليد اليسرى أعلى مع شفت (فتحة)', 'ً': 'بنصر اليد اليسرى أعلى مع شفت (تنوين فتح)',
        'ُ': 'وسطى اليد اليسرى أعلى مع شفت (ضمة)', 'ٌ': 'سبابة اليد اليسرى أعلى مع شفت (تنوين ضم)',
        'ِ': 'خنصر اليد اليسرى مع شفت (كسرة)', 'ٍ': 'بنصر اليد اليسرى مع شفت (تنوين كسر)',
        'ْ': 'بنصر اليد اليسرى أسفل مع شفت (سكون)', 'ّ': 'خنصر اليد اليسرى أقصى اليسار مع شفت (شدة)',
        
        # --- الإبهام ---
        ' ': 'الإبهام (مسافة)'
    }

    if lang == "ar":
        return ar_mapping.get(char.lower(), "")
    return en_mapping.get(char.lower(), "")
