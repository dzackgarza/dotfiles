#!/usr/bin/env python3
"""Test the complete Sacred GUI user experience with proper screenshots"""

import asyncio
from src.main import LLMReplApp
from src.core.config import Config

async def test_sacred_gui_experience():
    Config.enable_debug_mode()

    async with LLMReplApp().run_test(size=(72, 24)) as pilot:
        app = pilot.app
        await pilot.pause(0.5)

        # STEP 1: Capture IDLE STATE (2-way layout)
        print("=== STEP 1: IDLE STATE ===")
        screenshot = app.export_screenshot(title="Sacred GUI - Idle State")
        with open("debug_screenshots/sacred_gui_01_idle_state.svg", "w") as f:
            f.write(screenshot)
        print("Screenshot saved: sacred_gui_01_idle_state.svg")

        # STEP 2: User types a message
        print("\n=== STEP 2: USER TYPING ===")
        await pilot.click("#prompt-input")
        message = "What is the capital of France?"
        for char in message:
            await pilot.press(char)

        screenshot = app.export_screenshot(title="Sacred GUI - User Typing")
        with open("debug_screenshots/sacred_gui_02_user_typing.svg", "w") as f:
            f.write(screenshot)
        print("Screenshot saved: sacred_gui_02_user_typing.svg")

        # STEP 3: User presses Enter - PROCESSING STATE begins
        print("\n=== STEP 3: PROCESSING STARTS ===")
        await pilot.press("enter")
        await pilot.pause(0.2)  # Brief pause to capture transition

        screenshot = app.export_screenshot(title="Sacred GUI - Processing Starts")
        with open("debug_screenshots/sacred_gui_03_processing_starts.svg", "w") as f:
            f.write(screenshot)
        print("Screenshot saved: sacred_gui_03_processing_starts.svg")

        # STEP 4: During processing - Live Workspace should show cognition steps
        print("\n=== STEP 4: PROCESSING ACTIVE ===")
        await pilot.pause(1.0)  # Let cognition run

        screenshot = app.export_screenshot(title="Sacred GUI - Processing Active")
        with open("debug_screenshots/sacred_gui_04_processing_active.svg", "w") as f:
            f.write(screenshot)
        print("Screenshot saved: sacred_gui_04_processing_active.svg")

        # STEP 5: Processing complete - Debug mode waiting for inscription
        print("\n=== STEP 5: AWAITING INSCRIPTION ===")
        await pilot.pause(2.0)  # Let processing complete

        screenshot = app.export_screenshot(title="Sacred GUI - Awaiting Inscription")
        with open("debug_screenshots/sacred_gui_05_awaiting_inscription.svg", "w") as f:
            f.write(screenshot)
        print("Screenshot saved: sacred_gui_05_awaiting_inscription.svg")

        # STEP 6: User types /inscribe
        print("\n=== STEP 6: USER INSCRIBES ===")
        await pilot.click("#prompt-input")
        await pilot.pause(0.1)
        for char in "/inscribe":
            await pilot.press(char)

        screenshot = app.export_screenshot(title="Sacred GUI - Inscribe Command")
        with open("debug_screenshots/sacred_gui_06_inscribe_command.svg", "w") as f:
            f.write(screenshot)
        print("Screenshot saved: sacred_gui_06_inscribe_command.svg")

        # STEP 7: After inscription - back to IDLE STATE
        print("\n=== STEP 7: AFTER INSCRIPTION ===")
        await pilot.press("enter")
        await pilot.pause(1.0)  # Let inscription complete

        screenshot = app.export_screenshot(title="Sacred GUI - After Inscription")
        with open("debug_screenshots/sacred_gui_07_after_inscription.svg", "w") as f:
            f.write(screenshot)
        print("Screenshot saved: sacred_gui_07_after_inscription.svg")

        print("\n=== SACRED GUI TEST COMPLETE ===")
        print("All screenshots saved to debug_screenshots/")

        # Validate the experience
        print("\n=== VALIDATION ===")

        # Check current state
        staging = app.query_one("#staging-container")
        timeline = app.query_one("#chat-container")
        input_widget = app.query_one("#prompt-input")

        print(f"Staging area visible: {'hidden' not in staging.classes}")
        print(f"Timeline entries: {len(list(timeline.children))}")
        print(f"Input available: {not input_widget.disabled}")

        # Check for proper layout states
        if 'hidden' in staging.classes:
            print("✅ IDLE STATE: 2-way layout (Timeline + Input)")
        else:
            print("⚠️  Still showing 3-way layout")

if __name__ == "__main__":
    asyncio.run(test_sacred_gui_experience())
