from PySide6.QtCore import QObject, Signal

class EventBus(QObject):
    """Central event bus for communicating between components & extensions."""
    file_opened = Signal(str)       # Emitted when a file is opened in editor
    file_saved = Signal(str)        # Emitted when a file is saved
    folder_changed = Signal(str)    # Emitted when current workspace directory changes
    log_message = Signal(str)       # Emitted to log messages to the output panel
    rag_query = Signal(str)         # Placeholder for future RAG AI query events

# Global singleton instance of EventBus
events = EventBus()
