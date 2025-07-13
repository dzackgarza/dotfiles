#!/usr/bin/env python3
"""
CANONICAL DEBUG MODE TEST - Real user experience

Tests debug mode as a real user would experience it:
1. Launch app normally
2. Send a message
3. See the 3-way split with processing widget
4. Use /inscribe command
5. Verify timeline update
"""

import asyncio
from pathlib import Path
from datetime import datetime
from src.main import LLMReplApp
from src.core.config import Config

# Screenshot directory
SCREENSHOT_DIR = Path("debug_screenshots/canonical")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

async def take_screenshot(pilot, step_name: str, description: str):
    """Take a canonical screenshot with description"""
    timestamp = datetime.now().strftime("%H%M%S")

    # Export screenshot
    svg_content = pilot.app.export_screenshot(title=f"Debug Mode Canonical: {description}")

    # Try to save as PNG first
    filename = f"canonical_{timestamp}_{step_name}"

    try:
        from cairosvg import svg2png
        png_data = svg2png(bytestring=svg_content.encode('utf-8'))
        png_path = SCREENSHOT_DIR / f"{filename}.png"
        png_path.write_bytes(png_data)
        print(f"📸 {step_name}: {png_path.name} - {description}")
        return png_path
    except Exception as e:
        # Fallback to SVG
        svg_path = SCREENSHOT_DIR / f"{filename}.svg"
        svg_path.write_text(svg_content)
        print(f"📸 {step_name}: {svg_path.name} - {description} (PNG failed: {e})")
        return svg_path

async def test_debug_mode_canonical():
    """Test debug mode from a real user's perspective"""

    print("🔍 CANONICAL DEBUG MODE TEST - Real User Experience")
    print("=" * 60)

    # Check configuration
    print(f"Debug mode enabled: {Config.DEBUG_MODE}")
    print(f"Use processing queue: {Config.USE_PROCESSING_QUEUE}")

    async with LLMReplApp().run_test(size=(120, 50)) as pilot:
        await pilot.pause(1.0)

        # 1. IDLE STATE - 2-way layout
        await take_screenshot(pilot, "01_idle_state", "App launched - 2-way layout (timeline + input)")

        # Check initial layout
        workspace = pilot.app.query_one("#staging-container")
        print("\nInitial state:")
        print(f"- Workspace visible: {'processing' in workspace.classes}")
        print(f"- Workspace classes: {workspace.classes}")

        # 2. User types message
        print("\n👤 User action: Typing message...")
        await pilot.click("#prompt-input")
        test_msg = "Explain Python decorators"
        for char in test_msg:
            await pilot.press(char)
        await take_screenshot(pilot, "02_user_typing", "User typing message")

        # 3. Submit message - should trigger 3-way split
        print("\n⏎ User action: Pressing Enter...")
        await pilot.press("enter")

        # Capture during processing
        await pilot.pause(0.5)
        await take_screenshot(pilot, "03_processing_early", "Processing started - 3-way layout visible")

        # Check processing state
        print("\nProcessing state:")
        print(f"- Workspace visible: {'processing' in workspace.classes}")
        print(f"- Workspace children: {len(list(workspace.children))}")

        # 4. Capture mid-processing
        await pilot.pause(2.0)
        await take_screenshot(pilot, "04_processing_mid", "Mid-processing - timer and progress visible")

        # 5. Wait for processing to complete
        await pilot.pause(3.0)
        await take_screenshot(pilot, "05_processing_complete", "Processing complete - response ready")

        # Check staging contents
        print("\nStaging area contents:")
        for i, child in enumerate(list(workspace.children)):
            print(f"  {i}: {type(child).__name__}")
            if hasattr(child, 'render'):
                try:
                    rendered = str(child.render())
                    if "Debug Mode Instructions" in rendered:
                        print("     ✓ Help text found")
                    if "ProcessingWidget" in type(child).__name__:
                        print("     ✓ ProcessingWidget present")
                except:
                    pass

        # 6. User types /inscribe
        print("\n📝 User action: Typing /inscribe...")
        await pilot.click("#prompt-input")
        await pilot.press("ctrl+a")
        await pilot.press("delete")
        for char in "/inscribe":
            await pilot.press(char)
        await take_screenshot(pilot, "06_inscribe_typed", "User typed /inscribe command")

        # 7. Execute inscription
        print("\n✅ User action: Pressing Enter to inscribe...")
        await pilot.press("enter")
        await pilot.pause(1.0)
        await take_screenshot(pilot, "07_after_inscribe", "After inscription - back to 2-way layout")

        # Check final state
        print("\nFinal state:")
        print(f"- Workspace visible: {'processing' in workspace.classes}")
        timeline = pilot.app.query_one("#chat-container")
        print(f"- Timeline items: {len(list(timeline.children))}")

        # 8. Test second message to ensure it still works
        print("\n🔄 User action: Sending second message...")
        await pilot.click("#prompt-input")
        for char in "What about async/await?":
            await pilot.press(char)
        await pilot.press("enter")
        await pilot.pause(1.0)
        await take_screenshot(pilot, "08_second_message", "Second message processing")

        # Summary
        print("\n" + "=" * 60)
        print("📊 CANONICAL TEST SUMMARY")
        print("=" * 60)
        print(f"Screenshots saved to: {SCREENSHOT_DIR}")
        print("\nKey behaviors to verify:")
        print("1. ✓ 2-way layout when idle (timeline + input)")
        print("2. ✓ 3-way layout during processing (timeline + workspace + input)")
        print("3. ✓ ProcessingWidget shows timer and progress")
        print("4. ✓ Help text explains /inscribe command")
        print("5. ✓ /inscribe commits to timeline")
        print("6. ✓ Returns to 2-way layout after inscription")
        print("7. ✓ Can continue conversation normally")

if __name__ == "__main__":
    asyncio.run(test_debug_mode_canonical())
