from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QLabel, QSlider
from PySide6.QtCore import Qt

class AudioPage(QWidget):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        self.guided_mode_cb = QCheckBox(_("Enable Guided Mode (Voice Prompts)"))
        self.guided_mode_cb.setFont(self._get_font(14))
        layout.addWidget(self.guided_mode_cb)

        self.sound_effects_cb = QCheckBox(_("Enable Sound Effects (Typing Clicks & Errors)"))
        self.sound_effects_cb.setFont(self._get_font(14))
        layout.addWidget(self.sound_effects_cb)

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

        layout.addStretch()
        self.setLayout(layout)

    def _get_font(self, size, bold=False):
        font = self.font()
        font.setPointSize(size)
        font.setBold(bold)
        return font

    def load(self):
        self.guided_mode_cb.setChecked(self.settings.get("guided_mode", True))
        self.sound_effects_cb.setChecked(self.settings.get("sound_effects", True))
        self.volume_slider.setValue(self.settings.get("sound_volume", 70))

    def save(self):
        self.settings.set("guided_mode", self.guided_mode_cb.isChecked())
        self.settings.set("sound_effects", self.sound_effects_cb.isChecked())
        self.settings.set("sound_volume", self.volume_slider.value())
