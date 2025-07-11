"""
Live Block Widget - Textual UI components for live vs inscribed blocks

Provides visual representation of live blocks with real-time updates,
proper nesting for sub-blocks, and visual state indicators.
"""

from textual.widgets import Static
from textual.containers import Vertical
from rich.text import Text
from typing import List
import asyncio

from ..core.live_blocks import LiveBlock, BlockState


class LiveBlockWidget(Vertical):
    """Widget for displaying live blocks with real-time updates."""

    DEFAULT_CSS = """
    LiveBlockWidget {
        border: round $primary;
        margin-bottom: 1;
        padding: 1;
        height: auto;
        min-height: 5;
    }

    .live-block {
        border: round $success;
        background: $surface;
    }

    .transitioning-block {
        border: round $warning;
        background: $surface;
    }

    .inscribed-block {
        border: round $primary;
        background: $surface;
    }

    .block-header {
        text-style: bold;
        color: $text;
        margin-bottom: 1;
    }

    .block-content {
        color: $text;
        margin-bottom: 1;
    }

    .block-metadata {
        color: $text-muted;
        text-style: dim;
    }

    .sub-blocks-container {
        margin-left: 2;
        border-left: solid $accent;
        padding-left: 1;
    }
    """

    def __init__(self, live_block: LiveBlock, **kwargs):
        super().__init__(**kwargs)
        self.live_block = live_block

        # Create child widgets
        self.header_widget = Static(classes="block-header")
        self.content_widget = Static(classes="block-content")
        self.progress_widget = Static()
        self.metadata_widget = Static(classes="block-metadata")
        self.sub_blocks_container = Vertical(classes="sub-blocks-container")

        # Subscribe to block updates
        self.live_block.add_update_callback(self._on_block_update)

        # Track sub-block widgets
        self.sub_block_widgets: List[LiveBlockWidget] = []

        # Initial update (only if in app context)
        try:
            self._update_all_displays()
        except Exception:
            # Widget not in app context (e.g., during testing)
            pass

    def compose(self):
        """Compose the widget layout."""
        yield self.header_widget
        yield self.content_widget
        yield self.progress_widget
        yield self.metadata_widget
        yield self.sub_blocks_container

    def _on_block_update(self, block: LiveBlock) -> None:
        """Update display when block data changes."""
        self._update_all_displays()
        self._update_sub_blocks()

    def _update_all_displays(self) -> None:
        """Update all widget displays."""
        self._update_header()
        self._update_content()
        self._update_progress()
        self._update_metadata()
        self._update_css_classes()

    def _update_css_classes(self) -> None:
        """Update CSS classes based on block state."""
        # Remove all state classes
        self.remove_class("live-block")
        self.remove_class("transitioning-block")
        self.remove_class("inscribed-block")

        # Add appropriate state class
        if self.live_block.state == BlockState.LIVE:
            self.add_class("live-block")
        elif self.live_block.state == BlockState.TRANSITIONING:
            self.add_class("transitioning-block")
        else:
            self.add_class("inscribed-block")

    def _update_header(self) -> None:
        """Update header display."""
        header_text = Text()

        # Add role indicator
        role_indicator = self._get_role_indicator()
        header_text.append(f"{role_indicator} ", style="bold")

        # Add state indicator
        state_indicator = self._get_state_indicator()
        header_text.append(f"{state_indicator} ", style="bold")

        # Add role name
        header_text.append(self.live_block.role.title(), style="bold white")

        # Add ID for debugging
        if len(self.live_block.id) > 8:
            short_id = self.live_block.id[:8]
            header_text.append(f" ({short_id})", style="dim")

        self.header_widget.update(header_text)

    def _update_content(self) -> None:
        """Update content display."""
        content = self.live_block.data.content
        if not content:
            content = "[dim]No content yet...[/dim]"

        # Truncate very long content for better display
        if len(content) > 500:
            content = content[:497] + "..."

        self.content_widget.update(content)

    def _update_progress(self) -> None:
        """Update progress display."""
        if (
            self.live_block.state == BlockState.LIVE
            and self.live_block.data.progress > 0
        ):

            progress_text = Text()
            progress_text.append("Progress: ")

            # Simple progress bar
            bar_length = 20
            filled = int(self.live_block.data.progress * bar_length)
            bar = "█" * filled + "░" * (bar_length - filled)
            progress_text.append(
                f"[{bar}] {self.live_block.data.progress:.1%}", style="cyan"
            )

            self.progress_widget.update(progress_text)
        else:
            self.progress_widget.update("")

    def _update_metadata(self) -> None:
        """Update metadata display."""
        metadata_parts = []

        # Timing
        if self.live_block.data.wall_time_seconds > 0:
            metadata_parts.append(f"⏱️ {self.live_block.data.wall_time_seconds:.1f}s")

        # Tokens
        if (
            self.live_block.data.tokens_input > 0
            or self.live_block.data.tokens_output > 0
        ):
            metadata_parts.append(
                f"🎯 {self.live_block.data.tokens_input}↑/{self.live_block.data.tokens_output}↓"
            )

        # Sub-blocks count
        if self.live_block.data.sub_blocks:
            metadata_parts.append(
                f"📦 {len(self.live_block.data.sub_blocks)} sub-blocks"
            )

        # Simulation status
        if self.live_block._is_simulating:
            metadata_parts.append("🔄 Simulating")

        if metadata_parts:
            metadata_text = " | ".join(metadata_parts)
            self.metadata_widget.update(metadata_text)
        else:
            self.metadata_widget.update("")

    def _update_sub_blocks(self) -> None:
        """Update sub-block displays."""
        current_sub_blocks = self.live_block.data.sub_blocks

        # Remove widgets for sub-blocks that no longer exist
        for widget in self.sub_block_widgets[:]:
            if widget.live_block not in current_sub_blocks:
                try:
                    widget.remove()
                except Exception:
                    pass
                self.sub_block_widgets.remove(widget)

        # Add widgets for new sub-blocks
        for sub_block in current_sub_blocks:
            if not any(w.live_block == sub_block for w in self.sub_block_widgets):
                sub_widget = LiveBlockWidget(sub_block)
                self.sub_block_widgets.append(sub_widget)
                try:
                    self.sub_blocks_container.mount(sub_widget)
                except Exception:
                    # Container not mounted yet (e.g., during testing)
                    pass

        # Show/hide sub-blocks container
        if current_sub_blocks:
            self.sub_blocks_container.display = True
        else:
            self.sub_blocks_container.display = False

    def _get_role_indicator(self) -> str:
        """Get indicator emoji for block role."""
        indicators = {
            "user": "👤",
            "assistant": "🤖",
            "cognition": "🧠",
            "tool": "🛠️",
            "system": "⚙️",
            "sub_module": "└─",
            "error": "❌",
        }
        return indicators.get(self.live_block.role, "•")

    def _get_state_indicator(self) -> str:
        """Get indicator for block state."""
        if self.live_block.state == BlockState.LIVE:
            return "●"  # Live (green)
        elif self.live_block.state == BlockState.TRANSITIONING:
            return "⧗"  # Transitioning (yellow)
        else:
            return "◉"  # Inscribed (blue)


