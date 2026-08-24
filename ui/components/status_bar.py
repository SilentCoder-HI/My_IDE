from PySide6.QtWidgets import QStatusBar, QLabel

class StatusBar(QStatusBar):
    """Bottom status bar widget."""
    def __init__(self, current_dir: str, parent=None):
        super().__init__(parent)
        self.dir_label = QLabel(current_dir)
        self.addWidget(self.dir_label)

        self.addPermanentWidget(QLabel("UTF-8"))
        self.addPermanentWidget(QLabel("Ln 1, Col 1"))

    def update_dir(self, current_dir: str):
        self.dir_label.setText(current_dir)
