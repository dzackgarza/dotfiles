#!/usr/bin/env python3
"""Quick test to see if SubModuleWidgets are created during cognition"""

import asyncio
from src.main import LLMReplApp
from src.core.config import Config

async def test_quick_debug():
    Config.enable_debug_mode()
    Config.set_submodule_duration(1.0)  # Fast processing

    async with LLMReplApp().run_test(size=(72, 24)) as pilot:
        app = pilot.app
        await pilot.pause(0.5)

        print("\n=== Starting test ===")

        # Submit a message
        await pilot.click("#prompt-input")
        for char in "test":
            await pilot.press(char)
        await pilot.press("enter")

        # Check after 4 seconds (should be done)
        await pilot.pause(4.0)

        staging = app.query_one("#staging-container")
        widgets = list(staging.children)

        print("\nFinal state:")
        print(f"Total widgets: {len(widgets)}")

        for j, widget in enumerate(widgets):
            wtype = type(widget).__name__
            print(f"  Widget {j}: {wtype}")
            if hasattr(widget, 'sub_module'):
                print(f"    Role: {widget.sub_module.role}")
                print(f"    State: {widget.sub_module.state}")

if __name__ == "__main__":
    asyncio.run(test_quick_debug())
