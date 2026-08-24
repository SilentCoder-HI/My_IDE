from extensions.base_extension import BaseExtension
from core.event_bus import events

class Extension(BaseExtension):
    def activate(self):
        print("[SampleExtension] Extension activated successfully!")
        events.file_opened.connect(self.on_file_opened)

    def on_file_opened(self, file_path):
        print(f"[SampleExtension] File opened event detected: {file_path}")

    def deactivate(self):
        print("[SampleExtension] Extension deactivated.")
