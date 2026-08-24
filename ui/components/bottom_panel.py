from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QTextEdit
from ui.widgets.terminal_widget import TerminalWidget

class BottomPanel(QWidget):
    """Bottom container for Terminal, Output logs, and Problems."""
    def __init__(self, get_cwd, parent=None):
        super().__init__(parent)
        self.setObjectName("BottomPanel")
        self.get_cwd = get_cwd
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.panel_tabs = QTabWidget()
        self.terminal = TerminalWidget(get_cwd=self.get_cwd)
        self.output_edit = QTextEdit()
        self.output_edit.setReadOnly(True)
        self.problems_edit = QTextEdit()
        self.problems_edit.setReadOnly(True)

        self.panel_tabs.addTab(self.terminal, "TERMINAL")
        self.panel_tabs.addTab(self.output_edit, "OUTPUT")
        self.panel_tabs.addTab(self.problems_edit, "PROBLEMS")

        layout.addWidget(self.panel_tabs)

    def focus_terminal(self):
        self.panel_tabs.setCurrentWidget(self.terminal)
        self.terminal.input.setFocus()

    def log(self, text: str):
        self.output_edit.append(text)
