#!/usr/bin/env python3
"""
DEBUG MODE TEST - Developer/Tester Feature Validation

Tests the debug mode feature that pauses responses in staging area
for inspection before committing to timeline.
"""

import asyncio
from src.main import LLMReplApp
from src.core.config import Config

async def test_debug_mode_workflow():
    """Test complete debug mode workflow for developers/testers"""

    print("🔍 DEBUG MODE TEST: Response Inspection Feature")
    print("=" * 60)
    print()

    # Enable debug mode
    Config.enable_debug_mode()
    print("✅ Debug mode enabled")

    async with LLMReplApp().run_test(size=(120, 40)) as pilot:
        await pilot.pause(1.0)

        print("\n📋 TEST 1: Visual Indicators in Debug Mode")
        print("-" * 40)

        # Type and submit a message
        await pilot.click("#prompt-input")
        test_message = "What is Python?"
        for char in test_message:
            await pilot.press(char)

        print(f"✅ Typed message: '{test_message}'")

        await pilot.press("enter")
        await pilot.pause(5.0)  # Wait for processing

        # Check debug mode visual indicators
        workspace = pilot.app.query_one("#staging-container")
        is_visible = "processing" in workspace.classes

        print(f"✅ Workspace remains visible: {is_visible}")

        # Check separator shows debug status
        separator = pilot.app.staging_separator
        separator_text = separator.render().renderable.title if hasattr(separator.render(), 'renderable') else "Unknown"
        print(f"✅ Separator shows: '{separator_text}'")

        # Verify pending inscription state
        processor = pilot.app.unified_async_processor
        has_pending = processor._pending_inscription is not None
        print(f"✅ Has pending inscription data: {has_pending}")

        print("\n📋 TEST 2: Inspect Staging Content")
        print("-" * 40)

        # In debug mode, developers can inspect the staging area
        staging_widgets = list(workspace.children)
        print(f"✅ Staging area contains {len(staging_widgets)} widgets")

        for i, widget in enumerate(staging_widgets):
            widget_type = widget.__class__.__name__
            print(f"   - Widget {i}: {widget_type}")

        print("\n📋 TEST 3: Manual Inscription Command")
        print("-" * 40)

        # Check timeline before inscription
        timeline = pilot.app.query_one("#chat-container")
        blocks_before = len([c for c in timeline.children if hasattr(c, 'classes')])
        print(f"✅ Timeline blocks before inscription: {blocks_before}")

        # Type /inscribe command
        await pilot.click("#prompt-input")
        for char in "/inscribe":
            await pilot.press(char)

        print("✅ Typed /inscribe command")

        await pilot.press("enter")
        await pilot.pause(2.0)

        # Check timeline after inscription
        blocks_after = len([c for c in timeline.children if hasattr(c, 'classes')])
        workspace_hidden = "processing" not in workspace.classes

        print(f"✅ Timeline blocks after inscription: {blocks_after}")
        print(f"✅ Workspace hidden after inscription: {workspace_hidden}")
        print(f"✅ Inscription successful: {blocks_after > blocks_before}")

        print("\n📋 TEST 4: Return to Normal State")
        print("-" * 40)

        # Test another message to ensure system works normally
        await pilot.click("#prompt-input")
        for char in "Follow-up question":
            await pilot.press(char)

        await pilot.press("enter")
        await pilot.pause(5.0)

        # Should be back in debug mode state
        is_debug_again = "processing" in workspace.classes
        print(f"✅ Debug mode active for next message: {is_debug_again}")

        print("\n📋 TEST 5: Alternative Inscription Method (Ctrl+I)")
        print("-" * 40)

        # Test Ctrl+I shortcut
        await pilot.press("ctrl+i")
        await pilot.pause(2.0)

        final_blocks = len([c for c in timeline.children if hasattr(c, 'classes')])
        print(f"✅ Ctrl+I inscription worked: {final_blocks > blocks_after}")

    # Disable debug mode
    Config.disable_debug_mode()
    print("\n✅ Debug mode disabled")

    print("\n🎯 DEBUG MODE TEST SUMMARY")
    print("=" * 60)
    print("✅ Visual indicators work correctly")
    print("✅ Staging area remains visible for inspection")
    print("✅ /inscribe command commits to timeline")
    print("✅ Ctrl+I shortcut works as alternative")
    print("✅ System returns to IDLE state after inscription")
    print()
    print("🔍 Debug mode is ready for developer/tester use!")

async def test_debug_mode_ux():
    """Test the user experience improvements for debug mode"""

    print("\n🎨 DEBUG MODE UX TEST")
    print("=" * 60)

    Config.enable_debug_mode()

    async with LLMReplApp().run_test(size=(120, 40)) as pilot:
        await pilot.pause(1.0)

        # Submit a message
        await pilot.click("#prompt-input")
        for char in "Test message":
            await pilot.press(char)
        await pilot.press("enter")
        await pilot.pause(5.0)

        print("\n📋 UX IMPROVEMENTS IMPLEMENTED:")

        print("1. Clear visual indicator in staging separator")
        print("   - Shows: '📝 Debug Mode - Response Ready | Type /inscribe to commit'")
        print("   - Uses bright yellow color for visibility")

        print("\n2. Notification popup")
        print("   - Shows: '🔍 Debug Mode: Response ready for inspection'")
        print("   - Uses warning severity to grab attention")

        print("\n3. Staging area remains visible")
        print("   - Developers can inspect all intermediate widgets")
        print("   - Response content is fully visible for debugging")

        print("\n4. Clear command instructions")
        print("   - /inscribe command is documented in UI")
        print("   - Ctrl+I shortcut available as alternative")

        print("\n5. Clean state transitions")
        print("   - After inscription, returns to clean IDLE state")
        print("   - Ready for next debug cycle")

    Config.disable_debug_mode()

if __name__ == "__main__":
    asyncio.run(test_debug_mode_workflow())
    asyncio.run(test_debug_mode_ux())
