"""
Comprehensive tests for block ordering and sequence validation.

These tests ensure that:
1. Blocks are created in the correct order
2. The visual display matches the historical record
3. No blocks are missing, duplicated, or out of order
4. The system fails fast if block ordering is violated
"""

import pytest
import asyncio
import sys
from pathlib import Path
from typing import List, Dict, Any

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from blocks import (
    BlockType, BlockSequence, BlockRegistry,
    UserBlock, SystemCheckBlock, WelcomeBlock,
    InternalProcessingBlock, ProcessingSubBlock,
    AssistantBlock
)
from scrivener_v2 import ScrivenerV2, DisplayInterface


class MockDisplay(DisplayInterface):
    """Mock display for testing."""
    
    def __init__(self):
        self.rendered_blocks: List[Dict[str, Any]] = []
        self.render_count = 0
    
    async def render_block(self, block) -> None:
        self.rendered_blocks.append({
            "action": "render",
            "block_id": block.id,
            "block_type": block.metadata.type,
            "state": block.state,
            "render_count": self.render_count
        })
        self.render_count += 1
    
    async def update_block(self, block) -> None:
        self.rendered_blocks.append({
            "action": "update",
            "block_id": block.id,
            "block_type": block.metadata.type,
            "state": block.state,
            "render_count": self.render_count
        })
        self.render_count += 1
    
    async def clear_display(self) -> None:
        self.rendered_blocks.clear()
        self.render_count = 0


class TestBlockOrdering:
    """Test suite for block ordering."""
    
    @pytest.mark.asyncio
    async def test_basic_query_block_order(self):
        """Test that a basic query produces the correct block order."""
        display = MockDisplay()
        scrivener = ScrivenerV2(display)
        await scrivener.start()
        
        # Simulate a basic query flow
        # 1. System check
        system_check = await scrivener.create_system_check()
        system_check.add_check("Models", True, "All models available")
        
        # 2. Welcome
        welcome = await scrivener.create_welcome("v2")
        
        # 3. User input
        user_block = await scrivener.create_user_input("Hello")
        
        # 4. Internal processing
        processing = await scrivener.create_internal_processing()
        
        # Add intent detection sub-block
        intent_block = await scrivener.add_processing_step(
            processing, "🧠 Intent Detection", 
            "Analyzing query intent using ollama/tinyllama..."
        )
        
        # Start and complete intent detection
        await scrivener.start_processing_step(processing, 0)
        await scrivener.complete_processing_step(
            processing, 0, "CHAT", 15, 5,
            "Intent: CHAT. Routing to: ollama/tinyllama (Chat Mode)."
        )
        
        # Add main query sub-block
        main_query = await scrivener.add_processing_step(
            processing, "💬 Main Query",
            "Generating response using ollama/tinyllama..."
        )
        
        # Start and complete main query
        await scrivener.start_processing_step(processing, 1)
        await scrivener.complete_processing_step(
            processing, 1, "Hello! How can I help you?", 35, 308,
            "Relaying to user: ollama/tinyllama (Chat Mode)"
        )
        
        # Complete internal processing
        await scrivener.complete_internal_processing(processing)
        
        # 5. Assistant response
        assistant = await scrivener.create_assistant_response(
            "Hello! How can I help you today?",
            "10.8s"
        )
        
        # Wait for all events to process
        await asyncio.sleep(0.1)
        
        # Validate the sequence
        sequence = scrivener.get_current_sequence()
        assert sequence is not None
        
        # Check block types in order
        block_types = sequence.get_block_types()
        expected_types = [
            BlockType.SYSTEM_CHECK,
            BlockType.WELCOME,
            BlockType.USER,
            BlockType.INTERNAL_PROCESSING,
            BlockType.PROCESSING_SUB,  # Intent detection
            BlockType.PROCESSING_SUB,  # Main query
            BlockType.ASSISTANT
        ]
        
        assert block_types == expected_types, f"Expected {expected_types}, got {block_types}"
        
        # Validate using built-in validation
        assert scrivener.validate_sequence("default")
        
        # Check validation report
        report = scrivener.get_validation_report("default")
        assert report["valid"]
        assert len(report["missing"]) == 0
        assert len(report["matched"]) == 5  # The 5 main block types
        
        await scrivener.stop()
    
    @pytest.mark.asyncio
    async def test_missing_block_detection(self):
        """Test that missing blocks are detected."""
        display = MockDisplay()
        scrivener = ScrivenerV2(display)
        await scrivener.start()
        
        # Create sequence with missing welcome block
        system_check = await scrivener.create_system_check()
        # Skip welcome!
        user_block = await scrivener.create_user_input("Hello")
        processing = await scrivener.create_internal_processing()
        await scrivener.complete_internal_processing(processing)
        assistant = await scrivener.create_assistant_response("Hello!")
        
        await asyncio.sleep(0.1)
        
        # Validation should fail
        assert not scrivener.validate_sequence("default")
        
        # Check validation report
        report = scrivener.get_validation_report("default")
        assert not report["valid"]
        assert BlockType.WELCOME in report["missing"]
        
        await scrivener.stop()
    
    @pytest.mark.asyncio
    async def test_display_matches_history(self):
        """Test that the display state matches the historical record."""
        display = MockDisplay()
        scrivener = ScrivenerV2(display)
        await scrivener.start()
        
        # Create a simple sequence
        welcome = await scrivener.create_welcome()
        user = await scrivener.create_user_input("Test")
        assistant = await scrivener.create_assistant_response("Response")
        
        await asyncio.sleep(0.1)
        
        # Get display state and history
        display_state = scrivener.get_display_state()
        history = scrivener.get_block_history()
        
        # Both should have same number of blocks
        assert len(display_state) == len(history)
        
        # Block IDs should match in order
        display_ids = [block["id"] for block in display_state]
        history_ids = [block["metadata"]["id"] for block in history]
        assert display_ids == history_ids
        
        # Check that blocks rendered in correct order
        rendered_types = [
            r["block_type"] for r in display.rendered_blocks 
            if r["action"] == "render"
        ]
        expected_render_order = [
            BlockType.WELCOME,
            BlockType.USER,
            BlockType.ASSISTANT
        ]
        assert rendered_types == expected_render_order
        
        await scrivener.stop()
    
    @pytest.mark.asyncio
    async def test_block_state_transitions(self):
        """Test that blocks transition through states correctly."""
        display = MockDisplay()
        scrivener = ScrivenerV2(display)
        await scrivener.start()
        
        # Create internal processing block
        processing = await scrivener.create_internal_processing()
        
        # Check initial state
        assert processing.state.value == "live"
        
        # Complete it
        await scrivener.complete_internal_processing(processing)
        await asyncio.sleep(0.1)
        
        # Check final state
        assert processing.state.value == "inscribed"
        
        # Verify state transitions were rendered
        updates = [
            r for r in display.rendered_blocks 
            if r["block_id"] == processing.id
        ]
        
        # Should have: create (created), start (live), complete (inscribed)
        assert len(updates) >= 2
        assert updates[0]["action"] == "render"
        assert updates[-1]["action"] == "update"
        assert updates[-1]["state"].value == "inscribed"
        
        await scrivener.stop()
    
    @pytest.mark.asyncio
    async def test_no_split_block_states(self):
        """Test that blocks cannot have split states."""
        display = MockDisplay()
        scrivener = ScrivenerV2(display)
        await scrivener.start()
        
        # Create user block
        user_block = await scrivener.create_user_input("Hello")
        await asyncio.sleep(0.1)
        
        # User block should be atomic - created and immediately inscribed
        assert user_block.state.value == "inscribed"
        
        # Check that it was rendered exactly once with consistent state
        user_renders = [
            r for r in display.rendered_blocks
            if r["block_id"] == user_block.id and r["action"] == "render"
        ]
        
        assert len(user_renders) == 1
        
        # The title and content should be together
        render_data = user_block.render()
        assert render_data["title"] == "You"
        assert render_data["body"] == "Hello"
        
        await scrivener.stop()
    
    @pytest.mark.asyncio 
    async def test_processing_block_hierarchy(self):
        """Test that processing blocks maintain proper parent-child relationships."""
        display = MockDisplay()
        scrivener = ScrivenerV2(display)
        await scrivener.start()
        
        # Create processing block with sub-blocks
        processing = await scrivener.create_internal_processing()
        
        sub1 = await scrivener.add_processing_step(
            processing, "Step 1", "Processing step 1"
        )
        sub2 = await scrivener.add_processing_step(
            processing, "Step 2", "Processing step 2"
        )
        
        await asyncio.sleep(0.1)
        
        # Check parent-child relationships
        assert sub1.metadata.parent_id == processing.id
        assert sub2.metadata.parent_id == processing.id
        assert sub1.id in processing.metadata.children_ids
        assert sub2.id in processing.metadata.children_ids
        
        # Check that sub-blocks are registered
        sequence = scrivener.get_current_sequence()
        block_ids = [b.id for b in sequence.blocks]
        assert processing.id in block_ids
        assert sub1.id in block_ids
        assert sub2.id in block_ids
        
        await scrivener.stop()


