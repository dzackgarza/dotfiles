"""
Unified Timeline Widget - V3.15

Single widget that handles both live and inscribed blocks from UnifiedTimeline.
Eliminates duplicate rendering and ownership conflicts.
"""

from dataclasses import dataclass
from textual.widgets import Static
from textual.containers import Vertical, VerticalScroll
from textual.message import Message
from rich.text import Text
from typing import List, Dict, Union
from pathlib import Path

from ..core.unified_timeline import (
    UnifiedTimeline,
    TimelineEvent,
    BlockAdded,
    BlockUpdated,
    BlockInscribed,
)
from ..core.live_blocks import LiveBlock, InscribedBlock, BlockState


class UnifiedBlockWidget(Vertical):
    """Single widget that can display either live or inscribed blocks

    This eliminates the need for separate widget types and handles
    state transitions smoothly.
    """

    # Load CSS from external file
    _css_file = Path(__file__).parent / "unified_timeline_widget.tcss"
    DEFAULT_CSS = _css_file.read_text() if _css_file.exists() else ""

    def __init__(self, block: Union[LiveBlock, InscribedBlock], **kwargs):
        super().__init__(**kwargs)
        self.block = block
        self.is_live = isinstance(block, LiveBlock)

        # Create child widgets
        self.header_widget = Static(classes="unified-block-header")
        self.content_widget = Static(classes="unified-block-content")
        self.metadata_widget = Static(classes="unified-block-metadata")
        self.sub_blocks_container = Vertical(classes="unified-sub-blocks")

        # Track sub-block widgets for live blocks
        self.sub_block_widgets: List[UnifiedBlockWidget] = []

        # Subscribe to updates if live block
        if self.is_live and isinstance(self.block, LiveBlock):
            self.block.add_update_callback(self._on_block_update)
            self.block.add_progress_callback(self._on_progress_update)

        # CSS classes based on type and state
        self.add_class("unified-block")
        if self.is_live:
            self.add_class("unified-block-live")
            self._update_state_class()
        else:
            self.add_class("unified-block-inscribed")

        # Role-specific classes
        self.add_class(f"unified-block-{self.block.role}")

    def compose(self):
        """Compose the widget layout"""
        yield self.header_widget
        yield self.content_widget
        yield self.metadata_widget
        yield self.sub_blocks_container

    def on_mount(self) -> None:
        """Initialize display when mounted"""
        self._update_all_displays()
        if self.is_live:
            self._update_sub_blocks()

    def _on_block_update(self, block: LiveBlock) -> None:
        """Handle live block content updates"""
        self._update_all_displays()
        self._update_sub_blocks()
        self._update_state_class()

    def _on_progress_update(self, block: LiveBlock) -> None:
        """Handle live block progress updates"""
        self._update_metadata()
        self._update_state_class()

    def _update_state_class(self) -> None:
        """Update CSS classes based on live block state"""
        if not self.is_live or not isinstance(self.block, LiveBlock):
            return

        # Remove all state classes
        self.remove_class("state-live")
        self.remove_class("state-transitioning")
        self.remove_class("state-inscribed")

        # Add current state class
        if self.block.state == BlockState.LIVE:
            self.add_class("state-live")
        elif self.block.state == BlockState.TRANSITIONING:
            self.add_class("state-transitioning")
        else:
            self.add_class("state-inscribed")

    def _update_all_displays(self) -> None:
        """Update all widget displays"""
        self._update_header()
        self._update_content()
        self._update_metadata()

    def _update_header(self) -> None:
        """Update header display"""
        header_text = Text()

        # Role indicator
        role_indicator = self._get_role_indicator()
        header_text.append(f"{role_indicator} ", style="bold")

        # State indicator for live blocks
        if self.is_live:
            state_indicator = self._get_state_indicator()
            header_text.append(f"{state_indicator} ", style="bold")

        # Role name
        header_text.append(self.block.role.title(), style="bold white")

        # Block ID for debugging
        block_id = self.block.id[:8] if len(self.block.id) > 8 else self.block.id
        header_text.append(f" ({block_id})", style="dim")

        self.header_widget.update(header_text)

    def _update_content(self) -> None:
        """Update content display"""
        if self.is_live and isinstance(self.block, LiveBlock):
            content = self.block.data.content
        elif isinstance(self.block, InscribedBlock):
            content = self.block.content
        else:
            content = ""

        if not content:
            content = "[dim]No content yet...[/dim]"

        # Truncate very long content
        if len(content) > 1000:
            content = content[:997] + "..."

        self.content_widget.update(content)

    def _update_metadata(self) -> None:
        """Update metadata display"""
        metadata_parts = []

        if self.is_live and isinstance(self.block, LiveBlock):
            # Live block metadata
            if self.block.data.wall_time_seconds > 0:
                metadata_parts.append(f"⏱️ {self.block.data.wall_time_seconds:.1f}s")

            if self.block.data.tokens_input > 0 or self.block.data.tokens_output > 0:
                metadata_parts.append(
                    f"🎯 {self.block.data.tokens_input}↑/{self.block.data.tokens_output}↓"
                )

            # Progress for non-cognition blocks
            if (
                self.block.cognition_progress is None
                and self.block.data.progress > 0
                and self.block.state == BlockState.LIVE
            ):
                progress_pct = int(self.block.data.progress * 100)
                metadata_parts.append(f"📊 {progress_pct}%")

            # Simulation status
            if self.block._is_simulating:
                metadata_parts.append("🔄 Simulating")

        elif isinstance(self.block, InscribedBlock):
            # Inscribed block metadata
            if "wall_time_seconds" in self.block.metadata:
                wall_time = self.block.metadata["wall_time_seconds"]
                metadata_parts.append(f"⏱️ {wall_time:.1f}s")

            if (
                "tokens_input" in self.block.metadata
                or "tokens_output" in self.block.metadata
            ):
                tokens_in = self.block.metadata.get("tokens_input", 0)
                tokens_out = self.block.metadata.get("tokens_output", 0)
                metadata_parts.append(f"🎯 {tokens_in}↑/{tokens_out}↓")

        if metadata_parts:
            metadata_text = " | ".join(metadata_parts)
            self.metadata_widget.update(metadata_text)
        else:
            self.metadata_widget.update("")

    def _update_sub_blocks(self) -> None:
        """Update sub-block displays for live blocks"""
        if (
            not self.is_live
            or not self.is_mounted
            or not isinstance(self.block, LiveBlock)
        ):
            return

        current_sub_blocks = self.block.data.sub_blocks

        # Remove widgets for sub-blocks that no longer exist
        for widget in self.sub_block_widgets[:]:
            if widget.block not in current_sub_blocks:
                try:
                    widget.remove()
                except Exception:
                    pass
                self.sub_block_widgets.remove(widget)

        # Add widgets for new sub-blocks
        for sub_block in current_sub_blocks:
            if not any(w.block == sub_block for w in self.sub_block_widgets):
                sub_widget = UnifiedBlockWidget(sub_block)
                self.sub_block_widgets.append(sub_widget)
                try:
                    self.sub_blocks_container.mount(sub_widget)
                except Exception:
                    # Container not ready yet
                    pass

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

    def _get_state_indicator(self) -> str:
        """Get indicator for live block state"""
        if not self.is_live or not isinstance(self.block, LiveBlock):
            return "◉"  # Always inscribed

        if self.block.state == BlockState.LIVE:
            return "●"  # Live (green)
        elif self.block.state == BlockState.TRANSITIONING:
            return "⧗"  # Transitioning (yellow)
        else:
            return "◉"  # Inscribed (blue)

    def transition_to_inscribed(self, inscribed_block: InscribedBlock) -> None:
        """Handle transition from live to inscribed block

        This updates the widget to display the inscribed version
        without needing to recreate the entire widget tree.
        """
        if not self.is_live:
            return

        # Update internal state
        self.block = inscribed_block
        self.is_live = False

        # Update CSS classes
        self.remove_class("unified-block-live")
        self.remove_class("state-live")
        self.remove_class("state-transitioning")
        self.add_class("unified-block-inscribed")

        # Clear sub-blocks (they're now in metadata)
        for widget in self.sub_block_widgets:
            try:
                widget.remove()
            except Exception:
                pass
        self.sub_block_widgets.clear()

        # Update displays
        self._update_all_displays()


