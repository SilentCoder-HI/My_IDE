# VS Code "Dark+" color palette and stylesheet

COLORS = {
    "bg":            "#1e1e1e",   # editor background
    "bg_light":      "#252526",   # sidebar / panel background
    "bg_lighter":    "#2d2d2d",   # inactive tab
    "activity_bar":  "#333333",
    "border":        "#3c3c3c",
    "text":          "#cccccc",
    "text_dim":      "#8a8a8a",
    "accent":        "#007acc",   # status bar blue
    "accent_hover":  "#094771",
    "selection":     "#264f78",
}

STYLESHEET = f"""
QMainWindow {{
    background-color: {COLORS['bg']};
}}
QWidget {{
    background-color: {COLORS['bg']};
    color: {COLORS['text']};
    font-size: 13px;
}}
QMenuBar {{
    background-color: {COLORS['bg_light']};
    color: {COLORS['text']};
    border-bottom: 1px solid {COLORS['border']};
    padding: 2px;
}}
QMenuBar::item:selected {{
    background-color: {COLORS['selection']};
}}
QMenu {{
    background-color: {COLORS['bg_light']};
    color: {COLORS['text']};
    border: 1px solid {COLORS['border']};
}}
QMenu::item:selected {{
    background-color: {COLORS['selection']};
}}

/* Activity bar */
QWidget#ActivityBar {{
    background-color: {COLORS['activity_bar']};
    border-right: 1px solid {COLORS['border']};
}}
QToolButton#ActivityBtn {{
    background: transparent;
    border: none;
    color: {COLORS['text_dim']};
    padding: 12px 0px;
}}
QToolButton#ActivityBtn:checked {{
    color: {COLORS['text']};
    border-left: 2px solid {COLORS['accent']};
}}
QToolButton#ActivityBtn:hover {{
    color: {COLORS['text']};
}}

/* Sidebar */
QWidget#SideBar {{
    background-color: {COLORS['bg_light']};
}}
QLabel#SideBarTitle {{
    color: {COLORS['text_dim']};
    font-size: 11px;
    font-weight: bold;
    padding: 8px 12px 4px 12px;
    letter-spacing: 1px;
}}
QTreeView {{
    background-color: {COLORS['bg_light']};
    border: none;
    show-decoration-selected: 1;
}}
QTreeView::item {{
    padding: 2px;
}}
QTreeView::item:selected {{
    background-color: {COLORS['selection']};
}}
QTreeView::item:hover {{
    background-color: #2a2d2e;
}}
QHeaderView::section {{
    background-color: {COLORS['bg_light']};
    border: none;
    color: {COLORS['text_dim']};
}}

/* Editor tabs */
QTabWidget::pane {{
    border: none;
    background-color: {COLORS['bg']};
}}
QTabBar::tab {{
    background-color: {COLORS['bg_lighter']};
    color: {COLORS['text_dim']};
    padding: 6px 16px;
    border-right: 1px solid {COLORS['border']};
}}
QTabBar::tab:selected {{
    background-color: {COLORS['bg']};
    color: {COLORS['text']};
    border-top: 1px solid {COLORS['accent']};
}}
QPlainTextEdit, QTextEdit {{
    background-color: {COLORS['bg']};
    color: {COLORS['text']};
    border: none;
    selection-background-color: {COLORS['selection']};
}}

/* Bottom panel */
QWidget#BottomPanel {{
    background-color: {COLORS['bg']};
    border-top: 1px solid {COLORS['border']};
}}
QLineEdit {{
    background-color: {COLORS['bg']};
    color: {COLORS['text']};
    border: 1px solid {COLORS['border']};
    padding: 4px;
}}
QPushButton {{
    background-color: {COLORS['bg_lighter']};
    border: 1px solid {COLORS['border']};
    padding: 4px 10px;
}}
QPushButton:hover {{
    background-color: {COLORS['selection']};
}}

/* Status bar */
QStatusBar {{
    background-color: {COLORS['accent']};
    color: white;
}}
QStatusBar QLabel {{
    color: white;
    padding: 0 8px;
}}
QSplitter::handle {{
    background-color: {COLORS['border']};
}}
QSplitter::handle:horizontal {{ width: 1px; }}
QSplitter::handle:vertical {{ height: 1px; }}
"""
