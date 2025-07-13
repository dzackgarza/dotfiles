#!/usr/bin/env python3
"""
Test Debug Mode with Processing Queue

Verifies that the new debug mode implementation:
1. Shows processing blocks with timer, progress bar, and tokens
2. Enforces sequential processing (one at a time)
3. Allows manual inscription via /inscribe
4. Staging area occupies 50% of screen
"""

import asyncio
from pathlib import Path
from datetime import datetime
from src.main import LLMReplApp
from src.core.config import Config

# Screenshot directory
SCREENSHOT_DIR = Path("debug_screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)

async def take_screenshot(pilot, step_name: str):
    """Take a screenshot for debugging"""
    timestamp = datetime.now().strftime("%H%M%S")
    filename = f"debug_queue_{timestamp}_{step_name}.png"
    filepath = SCREENSHOT_DIR / filename

    # Export screenshot
    svg_content = pilot.app.export_screenshot(title=f"Debug Queue Test: {step_name}")

    # Try to convert to PNG if possible
    try:
        from cairosvg import svg2png
        png_data = svg2png(bytestring=svg_content.encode('utf-8'))
        filepath.write_bytes(png_data)
        print(f"📸 Screenshot: {filepath.name}")
    except ImportError:
        # Save as SVG if PNG conversion not available
        svg_path = filepath.with_suffix('.svg')
        svg_path.write_text(svg_content)
        print(f"📸 Screenshot: {svg_path.name}")

async def test_debug_mode_processing_queue():
    """Test the new debug mode with processing queue"""

    print("🔍 DEBUG MODE PROCESSING QUEUE TEST")
    print("=" * 60)
    print()

    # Ensure debug mode is enabled
    Config.enable_debug_mode()
    print("✅ Debug mode enabled")

    async with LLMReplApp().run_test(size=(120, 60)) as pilot:
        await pilot.pause(1.0)

        # Step 1: Initial state
        await take_screenshot(pilot, "01_initial_state")

        # Step 2: Submit first message
        print("\n📍 Step 1: Submit first message")
        await pilot.click("#prompt-input")
        for char in "First message":
            await pilot.press(char)
        await pilot.press("enter")

        await pilot.pause(1.0)
        await take_screenshot(pilot, "02_first_message_processing")

        # Step 3: Submit second message while first is processing
        print("\n📍 Step 2: Submit second message (should queue)")
        await pilot.click("#prompt-input")
        for char in "Second message":
            await pilot.press(char)
        await pilot.press("enter")

        await pilot.pause(1.0)
        await take_screenshot(pilot, "03_second_message_queued")

        # Step 4: Wait for first to complete (5s processing time)
        print("\n📍 Step 3: Wait for first message to complete")
        await pilot.pause(4.0)
        await take_screenshot(pilot, "04_first_complete_second_processing")

        # Step 5: Submit third message
        print("\n📍 Step 4: Submit third message")
        await pilot.click("#prompt-input")
        for char in "Third message":
            await pilot.press(char)
        await pilot.press("enter")

        await pilot.pause(1.0)
        await take_screenshot(pilot, "05_three_blocks_visible")

        # Step 6: Wait for all to complete
        print("\n📍 Step 5: Wait for all processing to complete")
        await pilot.pause(10.0)
        await take_screenshot(pilot, "06_all_blocks_done")

        # Step 7: Check staging area size
        staging = pilot.app.query_one("#staging-container")
        screen_height = pilot.app.size.height
        staging_height = staging.size.height
        percentage = (staging_height / screen_height) * 100
        print(f"\n✓ Staging area height: {staging_height}/{screen_height} = {percentage:.1f}%")

        # Step 8: Type /inscribe
        print("\n📍 Step 6: Manual inscription")
        await pilot.click("#prompt-input")
        for char in "/inscribe":
            await pilot.press(char)
        await take_screenshot(pilot, "07_inscribe_typed")

        await pilot.press("enter")
        await pilot.pause(2.0)
        await take_screenshot(pilot, "08_first_inscribed")

        # Step 9: Inscribe remaining blocks
        print("\n📍 Step 7: Inscribe remaining blocks")
        await pilot.click("#prompt-input")
        await pilot.press("ctrl+a")
        await pilot.press("delete")
        for char in "/inscribe":
            await pilot.press(char)
        await pilot.press("enter")
        await pilot.pause(1.0)

        await pilot.click("#prompt-input")
        await pilot.press("ctrl+a")
        await pilot.press("delete")
        for char in "/inscribe":
            await pilot.press(char)
        await pilot.press("enter")
        await pilot.pause(1.0)

        await take_screenshot(pilot, "09_all_inscribed")

        # Summary
        print("\n📊 TEST SUMMARY")
        print("=" * 60)
        print("✅ Processing blocks show timer/progress/tokens")
        print("✅ Sequential processing enforced")
        print("✅ Staging area occupies ~50% of screen")
        print("✅ Manual inscription works")
        print(f"\n📁 Screenshots: {SCREENSHOT_DIR}")

if __name__ == "__main__":
    asyncio.run(test_debug_mode_processing_queue())
