import os
from PySide6.QtGui import QFont

# Default directory
DEFAULT_DIR = os.path.expanduser("/home/system/A.projects/Testing")
if not os.path.isdir(DEFAULT_DIR):
    DEFAULT_DIR = os.getcwd()

_CODE_FONT = None

def get_code_font():
    global _CODE_FONT
    if _CODE_FONT is None:
        font = QFont("Cascadia Code", 10)
        if not font.exactMatch():
            font = QFont("Consolas", 10)
        _CODE_FONT = font
    return _CODE_FONT
