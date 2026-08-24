import os
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QSplitter, QHBoxLayout, QFileDialog
)

from config import DEFAULT_DIR
from ui.styles.dark_plus import STYLESHEET
from ui.components.activity_bar import ActivityBar
from ui.components.sidebar import SideBar
from ui.components.editor_area import EditorArea
from ui.components.bottom_panel import BottomPanel
from ui.components.status_bar import StatusBar
from core.extension_manager import ExtensionManager
from core.event_bus import events

class MainWindow(QMainWindow):
    """Main window shell assembling IDE layout and splitters."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Agent IDE")
        self.resize(1400, 850)

        self.current_dir = DEFAULT_DIR
        self._build_ui()
        self.setStyleSheet(STYLESHEET)

        # Initialize Extension Manager
        ext_dir = os.path.join(os.path.dirname(__file__), "..", "extensions")
        self.extension_manager = ExtensionManager(ext_dir, app_api=self)
        self.extension_manager.discover_and_load_all()

        # Set initial folder
        self._set_root_dir(self.current_dir)

    def _build_ui(self):
        central = QWidget()
        outer_layout = QHBoxLayout(central)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        # Activity Bar
        self.activity_bar = ActivityBar()
        self.activity_bar.toggle_explorer.connect(self.toggle_sidebar)
        outer_layout.addWidget(self.activity_bar)

        # Horizontal Splitter (Sidebar + Editor Area)
        self.h_splitter = QSplitter(Qt.Horizontal)

        # Sidebar
        self.sidebar = SideBar()
        self.sidebar.file_double_clicked.connect(self.open_file)
        self.sidebar.choose_folder_requested.connect(self.choose_folder)
        self.h_splitter.addWidget(self.sidebar)

        # Vertical Splitter (Editor Area + Bottom Panel)
        self.v_splitter = QSplitter(Qt.Vertical)
        self.editor_area = EditorArea()
        self.bottom_panel = BottomPanel(get_cwd=lambda: self.current_dir)

        self.v_splitter.addWidget(self.editor_area)
        self.v_splitter.addWidget(self.bottom_panel)
        self.v_splitter.setStretchFactor(0, 3)
        self.v_splitter.setStretchFactor(1, 2)
        self.v_splitter.setSizes([550, 250])

        self.h_splitter.addWidget(self.v_splitter)
        self.h_splitter.setStretchFactor(0, 0)
        self.h_splitter.setStretchFactor(1, 1)
        self.h_splitter.setSizes([260, 1140])

        outer_layout.addWidget(self.h_splitter)
        self.setCentralWidget(central)

        # Status bar
        self.status_bar = StatusBar(self.current_dir)
        self.setStatusBar(self.status_bar)

        # Build menu bar after widgets are initialized
        self._build_menu_bar()


    def _build_menu_bar(self):
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("&File")
        open_folder_act = QAction("Open Folder…", self)
        open_folder_act.triggered.connect(self.choose_folder)
        file_menu.addAction(open_folder_act)

        save_act = QAction("Save", self)
        save_act.setShortcut(QKeySequence.Save)
        save_act.triggered.connect(self.save_current_file)
        file_menu.addAction(save_act)

        file_menu.addSeparator()
        exit_act = QAction("Exit", self)
        exit_act.triggered.connect(self.close)
        file_menu.addAction(exit_act)

        # View Menu
        view_menu = menubar.addMenu("&View")
        toggle_sidebar_act = QAction("Toggle Sidebar", self)
        toggle_sidebar_act.triggered.connect(self.toggle_sidebar)
        view_menu.addAction(toggle_sidebar_act)

        toggle_panel_act = QAction("Toggle Panel", self)
        toggle_panel_act.triggered.connect(self.toggle_panel)
        view_menu.addAction(toggle_panel_act)

        # Terminal Menu
        terminal_menu = menubar.addMenu("&Terminal")
        new_terminal_act = QAction("New Terminal", self)
        new_terminal_act.setShortcut("Ctrl+`")
        new_terminal_act.triggered.connect(self.bottom_panel.focus_terminal)
        terminal_menu.addAction(new_terminal_act)

    def _set_root_dir(self, folder: str):
        self.current_dir = folder
        self.sidebar.set_root_path(folder)
        self.status_bar.update_dir(folder)
        self.setWindowTitle(f"{os.path.basename(folder) or folder} — My Agent IDE")
        events.folder_changed.emit(folder)

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Open Folder", self.current_dir)
        if folder:
            self._set_root_dir(folder)
            self.bottom_panel.log(f"[Workspace folder set to: {self.current_dir}]")

    def open_file(self, path: str):
        self.editor_area.open_file(path)

    def save_current_file(self):
        saved_path = self.editor_area.save_current_file()
        if saved_path:
            self.statusBar().showMessage(f"Saved {os.path.basename(saved_path)}", 3000)

    def toggle_sidebar(self):
        self.sidebar.setVisible(not self.sidebar.isVisible())

    def toggle_panel(self):
        self.bottom_panel.setVisible(not self.bottom_panel.isVisible())
