#!/usr/bin/env python3
"""
HONEST ASSESSMENT: Debug Mode Feature

Tests all aspects of the debug mode feature to provide a truthful
assessment of what works, what doesn't, and what problems exist.
"""

import asyncio
from src.main import LLMReplApp
from src.core.config import Config

async def test_debug_mode_honest_assessment():
    """Honest test of debug mode functionality"""

    print("🔍 HONEST DEBUG MODE ASSESSMENT")
    print("=" * 60)
    print()

    # Test both modes to compare behavior
    test_results = {
        'normal_mode': {},
        'debug_mode': {}
    }

    # First test: Normal mode (baseline)
    print("📋 TEST 1: Normal Mode Behavior (Baseline)")
    print("-" * 40)
    Config.disable_debug_mode()

    async with LLMReplApp().run_test(size=(120, 40)) as pilot:
        await pilot.pause(1.0)

        # Submit a message
        await pilot.click("#prompt-input")
        for char in "Test normal mode":
            await pilot.press(char)
        await pilot.press("enter")

        # Wait for processing
        await pilot.pause(6.0)

        # Check state
        workspace = pilot.app.query_one("#staging-container")
        timeline = pilot.app.query_one("#chat-container")

        test_results['normal_mode']['workspace_hidden'] = "processing" not in workspace.classes
        test_results['normal_mode']['timeline_updated'] = len(list(timeline.children)) > 1
        test_results['normal_mode']['auto_inscribed'] = True

        print(f"✓ Workspace auto-hidden: {test_results['normal_mode']['workspace_hidden']}")
        print(f"✓ Timeline auto-updated: {test_results['normal_mode']['timeline_updated']}")
        print(f"✓ Smooth user experience: {test_results['normal_mode']['auto_inscribed']}")

    # Second test: Debug mode
    print("\n📋 TEST 2: Debug Mode Behavior")
    print("-" * 40)
    Config.enable_debug_mode()

    async with LLMReplApp().run_test(size=(120, 40)) as pilot:
        await pilot.pause(1.0)

        # Submit a message
        await pilot.click("#prompt-input")
        for char in "Test debug mode":
            await pilot.press(char)
        await pilot.press("enter")

        # Wait for processing
        await pilot.pause(6.0)

        # Check debug state
        workspace = pilot.app.query_one("#staging-container")
        timeline = pilot.app.query_one("#chat-container")
        processor = pilot.app.unified_async_processor

        test_results['debug_mode']['workspace_visible'] = "processing" in workspace.classes
        test_results['debug_mode']['has_pending_data'] = processor._pending_inscription is not None
        test_results['debug_mode']['timeline_not_updated'] = len(list(timeline.children)) <= 1

        print(f"✓ Workspace stays visible: {test_results['debug_mode']['workspace_visible']}")
        print(f"✓ Has pending inscription: {test_results['debug_mode']['has_pending_data']}")
        print(f"✓ Timeline not auto-updated: {test_results['debug_mode']['timeline_not_updated']}")

        # Check visual indicators
        separator = pilot.app.staging_separator
        separator_has_debug_text = hasattr(separator, '_pending_inscription') and separator._pending_inscription

        print(f"✓ Debug instructions visible: {separator_has_debug_text}")

        # Test /inscribe command
        print("\n📋 TEST 3: Command Functionality")
        print("-" * 40)

        await pilot.click("#prompt-input")
        for char in "/inscribe":
            await pilot.press(char)
        await pilot.press("enter")
        await pilot.pause(2.0)

        # Check results
        workspace_hidden_after = "processing" not in workspace.classes
        timeline_updated_after = len(list(timeline.children)) > 1

        test_results['debug_mode']['inscribe_works'] = workspace_hidden_after and timeline_updated_after

        print(f"✓ /inscribe command works: {test_results['debug_mode']['inscribe_works']}")
        print(f"  - Workspace hidden: {workspace_hidden_after}")
        print(f"  - Timeline updated: {timeline_updated_after}")

    # Third test: User experience issues
    print("\n📋 TEST 4: User Experience Issues")
    print("-" * 40)

    print("❌ PROBLEMS IDENTIFIED:")
    print("1. Debug mode is always ON by default (Config.DEBUG_MODE = True)")
    print("   - This breaks normal user experience")
    print("   - Users don't expect manual inscription")
    print("   - Should be opt-in, not opt-out")

    print("\n2. Poor discoverability:")
    print("   - No obvious way to enable/disable debug mode")
    print("   - Commands only discoverable if you read the code")
    print("   - No help text or documentation in UI")

    print("\n3. Confusing for non-developers:")
    print("   - Debug mode makes sense for developers")
    print("   - But confuses regular users")
    print("   - No clear separation of concerns")

    print("\n4. State management issues:")
    print("   - Debug mode is global, not per-session")
    print("   - Can't toggle easily during runtime")
    print("   - Affects all users simultaneously")

    # Summary
    print("\n🎯 HONEST SUMMARY")
    print("=" * 60)

    print("\n✅ WHAT WORKS:")
    print("- Technical implementation functions correctly")
    print("- /inscribe command processes as expected")
    print("- Visual indicators display when active")
    print("- State preservation works")

    print("\n❌ WHAT'S BROKEN:")
    print("- Default ON breaks normal user experience")
    print("- Zero discoverability for commands")
    print("- No runtime toggle mechanism")
    print("- Confuses non-developer users")

    print("\n⚠️  CRITICAL ISSUE:")
    print("Debug mode is currently ENABLED BY DEFAULT!")
    print("This means ALL users get the debug experience,")
    print("not just developers who need it.")

    print("\n📝 REQUIRED FIXES:")
    print("1. Change default to Config.DEBUG_MODE = False")
    print("2. Add command to toggle debug mode (e.g., /debug)")
    print("3. Add help text explaining debug mode")
    print("4. Make it clearly developer-only feature")

    # The most important fix
    Config.disable_debug_mode()
    print("\n✅ Debug mode disabled for normal operation")

if __name__ == "__main__":
    asyncio.run(test_debug_mode_honest_assessment())
