"""Base class for cognition sub-modules."""

from abc import ABC, abstractmethod
from typing import Optional, Callable
import time

from ..live_blocks import LiveBlock


class SubModule(ABC):
    """Base class for all cognition sub-modules."""

    def __init__(self, live_block: LiveBlock, parent_block: Optional[LiveBlock] = None):
        """Initialize sub-module with its live block and optional parent."""
        self.live_block = live_block
        self.parent_block = parent_block
        self.completion_callback: Optional[Callable] = None
        self._is_complete = False
        self._start_time: Optional[float] = None

    def set_completion_callback(self, callback: Callable) -> None:
        """Set callback to notify parent when complete."""
        self.completion_callback = callback

    async def run(self) -> None:
        """Run the sub-module with timing tracking."""
        self._start_time = time.time()
        await self.execute()
        # Set wall time when complete
        self.live_block.data.wall_time_seconds = time.time() - self._start_time

    def update_progress_display(self, additional_text: str = "") -> None:
        """Update the progress display in the content."""
        if self._start_time:
            elapsed = time.time() - self._start_time
        else:
            elapsed = 0.0

        # Generate progress bar
        progress = self.live_block.data.progress
        bar_width = 20
        filled = int(progress * bar_width)
        bar = "█" * filled + "░" * (bar_width - filled)

        # Format timing and token info
        tokens_in = self.live_block.data.tokens_input
        tokens_out = self.live_block.data.tokens_output

        progress_line = f"⏱️ {elapsed:.1f}s | [{bar}] {int(progress * 100)}% | 🔢 {tokens_in}↑/{tokens_out}↓"

        # Update the content with the new progress line
        lines = self.live_block.data.content.split("\n")
        # Find and replace the progress line (last line typically)
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].startswith("⏱️"):
                lines[i] = progress_line
                break

        if additional_text:
            # Insert additional text before the progress line
            lines.insert(-1, additional_text)

        self.live_block.data.content = "\n".join(lines)
        self.live_block._notify_update()

    @abstractmethod
    async def execute(self) -> None:
        """Execute the sub-module's task. Must be implemented by subclasses."""
        pass

    @abstractmethod
    def get_initial_content(self) -> str:
        """Get initial content for the live block."""
        pass

    async def _notify_completion(self) -> None:
        """Notify parent that this sub-module is complete."""
        self._is_complete = True
        if self.completion_callback:
            await self.completion_callback()

    @property
    def is_complete(self) -> bool:
        """Check if sub-module has completed execution."""
        return self._is_complete
