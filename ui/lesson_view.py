from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QLabel,
    QPushButton,
    QTabWidget,
    QListWidgetItem,
)
from PySide6.QtCore import Signal, Qt
import logging

from services.lesson import LessonService
from models.lesson_model import Lesson
from core.modes import ExplorerMode

logger = logging.getLogger(__name__)


class LessonView(QWidget):
    lesson_selected = Signal(Lesson)
    explorer_requested = Signal(ExplorerMode)
    settings_requested = Signal()
    results_requested = Signal()
    editor_requested = Signal()

    def __init__(self, tts):
        super().__init__()
        self.tts = tts
        self.loader = LessonService()
        self.lessons = []

        self._setup_ui()
        self.load_lessons()

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.title_label = QLabel(_("Select a Category"))
        font = self.title_label.font()
        font.setPointSize(18)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)

        # ==========================================
        # Setup Tabs
        # ==========================================
        self.tabs = QTabWidget()
        tab_font = self.tabs.font()
        tab_font.setPointSize(14)
        self.tabs.setFont(tab_font)

        self.ar_list = QListWidget()
        self.en_list = QListWidget()
        self.test_list = QListWidget()
        self.explorer_list = QListWidget()

        self.tabs.addTab(self.ar_list, _("Arabic Lessons"))
        self.tabs.addTab(self.en_list, _("English Lessons"))
        self.tabs.addTab(self.test_list, _("Exams"))
        self.tabs.addTab(self.explorer_list, _("Explorer Modes"))

        layout.addWidget(self.tabs)

        # ==========================================
        # Buttons
        # ==========================================
        self.start_button = QPushButton(_("Start Selected (Enter)"))
        self.start_button.setMinimumHeight(40)
        self.start_button.clicked.connect(self._on_start_clicked)
        layout.addWidget(self.start_button)

        self.results_button = QPushButton(_("View Results (F4)"))
        self.results_button.setMinimumHeight(40)
        self.results_button.clicked.connect(self.results_requested.emit)
        layout.addWidget(self.results_button)

        self.settings_button = QPushButton(_("Settings (F3)"))
        self.settings_button.setMinimumHeight(40)
        self.settings_button.clicked.connect(self.settings_requested.emit)
        layout.addWidget(self.settings_button)

        self.editor_button = QPushButton(_("Lesson Editor (F9)"))
        self.editor_button.setMinimumHeight(40)
        self.editor_button.clicked.connect(self.editor_requested.emit)
        layout.addWidget(self.editor_button)

        self.setLayout(layout)
        self._populate_explorer_modes()

    def _populate_explorer_modes(self):
        modes = [
            ("Free Explorer (F5)", ExplorerMode.FREE),
            ("Arabic Letters Explorer (F6)", ExplorerMode.ARABIC),
            ("English Letters Explorer (F7)", ExplorerMode.ENGLISH),
            ("Numbers Explorer (F8)", ExplorerMode.NUMBERS),
        ]

        for title, mode_enum in modes:
            item = QListWidgetItem(title)
            item.setData(Qt.ItemDataRole.UserRole, mode_enum)
            self.explorer_list.addItem(item)

        self.explorer_list.setCurrentRow(0)

    def load_lessons(self):
        self.lessons = self.loader.load_all_lessons()

        self.ar_list.clear()
        self.en_list.clear()
        self.test_list.clear()

        for lesson in self.lessons:
            display_text = f"Level {lesson.difficulty}: {lesson.title}"
            item = QListWidgetItem(display_text)
            item.setData(Qt.ItemDataRole.UserRole, lesson)

            if getattr(lesson, "lesson_type", "lesson") == "test":
                self.test_list.addItem(item)
            elif getattr(lesson, "language", "en") == "ar":
                self.ar_list.addItem(item)
            else:
                self.en_list.addItem(item)

        for lst in (self.ar_list, self.en_list, self.test_list):
            if lst.count() > 0:
                lst.setCurrentRow(0)

    def _on_start_clicked(self):
        current_list = self.tabs.currentWidget()
        if not current_list:
            return

        selected_item = current_list.currentItem()
        if selected_item:
            data = selected_item.data(Qt.ItemDataRole.UserRole)
            if isinstance(data, ExplorerMode):
                self.explorer_requested.emit(data)
            else:
                self.lesson_selected.emit(data)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self._on_start_clicked()
            return
        super().keyPressEvent(event)

    def refresh_lessons(self):
        self.load_lessons()
