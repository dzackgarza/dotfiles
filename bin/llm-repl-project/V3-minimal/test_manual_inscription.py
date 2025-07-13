#!/usr/bin/env python3
"""
Test manual inscription feature specifically
"""

import asyncio
from pathlib import Path
from src.main import LLMReplApp
from src.core.config import Config

async def test_manual_inscription():
    """Test that manual inscription feature works as requested"""
    print("🔍 TESTING MANUAL INSCRIPTION FEATURE")

    # Ensure manual inscription mode is enabled
    Config.MANUAL_INSCRIBE_MODE = True
    print(f"📋 Manual inscription mode: {Config.MANUAL_INSCRIBE_MODE}")

    async with LLMReplApp().run_test(size=(72, 48)) as pilot:
        await pilot.pause(1.0)

        # Step 1: Submit a message
        print("\n📝 Step 1: Submitting message")
        await pilot.click("#prompt-input")
        for char in "test manual inscription":
            await pilot.press(char)
        await pilot.press("enter")

        # Step 2: Wait for processing to complete
        print("\n⏳ Step 2: Waiting for processing to complete...")
        await pilot.pause(8.0)  # Wait for processing

        # Step 3: Check timeline - should NOT have conversation yet
        print("\n🔍 Step 3: Checking timeline before inscription")
        chat_container = pilot.app.query_one("#chat-container")
        children_before = list(chat_container.children)
        print(f"📊 Timeline has {len(children_before)} children before inscription")

        # Should only have system message, no conversation
        user_blocks_before = [c for c in children_before if hasattr(c, 'classes') and 'human-message' in c.classes]
        print(f"📊 User blocks before inscription: {len(user_blocks_before)}")

        # Step 4: Manual inscription with /inscribe command
        print("\n📝 Step 4: Triggering manual inscription with /inscribe")
        await pilot.click("#prompt-input")
        await pilot.pause(0.2)
        await pilot.press("ctrl+a")  # Clear
        await pilot.pause(0.1)
        await pilot.press("delete")
        await pilot.pause(0.2)
        print("DEBUG: Typing /inscribe command")
        for char in "/inscribe":
            await pilot.press(char)
            await pilot.pause(0.05)
        await pilot.pause(0.2)
        print("DEBUG: Pressing enter to submit /inscribe")
        await pilot.press("enter")
        await pilot.pause(2.0)  # Wait for inscription

        # Step 5: Check timeline after inscription
        print("\n🔍 Step 5: Checking timeline after inscription")
        children_after = list(chat_container.children)
        print(f"📊 Timeline has {len(children_after)} children after inscription")

        user_blocks_after = [c for c in children_after if hasattr(c, 'classes') and 'human-message' in c.classes]
        print(f"📊 User blocks after inscription: {len(user_blocks_after)}")

        # Verify inscription worked
        if len(user_blocks_after) > len(user_blocks_before):
            print("✅ Manual inscription SUCCESS - conversation added to timeline")
        else:
            print("❌ Manual inscription FAILED - no conversation added")

        # Take screenshot of final state
        screenshot = pilot.app.export_screenshot(title="Manual Inscription Test")

        # Try to save as PNG first
        try:
            from cairosvg import svg2png
            png_data = svg2png(bytestring=screenshot.encode('utf-8'))
            Path("manual_inscription_test.png").write_bytes(png_data)
            print("📸 Screenshot saved: manual_inscription_test.png")
        except Exception:
            # Fallback to SVG
            Path("manual_inscription_test.svg").write_text(screenshot)
            print("📸 Screenshot saved: manual_inscription_test.svg (PNG conversion failed)")

if __name__ == "__main__":
    asyncio.run(test_manual_inscription())
