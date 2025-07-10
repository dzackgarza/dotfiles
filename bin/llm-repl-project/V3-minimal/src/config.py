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

    # Role indicators (ASCII symbols for each role)
    ROLE_INDICATORS: Dict[str, str] = {
        "user": "❯",
        "system": "⚡",
        "assistant": "🤖",
        "cognition": "⚙️",
        "turn": "🔄",
    }

    # Role colors for text display
    ROLE_COLORS: Dict[str, str] = {
        "user": "bright_green",
        "system": "bright_yellow",
        "assistant": "bright_cyan",
        "cognition": "bright_magenta",
        "turn": "bright_white",
    }

    # Border colors (subtle versions of role colors)
    BORDER_COLORS: Dict[str, str] = {
        "user": "green",
        "system": "yellow",
        "assistant": "cyan",
        "cognition": "magenta",
        "turn": "white",
    }


class AppConfig:
    """Application-level configuration"""

    # Application metadata
    TITLE = "LLM REPL V3-minimal"
    SUB_TITLE = "Sacred Timeline • Dracula Theme"

    # Default responses for common queries
    DEFAULT_RESPONSES: Dict[str, str] = {
        "hello": "Hello! I'm your LLM assistant running in the Sacred Timeline.",
        "test": "✅ V3-minimal is working correctly!\n\n• Enter sends messages\n• Shift+Enter creates new lines\n• Timeline scrolls bottom-up\n• Unix-rice theme active",
        "timeline": "📜 The Sacred Timeline ensures all interactions are:\n\n• Immutable\n• Append-only\n• Fully transparent\n• Chronologically ordered",
        "quit": "Use Ctrl+C to quit the application.",
    }

    # Initialization message
    WELCOME_MESSAGE = "🚀 LLM REPL V3-minimal initialized\nSacred Timeline active • Dracula theme loaded"

    # Default LLM response template
    DEFAULT_LLM_RESPONSE = "I received your message: '{user_input}'\n\nThis is a placeholder response. LLM integration will be added next."


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
