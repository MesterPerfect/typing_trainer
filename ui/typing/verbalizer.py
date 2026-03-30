def get_pronunciation(char: str, lang: str) -> str:
    """ Maps symbols, punctuation, and diacritics to pronounceable words. """
    
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
        '،': 'Arabic Comma', '؛': 'Arabic Semicolon', '؟': 'Arabic Question Mark',
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
        '+': 'زائد', '=': 'يساوي', '~': 'مدة', '`': 'حرف ذال إنجليزي',
        '،': 'فاصلة', '؛': 'فاصلة منقوطة', '؟': 'علامة استفهام',
        'َ': 'فتحة', 'ً': 'تنوين بالفتح', 'ُ': 'ضمة', 'ٌ': 'تنوين بالضم',
        'ِ': 'كسرة', 'ٍ': 'تنوين بالكسر', 'ْ': 'سكون', 'ّ': 'شدة'
    }
    
    if lang == 'ar':
        return ar_mapping.get(char, char)
    return en_mapping.get(char, char)
