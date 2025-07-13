#!/usr/bin/env python3
"""Capture the exact processing moment when CognitionWidget shows sub-modules"""

import asyncio
from src.main import LLMReplApp
from src.core.config import Config

async def test_processing_moment():
    Config.enable_debug_mode()

    async with LLMReplApp().run_test(size=(72, 24)) as pilot:
        app = pilot.app
        await pilot.pause(0.5)

        print("=== CAPTURING PROCESSING MOMENT ===")

        # Submit message to trigger cognition
        await pilot.click("#prompt-input")
        for char in "show cognition sub-modules":
            await pilot.press(char)
        await pilot.press("enter")

        # Wait just a tiny bit for cognition to start
        await pilot.pause(0.2)

        # Check if we can see the CognitionWidget with sub-modules
        staging = app.query_one("#staging-container")
        cognition_widget = None

        for widget in staging.children:
            if type(widget).__name__ == "CognitionWidget":
                cognition_widget = widget
                break

        if cognition_widget and len(cognition_widget.sub_modules) > 0:
            print(f"✅ Found CognitionWidget with {len(cognition_widget.sub_modules)} sub-modules!")

            # Take screenshot at the perfect moment
            screenshot = app.export_screenshot(title="Processing Moment - Sub-modules Visible")
            with open("debug_screenshots/processing_moment_submodules.svg", "w") as f:
                f.write(screenshot)
            print("Screenshot saved: processing_moment_submodules.svg")

            # Also show what we captured
            for i, sub_mod in enumerate(cognition_widget.sub_modules):
                print(f"  {i+1}. {sub_mod['icon']} {sub_mod['name']} ({sub_mod['state']})")
        else:
            print("❌ CognitionWidget not found or has no sub-modules yet")

            # Take screenshot anyway to see current state
            screenshot = app.export_screenshot(title="Processing Moment - Debug State")
            with open("debug_screenshots/processing_moment_debug.svg", "w") as f:
                f.write(screenshot)
            print("Debug screenshot saved: processing_moment_debug.svg")

if __name__ == "__main__":
    asyncio.run(test_processing_moment())
