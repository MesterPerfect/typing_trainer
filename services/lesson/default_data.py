"""
Contains the default lessons and exams used to initialize the application.
"""

DEFAULT_LESSONS = [
    # ==========================================
    # English Lessons
    # ==========================================
    {
        "id": "en_1", "title": "Home Row Basics (Characters)",
        "text": "asdf jkl; asdf jkl;", "difficulty": 1,
        "language": "en", "lesson_type": "lesson"
    },
    {
        "id": "en_2", "title": "Simple Words",
        "text": "ask dad fall glad", "difficulty": 2,
        "language": "en", "lesson_type": "lesson"
    },
    {
        "id": "en_3", "title": "Short Sentences",
        "text": "he had a glad dad.", "difficulty": 3,
        "language": "en", "lesson_type": "lesson"
    },
    {
        "id": "en_4", "title": "Numbers Row",
        "text": "1 2 3 4 5 6 7 8 9 0", "difficulty": 4,
        "language": "en", "lesson_type": "lesson"
    },
    {
        "id": "en_5", "title": "Punctuation Marks",
        "text": ". , : ; ' \" ? ! - _", "difficulty": 4,
        "language": "en", "lesson_type": "lesson"
    },
    {
        "id": "en_6", "title": "Brackets & Parentheses",
        "text": "( ) [ ] { } < >", "difficulty": 5,
        "language": "en", "lesson_type": "lesson"
    },
    {
        "id": "en_7", "title": "Math Operators",
        "text": "+ - * / = %", "difficulty": 5,
        "language": "en", "lesson_type": "lesson"
    },
    {
        "id": "en_8", "title": "Upper Row Symbols",
        "text": "! @ # $ % ^ & *", "difficulty": 5,
        "language": "en", "lesson_type": "lesson"
    },
    {
        "id": "en_9", "title": "Keyboard Keys Types",
        "text": "shift and alt are modifiers. enter is an action key. tab is a functional key.", "difficulty": 6,
        "language": "en", "lesson_type": "lesson"
    },

    # ==========================================
    # English Exams
    # ==========================================
    {
        "id": "en_test_1", "title": "Exam 1: Characters",
        "text": "a s d f j k l ;", "difficulty": 1,
        "language": "en", "lesson_type": "test"
    },
    {
        "id": "en_test_2", "title": "Exam 2: Words",
        "text": "sad flask dash all", "difficulty": 2,
        "language": "en", "lesson_type": "test"
    },
    {
        "id": "en_test_3", "title": "Exam 3: Sentences",
        "text": "all lads fall.", "difficulty": 3,
        "language": "en", "lesson_type": "test"
    },
    {
        "id": "en_test_4", "title": "Exam 4: Symbols & Numbers",
        "text": "price is $100! (10 * 10 = 100)", "difficulty": 6,
        "language": "en", "lesson_type": "test"
    },

    # ==========================================
    # Arabic Lessons
    # ==========================================
    {
        "id": "ar_1", "title": "أساسيات صف الارتكاز (حروف)",
        "text": "شسيبلاتنمك شسيبلاتنمك", "difficulty": 1,
        "language": "ar", "lesson_type": "lesson"
    },
    {
        "id": "ar_2", "title": "كلمات بسيطة",
        "text": "باب كتاب شمس قمر", "difficulty": 2,
        "language": "ar", "lesson_type": "lesson"
    },
    {
        "id": "ar_3", "title": "جمل قصيرة",
        "text": "هذا باب كبير.", "difficulty": 3,
        "language": "ar", "lesson_type": "lesson"
    },
    {
        "id": "ar_4", "title": "صف الأرقام",
        "text": "1 2 3 4 5 6 7 8 9 0", "difficulty": 4,
        "language": "ar", "lesson_type": "lesson"
    },
    {
        "id": "ar_5", "title": "علامات الترقيم",
        "text": "، ؛ . : ؟ ! - _", "difficulty": 4,
        "language": "ar", "lesson_type": "lesson"
    },
    {
        "id": "ar_6", "title": "الأقواس",
        "text": "( ) [ ] { } < >", "difficulty": 5,
        "language": "ar", "lesson_type": "lesson"
    },
    {
        "id": "ar_7", "title": "العمليات الحسابية",
        "text": "+ - * / = %", "difficulty": 5,
        "language": "ar", "lesson_type": "lesson"
    },
    {
        "id": "ar_8", "title": "التشكيل (الحركات)",
        "text": "بَ بً بُ بٌ بِ بٍ بْ بّ", "difficulty": 6,
        "language": "ar", "lesson_type": "lesson"
    },
    {
        "id": "ar_9", "title": "الرموز العلوية",
        "text": "! @ # $ % ^ & *", "difficulty": 5,
        "language": "ar", "lesson_type": "lesson"
    },
    {
        "id": "ar_10", "title": "أسماء وأنواع المفاتيح",
        "text": "شفت وألت مفاتيح تعديل. انتر مفتاح إجرائي. تاب مفتاح وظيفي.", "difficulty": 6,
        "language": "ar", "lesson_type": "lesson"
    },

    # ==========================================
    # Arabic Exams
    # ==========================================
    {
        "id": "ar_test_1", "title": "الاختبار الأول: الحروف",
        "text": "ش س ي ب ل ا ت ن م ك", "difficulty": 1,
        "language": "ar", "lesson_type": "test"
    },
    {
        "id": "ar_test_2", "title": "الاختبار الثاني: الكلمات",
        "text": "سماء ارض شجر بحر", "difficulty": 2,
        "language": "ar", "lesson_type": "test"
    },
    {
        "id": "ar_test_3", "title": "الاختبار الثالث: الجمل",
        "text": "الشمس تشرق كل يوم.", "difficulty": 3,
        "language": "ar", "lesson_type": "test"
    },
    {
        "id": "ar_test_4", "title": "الاختبار الرابع: التشكيل والأرقام",
        "text": "السِّعْرُ 100$ (مِائَةُ دُولَارٍ)!", "difficulty": 6,
        "language": "ar", "lesson_type": "test"
    }
]
