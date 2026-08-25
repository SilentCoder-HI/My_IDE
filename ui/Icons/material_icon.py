#!/usr/bin/env python3
"""
Material Icon Theme - Memory Loader
Reads material_icons.json and loads all icon data into local memory.
Provides fast lookup for file extensions, filenames, language IDs, and folder names.

Usage:
    from material_icon import MaterialIcons

    icons = MaterialIcons()  # auto-loads from material_icons.json

    # Get icon for a file
    icon = icons.get_file_icon("main.py")        # -> "python"
    icon = icons.get_file_icon("README.md")      # -> "readme"
    icon = icons.get_file_icon("Dockerfile")     # -> "docker"

    # Get icon for a language ID
    icon = icons.get_language_icon("python")     # -> "python"
    icon = icons.get_language_icon("typescript") # -> "typescript"

    # Get icon for a folder
    icon = icons.get_folder_icon("src")          # -> "folder-src"
    icon = icons.get_folder_icon("components")   # -> "folder-components"

    # Get SVG path for an icon name
    svg = icons.get_svg_path("python")           # -> "icons/python.svg"

    # Check if an SVG exists
    icons.has_svg("python")                      # -> True

    # Get all available icons
    all_svgs = icons.all_svg_names()
    all_file = icons.all_file_icon_names()
"""

import json
import os
from typing import Optional


class MaterialIcons:
    """In-memory icon lookup backed by material_icons.json."""

    def __init__(self, json_path: Optional[str] = None):
        if json_path is None:
            # Look in same directory as this file
            json_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "material_icons.json"
            )

        self._json_path = json_path
        self._data = {}
        self._loaded = False
        self.load()

    def load(self):
        """Load icon data from JSON into memory."""
        if self._loaded:
            return

        if not os.path.exists(self._json_path):
            raise FileNotFoundError(
                f"Icon data not found at {self._json_path}. "
                "Run material_icon_extractor.py first."
            )

        with open(self._json_path, "r", encoding="utf-8") as f:
            self._data = json.load(f)

        # Pre-build lookup dicts for fast access
        self._file_ext_lookup = {}       # extension -> default icon_name
        self._file_ext_candidates = {}   # extension -> list of {name, enabledFor?}
        self._file_name_lookup = {}      # filename (lower) -> default icon_name
        self._file_name_candidates = {}  # filename (lower) -> list of {name, enabledFor?}
        self._lang_lookup = {}           # language_id -> icon_name
        self._folder_lookup = {}         # folder_name (lower) -> icon_name

        # File icons lookup (simple + candidates)
        lookup_data = self._data.get("lookup", {})
        self._file_ext_lookup = dict(lookup_data.get("file", {}))
        self._file_ext_candidates = lookup_data.get("fileExtCandidates", {})
        self._file_name_candidates = lookup_data.get("fileNameCandidates", {})

        # Language icons lookup
        for lang in self._data.get("languageIcons", []):
            for lid in lang.get("ids", []):
                self._lang_lookup[lid] = lang["name"]

        # Folder icons lookup (use 'specific' theme - the default)
        for theme in self._data.get("folderIcons", []):
            if theme.get("name") == "specific":
                for fi in theme.get("icons", []):
                    for fn in fi.get("folderNames", []):
                        self._folder_lookup[fn.lower()] = fi["name"]
                break

        # SVG set for fast existence checks
        self._svg_set = set(self._data.get("availableSvgs", []))

        self._loaded = True

    def reload(self):
        """Force reload from disk."""
        self._loaded = False
        self.load()

    # --- File icons ---

    def get_file_icon(self, filename: str, enabled_packs: Optional[set] = None) -> str:
        """
        Get the icon name for a file.

        Args:
            filename: The full filename (e.g., "main.py", "README.md", "Dockerfile")
            enabled_packs: Optional set of enabled icon packs (e.g., {"React", "Vue"}).
                          If None, returns the default icon (first candidate).

        Returns:
            Icon name string (e.g., "python", "readme", "docker")
        """
        name_lower = filename.lower()

        # Check exact filename match first
        if name_lower in self._file_name_candidates:
            return self._resolve_candidate(
                self._file_name_candidates[name_lower], enabled_packs
            )

        # Extract extension and check
        if "." in filename:
            parts = filename.rsplit(".", 1)
            ext = parts[1].lower()
            if ext in self._file_ext_candidates:
                return self._resolve_candidate(
                    self._file_ext_candidates[ext], enabled_packs
                )

        # Default
        return self._data.get("lookup", {}).get("defaultFileIcon", "file")

    def _resolve_candidate(self, candidates, enabled_packs=None):
        """Pick the best icon from a list of candidates.

        If enabled_packs is provided, finds the first candidate whose
        enabledFor matches an enabled pack. Falls back to the first
        candidate (the default, no enabledFor).
        """
        if not candidates:
            return "file"

        if enabled_packs is None:
            return candidates[0]["name"]

        # Find framework-specific match
        for c in candidates:
            packs = c.get("enabledFor")
            if packs and any(p in enabled_packs for p in packs):
                return c["name"]

        # Fall back to default (no enabledFor)
        for c in candidates:
            if "enabledFor" not in c:
                return c["name"]

        return candidates[0]["name"]

    def get_file_icon_by_ext(self, extension: str) -> str:
        """Get icon name by file extension (without dot)."""
        return self._file_ext_lookup.get(extension.lower(), "file")

    # --- Language icons ---

    def get_language_icon(self, language_id: str) -> Optional[str]:
        """
        Get the icon name for a language ID.

        Args:
            language_id: The VS Code language ID (e.g., "python", "typescript")

        Returns:
            Icon name string or None
        """
        return self._lang_lookup.get(language_id)

    # --- Folder icons ---

    def get_folder_icon(self, folder_name: str) -> str:
        """
        Get the icon name for a folder.

        Args:
            folder_name: The folder name (e.g., "src", "components", "node_modules")

        Returns:
            Icon name string (e.g., "folder-src", "folder-components")
        """
        name_lower = folder_name.lower()
        return self._folder_lookup.get(name_lower, "folder")

    # --- SVG helpers ---

    def get_svg_path(self, icon_name: str) -> Optional[str]:
        """
        Get the relative SVG file path for an icon name.

        Args:
            icon_name: Icon name (e.g., "python", "folder-src")

        Returns:
            Relative path like "icons/python.svg" or None if not found
        """
        # Folder icons use the base name without "folder-" prefix
        svg_name = icon_name
        if self.has_svg(icon_name):
            return os.path.join("vscode-material-icon-theme", "icons", f"{icon_name}.svg")

        # Try without folder prefix for folder icons
        if icon_name.startswith("folder-"):
            base = icon_name[7:]  # remove "folder-"
            if base in self._svg_set:
                return os.path.join("vscode-material-icon-theme", "icons", f"{base}.svg")

        return None

    def get_svg_bytes(self, icon_name: str) -> Optional[bytes]:
        """
        Read and return the raw SVG content for an icon.

        Args:
            icon_name: Icon name (e.g., "python")

        Returns:
            SVG content as bytes, or None
        """
        svg_path = self.get_svg_path(icon_name)
        if svg_path is None:
            return None

        # Resolve relative to the JSON file location
        base_dir = os.path.dirname(self._json_path)
        full_path = os.path.join(base_dir, svg_path)

        if not os.path.exists(full_path):
            return None

        with open(full_path, "rb") as f:
            return f.read()

    def has_svg(self, icon_name: str) -> bool:
        """Check if an SVG file exists for this icon name."""
        return icon_name in self._svg_set

    # --- Bulk accessors ---

    def all_svg_names(self) -> list:
        """Return list of all available SVG icon names."""
        return list(self._svg_set)

    def all_file_icon_names(self) -> list:
        """Return list of all file icon names."""
        return list(self._data.get("fileIcons", {}).keys())

    def all_language_icon_names(self) -> list:
        """Return list of all language icon names."""
        return [lang["name"] for lang in self._data.get("languageIcons", [])]

    def all_folder_icon_names(self) -> list:
        """Return list of all folder icon names (specific theme)."""
        for theme in self._data.get("folderIcons", []):
            if theme.get("name") == "specific":
                return [fi["name"] for fi in theme.get("icons", [])]
        return []

    # --- Metadata ---

    @property
    def meta(self) -> dict:
        """Return metadata about the loaded icon set."""
        return self._data.get("meta", {})

    @property
    def default_file_icon(self) -> str:
        return "file"

    @property
    def default_folder_icon(self) -> str:
        return "folder"

    def __repr__(self):
        m = self.meta
        return (
            f"MaterialIcons("
            f"file={m.get('totalFileIcons', '?')}, "
            f"lang={m.get('totalLanguageIcons', '?')}, "
            f"folder={m.get('totalFolderIcons', '?')}, "
            f"svg={m.get('totalSvgFiles', '?')})"
        )

    def __len__(self):
        return (
            self.meta.get("totalFileIcons", 0)
            + self.meta.get("totalLanguageIcons", 0)
            + self.meta.get("totalFolderIcons", 0)
        )