class LiveBlockManagerWidget(Vertical):
    """Widget for displaying all live blocks from a LiveBlockManager."""

    DEFAULT_CSS = """
    LiveBlockManagerWidget {
        height: auto;
        width: 100%;
    }

    .manager-header {
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
        padding: 1;
        border-bottom: solid $accent;
    }

    .no-blocks {
        color: $text-muted;
        text-style: dim;
        text-align: center;
        padding: 2;
    }
    """

    def __init__(self, live_block_manager, **kwargs):
        super().__init__(**kwargs)
        self.live_block_manager = live_block_manager
        self.block_widgets: List[LiveBlockWidget] = []

        # Header widget
        self.header_widget = Static(classes="manager-header")
        self.no_blocks_widget = Static(
            "No live blocks currently active", classes="no-blocks"
        )

        # Subscribe to manager updates
        self.live_block_manager.add_block_update_callback(self._on_manager_update)

        # Initial display
        self._update_display()

    def compose(self):
        """Compose the widget layout."""
        yield self.header_widget
        yield self.no_blocks_widget

    def _on_manager_update(self, block: LiveBlock) -> None:
        """Handle updates from the block manager."""
        self._update_display()

    def _update_display(self) -> None:
        """Update the display of all live blocks."""
        self._update_header()
        self._update_block_widgets()

    def _update_header(self) -> None:
        """Update header with current status."""
        live_blocks = self.live_block_manager.get_live_blocks()
        count = len(live_blocks)

        if count == 0:
            header_text = "🔄 Live Block Manager - No active blocks"
        else:
            header_text = f"🔄 Live Block Manager - {count} active block{'s' if count != 1 else ''}"

        self.header_widget.update(header_text)

    def _update_block_widgets(self) -> None:
        """Update the list of block widgets."""
        current_blocks = self.live_block_manager.get_live_blocks()

        # Remove widgets for blocks that no longer exist
        for widget in self.block_widgets[:]:
            if widget.live_block not in current_blocks:
                try:
                    widget.remove()
                except Exception:
                    # Widget might not be mounted
                    pass
                self.block_widgets.remove(widget)

        # Add widgets for new blocks
        for block in current_blocks:
            if not any(w.live_block == block for w in self.block_widgets):
                block_widget = LiveBlockWidget(block)
                self.block_widgets.append(block_widget)
                try:
                    self.mount(block_widget)
                except Exception:
                    # Widget not mounted yet - skip mounting
                    pass

        # Show/hide no blocks message
        if current_blocks:
            self.no_blocks_widget.display = False
        else:
            self.no_blocks_widget.display = True