class UnifiedTimelineWidget(VerticalScroll):
    """Main timeline widget using UnifiedTimeline

    Simple scrolling timeline like V3 - contains blocks directly.
    """

    # Load CSS from external file
    _css_file = Path(__file__).parent / "unified_timeline_widget.tcss"
    DEFAULT_CSS = _css_file.read_text() if _css_file.exists() else ""

    @dataclass
    class TimelineUpdated(Message):
        """Message sent when timeline is updated"""

        event: TimelineEvent

    def __init__(self, unified_timeline: UnifiedTimeline, **kwargs):
        super().__init__(**kwargs)
        self.unified_timeline = unified_timeline

        # Track block widgets
        self.block_widgets: Dict[str, UnifiedBlockWidget] = {}

        # Subscribe to timeline events
        self.unified_timeline.add_observer(self)

        # Smart auto-scroll state
        self.user_is_following = True
        self.auto_scroll_threshold = 100
        import time

        self.last_user_scroll_time = time.time()

        # CSS classes
        self.add_class("unified-timeline")

    def on_mount(self) -> None:
        """Initialize timeline display"""
        # Display existing blocks
        for block in self.unified_timeline.get_all_blocks():
            self.app.run_worker(
                self._add_block_widget(block), name=f"mount_block_{block.id}"
            )

    def on_scroll(self, event) -> None:
        """Handle scroll events for smart auto-scroll"""
        import time

        # Calculate distance from bottom
        max_scroll = self.max_scroll_y
        current_scroll = self.scroll_y
        distance_from_bottom = max_scroll - current_scroll

        # Update following state
        if distance_from_bottom <= self.auto_scroll_threshold:
            self.user_is_following = True
        else:
            self.user_is_following = False
            self.last_user_scroll_time = time.time()

    def on_timeline_event(self, event: TimelineEvent) -> None:
        """Handle timeline events (implements TimelineObserver protocol)"""
        if isinstance(event, BlockAdded):
            # Use run_worker to handle async mounting
            self.app.run_worker(self._add_block_widget(event.block), name="add_block")
        elif isinstance(event, BlockUpdated):
            # Widget updates automatically via callbacks
            pass
        elif isinstance(event, BlockInscribed):
            self._handle_block_inscription(event)

        # Post message for other components
        self.post_message(self.TimelineUpdated(event))

    async def _add_block_widget(self, block: Union[LiveBlock, InscribedBlock]) -> None:
        """Add widget for new block (mount into scroll container like V3)"""
        if block.id in self.block_widgets:
            return  # Already exists

        widget = UnifiedBlockWidget(block)
        self.block_widgets[block.id] = widget

        # Mount widget directly into this scroll container
        await self.mount(widget)

        # Smart auto-scroll
        if self._should_auto_scroll():
            self.call_after_refresh(self.scroll_end, animate=False, force=False)

    def _handle_block_inscription(self, event: BlockInscribed) -> None:
        """Handle live block becoming inscribed"""
        original_widget = self.block_widgets.get(event.original_live_id)
        if original_widget:
            # Update widget to show inscribed version
            original_widget.transition_to_inscribed(event.inscribed_block)

            # Update widget tracking (ID might have changed)
            if event.inscribed_block.id != event.original_live_id:
                del self.block_widgets[event.original_live_id]
                self.block_widgets[event.inscribed_block.id] = original_widget

    def _should_auto_scroll(self) -> bool:
        """Smart auto-scroll logic"""
        import time

        if not self.user_is_following:
            return False

        current_time = time.time()
        if current_time - self.last_user_scroll_time < 1.0:
            return False

        return True

    def clear_timeline(self) -> None:
        """Clear all blocks from display"""
        for widget in self.block_widgets.values():
            try:
                widget.remove()
            except Exception:
                pass
        self.block_widgets.clear()


