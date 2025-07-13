"""
Live Block Staging Area Implementation

Provides a staging area for live blocks before they are inscribed to the Sacred Timeline.
This allows for real-time updates, token tracking, and wall-time monitoring of blocks
during processing before they become permanent.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Callable, Any
from threading import Lock
import uuid
import time

from .live_blocks import LiveBlock, BlockState, LiveBlockData
from .block_metadata import BlockMetadata, ProcessingStage, BlockRole


@dataclass
class StagingAreaMetrics:
    """Aggregate metrics for the staging area"""
    
    total_blocks_staged: int = 0
    total_blocks_inscribed: int = 0
    total_tokens_input: int = 0
    total_tokens_output: int = 0
    total_wall_time: float = 0.0
    active_blocks: int = 0
    
    def update_from_block(self, block: LiveBlock, action: str = "add") -> None:
        """Update metrics based on block action"""
        if action == "add":
            self.total_blocks_staged += 1
            self.active_blocks += 1
        elif action == "inscribe":
            self.total_blocks_inscribed += 1
            self.active_blocks -= 1
            self.total_tokens_input += block.data.tokens_input
            self.total_tokens_output += block.data.tokens_output
            self.total_wall_time += block.data.wall_time_seconds
        elif action == "remove":
            self.active_blocks -= 1


class LiveBlockStagingArea:
    """
    Staging area for live blocks before inscription to Sacred Timeline.
    
    This class manages the lifecycle of live blocks from creation through
    inscription, providing real-time visibility into processing operations.
    Features include:
    - Thread-safe block management
    - Real-time metrics tracking
    - Event callbacks for UI updates
    - Block retrieval and filtering
    - Concurrent block support
    """
    
    def __init__(self):
        """Initialize the staging area"""
        self._blocks: Dict[str, LiveBlock] = {}
        self._lock = Lock()
        self._metrics = StagingAreaMetrics()
        
        # Callbacks for different events
        self._on_block_added: List[Callable[[LiveBlock], None]] = []
        self._on_block_updated: List[Callable[[LiveBlock], None]] = []
        self._on_block_inscribed: List[Callable[[LiveBlock], None]] = []
        self._on_block_removed: List[Callable[[str], None]] = []
        
        # Block ordering for display
        self._block_order: List[str] = []
        
    def add_block(self, block: LiveBlock) -> None:
        """
        Add a new live block to the staging area.
        
        Args:
            block: The LiveBlock to add
            
        Raises:
            ValueError: If block with same ID already exists
        """
        with self._lock:
            if block.id in self._blocks:
                raise ValueError(f"Block with ID {block.id} already exists in staging")
                
            self._blocks[block.id] = block
            self._block_order.append(block.id)
            self._metrics.update_from_block(block, action="add")
            
            # Set up block update callbacks
            block.add_update_callback(self._handle_block_update)
            block.add_progress_callback(self._handle_block_progress)
            
        # Notify listeners outside lock
        self._notify_block_added(block)
        
    def create_block(self, role: BlockRole, content: str = "", **metadata) -> LiveBlock:
        """
        Create and add a new live block to the staging area.
        
        Args:
            role: The block role (user, assistant, cognition, etc.)
            content: Initial content for the block
            **metadata: Additional metadata for the block
            
        Returns:
            The created LiveBlock
        """
        # Create block with role and initial content
        block = LiveBlock(role=role.value, initial_content=content)
        
        # Add metadata
        if metadata:
            block.data.metadata.update(metadata)
        
        self.add_block(block)
        return block
        
    def get_block(self, block_id: str) -> Optional[LiveBlock]:
        """
        Retrieve a block by ID.
        
        Args:
            block_id: The block ID
            
        Returns:
            The LiveBlock if found, None otherwise
        """
        with self._lock:
            return self._blocks.get(block_id)
            
    def get_all_blocks(self) -> List[LiveBlock]:
        """
        Get all blocks in the staging area in order.
        
        Returns:
            List of LiveBlocks in the order they were added
        """
        with self._lock:
            return [self._blocks[bid] for bid in self._block_order if bid in self._blocks]
            
    def get_blocks_by_state(self, state: BlockState) -> List[LiveBlock]:
        """
        Get all blocks matching a specific state.
        
        Args:
            state: The BlockState to filter by
            
        Returns:
            List of LiveBlocks matching the state
        """
        with self._lock:
            return [
                block for block in self._blocks.values()
                if block.state == state
            ]
            
    def get_active_blocks(self) -> List[LiveBlock]:
        """
        Get all actively processing blocks.
        
        Returns:
            List of LiveBlocks that are currently processing
        """
        with self._lock:
            return [
                block for block in self._blocks.values()
                if block.data.progress < 1.0 and block.state == BlockState.LIVE
            ]
            
    def mark_block_complete(self, block_id: str) -> None:
        """
        Mark a block as complete and ready for inscription.
        
        Args:
            block_id: The block ID to mark complete
        """
        block = self.get_block(block_id)
        if block:
            block.data.progress = 1.0
            block.data.wall_time_seconds = time.time() - block.created_at.timestamp()
            self._handle_block_update(block)
            
    def inscribe_block(self, block_id: str) -> Optional[LiveBlock]:
        """
        Transition a block from live to inscribed state.
        
        Args:
            block_id: The block ID to inscribe
            
        Returns:
            The inscribed block if successful, None otherwise
        """
        with self._lock:
            block = self._blocks.get(block_id)
            if not block:
                return None
                
            # Transition to inscribed state
            block.state = BlockState.INSCRIBED
            
            # Update metrics
            self._metrics.update_from_block(block, action="inscribe")
            
            # Remove from staging area
            del self._blocks[block_id]
            self._block_order.remove(block_id)
            
        # Notify listeners outside lock
        self._notify_block_inscribed(block)
        return block
        
    def remove_block(self, block_id: str) -> bool:
        """
        Remove a block from staging without inscription.
        
        Args:
            block_id: The block ID to remove
            
        Returns:
            True if removed, False if not found
        """
        with self._lock:
            if block_id not in self._blocks:
                return False
                
            block = self._blocks[block_id]
            self._metrics.update_from_block(block, action="remove")
            
            del self._blocks[block_id]
            self._block_order.remove(block_id)
            
        # Notify listeners outside lock
        self._notify_block_removed(block_id)
        return True
        
    def clear_all(self) -> int:
        """
        Clear all blocks from staging area.
        
        Returns:
            Number of blocks cleared
        """
        with self._lock:
            count = len(self._blocks)
            block_ids = list(self._blocks.keys())
            
            for block_id in block_ids:
                block = self._blocks[block_id]
                self._metrics.update_from_block(block, action="remove")
                
            self._blocks.clear()
            self._block_order.clear()
            
        # Notify listeners for each removed block
        for block_id in block_ids:
            self._notify_block_removed(block_id)
            
        return count
        
    def get_metrics(self) -> StagingAreaMetrics:
        """
        Get current staging area metrics.
        
        Returns:
            Copy of current metrics
        """
        with self._lock:
            # Create a copy to avoid external modification
            return StagingAreaMetrics(
                total_blocks_staged=self._metrics.total_blocks_staged,
                total_blocks_inscribed=self._metrics.total_blocks_inscribed,
                total_tokens_input=self._metrics.total_tokens_input,
                total_tokens_output=self._metrics.total_tokens_output,
                total_wall_time=self._metrics.total_wall_time,
                active_blocks=self._metrics.active_blocks
            )
            
    # Event registration methods
    
    def on_block_added(self, callback: Callable[[LiveBlock], None]) -> None:
        """Register callback for block addition events"""
        self._on_block_added.append(callback)
        
    def on_block_updated(self, callback: Callable[[LiveBlock], None]) -> None:
        """Register callback for block update events"""
        self._on_block_updated.append(callback)
        
    def on_block_inscribed(self, callback: Callable[[LiveBlock], None]) -> None:
        """Register callback for block inscription events"""
        self._on_block_inscribed.append(callback)
        
    def on_block_removed(self, callback: Callable[[str], None]) -> None:
        """Register callback for block removal events"""
        self._on_block_removed.append(callback)
        
    # Internal event handlers
    
    def _handle_block_update(self, block: LiveBlock) -> None:
        """Handle block content update"""
        self._notify_block_updated(block)
        
    def _handle_block_progress(self, block: LiveBlock) -> None:
        """Handle block progress update (no content change)"""
        # Progress updates are lighter weight, don't trigger full update
        pass
        
    # Event notification methods
    
    def _notify_block_added(self, block: LiveBlock) -> None:
        """Notify listeners of block addition"""
        for callback in self._on_block_added:
            try:
                callback(block)
            except Exception as e:
                print(f"Error in block added callback: {e}")
                
    def _notify_block_updated(self, block: LiveBlock) -> None:
        """Notify listeners of block update"""
        for callback in self._on_block_updated:
            try:
                callback(block)
            except Exception as e:
                print(f"Error in block updated callback: {e}")
                
    def _notify_block_inscribed(self, block: LiveBlock) -> None:
        """Notify listeners of block inscription"""
        for callback in self._on_block_inscribed:
            try:
                callback(block)
            except Exception as e:
                print(f"Error in block inscribed callback: {e}")
                
    def _notify_block_removed(self, block_id: str) -> None:
        """Notify listeners of block removal"""
        for callback in self._on_block_removed:
            try:
                callback(block_id)
            except Exception as e:
                print(f"Error in block removed callback: {e}")
                
    def __repr__(self) -> str:
        """String representation of staging area state"""
        with self._lock:
            return (
                f"LiveBlockStagingArea("
                f"active={len(self._blocks)}, "
                f"total_staged={self._metrics.total_blocks_staged}, "
                f"total_inscribed={self._metrics.total_blocks_inscribed})"
            )