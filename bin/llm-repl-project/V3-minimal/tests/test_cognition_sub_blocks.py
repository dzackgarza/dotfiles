"""Tests for cognition sub-blocks functionality"""

import pytest
from src.sacred_timeline import timeline, SubBlock
from src.core.input_processor import InputProcessor
from src.core.response_generator import ResponseGenerator


@pytest.fixture(autouse=True)
def clear_timeline_fixture():
    """Clear the timeline before each test"""
    timeline.clear_timeline()


class TestCognitionSubBlocks:
    """Test the 3 sub-block cognition pipeline"""

    def test_cognition_block_has_three_sub_blocks(self):
        """Test that cognition blocks are created with 3 sub-blocks"""
        # Setup
        response_generator = ResponseGenerator()
        input_processor = InputProcessor(timeline, response_generator)

        # Process user input
        user_input = "test cognition pipeline"
        input_processor.process_user_input(user_input)

        # Get blocks from timeline
        blocks = timeline.get_blocks()

        # Should have: system (welcome), user, cognition, assistant
        assert len(blocks) >= 3

        # Find the cognition block
        cognition_block = None
        for block in blocks:
            if block.role == "cognition":
                cognition_block = block
                break

        assert cognition_block is not None, "Cognition block should exist"
        assert len(cognition_block.sub_blocks) == 3, "Should have exactly 3 sub-blocks"

        # Verify sub-blocks are properly structured
        expected_types = ["route_query", "call_tool", "format_output"]
        for i, sub_block in enumerate(cognition_block.sub_blocks):
            assert isinstance(sub_block, SubBlock)
            assert sub_block.type == expected_types[i]
            assert sub_block.content != ""
            assert sub_block.id != ""

    def test_cognition_sub_block_content(self):
        """Test that sub-blocks contain the expected cognition steps"""
        response_generator = ResponseGenerator()
        input_processor = InputProcessor(timeline, response_generator)

        # Process user input
        input_processor.process_user_input("test")

        # Get cognition block
        blocks = timeline.get_blocks()
        cognition_block = next((b for b in blocks if b.role == "cognition"), None)

        assert cognition_block is not None

        # Verify the 3 expected steps - check sub_block content directly
        expected_steps = ["Model:", "Status:"]

        for sub_block in cognition_block.sub_blocks:
            content = sub_block.content
            # Each sub-block should have model and status info
            assert "Model:" in content, f"Sub-block missing model info: {content}"
            assert "Status:" in content, f"Sub-block missing status info: {content}"

        # Verify we have the correct types
        actual_types = [sub_block.type for sub_block in cognition_block.sub_blocks]
        expected_types = ["route_query", "call_tool", "format_output"]
        assert (
            actual_types == expected_types
        ), f"Expected types {expected_types}, found {actual_types}"

    def test_cognition_block_metadata(self):
        """Test that cognition blocks have proper timing and token metadata"""
        response_generator = ResponseGenerator()
        input_processor = InputProcessor(timeline, response_generator)

        # Process user input
        input_processor.process_user_input("test metadata")

        # Get cognition block
        blocks = timeline.get_blocks()
        cognition_block = next((b for b in blocks if b.role == "cognition"), None)

        assert cognition_block is not None

        # Verify metadata
        assert cognition_block.time_taken is not None
        assert cognition_block.time_taken > 0
        assert cognition_block.tokens_input is not None
        assert cognition_block.tokens_input > 0
        assert cognition_block.tokens_output is not None
        assert cognition_block.tokens_output > 0

    def test_cognition_block_main_content(self):
        """Test that the main cognition block has proper summary content"""
        response_generator = ResponseGenerator()
        input_processor = InputProcessor(timeline, response_generator)

        # Process user input
        input_processor.process_user_input("test summary")

        # Get cognition block
        blocks = timeline.get_blocks()
        cognition_block = next((b for b in blocks if b.role == "cognition"), None)

        assert cognition_block is not None

        # Verify main content has pipeline summary
        content = cognition_block.content
        assert "Cognition Pipeline" in content
        assert "Summary" in content
        assert "Total Tokens" in content
        assert "Pipeline" in content
        assert "Route → Tool → Format" in content
