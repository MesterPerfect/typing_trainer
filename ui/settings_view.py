from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QCheckBox, 
                             QPushButton, QLabel, QSlider, QHBoxLayout)
from PyQt6.QtCore import pyqtSignal, Qt
import logging

logger = logging.getLogger(__name__)

class SettingsView(QWidget):
    return_requested = pyqtSignal()

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

        # TTS Guided Mode
        self.guided_mode_cb = QCheckBox("Enable Guided Mode (Voice Prompts)")
        self.guided_mode_cb.setFont(self._get_font(14))
        layout.addWidget(self.guided_mode_cb)

        # Sound Effects Enable/Disable
        self.sound_effects_cb = QCheckBox("Enable Sound Effects (Typing Clicks & Errors)")
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

        # Save and Return Button
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
        guided = self.settings.get("guided_mode", True)
        self.guided_mode_cb.setChecked(guided)

        sfx = self.settings.get("sound_effects", True)
        self.sound_effects_cb.setChecked(sfx)

        vol = self.settings.get("sound_volume", 70)
        self.volume_slider.setValue(vol)

    def save_and_return(self):
        self.settings.set("guided_mode", self.guided_mode_cb.isChecked())
        self.settings.set("sound_effects", self.sound_effects_cb.isChecked())
        self.settings.set("sound_volume", self.volume_slider.value())
        
        self.tts.speak("Settings saved")
        self.return_requested.emit()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.save_and_return()
        else:
            super().keyPressEvent(event)
