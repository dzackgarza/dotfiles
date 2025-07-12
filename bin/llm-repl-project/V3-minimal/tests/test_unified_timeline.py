"""
Tests for Unified Timeline System - V3.15

These tests verify that the unified timeline architecture eliminates
the dual-system ownership conflicts identified in the continue file.
"""

import pytest
from unittest.mock import Mock

from src.core.unified_timeline import (
    UnifiedTimeline,
    UnifiedTimelineManager,
    BlockAdded,
    BlockUpdated,
    BlockInscribed,
)
from src.core.live_blocks import LiveBlock, InscribedBlock


class TestUnifiedTimelineOwnership:
    """Test unified timeline ownership eliminates conflicts"""

    def test_single_source_of_truth(self):
        """Timeline is the single owner of all blocks"""
        timeline = UnifiedTimeline()

        # Add live block
        live_block = timeline.add_live_block("user", "test content")

        # Timeline owns it immediately
        assert timeline.owns_block(live_block.id)
        assert timeline.get_block(live_block.id) == live_block

        # Block appears in timeline list
        blocks = timeline.get_all_blocks()
        assert len(blocks) == 1
        assert blocks[0] == live_block

    def test_no_orphaned_sub_blocks(self):
        """Sub-blocks are owned by parent, not timeline independently"""
        timeline = UnifiedTimeline()

        # Create parent block
        parent = timeline.add_live_block("cognition", "parent content")

        # Add sub-block
        sub_block = timeline.add_sub_block(parent.id, "route_query", "sub content")

        # Sub-block exists in parent
        assert sub_block in parent.data.sub_blocks

        # Sub-block NOT in timeline index (parent owns it)
        assert not timeline.owns_block(sub_block.id)
        assert timeline.get_block(sub_block.id) is None

        # Only parent appears in timeline blocks
        blocks = timeline.get_all_blocks()
        assert len(blocks) == 1
        assert blocks[0] == parent

    @pytest.mark.asyncio
    async def test_atomic_inscription_preserves_structure(self):
        """Inscription preserves complete block structure atomically"""
        timeline = UnifiedTimeline()

        # Create parent with sub-blocks
        parent = timeline.add_live_block("cognition", "parent")
        sub1 = timeline.add_sub_block(parent.id, "route_query", "sub1")
        sub2 = timeline.add_sub_block(parent.id, "call_tool", "sub2")

        # Verify structure before inscription
        assert len(parent.data.sub_blocks) == 2
        assert sub1 in parent.data.sub_blocks
        assert sub2 in parent.data.sub_blocks

        # Inscribe atomically
        inscribed = await timeline.inscribe_block(parent.id)

        # Parent is now inscribed
        assert isinstance(inscribed, InscribedBlock)
        assert timeline.get_block(parent.id) == inscribed

        # Sub-blocks preserved in metadata
        sub_blocks_data = inscribed.metadata.get("sub_blocks", [])
        assert len(sub_blocks_data) == 2

        # Sub-blocks contain complete data
        sub_contents = [sb["data"]["content"] for sb in sub_blocks_data]
        assert "sub1" in sub_contents
        assert "sub2" in sub_contents

    @pytest.mark.asyncio
    async def test_clear_ownership_transfer(self):
        """Block ownership transfers cleanly during inscription"""
        timeline = UnifiedTimeline()

        # Create live block
        live_block = timeline.add_live_block("user", "test")
        live_id = live_block.id

        # Timeline owns live block
        assert timeline.owns_block(live_id)
        assert isinstance(timeline.get_block(live_id), LiveBlock)

        # Inscribe
        inscribed = await timeline.inscribe_block(live_id)

        # Timeline now owns inscribed block
        assert timeline.owns_block(inscribed.id)
        assert isinstance(timeline.get_block(inscribed.id), InscribedBlock)

        # No duplicate ownership
        all_blocks = timeline.get_all_blocks()
        assert len(all_blocks) == 1
        assert all_blocks[0] == inscribed


class TestUnifiedTimelineEvents:
    """Test event system for UI updates"""

    def test_block_added_event(self):
        """Timeline fires event when block added"""
        timeline = UnifiedTimeline()
        observer = Mock()
        timeline.add_observer(observer)

        # Add block
        block = timeline.add_live_block("user", "test")

        # Observer notified
        observer.on_timeline_event.assert_called_once()
        event = observer.on_timeline_event.call_args[0][0]
        assert isinstance(event, BlockAdded)
        assert event.block == block

    def test_block_updated_event(self):
        """Timeline fires event when live block updates"""
        timeline = UnifiedTimeline()
        observer = Mock()
        timeline.add_observer(observer)

        # Add block
        block = timeline.add_live_block("user", "test")
        observer.reset_mock()

        # Update block content
        block.update_content("updated content")

        # Observer notified of update
        observer.on_timeline_event.assert_called()
        event = observer.on_timeline_event.call_args[0][0]
        assert isinstance(event, BlockUpdated)
        assert event.block == block

    @pytest.mark.asyncio
    async def test_block_inscribed_event(self):
        """Timeline fires event when block becomes inscribed"""
        timeline = UnifiedTimeline()
        observer = Mock()
        timeline.add_observer(observer)

        # Add live block
        block = timeline.add_live_block("user", "test")
        original_id = block.id
        observer.reset_mock()

        # Inscribe block
        inscribed = await timeline.inscribe_block(block.id)

        # Observer notified of inscription
        observer.on_timeline_event.assert_called()
        event = observer.on_timeline_event.call_args[0][0]
        assert isinstance(event, BlockInscribed)
        assert event.inscribed_block == inscribed
        assert event.original_live_id == original_id


