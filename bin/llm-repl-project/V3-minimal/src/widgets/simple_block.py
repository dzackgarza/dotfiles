"""
Simple Block Widget - V3's Chatbox Pattern

Single widget that renders block content directly using render() method.
NO child containers - eliminates layout conflicts.
"""

from rich.console import RenderableType
from rich.text import Text
from rich.panel import Panel
from textual.widget import Widget
from typing import Union
from pathlib import Path

from ..core.live_blocks import LiveBlock, InscribedBlock, BlockState


class SimpleBlockWidget(Widget, can_focus=True):
    """Simple block widget using V3's Chatbox pattern - NO child containers

    Uses direct render() method like V3's Chatbox instead of child widgets.
    This eliminates nested container layout conflicts.
    """

    # Load CSS from external file
    _css_file = Path(__file__).parent / "simple_block.tcss"
    DEFAULT_CSS = _css_file.read_text() if _css_file.exists() else ""

    def __init__(self, block: Union[LiveBlock, InscribedBlock], **kwargs):
        super().__init__(**kwargs)
        self.block = block
        self.is_live = isinstance(block, LiveBlock)

        # CSS classes based on role (like V3's Chatbox)
        self.add_class("simple-block")
        self.add_class(f"block-{block.role}")

        if self.is_live:
            self.add_class("block-live")
            # Subscribe to live block updates
            if isinstance(self.block, LiveBlock):
                self.block.add_update_callback(self._on_block_update)
                self.block.add_progress_callback(self._on_progress_update)
        else:
            self.add_class("block-inscribed")

    def render(self) -> RenderableType:
        """Direct render like V3's Chatbox - no child widgets"""

        # Get block data
        if self.is_live and isinstance(self.block, LiveBlock):
            content = self.block.data.content
            wall_time = self.block.data.wall_time_seconds
            tokens_in = self.block.data.tokens_input
            tokens_out = self.block.data.tokens_output
            progress = self.block.data.progress
            state = self.block.state
        elif isinstance(self.block, InscribedBlock):
            content = self.block.content
            wall_time = self.block.metadata.get("wall_time_seconds", 0)
            tokens_in = self.block.metadata.get("tokens_input", 0)
            tokens_out = self.block.metadata.get("tokens_output", 0)
            progress = 1.0  # Completed
            state = None
        else:
            content = ""
            wall_time = 0
            tokens_in = 0
            tokens_out = 0
            progress = 0
            state = None

        # Build header
        header_parts = []

        # Role indicator emoji
        role_indicator = self._get_role_indicator()
        header_parts.append(f"{role_indicator} ")

        # State indicator for live blocks
        if self.is_live and state:
            state_indicator = self._get_state_indicator(state)
            header_parts.append(f"{state_indicator} ")

        # Role name
        header_parts.append(self.block.role.title())

        # Block ID for debugging
        block_id = self.block.id[:8] if len(self.block.id) > 8 else self.block.id
        header_parts.append(f" ({block_id})")

        header_text = "".join(header_parts)

        # Build metadata footer
        metadata_parts = []

        if wall_time > 0:
            metadata_parts.append(f"⏱️ {wall_time:.1f}s")

        if tokens_in > 0 or tokens_out > 0:
            metadata_parts.append(f"🎯 {tokens_in}↑/{tokens_out}↓")

        if self.is_live and progress > 0 and progress < 1.0:
            progress_pct = int(progress * 100)
            metadata_parts.append(f"📊 {progress_pct}%")

        if (
            self.is_live
            and isinstance(self.block, LiveBlock)
            and self.block._is_simulating
        ):
            metadata_parts.append("🔄 Simulating")

        metadata_text = " | ".join(metadata_parts) if metadata_parts else ""

        # Build content
        if not content:
            content = "[dim]No content yet...[/dim]"

        # Truncate very long content
        if len(content) > 2000:
            content = content[:1997] + "..."

        # Create panel like V3's bordered Chatbox
        panel_content = Text()
        panel_content.append(content)

        if metadata_text:
            panel_content.append("\n\n")
            panel_content.append(metadata_text, style="dim")

        # Border style based on role and state
        border_style = self._get_border_style()

        return Panel(
            panel_content, title=header_text, border_style=border_style, padding=(0, 1)
        )

    def _get_role_indicator(self) -> str:
        """Get indicator emoji for block role"""
        indicators = {
            "user": "👤",
            "assistant": "🤖",
            "cognition": "🧠",
            "tool": "🛠️",
            "system": "⚙️",
            "sub_module": "└─",
            "error": "❌",
            "route_query": "🎯",
            "call_tool": "🛠️",
            "format_output": "📝",
        }
        return indicators.get(self.block.role, "•")

    def _get_state_indicator(self, state: BlockState) -> str:
        """Get indicator for live block state"""
        if state == BlockState.LIVE:
            return "●"  # Live (green)
        elif state == BlockState.TRANSITIONING:
            return "⧗"  # Transitioning (yellow)
        else:
            return "◉"  # Inscribed (blue)

    def _get_border_style(self) -> str:
        """Get border style based on role and state"""
        if self.is_live and isinstance(self.block, LiveBlock):
            if self.block.state == BlockState.LIVE:
                return "green"
            elif self.block.state == BlockState.TRANSITIONING:
                return "yellow"
            else:
                return "blue"

        # Role-based colors for inscribed blocks
        role_colors = {
            "user": "green",
            "assistant": "blue",
            "cognition": "purple",
            "tool": "orange",
            "system": "cyan",
            "error": "red",
        }
        return role_colors.get(self.block.role, "white")

    def _on_block_update(self, block: LiveBlock) -> None:
        """Handle live block content updates"""
        self.refresh()

    def _on_progress_update(self, block: LiveBlock) -> None:
        """Handle live block progress updates"""
        self.refresh()

    def transition_to_inscribed(self, inscribed_block: InscribedBlock) -> None:
        """Handle transition from live to inscribed block

        Updates the widget to display the inscribed version
        without needing to recreate the widget.
        """
        if not self.is_live:
            return

        # Update internal state
        self.block = inscribed_block
        self.is_live = False

        # Update CSS classes
        self.remove_class("block-live")
        self.add_class("block-inscribed")

        # Refresh display
        self.refresh()
