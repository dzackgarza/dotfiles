#!/usr/bin/env python3
"""Test to see all 3 sub-modules get processed"""

import asyncio
from src.main import LLMReplApp
from src.core.config import Config

async def test_all_submodules():
    Config.enable_debug_mode()
    Config.set_submodule_duration(1.0)  # 1 second each

    async with LLMReplApp().run_test(size=(72, 24)) as pilot:
        app = pilot.app
        await pilot.pause(0.5)

        print("\n=== Starting test ===")

        # Submit a message
        await pilot.click("#prompt-input")
        for char in "test":
            await pilot.press(char)
        await pilot.press("enter")

        # Check every 2 seconds to see all 3 sub-modules
        for i in range(5):  # Check for 10 seconds total
            await pilot.pause(2.0)

            staging = app.query_one("#staging-container")
            widgets = list(staging.children)

            print(f"\n=== After {(i+1)*2} seconds ===")
            print(f"Total widgets: {len(widgets)}")

            submodule_count = 0
            for j, widget in enumerate(widgets):
                wtype = type(widget).__name__
                if wtype == "SubModuleWidget":
                    submodule_count += 1
                    print(f"  SubModuleWidget {submodule_count}: {widget.sub_module.role}")
                    print(f"    State: {widget.sub_module.state}")
                else:
                    print(f"  {wtype}")

            print(f"SubModuleWidget count: {submodule_count}")

            # Break if we have all 3 sub-modules and they're done processing
            if submodule_count >= 3:
                print("Found all 3 sub-modules!")
                break

if __name__ == "__main__":
    asyncio.run(test_all_submodules())
