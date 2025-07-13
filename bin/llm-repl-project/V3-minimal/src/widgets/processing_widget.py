"""
Processing Widget for Debug Mode

Shows a single processing block with:
- Timer (counts up during processing, freezes when done)
- Progress bar (linear fill over processing duration)
- Token counters (simulated up/down tokens)
- State indicator (Queued/Processing/Done)
"""

from textual.widget import Widget
from textual.reactive import reactive
from textual import work
from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text
from pathlib import Path
import asyncio
import time
import random
from enum import Enum
from typing import Optional


class ProcessingState(Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    DONE = "done"


class ProcessingWidget(Widget):
    """Individual processing block with visual progress tracking"""

    # Load CSS from external file
    _css_file = Path(__file__).parent / "processing_widget.tcss"
    DEFAULT_CSS = _css_file.read_text() if _css_file.exists() else ""

    # Reactive properties
    state = reactive(ProcessingState.QUEUED)
    elapsed_time = reactive(0.0)
    progress = reactive(0.0)
    tokens_up = reactive(0)
    tokens_down = reactive(0)

    # Configuration
    PROCESSING_DURATION = 5.0  # 5 seconds mock processing

    def __init__(self, message: str, **kwargs):
        super().__init__(**kwargs)
        self.message = message
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self._timer_task = None

        # Generate mock token counts
        self.tokens_up = random.randint(50, 200)
        self.tokens_down = random.randint(100, 400)

    def on_mount(self) -> None:
        """Start processing if this is the active block"""
        # Processing will be triggered by the queue manager
        pass

    async def start_processing(self) -> None:
        """Begin processing this block"""
        if self.state != ProcessingState.QUEUED:
            return

        self.state = ProcessingState.PROCESSING
        self.start_time = time.time()

        # Start timer update
        self._timer_task = self.run_timer()

        # Start progress update
        self.run_progress()

        # Simulate processing
        await asyncio.sleep(self.PROCESSING_DURATION)

        # Mark as done
        self.end_time = time.time()
        self.state = ProcessingState.DONE
        self.progress = 1.0

        # Cancel timer to freeze display
        if self._timer_task:
            self._timer_task.cancel()

    @work(exclusive=True)
    async def run_timer(self) -> None:
        """Update timer display"""
        while self.state == ProcessingState.PROCESSING:
            if self.start_time:
                self.elapsed_time = time.time() - self.start_time
            await asyncio.sleep(0.1)

    @work(exclusive=True)
    async def run_progress(self) -> None:
        """Update progress bar"""
        start = time.time()
        while self.state == ProcessingState.PROCESSING:
            elapsed = time.time() - start
            self.progress = min(elapsed / self.PROCESSING_DURATION, 1.0)
            await asyncio.sleep(0.05)

    def render(self) -> RenderableType:
        """Render the processing widget"""
        # State indicator with color
        state_colors = {
            ProcessingState.QUEUED: "dim white",
            ProcessingState.PROCESSING: "bright_yellow",
            ProcessingState.DONE: "bright_green"
        }
        state_text = Text(f"[{self.state.value.upper()}]", style=state_colors[self.state])

        # Timer display
        timer_text = f"⏱️  {self.elapsed_time:.1f}s"

        # Token counters
        tokens_text = f"↑ {self.tokens_up} tokens  ↓ {self.tokens_down} tokens"

        # Progress bar representation
        if self.state == ProcessingState.QUEUED:
            progress_bar = "━" * 30  # Empty bar
        else:
            filled = int(self.progress * 30)
            empty = 30 - filled
            progress_bar = "█" * filled + "━" * empty

        # Message preview (truncated)
        message_preview = self.message[:50] + "..." if len(self.message) > 50 else self.message

        # Compose the layout as a single Text object
        content = Text()
        content.append(state_text)
        content.append(" | ", style="dim")
        content.append(timer_text, style="bright_cyan")
        content.append(" | ", style="dim")
        content.append(tokens_text, style="bright_magenta")
        content.append("\n\n")
        content.append(message_preview, style="white")
        content.append("\n\n")
        content.append(f"[{progress_bar}] {int(self.progress * 100)}%", style="bright_blue")

        # Panel styling based on state
        border_style = state_colors[self.state]

        return Panel(
            content,
            title=f"Processing Block #{id(self) % 1000}",
            border_style=border_style,
            padding=(1, 2)
        )
