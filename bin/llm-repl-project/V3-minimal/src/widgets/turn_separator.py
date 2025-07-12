"""
Turn Separator Widget - Horizontal rule with turn number
"""

from rich.console import RenderableType
from rich.rule import Rule
from textual.widget import Widget
from pathlib import Path


class TurnSeparator(Widget):
    """Horizontal rule with turn number in the center"""

    # Load CSS from external file
    _css_file = Path(__file__).parent / "turn_separator.tcss"
    DEFAULT_CSS = _css_file.read_text() if _css_file.exists() else ""

    def __init__(self, turn_number: int, **kwargs):
        super().__init__(**kwargs)
        self.turn_number = turn_number
        self.add_class("turn-separator")
        # Explicitly set the height
        self.styles.height = 1
        self.styles.max_height = 1

    def render(self) -> RenderableType:
        """Render horizontal rule with turn number"""
        # Create the turn label
        turn_label = f"[Turn {self.turn_number}]"

        # Use Rich's Rule to create a nice horizontal line with centered text
        rule = Rule(turn_label, style="dim", align="center")

        return rule

    def get_content_height(self, container, viewport, width: int) -> int:
        """Explicitly return height of 1 for this widget"""
        return 1
