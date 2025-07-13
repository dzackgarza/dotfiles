#!/usr/bin/env python3
"""
Visual test to create PNG screenshot of manual inscription working
"""

import asyncio
from pathlib import Path
from src.main import LLMReplApp
from src.core.config import Config

async def test_manual_inscription_visual():
    """Test manual inscription and create PNG screenshot"""
    print("🔍 VISUAL TEST: Manual Inscription with PNG Screenshot")

    # Ensure manual inscription mode is enabled
    Config.MANUAL_INSCRIBE_MODE = True
    print(f"📋 Manual inscription mode: {Config.MANUAL_INSCRIBE_MODE}")

    async with LLMReplApp().run_test(size=(120, 40)) as pilot:
        await pilot.pause(1.0)

        # Submit a message
        print("📝 Submitting message...")
        await pilot.click("#prompt-input")
        for char in "test manual inscription":
            await pilot.press(char)
        await pilot.press("enter")

        # Wait for processing to complete
        print("⏳ Waiting for processing...")
        await pilot.pause(8.0)

        # Take screenshot BEFORE inscription (should show no conversation)
        screenshot_before = pilot.app.export_screenshot(title="Before Manual Inscription")

        # Manual inscription with /inscribe command
        print("📝 Triggering manual inscription...")
        await pilot.click("#prompt-input")
        await pilot.pause(0.2)
        await pilot.press("ctrl+a")
        await pilot.pause(0.1)
        await pilot.press("delete")
        await pilot.pause(0.2)
        for char in "/inscribe":
            await pilot.press(char)
            await pilot.pause(0.05)
        await pilot.pause(0.2)
        await pilot.press("enter")
        await pilot.pause(2.0)

        # Take screenshot AFTER inscription (should show conversation)
        screenshot_after = pilot.app.export_screenshot(title="After Manual Inscription - SUCCESS")

        # Save screenshots as PNG (with SVG fallback)
        try:
            import cairosvg

            # Save before screenshot as PNG
            png_data_before = cairosvg.svg2png(bytestring=screenshot_before.encode('utf-8'))
            Path("before_inscription.png").write_bytes(png_data_before)
            print("📸 Screenshot saved: before_inscription.png")

            # Save after screenshot as PNG
            png_data_after = cairosvg.svg2png(bytestring=screenshot_after.encode('utf-8'))
            Path("after_inscription.png").write_bytes(png_data_after)
            print("📸 Screenshot saved: after_inscription.png")

        except Exception as e:
            print(f"⚠️  PNG conversion failed: {e}")
            # Fallback to SVG
            Path("before_inscription.svg").write_text(screenshot_before)
            Path("after_inscription.svg").write_text(screenshot_after)
            print("📸 Screenshots saved as SVG (PNG conversion failed)")

        print("✅ Manual inscription visual test complete!")

if __name__ == "__main__":
    asyncio.run(test_manual_inscription_visual())
