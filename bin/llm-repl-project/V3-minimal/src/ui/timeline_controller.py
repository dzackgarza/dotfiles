"""Timeline UI Controller implementing Observer pattern

Coordinates between Sacred Timeline state and UI widgets,
following the established architectural patterns from V2/V3.
"""

from typing import TYPE_CHECKING, Dict

from ..widgets.timeline import TimelineBlock as UITimelineBlock, SubBlock as UISubBlock
from ..widgets.live_block_widget import LiveBlockWidget
from ..sacred_timeline import Block
from ..core.live_blocks import LiveBlock

if TYPE_CHECKING:
    from ..widgets.timeline import TimelineView


class TimelineViewController:
    """Coordinates between timeline state and UI widgets

    Implements the Observer pattern to keep UI in sync with Sacred Timeline.
    This follows the established V3 pattern of separating timeline state
    management from UI coordination.

    Responsibilities:
    - Observe Sacred Timeline changes
    - Convert timeline blocks to UI blocks
    - Update timeline view widget
    - Maintain UI state consistency
    - Handle live block updates
    """

    def __init__(self, timeline_view: "TimelineView"):
        """Initialize the timeline view controller

        Args:
            timeline_view: The UI widget displaying the timeline
        """
        self.timeline_view = timeline_view
        self.live_block_widgets: Dict[str, LiveBlockWidget] = {}

    def on_block_added(self, block: Block) -> None:
        """Handle timeline block addition (Observer pattern)

        Called when a new block is added to the Sacred Timeline.
        Converts the timeline block to a UI block and updates the view.

        Args:
            block: The timeline block that was added
        """
        # Check if this block already has a live widget (to prevent duplicates)
        if block.metadata.get("_has_live_widget", False):
            # Skip creating a new widget - the live widget will handle the display
            return

        ui_block = self._convert_to_ui_block(block)
        self.timeline_view.add_block(ui_block)

    def clear_timeline_view(self) -> None:
        """Clear the timeline view UI

        Used for timeline resets or application resets.
        """
        self.timeline_view.clear_timeline()

    def on_live_block_update(self, live_block: LiveBlock) -> None:
        """Handle live block updates

        Args:
            live_block: The live block that was updated
        """
        block_id = live_block.id

        # Check if we already have a widget for this live block
        if block_id not in self.live_block_widgets:
            # Create a new live block widget with the LiveBlock instance
            live_widget = LiveBlockWidget(live_block)

            # Add to timeline view
            self.timeline_view.add_live_block_widget(live_widget)
            self.live_block_widgets[block_id] = live_widget
        # The widget self-updates via callbacks, no need to manually update

        # Check if block is being inscribed
        if live_block.state.value == "inscribed":
            # Transform the live widget to inscribed state (don't remove)
            if block_id in self.live_block_widgets:
                # The widget will visually update itself based on state
                # Don't remove it - let it persist in the timeline
                pass

    def _convert_to_ui_block(self, timeline_block: Block) -> UITimelineBlock:
        """Convert a Sacred Timeline block to a UI timeline block

        Args:
            timeline_block: Block from the Sacred Timeline

        Returns:
            UI block ready for display in the timeline widget
        """
        # Convert sub-blocks
        ui_sub_blocks = []
        for sub_block in timeline_block.sub_blocks:
            ui_sub_blocks.append(
                UISubBlock(
                    id=sub_block.id,
                    type=sub_block.type,
                    content=sub_block.content,
                    timestamp=sub_block.timestamp,
                )
            )

        return UITimelineBlock(
            timestamp=timeline_block.timestamp,
            role=timeline_block.role,
            content=timeline_block.content,
            id=timeline_block.id,
            metadata=timeline_block.metadata,
            time_taken=timeline_block.time_taken,
            tokens_input=timeline_block.tokens_input,
            tokens_output=timeline_block.tokens_output,
            sub_blocks=ui_sub_blocks,
        )
