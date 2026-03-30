from PySide6.QtWidgets import QWidget, QVBoxLayout, QCheckBox

class TypingPage(QWidget):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        self.virtual_kb_cb = QCheckBox(_("Show Virtual Keyboard during lessons"))
        self.virtual_kb_cb.setFont(self._get_font(14))
        layout.addWidget(self.virtual_kb_cb)

        layout.addStretch()
        self.setLayout(layout)

    def _get_font(self, size, bold=False):
        font = self.font()
        font.setPointSize(size)
        font.setBold(bold)
        return font

    def load(self):
        self.virtual_kb_cb.setChecked(self.settings.get("show_virtual_keyboard", True))

    def save(self) -> bool:
        """ Saves typing settings efficiently. """
        # Even for a single setting, using update_many ensures identical pipeline
        self.settings.update_many({
            "show_virtual_keyboard": self.virtual_kb_cb.isChecked()
        })
        return False
