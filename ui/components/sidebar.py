import os
import shutil
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTreeView, 
    QFileSystemModel, QPushButton, QMenu, QMessageBox, QInputDialog
)
from ui.widgets.icon_provider import MaterialIconProvider


class SideBar(QWidget):
    """Explorer sidebar displaying workspace file tree."""
    file_double_clicked = Signal(str)
    choose_folder_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("SideBar")
        self._setup_ui()

    def show_tree_context_menu(self, position):
        index = self.tree.indexAt(position)
        target_dir = self.fs_model.rootPath()
        if index.isValid():
            # User clicked directly on a File or Folder
            item_name = self.fs_model.fileName(index)
            full_path = self.fs_model.filePath(index)
            is_folder = self.fs_model.isDir(index)

            print(f"Clicked on Item: {item_name}")
            print(f"Path: {full_path}")
            print(f"Is Folder: {is_folder}")

        else:
            root_path = self.fs_model.rootPath()
            print(f"Right-clicked empty space. Root folder is: {root_path}")

        menu = QMenu(self)
        new_file_action = menu.addAction("New File")
        new_folder_action = menu.addAction("New Folder")
        menu.addSeparator()

        cut_action = menu.addAction("Cut")
        copy_action = menu.addAction("Copy")
        paste_action = menu.addAction("Paste")
        menu.addSeparator()

        copy_path_action = menu.addAction("Copy Path")
        copy_relative_path_action = menu.addAction("Copy Relative Path")
        menu.addSeparator()

        rename_action = menu.addAction("Rename...")
        delete_action = menu.addAction("Delete")
        menu.addSeparator()

        reveal_in_explorer_action = menu.addAction("Reveal in File Explorer")
        open_in_terminal_action = menu.addAction("Open in Integrated Terminal")



        # Map position to screen coordinates correctly
        global_pos = self.tree.viewport().mapToGlobal(position)
        selected_action = menu.exec(global_pos)

          # FIXED: Removed () from the action variable
        if selected_action == new_file_action:
            print("User clicked 'New File'!")


            # Put your code here to create a new file
            
        elif selected_action == new_folder_action:
            print("User clicked 'New Folder'!")
            
        elif selected_action == delete_action:
            print("User clicked 'Delete'!")
        elif selected_action == rename_action:
            print("Your rename this file")

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.title_label = QLabel("EXPLORER")
        self.title_label.setObjectName("SideBarTitle")
        layout.addWidget(self.title_label)

        self.fs_model = QFileSystemModel()
        self.icon_provider = MaterialIconProvider()

        self.fs_model.setIconProvider(self.icon_provider)
        self.fs_model.setNameFilterDisables(False)
        self.fs_model.setRootPath("")

        self.tree = QTreeView()
        self.tree.setModel(self.fs_model)
        self.tree.setHeaderHidden(True)
        for col in range(1, 4):
            self.tree.hideColumn(col)

        # Context menu setup
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.show_tree_context_menu)
        layout.addWidget(self.tree)

        open_folder_btn = QPushButton("Open Folder")
        open_folder_btn.clicked.connect(self.choose_folder_requested.emit)
        layout.addWidget(open_folder_btn)

    def set_root_path(self, folder_path: str):
        self.fs_model.setRootPath(folder_path)
        self.tree.setRootIndex(self.fs_model.index(folder_path))
        folder_name = os.path.basename(folder_path.rstrip("/\\")).upper() or "EXPLORER"
        self.title_label.setText(folder_name)

    def _on_tree_double_click(self, index):
        path = self.fs_model.filePath(index)
        if not os.path.isdir(path):
            self.file_double_clicked.emit(path)