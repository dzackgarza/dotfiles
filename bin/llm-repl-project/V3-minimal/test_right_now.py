#!/usr/bin/env python3
"""
RIGHT NOW TEST - What actually happens when I run the app?
"""

import asyncio
from pathlib import Path
from datetime import datetime
from src.main import LLMReplApp

try:
    from cairosvg import svg2png
    HAS_CAIROSVG = True
except ImportError:
    HAS_CAIROSVG = False

# Clear old screenshots and create fresh directory
FRESH_DIR = Path("debug_screenshots/right_now")
if FRESH_DIR.exists():
    import shutil
    shutil.rmtree(FRESH_DIR)
FRESH_DIR.mkdir(parents=True, exist_ok=True)

async def take_fresh_screenshot(pilot, filename: str, title: str):
    """Take a completely fresh screenshot right now"""
    svg_content = pilot.app.export_screenshot(title=f"RIGHT NOW: {title}")

    timestamp = datetime.now().strftime("%H%M%S")
    base_name = f"right_now_{timestamp}_{filename}"

    if HAS_CAIROSVG:
        try:
            png_data = svg2png(bytestring=svg_content.encode('utf-8'))
            png_path = FRESH_DIR / f"{base_name}.png"
            png_path.write_bytes(png_data)
            print(f"🔥 FRESH: {png_path.name}")
        except Exception:
            svg_path = FRESH_DIR / f"{base_name}.svg"
            svg_path.write_text(svg_content)
            print(f"🔥 FRESH: {svg_path.name} (PNG failed)")
    else:
        svg_path = FRESH_DIR / f"{base_name}.svg"
        svg_path.write_text(svg_content)
        print(f"🔥 FRESH: {svg_path.name}")

async def test_right_now():
    """Test what actually happens RIGHT NOW"""
    print("🔥 RIGHT NOW TEST - FRESH EVIDENCE")
    print("=" * 50)

    try:
        async with LLMReplApp().run_test(size=(120, 40)) as pilot:
            # STEP 1: Launch state
            print("🔥 STEP 1: App launches")
            await pilot.pause(1.0)
            await take_fresh_screenshot(pilot, "01_launch", "App just launched")

            # STEP 2: Type message
            print("🔥 STEP 2: Type simple message")
            await pilot.click("#prompt-input")
            await pilot.pause(0.5)

            for char in "Hello":
                await pilot.press(char)
                await pilot.pause(0.05)

            await take_fresh_screenshot(pilot, "02_typed", "Message typed")

            # STEP 3: Submit and immediately capture
            print("🔥 STEP 3: Submit message")
            await pilot.press("enter")
            await pilot.pause(0.5)  # Just enough to see transition
            await take_fresh_screenshot(pilot, "03_submitted", "Just submitted")

            # STEP 4: Wait a bit and capture processing
            print("🔥 STEP 4: Check processing state")
            await pilot.pause(3.0)
            await take_fresh_screenshot(pilot, "04_processing", "During processing")

            # STEP 5: Wait for completion
            print("🔥 STEP 5: Wait for completion")
            await pilot.pause(5.0)
            await take_fresh_screenshot(pilot, "05_complete", "After processing")

            # STEP 6: Try /inscribe
            print("🔥 STEP 6: Try /inscribe command")
            await pilot.click("#prompt-input")
            await pilot.pause(0.5)

            # Clear and type /inscribe
            await pilot.press("ctrl+a")
            await pilot.pause(0.1)
            await pilot.press("delete")
            await pilot.pause(0.2)

            for char in "/inscribe":
                await pilot.press(char)
                await pilot.pause(0.05)

            await take_fresh_screenshot(pilot, "06_inscribe_typed", "Typed /inscribe")

            await pilot.press("enter")
            await pilot.pause(2.0)

            await take_fresh_screenshot(pilot, "07_final", "Final state")

            print()
            print("🔥 FRESH SCREENSHOTS COMPLETE")
            print(f"📁 Location: {FRESH_DIR}")
            print()
            print("🔍 ANALYSIS:")
            print("1. Does IDLE state work? Check 01_launch.png")
            print("2. Does PROCESSING state work? Check 04_processing.png")
            print("3. Do processing steps show? Check 04_processing.png")
            print("4. Does /inscribe work? Check 07_final.png")
            print("5. Are there errors? Check all screenshots")

    except Exception as e:
        print(f"💥 CRASHED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_right_now())
