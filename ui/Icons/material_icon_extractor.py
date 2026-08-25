#!/usr/bin/env python3
"""
Material Icon Theme - Icon Data Extractor
Reads the VS Code Material Icon Theme repo and extracts all icon mappings
into a single JSON file for use in other IDEs.
"""

import json
import os
import re
import sys

REPO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vscode-material-icon-theme")
OUTPUT_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "material_icons.json")


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_list_from_brackets(text, start_idx):
    """Extract a list of strings from [...] starting at start_idx."""
    if start_idx >= len(text) or text[start_idx] != "[":
        return [], start_idx
    depth = 0
    i = start_idx
    while i < len(text):
        if text[i] == "[":
            depth += 1
        elif text[i] == "]":
            depth -= 1
            if depth == 0:
                return text[start_idx:i+1], i+1
        i += 1
    return text[start_idx:], len(text)


def parse_string_list(text):
    """Parse a list like ['a', 'b', 'c'] into Python list."""
    text = text.strip()
    if not text.startswith("[") or not text.endswith("]"):
        return []
    inner = text[1:-1].strip()
    if not inner:
        return []
    return [s.strip().strip("'\"") for s in inner.split(",") if s.strip().strip("'\"")]


def extract_file_icons(filepath):
    """Extract file icon definitions from fileIcons.ts"""
    content = read_file(filepath)
    icons = {}

    # Find all icon blocks: { name: 'xxx', fileExtensions: [...], fileNames: [...] }
    # We parse each icon entry between { and }
    # Remove comments
    content = re.sub(r'//.*?\n', '\n', content)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    # Find the icons array start
    match = re.search(r'icons:\s*parseByPattern\(\[', content)
    if not match:
        return icons

    start = match.end()
    # Now find matching ]
    depth = 1
    i = start
    while i < len(content) and depth > 0:
        if content[i] == '[':
            depth += 1
        elif content[i] == ']':
            depth -= 1
        i += 1

    block = content[start:i-1]

    # Split by top-level { ... } blocks
    icon_entries = []
    depth = 0
    current_start = None
    for idx, ch in enumerate(block):
        if ch == '{':
            if depth == 0:
                current_start = idx
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0 and current_start is not None:
                icon_entries.append(block[current_start:idx+1])
                current_start = None

    for entry in icon_entries:
        icon = parse_icon_entry(entry)
        if icon and icon.get("name"):
            icons[icon["name"]] = icon

    return icons


def parse_icon_entry(entry):
    """Parse a single icon definition block."""
    icon = {}

    # Extract name
    name_match = re.search(r"name:\s*['\"]([^'\"]+)['\"]", entry)
    if not name_match:
        return None
    icon["name"] = name_match.group(1)

    # Extract fileExtensions
    ext_match = re.search(r'fileExtensions:\s*\[([^\]]*)\]', entry)
    if ext_match:
        icon["fileExtensions"] = parse_string_list("[" + ext_match.group(1) + "]")

    # Extract fileNames
    fname_match = re.search(r'fileNames:\s*\[([^\]]*)\]', entry)
    if fname_match:
        icon["fileNames"] = parse_string_list("[" + fname_match.group(1) + "]")

    # Extract patterns
    pat_match = re.search(r'patterns:\s*\{([^}]*)\}', entry)
    if pat_match:
        patterns = {}
        for m in re.finditer(r"['\"]?(\w[\w.-]*)['\"]?\s*:\s*FileNamePattern\.\w+", pat_match.group(1)):
            patterns[m.group(1)] = True
        if patterns:
            icon["patterns"] = patterns

    # Light theme indicator
    if re.search(r'light:\s*true', entry):
        icon["light"] = True

    # Clone info
    clone_match = re.search(r'clone:\s*\{([^}]+)\}', entry)
    if clone_match:
        base_match = re.search(r"base:\s*['\"]([^'\"]+)['\"]", clone_match.group(1))
        color_match = re.search(r"color:\s*['\"]([^'\"]+)['\"]", clone_match.group(1))
        if base_match:
            icon["clone"] = {
                "base": base_match.group(1),
                "color": color_match.group(1) if color_match else None
            }

    # Enabled for icon packs
    enabled_match = re.search(r'enabledFor:\s*\[([^\]]*)\]', entry)
    if enabled_match:
        packs = [s.strip().strip("'\"") for s in enabled_match.group(1).split(",") if s.strip()]
        icon["enabledFor"] = packs

    return icon


