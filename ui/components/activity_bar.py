from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QToolButton, QStyle

class ActivityBar(QWidget):
    """Vertical bar on the far left of the IDE containing primary view icons."""
    toggle_explorer = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ActivityBar")
        self.setFixedWidth(48)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 8, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)

        style = self.style()
        icons = [
            ("Explorer", QStyle.SP_DirIcon, True),
            ("Search", QStyle.SP_FileDialogContentsView, False),
            ("Source Control", QStyle.SP_DriveNetIcon, False),
            ("Run and Debug", QStyle.SP_MediaPlay, False),
            ("Extensions", QStyle.SP_ComputerIcon, False),
        ]

        for name, icon_enum, checked in icons:
            btn = QToolButton()
            btn.setObjectName("ActivityBtn")
            btn.setIcon(style.standardIcon(icon_enum))
            btn.setIconSize(QSize(20, 20))
            btn.setToolTip(name)
            btn.setCheckable(True)
            btn.setChecked(checked)
            btn.setFixedSize(48, 42)
            if name == "Explorer":
                btn.clicked.connect(self.toggle_explorer.emit)
            layout.addWidget(btn)

        layout.addStretch()
        settings_btn = QToolButton()
        settings_btn.setObjectName("ActivityBtn")
        settings_btn.setIcon(style.standardIcon(QStyle.SP_FileDialogDetailedView))
        settings_btn.setIconSize(QSize(20, 20))
        settings_btn.setFixedSize(48, 42)
        settings_btn.setToolTip("Settings")
        layout.addWidget(settings_btn)
