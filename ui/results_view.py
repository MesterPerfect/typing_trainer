from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QFileDialog,
    QFrame,
)
from PySide6.QtCore import Signal, Qt
from pathlib import Path
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
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(15)

        title = QLabel(_("Your Progress & Results History"))
        font = title.font()
        font.setPointSize(22)
        font.setBold(True)
        title.setFont(font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Lifetime Summary Card
        self.summary_card = QFrame()
        self.summary_card.setFrameShape(QFrame.Shape.StyledPanel)
        summary_layout = QHBoxLayout(self.summary_card)
        summary_layout.setContentsMargins(15, 10, 15, 10)

        self.summary_label = QLabel()
        summary_font = self.summary_card.font()
        summary_font.setPointSize(13)
        summary_font.setBold(True)
        self.summary_label.setFont(summary_font)
        self.summary_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary_layout.addWidget(self.summary_label)

        layout.addWidget(self.summary_card)

        # Results Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            [_("Date"), _("Lesson"), _("WPM"), _("CPM"), _("Accuracy"), _("Errors")]
        )

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        table_font = self.table.font()
        table_font.setPointSize(13)
        self.table.setFont(table_font)

        # Connect the cell change signal to our custom TTS function
        self.table.currentCellChanged.connect(self.announce_cell)

        layout.addWidget(self.table)

        # Action Buttons Layout
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)

        self.export_button = QPushButton(_("Export to CSV (Ctrl+E)"))
        self.export_button.setFont(self._get_btn_font(13))
        self.export_button.setMinimumHeight(45)
        self.export_button.clicked.connect(self.export_results)
        btn_layout.addWidget(self.export_button)

        self.clear_button = QPushButton(_("Clear History"))
        self.clear_button.setFont(self._get_btn_font(13))
        self.clear_button.setMinimumHeight(45)
        self.clear_button.clicked.connect(self.confirm_clear_history)
        btn_layout.addWidget(self.clear_button)

        self.back_button = QPushButton(_("Return to Menu (Esc)"))
        self.back_button.setFont(self._get_btn_font(13))
        self.back_button.setMinimumHeight(45)
        self.back_button.clicked.connect(self.return_requested.emit)
        btn_layout.addWidget(self.back_button)

        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def _get_btn_font(self, size):
        font = self.font()
        font.setPointSize(size)
        font.setBold(True)
        return font

    def load_results(self):
        """Fetch all results from the memory cache and populate the table & summary."""
        self.table.setRowCount(0)

        lessons = {
            str(lvl.id): lvl.title for lvl in self.lesson_loader.load_all_lessons()
        }

        # Update Lifetime Summary Banner
        summary = self.result_service.get_lifetime_summary()
        total_time_min = round(summary["total_time_seconds"] / 60.0, 1)
        summary_text = (
            f"{_('Total Sessions:')} {summary['total_sessions']}  |  "
            f"{_('Peak Speed:')} {summary['peak_wpm']} WPM ({summary['peak_cpm']} CPM)  |  "
            f"{_('Average WPM:')} {summary['avg_wpm']}  |  "
            f"{_('Avg Accuracy:')} {summary['avg_accuracy']}%  |  "
            f"{_('Total Time:')} {total_time_min} {_('min')}"
        )
        self.summary_label.setText(summary_text)

        try:
            # Retrieve data directly from the service cache, avoiding disk I/O
            data = self.result_service.cached_results.copy()
            data.reverse()

            for row_idx, item in enumerate(data):
                self.table.insertRow(row_idx)

                # Format Date safely
                ts = item.get("timestamp", 0)
                date_str = ""
                if ts:
                    try:
                        if isinstance(ts, (int, float)):
                            date_str = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
                        else:
                            date_str = str(ts)
                    except Exception:
                        date_str = str(ts)


                # Get Lesson Title
                lesson_id = str(item.get("lesson_id", ""))
                lesson_title = lessons.get(lesson_id, f"Lesson {lesson_id}")

                # Create items
                date_item = QTableWidgetItem(date_str)
                title_item = QTableWidgetItem(lesson_title)
                wpm_item = QTableWidgetItem(str(item.get("wpm", 0)))
                cpm_item = QTableWidgetItem(str(item.get("cpm", 0)))
                acc_item = QTableWidgetItem(f"{item.get('accuracy', 0)}%")
                err_item = QTableWidgetItem(str(item.get("errors", 0)))

                # Center align items
                for table_item in (date_item, title_item, wpm_item, cpm_item, acc_item, err_item):
                    table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                self.table.setItem(row_idx, 0, date_item)
                self.table.setItem(row_idx, 1, title_item)
                self.table.setItem(row_idx, 2, wpm_item)
                self.table.setItem(row_idx, 3, cpm_item)
                self.table.setItem(row_idx, 4, acc_item)
                self.table.setItem(row_idx, 5, err_item)

        except Exception as e:
            logger.error(f"Failed to populate results table: {e}")

    def export_results(self):
        """Export results to CSV file via file dialog."""
        lessons = {
            str(lvl.id): lvl.title for lvl in self.lesson_loader.load_all_lessons()
        }
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            _("Export Results"),
            "typing_results.csv",
            "CSV Files (*.csv);;All Files (*)"
        )
        if file_path:
            success = self.result_service.export_to_csv(Path(file_path), lessons)
            if success:
                msg = _("Results exported successfully.")
                self.tts.speak(msg)
                QMessageBox.information(self, _("Export Successful"), msg)
            else:
                msg = _("Failed to export results.")
                self.tts.speak(msg)
                QMessageBox.warning(self, _("Export Failed"), msg)

    def confirm_clear_history(self):
        """Prompt user confirmation before clearing all results."""
        reply = QMessageBox.question(
            self,
            _("Clear History"),
            _("Are you sure you want to permanently delete all typing test results and history?"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.result_service.clear_all_results()
            self.load_results()
            msg = _("Results history cleared.")
            self.tts.speak(msg)

    def keyPressEvent(self, event):
        """Handle shortcuts in Results view."""
        if event.key() == Qt.Key.Key_Escape:
            self.return_requested.emit()
            return

        modifiers = event.modifiers()
        if modifiers & Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_E:
                self.export_results()
                return

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
