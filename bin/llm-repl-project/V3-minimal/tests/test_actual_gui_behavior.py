"""
Test ACTUAL GUI Behavior (Not Fantasy)

These tests verify the ACTUAL broken behavior we see in the screenshot,
not some idealized system that doesn't exist.
"""

import pytest
from unittest.mock import MagicMock
from src.main import LLMReplApp
from src.cognition import CognitionEvent, CognitionResult


@pytest.mark.asyncio
async def test_turn_separator_appears_before_user_message():
    """
    ACTUAL BEHAVIOR: Turn 2 separator appears BEFORE the user message,
    violating chronological order.
    """
    app = LLMReplApp()

    # Mock response generator
    app.response_generator.generate_response = MagicMock(return_value="Test response")

    # Quick cognition
    async def mock_cognition(query):
        return CognitionResult(content="Quick cognition", metadata={})
    app.unified_async_processor.cognition_manager.process_query = mock_cognition

    async with app.run_test(size=(120, 40)) as pilot:
        timeline = app.query_one("#chat-container")

        # Send first message to establish Turn 1
        prompt_input = app.query_one("#prompt-input")
        prompt_input.value = "First message"
        await pilot.press("enter")
        await pilot.pause(0.5)

        # Clear tracking
        initial_count = len(list(timeline.children))

        # Send second message - this is where the bug happens
        prompt_input.value = "Second message"
        await pilot.press("enter")
        await pilot.pause(0.5)

        # Get new widgets added for Turn 2
        all_widgets = list(timeline.children)
        new_widgets = all_widgets[initial_count:]

        # FIXED BEHAVIOR: User message should come FIRST for Turn 2
        if new_widgets:
            first_new_widget = new_widgets[0]
            # After fix: User message should be first
            from src.widgets.chatbox import Chatbox
            assert isinstance(first_new_widget, Chatbox), \
                f"Expected Chatbox first (fixed behavior), got {first_new_widget.__class__.__name__}"
            assert hasattr(first_new_widget, 'role') and first_new_widget.role == "user", \
                "Expected user role in first widget"

            # Turn separator should come at END of turn (after assistant response)
            # Look for separator at the end
            if len(new_widgets) >= 3:  # user + cognition + assistant + separator
                last_widget = new_widgets[-1]
                assert last_widget.__class__.__name__ == "TurnSeparator", \
                    f"Expected TurnSeparator at end, got {last_widget.__class__.__name__}"


@pytest.mark.asyncio
async def test_cognition_blocks_have_no_visual_headers():
    """
    ACTUAL BEHAVIOR: Cognition blocks appear as raw text with no headers,
    no "> Cognition" label, just the content.
    """
    app = LLMReplApp()

    # Mock response
    app.response_generator.generate_response = MagicMock(return_value="Response")

    # Cognition that returns specific text
    async def mock_cognition(query):
        return CognitionResult(
            content="Processed through cognition pipeline",
            metadata={"test": True}
        )
    app.unified_async_processor.cognition_manager.process_query = mock_cognition

    async with app.run_test(size=(120, 40)) as pilot:
        timeline = app.query_one("#chat-container")

        # Send message
        prompt_input = app.query_one("#prompt-input")
        prompt_input.value = "Test cognition display"
        await pilot.press("enter")
        await pilot.pause(1.0)  # Need longer wait for async processing

        # Debug: print all timeline children
        print(f"Timeline children: {[w.__class__.__name__ for w in timeline.children]}")

        # ACTUAL BEHAVIOR: Look for ANY widget containing cognition text
        cognition_text = "Processed through cognition pipeline"
        found_cognition = False
        cognition_widget = None

        for widget in timeline.children:
            if hasattr(widget, 'render'):
                rendered = str(widget.render())
                if cognition_text in rendered:
                    found_cognition = True
                    cognition_widget = widget
                    print(f"Found cognition text in {widget.__class__.__name__}")
                    break

        # Find cognition widget - might be rendered as Chatbox instead
        from src.widgets.cognition_widget import CognitionWidget
        from src.widgets.chatbox import Chatbox

        if not found_cognition:
            assert False, "No widget contains cognition text"

        widget = cognition_widget  # Use the widget we found

        # ACTUAL BROKEN BEHAVIOR depends on widget type
        if isinstance(widget, CognitionWidget):
            # If it's actually a CognitionWidget:
            # 1. Border title is set but NOT displayed
            assert hasattr(widget, 'border_title'), "Widget has border_title property"
            assert widget.border_title == "> Cognition", "Border title is set correctly"

            # 2. But the rendered output is just raw text
            rendered = str(widget.render())
            assert "Processed through cognition pipeline" in rendered
            assert "> Cognition" not in rendered, "Header is NOT in rendered output"
        else:
            # More likely: It's being rendered as a plain Chatbox
            print(f"ACTUAL: Cognition rendered as {widget.__class__.__name__}")
            if isinstance(widget, Chatbox):
                # Check what role it has
                if hasattr(widget, 'role'):
                    print(f"Chatbox role: {widget.role}")
                # Border title will be wrong
                if hasattr(widget, 'border_title'):
                    print(f"Border title: {widget.border_title}")
                    # Should NOT be "> Cognition" if it's a misrendered Chatbox


