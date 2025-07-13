#!/usr/bin/env python3
"""
BRUTAL REALITY CHECK: Manual Inscription Feature

Let me be completely honest about what actually works vs what I claimed.
I'll test each claim against reality and report any gaps.
"""

import asyncio
from src.main import LLMReplApp
from src.core.config import Config

async def reality_check():
    """Brutal honesty test - what actually works vs what I claimed"""

    print("🔍 BRUTAL REALITY CHECK: Manual Inscription Feature")
    print("=" * 60)
    print()

    # Enable manual inscription for testing
    Config.MANUAL_INSCRIBE_MODE = True

    print("📋 TESTING MY CLAIMS AGAINST REALITY:")
    print()

    async with LLMReplApp().run_test(size=(120, 40)) as pilot:
        await pilot.pause(1.0)

        # === CLAIM 1: Sacred GUI has 2-way IDLE state ===
        print("🔍 CLAIM 1: Sacred GUI starts in 2-way IDLE state")
        staging = pilot.app.query_one("#staging-container")
        chat = pilot.app.query_one("#chat-container")
        prompt = pilot.app.query_one("#prompt-input")

        idle_correct = "processing" not in staging.classes
        has_timeline = chat is not None
        has_input = prompt is not None

        print(f"   ✅ Has Sacred Timeline: {has_timeline}")
        print(f"   ✅ Has Input area: {has_input}")
        print(f"   ✅ Workspace hidden in IDLE: {idle_correct}")

        if idle_correct and has_timeline and has_input:
            print("   ✅ CLAIM 1: TRUE - Sacred GUI IDLE state works")
        else:
            print("   ❌ CLAIM 1: FALSE - Sacred GUI IDLE state broken")
        print()

        # === CLAIM 2: Transitions to 3-way PROCESSING state ===
        print("🔍 CLAIM 2: Sacred GUI transitions to 3-way PROCESSING state")

        await pilot.click("#prompt-input")
        for char in "test processing transition":
            await pilot.press(char)
        await pilot.press("enter")
        await pilot.pause(1.0)

        processing_visible = "processing" in staging.classes
        timeline_still_there = chat is not None
        input_still_there = prompt is not None

        print(f"   ✅ Live Workspace visible: {processing_visible}")
        print(f"   ✅ Sacred Timeline still present: {timeline_still_there}")
        print(f"   ✅ Input still available: {input_still_there}")

        if processing_visible and timeline_still_there and input_still_there:
            print("   ✅ CLAIM 2: TRUE - Sacred GUI PROCESSING state works")
        else:
            print("   ❌ CLAIM 2: FALSE - Sacred GUI PROCESSING state broken")
        print()

        # === CLAIM 3: Manual inscription keeps workspace visible ===
        print("🔍 CLAIM 3: Manual inscription keeps workspace visible after processing")

        await pilot.pause(8.0)  # Wait for processing to complete

        still_visible_after = "processing" in staging.classes
        processor = pilot.app.unified_async_processor
        has_pending_data = processor._pending_inscription is not None

        print(f"   🔍 Workspace still visible after processing: {still_visible_after}")
        print(f"   🔍 Has pending inscription data: {has_pending_data}")

        if still_visible_after and has_pending_data:
            print("   ✅ CLAIM 3: TRUE - Manual inscription works as designed")
        else:
            print("   ❌ CLAIM 3: FALSE - Manual inscription doesn't work")
            print(f"      Debug: workspace visible={still_visible_after}, pending data={has_pending_data}")
        print()

        # === CLAIM 4: /inscribe command works ===
        print("🔍 CLAIM 4: /inscribe command triggers inscription")

        # Check timeline before inscription
        children_before = len([c for c in chat.children if hasattr(c, 'classes') and 'human-message' in c.classes])

        await pilot.click("#prompt-input")
        await pilot.pause(0.2)
        await pilot.press("ctrl+a")
        await pilot.press("delete")
        for char in "/inscribe":
            await pilot.press(char)
        await pilot.press("enter")
        await pilot.pause(2.0)

        # Check results
        children_after = len([c for c in chat.children if hasattr(c, 'classes') and 'human-message' in c.classes])
        workspace_hidden_after = "processing" not in staging.classes
        no_pending_after = processor._pending_inscription is None

        inscription_worked = children_after > children_before

        print(f"   🔍 Timeline updated: {inscription_worked} (before: {children_before}, after: {children_after})")
        print(f"   🔍 Workspace hidden after: {workspace_hidden_after}")
        print(f"   🔍 No pending data after: {no_pending_after}")

        if inscription_worked and workspace_hidden_after and no_pending_after:
            print("   ✅ CLAIM 4: TRUE - /inscribe command works perfectly")
        else:
            print("   ❌ CLAIM 4: FALSE - /inscribe command broken")
        print()

        # === CLAIM 5: Returns to IDLE state ===
        print("🔍 CLAIM 5: Sacred GUI returns to IDLE state after inscription")

        final_idle = "processing" not in staging.classes
        timeline_has_conversation = children_after > 0

        print(f"   🔍 Back to IDLE state: {final_idle}")
        print(f"   🔍 Timeline has conversations: {timeline_has_conversation}")

        if final_idle and timeline_has_conversation:
            print("   ✅ CLAIM 5: TRUE - Returns to IDLE with saved conversation")
        else:
            print("   ❌ CLAIM 5: FALSE - Doesn't return to proper IDLE state")
        print()

    # Reset
    Config.MANUAL_INSCRIBE_MODE = False

    print("🏆 REALITY CHECK SUMMARY:")
    print("=" * 60)
    print()
    print("I tested my 5 core claims against actual runtime behavior.")
    print("The results above show what actually works vs what I claimed.")
    print()
    print("If all claims are TRUE, the feature works as advertised.")
    print("If any claims are FALSE, I need to fix those gaps.")
    print()
    print("This is my honest assessment based on actual testing,")
    print("not assumptions or theoretical analysis.")

if __name__ == "__main__":
    asyncio.run(reality_check())
