from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QLabel, QComboBox

class SystemPage(QWidget):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        self.auto_update_cb = QCheckBox(_("Check for updates automatically on startup"))
        self.auto_update_cb.setFont(self._get_font(14))
        layout.addWidget(self.auto_update_cb)

        self.enable_logging_cb = QCheckBox(_("Enable Application Logging"))
        self.enable_logging_cb.setFont(self._get_font(14))
        layout.addWidget(self.enable_logging_cb)

        self.no_log_time_cb = QCheckBox(_("Remove Timestamp from Logs"))
        self.no_log_time_cb.setFont(self._get_font(14))
        layout.addWidget(self.no_log_time_cb)

        log_level_layout = QHBoxLayout()
        log_level_label = QLabel(_("Log Level:"))
        log_level_label.setFont(self._get_font(14))
        
        self.log_level_combo = QComboBox()
        self.log_level_combo.setFont(self._get_font(14))
        self.log_level_combo.addItems(["DEBUG", "INFO", "WARNING", "ERROR"])
        
        log_level_layout.addWidget(log_level_label)
        log_level_layout.addWidget(self.log_level_combo)
        layout.addLayout(log_level_layout)

        layout.addStretch()
        self.setLayout(layout)

    def _get_font(self, size, bold=False):
        font = self.font()
        font.setPointSize(size)
        font.setBold(bold)
        return font

    def load(self):
        self.auto_update_cb.setChecked(self.settings.get("auto_update", True))
        self.enable_logging_cb.setChecked(self.settings.get("enable_logging", True))
        self.no_log_time_cb.setChecked(self.settings.get("no_log_time", False))
        
        current_log_level = self.settings.get("log_level", "INFO")
        idx = self.log_level_combo.findText(current_log_level)
        if idx >= 0: self.log_level_combo.setCurrentIndex(idx)

    def save(self):
        self.settings.set("auto_update", self.auto_update_cb.isChecked())
        self.settings.set("enable_logging", self.enable_logging_cb.isChecked())
        self.settings.set("no_log_time", self.no_log_time_cb.isChecked())
        self.settings.set("log_level", self.log_level_combo.currentText())
