#!/usr/bin/env python3
"""
REAL USER EXPERIENCE TEST

This test simulates exactly what a real user would do:
1. Launch the app
2. Type a simple question
3. Hit enter
4. See what actually happens

No test frameworks, no mocking - just the real app.
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

# Create canonical screenshots directory
CANONICAL_DIR = Path("debug_screenshots/canonical")
CANONICAL_DIR.mkdir(parents=True, exist_ok=True)

async def save_canonical_screenshot(pilot, filename: str, title: str):
    """Save a canonical screenshot showing real user experience"""
    svg_content = pilot.app.export_screenshot(title=f"CANONICAL: {title}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"canonical_{timestamp}_{filename}"

    if HAS_CAIROSVG:
        try:
            png_data = svg2png(bytestring=svg_content.encode('utf-8'))
            png_path = CANONICAL_DIR / f"{base_name}.png"
            png_path.write_bytes(png_data)
            print(f"📸 CANONICAL: {png_path.name}")
        except Exception as e:
            print(f"❌ PNG failed: {e}")
            svg_path = CANONICAL_DIR / f"{base_name}.svg"
            svg_path.write_text(svg_content)
            print(f"📸 CANONICAL: {svg_path.name} (SVG fallback)")
    else:
        svg_path = CANONICAL_DIR / f"{base_name}.svg"
        svg_path.write_text(svg_content)
        print(f"📸 CANONICAL: {svg_path.name}")

async def test_real_user_workflow():
    """Test exactly what a real user would experience"""
    print("🎬 REAL USER EXPERIENCE TEST")
    print("=" * 50)
    print("Testing: Can a real user successfully use this app?")
    print()

    try:
        async with LLMReplApp().run_test(size=(120, 40)) as pilot:
            # STEP 1: App launches - what does user see?
            print("👤 USER ACTION: Launch app")
            await pilot.pause(1.0)
            await save_canonical_screenshot(pilot, "01_app_launch", "User launches app")
            print("✓ App launched")
            print()

            # STEP 2: User sees IDLE state - is it correct?
            print("👁️  USER SEES: Initial state")
            print("   Expected: Sacred Timeline (top) + Input (bottom)")
            await save_canonical_screenshot(pilot, "02_idle_state", "IDLE State - 2-way layout")
            print()

            # STEP 3: User types a simple question
            print("👤 USER ACTION: Type 'What is 2+2?'")
            await pilot.click("#prompt-input")
            await pilot.pause(0.5)

            simple_question = "What is 2+2?"
            for char in simple_question:
                await pilot.press(char)
                await pilot.pause(0.05)

            await save_canonical_screenshot(pilot, "03_message_typed", "User typed message")
            print("✓ Message typed")
            print()

            # STEP 4: User hits enter - what happens?
            print("👤 USER ACTION: Hit Enter to submit")
            print("   Expected: Switch to PROCESSING state with 3-way layout")

            await pilot.press("enter")
            await pilot.pause(0.5)  # Let the transition happen

            await save_canonical_screenshot(pilot, "04_submit_immediate", "Immediately after submit")
            print()

            # STEP 5: Check processing state
            print("👁️  USER SEES: Processing state (should be 3-way layout)")
            await pilot.pause(2.0)  # Let processing start
            await save_canonical_screenshot(pilot, "05_processing_active", "PROCESSING State - should show Live Workspace")
            print()

            # STEP 6: Wait for processing to complete
            print("⏳ WAITING: Let processing complete")
            await pilot.pause(8.0)  # Wait for full processing
            await save_canonical_screenshot(pilot, "06_processing_complete", "After processing completes")
            print()

            # STEP 7: Check if inscription is needed (debug mode)
            print("🔍 CHECKING: Is manual inscription required?")
            await save_canonical_screenshot(pilot, "07_inscription_check", "Check if inscription needed")

            # Try /inscribe command
            print("👤 USER ACTION: Try /inscribe command")
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

            await save_canonical_screenshot(pilot, "08_inscribe_typed", "User typed /inscribe")

            await pilot.press("enter")
            await pilot.pause(2.0)

            await save_canonical_screenshot(pilot, "09_after_inscribe", "After /inscribe command")
            print()

            # STEP 8: Final state - back to IDLE?
            print("👁️  USER SEES: Final state")
            print("   Expected: Back to IDLE with conversation in timeline")
            await save_canonical_screenshot(pilot, "10_final_state", "Final state - conversation should be visible")

            print()
            print("=" * 50)
            print("✅ REAL USER WORKFLOW TEST COMPLETE")
            print(f"📁 Canonical screenshots saved to: {CANONICAL_DIR}")
            print()
            print("🔍 ANALYSIS NEEDED:")
            print("1. Does IDLE state show correct 2-way layout?")
            print("2. Does PROCESSING state show correct 3-way layout?")
            print("3. Does Live Workspace show processing steps?")
            print("4. Does /inscribe work correctly?")
            print("5. Does conversation appear in timeline?")
            print("6. Are there any errors or crashes?")

    except Exception as e:
        print(f"💥 CRITICAL ERROR: {e}")
        print("❌ App failed - real user would be blocked!")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_real_user_workflow())
