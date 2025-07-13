"""
Sub-Module Widget - V3's Chatbox Pattern for Cognition

Single widget that renders sub-module content with streaming support.
Uses V3's render() method pattern - NO child containers.
"""

from rich.console import RenderableType
from rich.text import Text
from rich.panel import Panel
from textual.widget import Widget
from textual.reactive import reactive
from textual import work
import asyncio
import time

from ..core.live_blocks import LiveBlock, BlockState


class SubModuleWidget(Widget, can_focus=True):
    """Sub-module widget using ProcessingWidget style

    Shows timer, progress bar, and token counters like ProcessingWidget.
    Timer freezes when processing completes.
    """

    # Reactive properties
    elapsed_time = reactive(0.0)

    def __init__(self, sub_module: LiveBlock, **kwargs):
        super().__init__(**kwargs)
        self.sub_module = sub_module
        self.start_time = None
        self.end_time = None
        self._timer_task = None

        # CSS classes based on role (like V3's Chatbox)
        self.add_class("sub-module")
        self.add_class(f"sub-module-{sub_module.role}")

        # Subscribe to live updates
        self.sub_module.add_update_callback(self._on_sub_module_update)
        self.sub_module.add_progress_callback(self._on_progress_update)

        # State-based CSS classes
        self.add_class("sub-module-live")
        self._update_state_class()

        # Start timer if already processing (only when mounted)
        if sub_module.state == BlockState.LIVE:
            self.start_time = time.time()
            # Timer will be started in on_mount

    def on_mount(self) -> None:
        """Start timer when widget is mounted to the app"""
        if self.start_time and self.sub_module.state == BlockState.LIVE:
            self._start_timer()

    def render(self) -> RenderableType:
        """Render widget in ProcessingWidget style"""

        # Get sub-module data
        content = self.sub_module.data.content
        # Use elapsed_time for live updates, wall_time for final
        if self.sub_module.state == BlockState.LIVE:
            display_time = self.elapsed_time
        else:
            display_time = self.sub_module.data.wall_time_seconds
        tokens_in = self.sub_module.data.tokens_input or 0
        tokens_out = self.sub_module.data.tokens_output or 0
        progress = self.sub_module.data.progress or 0.0
        state = self.sub_module.state

        # Map states to ProcessingWidget style
        state_map = {
            BlockState.LIVE: "PROCESSING",
            BlockState.TRANSITIONING: "PROCESSING",
            BlockState.INSCRIBED: "DONE"
        }

        # State colors
        state_colors = {
            BlockState.LIVE: "bright_yellow",
            BlockState.TRANSITIONING: "bright_yellow",
            BlockState.INSCRIBED: "bright_green"
        }

        # Create content matching ProcessingWidget format
        display_content = Text()

        # First line: STATE | Timer | Tokens
        display_state = state_map.get(state, "UNKNOWN")
        display_content.append(f"[{display_state}]", style=state_colors.get(state, "white"))
        display_content.append(" | ", style="dim")
        display_content.append(f"⏱️  {display_time:.1f}s", style="bright_cyan")
        display_content.append(" | ", style="dim")
        display_content.append(f"↑ {tokens_in} tokens  ↓ {tokens_out} tokens", style="bright_magenta")

        # Second line: Role with emoji
        role_indicator = self._get_role_indicator()
        role_name = self.sub_module.role.replace("_", " ").title()
        display_content.append(f"\n{role_indicator} {role_name}", style="white")

        # Third line: Progress bar
        if state == BlockState.INSCRIBED:
            # Show full progress bar for completed tasks
            progress_bar = "█" * 30
        else:
            filled = int(progress * 30)
            empty = 30 - filled
            progress_bar = "█" * filled + "━" * empty

        display_content.append(f"\n[{progress_bar}] {int(progress * 100)}%", style="bright_blue")

        # Panel with state-based border
        border_style = state_colors.get(state, "white")

        return Panel(
            display_content,
            title="Cognition Module",
            border_style=border_style,
            padding=(1, 2)
        )

    def _get_role_indicator(self) -> str:
        """Get indicator emoji for sub-module role"""
        indicators = {
            "route_query": "🎯",
            "call_tool": "🛠️",
            "format_output": "📝",
            "sub_module": "🔧",
            "assistant": "🤖",
        }
        return indicators.get(self.sub_module.role, "🔧")

    def _get_state_indicator(self, state: BlockState) -> str:
        """Get indicator for sub-module state"""
        if state == BlockState.LIVE:
            return "●"  # Live (green)
        elif state == BlockState.TRANSITIONING:
            return "⧗"  # Transitioning (yellow)
        else:
            return "◉"  # Completed (blue)

    def _get_border_style(self, state: BlockState) -> str:
        """Get border style based on state"""
        if state == BlockState.LIVE:
            return "green"
        elif state == BlockState.TRANSITIONING:
            return "yellow"
        else:
            return "blue"

    def _create_progress_bar(self, progress: float) -> str:
        """Create simple text-based progress bar"""
        width = 20
        filled = int(progress * width)
        bar = "█" * filled + "░" * (width - filled)
        percentage = int(progress * 100)
        return f"[{bar}] {percentage}%"

    def _update_state_class(self) -> None:
        """Update CSS classes based on sub-module state"""
        # Remove all state classes
        self.remove_class("state-live")
        self.remove_class("state-transitioning")
        self.remove_class("state-completed")

        # Add current state class
        if self.sub_module.state == BlockState.LIVE:
            self.add_class("state-live")
        elif self.sub_module.state == BlockState.TRANSITIONING:
            self.add_class("state-transitioning")
        else:
            self.add_class("state-completed")

    def _start_timer(self):
        """Start the timer update task"""
        if not self._timer_task or self._timer_task.is_finished:
            self._timer_task = self._update_timer()

    @work(exclusive=True)
    async def _update_timer(self):
        """Update timer in background"""
        while self.sub_module.state == BlockState.LIVE and self.start_time:
            self.elapsed_time = time.time() - self.start_time
            await asyncio.sleep(0.1)

    def _on_sub_module_update(self, sub_module: LiveBlock) -> None:
        """Handle sub-module content updates"""
        # Check state transitions
        if sub_module.state == BlockState.LIVE and not self.start_time:
            # Started processing
            self.start_time = time.time()
            self._start_timer()
        elif sub_module.state == BlockState.INSCRIBED and self.start_time:
            # Finished processing - freeze timer
            self.end_time = time.time()
            self.elapsed_time = self.end_time - self.start_time
            if self._timer_task:
                self._timer_task.cancel()

        self._update_state_class()
        self.refresh()

    def _on_progress_update(self, sub_module: LiveBlock) -> None:
        """Handle sub-module progress updates"""
        self._update_state_class()
        self.refresh()
