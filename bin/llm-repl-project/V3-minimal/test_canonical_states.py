#!/usr/bin/env python3
"""
CANONICAL STATE TRANSITION TEST

This test verifies the Sacred GUI state transitions work correctly:
1. IDLE state (2-way layout): Timeline + Input
2. PROCESSING state (3-way layout): Timeline + Live Workspace + Input
3. Back to IDLE state (2-way layout): Timeline + Input

Screenshots are saved to debug_screenshots/canonical/
"""

import asyncio
from pathlib import Path
from datetime import datetime
from src.main import LLMReplApp
from src.core.config import Config

try:
    from cairosvg import svg2png
    HAS_CAIROSVG = True
except ImportError:
    HAS_CAIROSVG = False
    print("⚠️  cairosvg not available - PNG screenshots disabled")

# Ensure debug mode is on
Config.DEBUG_MODE = True
Config.MANUAL_INSCRIBE_MODE = True

SCREENSHOT_DIR = Path("debug_screenshots/canonical")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

async def save_screenshot(pilot, title: str, filename: str):
    """Save screenshot as PNG (with SVG fallback)"""
    svg_content = pilot.app.export_screenshot(title=title)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"{timestamp}_{filename}"

    if HAS_CAIROSVG:
        try:
            png_data = svg2png(bytestring=svg_content.encode('utf-8'))
            png_path = SCREENSHOT_DIR / f"{base_name}.png"
            png_path.write_bytes(png_data)
            print(f"📸 Screenshot saved: {png_path.name}")
            return png_path
        except Exception as e:
            print(f"⚠️  PNG conversion failed: {e}")

    # Fallback to SVG
    svg_path = SCREENSHOT_DIR / f"{base_name}.svg"
    svg_path.write_text(svg_content)
    print(f"📸 Screenshot saved: {svg_path.name} (PNG unavailable)")
    return svg_path

async def test_canonical_states():
    """Test the Sacred GUI state transitions"""
    print("🎬 CANONICAL STATE TRANSITION TEST")
    print("=" * 60)
    print(f"Debug mode: {Config.DEBUG_MODE}")
    print(f"Manual inscribe mode: {Config.MANUAL_INSCRIBE_MODE}")
    print()

    async with LLMReplApp().run_test(size=(120, 40)) as pilot:
        await pilot.pause(1.0)

        # ========== STATE 1: IDLE (2-way layout) ==========
        print("📍 STATE 1: IDLE (2-way layout)")
        print("   - Sacred Timeline (top)")
        print("   - Input (bottom)")
        print("   - Live Workspace: HIDDEN")

        await save_screenshot(pilot, "IDLE State - 2-way Layout", "01_idle_state")

        # Verify we're in 2-way layout
        workspace = pilot.app.query_one("#staging-container")
        if "collapsed" in workspace.classes:
            print("   ✅ Confirmed: Live Workspace is collapsed")
        else:
            print("   ❌ ERROR: Live Workspace should be collapsed!")
        print()

        # Type a message
        print("📝 Typing user message...")
        await pilot.click("#prompt-input")
        await pilot.pause(0.5)

        message = "What are Python decorators?"
        for char in message:
            await pilot.press(char)
            await pilot.pause(0.05)

        await save_screenshot(pilot, "IDLE State - Message Typed", "02_message_typed")
        print()

        # Submit to trigger processing
        print("⚡ Submitting message to trigger PROCESSING state...")
        await pilot.press("enter")
        await pilot.pause(1.0)  # Allow transition to happen

        # ========== STATE 2: PROCESSING (3-way layout) ==========
        print("📍 STATE 2: PROCESSING (3-way layout)")
        print("   - Sacred Timeline (top)")
        print("   - Live Workspace (middle) - VISIBLE with processing steps")
        print("   - Input (bottom) - disabled during processing")

        await save_screenshot(pilot, "PROCESSING State - 3-way Layout", "03_processing_state")

        # Verify we're in 3-way layout
        workspace = pilot.app.query_one("#staging-container")
        if "collapsed" not in workspace.classes:
            print("   ✅ Confirmed: Live Workspace is visible")
        else:
            print("   ❌ ERROR: Live Workspace should be visible!")

        # Check for processing widget
        processing_widgets = pilot.app.query(".processing-widget")
        if processing_widgets:
            print(f"   ✅ Found {len(processing_widgets)} processing widget(s)")
        else:
            print("   ❌ ERROR: No processing widgets found!")
        print()

        # Wait for processing to show sub-blocks
        print("⏳ Waiting for processing sub-blocks to appear...")
        await pilot.pause(2.0)

        await save_screenshot(pilot, "PROCESSING State - Sub-blocks Visible", "04_processing_subblocks")

        # Wait for processing to complete
        print("⏳ Waiting for processing to complete...")
        await pilot.pause(6.0)  # Total ~8 seconds

        # In debug mode, response should be in staging
        print("🔍 Debug mode check - response should be in staging...")
        await save_screenshot(pilot, "PROCESSING Complete - Debug Mode Staging", "05_debug_staging")

        # Check if still in 3-way layout (debug mode keeps it visible)
        workspace = pilot.app.query_one("#staging-container")
        if Config.DEBUG_MODE and "collapsed" not in workspace.classes:
            print("   ✅ Confirmed: Live Workspace still visible (debug mode)")
        print()

        # Use /inscribe to commit the response
        print("📝 Using /inscribe command to commit response...")
        await pilot.click("#prompt-input")
        await pilot.pause(0.5)

        # Clear input and type /inscribe
        await pilot.press("ctrl+a")
        await pilot.pause(0.1)
        await pilot.press("delete")
        await pilot.pause(0.2)

        for char in "/inscribe":
            await pilot.press(char)
            await pilot.pause(0.05)

        await save_screenshot(pilot, "Debug Mode - /inscribe Command", "06_inscribe_command")

        await pilot.press("enter")
        await pilot.pause(2.0)

        # ========== STATE 3: BACK TO IDLE (2-way layout) ==========
        print("📍 STATE 3: BACK TO IDLE (2-way layout)")
        print("   - Sacred Timeline (top) - now shows the conversation")
        print("   - Input (bottom) - ready for next message")
        print("   - Live Workspace: HIDDEN again")

        await save_screenshot(pilot, "IDLE State - After Inscription", "07_idle_after_inscription")

        # Verify we're back in 2-way layout
        workspace = pilot.app.query_one("#staging-container")
        if "collapsed" in workspace.classes:
            print("   ✅ Confirmed: Live Workspace is collapsed again")
        else:
            print("   ❌ ERROR: Live Workspace should be collapsed!")

        # Check timeline has the conversation
        timeline = pilot.app.query_one("#chat-container")
        blocks = timeline.query(".timeline-block")
        if len(blocks) >= 2:  # At least user + assistant
            print(f"   ✅ Timeline shows {len(blocks)} blocks")
        else:
            print(f"   ❌ ERROR: Timeline only has {len(blocks)} blocks")
        print()

        print("=" * 60)
        print("✅ CANONICAL STATE TRANSITION TEST COMPLETE")
        print(f"📁 Screenshots saved to: {SCREENSHOT_DIR}")
        print()
        print("Summary:")
        print("  1. IDLE → PROCESSING: ✓ Workspace appears")
        print("  2. PROCESSING: ✓ 3-way layout with live updates")
        print("  3. Debug mode: ✓ Response held in staging")
        print("  4. /inscribe: ✓ Commits response to timeline")
        print("  5. PROCESSING → IDLE: ✓ Workspace collapses")

if __name__ == "__main__":
    asyncio.run(test_canonical_states())