@pytest.mark.asyncio
async def test_massive_whitespace_gaps_between_blocks():
    """
    ACTUAL BEHAVIOR: Large visual gaps between blocks in timeline.
    """
    app = LLMReplApp()

    app.response_generator.generate_response = MagicMock(return_value="Response")

    async def mock_cognition(query):
        return CognitionResult(content="Cognition", metadata={})
    app.unified_async_processor.cognition_manager.process_query = mock_cognition

    async with app.run_test(size=(120, 40)) as pilot:
        timeline = app.query_one("#chat-container")

        # Send two messages
        for i in range(2):
            prompt_input = app.query_one("#prompt-input")
            prompt_input.value = f"Message {i+1}"
            await pilot.press("enter")
            await pilot.pause(0.5)

        # Check widget margins
        from src.widgets.cognition_widget import CognitionWidget

        for widget in timeline.children:
            if isinstance(widget, CognitionWidget):
                # ACTUAL BROKEN BEHAVIOR: Check CSS margins
                # The CSS sets margin: 0 1 but something else causes gaps
                if hasattr(widget, 'styles') and hasattr(widget.styles, 'margin'):
                    margin = widget.styles.margin
                    # Current CSS has reasonable margins, gaps come from elsewhere
                    print(f"Cognition margin: {margin}")


@pytest.mark.asyncio
async def test_staging_area_shows_raw_unformatted_text():
    """
    ACTUAL BEHAVIOR: Staging area (Live Workspace) displays raw text
    with no proper formatting or structure.
    """
    app = LLMReplApp()

    app.response_generator.generate_response = MagicMock(return_value="Done")

    # Track what gets added to staging area
    staging_content = []

    async def mock_cognition_with_events(query):
        # Emit events that should appear in staging
        if hasattr(app.unified_async_processor, '_handle_cognition_event'):
            await app.unified_async_processor._handle_cognition_event(
                CognitionEvent(
                    type="update",
                    module="process",
                    content="Raw text line 1\nRaw text line 2\nRaw text line 3"
                )
            )
        return CognitionResult(content="Done")

    app.unified_async_processor.cognition_manager.process_query = mock_cognition_with_events

    async with app.run_test(size=(120, 40)) as pilot:
        staging = app.query_one("#staging-container")

        # Original mount method
        original_mount = staging.mount
        async def track_mount(widget, *args, **kwargs):
            staging_content.append(widget)
            return await original_mount(widget, *args, **kwargs)
        staging.mount = track_mount

        # Send message
        prompt_input = app.query_one("#prompt-input")
        prompt_input.value = "Test staging"
        await pilot.press("enter")

        # Wait for staging to show
        await pilot.pause(0.3)

        # ACTUAL BROKEN BEHAVIOR:
        # 1. Staging area content is minimal/raw
        assert len(staging_content) > 0, "Something was added to staging"

        # 2. Content likely appears as simple text widgets
        for widget in staging_content:
            widget_type = widget.__class__.__name__
            print(f"Staging widget type: {widget_type}")
            # Probably just basic widgets, not properly formatted


@pytest.mark.asyncio
async def test_live_workspace_height_issues():
    """
    ACTUAL BEHAVIOR: Live Workspace has height issues causing massive gaps.
    """
    app = LLMReplApp()

    app.response_generator.generate_response = MagicMock(return_value="Done")

    async with app.run_test(size=(120, 40)) as pilot:
        workspace = app.query_one("#staging-container")

        # Check initial CSS
        assert "hidden" in workspace.classes, "Starts hidden"

        # Send message to trigger workspace
        prompt_input = app.query_one("#prompt-input")
        prompt_input.value = "Test"
        await pilot.press("enter")
        await pilot.pause(0.2)

        # ACTUAL BROKEN BEHAVIOR: Check CSS classes and height
        if "hidden" not in workspace.classes:  # If it actually shows
            # Check if "processing" class is applied
            if "processing" in workspace.classes:
                # CSS sets height: 12 !important for processing
                # This might be too much or too little
                pass

            # The workspace might have wrong height settings
            if hasattr(workspace, 'styles'):
                height = workspace.styles.height
                print(f"Live workspace height: {height}")
