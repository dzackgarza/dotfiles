"""Tests for Sacred Timeline functionality"""

from datetime import datetime
from src.sacred_timeline import SacredTimeline, Block


class TestSacredTimeline:
    """Test the Sacred Timeline core functionality"""

    def test_create_empty_timeline(self) -> None:
        """Test creating an empty timeline"""
        timeline = SacredTimeline()
        assert len(timeline) == 0
        assert timeline.get_blocks() == []

    def test_add_block(self) -> None:
        """Test adding a block to the timeline"""
        timeline = SacredTimeline()

        block = timeline.add_block(role="user", content="Hello world")

        assert len(timeline) == 1
        assert block.role == "user"
        assert block.content == "Hello world"
        assert isinstance(block.timestamp, datetime)
        assert block.id is not None

    def test_append_only_behavior(self) -> None:
        """Test that timeline is append-only"""
        timeline = SacredTimeline()

        block1 = timeline.add_block(role="user", content="First")
        block2 = timeline.add_block(role="assistant", content="Second")

        blocks = timeline.get_blocks()
        assert len(blocks) == 2
        assert blocks[0].id == block1.id
        assert blocks[1].id == block2.id

    def test_immutable_blocks(self) -> None:
        """Test that blocks are immutable once created"""
        timeline = SacredTimeline()
        block = timeline.add_block(role="user", content="Original")

        # Getting blocks should return a copy
        blocks_copy = timeline.get_blocks()
        assert blocks_copy is not timeline._blocks

    def test_filter_by_role(self) -> None:
        """Test filtering blocks by role"""
        timeline = SacredTimeline()

        timeline.add_block(role="user", content="User 1")
        timeline.add_block(role="assistant", content="Assistant 1")
        timeline.add_block(role="user", content="User 2")

        user_blocks = timeline.get_blocks_by_role("user")
        assert len(user_blocks) == 2
        assert all(block.role == "user" for block in user_blocks)

    def test_observer_pattern(self) -> None:
        """Test that observers are notified of new blocks"""
        timeline = SacredTimeline()
        observed_blocks = []

        class TestObserver:
            def on_block_added(self, block: Block) -> None:
                observed_blocks.append(block)

        observer = TestObserver()
        timeline.add_observer(observer)

        block = timeline.add_block(role="system", content="Test")

        assert len(observed_blocks) == 1
        assert observed_blocks[0].id == block.id


class TestBlock:
    """Test the Block data structure"""

    def test_block_creation(self) -> None:
        """Test creating a block with default values"""
        block = Block(role="user", content="Hello")

        assert block.role == "user"
        assert block.content == "Hello"
        assert isinstance(block.timestamp, datetime)
        assert block.id is not None
        assert block.metadata == {}

    def test_block_serialization(self) -> None:
        """Test block serialization to/from dict"""
        original = Block(
            role="assistant", content="Response", metadata={"model": "test"}
        )

        # Serialize
        data = original.to_dict()
        assert data["role"] == "assistant"
        assert data["content"] == "Response"
        assert data["metadata"]["model"] == "test"

        # Deserialize
        restored = Block.from_dict(data)
        assert restored.role == original.role
        assert restored.content == original.content
        assert restored.id == original.id
        assert restored.metadata == original.metadata
