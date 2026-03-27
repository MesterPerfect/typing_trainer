from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt

class StatsPanel(QFrame):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        """ Initialize and layout the UI components. """
        self.setFrameShape(QFrame.Shape.StyledPanel)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        # Initialize labels with default values
        self.wpm_label = QLabel("WPM: 0")
        self.accuracy_label = QLabel("Accuracy: 100%")
        self.errors_label = QLabel("Errors: 0")
        self.time_label = QLabel("Time: 0.0s")

        # Apply basic styling and alignment
        font = self.font()
        font.setPointSize(12)
        font.setBold(True)

        for label in (self.wpm_label, self.accuracy_label, self.errors_label, self.time_label):
            label.setFont(font)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label)

        self.setLayout(layout)

    def update_stats(self, stats: dict):
        """ Update the labels with new statistics. """
        self.wpm_label.setText(f"WPM: {stats.get('wpm', 0)}")
        self.accuracy_label.setText(f"Accuracy: {stats.get('accuracy', 100.0)}%")
        self.errors_label.setText(f"Errors: {stats.get('errors', 0)}")
        self.time_label.setText(f"Time: {stats.get('time', 0.0)}s")
