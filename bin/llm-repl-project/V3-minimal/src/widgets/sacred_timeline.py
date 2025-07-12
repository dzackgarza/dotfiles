"""
Sacred Timeline Widget - V3's chat_container Pattern

Uses V3's proven VerticalScroll + simple widget children pattern.
Handles conversation history with turn separators.
"""

from textual.containers import VerticalScroll
from textual.widgets import Rule
from typing import List, Dict, Union
from pathlib import Path

from ..core.live_blocks import LiveBlock, InscribedBlock
from .simple_block import SimpleBlockWidget


class SacredTimelineWidget(VerticalScroll):
    """Sacred Timeline using V3's chat_container pattern

    Displays conversation history with turn separators.
    Uses V3's proven pattern: VerticalScroll with simple widget children.
    """

    # Load CSS from external file
    _css_file = Path(__file__).parent / "sacred_timeline.tcss"
    DEFAULT_CSS = _css_file.read_text() if _css_file.exists() else ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Track mounted widgets for management
        self.block_widgets: Dict[str, SimpleBlockWidget] = {}

        # CSS classes
        self.add_class("sacred-timeline")
        
        # Enable mouse wheel scrolling (like V3)
        self.can_focus = False

        # Smart auto-scroll state (like V3)
        self.user_is_following = True
        self.auto_scroll_threshold = 100
        import time

        self.last_user_scroll_time = time.time()

    async def add_block(self, block: Union[LiveBlock, InscribedBlock]) -> None:
        """Mount block like V3: await self.mount(SimpleBlockWidget(block))"""
        if block.id in self.block_widgets:
            return  # Already exists

        widget = SimpleBlockWidget(block)
        self.block_widgets[block.id] = widget

        # Mount widget directly (like V3's chat_container.mount)
        await self.mount(widget)

        # Smart auto-scroll (like V3's scroll_to_latest_message)
        if self._should_auto_scroll():
            self.call_after_refresh(self._scroll_to_latest)

    async def add_turn_separator(self) -> None:
        """Mount hrule like V3: await self.mount(Rule())"""
        separator = Rule(orientation="horizontal", classes="turn-separator")
        await self.mount(separator)

        # Auto-scroll after separator
        if self._should_auto_scroll():
            self.call_after_refresh(self._scroll_to_latest)

    def remove_block(self, block_id: str) -> None:
        """Remove block widget"""
        if block_id in self.block_widgets:
            widget = self.block_widgets[block_id]
            try:
                widget.remove()
            except Exception:
                pass
            del self.block_widgets[block_id]

    def clear_timeline(self) -> None:
        """Remove all widgets like V3's chat clearing"""
        for widget in self.block_widgets.values():
            try:
                widget.remove()
            except Exception:
                pass
        self.block_widgets.clear()

        # Also remove any separator rules
        for child in list(self.children):
            if isinstance(child, Rule):
                try:
                    child.remove()
                except Exception:
                    pass

    def update_block(self, block: Union[LiveBlock, InscribedBlock]) -> None:
        """Update existing block widget"""
        if block.id in self.block_widgets:
            widget = self.block_widgets[block.id]
            widget.block = block
            widget.refresh()

    def transition_block_to_inscribed(
        self, original_live_id: str, inscribed_block: InscribedBlock
    ) -> None:
        """Handle live block becoming inscribed"""
        original_widget = self.block_widgets.get(original_live_id)
        if original_widget:
            # Update widget to show inscribed version
            original_widget.transition_to_inscribed(inscribed_block)

            # Update widget tracking (ID might have changed)
            if inscribed_block.id != original_live_id:
                del self.block_widgets[original_live_id]
                self.block_widgets[inscribed_block.id] = original_widget

    def on_scroll(self, event) -> None:
        """Handle scroll events for smart auto-scroll (like V3)"""
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

    def _scroll_to_latest(self) -> None:
        """Scroll to latest message (like V3's scroll_to_latest_message)"""
        self.refresh()
        self.scroll_end(animate=False, force=True)

    def _should_auto_scroll(self) -> bool:
        """Smart auto-scroll logic (like V3)"""
        import time

        if not self.user_is_following:
            return False

        current_time = time.time()
        if current_time - self.last_user_scroll_time < 1.0:
            return False

        return True

    def get_block_count(self) -> int:
        """Get number of blocks in timeline"""
        return len(self.block_widgets)

    def get_blocks(self) -> List[SimpleBlockWidget]:
        """Get all block widgets"""
        return list(self.block_widgets.values())
