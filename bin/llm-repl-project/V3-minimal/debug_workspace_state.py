#!/usr/bin/env python3
"""
Debug workspace state during manual inscription to understand
exactly how the Live Workspace behaves in manual inscription mode.
"""

import asyncio
from pathlib import Path
from src.main import LLMReplApp
from src.core.config import Config

async def debug_workspace_state():
    """Debug workspace state transitions in manual inscription mode"""
    print("🔍 DEBUGGING WORKSPACE STATE IN MANUAL INSCRIPTION MODE")
    print("=" * 60)

    Config.MANUAL_INSCRIBE_MODE = True

    async with LLMReplApp().run_test(size=(120, 40)) as pilot:
        await pilot.pause(1.0)

        staging_container = pilot.app.query_one("#staging-container")

        # Initial state
        print("🔸 INITIAL STATE:")
        print(f"   Classes: {staging_container.classes}")
        print(f"   Processing class present: {'processing' in staging_container.classes}")

        # Submit message
        await pilot.click("#prompt-input")
        for char in "debug workspace state":
            await pilot.press(char)
        await pilot.press("enter")

        # Check during processing start
        await pilot.pause(0.5)
        print("\n🔸 DURING PROCESSING START:")
        print(f"   Classes: {staging_container.classes}")
        print(f"   Processing class present: {'processing' in staging_container.classes}")

        # Check during processing
        await pilot.pause(3.0)
        print("\n🔸 DURING PROCESSING:")
        print(f"   Classes: {staging_container.classes}")
        print(f"   Processing class present: {'processing' in staging_container.classes}")

        # Check after processing complete (manual inscription pending)
        await pilot.pause(6.0)
        print("\n🔸 AFTER PROCESSING (MANUAL INSCRIPTION PENDING):")
        print(f"   Classes: {staging_container.classes}")
        print(f"   Processing class present: {'processing' in staging_container.classes}")
        print(f"   Children count: {len(list(staging_container.children))}")

        # Check if processor has pending inscription
        processor = pilot.app.unified_async_processor
        has_pending = processor._pending_inscription is not None
        print(f"   Has pending inscription: {has_pending}")

        # Take screenshot
        screenshot = pilot.app.export_screenshot(title="Workspace State Debug")
        Path("workspace_debug.svg").write_text(screenshot)
        print("   Screenshot saved: workspace_debug.svg")

        # Now trigger inscription
        print("\n🔸 TRIGGERING MANUAL INSCRIPTION:")
        await pilot.click("#prompt-input")
        await pilot.pause(0.2)
        await pilot.press("ctrl+a")
        await pilot.press("delete")
        for char in "/inscribe":
            await pilot.press(char)
        await pilot.press("enter")
        await pilot.pause(2.0)

        print("\n🔸 AFTER MANUAL INSCRIPTION:")
        print(f"   Classes: {staging_container.classes}")
        print(f"   Processing class present: {'processing' in staging_container.classes}")
        print(f"   Children count: {len(list(staging_container.children))}")

        has_pending_after = processor._pending_inscription is not None
        print(f"   Has pending inscription: {has_pending_after}")

if __name__ == "__main__":
    asyncio.run(debug_workspace_state())
