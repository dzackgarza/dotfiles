"""
Test suite for V3 core components

Tests the extracted and refined core functionality from V2.
"""

import asyncio
import pytest
import sys
from pathlib import Path

# Add V3 to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.blocks import (
    BlockType, TimelineBlock, 
    create_system_check_block, create_welcome_block,
    create_user_input_block, create_cognition_block,
    create_assistant_response_block, create_error_block
)
from core.cognition import CognitionProcessor
from core.timeline import TimelineManager


class TestTimelineBlocks:
    """Test timeline block functionality."""
    
    def test_block_creation(self):
        """Test basic block creation."""
        block = TimelineBlock.create(
            BlockType.USER_INPUT,
            "Test Block",
            "Test content",
            {"input": 5, "output": 10},
            {"test": True}
        )
        
        assert block.id is not None
        assert block.type == BlockType.USER_INPUT
        assert block.title == "Test Block"
        assert block.content == "Test content"
        assert block.tokens["input"] == 5
        assert block.tokens["output"] == 10
        assert block.metadata["test"] is True
        assert block.timestamp > 0
    
    def test_block_helper_methods(self):
        """Test block helper methods."""
        block = TimelineBlock.create(
            BlockType.COGNITION,
            "Cognition ✅",
            "Processing...",
            {"input": 15, "output": 30}
        )
        
        assert block.has_tokens() is True
        assert block.get_token_summary() == "[↑15 ↓30]"
        assert "Cognition ✅" in block.get_formatted_header()
        assert "[↑15 ↓30]" in block.get_formatted_header()
        assert "s)" in block.get_formatted_header()  # Duration
    
    def test_block_factory_functions(self):
        """Test block factory functions."""
        # System check block
        system_block = create_system_check_block("test")
        assert system_block.type == BlockType.SYSTEM_CHECK
        assert "System_Check ✅" in system_block.title
        assert "test" in system_block.metadata["config"]
        
        # Welcome block
        welcome_block = create_welcome_block("test")
        assert welcome_block.type == BlockType.WELCOME
        assert "Welcome ✅" in welcome_block.title
        assert "test" in welcome_block.content
        
        # User input block
        user_block = create_user_input_block("Hello world")
        assert user_block.type == BlockType.USER_INPUT
        assert "User_Input ✅" in user_block.title
        assert "> Hello world" in user_block.content
        
        # Error block
        error_block = create_error_block("Test error")
        assert error_block.type == BlockType.ERROR
        assert "Error ❌" in error_block.title
        assert "Test error" in error_block.content


class TestCognitionProcessor:
    """Test cognition processor functionality."""
    
    def test_processor_initialization(self):
        """Test processor initialization."""
        processor = CognitionProcessor()
        
        assert len(processor.get_step_names()) == 3
        assert "Query Routing" in processor.get_step_names()
        assert "Prompt Enhancement" in processor.get_step_names()
        assert "Response Generation" in processor.get_step_names()
        assert processor.processing_delay == 0.3
    
    @pytest.mark.asyncio
    async def test_processing(self):
        """Test cognitive processing."""
        processor = CognitionProcessor()
        processor.configure_processing_delay(0.01)  # Speed up for testing
        
        result = await processor.process("Test input")
        
        assert "final_output" in result
        assert "transparency_log" in result
        assert "total_tokens" in result
        assert "processing_duration" in result
        
        # Check transparency log
        log = result["transparency_log"]
        assert len(log) == 3
        
        for i, entry in enumerate(log):
            assert entry["step"] == i + 1
            assert "name" in entry
            assert entry["status"] == "✅ Complete"
            assert "tokens" in entry
        
        # Check tokens
        tokens = result["total_tokens"]
        assert tokens["input"] > 0
        assert tokens["output"] > 0
        
        # Check response content
        response = result["final_output"]
        assert "Test input" in response
        assert "cognitive steps" in response
    
    def test_processor_configuration(self):
        """Test processor configuration."""
        processor = CognitionProcessor()
        
        # Test delay configuration
        processor.configure_processing_delay(0.5)
        assert processor.processing_delay == 0.5
        
        # Test clamping
        processor.configure_processing_delay(-1.0)  # Too low
        assert processor.processing_delay == 0.1
        
        processor.configure_processing_delay(5.0)  # Too high
        assert processor.processing_delay == 2.0
        
        # Test step management
        original_count = len(processor.get_step_names())
        processor.add_cognitive_step("New Step")
        assert len(processor.get_step_names()) == original_count + 1
        
        processor.remove_cognitive_step("New Step")
        assert len(processor.get_step_names()) == original_count


