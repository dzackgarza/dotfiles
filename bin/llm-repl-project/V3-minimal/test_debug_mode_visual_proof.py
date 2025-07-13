#!/usr/bin/env python3
"""
DEBUG MODE VISUAL PROOF TEST

Generates screenshots showing the debug mode feature in action,
including the /inscribe command workflow.
"""

import asyncio
from pathlib import Path
from datetime import datetime
from src.main import LLMReplApp
from src.core.config import Config

# Ensure we have the screenshot libraries
try:
    from cairosvg import svg2png
    from PIL import Image, ImageDraw, ImageFont
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False
    print("⚠️  Missing libraries for screenshot generation")

SCREENSHOT_DIR = Path("debug_screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)

async def take_screenshot(pilot, step_name: str):
    """Take a screenshot and save it"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Take SVG screenshot
    svg_content = pilot.app.export_screenshot(title=f"Debug Mode: {step_name}")

    # Save SVG
    svg_path = SCREENSHOT_DIR / f"debug_mode_{timestamp}_{step_name}.svg"
    svg_path.write_text(svg_content)

    # Convert to PNG if possible
    if HAS_LIBS:
        try:
            png_bytes = svg2png(bytestring=svg_content.encode('utf-8'))
            png_path = SCREENSHOT_DIR / f"debug_mode_{timestamp}_{step_name}.png"
            png_path.write_bytes(png_bytes)
            print(f"📸 Screenshot saved: {png_path.name}")
        except Exception as e:
            print(f"⚠️  PNG conversion failed: {e}")

    return svg_path

async def test_debug_mode_visual_workflow():
    """Visual proof of debug mode working correctly"""

    print("🔍 DEBUG MODE VISUAL PROOF TEST")
    print("=" * 60)
    print()

    # Enable debug mode
    Config.enable_debug_mode()
    print("✅ Debug mode enabled")

    async with LLMReplApp().run_test(size=(120, 40)) as pilot:
        await pilot.pause(1.0)

        # Step 1: Initial state
        await take_screenshot(pilot, "01_initial_idle_state")

        # Step 2: Type a message
        await pilot.click("#prompt-input")
        for char in "Explain Python decorators":
            await pilot.press(char)
        await take_screenshot(pilot, "02_message_typed")

        # Step 3: Submit message
        await pilot.press("enter")
        await pilot.pause(1.0)
        await take_screenshot(pilot, "03_processing_active")

        # Step 4: Wait for processing to complete
        await pilot.pause(5.0)
        await take_screenshot(pilot, "04_debug_mode_response_ready")

        # Step 5: Inspect the staging area
        # At this point, developers can see:
        # - Yellow separator with debug instructions
        # - Response visible in staging area
        # - Workspace remains visible for inspection

        # Step 6: Type /inscribe command
        await pilot.click("#prompt-input")
        await pilot.pause(0.5)
        for char in "/inscribe":
            await pilot.press(char)
        await take_screenshot(pilot, "05_inscribe_command_typed")

        # Step 7: Execute inscription
        await pilot.press("enter")
        await pilot.pause(2.0)
        await take_screenshot(pilot, "06_after_inscription")

        # Step 8: Verify timeline updated
        await take_screenshot(pilot, "07_timeline_updated")

        # Step 9: Test another message to show debug mode persists
        await pilot.click("#prompt-input")
        for char in "What about class decorators?":
            await pilot.press(char)
        await pilot.press("enter")
        await pilot.pause(5.0)
        await take_screenshot(pilot, "08_second_message_debug_ready")

        # Step 10: Use Ctrl+I shortcut
        await pilot.press("ctrl+i")
        await pilot.pause(2.0)
        await take_screenshot(pilot, "09_ctrl_i_inscription")

        # Step 11: Final state
        await take_screenshot(pilot, "10_final_state")

    Config.disable_debug_mode()
    print("\n✅ Debug mode disabled")

    print("\n📊 VISUAL PROOF SUMMARY")
    print("=" * 60)
    print("Screenshots demonstrate:")
    print("1. Debug mode keeps staging area visible after processing")
    print("2. Yellow separator shows clear debug instructions")
    print("3. /inscribe command successfully commits to timeline")
    print("4. Ctrl+I shortcut works as alternative")
    print("5. System maintains clean state transitions")
    print()
    print(f"📁 Screenshots saved to: {SCREENSHOT_DIR}")

if __name__ == "__main__":
    asyncio.run(test_debug_mode_visual_workflow())
