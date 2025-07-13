#!/usr/bin/env python3
"""Simple test to check debug mode widgets"""

import asyncio
from src.main import LLMReplApp
from src.core.config import Config

async def test_simple_debug():
    Config.enable_debug_mode()

    async with LLMReplApp().run_test(size=(72, 24)) as pilot:
        app = pilot.app
        await pilot.pause(0.5)

        # Submit a message
        await pilot.click("#prompt-input")
        for char in "test":
            await pilot.press(char)
        await pilot.press("enter")

        # Wait for all sub-modules to be created (3 modules * 2s each = 6s)
        await pilot.pause(8.0)

        # Check staging area
        staging = app.query_one("#staging-container")
        print(f"\nStaging visible: {'hidden' not in staging.classes}")
        print(f"Staging classes: {staging.classes}")

        # Look for widgets
        all_widgets = list(staging.children)
        print(f"\nTotal widgets in staging: {len(all_widgets)}")

        for i, widget in enumerate(all_widgets):
            print(f"\nWidget {i}:")
            print(f"  Type: {type(widget).__name__}")
            print(f"  Classes: {widget.classes}")
            if hasattr(widget, 'sub_module'):
                print(f"  Sub-module role: {widget.sub_module.role}")
                print(f"  Sub-module state: {widget.sub_module.state}")
                print(f"  Timer: {getattr(widget, 'elapsed_time', 'N/A')}")

        # Save screenshot
        screenshot = app.export_screenshot(title="Simple Debug Test")
        with open("debug_simple_test.svg", "w") as f:
            f.write(screenshot)
        print("\nScreenshot saved: debug_simple_test.svg")

if __name__ == "__main__":
    asyncio.run(test_simple_debug())
