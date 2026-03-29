from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem, 
    QStackedWidget, QPushButton, QLabel, QFrame, QMessageBox
)
from PySide6.QtCore import Signal, Qt
import logging

from .pages import AppearancePage, AudioPage, TypingPage, SystemPage

logger = logging.getLogger(__name__)

class SettingsView(QWidget):
    return_requested = Signal()

    def __init__(self, settings, tts):
        super().__init__()
        self.settings = settings
        self.tts = tts
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Title
        title = QLabel(_("Settings"))
        font = title.font()
        font.setPointSize(18)
        font.setBold(True)
        title.setFont(font)
        main_layout.addWidget(title)

        # Master-Detail Layout (Tree on left, Pages on right)
        split_layout = QHBoxLayout()

        # 1. Left Side: Category Tree
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderHidden(True)
        self.tree_widget.setFixedWidth(200)
        self.tree_widget.setFont(self._get_font(14))
        
        categories = [
            _("Appearance"), 
            _("Audio & Voice"), 
            _("Typing Setup"), 
            _("System")
        ]
        
        for cat in categories:
            item = QTreeWidgetItem([cat])
            self.tree_widget.addTopLevelItem(item)

        # 2. Right Side: Stacked Widget for Pages
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setFrameShape(QFrame.Shape.StyledPanel)
        
        self.pages = [
            AppearancePage(self.settings),
            AudioPage(self.settings),
            TypingPage(self.settings),
            SystemPage(self.settings)
        ]
        
        for page in self.pages:
            self.stacked_widget.addWidget(page)

        # Connect Tree Selection to Stacked Widget
        self.tree_widget.currentItemChanged.connect(self._on_category_changed)

        split_layout.addWidget(self.tree_widget)
        split_layout.addWidget(self.stacked_widget)
        main_layout.addLayout(split_layout)

        # Buttons Layout (Bottom)
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        # Close/Cancel Button
        self.cancel_btn = QPushButton(_("Close (Esc)"))
        self.cancel_btn.setFont(self._get_font(14))
        self.cancel_btn.setMinimumHeight(40)
        self.cancel_btn.clicked.connect(self.close_without_saving)
        buttons_layout.addWidget(self.cancel_btn)

        # Save Button
        self.save_btn = QPushButton(_("Save Settings"))
        self.save_btn.setFont(self._get_font(14, bold=True))
        self.save_btn.setMinimumHeight(40)
        self.save_btn.clicked.connect(self.save_and_return)
        buttons_layout.addWidget(self.save_btn)

        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)

    def _get_font(self, size, bold=False):
        font = self.font()
        font.setPointSize(size)
        font.setBold(bold)
        return font

    def _on_category_changed(self, current, previous):
        if current:
            index = self.tree_widget.indexOfTopLevelItem(current)
            self.stacked_widget.setCurrentIndex(index)

    def load_current_settings(self):
        # Select first item by default
        if self.tree_widget.topLevelItemCount() > 0:
            self.tree_widget.setCurrentItem(self.tree_widget.topLevelItem(0))
            
        for page in self.pages:
            page.load()

    def close_without_saving(self):
        """Closes the settings view without applying any changes."""
        self.tts.speak(_("Settings canceled."))
        # Reloading resets the UI elements back to the currently saved JSON state
        self.load_current_settings() 
        self.return_requested.emit()

    def save_and_return(self):
        """Saves settings and checks if any page requires an app restart."""
        restart_required = False
        
        for page in self.pages:
            # Check if the page's save method explicitly returns True (needs restart)
            result = page.save()
            if result is True:
                restart_required = True

        self.tts.speak(_("Settings saved."))

        if restart_required:
            msg_title = _("Restart Required")
            msg_text = _("Some changes (like Language or Theme) require the application to be restarted to take full effect.")
            
            # Speak the warning for screen reader users
            self.tts.speak(msg_text)
            
            # Show visual warning
            QMessageBox.information(self, msg_title, msg_text)

        self.return_requested.emit()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close_without_saving()
            event.accept()
        else:
            super().keyPressEvent(event)
