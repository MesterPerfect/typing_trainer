from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox

class AppearancePage(QWidget):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Language Selection
        lang_layout = QHBoxLayout()
        lang_label = QLabel(_("UI Language (Requires Restart):"))
        lang_label.setFont(self._get_font(14))
        
        self.lang_combo = QComboBox()
        self.lang_combo.setFont(self._get_font(14))
        self.lang_combo.addItem("English", "en")
        self.lang_combo.addItem("العربية", "ar")
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.lang_combo)
        layout.addLayout(lang_layout)

        # Theme Selection
        theme_layout = QHBoxLayout()
        theme_label = QLabel(_("Application Theme (Requires Restart):"))
        theme_label.setFont(self._get_font(14))
        
        self.theme_combo = QComboBox()
        self.theme_combo.setFont(self._get_font(14))
        self.theme_combo.addItem("Dark Theme", "dark_theme")
        self.theme_combo.addItem("High Contrast", "high_contrast")
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        layout.addLayout(theme_layout)

        layout.addStretch()
        self.setLayout(layout)

    def _get_font(self, size, bold=False):
        font = self.font()
        font.setPointSize(size)
        font.setBold(bold)
        return font

    def load(self):
        current_lang = self.settings.get("ui_language", "en")
        idx = self.lang_combo.findData(current_lang)
        if idx >= 0: self.lang_combo.setCurrentIndex(idx)

        current_theme = self.settings.get("theme", "dark_theme")
        idx = self.theme_combo.findData(current_theme)
        if idx >= 0: self.theme_combo.setCurrentIndex(idx)

    def save(self) -> bool:
        """
        Saves settings and returns True if a restart is required.
        """
        restart_required = False

        old_lang = self.settings.get("ui_language", "en")
        new_lang = self.lang_combo.currentData()
        if old_lang != new_lang:
            self.settings.set("ui_language", new_lang)
            restart_required = True

        old_theme = self.settings.get("theme", "dark_theme")
        new_theme = self.theme_combo.currentData()
        if old_theme != new_theme:
            self.settings.set("theme", new_theme)
            restart_required = True

        return restart_required