def extract_language_icons(filepath):
    """Extract language icon definitions from languageIcons.ts"""
    content = read_file(filepath)
    icons = []

    content = re.sub(r'//.*?\n', '\n', content)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    # Find the array start
    match = re.search(r'export\s+const\s+languageIcons\s*:\s*LanguageIcon\[\]\s*=\s*\[', content)
    if not match:
        return icons

    start = match.end()
    depth = 1
    i = start
    while i < len(content) and depth > 0:
        if content[i] == '[':
            depth += 1
        elif content[i] == ']':
            depth -= 1
        i += 1

    block = content[start:i-1]

    # Split by top-level { ... } entries
    entries = []
    depth = 0
    current_start = None
    for idx, ch in enumerate(block):
        if ch == '{':
            if depth == 0:
                current_start = idx
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0 and current_start is not None:
                entries.append(block[current_start:idx+1])
                current_start = None

    for entry in entries:
        icon = {}
        name_match = re.search(r"name:\s*['\"]([^'\"]+)['\"]", entry)
        if not name_match:
            continue
        icon["name"] = name_match.group(1)

        ids_match = re.search(r'ids:\s*\[([^\]]*)\]', entry)
        if ids_match:
            inner = ids_match.group(1).strip()
            if inner:
                icon["ids"] = [s.strip().strip("'\"") for s in inner.split(",") if s.strip()]
            else:
                icon["ids"] = []
        else:
            icon["ids"] = []

        if re.search(r'light:\s*true', entry):
            icon["light"] = True

        clone_match = re.search(r'clone:\s*\{([^}]+)\}', entry)
        if clone_match:
            base_match = re.search(r"base:\s*['\"]([^'\"]+)['\"]", clone_match.group(1))
            color_match = re.search(r"color:\s*['\"]([^'\"]+)['\"]", clone_match.group(1))
            if base_match:
                icon["clone"] = {
                    "base": base_match.group(1),
                    "color": color_match.group(1) if color_match else None
                }

        icons.append(icon)

    return icons


def extract_folder_icons(filepath):
    """Extract folder icon definitions from folderIcons.ts"""
    content = read_file(filepath)
    themes = []

    content = re.sub(r'//.*?\n', '\n', content)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    match = re.search(r'export\s+const\s+folderIcons\s*:\s*FolderTheme\[\]\s*=\s*\[', content)
    if not match:
        return themes

    start = match.end()
    depth = 1
    i = start
    while i < len(content) and depth > 0:
        if content[i] == '[':
            depth += 1
        elif content[i] == ']':
            depth -= 1
        i += 1

    block = content[start:i-1]

    # Split into theme blocks at top level
    theme_entries = []
    depth = 0
    current_start = None
    for idx, ch in enumerate(block):
        if ch == '{':
            if depth == 0:
                current_start = idx
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0 and current_start is not None:
                theme_entries.append(block[current_start:idx+1])
                current_start = None

    for theme_entry in theme_entries:
        theme = {}
        name_match = re.search(r"name:\s*['\"]([^'\"]+)['\"]", theme_entry)
        if name_match:
            theme["name"] = name_match.group(1)
        else:
            continue

        # Default icon
        def_match = re.search(r'defaultIcon:\s*\{[^}]*name:\s*[\'"]([^\'"]+)[\'"]', theme_entry)
        if def_match:
            theme["defaultIcon"] = def_match.group(1)

        # Root folder
        root_match = re.search(r'rootFolder:\s*\{[^}]*name:\s*[\'"]([^\'"]+)[\'"]', theme_entry)
        if root_match:
            theme["rootFolder"] = root_match.group(1)

        # Icons array
        icons_match = re.search(r'icons:\s*\[', theme_entry)
        if icons_match:
            inner_start = icons_match.end()
            depth2 = 1
            j = inner_start
            while j < len(theme_entry) and depth2 > 0:
                if theme_entry[j] == '[':
                    depth2 += 1
                elif theme_entry[j] == ']':
                    depth2 -= 1
                j += 1

            icons_block = theme_entry[inner_start:j-1]

            folder_icon_entries = []
            depth3 = 0
            cs = None
            for idx2, ch2 in enumerate(icons_block):
                if ch2 == '{':
                    if depth3 == 0:
                        cs = idx2
                    depth3 += 1
                elif ch2 == '}':
                    depth3 -= 1
                    if depth3 == 0 and cs is not None:
                        folder_icon_entries.append(icons_block[cs:idx2+1])
                        cs = None

            folder_icons = []
            for fic in folder_icon_entries:
                fi = {}
                fi_name = re.search(r"name:\s*['\"]([^'\"]+)['\"]", fic)
                if fi_name:
                    fi["name"] = fi_name.group(1)

                fn_match = re.search(r'folderNames:\s*\[([^\]]*)\]', fic)
                if fn_match:
                    fi["folderNames"] = parse_string_list("[" + fn_match.group(1) + "]")

                if re.search(r'light:\s*true', fic):
                    fi["light"] = True

                clone_match = re.search(r'clone:\s*\{([^}]+)\}', fic)
                if clone_match:
                    base_m = re.search(r"base:\s*['\"]([^'\"]+)['\"]", clone_match.group(1))
                    color_m = re.search(r"color:\s*['\"]([^'\"]+)['\"]", clone_match.group(1))
                    if base_m:
                        fi["clone"] = {
                            "base": base_m.group(1),
                            "color": color_m.group(1) if color_m else None
                        }

                enabled_match = re.search(r'enabledFor:\s*\[([^\]]*)\]', fic)
                if enabled_match:
                    packs = [s.strip().strip("'\"") for s in enabled_match.group(1).split(",") if s.strip()]
                    fi["enabledFor"] = packs

                folder_icons.append(fi)

            theme["icons"] = folder_icons

        themes.append(theme)

    return themes


