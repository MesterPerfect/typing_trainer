from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt


class TextDisplay(QLabel):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByKeyboard)
        # Enable word wrap so long sentences don't break the window width
        self.setWordWrap(True) 

    def update_display(
        self, full_text: str, correct: str, current: str, remaining: str
    ):
        """
        Updates the label with HTML formatted text.
        Highlights the correct text in green, shows a HUGE target character for low vision,
        and displays the remaining text in gray.
        """
        # 1. Smart Space Handling for the Huge Display
        if not current:
            huge_char = "✓"  # Finished!
        elif current == " ":
            huge_char = "␣"  # Visible symbol for Spacebar
        else:
            huge_char = current

        # 2. HTML/CSS Injector (Dark Mode & Low Vision Friendly)
        html = f"""
        <div style='text-align: center; margin-bottom: 40px;'>
            <span style='font-size: 100px; font-weight: 900; color: #f9e2af; background-color: #1e1e2e; padding: 10px 50px; border: 4px solid #f9e2af; border-radius: 20px;'>
                {huge_char}
            </span>
        </div>
        
        <div style='text-align: center; font-size: 38px; font-family: monospace; letter-spacing: 3px; line-height: 1.5;'>
            <span style='color: #a6e3a1; font-weight: bold;'>{correct}</span>
            <span style='color: #1e1e2e; background-color: #89b4fa; font-weight: bold; padding: 0px 4px; border-radius: 4px;'>{current}</span>
            <span style='color: #9399b2;'>{remaining}</span>
        </div>
        """
        self.setText(html)

