import sys
import os
import time
import tempfile
from pathlib import Path

# Add project root to sys.path
base_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(base_dir))

# Mock gettext _
import builtins
builtins._ = lambda s: s

from utils.helpers import get_finger_instruction
from ui.typing.verbalizer import get_pronunciation
from core.statistics import TypingStatistics
from models.result_model import LessonResult
from services.result_service import ResultService
from services.lesson import LessonService
from models.lesson_model import Lesson
from services.settings_service import SettingsService

def test_helpers_and_verbalizer():
    print("Testing helpers & verbalizer...")
    extended_chars = ["أ", "إ", "آ", "لأ", "لإ", "لآ", "،", "؛", "؟", "ـ", "×", "÷"]
    for ch in extended_chars:
        instr_ar = get_finger_instruction(ch, "ar")
        instr_en = get_finger_instruction(ch, "en")
        pron_ar = get_pronunciation(ch, "ar")
        pron_en = get_pronunciation(ch, "en")
        assert len(instr_ar) > 0, f"Arabic instruction missing for {ch}"
        assert len(instr_en) > 0, f"English instruction missing for {ch}"
        assert len(pron_ar) > 0, f"Arabic pronunciation missing for {ch}"
        assert len(pron_en) > 0, f"English pronunciation missing for {ch}"
    print("✓ Helpers & verbalizer passed!")

def test_statistics_engine():
    print("Testing statistics engine (CPM, smoothing, pause)...")
    stats = TypingStatistics()
    stats.start()
    
    # Early spike smoothing (< 2.0s)
    stats.record_keystroke(True)
    assert stats.get_wpm() == 0, "WPM should be 0 before 2 seconds elapsed"
    assert stats.get_cpm() == 0, "CPM should be 0 before 2 seconds elapsed"

    # Simulate elapsed time
    stats.start_time = time.time() - 60.0 # 1 minute ago
    for _ in range(29): # total 30 correct keystrokes
        stats.record_keystroke(True)

    cpm = stats.get_cpm()
    wpm = stats.get_wpm()
    assert cpm == 30, f"Expected 30 CPM, got {cpm}"
    assert wpm == 6, f"Expected 6 WPM, got {wpm}"

    # Test Pause / Resume
    stats.pause()
    assert stats.is_paused is True
    time.sleep(0.05)
    stats.resume()
    assert stats.is_paused is False
    assert stats.total_paused_duration > 0
    print("✓ Statistics engine passed!")

def test_result_service():
    print("Testing result service (Lifetime summary, CSV, Clear)...")
    with tempfile.TemporaryDirectory() as tmpdir:
        res_file = Path(tmpdir) / "test_results.json"
        service = ResultService(res_file)

        res1 = LessonResult(lesson_id="1", wpm=60, cpm=300, accuracy=95.0, errors=2, time_elapsed=30.0)
        res2 = LessonResult(lesson_id="2", wpm=80, cpm=400, accuracy=99.0, errors=1, time_elapsed=45.0)
        service.save_result(res1)
        service.save_result(res2)

        summary = service.get_lifetime_summary()
        assert summary["total_sessions"] == 2
        assert summary["peak_wpm"] == 80
        assert summary["peak_cpm"] == 400
        assert summary["avg_wpm"] == 70.0
        assert summary["avg_accuracy"] == 97.0
        assert summary["total_time_seconds"] == 75.0

        csv_file = Path(tmpdir) / "export.csv"
        success = service.export_to_csv(csv_file, {"1": "Lesson One", "2": "Lesson Two"})
        assert success is True
        assert csv_file.exists()
        with open(csv_file, "r", encoding="utf-8-sig") as f:
            csv_content = f.read()
            assert "Lesson One" in csv_content
            assert "400" in csv_content

        service.clear_all_results()
        assert len(service.cached_results) == 0
        summary_cleared = service.get_lifetime_summary()
        assert summary_cleared["total_sessions"] == 0
    print("✓ Result service passed!")

def test_lesson_package_export_import():
    print("Testing lesson package import/export...")
    with tempfile.TemporaryDirectory() as tmpdir:
        lesson_file = Path(tmpdir) / "lessons.json"
        service = LessonService(lesson_file)
        
        pkg_file = Path(tmpdir) / "pkg.json"
        lessons = [
            Lesson(id="custom_1", title="Arabic Practice", text="مرحبا بكم", difficulty=1, language="ar"),
            Lesson(id="custom_2", title="English Practice", text="Hello world", difficulty=2, language="en")
        ]
        
        ok = service.export_package(pkg_file, lessons)
        assert ok is True
        assert pkg_file.exists()

        imported = service.import_package(pkg_file)
        assert len(imported) == 2
        assert imported[0].title == "Arabic Practice"
        assert imported[1].title == "English Practice"
    print("✓ Lesson package export/import passed!")

def test_settings_service():
    print("Testing settings service auto-repeat...")
    with tempfile.TemporaryDirectory() as tmpdir:
        settings_file = Path(tmpdir) / "settings.json"
        service = SettingsService(settings_file)
        assert service.get("auto_repeat_prompt") is False
        assert service.get("auto_repeat_interval") == 4
        service.set("auto_repeat_prompt", True)
        service.set("auto_repeat_interval", 6)
        assert service.get("auto_repeat_prompt") is True
        assert service.get("auto_repeat_interval") == 6
    print("✓ Settings service passed!")

if __name__ == "__main__":
    test_helpers_and_verbalizer()
    test_statistics_engine()
    test_result_service()
    test_lesson_package_export_import()
    test_settings_service()
    print("\n🎉 ALL TESTS PASSED SUCCESSFULLY!")
