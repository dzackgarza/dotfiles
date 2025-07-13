#!/usr/bin/env python3
"""Trace cognition events to understand why SubModuleWidgets aren't being created"""

import asyncio
from src.main import LLMReplApp
from src.core.config import Config

async def test_trace_events():
    Config.enable_debug_mode()
    Config.set_submodule_duration(2.0)  # Longer for debugging

    async with LLMReplApp().run_test(size=(72, 24)) as pilot:
        app = pilot.app
        await pilot.pause(0.5)

        print("\n=== Starting test ===")

        # Submit a message
        await pilot.click("#prompt-input")
        for char in "test":
            await pilot.press(char)
        await pilot.press("enter")

        # Check every second for the first 10 seconds
        for i in range(10):
            await pilot.pause(1.0)
            staging = app.query_one("#staging-container")
            widgets = list(staging.children)

            print(f"\n=== After {i+1} seconds ===")
            print(f"Total widgets: {len(widgets)}")

            for j, widget in enumerate(widgets):
                wtype = type(widget).__name__
                print(f"  Widget {j}: {wtype}")
                if hasattr(widget, 'sub_module'):
                    print(f"    Role: {widget.sub_module.role}")
                    print(f"    State: {widget.sub_module.state}")
                elif hasattr(widget, 'border_title'):
                    print(f"    Border title: {widget.border_title}")
                elif hasattr(widget, 'renderable'):
                    content = str(widget.renderable)[:100]
                    print(f"    Content: {content}")

if __name__ == "__main__":
    asyncio.run(test_trace_events())
