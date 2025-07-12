"""
Sub-Module Widget - V3's Chatbox Pattern for Cognition

Single widget that renders sub-module content with streaming support.
Uses V3's render() method pattern - NO child containers.
"""

from rich.console import RenderableType
from rich.text import Text
from rich.panel import Panel
from textual.widget import Widget

from ..core.live_blocks import LiveBlock, BlockState


class SubModuleWidget(Widget, can_focus=True):
    """Sub-module widget using V3's Chatbox pattern - streaming support

    Uses direct render() method like V3's Chatbox for sub-modules.
    Handles streaming content updates without layout conflicts.
    """

    def __init__(self, sub_module: LiveBlock, **kwargs):
        super().__init__(**kwargs)
        self.sub_module = sub_module

        # CSS classes based on role (like V3's Chatbox)
        self.add_class("sub-module")
        self.add_class(f"sub-module-{sub_module.role}")

        # Subscribe to live updates
        self.sub_module.add_update_callback(self._on_sub_module_update)
        self.sub_module.add_progress_callback(self._on_progress_update)

        # State-based CSS classes
        self.add_class("sub-module-live")
        self._update_state_class()

    def render(self) -> RenderableType:
        """Direct render with streaming content like V3's Chatbox"""

        # Get sub-module data
        content = self.sub_module.data.content
        wall_time = self.sub_module.data.wall_time_seconds
        tokens_in = self.sub_module.data.tokens_input
        tokens_out = self.sub_module.data.tokens_output
        progress = self.sub_module.data.progress
        state = self.sub_module.state

        # Build header
        header_parts = []

        # Sub-module indicator
        header_parts.append("└─ ")

        # Role indicator emoji
        role_indicator = self._get_role_indicator()
        header_parts.append(f"{role_indicator} ")

        # State indicator
        state_indicator = self._get_state_indicator(state)
        header_parts.append(f"{state_indicator} ")

        # Role name
        header_parts.append(self.sub_module.role.replace("_", " ").title())

        # Sub-module ID for debugging
        sub_id = (
            self.sub_module.id[:8]
            if len(self.sub_module.id) > 8
            else self.sub_module.id
        )
        header_parts.append(f" ({sub_id})")

        header_text = "".join(header_parts)

        # Build content with streaming support
        if not content:
            if state == BlockState.LIVE:
                content_text = Text("Processing...", style="dim italic")
            else:
                content_text = Text("No content", style="dim")
        else:
            content_text = Text(content)

        # Add progress bar for active sub-modules
        if state == BlockState.LIVE and progress > 0 and progress < 1.0:
            progress_bar = self._create_progress_bar(progress)
            content_text.append("\n\n")
            content_text.append(progress_bar)

        # Build metadata footer
        metadata_parts = []

        if wall_time > 0:
            metadata_parts.append(f"⏱️ {wall_time:.1f}s")

        if tokens_in > 0 or tokens_out > 0:
            metadata_parts.append(f"🎯 {tokens_in}↑/{tokens_out}↓")

        if state == BlockState.LIVE and progress > 0:
            progress_pct = int(progress * 100)
            metadata_parts.append(f"📊 {progress_pct}%")

        if self.sub_module._is_simulating:
            metadata_parts.append("🔄 Simulating")

        if metadata_parts:
            metadata_text = " | ".join(metadata_parts)
            content_text.append("\n")
            content_text.append(metadata_text, style="dim")

        # Border style based on state
        border_style = self._get_border_style(state)

        return Panel(
            content_text, title=header_text, border_style=border_style, padding=(0, 1)
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

    def _on_sub_module_update(self, sub_module: LiveBlock) -> None:
        """Handle sub-module content updates"""
        self._update_state_class()
        self.refresh()

    def _on_progress_update(self, sub_module: LiveBlock) -> None:
        """Handle sub-module progress updates"""
        self._update_state_class()
        self.refresh()
