#!/usr/bin/env python3
"""
Test Live Streaming Implementation

Validates that the 5 committed user-visible behaviors are implemented:
1. Real-time streaming text (character by character)
2. Live token counters (incrementing visually)
3. Animated progress indicators (smooth 0-100%)
4. Live → Inscribed transitions (visual animation)
5. Nested sub-block streaming (sub-modules with own counters)
"""

import pytest
from src.core.live_blocks import LiveBlock, BlockState, LiveBlockManager
from src.core.animation_clock import AnimationClock

# Set high FPS for fast but real animations in tests
AnimationClock.set_testing_mode()  # 1000 FPS - fast but still validates real behavior


class TestLiveStreamingBehaviors:
    """Test the 5 committed user-visible behaviors."""

    @pytest.mark.asyncio
    async def test_streaming_text_character_by_character(self):
        """Test behavior 1: Real-time streaming text."""
        block = LiveBlock("test")
        updates = []

        def capture_update(b):
            updates.append(b.data.content)

        block.add_update_callback(capture_update)

        # Test immediate update (for API compatibility)
        block.stream_content("Hello")
        assert len(updates) >= 1
        assert updates[-1] == "Hello"

        # Reset for animated test
        updates.clear()
        block.data.content = ""

        # Test animated streaming - this validates real user behavior
        await block.stream_content_animated(
            "World", chars_per_second=1000
        )  # Fast for testing

        # Should have multiple frame updates showing character progression
        assert (
            len(updates) > 1
        ), f"Expected multiple updates for animation, got {len(updates)}"

        # Should progress through: "", "W", "Wo", "Wor", "Worl", "World"
        content_progression = [update for update in updates]
        assert "" in content_progression  # Start state
        assert "W" in content_progression  # First character
        assert "World" in content_progression  # Final state

        # Verify the progression makes sense (each step adds characters)
        for i in range(1, len(content_progression)):
            prev_content = content_progression[i - 1]
            curr_content = content_progression[i]
            assert len(curr_content) >= len(
                prev_content
            ), "Content should only grow during streaming"

    @pytest.mark.asyncio
    async def test_animated_token_counters(self):
        """Test behavior 2: Live token counters with smooth animation."""
        block = LiveBlock("test")
        token_updates = []

        def capture_tokens(b):
            token_updates.append((b.data.tokens_input, b.data.tokens_output))

        block.add_update_callback(capture_tokens)

        # Test immediate update (for API compatibility)
        block.set_tokens(10, 20)
        assert len(token_updates) >= 1
        assert token_updates[-1] == (10, 20)

        # Reset for animated test
        token_updates.clear()
        block.data.tokens_input = 0
        block.data.tokens_output = 0

        # Test animated token counting - this validates real user behavior
        await block.animate_tokens(30, 50, duration_seconds=0.1)  # Fast for testing

        # Should have multiple updates showing smooth progression
        assert (
            len(token_updates) > 1
        ), f"Expected multiple token updates for animation, got {len(token_updates)}"

        # Verify progression from (0,0) to (30,50)
        first_update = token_updates[0]
        last_update = token_updates[-1]

        assert first_update == (0, 0) or first_update[0] <= 5, "Should start near 0"
        assert last_update == (30, 50), f"Should end at (30, 50), got {last_update}"

        # Verify smooth progression (tokens should generally increase)
        for i in range(1, len(token_updates)):
            prev_input, prev_output = token_updates[i - 1]
            curr_input, curr_output = token_updates[i]
            assert (
                curr_input >= prev_input
            ), "Input tokens should not decrease during animation"
            assert (
                curr_output >= prev_output
            ), "Output tokens should not decrease during animation"

    @pytest.mark.asyncio
    async def test_animated_progress_indicators(self):
        """Test behavior 3: Animated progress indicators with smooth progression."""
        block = LiveBlock("test")
        progress_updates = []

        def capture_progress(b):
            progress_updates.append(b.data.progress)

        block.add_update_callback(capture_progress)

        # Test immediate update (for API compatibility)
        block.set_progress(1.0)
        assert len(progress_updates) >= 1
        assert progress_updates[-1] == 1.0

        # Reset for animated test
        progress_updates.clear()
        block.data.progress = 0.0

        # Test animated progress - this validates real user behavior
        await block.animate_progress(1.0, duration_seconds=0.1)  # Fast for testing

        # Should have multiple updates showing smooth progression
        assert (
            len(progress_updates) > 1
        ), f"Expected multiple progress updates for animation, got {len(progress_updates)}"

        # Verify progression from 0.0 to 1.0
        first_progress = progress_updates[0]
        last_progress = progress_updates[-1]

        assert first_progress <= 0.1, f"Should start near 0.0, got {first_progress}"
        assert (
            abs(last_progress - 1.0) < 0.01
        ), f"Should end at 1.0, got {last_progress}"

        # Verify smooth progression (progress should not decrease)
        for i in range(1, len(progress_updates)):
            prev_progress = progress_updates[i - 1]
            curr_progress = progress_updates[i]
            assert (
                curr_progress >= prev_progress - 0.01
            ), f"Progress should not decrease significantly: {prev_progress} -> {curr_progress}"

    @pytest.mark.asyncio
    async def test_live_to_inscribed_transition(self):
        """Test behavior 4: Live → Inscribed transitions with animation."""
        block = LiveBlock("test")
        state_updates = []

        def capture_state(b):
            state_updates.append(b.state)

        block.add_update_callback(capture_state)

        # Add some content and progress
        block.stream_content("Test content")
        block.set_progress(0.8)

        # Transition to inscribed with animation
        inscribed = await block.to_inscribed_block()

        # Should go through TRANSITIONING state
        assert BlockState.TRANSITIONING in state_updates
        assert block.state == BlockState.INSCRIBED

        # Content should include transition message
        assert "Inscribing to Sacred Timeline" in block.data.content
        assert "Test content" in inscribed.content
        assert "Inscribing to Sacred Timeline" in inscribed.content

    @pytest.mark.asyncio
    async def test_nested_sub_block_streaming(self):
        """Test behavior 5: Nested sub-block streaming with individual counters."""
        parent_block = LiveBlock("cognition")

        # Run cognition simulation which creates nested sub-blocks
        await parent_block.start_mock_simulation("cognition")

        # Should have created sub-blocks
        assert len(parent_block.data.sub_blocks) > 0, "Expected nested sub-blocks"

        # Each sub-block should have content and tokens
        for sub_block in parent_block.data.sub_blocks:
            assert (
                sub_block.data.content
            ), f"Sub-block should have content: {sub_block.data.content}"
            # Most sub-blocks should have token counts
            total_tokens = sub_block.data.tokens_input + sub_block.data.tokens_output
            assert total_tokens > 0, f"Sub-block should have tokens: {total_tokens}"

    @pytest.mark.asyncio
    async def test_specific_sub_module_scenarios(self):
        """Test that different sub-module scenarios work with streaming."""
        scenarios = ["route_analysis", "tool_selection", "response_gen"]

        for scenario in scenarios:
            block = LiveBlock("sub_module")
            await block.start_mock_simulation(scenario)

            # Each scenario should generate content and tokens
            assert block.data.content, f"Scenario {scenario} should have content"
            assert block.data.progress == 1.0, f"Scenario {scenario} should complete"
            total_tokens = block.data.tokens_input + block.data.tokens_output
            assert total_tokens > 0, f"Scenario {scenario} should have tokens"

    def test_live_block_manager_integration(self):
        """Test that LiveBlockManager properly manages blocks."""
        manager = LiveBlockManager()

        # Create blocks through manager
        block1 = manager.create_live_block("test1", "Initial content")
        block2 = manager.create_live_block("test2")

        # Manager should track blocks
        assert len(manager.live_blocks) == 2
        assert block1.id in manager.live_blocks
        assert block2.id in manager.live_blocks

        # Blocks should have callbacks registered
        assert len(block1.content_update_callbacks) > 0
        assert len(block2.content_update_callbacks) > 0
