from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QLabel,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QPushButton,
    QListWidgetItem,
    QMessageBox,
    QSpinBox,
)
from PySide6.QtCore import Signal, Qt
import logging
import uuid

from services.lesson import LessonService
from models.lesson_model import Lesson

logger = logging.getLogger(__name__)


class LessonEditorView(QWidget):
    return_requested = Signal()

    def __init__(self, tts):
        super().__init__()
        self.tts = tts
        self.lesson_service = LessonService()
        self.lessons = []
        self.current_lesson_id = None

        self._setup_ui()

    def _setup_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # ==========================================
        # Left Panel: Lesson List
        # ==========================================
        left_panel = QVBoxLayout()

        list_label = QLabel(_("Saved Lessons / Exams"))
        list_label.setFont(self._get_font(14, bold=True))
        left_panel.addWidget(list_label)

        self.lesson_list = QListWidget()
        self.lesson_list.setFont(self._get_font(12))
        self.lesson_list.itemClicked.connect(self._on_item_clicked)
        left_panel.addWidget(self.lesson_list)

        self.btn_new = QPushButton(_("Create New Lesson (Ctrl+N)"))
        self.btn_new.setFont(self._get_font(12, bold=True))
        self.btn_new.setMinimumHeight(40)
        self.btn_new.clicked.connect(self.clear_form)
        left_panel.addWidget(self.btn_new)

        main_layout.addLayout(left_panel, 1)  # Takes 1 part of screen

        # ==========================================
        # Right Panel: Editor Form
        # ==========================================
        right_panel = QVBoxLayout()

        form_label = QLabel(_("Lesson Editor"))
        form_label.setFont(self._get_font(18, bold=True))
        form_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_panel.addWidget(form_label)

        # Title
        right_panel.addWidget(QLabel(_("Title:")))
        self.title_input = QLineEdit()
        self.title_input.setFont(self._get_font(12))
        right_panel.addWidget(self.title_input)

        # Language & Type
        row1 = QHBoxLayout()

        lang_label = QLabel(_("Language:"))
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["en", "ar"])
        self.lang_combo.setFont(self._get_font(12))

        type_label = QLabel(_("Type:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["lesson", "test"])
        self.type_combo.setFont(self._get_font(12))

        diff_label = QLabel(_("Difficulty (1-3):"))
        self.diff_spin = QSpinBox()
        self.diff_spin.setRange(1, 3)
        self.diff_spin.setFont(self._get_font(12))

        row1.addWidget(lang_label)
        row1.addWidget(self.lang_combo)
        row1.addWidget(type_label)
        row1.addWidget(self.type_combo)
        row1.addWidget(diff_label)
        row1.addWidget(self.diff_spin)
        right_panel.addLayout(row1)

        # Text Content
        right_panel.addWidget(QLabel(_("Text Content:")))
        self.text_input = QTextEdit()
        self.text_input.setFont(self._get_font(14))
        right_panel.addWidget(self.text_input)

        # Action Buttons
        btn_layout = QHBoxLayout()

        self.btn_save = QPushButton(_("Save (Ctrl+S)"))
        self.btn_save.setFont(self._get_font(12, bold=True))
        self.btn_save.setMinimumHeight(40)
        self.btn_save.clicked.connect(self.save_lesson)

        self.btn_delete = QPushButton(_("Delete"))
        self.btn_delete.setFont(self._get_font(12, bold=True))
        self.btn_delete.setMinimumHeight(40)
        self.btn_delete.clicked.connect(self.delete_lesson)

        self.btn_return = QPushButton(_("Return (Esc)"))
        self.btn_return.setFont(self._get_font(12, bold=True))
        self.btn_return.setMinimumHeight(40)
        self.btn_return.clicked.connect(self.return_requested.emit)

        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_return)

        right_panel.addLayout(btn_layout)

        main_layout.addLayout(right_panel, 2)  # Takes 2 parts of screen

        self.setLayout(main_layout)

    def _get_font(self, size, bold=False):
        font = self.font()
        font.setPointSize(size)
        font.setBold(bold)
        return font

    def load_data(self):
        """Fetch all lessons and populate the list."""
        self.lesson_list.clear()
        self.lessons = self.lesson_service.load_all_lessons()

        for lesson in self.lessons:
            item = QListWidgetItem(f"[{lesson.language.upper()}] {lesson.title}")
            item.setData(Qt.ItemDataRole.UserRole, lesson)
            self.lesson_list.addItem(item)

        self.clear_form()

    def _on_item_clicked(self, item):
        """Populate the form when a lesson is selected from the list."""
        lesson = item.data(Qt.ItemDataRole.UserRole)
        self.current_lesson_id = lesson.id

        self.title_input.setText(lesson.title)
        self.text_input.setPlainText(lesson.text)
        self.diff_spin.setValue(lesson.difficulty)

        self.lang_combo.setCurrentText(lesson.language)
        self.type_combo.setCurrentText(lesson.lesson_type)

        self.tts.speak(f"Loaded {lesson.title}")

    def clear_form(self):
        """Reset the form to create a new lesson."""
        self.current_lesson_id = None
        self.title_input.clear()
        self.text_input.clear()
        self.diff_spin.setValue(1)
        self.lang_combo.setCurrentIndex(0)
        self.type_combo.setCurrentIndex(0)

        self.title_input.setFocus()
        self.tts.speak("New lesson form ready")

    def save_lesson(self):
        """Save the current form data as a new lesson or update existing."""
        title = self.title_input.text().strip()
        text = self.text_input.toPlainText().strip()

        # Enhanced validation
        if not title or not text:
            self.tts.speak("Title and text must contain at least 2 characters")
            return

        # Create or update lesson object
        lesson_id = (
            self.current_lesson_id
            if self.current_lesson_id
            else f"custom_{uuid.uuid4().hex[:8]}"
        )

        new_lesson = Lesson(
            id=lesson_id,
            title=title,
            text=text,
            difficulty=self.diff_spin.value(),
            language=self.lang_combo.currentText(),
            lesson_type=self.type_combo.currentText()
        )

        # Update the list in memory
        if self.current_lesson_id:
            for i, l in enumerate(self.lessons):
                if l.id == self.current_lesson_id:
                    self.lessons[i] = new_lesson
                    break
        else:
            self.lessons.append(new_lesson)

        # Save to disk
        success = self.lesson_service.save_all_lessons(self.lessons)

        if success:
            self.tts.speak("Lesson saved successfully")
            self.load_data()  # Refresh the list
        else:
            self.tts.speak("Failed to save lesson")

    def delete_lesson(self):
        """Delete the currently selected lesson and clear the form."""
        if not self.current_lesson_id:
            self.tts.speak("No lesson selected to delete")
            return

        self.lessons = [l for l in self.lessons if l.id != self.current_lesson_id]

        success = self.lesson_service.save_all_lessons(self.lessons)
        if success:
            self.tts.speak("Lesson deleted")
            self.load_data()
            self.clear_form() # Reset the form to prevent ghost saving
        else:
            self.tts.speak("Failed to delete lesson")

    def keyPressEvent(self, event):
        """Handle shortcuts."""
        if event.key() == Qt.Key.Key_Escape:
            self.return_requested.emit()
            return

        modifiers = event.modifiers()
        if modifiers == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_S:
                self.save_lesson()
                return
            elif event.key() == Qt.Key.Key_N:
                self.clear_form()
                return

        super().keyPressEvent(event)
