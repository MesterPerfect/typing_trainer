from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QFont, QPen, QBrush, QPainterPath
from PySide6.QtCore import Qt, QRectF
import logging

logger = logging.getLogger(__name__)

class VirtualKeyboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_lang = "ar"  # Default language
        self.target_key = ""      # The key that needs to be pressed
        
        # Define minimum height so it doesn't get crushed in the layout
        self.setMinimumHeight(200)
        
        # Finger Color Coding (Dark Mode Friendly)
        self.finger_colors = {
            "LP": QColor("#3f272c"), # Left Pinky (Reddish)
            "LR": QColor("#403024"), # Left Ring (Orangish)
            "LM": QColor("#3f3c22"), # Left Middle (Yellowish)
            "LI": QColor("#233a2a"), # Left Index (Greenish)
            "RI": QColor("#223440"), # Right Index (Bluish)
            "RM": QColor("#2c273f"), # Right Middle (Purplish)
            "RR": QColor("#3f2434"), # Right Ring (Pinkish)
            "RP": QColor("#2c3138"), # Right Pinky (Slate)
            "TH": QColor("#2c3138"), # Thumbs (Spacebar)
        }
        
        self.active_color = QColor("#00ff00") # Bright Green for target key
        self.active_text_color = QColor("#000000")
        self.idle_text_color = QColor("#e2e8f0")

        self._init_key_map()

    def _init_key_map(self):
        """
        Map each key with its English char, Arabic char, and responsible finger.
        Format: (English, Arabic, Finger_Code, Width_Multiplier)
        """
        self.rows = [
            # Top Row (QWERTY)
            [
                ('q', 'ض', 'LP', 1), ('w', 'ص', 'LR', 1), ('e', 'ث', 'LM', 1), 
                ('r', 'ق', 'LI', 1), ('t', 'ف', 'LI', 1), ('y', 'غ', 'RI', 1), 
                ('u', 'ع', 'RI', 1), ('i', 'ه', 'RM', 1), ('o', 'خ', 'RR', 1), 
                ('p', 'ح', 'RP', 1), ('[', 'ج', 'RP', 1), (']', 'د', 'RP', 1)
            ],
            # Home Row (ASDFG)
            [
                ('a', 'ش', 'LP', 1), ('s', 'س', 'LR', 1), ('d', 'ي', 'LM', 1), 
                ('f', 'ب', 'LI', 1), ('g', 'ل', 'LI', 1), ('h', 'ا', 'RI', 1), 
                ('j', 'ت', 'RI', 1), ('k', 'ن', 'RM', 1), ('l', 'م', 'RR', 1), 
                (';', 'ك', 'RP', 1), ("'", 'ط', 'RP', 1)
            ],
            # Bottom Row (ZXCVB)
            [
                ('z', 'ئ', 'LP', 1), ('x', 'ء', 'LR', 1), ('c', 'ؤ', 'LM', 1), 
                ('v', 'ر', 'LI', 1), ('b', 'لا', 'LI', 1), ('n', 'ى', 'RI', 1), 
                ('m', 'ة', 'RI', 1), (',', 'و', 'RM', 1), ('.', 'ز', 'RR', 1), 
                ('/', 'ظ', 'RP', 1)
            ],
            # Spacebar Row
            [
                (' ', ' ', 'TH', 6) # Spacebar is 6 times wider than a normal key
            ]
        ]
        
        # Row starting offsets (in key widths) to simulate realistic staggered keyboard
        self.row_offsets = [0.5, 0.8, 1.2, 3.5]

    def set_language(self, lang_code: str):
        """Update the displayed language on the keyboard ('en' or 'ar')."""
        self.current_lang = lang_code
        self.update() # Trigger a repaint

    def highlight_key(self, target_char: str):
        """Highlight the key that the user needs to press."""
        if target_char == "space":
            self.target_key = " "
        else:
            self.target_key = target_char.lower()
        self.update() # Trigger a repaint

    def paintEvent(self, event):
        """The core drawing engine. Paints the keyboard dynamically."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Calculate dimensions
        width = self.width()
        height = self.height()
        
        # We assume a max width of 13 normal keys + offsets to calculate base unit width
        gap = 6
        cols = 13.5
        rows_count = len(self.rows)
        
        key_w = (width - (cols * gap)) / cols
        key_h = (height - (rows_count * gap)) / rows_count

        # Setup Fonts
        primary_font = QFont("Arial", int(key_h * 0.4), QFont.Weight.Bold)
        secondary_font = QFont("Arial", int(key_h * 0.2))

        # Start drawing rows
        current_y = gap

        for row_idx, row in enumerate(self.rows):
            # Calculate starting X based on row offset
            current_x = (self.row_offsets[row_idx] * key_w) + gap

            for en_char, ar_char, finger, w_mult in row:
                is_target = False
                
                # Check if this key is the target key
                if self.target_key:
                    if self.current_lang == "ar" and self.target_key == ar_char:
                        is_target = True
                    elif self.current_lang == "en" and self.target_key == en_char:
                        is_target = True
                    elif self.target_key == en_char == ar_char == " ":
                        is_target = True

                # Determine key width (useful for spacebar)
                actual_key_w = (key_w * w_mult) + (gap * (w_mult - 1))
                key_rect = QRectF(current_x, current_y, actual_key_w, key_h)

                # Set colors based on state
                if is_target:
                    bg_color = self.active_color
                    txt_color = self.active_text_color
                    # Glowing border for target key
                    pen = QPen(QColor("#ffffff"), 3)
                else:
                    bg_color = self.finger_colors.get(finger, QColor("#333333"))
                    txt_color = self.idle_text_color
                    pen = QPen(QColor("#1e293b"), 1)

                # Draw the key shape
                painter.setBrush(QBrush(bg_color))
                painter.setPen(pen)
                painter.drawRoundedRect(key_rect, 8, 8)

                # Draw the Text
                painter.setPen(QPen(txt_color))
                
                if self.current_lang == "ar":
                    primary_char = ar_char
                    secondary_char = en_char
                else:
                    primary_char = en_char.upper()
                    secondary_char = ar_char

                # Draw Primary Character (Centered)
                painter.setFont(primary_font)
                painter.drawText(key_rect, Qt.AlignmentFlag.AlignCenter, primary_char)

                # Draw Secondary Character (Small, Top-Right)
                if primary_char != " ": # Don't draw secondary for spacebar
                    painter.setFont(secondary_font)
                    # Create a smaller rect for the top right corner
                    sec_rect = key_rect.adjusted(0, 4, -8, 0)
                    painter.drawText(sec_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop, secondary_char)

                # Move to next key position
                current_x += actual_key_w + gap

            # Move to next row position
            current_y += key_h + gap
