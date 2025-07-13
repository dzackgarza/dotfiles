#!/usr/bin/env python3
"""Test live processing widgets with real-time updates"""

import asyncio
from src.main import LLMReplApp
from src.core.config import Config

async def test_live_processing():
    """Test the live processing widgets with simulated stream events"""
    Config.enable_debug_mode()

    async with LLMReplApp().run_test(size=(90, 30)) as pilot:
        app = pilot.app
        await pilot.pause(0.5)

        print("=== TESTING LIVE PROCESSING WIDGETS ===")

        # Submit message to trigger processing
        await pilot.click("#prompt-input")
        for char in "test live processing widgets":
            await pilot.press(char)
        await pilot.press("enter")

        await pilot.pause(0.2)  # Wait for processing to start

        # Find the CognitionWidget
        staging = app.query_one("#staging-container")
        cognition_widget = None

        for widget in staging.children:
            if type(widget).__name__ == "CognitionWidget":
                cognition_widget = widget
                break

        if cognition_widget:
            print(f"✅ Found CognitionWidget with {len(cognition_widget.sub_modules)} sub-modules")

            # Test live token incrementing
            print("Testing live token increments...")
            for i in range(5):
                cognition_widget.increment_tokens("Route Query", tokens_out=10)
                await pilot.pause(0.2)

            # Test progress updates
            print("Testing progress updates...")
            for progress in [0.2, 0.4, 0.6, 0.8, 1.0]:
                cognition_widget.update_progress("Route Query", progress)
                await pilot.pause(0.3)

            # Complete the first sub-module
            cognition_widget.complete_sub_module("Route Query")
            print("✅ Completed Route Query sub-module")
            await pilot.pause(0.5)

            # Test second sub-module
            print("Testing second sub-module...")
            for i in range(3):
                cognition_widget.increment_tokens("Call Tool", tokens_out=15)
                await pilot.pause(0.2)

            # Complete all processing
            cognition_widget.complete_cognition()
            print("✅ Completed entire cognition - ready for inscription")

            # Take final screenshot
            screenshot = app.export_screenshot(title="Live Processing Test Complete")
            with open("debug_screenshots/live_processing_test.svg", "w") as f:
                f.write(screenshot)

            print("Screenshot saved: live_processing_test.svg")
            print(f"Ready for inscription: {cognition_widget.is_ready_for_inscription()}")

        else:
            print("❌ No CognitionWidget found")

if __name__ == "__main__":
    asyncio.run(test_live_processing())
