from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt


class TextDisplay(QLabel):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByKeyboard)

    def update_display(
        self, full_text: str, correct: str, current: str, remaining: str
    ):
        """
        Updates the label with HTML formatted text.
        Shows the full target text on top, and highlights the current character.
        """
        html = f"""
        <div style='text-align: center; margin-bottom: 40px;'>
            <span style='font-size: 24px; color: #a6adc8;'>{full_text}</span>
        </div>
        <div style='text-align: center; font-size: 48px; letter-spacing: 2px;'>
            <span style='color: #a6e3a1;'>{correct}</span>
            <span style='color: #11111b; background-color: #f38ba8; border-radius: 6px; padding: 2px 8px; font-weight: bold;'>{current}</span>
            <span style='color: #6c7086;'>{remaining}</span>
        </div>
        """
        self.setText(html)
