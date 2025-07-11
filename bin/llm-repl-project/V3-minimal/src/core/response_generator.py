"""Response generation service for LLM REPL

Handles response generation and provides placeholder functionality
for future LLM integration following the plugin-based architecture.
"""

from typing import Dict, Optional, TYPE_CHECKING
import re

from ..config import AppConfig, ThemeConfig

if TYPE_CHECKING:
    from ..main import LLMReplApp


class ResponseGenerator:
    """Generates responses to user input

    This service provides placeholder response generation and is designed
    to be easily replaced with LLM integration plugins in the future.

    Responsibilities:
    - Pattern matching for common queries
    - Default response generation
    - Future: LLM integration interface
    """

    def __init__(self, app: Optional["LLMReplApp"] = None):
        self.app = app
        self.response_patterns: Dict[str, str] = AppConfig.DEFAULT_RESPONSES
        self.default_template: str = AppConfig.DEFAULT_LLM_RESPONSE

    def generate_response(self, user_input: str) -> str:
        """Generate a response to user input

        Args:
            user_input: The user's input text

        Returns:
            Generated response string

        Current Implementation:
        - Theme switching commands
        - Pattern matching against predefined responses
        - Fallback to template response

        Future Enhancement:
        - Plugin-based LLM integration
        - Context-aware response generation
        - Multi-model routing
        """
        user_input_lower = user_input.lower().strip()

        # Handle theme switching commands
        theme_match = re.match(r"theme\s+(\w+)", user_input_lower)
        if theme_match:
            return self._handle_theme_command(theme_match.group(1))

        # Check for pattern matches in predefined responses
        for pattern, response in self.response_patterns.items():
            if pattern in user_input_lower:
                return response

        # Fallback to default template response
        return self.default_template.format(user_input=user_input)

    def _handle_theme_command(self, theme_name: str) -> str:
        """Handle theme switching command

        Args:
            theme_name: Name of theme to switch to

        Returns:
            Response message about theme switching
        """
        if not self.app:
            return "❌ theme switching not available (no app instance)"

        if theme_name not in ThemeConfig.AVAILABLE_THEMES:
            available = ", ".join(ThemeConfig.AVAILABLE_THEMES.keys())
            return f"❌ unknown theme '{theme_name}'\n\navailable themes: {available}"

        if self.app.switch_theme(theme_name):
            theme_info = ThemeConfig.AVAILABLE_THEMES[theme_name]
            return f"✅ switched to {theme_info['name']} theme\n\n{theme_info['description']}\n\n💡 tip: you can also use Ctrl+P to access Textual's built-in theme picker"
        else:
            return f"❌ failed to switch to theme '{theme_name}'"

    def add_response_pattern(self, pattern: str, response: str) -> None:
        """Add a new response pattern

        Args:
            pattern: Text pattern to match (case-insensitive)
            response: Response to return when pattern matches
        """
        self.response_patterns[pattern.lower()] = response

    def remove_response_pattern(self, pattern: str) -> None:
        """Remove a response pattern

        Args:
            pattern: Pattern to remove
        """
        self.response_patterns.pop(pattern.lower(), None)

    def set_default_template(self, template: str) -> None:
        """Set the default response template

        Args:
            template: Template string with {user_input} placeholder
        """
        self.default_template = template
