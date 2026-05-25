"""
Icon Infrastructure Tests

Verifies that the icon configuration in the AGS control panel
correctly points to valid icon files on the filesystem.

Following TDD: write failing test first, then fix the code.
"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
APP_TSX = PROJECT_ROOT / "app.tsx"
ICONS_DIR = PROJECT_ROOT / "icons"


# ---- All icon names referenced in the codebase ----
# Extracted from .tsx files in src/ and widget/
STATIC_ICON_NAMES = {
    # Custom project icons (in icons/hicolor/scalable/status/)
    "claude-ai-symbolic",
    "openai-symbolic",
    "ollama-symbolic",
    "opencode-symbolic",
    "anthropic-symbolic",
    "ram-symbolic",
    "battery-bolt-symbolic",
    "hourglass-symbolic",
    "wattage-symbolic",
    # xsi-* system icons (from /usr/share/icons/hicolor/scalable/actions/)
    "xsi-bluetooth-active-symbolic",
    "xsi-bluetooth-disabled-symbolic",
    "xsi-network-wireless-signal-excellent-symbolic",
    "xsi-network-wireless-offline-symbolic",
    "xsi-weather-clear-night-symbolic",
    "xsi-weather-clear-symbolic",
    "xsi-notifications-disabled-symbolic",
    "xsi-notifications-symbolic",
    "xsi-microphone-sensitivity-muted-symbolic",
    "xsi-audio-input-microphone-symbolic",
    "xsi-software-update-available-symbolic",
    "xsi-cpu-symbolic",
    "xsi-drive-harddisk-symbolic",
    "xsi-audio-volume-high-symbolic",
    "xsi-display-brightness-symbolic",
    "xsi-shutdown-symbolic",
    "xsi-power-profile-power-saver-symbolic",
    "xsi-power-profile-balanced-symbolic",
    "xsi-power-profile-performance-symbolic",
    # Other system theme icons
    "media-playback-pause-symbolic",
    "media-playback-stop-symbolic",
    "view-refresh-symbolic",
    # Battery fallback
    "battery-missing-symbolic",
}

# ---- Provider keys from usage-limits --json ----
# These are all known LLM provider identifiers that should have icon mappings.
# Source: `usage-limits --json` output keys.
KNOWN_PROVIDER_KEYS = {
    "antigravity",
    "claude",
    "codex",
    "copilot",
    "cursor",
    "kiro",
    "ollama",
    "opencode",
    "opencode-go",
    "opencode-zen",
    "qoder",
    "trae",
    "windsurf",
}

# Expected icon name for each provider key
EXPECTED_PROVIDER_ICONS = {
    "antigravity": "antigravity-symbolic",
    "claude": "claude-ai-symbolic",
    "codex": "codex-symbolic",
    "copilot": "copilot-symbolic",
    "cursor": "cursor-symbolic",
    "kiro": "kiro-symbolic",
    "ollama": "ollama-symbolic",
    "opencode": "opencode-symbolic",
    "opencode-go": "opencode-symbolic",
    "opencode-zen": "opencode-symbolic",
    "qoder": "qoder-symbolic",
    "trae": "trae-symbolic",
    "windsurf": "windsurf-symbolic",
}

# Known system icon theme directories where icons may reside
SYSTEM_ICON_DIRS = [
    Path("/usr/share/icons/hicolor/scalable/actions"),
    Path("/usr/share/icons/hicolor/scalable/status"),
    Path("/usr/share/icons/Adwaita/symbolic/actions"),
    Path("/usr/share/icons/Adwaita/symbolic/status"),
    Path("/usr/share/icons/hicolor/scalable/apps"),
]


def test_project_icons_directory_exists():
    """
    The project's icons/ directory must exist and follow the freedesktop
    icon theme specification (hicolor/scalable/<category>/).
    """
    assert ICONS_DIR.is_dir(), (
        f"Project icons directory not found at {ICONS_DIR}\n"
        "The app.tsx `icons` config should reference this directory.\n"
        "Current config: icons: `${SRC}/icons`,"
        "   (SRC resolves to project root at runtime)"
    )

    # Verify the icon directory has the expected freedesktop structure
    hicolor_dir = ICONS_DIR / "hicolor"
    assert hicolor_dir.is_dir(), (
        f"Expected '{ICONS_DIR}' to contain a 'hicolor/' subdirectory\n"
        "following the freedesktop icon theme specification."
    )

    scalable_dir = hicolor_dir / "scalable"
    assert scalable_dir.is_dir(), (
        f"Expected '{hicolor_dir}' to contain a 'scalable/' subdirectory."
    )

    # Must have at least one category subdirectory with SVG files
    category_dirs = [d for d in scalable_dir.iterdir() if d.is_dir()]
    assert len(category_dirs) > 0, (
        f"Expected '{scalable_dir}' to contain at least one category "
        f"subdirectory (e.g. 'actions', 'status')."
    )


def test_custom_project_icons_exist():
    """
    Every custom icon referenced in the code must have a corresponding SVG
    file in the project's icons/hicolor/scalable/ directory.
    """
    assert ICONS_DIR.is_dir(), f"Project icons directory not found at {ICONS_DIR}"

    # Find all SVG files in the project icons directory
    project_svg_files = set()
    for svg in ICONS_DIR.rglob("*-symbolic.svg"):
        project_svg_files.add(svg.stem)  # stem = filename without .svg

    custom_icon_names = {
        "antigravity-symbolic",
        "anthropic-symbolic",
        "battery-bolt-symbolic",
        "claude-ai-symbolic",
        "codex-symbolic",
        "copilot-symbolic",
        "cursor-symbolic",
        "hourglass-symbolic",
        "kiro-symbolic",
        "ollama-symbolic",
        "openai-symbolic",
        "opencode-symbolic",
        "qoder-symbolic",
        "ram-symbolic",
        "trae-symbolic",
        "wattage-symbolic",
        "windsurf-symbolic",
    }

    missing = custom_icon_names - project_svg_files
    assert not missing, (
        f"Custom icons referenced in code but missing from project icons dir "
        f"({ICONS_DIR}):\n  {sorted(missing)}"
    )


def test_system_icons_exist():
    """
    Every system icon referenced in the code must be available from at least
    one installed icon theme.
    """
    system_icon_names = STATIC_ICON_NAMES - {
        # Remove custom project icons — they're in the project dir, not system
        "antigravity-symbolic",
        "anthropic-symbolic",
        "battery-bolt-symbolic",
        "claude-ai-symbolic",
        "codex-symbolic",
        "copilot-symbolic",
        "cursor-symbolic",
        "hourglass-symbolic",
        "kiro-symbolic",
        "ollama-symbolic",
        "openai-symbolic",
        "opencode-symbolic",
        "qoder-symbolic",
        "ram-symbolic",
        "trae-symbolic",
        "wattage-symbolic",
        "windsurf-symbolic",
    }

    # Build set of all available system icon names (without extension)
    available_system_icons = set()
    for icon_dir in SYSTEM_ICON_DIRS:
        if icon_dir.is_dir():
            for svg in icon_dir.glob("*-symbolic.svg"):
                available_system_icons.add(svg.stem)

    missing = system_icon_names - available_system_icons
    assert not missing, (
        f"System icons referenced in code but not found in any known "
        f"system icon directory:\n  {sorted(missing)}"
    )


def test_icons_directory_uses_src_variable():
    """
    The icons path in app.tsx should use the AGS v2 global `SRC` variable
    instead of a hardcoded absolute path, so it works regardless of where
    the project is cloned.
    """
    tsx_content = APP_TSX.read_text()

    # Check that the icons path contains SRC (template variable)
    has_src = "${SRC}" in tsx_content or "icons: `" in tsx_content
    has_hardcoded_absolute = re.search(r'icons:\s*"/home/', tsx_content)

    assert has_src or not has_hardcoded_absolute, (
        "app.tsx uses a hardcoded absolute path for icons.\n"
        "It should use the AGS v2 SRC global variable instead:\n"
        "  icons: `${SRC}/icons`,"
    )


def _parse_provider_icons() -> dict[str, str]:
    """Extract the PROVIDER_ICONS mapping from control-center.tsx."""
    tsx_path = PROJECT_ROOT / "src" / "windows" / "control-center.tsx"
    text = tsx_path.read_text()

    # Find the PROVIDER_ICONS record and extract key-value pairs
    mapping: dict[str, str] = {}
    in_block = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("const PROVIDER_ICONS"):
            in_block = True
            continue
        if in_block:
            if stripped == "}":
                break
            # Match: provider_key: "icon-name",
            m = re.match(r'^\s*"?(\S+?)"?:\s*"([^"]+)"', stripped)
            if m:
                key = m.group(1).rstrip(",")
                mapping[key] = m.group(2)
    return mapping


def test_provider_icons_coverage():
    """
    Every known provider key must have an entry in the PROVIDER_ICONS map
    in control-center.tsx. If this test fails, a new provider was added to
    usage-limits but has no corresponding icon mapping.
    """
    mapping = _parse_provider_icons()
    mapped_keys = set(mapping.keys())

    missing = KNOWN_PROVIDER_KEYS - mapped_keys
    assert not missing, (
        f"Provider keys missing from PROVIDER_ICONS mapping:\n  {sorted(missing)}\n\n"
        f"Current mapped keys:\n  {sorted(mapped_keys)}\n\n"
        "Add an entry to PROVIDER_ICONS in src/windows/control-center.tsx\n"
        "and create an SVG icon in icons/hicolor/scalable/status/."
    )

    extra = mapped_keys - KNOWN_PROVIDER_KEYS
    assert not extra, (
        f"Provider keys in PROVIDER_ICONS not in KNOWN_PROVIDER_KEYS:\n  {sorted(extra)}\n\n"
        "Either add them to KNOWN_PROVIDER_KEYS (if they're real providers) or\n"
        "remove them from PROVIDER_ICONS."
    )


def test_provider_icons_correct():
    """
    Every provider key must map to its expected icon name.
    """
    mapping = _parse_provider_icons()
    for key, expected_icon in EXPECTED_PROVIDER_ICONS.items():
        actual = mapping.get(key)
        assert actual == expected_icon, (
            f"Provider '{key}' expected icon '{expected_icon}' but got '{actual}'"
        )


def test_provider_icon_files_exist():
    """
    Every icon referenced in PROVIDER_ICONS must exist as an SVG file
    in the project's icon directory.
    """
    mapping = _parse_provider_icons()
    icon_names = set(mapping.values())

    project_svg_files = set()
    for svg in ICONS_DIR.rglob("*-symbolic.svg"):
        project_svg_files.add(svg.stem)

    missing = icon_names - project_svg_files
    assert not missing, (
        f"Icons referenced in PROVIDER_ICONS but missing from project:\n  {sorted(missing)}"
    )
