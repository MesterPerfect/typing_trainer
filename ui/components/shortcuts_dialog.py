from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QPushButton,
)
from PySide6.QtCore import Qt


class ShortcutsDialog(QDialog):
    """
    Interactive and accessible keyboard shortcuts guide dialog.
    Allows screen reader users and visual users to quickly review all application keybindings.
    """

    def __init__(self, parent=None, tts=None):
        super().__init__(parent)
        self.tts = tts
        self.setWindowTitle(_("Keyboard Shortcuts Guide"))
        self.resize(720, 520)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(15)

        title = QLabel(_("Keyboard Shortcuts Guide"))
        font = title.font()
        font.setPointSize(18)
        font.setBold(True)
        title.setFont(font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Shortcuts Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels([_("Category"), _("Shortcut"), _("Description")])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        table_font = self.table.font()
        table_font.setPointSize(12)
        self.table.setFont(table_font)

        # Connect cell changed for TTS announcements
        self.table.currentCellChanged.connect(self._announce_cell)

        self._populate_shortcuts()
        layout.addWidget(self.table)

        # Close Button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.close_btn = QPushButton(_("Close (Esc)"))
        btn_font = self.close_btn.font()
        btn_font.setPointSize(13)
        btn_font.setBold(True)
        self.close_btn.setFont(btn_font)
        self.close_btn.setMinimumHeight(40)
        self.close_btn.setMinimumWidth(140)
        self.close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(self.close_btn)
        btn_layout.addStretch()

        layout.addLayout(btn_layout)

    def _populate_shortcuts(self):
        shortcuts_data = [
            # General Navigation
            (_("General"), "F1", _("Open User Guide Documentation")),
            (_("General"), "F2", _("Toggle Spoken Guided Mode (Finger & Keyboard Instructions)")),
            (_("General"), "F3", _("Open Settings Screen")),
            (_("General"), "F4", _("Open Results & Progress History")),
            (_("General"), "Ctrl+L", _("Open Lesson Manager / Editor")),
            (_("General"), "Ctrl+H", _("Open Keyboard Shortcuts Guide")),
            (_("General"), "Alt+F4", _("Exit Application")),
            (_("General"), "Esc", _("Return to Main Menu / Cancel / Close Dialog")),

            # Typing Practice
            (_("Typing"), "Ctrl+P / Pause", _("Pause or Resume Active Typing Session")),
            (_("Typing"), "Ctrl+R", _("Repeat Current Target Character & Finger Position")),
            (_("Typing"), "Backspace", _("Delete Previous Character with Spoken Feedback")),

            # Exploration Modes
            (_("Explorer"), "F5", _("Free Keyboard Exploration Mode")),
            (_("Explorer"), "F6", _("Arabic Letters Learning Mode")),
            (_("Explorer"), "F7", _("English Letters Learning Mode")),
            (_("Explorer"), "F8", _("Numbers Learning Mode")),
            (_("Explorer"), "F9", _("Special Keys & Symbols Learning Mode")),

            # Lesson Editor & Results
            (_("Editor"), "Ctrl+N", _("Create New Lesson")),
            (_("Editor"), "Ctrl+S", _("Save Current Lesson")),
            (_("Results"), "Ctrl+E", _("Export Typing Results to CSV File")),
        ]

        self.table.setRowCount(len(shortcuts_data))
        for row, (cat, key, desc) in enumerate(shortcuts_data):
            cat_item = QTableWidgetItem(cat)
            key_item = QTableWidgetItem(key)
            desc_item = QTableWidgetItem(desc)

            cat_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            key_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            desc_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

            self.table.setItem(row, 0, cat_item)
            self.table.setItem(row, 1, key_item)
            self.table.setItem(row, 2, desc_item)

    def _announce_cell(self, current_row, current_col, previous_row, previous_col):
        if self.tts and current_row >= 0:
            key_item = self.table.item(current_row, 1)
            desc_item = self.table.item(current_row, 2)
            if key_item and desc_item:
                self.tts.speak(f"{key_item.text()}: {desc_item.text()}")