class TestBlockValidation:
    """Test suite for block sequence validation rules."""
    
    def test_sequence_rule_validation(self):
        """Test that sequence rules are properly validated."""
        from blocks.registry import BlockSequenceRule
        
        # Valid rule
        rule = BlockSequenceRule(
            query_type="test",
            expected_sequence=[BlockType.USER, BlockType.ASSISTANT]
        )
        assert len(rule.expected_sequence) == 2
        
        # Invalid rule (empty sequence)
        with pytest.raises(ValueError, match="Sequence cannot be empty"):
            BlockSequenceRule(
                query_type="invalid",
                expected_sequence=[]
            )
    
    def test_custom_sequence_rules(self):
        """Test that custom sequence rules can be defined."""
        sequence = BlockSequence()
        
        # Add custom rule for a different query type
        sequence.sequence_rules["code_query"] = BlockSequenceRule(
            query_type="code_query",
            expected_sequence=[
                BlockType.USER,
                BlockType.INTERNAL_PROCESSING,
                BlockType.ASSISTANT
            ]
        )
        
        # Create blocks matching custom rule
        user = UserBlock("Write a function")
        processing = InternalProcessingBlock()
        assistant = AssistantBlock("Here's the function...")
        
        sequence.add_block(user)
        sequence.add_block(processing)
        sequence.add_block(assistant)
        
        # Should validate against custom rule
        assert sequence.validate_sequence("code_query")
        
        # Should fail against default rule (missing system check and welcome)
        assert not sequence.validate_sequence("default")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])