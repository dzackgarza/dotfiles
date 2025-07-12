"""
Simple CognitionWidget for displaying cognition results.
"""

from textual.widgets import Static
from rich.text import Text


class CognitionWidget(Static):
    """Simple widget for displaying cognition processing results."""

    DEFAULT_CSS = """
    CognitionWidget {
        border: round $accent;
        margin: 1 0;
        padding: 1;
        height: auto;
        background: $surface;
    }
    """

    def __init__(self, content="", is_live=False, **kwargs):
        super().__init__(**kwargs)
        self.content = content
        self.is_live = is_live
        self._update_display()

    def _update_display(self):
        """Update the widget display."""
        display_text = Text()
        display_text.append("🧠 ", style="bold cyan")
        display_text.append("Cognition", style="bold white")
        
        if self.is_live:
            display_text.append(" 🔄", style="yellow")
        else:
            display_text.append(" ✅", style="green")
            
        if self.content:
            display_text.append(f"\n{self.content}", style="white")
            
        self.update(display_text)

    def update_content(self, content, is_live=None):
        """Update the widget content."""
        self.content = content
        if is_live is not None:
            self.is_live = is_live
        self._update_display()

    def set_live_content(self, content):
        """Set live content for the cognition widget."""
        self.update_content(content, is_live=True)