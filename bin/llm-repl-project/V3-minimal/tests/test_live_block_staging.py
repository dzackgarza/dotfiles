"""
Test Live Block Staging Area Implementation

Validates the staging area functionality for managing live blocks
before they are inscribed to the Sacred Timeline.
"""

import pytest
import time
import asyncio
from threading import Thread
from unittest.mock import Mock

from src.core.live_block_staging import LiveBlockStagingArea, StagingAreaMetrics
from src.core.live_blocks import LiveBlock, BlockState, LiveBlockData
from src.core.block_metadata import BlockRole


class TestLiveBlockStagingArea:
    """Test suite for LiveBlockStagingArea"""
    
    def test_initialization(self):
        """Test staging area initialization"""
        staging = LiveBlockStagingArea()
        
        assert len(staging.get_all_blocks()) == 0
        metrics = staging.get_metrics()
        assert metrics.total_blocks_staged == 0
        assert metrics.total_blocks_inscribed == 0
        assert metrics.active_blocks == 0
        
    def test_add_block(self):
        """Test adding blocks to staging area"""
        staging = LiveBlockStagingArea()
        
        # Create a block
        block = LiveBlock(role="user", initial_content="Hello world")
        block_id = block.id
        
        # Add to staging
        staging.add_block(block)
        
        # Verify block was added
        assert len(staging.get_all_blocks()) == 1
        assert staging.get_block(block_id) == block
        
        # Check metrics
        metrics = staging.get_metrics()
        assert metrics.total_blocks_staged == 1
        assert metrics.active_blocks == 1
        
    def test_duplicate_block_id(self):
        """Test that duplicate block IDs are rejected"""
        staging = LiveBlockStagingArea()
        
        block1 = LiveBlock(role="user")
        # Manually set same ID for test
        block2 = LiveBlock(role="assistant")
        block2.id = block1.id  # Force duplicate ID
        
        staging.add_block(block1)
        
        with pytest.raises(ValueError, match="already exists"):
            staging.add_block(block2)
            
    def test_create_block(self):
        """Test creating blocks through staging area"""
        staging = LiveBlockStagingArea()
        
        # Create block through staging area
        block = staging.create_block(
            role=BlockRole.COGNITION,
            content="Processing...",
            model="gpt-4"
        )
        
        assert block is not None
        assert block.role == "cognition"
        assert block.data.content == "Processing..."
        assert block.data.metadata.get("model") == "gpt-4"
        
        # Verify it was added
        assert len(staging.get_all_blocks()) == 1
        
    def test_get_blocks_by_state(self):
        """Test filtering blocks by state"""
        staging = LiveBlockStagingArea()
        
        # Add multiple blocks
        block1 = staging.create_block(BlockRole.USER, "Hello")
        block2 = staging.create_block(BlockRole.ASSISTANT, "Hi there")
        block3 = staging.create_block(BlockRole.COGNITION, "Thinking...")
        
        # All should be LIVE initially
        live_blocks = staging.get_blocks_by_state(BlockState.LIVE)
        assert len(live_blocks) == 3
        
        # Inscribe one block manually by changing state
        block1.state = BlockState.INSCRIBED
        
        # Now only 2 should be LIVE
        live_blocks = staging.get_blocks_by_state(BlockState.LIVE)
        assert len(live_blocks) == 2
        
        inscribed_blocks = staging.get_blocks_by_state(BlockState.INSCRIBED)
        assert len(inscribed_blocks) == 1
        
    def test_get_active_blocks(self):
        """Test getting actively processing blocks"""
        staging = LiveBlockStagingArea()
        
        # Create blocks with different progress
        block1 = staging.create_block(BlockRole.USER, "Input")
        block1.data.progress = 1.0  # Complete
        
        block2 = staging.create_block(BlockRole.COGNITION, "Processing")
        block2.data.progress = 0.5  # In progress
        
        block3 = staging.create_block(BlockRole.ASSISTANT, "Responding")
        block3.data.progress = 0.0  # Just started
        
        # Get active blocks
        active = staging.get_active_blocks()
        assert len(active) == 2  # block2 and block3
        assert block1 not in active
        assert block2 in active
        assert block3 in active
        
    def test_mark_block_complete(self):
        """Test marking a block as complete"""
        staging = LiveBlockStagingArea()
        
        block = staging.create_block(BlockRole.COGNITION, "Processing")
        block_id = block.id
        
        # Initially not complete
        assert block.data.progress < 1.0
        
        # Mark complete
        staging.mark_block_complete(block_id)
        
        # Verify completion
        assert block.data.progress == 1.0
        assert block.data.wall_time_seconds > 0
        
    def test_inscribe_block(self):
        """Test inscribing a block"""
        staging = LiveBlockStagingArea()
        
        # Create and add block
        block = staging.create_block(BlockRole.USER, "Hello world")
        block_id = block.id
        
        # Set some token usage
        block.data.tokens_input = 10
        block.data.tokens_output = 20
        
        # Inscribe the block
        inscribed = staging.inscribe_block(block_id)
        
        assert inscribed is not None
        assert inscribed.state == BlockState.INSCRIBED
        
        # Block should be removed from staging
        assert staging.get_block(block_id) is None
        assert len(staging.get_all_blocks()) == 0
        
        # Check metrics
        metrics = staging.get_metrics()
        assert metrics.total_blocks_inscribed == 1
        assert metrics.total_tokens_input == 10
        assert metrics.total_tokens_output == 20
        assert metrics.active_blocks == 0
        
    def test_remove_block(self):
        """Test removing a block without inscription"""
        staging = LiveBlockStagingArea()
        
        block = staging.create_block(BlockRole.ERROR, "Error occurred")
        block_id = block.id
        
        # Remove the block
        removed = staging.remove_block(block_id)
        assert removed is True
        
        # Block should be gone
        assert staging.get_block(block_id) is None
        assert len(staging.get_all_blocks()) == 0
        
        # Metrics should reflect removal
        metrics = staging.get_metrics()
        assert metrics.active_blocks == 0
        assert metrics.total_blocks_inscribed == 0  # Not inscribed
        
    def test_clear_all(self):
        """Test clearing all blocks"""
        staging = LiveBlockStagingArea()
        
        # Add multiple blocks
        for i in range(5):
            staging.create_block(BlockRole.USER, f"Message {i}")
            
        assert len(staging.get_all_blocks()) == 5
        
        # Clear all
        count = staging.clear_all()
        assert count == 5
        assert len(staging.get_all_blocks()) == 0
        
        metrics = staging.get_metrics()
        assert metrics.active_blocks == 0
        
    def test_block_ordering(self):
        """Test that blocks maintain insertion order"""
        staging = LiveBlockStagingArea()
        
        # Add blocks in specific order
        block1 = staging.create_block(BlockRole.USER, "First")
        block2 = staging.create_block(BlockRole.ASSISTANT, "Second")
        block3 = staging.create_block(BlockRole.COGNITION, "Third")
        
        # Get all blocks
        blocks = staging.get_all_blocks()
        
        assert len(blocks) == 3
        assert blocks[0].data.content == "First"
        assert blocks[1].data.content == "Second"
        assert blocks[2].data.content == "Third"
        
    def test_event_callbacks(self):
        """Test event callback system"""
        staging = LiveBlockStagingArea()
        
        # Set up mock callbacks
        added_callback = Mock()
        updated_callback = Mock()
        inscribed_callback = Mock()
        removed_callback = Mock()
        
        staging.on_block_added(added_callback)
        staging.on_block_updated(updated_callback)
        staging.on_block_inscribed(inscribed_callback)
        staging.on_block_removed(removed_callback)
        
        # Create a block - should trigger added callback
        block = staging.create_block(BlockRole.USER, "Test")
        added_callback.assert_called_once()
        
        # Update block content - should trigger updated callback
        block.update_content("Updated test")
        updated_callback.assert_called()
        
        # Inscribe block - should trigger inscribed callback
        staging.inscribe_block(block.id)
        inscribed_callback.assert_called_once()
        
        # Remove a different block - should trigger removed callback
        block2 = staging.create_block(BlockRole.ERROR, "Error")
        staging.remove_block(block2.id)
        removed_callback.assert_called_once()
        
    def test_concurrent_access(self):
        """Test thread-safe concurrent access"""
        staging = LiveBlockStagingArea()
        results = []
        
        def add_blocks(prefix, count):
            """Add blocks from a thread"""
            for i in range(count):
                try:
                    block = staging.create_block(
                        BlockRole.USER,
                        f"{prefix}-{i}"
                    )
                    results.append(f"added-{block.id}")
                except Exception as e:
                    results.append(f"error-{e}")
                    
        # Create multiple threads
        threads = []
        for i in range(3):
            t = Thread(target=add_blocks, args=(f"thread-{i}", 10))
            threads.append(t)
            t.start()
            
        # Wait for all threads
        for t in threads:
            t.join()
            
        # Should have 30 blocks
        assert len(staging.get_all_blocks()) == 30
        
        # No errors should have occurred
        errors = [r for r in results if r.startswith("error-")]
        assert len(errors) == 0
        
    def test_metrics_accuracy(self):
        """Test that metrics are accurately tracked"""
        staging = LiveBlockStagingArea()
        
        # Add blocks with token usage
        for i in range(3):
            block = staging.create_block(BlockRole.ASSISTANT, f"Response {i}")
            block.data.tokens_input = 10 * (i + 1)
            block.data.tokens_output = 20 * (i + 1)
            block.data.wall_time_seconds = 1.5 * (i + 1)
            
        # Check staging metrics
        metrics = staging.get_metrics()
        assert metrics.total_blocks_staged == 3
        assert metrics.active_blocks == 3
        
        # Inscribe all blocks
        blocks = staging.get_all_blocks()
        for block in blocks:
            staging.inscribe_block(block.id)
            
        # Check final metrics
        metrics = staging.get_metrics()
        assert metrics.total_blocks_staged == 3
        assert metrics.total_blocks_inscribed == 3
        assert metrics.active_blocks == 0
        assert metrics.total_tokens_input == 60  # 10 + 20 + 30
        assert metrics.total_tokens_output == 120  # 20 + 40 + 60
        assert metrics.total_wall_time == 9.0  # 1.5 + 3.0 + 4.5
        
    @pytest.mark.asyncio
    async def test_async_block_updates(self):
        """Test handling async block updates"""
        staging = LiveBlockStagingArea()
        
        # Create a cognition block
        block = staging.create_block(BlockRole.COGNITION, "Starting...")
        
        # Track updates
        updates = []
        staging.on_block_updated(lambda b: updates.append(b.data.content))
        
        # Simulate async content streaming
        async def stream_content():
            messages = ["Analyzing...", "Processing...", "Generating...", "Complete!"]
            for msg in messages:
                block.update_content(msg)
                await asyncio.sleep(0.01)  # Small delay
                
        await stream_content()
        
        # Should have received all updates
        assert len(updates) >= 4
        assert "Complete!" in updates


if __name__ == "__main__":
    pytest.main([__file__, "-v"])