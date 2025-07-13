#!/usr/bin/env python3
"""Capture sub-modules during active animation"""

import asyncio
from src.main import LLMReplApp
from src.core.config import Config

async def test_animation_capture():
    Config.enable_debug_mode()

    async with LLMReplApp().run_test(size=(72, 24)) as pilot:
        app = pilot.app
        await pilot.pause(0.5)

        print("=== CAPTURING ANIMATED SUB-MODULES ===")

        # Submit message to trigger cognition
        await pilot.click("#prompt-input")
        for char in "debug test with animation":
            await pilot.press(char)
        await pilot.press("enter")

        # Wait for cognition to start but not complete
        await pilot.pause(0.8)

        # Check staging area for active widgets
        staging = app.query_one("#staging-container")
        print(f"\nStaging area children: {len(staging.children)}")

        for i, widget in enumerate(staging.children):
            wtype = type(widget).__name__
            print(f"  {i}: {wtype}")

            if wtype == "CognitionWidget":
                print(f"    sub_modules: {len(widget.sub_modules)}")
                print(f"    is_live: {widget.is_live}")
                print(f"    elapsed_time: {widget.elapsed_time}")

                # Force refresh to ensure display is current
                widget.refresh()

                # Try to capture the actual render content
                try:
                    content = str(widget.render())
                    print(f"    content length: {len(content)}")
                    if "Route Query" in content or "Call Tool" in content:
                        print("    ✅ Contains sub-module content!")
                        break
                except Exception as e:
                    print(f"    render error: {e}")

        # Take screenshot during processing
        screenshot = app.export_screenshot(title="Active Sub-modules Animation")
        with open("debug_screenshots/active_submodules_animation.svg", "w") as f:
            f.write(screenshot)

        print("\nScreenshot saved: active_submodules_animation.svg")

if __name__ == "__main__":
    asyncio.run(test_animation_capture())