class TestTimelineManager:
    """Test timeline manager functionality."""
    
    def test_timeline_initialization(self):
        """Test timeline manager initialization."""
        manager = TimelineManager()
        
        assert manager.get_block_count() == 0
        assert manager.get_latest_block() is None
        assert manager.get_total_tokens() == {"input": 0, "output": 0}
    
    def test_block_management(self):
        """Test adding and managing blocks."""
        manager = TimelineManager()
        
        # Add a block
        block = TimelineBlock.create(
            BlockType.USER_INPUT,
            "Test",
            "Content",
            {"input": 5, "output": 10}
        )
        
        manager.add_block(block)
        
        assert manager.get_block_count() == 1
        assert manager.get_latest_block() == block
        assert manager.get_total_tokens() == {"input": 5, "output": 10}
        
        # Add another block
        block2 = TimelineBlock.create(
            BlockType.ASSISTANT_RESPONSE,
            "Response",
            "Response content",
            {"input": 3, "output": 7}
        )
        
        manager.add_block(block2)
        
        assert manager.get_block_count() == 2
        assert manager.get_latest_block() == block2
        assert manager.get_total_tokens() == {"input": 8, "output": 17}
    
    def test_block_filtering(self):
        """Test filtering blocks by type."""
        manager = TimelineManager()
        
        # Add different types of blocks
        user_block = TimelineBlock.create(BlockType.USER_INPUT, "User", "Content")
        assistant_block = TimelineBlock.create(BlockType.ASSISTANT_RESPONSE, "Assistant", "Response")
        error_block = TimelineBlock.create(BlockType.ERROR, "Error", "Error message")
        
        manager.add_block(user_block)
        manager.add_block(assistant_block)
        manager.add_block(error_block)
        
        # Test filtering
        user_blocks = manager.get_blocks_by_type(BlockType.USER_INPUT)
        assert len(user_blocks) == 1
        assert user_blocks[0] == user_block
        
        assistant_blocks = manager.get_blocks_by_type(BlockType.ASSISTANT_RESPONSE)
        assert len(assistant_blocks) == 1
        assert assistant_blocks[0] == assistant_block
        
        error_blocks = manager.get_blocks_by_type(BlockType.ERROR)
        assert len(error_blocks) == 1
        assert error_blocks[0] == error_block
    
    def test_startup_initialization(self):
        """Test startup block initialization."""
        manager = TimelineManager()
        manager.initialize_with_startup_blocks("test")
        
        assert manager.get_block_count() == 2
        
        blocks = manager.get_blocks()
        assert blocks[0].type == BlockType.SYSTEM_CHECK
        assert blocks[1].type == BlockType.WELCOME
        
        # Check content
        assert "test" in blocks[0].metadata["config"]
        assert "test" in blocks[1].content
    
    def test_conversation_summary(self):
        """Test conversation summary generation."""
        manager = TimelineManager()
        
        # Add various blocks
        manager.add_block(TimelineBlock.create(BlockType.USER_INPUT, "User", "Hello"))
        manager.add_block(TimelineBlock.create(BlockType.COGNITION, "Cognition", "Processing"))
        manager.add_block(TimelineBlock.create(BlockType.ASSISTANT_RESPONSE, "Assistant", "Hi there"))
        manager.add_block(TimelineBlock.create(BlockType.ERROR, "Error", "Oops"))
        
        summary = manager.get_conversation_summary()
        
        assert summary["total_blocks"] == 4
        assert summary["user_inputs"] == 1
        assert summary["assistant_responses"] == 1
        assert summary["cognition_blocks"] == 1
        assert summary["errors"] == 1
    
    def test_timeline_export(self):
        """Test timeline export functionality."""
        manager = TimelineManager()
        
        block = TimelineBlock.create(
            BlockType.USER_INPUT,
            "Test Block",
            "Test content",
            {"input": 5, "output": 10},
            {"test": True}
        )
        manager.add_block(block)
        
        # Test dictionary export
        exported = manager.export_timeline()
        assert len(exported) == 1
        assert exported[0]["type"] == "user_input"
        assert exported[0]["title"] == "Test Block"
        assert exported[0]["content"] == "Test content"
        
        # Test text export
        text = manager.get_timeline_text()
        assert "Test Block" in text
        assert "Test content" in text
    
    def test_observer_pattern(self):
        """Test observer pattern for block additions."""
        manager = TimelineManager()
        observed_blocks = []
        
        def observer(block):
            observed_blocks.append(block)
        
        manager.add_observer(observer)
        
        block = TimelineBlock.create(BlockType.USER_INPUT, "Test", "Content")
        manager.add_block(block)
        
        assert len(observed_blocks) == 1
        assert observed_blocks[0] == block
        
        # Test observer removal
        manager.remove_observer(observer)
        
        block2 = TimelineBlock.create(BlockType.ASSISTANT_RESPONSE, "Test2", "Content2")
        manager.add_block(block2)
        
        assert len(observed_blocks) == 1  # Should not have increased


if __name__ == "__main__":
    pytest.main([__file__])