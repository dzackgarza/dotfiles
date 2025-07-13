"""
Unified Timeline Architecture - V3.15

Single source of truth for all blocks (live and inscribed).
Eliminates dual-system architectural conflicts by making Timeline own everything.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Union, Protocol, Any
import asyncio

from .live_blocks import LiveBlock, InscribedBlock, BlockState
from ..widgets.timeline import TimelineBlock
from .wall_time_tracker import (
    track_block_creation,
    time_block_stage,
    complete_block_tracking,
)


class TimelineEvent:
    """Base class for timeline events"""

    pass


@dataclass
class BlockAdded(TimelineEvent):
    """Event fired when a block is added to timeline"""

    block: Union[LiveBlock, InscribedBlock]


@dataclass
class BlockUpdated(TimelineEvent):
    """Event fired when a block is updated"""

    block: Union[LiveBlock, InscribedBlock]


@dataclass
class BlockInscribed(TimelineEvent):
    """Event fired when a live block becomes inscribed"""

    inscribed_block: InscribedBlock
    original_live_id: str


class TimelineObserver(Protocol):
    """Protocol for timeline observers"""

    def on_timeline_event(self, event: TimelineEvent) -> None:
        """Handle timeline events"""
        ...


class UnifiedTimeline:
    """Single timeline that handles both live and inscribed blocks

    This eliminates the fundamental ownership conflict between LiveBlockManager
    and Timeline by making Timeline the single source of truth for all blocks.

    Architecture:
    - Timeline owns all blocks (live and inscribed)
    - LiveBlockManager becomes a pure factory (no ownership)
    - Atomic inscription preserves complete block structures
    - Single widget tree matches timeline structure
    """

    def __init__(self):
        # Single list containing both live and inscribed blocks
        self._blocks: List[Union[LiveBlock, InscribedBlock]] = []

        # Observer pattern for UI updates
        self._observers: List[TimelineObserver] = []

        # Index for fast lookup
        self._block_index: Dict[str, Union[LiveBlock, InscribedBlock]] = {}

        # State tracking
        self._inscription_lock = asyncio.Lock()

    def add_observer(self, observer: TimelineObserver) -> None:
        """Add observer for timeline events"""
        self._observers.append(observer)

    def remove_observer(self, observer: TimelineObserver) -> None:
        """Remove observer"""
        if observer in self._observers:
            self._observers.remove(observer)

    def _notify_observers(self, event: TimelineEvent) -> None:
        """Notify all observers of timeline event"""
        for observer in self._observers:
            try:
                observer.on_timeline_event(event)
            except Exception as e:
                print(f"Error in timeline observer: {e}")

    def add_live_block(self, role: str, content: str = "") -> LiveBlock:
        """Create and add a live block to timeline

        The block is immediately added to the timeline in live state.
        UI can show it with live styling while it updates.
        """
        # Time the block creation process
        with time_block_stage("timeline_creation", "creation"):
            block = LiveBlock(role, content)

            # Add to timeline immediately
            self._blocks.append(block)
            self._block_index[block.id] = block

            # Set up callback to notify observers when block updates
            block.add_update_callback(self._on_live_block_update)

        # Notify observers
        self._notify_observers(BlockAdded(block))

        return block

    def _on_live_block_update(self, block: LiveBlock) -> None:
        """Handle live block updates"""
        self._notify_observers(BlockUpdated(block))

    def get_block(self, block_id: str) -> Optional[Union[LiveBlock, InscribedBlock]]:
        """Get block by ID"""
        return self._block_index.get(block_id)

    def owns_block(self, block_id: str) -> bool:
        """Check if timeline owns this block"""
        return block_id in self._block_index

    def get_all_blocks(self) -> List[Union[LiveBlock, InscribedBlock]]:
        """Get all blocks in timeline order"""
        return self._blocks.copy()

    def get_live_blocks(self) -> List[LiveBlock]:
        """Get only live blocks"""
        return [block for block in self._blocks if isinstance(block, LiveBlock)]

    def get_inscribed_blocks(self) -> List[InscribedBlock]:
        """Get only inscribed blocks"""
        return [block for block in self._blocks if isinstance(block, InscribedBlock)]

    async def inscribe_block(self, block_id: str, force: bool = False) -> Optional[InscribedBlock]:
        """Atomically convert live block to inscribed, including all sub-blocks

        This is the critical method that fixes the ownership conflicts.
        It converts the complete live block tree to inscribed state atomically.
        Now includes comprehensive validation and error handling.
        
        Args:
            block_id: ID of the block to inscribe
            force: Skip validation checks if True (use with caution)
        """
        from .block_state_transitions import transition_manager, ValidationError, InscriptionError
        
        async with self._inscription_lock:
            # Find the live block
            live_block = self._block_index.get(block_id)
            if not live_block or not isinstance(live_block, LiveBlock):
                return None

            try:
                # Use the new transition manager for safe inscription
                inscribed_block = await transition_manager.transition_to_inscribed(
                    block=live_block,
                    force=force,
                    auto_recover=True
                )
                
                if not inscribed_block:
                    return None

                # Atomic replacement in timeline
                block_index = self._blocks.index(live_block)
                self._blocks[block_index] = inscribed_block

                # Update index
                del self._block_index[block_id]
                self._block_index[inscribed_block.id] = inscribed_block

                # Notify observers
                self._notify_observers(BlockInscribed(inscribed_block, block_id))

                return inscribed_block
                
            except (ValidationError, InscriptionError) as e:
                print(f"Failed to inscribe block {block_id}: {e}")
                # Block remains in live state
                return None
            except Exception as e:
                print(f"Unexpected error inscribing block {block_id}: {e}")
                return None

    async def validate_block_for_inscription(self, block_id: str) -> Optional[Dict[str, Any]]:
        """Validate if a block is ready for inscription.
        
        Returns:
            Dictionary with validation results, or None if block not found
        """
        from .block_state_transitions import transition_manager
        
        live_block = self._block_index.get(block_id)
        if not live_block or not isinstance(live_block, LiveBlock):
            return None
        
        try:
            validation_result = await transition_manager.validate_transition(
                live_block, 
                BlockState.INSCRIBED
            )
            
            return {
                'is_valid': validation_result.is_valid,
                'failed_conditions': [c.value for c in validation_result.failed_conditions],
                'errors': validation_result.error_messages,
                'warnings': validation_result.warnings,
                'block_id': block_id
            }
        except Exception as e:
            return {
                'is_valid': False,
                'failed_conditions': [],
                'errors': [f"Validation error: {e}"],
                'warnings': [],
                'block_id': block_id
            }

    def get_blocks_ready_for_inscription(self) -> List[str]:
        """Get IDs of live blocks that appear ready for inscription.
        
        This is a synchronous check based on basic conditions.
        Use validate_block_for_inscription() for comprehensive async validation.
        """
        ready_block_ids = []
        
        for block in self.get_live_blocks():
            # Basic readiness checks
            if (block.data.progress >= 1.0 and 
                block.data.content.strip() and
                not block._is_simulating and
                block.state == BlockState.LIVE):
                ready_block_ids.append(block.id)
        
        return ready_block_ids

    def add_sub_block(
        self, parent_id: str, role: str, content: str = ""
    ) -> Optional[LiveBlock]:
        """Add sub-block to existing live block

        Sub-blocks are owned by their parent - they never exist independently.
        This prevents the orphaned sub-block problem.
        """
        parent_block = self._block_index.get(parent_id)
        if not parent_block or not isinstance(parent_block, LiveBlock):
            return None

        # Create sub-block
        sub_block = LiveBlock(role, content)

        # Add to parent (parent owns it, not timeline)
        parent_block.add_sub_block(sub_block)

        # Sub-blocks are NOT added to timeline index - parent owns them
        # This prevents duplicate rendering and ownership conflicts

        return sub_block

    def clear_all_live_blocks(self) -> None:
        """Stop all live block simulations"""
        for block in self.get_live_blocks():
            block.stop_simulation()

    def to_timeline_blocks(self) -> List[TimelineBlock]:
        """Convert to legacy TimelineBlock format for compatibility

        This allows gradual migration from old timeline system.
        """
        timeline_blocks = []

        for block in self._blocks:
            if isinstance(block, InscribedBlock):
                # Convert inscribed block
                timeline_block = TimelineBlock(
                    id=block.id,
                    timestamp=block.timestamp,
                    role=block.role,
                    content=block.content,
                    metadata=block.metadata.copy(),
                    time_taken=block.metadata.get("wall_time_seconds"),
                    tokens_input=block.metadata.get("tokens_input"),
                    tokens_output=block.metadata.get("tokens_output"),
                    sub_blocks=[],  # Sub-blocks are in metadata for inscribed blocks
                )
                timeline_blocks.append(timeline_block)

            elif isinstance(block, LiveBlock):
                # Convert live block (for current display)
                timeline_block = TimelineBlock(
                    id=block.id,
                    timestamp=block.created_at,
                    role=block.role,
                    content=block.data.content,
                    metadata=block.data.metadata.copy(),
                    time_taken=block.data.wall_time_seconds,
                    tokens_input=block.data.tokens_input,
                    tokens_output=block.data.tokens_output,
                    sub_blocks=[],  # Live sub-blocks handled separately
                )
                timeline_blocks.append(timeline_block)

        return timeline_blocks


class UnifiedTimelineManager:
    """Manages multiple timeline instances and provides factory methods

    This replaces LiveBlockManager but with clear ownership boundaries.
    """

    def __init__(self):
        self.timeline = UnifiedTimeline()

    def create_live_block(self, role: str, initial_content: str = "") -> LiveBlock:
        """Create live block - delegates to timeline for ownership"""
        return self.timeline.add_live_block(role, initial_content)

    def add_sub_block(
        self, parent_id: str, role: str, content: str = ""
    ) -> Optional[LiveBlock]:
        """Add sub-block to parent - delegates to timeline"""
        return self.timeline.add_sub_block(parent_id, role, content)

    async def inscribe_block(self, block_id: str) -> Optional[InscribedBlock]:
        """Inscribe block - delegates to timeline"""
        return await self.timeline.inscribe_block(block_id)

    def get_timeline(self) -> UnifiedTimeline:
        """Get the unified timeline"""
        return self.timeline

    def stop_all_simulations(self) -> None:
        """Stop all live simulations"""
        self.timeline.clear_all_live_blocks()