class TestUnifiedTimelineManager:
    """Test manager class that replaces LiveBlockManager"""

    def test_manager_delegates_to_timeline(self):
        """Manager is pure factory, timeline owns everything"""
        manager = UnifiedTimelineManager()

        # Create block through manager
        block = manager.create_live_block("user", "test")

        # Timeline owns it
        timeline = manager.get_timeline()
        assert timeline.owns_block(block.id)
        assert timeline.get_block(block.id) == block

    def test_manager_creates_sub_blocks(self):
        """Manager can create sub-blocks with proper ownership"""
        manager = UnifiedTimelineManager()

        # Create parent
        parent = manager.create_live_block("cognition", "parent")

        # Create sub-block through manager
        sub_block = manager.add_sub_block(parent.id, "route_query", "sub")

        # Sub-block owned by parent, not timeline
        timeline = manager.get_timeline()
        assert sub_block in parent.data.sub_blocks
        assert not timeline.owns_block(sub_block.id)

    @pytest.mark.asyncio
    async def test_manager_inscription_integration(self):
        """Manager inscription works with timeline"""
        manager = UnifiedTimelineManager()

        # Create block through manager
        block = manager.create_live_block("user", "test")

        # Inscribe through manager
        inscribed = await manager.inscribe_block(block.id)

        # Timeline has inscribed block
        timeline = manager.get_timeline()
        assert timeline.get_block(inscribed.id) == inscribed
        assert isinstance(timeline.get_block(inscribed.id), InscribedBlock)


class TestArchitecturalFixes:
    """Test that architectural issues from continue file are fixed"""

    @pytest.mark.asyncio
    async def test_no_duplicate_rendering(self):
        """Blocks don't appear in multiple places"""
        timeline = UnifiedTimeline()

        # Create parent with sub-blocks
        parent = timeline.add_live_block("cognition", "parent")
        timeline.add_sub_block(parent.id, "route_query", "sub1")
        timeline.add_sub_block(parent.id, "call_tool", "sub2")

        # Only parent appears in timeline
        blocks = timeline.get_all_blocks()
        assert len(blocks) == 1
        assert blocks[0] == parent

        # Sub-blocks contained within parent
        assert len(parent.data.sub_blocks) == 2

        # After inscription, still no duplicates
        inscribed = await timeline.inscribe_block(parent.id)
        blocks = timeline.get_all_blocks()
        assert len(blocks) == 1
        assert blocks[0] == inscribed

    def test_no_mixed_containment(self):
        """All sub-blocks consistently contained in parent"""
        timeline = UnifiedTimeline()

        # Create parent
        parent = timeline.add_live_block("cognition", "parent")

        # Add multiple sub-blocks
        sub1 = timeline.add_sub_block(parent.id, "route_query", "sub1")
        sub2 = timeline.add_sub_block(parent.id, "call_tool", "sub2")
        sub3 = timeline.add_sub_block(parent.id, "format_output", "sub3")

        # All contained in parent
        assert len(parent.data.sub_blocks) == 3
        assert sub1 in parent.data.sub_blocks
        assert sub2 in parent.data.sub_blocks
        assert sub3 in parent.data.sub_blocks

        # None in timeline independently
        assert not timeline.owns_block(sub1.id)
        assert not timeline.owns_block(sub2.id)
        assert not timeline.owns_block(sub3.id)

    def test_single_ownership_no_confusion(self):
        """Only one system owns each block at any time"""
        timeline = UnifiedTimeline()

        # Create blocks
        block1 = timeline.add_live_block("user", "test1")
        block2 = timeline.add_live_block("assistant", "test2")

        # Timeline owns both
        assert timeline.owns_block(block1.id)
        assert timeline.owns_block(block2.id)

        # Clear ownership identity
        assert timeline.get_block(block1.id) == block1
        assert timeline.get_block(block2.id) == block2

        # No external system has ownership
        # (In old system, LiveBlockManager would also claim ownership)

    @pytest.mark.asyncio
    async def test_inscription_preserves_relationships(self):
        """Parent-child relationships maintained through inscription"""
        timeline = UnifiedTimeline()

        # Create hierarchy
        parent = timeline.add_live_block("cognition", "cognition content")
        sub1 = timeline.add_sub_block(parent.id, "route_query", "route content")
        sub2 = timeline.add_sub_block(parent.id, "call_tool", "tool content")

        # Record original structure
        original_sub_count = len(parent.data.sub_blocks)
        original_sub_contents = [s.data.content for s in parent.data.sub_blocks]

        # Inscribe
        inscribed = await timeline.inscribe_block(parent.id)

        # Relationships preserved in metadata
        sub_blocks_data = inscribed.metadata.get("sub_blocks", [])
        assert len(sub_blocks_data) == original_sub_count

        preserved_contents = [sb["data"]["content"] for sb in sub_blocks_data]
        assert set(preserved_contents) == set(original_sub_contents)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
