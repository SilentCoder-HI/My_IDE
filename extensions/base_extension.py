from abc import ABC, abstractmethod

class BaseExtension(ABC):
    """Abstract Base Class that every extension must inherit from."""
    def __init__(self, api):
        self.api = api

    @abstractmethod
    def activate(self):
        """Called when the extension is loaded by ExtensionManager."""
        pass

    def deactivate(self):
        """Called when the extension is unloaded or app shuts down."""
        pass
