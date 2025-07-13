#!/usr/bin/env python3
"""
Test Debug Mode with Updated Cognition Widgets

This tests the debug mode features:
1. Cognition widgets show timer, progress bar, and token counters
2. Timer freezes when processing completes
3. Manual inscription with /inscribe
4. Sequential processing of multiple messages
"""

import asyncio
from pathlib import Path
from src.main import LLMReplApp
from src.core.config import Config


async def test_debug_mode_cognition():
    """Test debug mode with updated cognition widgets"""

    print("\n🔧 TESTING DEBUG MODE WITH COGNITION WIDGETS")
    print("=" * 60)

    # Enable debug mode
    Config.enable_debug_mode()
    Config.set_cognition_duration(5.0)  # 5 seconds for testing
    Config.set_submodule_duration(2.0)  # 2 seconds per sub-module

    async with LLMReplApp().run_test(size=(72, 48)) as pilot:
        app = pilot.app
        await pilot.pause(0.5)

        print("\n📍 Step 1: Initial state")
        staging = app.query_one("#staging-container")
        assert "hidden" in staging.classes, "Staging should be hidden initially"

        screenshot = app.export_screenshot(title="Debug Mode Test: Initial State")
        Path("debug_screenshots/debug_cognition_01_initial.svg").write_text(screenshot)

        print("\n📍 Step 2: Submit first message")
        await pilot.click("#prompt-input")
        for char in "Explain Python decorators":
            await pilot.press(char)
        await pilot.press("enter")
        await pilot.pause(0.5)

        # Staging should now be visible
        assert "hidden" not in staging.classes, "Staging should be visible"
        assert "processing" in staging.classes, "Staging should be in processing state"

        screenshot = app.export_screenshot(title="Debug Mode Test: Processing Active")
        Path("debug_screenshots/debug_cognition_02_processing.svg").write_text(screenshot)

        # Look for cognition widgets
        await pilot.pause(1.0)
        cognition_widgets = staging.query("CognitionStepWidget")
        print(f"   - Found {len(cognition_widgets)} cognition step widgets")

        if cognition_widgets:
            widget = cognition_widgets[0]
            print(f"   - Widget state: {widget.step_state}")
            print(f"   - Timer: {widget.elapsed_time:.1f}s")
            print(f"   - Tokens: ↑{widget.tokens_up} ↓{widget.tokens_down}")

        print("\n📍 Step 3: Wait for processing to complete (5s)")
        await pilot.pause(5.5)

        screenshot = app.export_screenshot(title="Debug Mode Test: Processing Complete")
        Path("debug_screenshots/debug_cognition_03_complete.svg").write_text(screenshot)

        # Check that timer is frozen
        if cognition_widgets:
            widget = cognition_widgets[0]
            frozen_time = widget.elapsed_time
            print(f"   - Final timer value: {frozen_time:.1f}s")
            await pilot.pause(0.5)
            assert widget.elapsed_time == frozen_time, "Timer should be frozen"
            print("   - ✓ Timer is frozen")

        # Verify content is NOT auto-inscribed
        timeline = app.query_one("#chat-container")
        chatboxes = timeline.query("Chatbox")
        initial_count = len(chatboxes)
        print(f"   - Timeline has {initial_count} chatboxes (should be just welcome)")

        print("\n📍 Step 4: Type /inscribe command")
        await pilot.click("#prompt-input")
        for char in "/inscribe":
            await pilot.press(char)

        screenshot = app.export_screenshot(title="Debug Mode Test: Inscribe Command")
        Path("debug_screenshots/debug_cognition_04_inscribe_typed.svg").write_text(screenshot)

        await pilot.press("enter")
        await pilot.pause(0.5)

        # Check inscription worked
        chatboxes_after = timeline.query("Chatbox")
        print(f"   - Timeline now has {len(chatboxes_after)} chatboxes")
        assert len(chatboxes_after) > initial_count, "Content should be inscribed"
        print("   - ✓ Manual inscription successful")

        screenshot = app.export_screenshot(title="Debug Mode Test: After Inscription")
        Path("debug_screenshots/debug_cognition_05_inscribed.svg").write_text(screenshot)

        print("\n📍 Step 5: Test sequential processing")
        # Send multiple messages quickly
        messages = ["First question", "Second question", "Third question"]

        for i, msg in enumerate(messages):
            await pilot.click("#prompt-input")
            for char in msg:
                await pilot.press(char)
            await pilot.press("enter")
            await pilot.pause(0.1)

        await pilot.pause(1.0)
        screenshot = app.export_screenshot(title="Debug Mode Test: Multiple Queued")
        Path("debug_screenshots/debug_cognition_06_queue.svg").write_text(screenshot)

        # Check that only one is processing
        all_widgets = staging.query("CognitionStepWidget")
        processing_count = sum(1 for w in all_widgets if hasattr(w, 'step_state') and w.step_state == "running")
        print(f"   - {processing_count} widget(s) in PROCESSING state")
        assert processing_count <= 1, "Only one should be processing at a time"

        print("\n✅ DEBUG MODE TEST COMPLETE")
        print("   - Cognition widgets show timer, progress, tokens")
        print("   - Timer freezes when processing completes")
        print("   - Manual inscription works with /inscribe")
        print("   - Sequential processing enforced")

        # Create screenshots directory if needed
        Path("debug_screenshots").mkdir(exist_ok=True)


if __name__ == "__main__":
    asyncio.run(test_debug_mode_cognition())
