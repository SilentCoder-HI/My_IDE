import os
from PySide6.QtWidgets import QTabWidget, QPlainTextEdit, QMessageBox
from config import get_code_font
from services.file_service import FileService
from core.event_bus import events

class EditorArea(QTabWidget):
    """Tabbed code editor container."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.open_files = {}  # tab index -> file path
        self.tabCloseRequested.connect(self.close_tab)

        self._show_welcome_tab()

    def _show_welcome_tab(self):
        welcome = QPlainTextEdit()
        welcome.setReadOnly(True)
        welcome.setFont(get_code_font())
        welcome.setPlainText(
            "  Welcome to your Custom IDE\n\n"
            "  - Open a folder from the Explorer sidebar.\n"
            "  - Double-click files to open and edit them.\n"
            "  - Use the built-in terminal below to run commands.\n"
            "  - Extensions and RAG integration ready.\n"
        )
        self.addTab(welcome, "Welcome")

    def open_file(self, path: str):
        # Check if already open
        for i in range(self.count()):
            if self.open_files.get(i) == path:
                self.setCurrentIndex(i)
                return

        try:
            content = FileService.read_file(path)
        except Exception as e:
            QMessageBox.warning(self, "Could not open file", str(e))
            return

        editor = QPlainTextEdit()
        editor.setFont(get_code_font())
        editor.setPlainText(content)

        index = self.addTab(editor, os.path.basename(path))
        self.open_files[index] = path
        self.setCurrentIndex(index)
        events.file_opened.emit(path)

    def save_current_file(self):
        index = self.currentIndex()
        path = self.open_files.get(index)
        if not path:
            return None

        editor = self.widget(index)
        try:
            FileService.write_file(path, editor.toPlainText())
            events.file_saved.emit(path)
            return path
        except Exception as e:
            QMessageBox.warning(self, "Could not save file", str(e))
            return None

    def close_tab(self, index: int):
        self.removeTab(index)
        self.open_files.pop(index, None)
        new_open_files = {}
        for old_idx, path in list(self.open_files.items()):
            if old_idx > index:
                new_open_files[old_idx - 1] = path
            elif old_idx < index:
                new_open_files[old_idx] = path
        self.open_files = new_open_files

