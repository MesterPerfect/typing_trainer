from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QLabel, QSpinBox

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

        self.auto_repeat_cb = QCheckBox(_("Automatically repeat current character prompt when idle"))
        self.auto_repeat_cb.setFont(self._get_font(14))
        self.auto_repeat_cb.toggled.connect(self._on_auto_repeat_toggled)
        layout.addWidget(self.auto_repeat_cb)

        # Interval row
        interval_layout = QHBoxLayout()
        self.interval_label = QLabel(_("Repeat interval (seconds):"))
        self.interval_label.setFont(self._get_font(12))
        
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(2, 20)
        self.interval_spin.setSingleStep(1)
        self.interval_spin.setFont(self._get_font(12))
        
        interval_layout.addWidget(self.interval_label)
        interval_layout.addWidget(self.interval_spin)
        interval_layout.addStretch()
        layout.addLayout(interval_layout)

        layout.addStretch()
        self.setLayout(layout)

    def _on_auto_repeat_toggled(self, checked: bool):
        self.interval_label.setEnabled(checked)
        self.interval_spin.setEnabled(checked)

    def _get_font(self, size, bold=False):
        font = self.font()
        font.setPointSize(size)
        font.setBold(bold)
        return font

    def load(self):
        self.virtual_kb_cb.setChecked(self.settings.get("show_virtual_keyboard", True))
        auto_repeat = self.settings.get("auto_repeat_prompt", False)
        self.auto_repeat_cb.setChecked(auto_repeat)
        self.interval_spin.setValue(int(self.settings.get("auto_repeat_interval", 4)))
        self._on_auto_repeat_toggled(auto_repeat)

    def save(self) -> bool:
        """ Saves typing settings efficiently. """
        self.settings.update_many({
            "show_virtual_keyboard": self.virtual_kb_cb.isChecked(),
            "auto_repeat_prompt": self.auto_repeat_cb.isChecked(),
            "auto_repeat_interval": self.interval_spin.value()
        })
        return False
