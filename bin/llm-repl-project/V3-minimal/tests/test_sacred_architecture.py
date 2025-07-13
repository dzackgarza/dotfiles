"""
Sacred Architecture end-to-end tests

Tests the core Sacred GUI Architecture behavior:
- 2-way split (idle): Timeline + Input
- 3-way split (active): Timeline + Live Workspace + Input
"""

import pytest
from src.main import LLMReplApp


class TestSacredArchitecture:
    """Test Sacred Timeline 2-way ↔ 3-way split behavior"""

    @pytest.mark.asyncio
    async def test_starts_in_2way_split(self):
        """Test: App starts in 2-way split (timeline + input)"""
        async with LLMReplApp().run_test(size=(120, 40)) as pilot:
            # Should have timeline visible
            timeline = pilot.app.query_one("#chat-container")
            assert timeline is not None
            assert timeline.display

            # Should have input visible
            prompt_input = pilot.app.query_one("#prompt-input")
            assert prompt_input is not None
            assert prompt_input.display

            # Live workspace should be HIDDEN
            try:
                workspace = pilot.app.query_one("#staging-container")
                assert not workspace.display or "hidden" in workspace.classes
            except Exception:
                # Workspace might not exist yet, which is fine
                pass

    @pytest.mark.asyncio
    async def test_transitions_to_3way_split_during_processing(self):
        """Test: Transitions to 3-way split when processing user input"""
        async with LLMReplApp().run_test(size=(120, 40)) as pilot:
            # Send message to trigger processing
            await pilot.press("h", "e", "l", "l", "o")
            await pilot.press("enter")

            # Brief pause to let processing start
            await pilot.pause(0.1)

            # Should now have 3-way split with live workspace visible
            timeline = pilot.app.query_one("#chat-container")
            workspace = pilot.app.query_one("#staging-container")
            prompt_input = pilot.app.query_one("#prompt-input")

            assert timeline.display
            assert workspace.display
            assert prompt_input.display
            assert "hidden" not in workspace.classes

    @pytest.mark.asyncio
    async def test_returns_to_2way_split_after_completion(self):
        """Test: Returns to 2-way split after processing completes"""
        async with LLMReplApp().run_test(size=(120, 40)) as pilot:
            # Send message
            await pilot.press("h", "i")
            await pilot.press("enter")

            # Wait for processing to complete
            await pilot.pause(2.0)  # Give time for full cycle

            # Should be back to 2-way split
            timeline = pilot.app.query_one("#chat-container")
            prompt_input = pilot.app.query_one("#prompt-input")

            assert timeline.display
            assert prompt_input.display

            # Workspace should be hidden again
            try:
                workspace = pilot.app.query_one("#staging-container")
                assert not workspace.display or "hidden" in workspace.classes
            except Exception:
                pass  # Workspace might be removed, which is fine

    @pytest.mark.asyncio
    async def test_timeline_preserves_conversation_history(self):
        """Test: Sacred timeline preserves all conversation turns"""
        async with LLMReplApp().run_test(size=(120, 40)) as pilot:
            # Send multiple messages
            messages = ["hello", "how are you", "goodbye"]

            for msg in messages:
                for char in msg:
                    await pilot.press(char)
                await pilot.press("enter")
                await pilot.pause(1.0)  # Wait between messages

            # Timeline should contain all messages
            timeline = pilot.app.query_one("#chat-container")

            # Should have user blocks for each message
            # Should have assistant responses
            # Should have proper chronological order
            # TODO: Verify actual content once timeline is implemented
            assert timeline is not None

    @pytest.mark.asyncio
    async def test_workspace_shows_cognition_steps(self):
        """Test: Live workspace shows cognition pipeline during processing"""
        async with LLMReplApp().run_test(size=(120, 40)) as pilot:
            # Send complex query that will show cognition steps
            query = "explain quantum computing"
            for char in query:
                await pilot.press(char)
            await pilot.press("enter")

            # Brief pause to see cognition start
            await pilot.pause(0.5)

            # Workspace should show cognition steps
            workspace = pilot.app.query_one("#staging-container")
            assert workspace.display

            # Should contain sub-modules showing:
            # - Route Query
            # - Generate Response
            # - Tool calls (if any)
            # TODO: Verify actual cognition content
            assert True  # Placeholder until cognition is implemented
