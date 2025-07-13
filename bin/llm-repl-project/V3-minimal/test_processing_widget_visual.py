#!/usr/bin/env python3
"""
Test ProcessingWidget Visual Display

Captures screenshots of the ProcessingWidget during active processing
to verify timer and progress bar are visible.
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
    """Take a screenshot for evidence"""
    timestamp = datetime.now().strftime("%H%M%S")

    # Export screenshot
    svg_content = pilot.app.export_screenshot(title=f"ProcessingWidget Test: {step_name}")

    # Save it
    svg_path = SCREENSHOT_DIR / f"processing_widget_{timestamp}_{step_name}.svg"
    svg_path.write_text(svg_content)

    # Try PNG conversion
    try:
        from cairosvg import svg2png
        png_data = svg2png(bytestring=svg_content.encode('utf-8'))
        png_path = svg_path.with_suffix('.png')
        png_path.write_bytes(png_data)
        print(f"📸 Screenshot: {png_path.name}")
        return png_path
    except:
        print(f"📸 Screenshot: {svg_path.name}")
        return svg_path

async def test_processing_widget_visual():
    """Test ProcessingWidget visual display"""

    print("🔍 PROCESSING WIDGET VISUAL TEST")
    print("=" * 60)

    # Verify debug mode is on
    print(f"Debug mode enabled: {Config.DEBUG_MODE}")
    if not Config.DEBUG_MODE:
        print("❌ Debug mode must be enabled for this test!")
        return

    async with LLMReplApp().run_test(size=(120, 50)) as pilot:
        await pilot.pause(1.0)

        # Take initial screenshot
        await take_screenshot(pilot, "01_initial")

        # Type and submit a message
        print("\n📝 Submitting test message...")
        await pilot.click("#prompt-input")
        test_msg = "Show processing widget"
        for char in test_msg:
            await pilot.press(char)
        await pilot.press("enter")

        # Immediately take screenshots during processing
        print("\n⏱️ Capturing ProcessingWidget states...")

        # Capture at 0.5s - should show timer ~0.5s
        await pilot.pause(0.5)
        await take_screenshot(pilot, "02_processing_0.5s")

        # Capture at 1.5s - should show timer ~1.5s
        await pilot.pause(1.0)
        await take_screenshot(pilot, "03_processing_1.5s")

        # Capture at 3s - should show timer ~3s
        await pilot.pause(1.5)
        await take_screenshot(pilot, "04_processing_3s")

        # Capture at 5s - should be near completion
        await pilot.pause(2.0)
        await take_screenshot(pilot, "05_processing_5s")

        # Final capture after processing complete
        await pilot.pause(1.0)
        await take_screenshot(pilot, "06_complete")

        # Check what's in staging
        workspace = pilot.app.query_one("#staging-container")
        print(f"\n📋 Staging area contents ({len(list(workspace.children))} items):")
        for i, child in enumerate(list(workspace.children)):
            print(f"  {i}: {type(child).__name__}")
            if hasattr(child, 'render'):
                try:
                    rendered = child.render()
                    if rendered and hasattr(rendered, 'plain'):
                        preview = rendered.plain[:100] if hasattr(rendered, 'plain') else str(rendered)[:100]
                        print(f"     Content preview: {preview}")
                except:
                    pass

        print(f"\n✅ Test complete! Check screenshots in {SCREENSHOT_DIR}")

if __name__ == "__main__":
    asyncio.run(test_processing_widget_visual())
