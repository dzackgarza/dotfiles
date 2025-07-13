#!/usr/bin/env python3
"""Test the enhanced CognitionWidget with sub-modules"""

import asyncio
from src.main import LLMReplApp
from src.core.config import Config

async def test_enhanced_cognition():
    Config.enable_debug_mode()

    async with LLMReplApp().run_test(size=(72, 24)) as pilot:
        app = pilot.app
        await pilot.pause(0.5)

        print("\n=== Testing Enhanced CognitionWidget ===")

        # Submit a message
        await pilot.click("#prompt-input")
        for char in "test cognition":
            await pilot.press(char)
        await pilot.press("enter")

        # Wait for cognition to complete
        await pilot.pause(2.0)

        # Take a screenshot
        screenshot = app.export_screenshot(title="Enhanced Cognition Debug")
        with open("enhanced_cognition_debug.svg", "w") as f:
            f.write(screenshot)

        print("Screenshot saved: enhanced_cognition_debug.svg")

        # Check the staging area contents
        staging = app.query_one("#staging-container")
        widgets = list(staging.children)

        print("\nStaging area contents:")
        for i, widget in enumerate(widgets):
            wtype = type(widget).__name__
            print(f"  Widget {i}: {wtype}")

            if wtype == "CognitionWidget":
                print(f"    Sub-modules: {len(widget.sub_modules)}")
                for j, sub_module in enumerate(widget.sub_modules):
                    print(f"      {j+1}. {sub_module['icon']} {sub_module['name']} - {sub_module['state']}")

if __name__ == "__main__":
    asyncio.run(test_enhanced_cognition())
