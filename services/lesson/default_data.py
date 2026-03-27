"""
Contains the default lessons and exams used to initialize the application.
"""

DEFAULT_LESSONS = [
    # --- English Lessons ---
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

    # --- English Exams ---
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

    # --- Arabic Lessons ---
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

    # --- Arabic Exams ---
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
    }
]
