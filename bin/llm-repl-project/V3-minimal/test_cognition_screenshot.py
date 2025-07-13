#!/usr/bin/env python3
"""Test CognitionWidget rendering with screenshot"""

import asyncio
from src.main import LLMReplApp
from src.core.config import Config

async def test_cognition_screenshot():
    Config.enable_debug_mode()

    async with LLMReplApp().run_test(size=(72, 24)) as pilot:
        app = pilot.app
        await pilot.pause(0.5)

        # Submit message to trigger cognition
        await pilot.click("#prompt-input")
        for char in "debug cognition test":
            await pilot.press(char)
        await pilot.press("enter")

        # Wait for cognition to process
        await pilot.pause(1.0)

        # Check the CognitionWidget state
        staging = app.query_one("#staging-container")
        cognition_widget = None

        for widget in staging.children:
            if type(widget).__name__ == "CognitionWidget":
                cognition_widget = widget
                break

        if cognition_widget:
            print("Found CognitionWidget:")
            print(f"  is_live: {cognition_widget.is_live}")
            print(f"  elapsed_time: {cognition_widget.elapsed_time}")
            print(f"  sub_modules: {len(cognition_widget.sub_modules)}")

            # Force a display update
            cognition_widget._update_display()

            # Check what's actually being rendered
            try:
                rendered = cognition_widget.render()
                print(f"  rendered type: {type(rendered)}")
                print(f"  rendered content preview: {str(rendered)[:200]}...")
            except Exception as e:
                print(f"  render error: {e}")

        # Take screenshot
        screenshot = app.export_screenshot(title="CognitionWidget Debug")
        with open("debug_screenshots/cognition_widget_debug.svg", "w") as f:
            f.write(screenshot)

        print("Screenshot saved: cognition_widget_debug.svg")

if __name__ == "__main__":
    asyncio.run(test_cognition_screenshot())
