def get_finger_instruction(char: str, lang: str = "en") -> str:
    """ Returns the finger instruction for a given character in the appropriate language. """
    en_mapping = {
        # --- English Left Hand ---
        'a': 'Left Pinky', 'q': 'Top Left Pinky', 'z': 'Bottom Left Pinky',
        's': 'Left Ring', 'w': 'Top Left Ring', 'x': 'Bottom Left Ring',
        'd': 'Left Middle', 'e': 'Top Left Middle', 'c': 'Bottom Left Middle',
        'f': 'Left Index', 'r': 'Top Left Index', 'v': 'Bottom Left Index',
        'g': 'Right of Left Index', 't': 'Top Right of Left Index', 'b': 'Bottom Right of Left Index',
        
        # --- Uppercase English Left Hand (with Shift) ---
        'A': 'Left Pinky (with Right Shift)', 'Q': 'Top Left Pinky (with Right Shift)', 'Z': 'Bottom Left Pinky (with Right Shift)',
        'S': 'Left Ring (with Right Shift)', 'W': 'Top Left Ring (with Right Shift)', 'X': 'Bottom Left Ring (with Right Shift)',
        'D': 'Left Middle (with Right Shift)', 'E': 'Top Left Middle (with Right Shift)', 'C': 'Bottom Left Middle (with Right Shift)',
        'F': 'Left Index (with Right Shift)', 'R': 'Top Left Index (with Right Shift)', 'V': 'Bottom Left Index (with Right Shift)',
        'G': 'Right of Left Index (with Right Shift)', 'T': 'Top Right of Left Index (with Right Shift)', 'B': 'Bottom Right of Left Index (with Right Shift)',

        # --- Numbers Row ---
        '1': 'Top Left Pinky (Number Row)', '2': 'Top Left Ring (Number Row)',
        '3': 'Top Left Middle (Number Row)', '4': 'Top Left Index (Number Row)', '5': 'Top Left Index (Number Row)',
        '6': 'Top Right Index (Number Row)', '7': 'Top Right Index (Number Row)', '8': 'Top Right Middle (Number Row)',
        '9': 'Top Right Ring (Number Row)', '0': 'Top Right Pinky (Number Row)',
        '-': 'Top Right Pinky', '=': 'Far Top Right Pinky', '`': 'Far Top Left Pinky',
        
        # --- English Right Hand ---
        'j': 'Right Index', 'u': 'Top Right Index', 'm': 'Bottom Right Index',
        'h': 'Left of Right Index', 'y': 'Top Left of Right Index', 'n': 'Bottom Left of Right Index',
        'k': 'Right Middle', 'i': 'Top Right Middle', ',': 'Bottom Right Middle',
        'l': 'Right Ring', 'o': 'Top Right Ring', '.': 'Bottom Right Ring',
        ';': 'Right Pinky', 'p': 'Top Right Pinky', '/': 'Bottom Right Pinky',
        '[': 'Top Right Pinky (reach)', ']': 'Far Top Right Pinky', "'": 'Right Pinky',

        # --- Uppercase English Right Hand (with Shift) ---
        'J': 'Right Index (with Left Shift)', 'U': 'Top Right Index (with Left Shift)', 'M': 'Bottom Right Index (with Left Shift)',
        'H': 'Left of Right Index (with Left Shift)', 'Y': 'Top Left of Right Index (with Left Shift)', 'N': 'Bottom Left of Right Index (with Left Shift)',
        'K': 'Right Middle (with Left Shift)', 'I': 'Top Right Middle (with Left Shift)',
        'L': 'Right Ring (with Left Shift)', 'O': 'Top Right Ring (with Left Shift)',
        'P': 'Top Right Pinky (with Left Shift)',
        
        # --- Punctuation and Symbols ---
        ':': 'Right Pinky (with Shift)', '"': 'Right Pinky (with Shift)',
        '?': 'Bottom Right Pinky (with Shift)', '_': 'Top Right Pinky (with Shift)',
        '+': 'Far Top Right Pinky (with Shift)', '~': 'Far Top Left Pinky (with Shift)',
        '!': 'Top Left Pinky (with Shift)', '@': 'Top Left Ring (with Shift)',
        '#': 'Top Left Middle (with Shift)', '$': 'Top Left Index (with Shift)',
        '%': 'Top Left Index (with Shift)', '^': 'Top Right Index (with Shift)',
        '&': 'Top Right Index (with Shift)', '*': 'Top Right Middle (with Shift)',
        '(': 'Top Right Ring (with Shift)', ')': 'Top Right Pinky (with Shift)',
        '{': 'Top Right Pinky (with Shift)', '}': 'Far Top Right Pinky (with Shift)',
        '<': 'Bottom Right Middle (with Shift)', '>': 'Bottom Right Ring (with Shift)',
        '|': 'Far Right Pinky (with Shift)',
        
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

        # --- Arabic Shifted Letters & Ligatures ---
        'أ': 'Left of Right Index (with Shift)',       # Shift + H (ا)
        'إ': 'Top Left of Right Index (with Shift)',   # Shift + Y (غ)
        'آ': 'Bottom Left of Right Index (with Shift)',# Shift + N (ى)
        'لأ': 'Right of Left Index (with Shift)',      # Shift + G (ل)
        'لإ': 'Top Right of Left Index (with Shift)',  # Shift + T (ف)
        'لآ': 'Bottom Right of Left Index (with Shift)',# Shift + B (لا)
        '،': 'Right Middle (with Shift)',              # Shift + K (ن)
        '؛': 'Top Right Pinky (with Shift)',           # Shift + P (ح)
        '؟': 'Bottom Right Pinky (with Shift)',        # Shift + / (ظ)
        'ـ': 'Right Index (with Shift)',               # Shift + J (ت)
        '×': 'Top Right Ring (with Shift)',            # Shift + O (خ)
        '÷': 'Top Right Middle (with Shift)',          # Shift + I (ه)
        
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
        
        # --- الإنجليزية الكبيرة (مع شفت) ---
        'A': 'خنصر اليد اليسرى مع شفت', 'Q': 'خنصر اليد اليسرى أعلى مع شفت', 'Z': 'خنصر اليد اليسرى أسفل مع شفت',
        'S': 'بنصر اليد اليسرى مع شفت', 'W': 'بنصر اليد اليسرى أعلى مع شفت', 'X': 'بنصر اليد اليسرى أسفل مع شفت',
        'D': 'وسطى اليد اليسرى مع شفت', 'E': 'وسطى اليد اليسرى أعلى مع شفت', 'C': 'وسطى اليد اليسرى أسفل مع شفت',
        'F': 'سبابة اليد اليسرى مع شفت', 'R': 'سبابة اليد اليسرى أعلى مع شفت', 'V': 'سبابة اليد اليسرى أسفل مع شفت',
        'G': 'سبابة اليد اليسرى يميناً مع شفت', 'T': 'سبابة اليد اليسرى أعلى يميناً مع شفت', 'B': 'سبابة اليد اليسرى أسفل يميناً مع شفت',

        # --- صف الأرقام ---
        '1': 'خنصر اليد اليسرى في صف الأرقام', '2': 'بنصر اليد اليسرى في صف الأرقام',
        '3': 'وسطى اليد اليسرى في صف الأرقام', '4': 'سبابة اليد اليسرى في صف الأرقام', '5': 'سبابة اليد اليسرى في صف الأرقام',
        '6': 'سبابة اليد اليمنى في صف الأرقام', '7': 'سبابة اليد اليمنى في صف الأرقام', '8': 'وسطى اليد اليمنى في صف الأرقام',
        '9': 'بنصر اليد اليمنى في صف الأرقام', '0': 'خنصر اليد اليمنى في صف الأرقام',
        '-': 'خنصر اليد اليمنى في صف الأرقام', '=': 'خنصر اليد اليمنى أقصى اليمين', '`': 'خنصر اليد اليسرى أقصى اليسار أعلى',
        
        # --- الإنجليزية واليمنى ---
        'j': 'سبابة اليد اليمنى', 'u': 'سبابة اليد اليمنى أعلى', 'm': 'سبابة اليد اليمنى أسفل',
        'h': 'سبابة اليد اليمنى يساراً', 'y': 'سبابة اليد اليمنى أعلى يساراً', 'n': 'سبابة اليد اليمنى أسفل يساراً',
        'k': 'وسطى اليد اليمنى', 'i': 'وسطى اليد اليمنى أعلى', ',': 'وسطى اليد اليمنى أسفل',
        'l': 'بنصر اليد اليمنى', 'o': 'بنصر اليد اليمنى أعلى', '.': 'بنصر اليد اليمنى أسفل',
        ';': 'خنصر اليد اليمنى', 'p': 'خنصر اليد اليمنى أعلى', '/': 'خنصر اليد اليمنى أسفل',
        '[': 'خنصر اليد اليمنى أعلى يميناً', ']': 'خنصر اليد اليمنى أقصى اليمين أعلى', "'": 'خنصر اليد اليمنى',

        # --- الإنجليزية الكبيرة اليمنى ---
        'J': 'سبابة اليد اليمنى مع شفت', 'U': 'سبابة اليد اليمنى أعلى مع شفت', 'M': 'سبابة اليد اليمنى أسفل مع شفت',
        'H': 'سبابة اليد اليمنى يساراً مع شفت', 'Y': 'سبابة اليد اليمنى أعلى يساراً مع شفت', 'N': 'سبابة اليد اليمنى أسفل يساراً مع شفت',
        'K': 'وسطى اليد اليمنى مع شفت', 'I': 'وسطى اليد اليمنى أعلى مع شفت',
        'L': 'بنصر اليد اليمنى مع شفت', 'O': 'بنصر اليد اليمنى أعلى مع شفت',
        'P': 'خنصر اليد اليمنى أعلى مع شفت',
        
        # --- الرموز ---
        ':': 'خنصر اليد اليمنى مع شفت', '"': 'خنصر اليد اليمنى مع شفت',
        '?': 'خنصر اليد اليمنى أسفل مع شفت', '_': 'خنصر اليد اليمنى أعلى مع شفت',
        '+': 'خنصر اليد اليمنى أقصى اليمين مع شفت', '~': 'خنصر اليد اليسرى أقصى اليسار مع شفت',
        '!': 'خنصر اليد اليسرى مع شفت', '@': 'بنصر اليد اليسرى مع شفت',
        '#': 'وسطى اليد اليسرى مع شفت', '$': 'سبابة اليد اليسرى مع شفت',
        '%': 'سبابة اليد اليسرى مع شفت', '^': 'سبابة اليد اليمنى مع شفت',
        '&': 'سبابة اليد اليمنى مع شفت', '*': 'وسطى اليد اليمنى مع شفت',
        '(': 'بنصر اليد اليمنى مع شفت', ')': 'خنصر اليد اليمنى مع شفت',
        '{': 'خنصر اليد اليمنى أعلى مع شفت', '}': 'خنصر اليد اليمنى أقصى اليمين مع شفت',
        '<': 'وسطى اليد اليمنى أسفل مع شفت', '>': 'بنصر اليد اليمنى أسفل مع شفت',
        '|': 'خنصر اليد اليمنى أقصى اليمين مع شفت',
        
        # --- العربية اليد اليسرى ---
        'ش': 'خنصر اليد اليسرى', 'ض': 'خنصر اليد اليسرى أعلى', 'ذ': 'خنصر اليد اليسرى أقصى اليسار أعلى',
        'س': 'بنصر اليد اليسرى', 'ص': 'بنصر اليد اليسرى أعلى', 'ئ': 'خنصر اليد اليسرى أسفل',
        'ي': 'وسطى اليد اليسرى', 'ث': 'وسطى اليد اليسرى أعلى', 'ء': 'بنصر اليد اليسرى أسفل',
        'ب': 'سبابة اليد اليسرى', 'ق': 'سبابة اليد اليسرى أعلى', 'ؤ': 'وسطى اليد اليسرى أسفل',
        'ل': 'سبابة اليد اليسرى يميناً', 'ف': 'سبابة اليد اليسرى أعلى يميناً', 'ر': 'سبابة اليد اليسرى أسفل يميناً',
        
        # --- العربية اليد اليمنى ---
        'ت': 'سبابة اليد اليمنى', 'ع': 'سبابة اليد اليمنى أعلى', 'ى': 'سبابة اليد اليمنى أسفل',
        'ا': 'سبابة اليد اليمنى يساراً', 'غ': 'سبابة اليد اليمنى أعلى يساراً',
        'ن': 'وسطى اليد اليمنى', 'ه': 'وسطى اليد اليمنى أعلى', 'ة': 'سبابة اليد اليمنى أسفل',
        'م': 'بنصر اليد اليمنى', 'خ': 'بنصر اليد اليمنى أعلى', 'و': 'بنصر اليد اليمنى أسفل',
        'ك': 'خنصر اليد اليمنى', 'ح': 'خنصر اليد اليمنى أعلى', 'ز': 'بنصر اليد اليمنى أسفل',
        'ط': 'خنصر اليد اليمنى يميناً', 'ج': 'خنصر اليد اليمنى أعلى يميناً', 'ظ': 'خنصر اليد اليمنى أسفل يميناً',
        'د': 'خنصر اليد اليمنى أقصى اليمين',

        # --- الحروف العربية المركبة والمهموزة مع شفت ---
        'أ': 'سبابة اليد اليمنى يساراً مع شفت (ألف همزة أعلى)',
        'إ': 'سبابة اليد اليمنى أعلى يساراً مع شفت (ألف همزة أسفل)',
        'آ': 'سبابة اليد اليمنى أسفل يساراً مع شفت (ألف ممدودة)',
        'لأ': 'سبابة اليد اليسرى يميناً مع شفت (لام ألف همزة أعلى)',
        'لإ': 'سبابة اليد اليسرى أعلى يميناً مع شفت (لام ألف همزة أسفل)',
        'لآ': 'سبابة اليد اليسرى أسفل يميناً مع شفت (لام ألف ممدودة)',
        '،': 'وسطى اليد اليمنى مع شفت (فاصلة عربية)',
        '؛': 'خنصر اليد اليمنى أعلى مع شفت (فاصلة منقوطة عربية)',
        '؟': 'خنصر اليد اليمنى أسفل مع شفت (علامة استفهام عربية)',
        'ـ': 'سبابة اليد اليمنى مع شفت (تطويل/كشيدة)',
        '×': 'بنصر اليد اليمنى أعلى مع شفت (علامة ضرب)',
        '÷': 'وسطى اليد اليمنى أعلى مع شفت (علامة قسمة)',
        
        # --- التشكيل العربي ---
        'َ': 'خنصر اليد اليسرى أعلى مع شفت (فتحة)', 'ً': 'بنصر اليد اليسرى أعلى مع شفت (تنوين فتح)',
        'ُ': 'وسطى اليد اليسرى أعلى مع شفت (ضمة)', 'ٌ': 'سبابة اليد اليسرى أعلى مع شفت (تنوين ضم)',
        'ِ': 'خنصر اليد اليسرى مع شفت (كسرة)', 'ٍ': 'بنصر اليد اليسرى مع شفت (تنوين كسر)',
        'ْ': 'بنصر اليد اليسرى أسفل مع شفت (سكون)', 'ّ': 'خنصر اليد اليسرى أقصى اليسار مع شفت (شدة)',
        
        # --- الإبهام ---
        ' ': 'الإبهام (مسافة)'
    }

    mapping = ar_mapping if lang == "ar" else en_mapping
    # Try exact character first, then lowercase fallback
    if char in mapping:
        return mapping[char]
    return mapping.get(char.lower(), "")
