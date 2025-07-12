"""
Staging Separator Widget - Shows hrule-style separator in staging area

Two states:
- Idle: --------XXX-------- (animated)
- Processing: -------[Turn N]-------
"""

from rich.console import RenderableType
from rich.rule import Rule
from textual.widget import Widget
from textual.reactive import reactive
from textual import work
from pathlib import Path


class StagingSeparator(Widget):
    """hrule-style separator for staging area with idle animation or turn info"""

    # Load CSS from external file
    _css_file = Path(__file__).parent / "staging_separator.tcss"
    DEFAULT_CSS = _css_file.read_text() if _css_file.exists() else ""

    # Animation frames for idle state
    IDLE_FRAMES = [
        "◇",
        "◆",
        "◇",
        "◇",
    ]

    frame_index = reactive(0)
    processing = reactive(False)
    turn_number = reactive(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_class("staging-separator")

    def on_mount(self) -> None:
        """Start animation when mounted"""
        self.run_animation()

    @work(exclusive=True)
    async def run_animation(self) -> None:
        """Animation loop for idle state"""
        import asyncio

        while True:
            if not self.processing:
                await asyncio.sleep(0.8)  # Slower, more subtle animation
                self.frame_index = (self.frame_index + 1) % len(self.IDLE_FRAMES)
            else:
                await asyncio.sleep(0.1)  # Check processing state frequently

    def set_processing(self, turn_number: int) -> None:
        """Switch to processing state showing turn number"""
        self.processing = True
        self.turn_number = turn_number
        self.refresh()

    def set_idle(self) -> None:
        """Switch to idle state with animation"""
        self.processing = False
        self.refresh()

    def render(self) -> RenderableType:
        """Render separator based on state"""
        if self.processing:
            # Processing state: -------[Turn N]-------
            title = f"Turn {self.turn_number}"
            return Rule(title, style="bright_blue")
        else:
            # Idle state: --------◇-------- (animated)
            frame = self.IDLE_FRAMES[self.frame_index]
            return Rule(frame, style="dim")
