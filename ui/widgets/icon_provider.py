from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor
from PySide6.QtWidgets import QFileIconProvider
from PySide6.QtSvg import QSvgRenderer

from ui.Icons.material_icon import MaterialIcons

_DEFAULT_FOLDER_SVG = b'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
<path fill="#FFCA28" d="M10 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/>
</svg>'''

_DEFAULT_FILE_SVG = b'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
<path fill="#90A4AE" d="M14 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8l-6-6zm4 18H6V4h7v5h5v11z"/>
</svg>'''


class MaterialIconProvider(QFileIconProvider):
    """QFileIconProvider backed by the MaterialIcons lookup system."""

    def __init__(self):
        super().__init__()
        self._icons = MaterialIcons()
        self._cache: dict[str, QIcon] = {}

    @staticmethod
    def _make_svg_icon(svg_bytes: bytes) -> QIcon:
        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer = QSvgRenderer(svg_bytes)
        renderer.render(painter)
        painter.end()
        return QIcon(pixmap)

    def icon(self, info):
        if info.isDir():
            icon_name = self._icons.get_folder_icon(info.fileName())
            cache_key = f"folder:{icon_name}"
        else:
            icon_name = self._icons.get_file_icon(info.fileName())
            cache_key = f"file:{icon_name}"

        if cache_key in self._cache:
            return self._cache[cache_key]

        svg_bytes = self._icons.get_svg_bytes(icon_name)
        if svg_bytes is None:
            if info.isDir():
                svg_bytes = _DEFAULT_FOLDER_SVG
            else:
                svg_bytes = _DEFAULT_FILE_SVG

        icon = self._make_svg_icon(svg_bytes)
        self._cache[cache_key] = icon
        return icon
