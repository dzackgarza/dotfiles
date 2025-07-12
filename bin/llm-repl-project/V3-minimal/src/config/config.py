"""Configuration constants for V3-minimal LLM REPL"""

from typing import Dict, Optional
import yaml
from pathlib import Path


class UIConfig:
    """UI-related configuration constants"""

    # Content preview limits
    MAX_CONTENT_PREVIEW = 50

    # Cursor positions
    CURSOR_TOP_POSITION = (0, 0)

    # Syntax highlighting
    DEFAULT_SYNTAX_THEME = "monokai"
    DEFAULT_BACKGROUND_COLOR = "default"

    # Timeline styling
    TIMELINE_MARGIN_BOTTOM = 1
    TIMELINE_PADDING = (0, 1)


class ConfigLoader:
    """Loads configuration from YAML files"""

    @staticmethod
    def find_config_file() -> Optional[Path]:
        """Find config file in order of preference"""
        search_paths = [
            Path.cwd() / "config.yaml",  # Current directory
            Path.home() / ".config" / "llm-repl" / "config.yaml",  # User config
            Path(__file__).parent.parent / "config.yaml",  # Project default
        ]

        for path in search_paths:
            if path.exists():
                return path
        return None

    @staticmethod
    def load_config() -> dict:
        """Load configuration from YAML file"""
        config_file = ConfigLoader.find_config_file()
        if not config_file:
            return {}

        try:
            with open(config_file, "r") as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: Could not load config from {config_file}: {e}")
            return {}


class AnimationConfig:
    """Animation and typewriter speed configuration"""

    # Load from YAML config
    _config = ConfigLoader.load_config()
    _animation_config = _config.get("animation", {})

    # Default fallback presets
    _DEFAULT_PRESETS = {
        "slow": {"initial": 100, "progress": 150, "completion": 200, "summary": 120},
        "medium": {"initial": 500, "progress": 800, "completion": 1000, "summary": 600},
        "fast": {
            "initial": 1500,
            "progress": 2000,
            "completion": 2500,
            "summary": 1800,
        },
        "ultra": {
            "initial": 3000,
            "progress": 4000,
            "completion": 5000,
            "summary": 3500,
        },
        "instant": {
            "initial": 8000,
            "progress": 8000,
            "completion": 8000,
            "summary": 8000,
        },
    }

    @classmethod
    def get_current_speeds(cls) -> dict:
        """Get current speed settings from YAML config or fallback preset"""

        # Check if using a preset
        if "preset" in cls._animation_config:
            preset_name = cls._animation_config["preset"]
            if preset_name in cls._DEFAULT_PRESETS:
                return cls._DEFAULT_PRESETS[preset_name]

        # Check if using custom speeds
        if "typewriter_speeds" in cls._animation_config:
            speeds = cls._animation_config["typewriter_speeds"]
            return {
                "initial": speeds.get("initial", 1500),
                "progress": speeds.get("progress", 2000),
                "completion": speeds.get("completion", 2500),
                "summary": speeds.get("summary", 1800),
            }

        # Fallback to fast preset
        return cls._DEFAULT_PRESETS["fast"]

    @classmethod
    def reload_config(cls):
        """Reload configuration from file"""
        cls._config = ConfigLoader.load_config()
        cls._animation_config = cls._config.get("animation", {})


class RoleConfig:
    """Role-related configuration for Sacred Timeline"""

    # Elegant role indicators (no capitals, refined symbols)
    ROLE_INDICATORS: Dict[str, str] = {
        "user": "›",  # Simple chevron
        "system": "⚙",  # Gear (no variation selector)
        "assistant": "•",  # Bullet point
        "cognition": "◦",  # Small circle
        "turn": "→",  # Arrow
        "tool": "▸",  # Right-pointing triangle
        "error": "⚠",  # Warning triangle
        "processing": "⋯",  # Ellipsis
    }

    # Elegant role titles (no capitals)
    ROLE_TITLES: Dict[str, str] = {
        "user": "user input",
        "system": "system message",
        "assistant": "assistant response",
        "cognition": "cognition pipeline",
        "turn": "conversation turn",
        "tool": "tool execution",
        "error": "error occurred",
        "processing": "processing",
    }

    # Role colors for text display (muted, terminal-appropriate - no bright colors)
    ROLE_COLORS: Dict[str, str] = {
        "user": "green",
        "system": "yellow",
        "assistant": "cyan",
        "cognition": "magenta",
        "turn": "white",
        "tool": "blue",
        "error": "red",
        "processing": "yellow",
    }

    # Border colors (subtle versions of role colors)
    BORDER_COLORS: Dict[str, str] = {
        "user": "#404858",  # Slightly darker than Nord's panel/surface
        "system": "#303642",  # Slightly darker than Nord's background
        "assistant": "#404858",
        "cognition": "#404858",
        "turn": "#454F60",  # Another subtle dark gray/blue-gray
        "tool": "#404858",
        "error": "#8f4950",  # Muted red
        "processing": "#b09a6a",  # Muted yellow
    }


