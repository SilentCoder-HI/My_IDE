import subprocess
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit
from config import get_code_font

class TerminalWidget(QWidget):
    """Integrated shell terminal widget."""
    def __init__(self, get_cwd, parent=None):
        super().__init__(parent)
        self.get_cwd = get_cwd
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(4)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(get_code_font())

        self.input = QLineEdit()
        self.input.setPlaceholderText("Type a command and press Enter…")
        self.input.setFont(get_code_font())
        self.input.returnPressed.connect(self.handle_command)

        layout.addWidget(self.output)
        layout.addWidget(self.input)

    def handle_command(self):
        command = self.input.text()
        cwd = self.get_cwd()
        self.output.append(f'<span style="color:#4ec9b0;">{cwd}&gt;</span> {command}')
        self.input.clear()

        if not command.strip():
            return
        if command.strip() == "clear":
            self.output.clear()
            return

        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True
        )
        if result.stdout:
            self.output.append(result.stdout)
        if result.stderr:
            self.output.append(f'<span style="color:#f14c4c;">{result.stderr}</span>')
