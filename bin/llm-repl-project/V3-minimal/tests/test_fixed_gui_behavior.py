"""
Test Fixed GUI Behavior

These tests verify that our fixes actually work and prevent regressions.
They test the FIXED behavior, not the broken behavior.
"""

import asyncio
import pytest
from src.test_harness.base import AppTestHarness
from src.main import LLMReplApp
from src.widgets.chatbox import Chatbox


@pytest.mark.asyncio
async def test_turn_separator_fixed_chronological_order():
    """
    FIXED BEHAVIOR: Turn separator appears AFTER the complete turn,
    maintaining proper chronological order.
    
    Turn flow should be:
    1. User message (start of Turn 2)
    2. Cognition block  
    3. Assistant response
    4. Turn separator (end of Turn 2)
    """
    harness = AppTestHarness()
    async with harness.pilot(LLMReplApp()) as pilot:
        app = pilot.app
        await pilot.pause()

        # Get initial widget count (should have welcome message)
        chat_container = app.query_one("#chat-container")
        initial_count = len(chat_container.children)

        # Submit a message (this starts Turn 2)
        prompt_input = app.query_one("#prompt-input")
        prompt_input.text = "test message"

        # Trigger submission
        await pilot.press("enter")
        await pilot.pause()

        # Allow async processing time
        await asyncio.sleep(3.0)

        # Get new widgets added after submission
        new_widgets = list(chat_container.children)[initial_count:]

        # Verify proper order
        assert len(new_widgets) >= 3, f"Expected at least 3 new widgets, got {len(new_widgets)}"

        # First should be user message (start of Turn 2)
        assert isinstance(new_widgets[0], Chatbox), \
            f"First widget should be Chatbox (user), got {new_widgets[0].__class__.__name__}"
        assert new_widgets[0].role == "user", \
            f"First widget should have role 'user', got {new_widgets[0].role}"

        # Last should be turn separator (end of Turn 2)
        last_widget = new_widgets[-1]
        assert last_widget.__class__.__name__ == "TurnSeparator", \
            f"Last widget should be TurnSeparator, got {last_widget.__class__.__name__}"


@pytest.mark.asyncio
async def test_cognition_has_header():
    """
    FIXED BEHAVIOR: Cognition blocks have "> Cognition" header
    """
    harness = AppTestHarness()
    async with harness.pilot(LLMReplApp()) as pilot:
        app = pilot.app
        await pilot.pause()

        # Submit a message
        prompt_input = app.query_one("#prompt-input")
        prompt_input.text = "test cognition header"
        await pilot.press("enter")
        await pilot.pause()

        # Allow processing
        await asyncio.sleep(3.0)

        # Find cognition widget
        from src.widgets.cognition_widget import CognitionWidget
        cognition_widgets = app.query(CognitionWidget)

        assert len(cognition_widgets) > 0, "No cognition widgets found"

        # Check content includes header
        cognition = cognition_widgets[0]
        assert "> Cognition" in cognition.content, \
            f"Cognition content missing header. Content: {cognition.content[:100]}..."


@pytest.mark.asyncio
async def test_sub_modules_on_separate_lines():
    """
    FIXED BEHAVIOR: Sub-modules render on separate lines, not jammed together
    """
    harness = AppTestHarness()
    async with harness.pilot(LLMReplApp()) as pilot:
        app = pilot.app
        await pilot.pause()

        # Submit a message
        prompt_input = app.query_one("#prompt-input")
        prompt_input.text = "test sub-modules"
        await pilot.press("enter")
        await pilot.pause()

        # Allow processing
        await asyncio.sleep(3.0)

        # Find cognition widget
        from src.widgets.cognition_widget import CognitionWidget
        cognition_widgets = app.query(CognitionWidget)

        assert len(cognition_widgets) > 0, "No cognition widgets found"

        cognition = cognition_widgets[0]
        # Sub-modules should be on separate lines with bullet points
        # Not all jammed on one line
        content_lines = cognition.content.split('\n')

        # Count lines that start with bullet point
        bullet_lines = [line for line in content_lines if line.strip().startswith('•')]

        # Should have multiple bullet lines if sub-modules are properly formatted
        assert len(bullet_lines) >= 2, \
            f"Sub-modules not on separate lines. Found {len(bullet_lines)} bullet lines"


@pytest.mark.asyncio
async def test_staging_area_reasonable_height():
    """
    FIXED BEHAVIOR: Staging area has reasonable height (8 units, not 12)
    """
    harness = AppTestHarness()
    async with harness.pilot(LLMReplApp()) as pilot:
        app = pilot.app
        await pilot.pause()

        # Get staging container
        staging = app.query_one("#staging-container")

        # Check CSS classes include our fixed height
        # The processing class should set height to 8
        from src.widgets.live_workspace import LiveWorkspaceWidget
        assert isinstance(staging, LiveWorkspaceWidget)

        # The CSS should have our fixed height
        # This is a simple check that our CSS fix is loaded
        css_content = staging.DEFAULT_CSS
        assert "height: 8" in css_content, \
            "Staging area CSS doesn't have fixed height of 8"
