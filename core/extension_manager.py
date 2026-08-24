import os
import json
import importlib.util
from typing import Dict, Any

class ExtensionManager:
    """Discovers, loads, and manages IDE extensions/plugins."""
    def __init__(self, extensions_dir: str, app_api: Any):
        self.extensions_dir = extensions_dir
        self.app_api = app_api
        self.loaded_extensions: Dict[str, Any] = {}

    def discover_and_load_all(self):
        """Scans extension directory and activates extensions."""
        if not os.path.exists(self.extensions_dir):
            return

        for item in os.listdir(self.extensions_dir):
            ext_path = os.path.join(self.extensions_dir, item)
            manifest_path = os.path.join(ext_path, "extension.json")
            entry_path = os.path.join(ext_path, "main.py")

            if os.path.isdir(ext_path) and os.path.exists(manifest_path) and os.path.exists(entry_path):
                try:
                    self._load_extension(item, manifest_path, entry_path)
                except Exception as e:
                    print(f"[ExtensionManager] Failed to load '{item}': {e}")

    def _load_extension(self, ext_id: str, manifest_path: str, entry_path: str):
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        spec = importlib.util.spec_from_file_location(f"ext_{ext_id}", entry_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Instantiates Extension class if available
            if hasattr(module, "Extension"):
                instance = module.Extension(self.app_api)
                instance.activate()
                self.loaded_extensions[ext_id] = {
                    "manifest": manifest,
                    "instance": instance
                }
                print(f"[ExtensionManager] Activated extension: {manifest.get('name', ext_id)}")
