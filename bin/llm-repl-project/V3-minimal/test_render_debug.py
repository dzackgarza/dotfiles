#!/usr/bin/env python3
"""Debug what CognitionWidget is actually rendering"""

import asyncio
from src.main import LLMReplApp
from src.core.config import Config

async def test_render_debug():
    Config.enable_debug_mode()

    async with LLMReplApp().run_test(size=(72, 24)) as pilot:
        app = pilot.app
        await pilot.pause(0.5)

        # Submit message to trigger cognition
        await pilot.click("#prompt-input")
        for char in "render debug":
            await pilot.press(char)
        await pilot.press("enter")

        # Wait for cognition to start
        await pilot.pause(0.3)

        # Find the CognitionWidget
        staging = app.query_one("#staging-container")
        cognition_widget = None

        for widget in staging.children:
            if type(widget).__name__ == "CognitionWidget":
                cognition_widget = widget
                break

        if cognition_widget:
            print("Found CognitionWidget:")
            print(f"  sub_modules count: {len(cognition_widget.sub_modules)}")
            print(f"  is_live: {cognition_widget.is_live}")
            print(f"  elapsed_time: {cognition_widget.elapsed_time}")

            # Show sub-modules
            for i, sub_mod in enumerate(cognition_widget.sub_modules):
                print(f"  {i+1}: {sub_mod}")

            # Get the rendered content
            try:
                content = cognition_widget.render()
                print(f"\nRendered content type: {type(content)}")
                print(f"Rendered content:\n{content}")
            except Exception as e:
                print(f"Render error: {e}")
        else:
            print("No CognitionWidget found")

if __name__ == "__main__":
    asyncio.run(test_render_debug())