# --- Standalone helper functions (no class needed) ---

_instance: Optional[MaterialIcons] = None


def _get_instance() -> MaterialIcons:
    global _instance
    if _instance is None:
        _instance = MaterialIcons()
    return _instance


def get_file_icon(filename: str) -> str:
    """Quick helper: get icon name for a file."""
    return _get_instance().get_file_icon(filename)


def get_language_icon(language_id: str) -> Optional[str]:
    """Quick helper: get icon name for a language."""
    return _get_instance().get_language_icon(language_id)


def get_folder_icon(folder_name: str) -> str:
    """Quick helper: get icon name for a folder."""
    return _get_instance().get_folder_icon(folder_name)


if __name__ == "__main__":
    icons = MaterialIcons()
    print(icons)
    print()

    # Demo lookups
    test_files = [
        "main.py", "README.md", "Dockerfile", "index.tsx", "style.css",
        "package.json", "Makefile", "Cargo.toml", "go.mod", "app.vue",
        "nginx.conf", "docker-compose.yml", "jest.config.js",
    ]
    print("--- File Icon Lookups ---")
    for f in test_files:
        icon = icons.get_file_icon(f)
        svg = icons.get_svg_path(icon)
        print(f"  {f:35s} -> {icon:30s} ({svg})")

    print()
    print("--- Language Icon Lookups ---")
    test_langs = ["python", "typescript", "rust", "go", "java", "html", "css", "dockerfile"]
    for lang in test_langs:
        icon = icons.get_language_icon(lang)
        print(f"  {lang:20s} -> {icon}")

    print()
    print("--- Folder Icon Lookups ---")
    test_folders = ["src", "components", "node_modules", "dist", "test", ".git", "docs", "api"]
    for folder in test_folders:
        icon = icons.get_folder_icon(folder)
        print(f"  {folder:20s} -> {icon}")
