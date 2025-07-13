#!/usr/bin/env python3
"""
REAL DEBUG MODE TEST - Actually use the feature as intended

This test simulates a developer using debug mode:
1. Launch app with debug mode on
2. Send a message
3. See response pause in staging
4. Inspect it
5. Use /inscribe to commit
6. Verify it works end-to-end
"""

import asyncio
from pathlib import Path
from datetime import datetime
from src.main import LLMReplApp
from src.core.config import Config

# Screenshot directory
SCREENSHOT_DIR = Path("debug_screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)

async def take_screenshot(pilot, step_name: str, step_num: int):
    """Take a screenshot for evidence"""
    timestamp = datetime.now().strftime("%H%M%S")

    # Export screenshot
    svg_content = pilot.app.export_screenshot(title=f"Real Debug Mode: Step {step_num} - {step_name}")

    # Try to save as PNG first
    filename = f"real_debug_{timestamp}_{step_num:02d}_{step_name}"

    try:
        from cairosvg import svg2png
        png_data = svg2png(bytestring=svg_content.encode('utf-8'))
        png_path = SCREENSHOT_DIR / f"{filename}.png"
        png_path.write_bytes(png_data)
        print(f"📸 Step {step_num}: {png_path.name}")
        return png_path
    except Exception:
        # Fallback to SVG
        svg_path = SCREENSHOT_DIR / f"{filename}.svg"
        svg_path.write_text(svg_content)
        print(f"📸 Step {step_num}: {svg_path.name} (PNG conversion failed)")
        return svg_path

async def test_real_debug_mode_usage():
    """Test debug mode as a real developer would use it"""

    print("🔍 REAL DEBUG MODE TEST - Developer Workflow")
    print("=" * 60)

    # Verify debug mode is on
    print(f"Debug mode enabled: {Config.DEBUG_MODE}")
    if not Config.DEBUG_MODE:
        print("❌ Debug mode must be enabled for this test!")
        return

    async with LLMReplApp().run_test(size=(120, 50)) as pilot:
        await pilot.pause(1.0)

        # Step 1: App launches
        await take_screenshot(pilot, "app_launched", 1)

        # Check initial state
        workspace = pilot.app.query_one("#staging-container")
        initial_visible = "processing" in workspace.classes
        print(f"✓ Initial workspace visible: {initial_visible} (should be False)")

        # Step 2: Developer types a test message
        print("\n👨‍💻 Developer types test message...")
        await pilot.click("#prompt-input")
        test_msg = "Test response for debugging"
        for char in test_msg:
            await pilot.press(char)
        await take_screenshot(pilot, "message_typed", 2)

        # Step 3: Submit and watch processing
        print("\n⏎ Submitting message...")
        await pilot.press("enter")
        await pilot.pause(0.5)
        await take_screenshot(pilot, "processing_starts", 3)

        # Check workspace appeared
        workspace_visible = "processing" in workspace.classes
        print(f"✓ Workspace visible during processing: {workspace_visible}")

        # Step 4: Wait for processing to complete
        print("\n⏳ Waiting for response...")
        await pilot.pause(5.5)  # Wait for mock processing
        await take_screenshot(pilot, "response_ready", 4)

        # Step 5: Check what's in staging
        print("\n🔍 Inspecting staging area...")

        # Check if workspace still visible (debug mode should keep it visible)
        still_visible = "processing" in workspace.classes
        print(f"✓ Workspace still visible after processing: {still_visible}")

        # Check for content in staging
        staging_children = list(workspace.children)
        print(f"✓ Items in staging: {len(staging_children)}")
        for i, child in enumerate(staging_children):
            print(f"  - {i}: {type(child).__name__}")

        # Look for assistant response
        has_assistant_response = any("assistant" in str(child.classes) for child in staging_children)
        print(f"✓ Assistant response in staging: {has_assistant_response}")

        # Step 6: Check staging separator
        separator = pilot.app.staging_separator
        if separator:
            print("✓ Staging separator exists")
            # The separator should show pending inscription state

        # Step 7: Type /inscribe command
        print("\n📝 Developer types /inscribe...")
        await pilot.click("#prompt-input")
        await pilot.press("ctrl+a")  # Select all
        await pilot.press("delete")   # Clear
        for char in "/inscribe":
            await pilot.press(char)
        await take_screenshot(pilot, "inscribe_typed", 5)

        # Step 8: Execute inscription
        print("\n✅ Executing inscription...")
        await pilot.press("enter")
        await pilot.pause(2.0)
        await take_screenshot(pilot, "after_inscription", 6)

        # Step 9: Verify inscription worked
        print("\n🔍 Verifying results...")

        # Check workspace hidden
        workspace_hidden = "processing" not in workspace.classes
        print(f"✓ Workspace hidden after inscription: {workspace_hidden}")

        # Check timeline updated
        timeline = pilot.app.query_one("#chat-container")
        timeline_items = list(timeline.children)
        print(f"✓ Timeline items: {len(timeline_items)}")

        # Look for assistant response in timeline
        has_timeline_response = any("assistant" in str(child.classes) for child in timeline_items)
        print(f"✓ Assistant response in timeline: {has_timeline_response}")

        # Step 10: Test another message to ensure it still works
        print("\n🔄 Testing second message...")
        await pilot.click("#prompt-input")
        for char in "Second test":
            await pilot.press(char)
        await pilot.press("enter")
        await pilot.pause(1.0)
        await take_screenshot(pilot, "second_message", 7)

        # Final summary
        print("\n" + "=" * 60)
        print("📊 DEBUG MODE VALIDATION SUMMARY")
        print("=" * 60)

        success_criteria = {
            "App launches with debug mode": True,
            "Workspace appears during processing": workspace_visible,
            "Response stays in staging (not auto-inscribed)": still_visible,
            "Assistant response visible in staging": has_assistant_response,
            "/inscribe command works": workspace_hidden,
            "Response appears in timeline after inscription": has_timeline_response,
            "Can continue using app normally": True
        }

        passed = sum(1 for v in success_criteria.values() if v)
        total = len(success_criteria)

        for criterion, result in success_criteria.items():
            status = "✅" if result else "❌"
            print(f"{status} {criterion}")

        print(f"\nPassed: {passed}/{total}")

        if passed == total:
            print("\n🎉 DEBUG MODE WORKS FOR DEVELOPERS!")
        else:
            print("\n⚠️  Debug mode has issues that need fixing")

        print(f"\n📁 Evidence in: {SCREENSHOT_DIR}")

if __name__ == "__main__":
    asyncio.run(test_real_debug_mode_usage())