class ThemeConfig:
    """Theme configuration using Textual's built-in theme system"""

    # Available custom themes (using Textual's Theme objects)
    AVAILABLE_THEMES = {
        "dracula": {
            "name": "Dracula",
            "description": "vibrant dark theme",
            "primary": "#5A67D8",  # Subtle Accent 2 (for Assistant/Cognition)
            "secondary": "#333333",  # Neutral/Base (for System)
            "accent": "#38A169",  # Subtle Accent 3 (for Processing/Tool)
            "warning": "#f1fa8c",  # Yellow
            "error": "#ff5555",  # Red
            "success": "#4A5568",  # Subtle Accent 1 (for User)
            "dark": True,
        },
        "tokyo_night": {
            "name": "Tokyo Night",
            "description": "clean dark theme celebrating tokyo lights",
            "primary": "#7dcfff",  # Cyan
            "secondary": "#bb9af7",  # Purple
            "accent": "#7aa2f7",  # Blue
            "warning": "#e0af68",  # Orange
            "error": "#f7768e",  # Red
            "success": "#9ece6a",  # Green
            "dark": True,
        },
        "nord": {
            "name": "Nord",
            "description": "arctic minimalism with frost blue accents",
            "primary": "#88c0d0",  # Frost cyan
            "secondary": "#b48ead",  # Aurora purple
            "accent": "#81a1c1",  # Frost blue
            "warning": "#ebcb8b",  # Aurora yellow
            "error": "#bf616a",  # Aurora red
            "success": "#a3be8c",  # Aurora green
            "dark": True,
        },
        "rose_pine": {
            "name": "Rosé Pine",
            "description": "warm, cozy aesthetics with rose and pine colors",
            "primary": "#9ccfd8",  # Foam cyan
            "secondary": "#c4a7e7",  # Iris purple
            "accent": "#ebbcba",  # Rose
            "warning": "#f6c177",  # Gold
            "error": "#eb6f92",  # Love pink
            "success": "#31748f",  # Pine teal
            "dark": True,
        },
        "kanagawa": {
            "name": "Kanagawa",
            "description": "japanese wave aesthetics with muted tones",
            "primary": "#7e9cd8",  # Crystal blue
            "secondary": "#938aa9",  # Violet
            "accent": "#dca561",  # Yellow
            "warning": "#ffa066",  # Orange
            "error": "#e82424",  # Red
            "success": "#76946a",  # Green
            "dark": True,
        },
    }

    # Default theme
    DEFAULT_THEME = "nord"


class AppConfig:
    """Application-level configuration"""

    # Application metadata
    TITLE = "LLM REPL V3-minimal"
    SUB_TITLE = "Sacred Timeline • Elegant Typography"

    # Default responses for common queries
    DEFAULT_RESPONSES: Dict[str, str] = {
        "hello": "Hello! I'm your LLM assistant running in the Sacred Timeline.",
        "test": "✅ V3-minimal is working correctly!\n\n• Enter sends messages\n• Shift+Enter creates new lines (requires Kitty terminal)\n• Ctrl+P for instant theme switching\n• Timeline scrolls bottom-up\n• Elegant typography active",
        "timeline": "📜 the sacred timeline ensures all interactions are:\n\n• immutable\n• append-only\n• fully transparent\n• chronologically ordered",
        "themes": "🎨 available themes:\n\n• dracula - vibrant dark theme\n• tokyo_night - clean tokyo lights\n• nord - arctic minimalism\n• rose_pine - warm, cozy aesthetics\n• kanagawa - japanese wave aesthetics\n\nType 'theme <name>' to switch themes.",
        "quit": "use ctrl+c to quit the application.",
    }

    # Initialization message
    WELCOME_MESSAGE = "🚀 llm repl v3-minimal initialized\nsacred timeline active • elegant typography loaded"

    # Default LLM response template
    DEFAULT_LLM_RESPONSE = "i received your message: '{user_input}'\n\nthis is a placeholder response. llm integration will be added next."


class TimelineConfig:
    """Sacred Timeline configuration"""

    # Content limits
    MAX_CONTENT_PREVIEW = 50

    # Timestamp formats
    TIMESTAMP_FORMAT = "%H:%M:%S"
    BORDER_TITLE_FORMAT = "%H:%M"

    # Default metadata
    DEFAULT_METADATA: dict = {}

    # Block processing
    COGNITION_PREVIEW_PREFIX = "Processing user query: '"
    COGNITION_PREVIEW_SUFFIX = "...'"
