"""Tests for live block system."""

import pytest
import asyncio
from datetime import datetime
from src.core.live_blocks import (
    LiveBlock,
    LiveBlockManager,
    InscribedBlock,
    BlockState,
    LiveBlockData,
)


class TestLiveBlockData:
    """Test LiveBlockData functionality."""

    def test_initialization(self):
        """Test LiveBlockData initializes with defaults."""
        data = LiveBlockData()
        assert data.content == ""
        assert data.tokens_input == 0
        assert data.tokens_output == 0
        assert data.progress == 0.0
        assert data.sub_blocks == []
        assert data.metadata == {}

    def test_to_dict(self):
        """Test LiveBlockData converts to dictionary."""
        data = LiveBlockData(
            content="test content", tokens_input=10, tokens_output=20, progress=0.5
        )
        result = data.to_dict()

        assert result["content"] == "test content"
        assert result["tokens_input"] == 10
        assert result["tokens_output"] == 20
        assert result["progress"] == 0.5


class TestLiveBlock:
    """Test LiveBlock functionality."""

    def test_initialization(self):
        """Test LiveBlock initializes correctly."""
        block = LiveBlock("user", "Hello world")

        assert block.role == "user"
        assert block.state == BlockState.LIVE
        assert block.data.content == "Hello world"
        assert isinstance(block.created_at, datetime)
        assert len(block.id) > 0

    def test_update_content(self):
        """Test content updates work in live state."""
        block = LiveBlock("user")

        # Should work in live state
        block.update_content("New content")
        assert block.data.content == "New content"

        # Should fail in inscribed state
        block.state = BlockState.INSCRIBED
        with pytest.raises(ValueError, match="Cannot update inscribed block"):
            block.update_content("Should fail")

    def test_append_content(self):
        """Test content appending works."""
        block = LiveBlock("user", "Hello ")
        block.append_content("world!")
        assert block.data.content == "Hello world!"

    def test_update_tokens(self):
        """Test token updates."""
        block = LiveBlock("assistant")

        block.update_tokens(input_tokens=10, output_tokens=5)
        assert block.data.tokens_input == 10
        assert block.data.tokens_output == 5

        # Additional tokens should accumulate
        block.update_tokens(input_tokens=5, output_tokens=3)
        assert block.data.tokens_input == 15
        assert block.data.tokens_output == 8

    def test_update_progress(self):
        """Test progress updates with bounds checking."""
        block = LiveBlock("system")

        # Normal progress
        block.update_progress(0.5)
        assert block.data.progress == 0.5

        # Should clamp to bounds
        block.update_progress(-0.1)
        assert block.data.progress == 0.0

        block.update_progress(1.5)
        assert block.data.progress == 1.0

    def test_add_sub_block(self):
        """Test adding sub-blocks."""
        parent = LiveBlock("cognition")
        child = LiveBlock("sub_module", "Step 1")

        parent.add_sub_block(child)

        assert len(parent.data.sub_blocks) == 1
        assert parent.data.sub_blocks[0] == child

    def test_update_callbacks(self):
        """Test update callback system."""
        block = LiveBlock("user")
        callback_called = False

        def test_callback(updated_block):
            nonlocal callback_called
            callback_called = True
            assert updated_block == block

        block.add_update_callback(test_callback)
        block.update_content("Trigger callback")

        assert callback_called

    def test_to_inscribed_block(self):
        """Test conversion to inscribed block."""
        live_block = LiveBlock("assistant", "Test content")
        live_block.update_tokens(input_tokens=10, output_tokens=20)
        live_block.data.metadata["test_key"] = "test_value"

        inscribed = live_block.to_inscribed_block()

        assert isinstance(inscribed, InscribedBlock)
        assert inscribed.id == live_block.id
        assert inscribed.role == "assistant"
        assert inscribed.content == "Test content"
        assert inscribed.metadata["tokens_input"] == 10
        assert inscribed.metadata["tokens_output"] == 20
        assert inscribed.metadata["test_key"] == "test_value"

        # Original block should be inscribed
        assert live_block.state == BlockState.INSCRIBED

    def test_to_dict(self):
        """Test dictionary conversion."""
        block = LiveBlock("user", "Test")
        block.update_progress(0.5)

        result = block.to_dict()

        assert result["id"] == block.id
        assert result["role"] == "user"
        assert result["state"] == "live"
        assert "created_at" in result
        assert result["data"]["content"] == "Test"
        assert result["data"]["progress"] == 0.5


