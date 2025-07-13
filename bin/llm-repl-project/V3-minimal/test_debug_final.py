#!/usr/bin/env python3
"""Final debug mode test"""

import asyncio
from src.main import LLMReplApp
from src.core.config import Config

async def test_debug_final():
    Config.enable_debug_mode()
    Config.set_submodule_duration(1.0)  # Faster for testing

    async with LLMReplApp().run_test(size=(72, 24)) as pilot:
        app = pilot.app
        await pilot.pause(0.5)

        # Submit
        await pilot.click("#prompt-input")
        for char in "test message":
            await pilot.press(char)
        await pilot.press("enter")

        # Wait for events to be emitted
        await pilot.pause(0.5)
        print("\n=== After 0.5s ===")
        check_widgets(app)

        await pilot.pause(2.0)
        print("\n=== After 2.5s ===")
        check_widgets(app)

        await pilot.pause(3.0)
        print("\n=== After 5.5s (all done) ===")
        check_widgets(app)

        # Test inscription
        print("\n=== Testing /inscribe ===")
        await pilot.click("#prompt-input")
        for char in "/inscribe":
            await pilot.press(char)
        await pilot.press("enter")
        await pilot.pause(0.5)

        timeline = app.query_one("#chat-container")
        print(f"Timeline children: {len(list(timeline.children))}")

def check_widgets(app):
    staging = app.query_one("#staging-container")
    widgets = list(staging.children)
    print(f"Total widgets: {len(widgets)}")

    for widget in widgets:
        wtype = type(widget).__name__
        if wtype == "SubModuleWidget":
            print(f"  - SubModuleWidget: {widget.sub_module.role}")
            print(f"    State: {widget.sub_module.state}")
            print(f"    Timer: {widget.elapsed_time:.1f}s")
            print(f"    Tokens: ↑{widget.sub_module.data.tokens_input} ↓{widget.sub_module.data.tokens_output}")
        else:
            print(f"  - {wtype}")

if __name__ == "__main__":
    asyncio.run(test_debug_final())