def get_svg_icons():
    """List all available SVG icon names."""
    icons_dir = os.path.join(REPO_PATH, "icons")
    if not os.path.isdir(icons_dir):
        return []
    svgs = []
    for f in sorted(os.listdir(icons_dir)):
        if f.endswith(".svg"):
            svgs.append(f[:-4])  # remove .svg
    return svgs


def build_lookup_tables(file_icons, language_icons, folder_themes):
    """Build fast lookup tables for the IDE.

    When multiple icons claim the same extension/filename, we store a list.
    The first entry (no enabledFor) is the default; others are framework-specific.
    """
    # extension -> list of icon candidates (first is default)
    file_ext_lookup = {}
    # filename (lower) -> list of icon candidates
    file_name_lookup = {}

    for icon_name, icon_data in file_icons.items():
        has_enabled = "enabledFor" in icon_data
        if "fileExtensions" in icon_data:
            for ext in icon_data["fileExtensions"]:
                if ext not in file_ext_lookup:
                    file_ext_lookup[ext] = []
                entry = {"name": icon_name}
                if has_enabled:
                    entry["enabledFor"] = icon_data["enabledFor"]
                file_ext_lookup[ext].append(entry)
        if "fileNames" in icon_data:
            for fname in icon_data["fileNames"]:
                key = fname.lower()
                if key not in file_name_lookup:
                    file_name_lookup[key] = []
                entry = {"name": icon_name}
                if has_enabled:
                    entry["enabledFor"] = icon_data["enabledFor"]
                file_name_lookup[key].append(entry)

    # Flatten to simple lookup: pick first candidate (the default)
    file_lookup = {}
    for ext, candidates in file_ext_lookup.items():
        file_lookup[ext] = candidates[0]["name"]
    for fname, candidates in file_name_lookup.items():
        file_lookup[fname] = candidates[0]["name"]

    # Also store full candidate lists for pack-aware resolution
    file_ext_candidates = file_ext_lookup
    file_name_candidates = file_name_lookup

    # language id -> icon name
    lang_lookup = {}
    for lang in language_icons:
        if "ids" in lang:
            for lid in lang["ids"]:
                lang_lookup[lid] = lang["name"]

    # folder name -> icon name (for 'specific' theme which is the default)
    folder_lookup = {}
    default_folder_icon = "folder"
    for theme in folder_themes:
        if theme["name"] == "specific":
            for fi in theme.get("icons", []):
                if "folderNames" in fi:
                    for fn in fi["folderNames"]:
                        folder_lookup[fn.lower()] = fi["name"]
            break

    return {
        "defaultFileIcon": "file",
        "defaultFolderIcon": default_folder_icon,
        "file": file_lookup,
        "fileExtCandidates": file_ext_candidates,
        "fileNameCandidates": file_name_candidates,
        "language": lang_lookup,
        "folder": folder_lookup,
    }


def main():
    print("=== Material Icon Theme Extractor ===")
    print(f"Repo path: {REPO_PATH}")

    if not os.path.isdir(REPO_PATH):
        print(f"ERROR: Repo not found at {REPO_PATH}")
        print("Clone it first: git clone https://github.com/material-extensions/vscode-material-icon-theme.git")
        sys.exit(1)

    file_icons_path = os.path.join(REPO_PATH, "src", "core", "icons", "fileIcons.ts")
    lang_icons_path = os.path.join(REPO_PATH, "src", "core", "icons", "languageIcons.ts")
    folder_icons_path = os.path.join(REPO_PATH, "src", "core", "icons", "folderIcons.ts")

    print("Extracting file icons...")
    file_icons = extract_file_icons(file_icons_path)
    print(f"  -> {len(file_icons)} file icons")

    print("Extracting language icons...")
    language_icons = extract_language_icons(lang_icons_path)
    print(f"  -> {len(language_icons)} language icons")

    print("Extracting folder icons...")
    folder_themes = extract_folder_icons(folder_icons_path)
    total_folder_icons = sum(len(t.get("icons", [])) for t in folder_themes)
    print(f"  -> {len(folder_themes)} folder themes, {total_folder_icons} folder icons")

    print("Listing SVG files...")
    svg_names = get_svg_icons()
    print(f"  -> {len(svg_names)} SVG files")

    print("Building lookup tables...")
    lookup = build_lookup_tables(file_icons, language_icons, folder_themes)
    print(f"  -> {len(lookup['file'])} file lookups, {len(lookup['language'])} language lookups, {len(lookup['folder'])} folder lookups")

    data = {
        "meta": {
            "source": "vscode-material-icon-theme",
            "version": "extracted",
            "totalFileIcons": len(file_icons),
            "totalLanguageIcons": len(language_icons),
            "totalFolderIcons": total_folder_icons,
            "totalSvgFiles": len(svg_names),
        },
        "fileIcons": file_icons,
        "languageIcons": language_icons,
        "folderIcons": folder_themes,
        "availableSvgs": svg_names,
        "lookup": lookup,
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\nDone! Output: {OUTPUT_JSON}")
    print(f"File size: {os.path.getsize(OUTPUT_JSON) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