class TestLiveBlockManager:
    """Test LiveBlockManager functionality."""

    def test_initialization(self):
        """Test manager initializes correctly."""
        manager = LiveBlockManager()
        assert len(manager.live_blocks) == 0
        assert len(manager.block_update_callbacks) == 0

    def test_create_live_block(self):
        """Test creating live blocks."""
        manager = LiveBlockManager()

        block = manager.create_live_block("user", "Hello")

        assert block.role == "user"
        assert block.data.content == "Hello"
        assert block.id in manager.live_blocks
        assert manager.live_blocks[block.id] == block

    def test_inscribe_block(self):
        """Test inscribing live blocks."""
        manager = LiveBlockManager()

        block = manager.create_live_block("assistant", "Response")
        block_id = block.id

        inscribed = manager.inscribe_block(block_id)

        assert isinstance(inscribed, InscribedBlock)
        assert inscribed.content == "Response"
        assert block_id not in manager.live_blocks  # Should be removed

    def test_inscribe_nonexistent_block(self):
        """Test inscribing non-existent block returns None."""
        manager = LiveBlockManager()
        result = manager.inscribe_block("fake-id")
        assert result is None

    def test_get_live_blocks(self):
        """Test getting all live blocks."""
        manager = LiveBlockManager()

        block1 = manager.create_live_block("user", "First")
        block2 = manager.create_live_block("assistant", "Second")

        blocks = manager.get_live_blocks()

        assert len(blocks) == 2
        assert block1 in blocks
        assert block2 in blocks

    def test_block_update_callbacks(self):
        """Test manager-level update callbacks."""
        manager = LiveBlockManager()
        callback_called = False
        updated_block = None

        def test_callback(block):
            nonlocal callback_called, updated_block
            callback_called = True
            updated_block = block

        manager.add_block_update_callback(test_callback)
        block = manager.create_live_block("user", "Test")

        # Trigger update
        block.update_content("Updated")

        assert callback_called
        assert updated_block == block


class TestInscribedBlock:
    """Test InscribedBlock functionality."""

    def test_initialization(self):
        """Test InscribedBlock initializes correctly."""
        timestamp = datetime.now()
        metadata = {"tokens": 10}

        block = InscribedBlock(
            id="test-id",
            role="assistant",
            content="Test content",
            timestamp=timestamp,
            metadata=metadata,
        )

        assert block.id == "test-id"
        assert block.role == "assistant"
        assert block.content == "Test content"
        assert block.timestamp == timestamp
        assert block.metadata == metadata

    def test_to_dict(self):
        """Test dictionary conversion."""
        timestamp = datetime.now()
        block = InscribedBlock(
            id="test-id",
            role="user",
            content="Hello",
            timestamp=timestamp,
            metadata={"test": "value"},
        )

        result = block.to_dict()

        assert result["id"] == "test-id"
        assert result["role"] == "user"
        assert result["content"] == "Hello"
        assert result["timestamp"] == timestamp.isoformat()
        assert result["metadata"]["test"] == "value"


@pytest.mark.asyncio
class TestMockSimulations:
    """Test mock simulation functionality."""

    async def test_basic_simulation(self):
        """Test basic mock simulation."""
        block = LiveBlock("system")

        # Start simulation and wait for completion
        await block.start_mock_simulation("default")

        # Wait a bit more to ensure task completes
        await asyncio.sleep(0.1)

        # Should have updated content and progress
        assert "Complete" in block.data.content
        assert block.data.progress == 1.0

    async def test_assistant_response_simulation(self):
        """Test assistant response simulation."""
        block = LiveBlock("assistant")

        await block.start_mock_simulation("assistant_response")

        # Wait for completion
        await asyncio.sleep(0.1)

        # Should have streaming content
        assert len(block.data.content) > 0
        assert block.data.progress == 1.0
        assert block.data.tokens_output > 0

    async def test_cognition_simulation(self):
        """Test cognition simulation with sub-blocks."""
        block = LiveBlock("cognition")

        await block.start_mock_simulation("cognition")

        # Wait for completion
        await asyncio.sleep(0.2)

        # Should have sub-blocks
        assert len(block.data.sub_blocks) > 0
        assert block.data.progress == 1.0
        assert "completed" in block.data.content.lower()

    async def test_simulation_cancellation(self):
        """Test simulation can be stopped."""
        block = LiveBlock("system")

        # Start simulation but don't await
        task = asyncio.create_task(block.start_mock_simulation("default"))

        # Stop simulation immediately
        block.stop_simulation()

        # Task should be cancelled or complete
        await asyncio.sleep(0.1)  # Give it time to process cancellation
