"""Configuration constants for V3-minimal LLM REPL"""

from typing import Dict


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
