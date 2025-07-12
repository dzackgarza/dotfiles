"""
Idle Animation Widget - Shows subtle animation in staging area
"""

from rich.console import RenderableType
from rich.text import Text
from textual.widget import Widget
from textual.reactive import reactive
from textual import work
from datetime import datetime
from pathlib import Path


class IdleAnimation(Widget):
    """Subtle idle animation for staging area"""

    # Load CSS from external file
    _css_file = Path(__file__).parent / "idle_animation.tcss"
    DEFAULT_CSS = _css_file.read_text() if _css_file.exists() else ""

    # Animation frames for subtle effect
    IDLE_FRAMES = [
        "✨ Awaiting your query",
        "✨ Awaiting your query.",
        "✨ Awaiting your query..",
        "✨ Awaiting your query...",
    ]

    frame_index = reactive(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_class("idle-animation")

    def on_mount(self) -> None:
        """Start animation when mounted"""
        self.animate()

    @work(exclusive=True)
    async def animate(self) -> None:
        """Subtle animation loop using Textual's worker"""
        import asyncio

        while True:
            await asyncio.sleep(0.5)  # Update every 500ms
            self.frame_index = (self.frame_index + 1) % len(self.IDLE_FRAMES)

    def render(self) -> RenderableType:
        """Render current animation frame"""
        frame = self.IDLE_FRAMES[self.frame_index]
        # Add subtle timestamp for extra dynamism
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")

        text = Text()
        text.append(frame, style="dim italic")
        text.append(f"  [{time_str}]", style="dim")

        return text
