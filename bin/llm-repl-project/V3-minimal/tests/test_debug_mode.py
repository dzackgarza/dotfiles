#!/usr/bin/env python3
"""
Debug Mode Feature Test Suite

Tests the complete debug mode functionality:
- Processing widgets with timers, progress bars, and token counters
- Sequential processing enforcement
- Manual inscription with /inscribe command
- Screenshot verification of state transitions
"""

import pytest
from pathlib import Path
from datetime import datetime
from src.main import LLMReplApp
from src.core.config import Config
from src.widgets.processing_widget import ProcessingState

# Ensure debug mode is enabled for tests
Config.enable_debug_mode()
Config.USE_PROCESSING_QUEUE = True

# Screenshot directory
SCREENSHOT_DIR = Path("debug_screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)


async def take_debug_screenshot(pilot, step_name: str, step_number: int):
    """Take a screenshot for debug mode verification"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"debug_mode_{timestamp}_{step_number:02d}_{step_name}"

    # Take both SVG and PNG screenshots
    svg_path = SCREENSHOT_DIR / f"{filename}.svg"
    png_path = SCREENSHOT_DIR / f"{filename}.png"

    pilot.app.save_screenshot(str(svg_path))
    pilot.app.save_screenshot(str(png_path))

    return filename


@pytest.mark.asyncio
async def test_debug_mode_complete_flow(snap_compare):
    """Test complete debug mode flow with visual verification"""

    async with LLMReplApp().run_test() as pilot:
        app = pilot.app

        # Step 1: Initial state - idle
        await pilot.pause(1.0)
        await take_debug_screenshot(pilot, "initial_idle_state", 1)

        # Verify staging area is hidden initially
        staging = app.query_one("#staging-container")
        assert "hidden" in staging.classes

        # Step 2: Type first message
        await pilot.click("#prompt-input")
        await pilot.type("What is 2+2?")
        await take_debug_screenshot(pilot, "message_typed", 2)

        # Step 3: Submit message (should create processing widget)
        await pilot.press("enter")
        await pilot.pause(0.5)
        await take_debug_screenshot(pilot, "processing_active", 3)

        # Verify staging area is now visible and has processing class
        assert "hidden" not in staging.classes
        assert "processing" in staging.classes

        # Find the processing widget
        processing_widgets = staging.query("ProcessingWidget")
        assert len(processing_widgets) == 1
        widget = processing_widgets[0]

        # Verify widget is in processing state
        assert widget.state == ProcessingState.PROCESSING
        assert widget.elapsed_time > 0
        assert 0 < widget.progress < 1

        # Step 4: Wait for processing to complete (5 seconds)
        await pilot.pause(5.5)
        await take_debug_screenshot(pilot, "debug_mode_response_ready", 4)

        # Verify widget is now done
        assert widget.state == ProcessingState.DONE
        assert widget.progress == 1.0
        # Timer should be frozen
        frozen_time = widget.elapsed_time
        await pilot.pause(0.5)
        assert widget.elapsed_time == frozen_time  # Time didn't change

        # Step 5: Type /inscribe command
        await pilot.click("#prompt-input")
        await pilot.type("/inscribe")
        await take_debug_screenshot(pilot, "inscribe_command_typed", 5)

        # Step 6: Execute inscription
        await pilot.press("enter")
        await pilot.pause(0.5)
        await take_debug_screenshot(pilot, "after_inscription", 6)

        # Verify processing widget was removed
        processing_widgets = staging.query("ProcessingWidget")
        assert len(processing_widgets) == 0

        # Verify content was inscribed to timeline
        timeline = app.query_one("#chat-container")
        chatboxes = timeline.query("Chatbox")
        # Should have: welcome, user message, assistant response
        assert len(chatboxes) >= 3

        # Step 7: Verify timeline was updated
        await take_debug_screenshot(pilot, "timeline_updated", 7)

        # Step 8: Send another message to test sequential processing
        await pilot.click("#prompt-input")
        await pilot.type("What is 3+3?")
        await pilot.press("enter")
        await pilot.pause(0.5)
        await take_debug_screenshot(pilot, "second_message_debug_ready", 8)

        # Step 9: Use Ctrl+I shortcut for inscription
        await pilot.press("ctrl+i")
        await pilot.pause(0.5)
        await take_debug_screenshot(pilot, "ctrl_i_inscription", 9)

        # Step 10: Final state verification
        await take_debug_screenshot(pilot, "final_state", 10)


@pytest.mark.asyncio
async def test_debug_mode_sequential_processing():
    """Test that only one block processes at a time"""

    async with LLMReplApp().run_test() as pilot:
        app = pilot.app
        staging = app.query_one("#staging-container")

        # Send multiple messages quickly
        messages = ["First message", "Second message", "Third message"]

        for msg in messages:
            await pilot.click("#prompt-input")
            await pilot.type(msg)
            await pilot.press("enter")
            await pilot.pause(0.1)  # Small pause between submissions

        # Wait for widgets to be created
        await pilot.pause(1.0)

        # Get all processing widgets
        widgets = staging.query("ProcessingWidget")
        assert len(widgets) == 3

        # Check states - only first should be processing
        assert widgets[0].state == ProcessingState.PROCESSING
        assert widgets[1].state == ProcessingState.QUEUED
        assert widgets[2].state == ProcessingState.QUEUED

        # Wait for first to complete
        await pilot.pause(5.5)

        # Now second should be processing
        assert widgets[0].state == ProcessingState.DONE
        assert widgets[1].state == ProcessingState.PROCESSING
        assert widgets[2].state == ProcessingState.QUEUED

        # Wait for second to complete
        await pilot.pause(5.5)

        # Now third should be processing
        assert widgets[0].state == ProcessingState.DONE
        assert widgets[1].state == ProcessingState.DONE
        assert widgets[2].state == ProcessingState.PROCESSING


@pytest.mark.asyncio
async def test_debug_mode_timer_freeze():
    """Test that timers freeze when processing completes"""

    async with LLMReplApp().run_test() as pilot:
        app = pilot.app

        # Send a message
        await pilot.click("#prompt-input")
        await pilot.type("Test message")
        await pilot.press("enter")
        await pilot.pause(1.0)

        # Get the processing widget
        staging = app.query_one("#staging-container")
        widget = staging.query_one("ProcessingWidget")

        # Wait for completion
        await pilot.pause(5.0)

        # Verify state is done
        assert widget.state == ProcessingState.DONE

        # Record the timer value
        final_time = widget.elapsed_time
        assert final_time >= 5.0  # Should be at least 5 seconds

        # Wait and verify timer hasn't changed
        await pilot.pause(1.0)
        assert widget.elapsed_time == final_time  # Timer frozen


@pytest.mark.asyncio
async def test_debug_mode_token_display():
    """Test that token counters are displayed correctly"""

    async with LLMReplApp().run_test() as pilot:
        app = pilot.app

        # Send a message
        await pilot.click("#prompt-input")
        await pilot.type("Check tokens")
        await pilot.press("enter")
        await pilot.pause(0.5)

        # Get the processing widget
        staging = app.query_one("#staging-container")
        widget = staging.query_one("ProcessingWidget")

        # Verify token values are set
        assert 50 <= widget.tokens_up <= 200
        assert 100 <= widget.tokens_down <= 400

        # Verify they're displayed in the render
        rendered = widget.render()
        assert str(widget.tokens_up) in str(rendered)
        assert str(widget.tokens_down) in str(rendered)


@pytest.mark.asyncio
async def test_debug_mode_toggle():
    """Test toggling debug mode on/off"""

    # Start with debug mode off
    Config.disable_debug_mode()
    Config.USE_PROCESSING_QUEUE = False

    async with LLMReplApp().run_test() as pilot:
        app = pilot.app

        # Send a message - should auto-inscribe
        await pilot.click("#prompt-input")
        await pilot.type("Normal mode test")
        await pilot.press("enter")
        await pilot.pause(6.0)  # Wait for processing

        # Check timeline has the message (auto-inscribed)
        timeline = app.query_one("#chat-container")
        chatboxes = timeline.query("Chatbox")
        assert any("Normal mode test" in str(box.content) for box in chatboxes)

        # Enable debug mode
        Config.enable_debug_mode()
        Config.USE_PROCESSING_QUEUE = True

        # Send another message - should NOT auto-inscribe
        await pilot.click("#prompt-input")
        await pilot.type("Debug mode test")
        await pilot.press("enter")
        await pilot.pause(6.0)  # Wait for processing

        # Message should still be in staging
        staging = app.query_one("#staging-container")
        widgets = staging.query("ProcessingWidget")
        assert len(widgets) > 0

        # Timeline should NOT have the new message yet
        chatboxes = timeline.query("Chatbox")
        assert not any("Debug mode test" in str(box.content) for box in chatboxes)

    # Reset to debug mode for other tests
    Config.enable_debug_mode()
    Config.USE_PROCESSING_QUEUE = True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
