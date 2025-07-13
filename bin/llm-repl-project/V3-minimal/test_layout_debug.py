#!/usr/bin/env python3
"""Debug the staging area layout issue"""

import asyncio
from src.main import LLMReplApp
from src.core.config import Config

async def test_layout_debug():
    Config.enable_debug_mode()

    async with LLMReplApp().run_test(size=(72, 24)) as pilot:
        app = pilot.app
        await pilot.pause(0.5)

        print("=== LAYOUT DEBUG ===")

        # Submit message to trigger cognition
        await pilot.click("#prompt-input")
        for char in "layout test":
            await pilot.press(char)
        await pilot.press("enter")

        await pilot.pause(1.0)

        # Examine staging area layout
        staging = app.query_one("#staging-container")
        print("Staging container:")
        print(f"  Size: {staging.size}")
        print(f"  Region: {staging.region}")
        print(f"  Classes: {staging.classes}")
        print(f"  Scrollable height: {staging.scrollable_content_region}")

        # Check each child widget
        for i, widget in enumerate(staging.children):
            wtype = type(widget).__name__
            print(f"\nWidget {i}: {wtype}")
            print(f"  Size: {widget.size}")
            print(f"  Region: {widget.region}")
            print(f"  Visible: {widget.visible}")

            if wtype == "CognitionWidget":
                print(f"  Content height estimate: {len(str(widget.render()).split('\\n'))} lines")
                print(f"  Sub-modules: {len(widget.sub_modules)}")

                # Try to force the widget to be visible
                print("  Attempting to force visibility...")
                widget.styles.height = "auto"
                widget.styles.min_height = 10
                widget.refresh()

if __name__ == "__main__":
    asyncio.run(test_layout_debug())