# Create CSS file if it doesn't exist
_css_content = """
/* Unified Timeline Widget Styles */

.unified-timeline {
    padding: 1;
    background: $background;
}

.unified-block {
    margin: 1 0;
    padding: 1;
    border: solid $primary;
    border-radius: 1;
}

.unified-block-live {
    border: solid $success;
    background: $surface;
}

.unified-block-inscribed {
    border: solid $primary;
    background: $background;
}

.unified-block.state-live {
    border: solid $success;
}

.unified-block.state-transitioning {
    border: solid $warning;
    background: $warning 10%;
}

.unified-block.state-inscribed {
    border: solid $primary;
}

.unified-block-header {
    padding: 0 1;
    color: $text;
}

.unified-block-content {
    padding: 1;
    color: $text;
}

.unified-block-metadata {
    padding: 0 1;
    color: $text-muted;
}

.unified-sub-blocks {
    margin-left: 2;
    padding-left: 1;
    border-left: solid $text-muted;
}

/* Role-specific styling */
.unified-block-user {
    border-color: $success;
}

.unified-block-assistant {
    border-color: $primary;
}

.unified-block-cognition {
    border-color: $secondary;
}

.unified-block-tool {
    border-color: $accent;
}

.unified-block-error {
    border-color: $error;
}
"""

# Write CSS file
_css_file = Path(__file__).parent / "unified_timeline_widget.tcss"
if not _css_file.exists():
    _css_file.write_text(_css_content)
