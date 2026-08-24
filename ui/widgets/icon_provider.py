from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtWidgets import QFileIconProvider
from PySide6.QtSvg import QSvgRenderer

class MaterialIconProvider(QFileIconProvider):
    """Generates Material-style SVG icons dynamically for file tree views."""
    def __init__(self):
        super().__init__()
        self.cache = {}

    def _make_svg_icon(self, svg_str: str) -> QIcon:
        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer = QSvgRenderer(svg_str.encode("utf-8"))
        renderer.render(painter)
        painter.end()
        return QIcon(pixmap)

    def icon(self, info):
        filename = info.fileName().lower()
        suffix = info.suffix().lower()

        if info.isDir():
            key = "folder"
        elif filename == "package.json":
            key = "npm"
        elif filename in [".gitignore", ".gitattributes"]:
            key = "git"
        elif suffix in ["py", "pyw"]:
            key = "python"
        elif suffix in ["js", "jsx", "mjs"]:
            key = "javascript"
        elif suffix in ["ts", "tsx"]:
            key = "typescript"
        elif suffix in ["html", "htm"]:
            key = "html"
        elif suffix == "css":
            key = "css"
        elif suffix in ["json", "yaml", "yml", "toml"]:
            key = "json"
        elif suffix in ["md", "markdown"]:
            key = "markdown"
        elif suffix in ["png", "jpg", "jpeg", "gif", "svg", "webp"]:
            key = "image"
        else:
            key = "file"

        if key in self.cache:
            return self.cache[key]

        svg_data = self._get_svg_data(key)
        icon = self._make_svg_icon(svg_data)
        self.cache[key] = icon
        return icon

    def _get_svg_data(self, key: str) -> str:
        svgs = {
            "folder": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="#90a4ae" d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/></svg>',
            "python": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="#3776ab" d="M12 2c-5.5 0-5 2.4-5 2.4V7h5v1H5.4S2 7.5 2 13s3.4 5.3 3.4 5.3h2V16s0-2.3 2.3-2.3h4.6s2.3 0 2.3-2.3V6.3S17.5 2 12 2zm-2.3 2.5a.9.9 0 1 1 0 1.8.9.9 0 0 1 0-1.8z"/><path fill="#ffd43b" d="M12 22c5.5 0 5-2.4 5-2.4V17h-5v-1h6.6s3.4.5 3.4-5-3.4-5.3-3.4-5.3h-2V9s0 2.3-2.3 2.3h-4.6S7.4 11.3 7.4 13.6v5.1s-.9 4.3 4.6 4.3zm2.3-2.5a.9.9 0 1 1 0-1.8.9.9 0 0 1 0 1.8z"/></svg>',
            "javascript": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect width="24" height="24" fill="#f7df1e" rx="3"/><path fill="#000" d="M12.8 17.5c.3.5.7.9 1.4.9.7 0 1.1-.3 1.1-.8 0-.5-.4-.7-1.2-1l-.4-.2c-1.2-.5-2-1.1-2-2.4 0-1.3 1-2.3 2.6-2.3 1.2 0 2 .4 2.6 1.4l-1.3.8c-.3-.5-.7-.7-1.3-.7-.5 0-.9.3-.9.7 0 .4.3.6 1 .9l.4.2c1.4.6 2.2 1.2 2.2 2.5 0 1.5-1.2 2.4-2.8 2.4-1.6 0-2.5-.7-3-1.6l1.5-.8zm-5.7.1c.3.5.7.8 1.3.8.6 0 1-.3 1-1.3v-5.4h1.7v5.5c0 1.9-1.1 2.7-2.6 2.7-1.3 0-2.2-.6-2.7-1.6l1.3-.7z"/></svg>',
            "typescript": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect width="24" height="24" fill="#3178c6" rx="3"/><path fill="#fff" d="M14.7 17.5c.3.5.7.9 1.4.9.7 0 1.1-.3 1.1-.8 0-.5-.4-.7-1.2-1l-.4-.2c-1.2-.5-2-1.1-2-2.4 0-1.3 1-2.3 2.6-2.3 1.2 0 2 .4 2.6 1.4l-1.3.8c-.3-.5-.7-.7-1.3-.7-.5 0-.9.3-.9.7 0 .4.3.6 1 .9l.4.2c1.4.6 2.2 1.2 2.2 2.5 0 1.5-1.2 2.4-2.8 2.4-1.6 0-2.5-.7-3-1.6l1.5-.8zM5 13.2h2.5v6.5h1.7v-6.5H12v-1.4H5v1.4z"/></svg>',
            "html": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="#e34f26" d="M1.5 0h21l-1.9 21-8.6 2.4-8.6-2.4L1.5 0zm16.5 6h-12l.3 3.5h8.2l-.4 4.5-3.6 1-3.6-1-.2-2.5H5.2l.4 5 6.4 1.8 6.4-1.8 1.1-10.5z"/></svg>',
            "css": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="#1572b6" d="M1.5 0h21l-1.9 21-8.6 2.4-8.6-2.4L1.5 0zm16.5 6H6l.2 2.5h9.6l-.4 4.5-3.4 1-3.4-1-.2-2.5H6.9l.4 5 4.7 1.3 4.7-1.3.8-9.5z"/></svg>',
            "json": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="#cbd5e1" d="M5 3h2v2H5v4H3V7H1V5h2V3c0-1.1.9-2 2-2zm14 0h-2v2h2v4h2V7h2V5h-2V3c0-1.1-.9-2-2-2zm0 18h-2v-2h2v-4h2v2h2v2h-2v2c0 1.1-.9 2-2 2zM5 21h2v-2H5v-4H3v2H1v2h2v2c0 1.1.9 2 2 2z"/></svg>',
            "markdown": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="#42a5f5" d="M2 4h20c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H2c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2zm2 4v8h2v-4l2.5 3 2.5-3v4h2V8h-2l-3 3.5L5 8H4zm13 0l-3 4h2v4h2v-4h2l-3-4z"/></svg>',
            "git": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="#f05032" d="M21.6 10.9L13.1 2.4c-.6-.6-1.5-.6-2.1 0L8.8 4.6l2.7 2.7c.6-.2 1.3 0 1.7.5.5.5.6 1.2.4 1.8l2.6 2.6c.6-.2 1.3 0 1.8.4.7.7.7 1.8 0 2.5-.7.7-1.8.7-2.5 0-.5-.5-.7-1.3-.4-1.9l-2.4-2.4v5.3c.2.2.3.5.3.8 0 .8-.7 1.5-1.5 1.5s-1.5-.7-1.5-1.5c0-.8.7-1.5 1.5-1.5.3 0 .6.1.8.3V9.7c-.2-.2-.3-.5-.3-.8 0-.6.4-1.2 1-1.4L10.3 5 2.4 12.9c-.6.6-.6 1.5 0 2.1l8.5 8.5c.6.6 1.5.6 2.1 0l8.6-8.5c.6-.6.6-1.6 0-2.1z"/></svg>',
            "npm": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="#cb3837" d="M0 0v24h24V0H0zm18 18h-3V9h-3v9H6V6h12v12z"/></svg>',
            "image": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="#26a69a" d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/></svg>',
            "file": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="#78909c" d="M6 2c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6H6zm7 7V3.5L18.5 9H13z"/></svg>',
        }
        return svgs.get(key, svgs["file"])
