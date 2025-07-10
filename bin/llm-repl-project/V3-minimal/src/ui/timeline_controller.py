"""Timeline UI Controller implementing Observer pattern

Coordinates between Sacred Timeline state and UI widgets,
following the established architectural patterns from V2/V3.
"""

from typing import TYPE_CHECKING

from ..widgets.timeline import TimelineBlock as UITimelineBlock
from ..sacred_timeline import Block

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
    """

    def __init__(self, timeline_view: "TimelineView"):
        """Initialize the timeline view controller

        Args:
            timeline_view: The UI widget displaying the timeline
        """
        self.timeline_view = timeline_view

    def on_block_added(self, block: Block) -> None:
        """Handle timeline block addition (Observer pattern)

        Called when a new block is added to the Sacred Timeline.
        Converts the timeline block to a UI block and updates the view.

        Args:
            block: The timeline block that was added
        """
        ui_block = self._convert_to_ui_block(block)
        self.timeline_view.add_block(ui_block)

    def clear_timeline_view(self) -> None:
        """Clear the timeline view UI

        Used for timeline resets or application resets.
        """
        self.timeline_view.clear_timeline()

    def _convert_to_ui_block(self, timeline_block: Block) -> UITimelineBlock:
        """Convert a Sacred Timeline block to a UI timeline block

        Args:
            timeline_block: Block from the Sacred Timeline

        Returns:
            UI block ready for display in the timeline widget
        """
        return UITimelineBlock(
            timestamp=timeline_block.timestamp,
            role=timeline_block.role,
            content=timeline_block.content,
            id=timeline_block.id,
            metadata=timeline_block.metadata,
            time_taken=timeline_block.metadata.get("time_taken"),
            tokens_input=timeline_block.metadata.get("tokens_input"),
            tokens_output=timeline_block.metadata.get("tokens_output"),
        )
