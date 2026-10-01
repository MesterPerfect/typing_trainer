import sys
import os
import time

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

import core.constants as const
from utils.i18n import setup_translations
from app.theme import setup_theme
from ui.main_window import MainWindow
from ui.components.shortcuts_dialog import ShortcutsDialog
from models.lesson_model import Lesson
from models.result_model import LessonResult
from core.modes import ExplorerMode

def capture():
    # 1. Initialize Application
    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName("Typing Trainer")
    app.setOrganizationName("MesterPerfect")
    
    # Set Arabic / RTL by default for screenshots
    setup_translations("ar")
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    
    # Apply Dark Theme
    setup_theme(app, "dark_theme")

    out_dir = os.path.join(const.BASE_DIR, "docs", "screenshots")
    os.makedirs(out_dir, exist_ok=True)

    # 2. Initialize Main Window
    class DummyArgs:
        lang = "ar"
        no_tts = True
        log_level = "INFO"
        no_log_time = True

    window = MainWindow(args=DummyArgs())
    window.resize(1020, 720)
    window.show()

    def grab_and_save(filename):
        app.processEvents()
        time.sleep(0.15)
        app.processEvents()
        pixmap = window.grab()
        file_path = os.path.join(out_dir, filename)
        pixmap.save(file_path, "PNG")
        print(f"Captured: {filename}")

    # 1. Main Menu / Lesson View
    window.show_lessons()
    grab_and_save("01_main_menu.png")

    # 2. Typing Session View
    sample_lesson = Lesson(
        id="sample_ar_1",
        title="تدريب صف الارتكاز (ك، م، ن، ت)",
        text="كمن نمت تمكن كنت كمن نمت تمكن كنت",
        difficulty=1,
        language="ar",
        lesson_type="lesson"
    )
    window.start_lesson(sample_lesson)
    try:
        window.typing_view.input_field.setText("كمن ")
    except Exception:
        pass
    grab_and_save("02_typing_session.png")

    # 3. Results View
    try:
        dummy_result = LessonResult(
            lesson_id="sample_ar_1",
            wpm=68,
            accuracy=98.5,
            errors=2,
            time_elapsed=45.0,
            cpm=340
        )
        window.result_service.save_result(dummy_result)
    except Exception as e:
        print(f"Note on dummy result: {e}")

    window.show_results()
    grab_and_save("03_results.png")

    # 4. Explorer Mode View
    window.start_explorer(ExplorerMode.ARABIC)
    try:
        window.explorer_view.label.setText(
            "مستكشف الحروف العربية (Arabic Letters Explorer)\n\n"
            "الحرف الحالي: ك (Kaf)\n"
            "تموضع الإصبع: السبابة اليمنى (Right Index Finger)\n"
            "الصف: صف الارتكاز (Home Row)\n\n"
            "للخروج: اضغط على مفتاح الهروب (Escape) ثلاث مرات متتالية"
        )
    except Exception:
        pass
    grab_and_save("04_explorer.png")

    # 5. Lesson Editor View
    window.show_editor()
    try:
        if window.editor_view.lesson_list.count() > 0:
            item = window.editor_view.lesson_list.item(0)
            window.editor_view.lesson_list.setCurrentItem(item)
            window.editor_view._on_item_clicked(item)
    except Exception as e:
        print(f"Note on editor selection: {e}")
    grab_and_save("05_editor.png")

    # 6. Settings View (Typing Page)
    window.show_settings()
    try:
        # Select Audio or Typing settings page
        window.settings_view.tree_widget.setCurrentItem(window.settings_view.tree_widget.topLevelItem(1))
        window.settings_view._on_category_changed(window.settings_view.tree_widget.topLevelItem(1), None)
    except Exception as e:
        print(f"Note on settings page selection: {e}")
    grab_and_save("06_settings.png")

    # 7. Shortcuts Dialog
    try:
        dialog = ShortcutsDialog(window, window.tts)
        dialog.resize(780, 580)
        dialog.show()
        app.processEvents()
        time.sleep(0.15)
        app.processEvents()
        dialog_pixmap = dialog.grab()
        dialog_path = os.path.join(out_dir, "07_shortcuts.png")
        dialog_pixmap.save(dialog_path, "PNG")
        print("Captured: 07_shortcuts.png")
        dialog.close()
    except Exception as e:
        print(f"Error capturing shortcuts dialog: {e}")

    print("All screenshots generated successfully!")
    window.close()

if __name__ == "__main__":
    capture()
