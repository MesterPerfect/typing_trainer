def get_pronunciation(char: str, lang: str) -> str:
    """ Maps symbols, punctuation, letters, and diacritics to pronounceable words. """
    
    # English Verbalization Map
    en_mapping = {
        ' ': 'Space', '\n': 'Enter',
        '.': 'Dot', ',': 'Comma', ';': 'Semicolon', ':': 'Colon',
        "'": 'Apostrophe', '"': 'Quote', '?': 'Question Mark', '!': 'Exclamation Mark',
        '-': 'Dash', '_': 'Underscore', 
        '(': 'Left Parenthesis', ')': 'Right Parenthesis',
        '[': 'Left Bracket', ']': 'Right Bracket', 
        '{': 'Left Brace', '}': 'Right Brace',
        '<': 'Less Than', '>': 'Greater Than', 
        '/': 'Slash', '\\': 'Backslash', '|': 'Pipe',
        '@': 'At sign', '#': 'Hash', '$': 'Dollar sign', '%': 'Percent',
        '^': 'Caret', '&': 'Ampersand', '*': 'Asterisk', 
        '+': 'Plus', '=': 'Equals', '~': 'Tilde', '`': 'Backtick',
        '×': 'Multiplication Sign', '÷': 'Division Sign',
        '«': 'Left Guillemet', '»': 'Right Guillemet',
        '،': 'Arabic Comma', '؛': 'Arabic Semicolon', '؟': 'Arabic Question Mark',
        'ـ': 'Kashida',
        'أ': 'Alef with Hamza', 'إ': 'Alef with Hamza Below', 'آ': 'Alef with Madda',
        'ء': 'Hamza', 'ئ': 'Hamza on Nabrah', 'ؤ': 'Hamza on Waw',
        'ى': 'Alef Maksura', 'ة': 'Taa Marbuta',
        'لأ': 'Lam Alef with Hamza', 'لإ': 'Lam Alef with Hamza Below', 'لآ': 'Lam Alef with Madda',
        'َ': 'Fatha', 'ً': 'Tanween Fath', 'ُ': 'Damma', 'ٌ': 'Tanween Damm',
        'ِ': 'Kasra', 'ٍ': 'Tanween Kasr', 'ْ': 'Sukun', 'ّ': 'Shadda'
    }
    
    # Arabic Verbalization Map
    ar_mapping = {
        ' ': 'مسافة', '\n': 'سطر جديد',
        '.': 'نقطة', ',': 'فاصلة إنجليزية', ';': 'فاصلة منقوطة إنجليزية', ':': 'نقطتان',
        "'": 'علامة تنصيص مفردة', '"': 'علامة تنصيص مزدوجة', '?': 'علامة استفهام إنجليزية', '!': 'علامة تعجب',
        '-': 'شرطة', '_': 'شرطة سفلية', 
        '(': 'قوس أيسر', ')': 'قوس أيمن',
        '[': 'قوس مربع أيسر', ']': 'قوس مربع أيمن', 
        '{': 'قوس معقوف أيسر', '}': 'قوس معقوف أيمن',
        '<': 'أصغر من', '>': 'أكبر من', 
        '/': 'شرطة مائلة', '\\': 'شرطة مائلة عكسية', '|': 'خط عمودي',
        '@': 'علامة آت', '#': 'شباك', '$': 'علامة الدولار', '%': 'علامة بالمائة',
        '^': 'علامة أُس', '&': 'علامة و', '*': 'نجمة', 
        '+': 'زائد', '=': 'يساوي', '~': 'مدة', '`': 'ذال إنجليزي',
        '×': 'علامة ضرب', '÷': 'علامة قسمة',
        '«': 'قوس تنصيص أيمن', '»': 'قوس تنصيص أيسر',
        '،': 'فاصلة عربية', '؛': 'فاصلة منقوطة عربية', '؟': 'علامة استفهام عربية',
        'ـ': 'تطويل',
        'أ': 'ألف همزة أعلى', 'إ': 'ألف همزة أسفل', 'آ': 'ألف ممدودة',
        'ء': 'همزة على السطر', 'ئ': 'همزة على نبرة', 'ؤ': 'همزة على واو',
        'ى': 'ألف لينة', 'ة': 'تاء مربوطة',
        'لأ': 'لام ألف همزة أعلى', 'لإ': 'لام ألف همزة أسفل', 'لآ': 'لام ألف ممدودة',
        'َ': 'فتحة', 'ً': 'تنوين بالفتح', 'ُ': 'ضمة', 'ٌ': 'تنوين بالضم',
        'ِ': 'كسرة', 'ٍ': 'تنوين بالكسر', 'ْ': 'سكون', 'ّ': 'شدة'
    }
    
    mapping = ar_mapping if str(lang).lower().startswith('ar') else en_mapping
    return mapping.get(char, char)