class BlockTransitionWidget(Static):
    """Widget for displaying block state transitions."""

    DEFAULT_CSS = """
    BlockTransitionWidget {
        height: 3;
        width: 100%;
        text-align: center;
        padding: 1;
        border: dashed $accent;
        margin: 1 0;
    }

    .transition-active {
        border: solid $warning;
        background: $warning 10%;
    }
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_transitioning = False

    def show_transition(self, from_state: BlockState, to_state: BlockState) -> None:
        """Show a transition animation."""
        self.is_transitioning = True
        self.add_class("transition-active")

        transition_text = f"⧗ Transitioning: {from_state.value} → {to_state.value}"
        self.update(transition_text)

        # Auto-hide after a delay (only if event loop is running)
        try:
            asyncio.create_task(self._hide_after_delay())
        except RuntimeError:
            # No event loop running (e.g., during testing)
            pass

    async def _hide_after_delay(self) -> None:
        """Hide the transition after a delay."""
        await asyncio.sleep(2.0)
        self.hide_transition()

    def hide_transition(self) -> None:
        """Hide the transition display."""
        self.is_transitioning = False
        self.remove_class("transition-active")
        self.update("")


class LiveBlockDemoWidget(Vertical):
    """Demo widget showing live block capabilities."""

    DEFAULT_CSS = """
    LiveBlockDemoWidget {
        height: auto;
        width: 100%;
        padding: 1;
    }

    .demo-header {
        text-style: bold;
        color: $primary;
        text-align: center;
        margin-bottom: 2;
    }

    .demo-controls {
        text-align: center;
        margin: 1 0;
        padding: 1;
        border: round $accent;
    }
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create demo components
        self.header_widget = Static("🧠 Live Block System Demo", classes="demo-header")

        self.controls_widget = Static(
            "Press 'c' for cognition demo, 'a' for assistant demo, 'q' to quit",
            classes="demo-controls",
        )

        # Demo manager and widgets
        from ..core.live_blocks import LiveBlockManager

        self.demo_manager = LiveBlockManager()
        self.manager_widget = LiveBlockManagerWidget(self.demo_manager)

        self.transition_widget = BlockTransitionWidget()

    def compose(self):
        """Compose the demo layout."""
        yield self.header_widget
        yield self.controls_widget
        yield self.transition_widget
        yield self.manager_widget

    async def demo_cognition_pipeline(self) -> None:
        """Demonstrate a cognition pipeline."""
        block = self.demo_manager.create_live_block(
            "cognition", "Starting cognition demo..."
        )

        # Show transition
        self.transition_widget.show_transition(BlockState.LIVE, BlockState.LIVE)

        # Run simulation
        await block.start_mock_simulation("cognition")

        # Wait a moment, then inscribe
        await asyncio.sleep(2.0)
        self.transition_widget.show_transition(BlockState.LIVE, BlockState.INSCRIBED)

        inscribed = self.demo_manager.inscribe_block(block.id)
        return inscribed

    async def demo_assistant_response(self) -> None:
        """Demonstrate an assistant response."""
        block = self.demo_manager.create_live_block(
            "assistant", "Preparing response..."
        )

        self.transition_widget.show_transition(BlockState.LIVE, BlockState.LIVE)

        await block.start_mock_simulation("assistant_response")

        await asyncio.sleep(1.0)
        self.transition_widget.show_transition(BlockState.LIVE, BlockState.INSCRIBED)

        inscribed = self.demo_manager.inscribe_block(block.id)
        return inscribed

    def on_key(self, event) -> None:
        """Handle key presses for demo controls."""
        if event.key == "c":
            asyncio.create_task(self.demo_cognition_pipeline())
        elif event.key == "a":
            asyncio.create_task(self.demo_assistant_response())
        elif event.key == "q":
            self.app.exit()
