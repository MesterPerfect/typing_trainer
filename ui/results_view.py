from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
from PySide6.QtCore import Signal, Qt
import logging
from datetime import datetime

from services.lesson import LessonService

logger = logging.getLogger(__name__)


class ResultsView(QWidget):
    return_requested = Signal()

    def __init__(self, result_service, tts):
        super().__init__()
        self.result_service = result_service
        self.tts = tts
        self.lesson_loader = LessonService()

        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        title = QLabel(_("Your Progress"))
        font = title.font()
        font.setPointSize(24)
        font.setBold(True)
        title.setFont(font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Date", "Lesson", "WPM", "Accuracy", "Errors"]
        )

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        table_font = self.table.font()
        table_font.setPointSize(14)
        self.table.setFont(table_font)

        # Connect the cell change signal to our custom TTS function
        self.table.currentCellChanged.connect(self.announce_cell)

        layout.addWidget(self.table)

        self.back_button = QPushButton(_("Return to Menu (Esc)"))
        btn_font = self.back_button.font()
        btn_font.setPointSize(16)
        btn_font.setBold(True)
        self.back_button.setFont(btn_font)
        self.back_button.setMinimumHeight(50)
        self.back_button.clicked.connect(self.return_requested.emit)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def load_results(self):
        """Fetch all results and populate the table."""
        self.table.setRowCount(0)

        lessons = {
            str(lvl.id): lvl.title for lvl in self.lesson_loader.load_all_lessons()
        }

        import json
        import os

        file_path = self.result_service.file_path
        if not os.path.exists(file_path):
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Reverse data to show newest first
            data.reverse()

            for row_idx, item in enumerate(data):
                self.table.insertRow(row_idx)

                # Format Date
                date_str = datetime.fromtimestamp(item.get("timestamp", 0)).strftime(
                    "%Y-%m-%d %H:%M"
                )

                # Get Lesson Title
                lesson_id = str(item.get("lesson_id", ""))
                lesson_title = lessons.get(lesson_id, f"Lesson {lesson_id}")

                # Create items
                date_item = QTableWidgetItem(date_str)
                title_item = QTableWidgetItem(lesson_title)
                wpm_item = QTableWidgetItem(str(item.get("wpm", 0)))
                acc_item = QTableWidgetItem(f"{item.get('accuracy', 0)}%")
                err_item = QTableWidgetItem(str(item.get("errors", 0)))

                # Center align items
                for table_item in (date_item, title_item, wpm_item, acc_item, err_item):
                    table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                self.table.setItem(row_idx, 0, date_item)
                self.table.setItem(row_idx, 1, title_item)
                self.table.setItem(row_idx, 2, wpm_item)
                self.table.setItem(row_idx, 3, acc_item)
                self.table.setItem(row_idx, 4, err_item)

        except Exception as e:
            logger.error(f"Failed to populate results table: {e}")

    def keyPressEvent(self, event):
        """Allow returning by pressing Escape."""
        if event.key() == Qt.Key.Key_Escape:
            self.return_requested.emit()
        else:
            super().keyPressEvent(event)

    def announce_cell(self, current_row, current_col, previous_row, previous_col):
        """Announce the column header and cell value for accessibility."""
        if current_row >= 0 and current_col >= 0:
            header_item = self.table.horizontalHeaderItem(current_col)
            cell_item = self.table.item(current_row, current_col)

            header_text = header_item.text() if header_item else ""
            cell_text = cell_item.text() if cell_item else ""

            # Speak the header then the value
            self.tts.speak(f"{header_text}, {cell_text}")
