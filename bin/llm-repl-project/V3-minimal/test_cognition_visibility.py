#!/usr/bin/env python3
"""Test if the enhanced CognitionWidget is actually visible in processing state"""

import asyncio
from src.main import LLMReplApp
from src.core.config import Config

async def test_cognition_visibility():
    Config.enable_debug_mode()

    async with LLMReplApp().run_test(size=(72, 24)) as pilot:
        app = pilot.app
        await pilot.pause(0.5)

        print("=== BEFORE PROCESSING ===")
        staging = app.query_one("#staging-container")
        print(f"Staging visible: {'hidden' not in staging.classes}")
        print(f"Staging widgets: {[type(w).__name__ for w in staging.children]}")

        # Submit message
        await pilot.click("#prompt-input")
        for char in "test":
            await pilot.press(char)
        await pilot.press("enter")

        # Brief pause to let processing start
        await pilot.pause(0.5)

        print("\n=== DURING PROCESSING ===")
        staging = app.query_one("#staging-container")
        print(f"Staging visible: {'hidden' not in staging.classes}")
        print(f"Staging classes: {staging.classes}")
        print(f"Staging widgets: {[type(w).__name__ for w in staging.children]}")

        # Check each widget in detail
        for i, widget in enumerate(staging.children):
            wtype = type(widget).__name__
            print(f"\nWidget {i}: {wtype}")

            if wtype == "CognitionWidget":
                print("  CognitionWidget details:")
                print(f"    is_live: {widget.is_live}")
                print(f"    content: {widget.content[:50]}...")
                print(f"    sub_modules count: {len(widget.sub_modules)}")
                for j, sub_mod in enumerate(widget.sub_modules):
                    print(f"      {j+1}. {sub_mod['icon']} {sub_mod['name']} - {sub_mod['state']}")

                # Check if widget is visible
                print(f"    widget classes: {widget.classes}")
                print(f"    widget styles: {widget.styles}")

            elif hasattr(widget, 'renderable'):
                content = str(widget.renderable)[:100]
                print(f"    content: {content}")

        # Wait for processing to complete
        await pilot.pause(2.0)

        print("\n=== AFTER PROCESSING ===")
        staging = app.query_one("#staging-container")
        print(f"Staging visible: {'hidden' not in staging.classes}")
        print(f"Staging widgets: {[type(w).__name__ for w in staging.children]}")

if __name__ == "__main__":
    asyncio.run(test_cognition_visibility())
