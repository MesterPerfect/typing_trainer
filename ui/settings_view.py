from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QCheckBox,
    QPushButton,
    QLabel,
    QSlider,
    QHBoxLayout,
    QComboBox,
)
from PySide6.QtCore import Signal, Qt
import logging

logger = logging.getLogger(__name__)


class SettingsView(QWidget):
    return_requested = Signal()

    def __init__(self, settings, tts):
        super().__init__()
        self.settings = settings
        self.tts = tts
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel(_("Settings"))
        title.setFont(self._get_font(18, bold=True))
        layout.addWidget(title)

        # ==========================================
        # General & UI Settings
        # ==========================================
        
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

        # Auto Update Toggle
        self.auto_update_cb = QCheckBox(_("Check for updates automatically on startup"))
        self.auto_update_cb.setFont(self._get_font(14))
        layout.addWidget(self.auto_update_cb)

        # ==========================================
        # Audio & TTS Settings
        # ==========================================
        
        # TTS Guided Mode
        self.guided_mode_cb = QCheckBox(_("Enable Guided Mode (Voice Prompts)"))
        self.guided_mode_cb.setFont(self._get_font(14))
        layout.addWidget(self.guided_mode_cb)

        # Sound Effects Enable/Disable
        self.sound_effects_cb = QCheckBox(_("Enable Sound Effects (Typing Clicks & Errors)"))
        self.sound_effects_cb.setFont(self._get_font(14))
        layout.addWidget(self.sound_effects_cb)

        # Sound Effects Volume Slider
        vol_layout = QHBoxLayout()
        vol_label = QLabel(_("Sound Effects Volume:"))
        vol_label.setFont(self._get_font(14))

        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.volume_slider.setTickInterval(10)

        vol_layout.addWidget(vol_label)
        vol_layout.addWidget(self.volume_slider)
        layout.addLayout(vol_layout)

        # ==========================================
        # Logging Settings
        # ==========================================

        # Enable/Disable Logging
        self.enable_logging_cb = QCheckBox(_("Enable Application Logging"))
        self.enable_logging_cb.setFont(self._get_font(14))
        layout.addWidget(self.enable_logging_cb)

        # Log Level Selection
        log_level_layout = QHBoxLayout()
        log_level_label = QLabel(_("Log Level:"))
        log_level_label.setFont(self._get_font(14))
        
        self.log_level_combo = QComboBox()
        self.log_level_combo.setFont(self._get_font(14))
        self.log_level_combo.addItems(["DEBUG", "INFO", "WARNING", "ERROR"])
        
        log_level_layout.addWidget(log_level_label)
        log_level_layout.addWidget(self.log_level_combo)
        layout.addLayout(log_level_layout)

        # Remove Timestamp from Logs
        self.no_log_time_cb = QCheckBox(_("Remove Timestamp from Logs"))
        self.no_log_time_cb.setFont(self._get_font(14))
        layout.addWidget(self.no_log_time_cb)

        # ==========================================
        # Save Button
        # ==========================================
        
        self.save_btn = QPushButton(_("Save and Return (Esc)"))
        self.save_btn.setFont(self._get_font(14, bold=True))
        self.save_btn.setMinimumHeight(40)
        self.save_btn.clicked.connect(self.save_and_return)
        layout.addWidget(self.save_btn)

        layout.addStretch()
        self.setLayout(layout)

    def _get_font(self, size, bold=False):
        font = self.font()
        font.setPointSize(size)
        font.setBold(bold)
        return font

    def load_current_settings(self):
        # Language
        current_lang = self.settings.get("ui_language", "en")
        index = self.lang_combo.findData(current_lang)
        if index >= 0:
            self.lang_combo.setCurrentIndex(index)

        # General & Audio
        self.auto_update_cb.setChecked(self.settings.get("auto_update", True))
        self.guided_mode_cb.setChecked(self.settings.get("guided_mode", True))
        self.sound_effects_cb.setChecked(self.settings.get("sound_effects", True))
        self.volume_slider.setValue(self.settings.get("sound_volume", 70))

        # Logging
        self.enable_logging_cb.setChecked(self.settings.get("enable_logging", True))
        
        current_log_level = self.settings.get("log_level", "INFO")
        level_index = self.log_level_combo.findText(current_log_level)
        if level_index >= 0:
            self.log_level_combo.setCurrentIndex(level_index)
            
        self.no_log_time_cb.setChecked(self.settings.get("no_log_time", False))

    def save_and_return(self):
        # Save all settings
        self.settings.set("ui_language", self.lang_combo.currentData())
        self.settings.set("auto_update", self.auto_update_cb.isChecked())
        self.settings.set("guided_mode", self.guided_mode_cb.isChecked())
        self.settings.set("sound_effects", self.sound_effects_cb.isChecked())
        self.settings.set("sound_volume", self.volume_slider.value())
        self.settings.set("enable_logging", self.enable_logging_cb.isChecked())
        self.settings.set("log_level", self.log_level_combo.currentText())
        self.settings.set("no_log_time", self.no_log_time_cb.isChecked())

        self.tts.speak(_("Settings saved. Some changes may require a restart."))
        self.return_requested.emit()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.save_and_return()
        else:
            super().keyPressEvent(event)
