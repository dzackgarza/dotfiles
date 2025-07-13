#!/usr/bin/env python3
"""Test complete debug mode workflow from processing to inscription"""

import asyncio
from src.main import LLMReplApp
from src.core.config import Config

async def test_debug_workflow():
    """Test the complete debug mode workflow"""
    Config.enable_debug_mode()

    async with LLMReplApp().run_test(size=(90, 30)) as pilot:
        app = pilot.app
        await pilot.pause(0.5)

        print("=== TESTING COMPLETE DEBUG WORKFLOW ===")

        # Step 1: Submit message to trigger processing
        print("Step 1: Submitting message...")
        await pilot.click("#prompt-input")
        for char in "debug workflow test":
            await pilot.press(char)
        await pilot.press("enter")

        await pilot.pause(1.0)  # Wait for processing

        # Step 2: Take screenshot of processing state
        screenshot = app.export_screenshot(title="Debug Processing State")
        with open("debug_screenshots/debug_workflow_01_processing.svg", "w") as f:
            f.write(screenshot)
        print("Screenshot 1: debug_workflow_01_processing.svg")

        # Step 3: Test manual inscription with /inscribe command
        print("Step 3: Testing /inscribe command...")
        await pilot.click("#prompt-input")
        for char in "/inscribe":
            await pilot.press(char)
        await pilot.press("enter")

        await pilot.pause(0.5)  # Wait for inscription

        # Step 4: Take screenshot after inscription
        screenshot = app.export_screenshot(title="Debug After Inscription")
        with open("debug_screenshots/debug_workflow_02_inscribed.svg", "w") as f:
            f.write(screenshot)
        print("Screenshot 2: debug_workflow_02_inscribed.svg")

        # Step 5: Test second message to verify system is ready
        print("Step 5: Testing second message...")
        await pilot.click("#prompt-input")
        for char in "second message test":
            await pilot.press(char)
        await pilot.press("enter")

        await pilot.pause(1.0)

        # Step 6: Final screenshot
        screenshot = app.export_screenshot(title="Debug Second Message")
        with open("debug_screenshots/debug_workflow_03_second_message.svg", "w") as f:
            f.write(screenshot)
        print("Screenshot 3: debug_workflow_03_second_message.svg")

        print("✅ Complete debug workflow test finished!")

if __name__ == "__main__":
    asyncio.run(test_debug_workflow())
