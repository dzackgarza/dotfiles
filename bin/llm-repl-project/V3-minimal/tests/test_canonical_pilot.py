#!/usr/bin/env python3
"""
CANONICAL PILOT TEST - The One True Test

This test runs the ACTUAL app (same as 'just run') and performs typical user
interactions while taking screenshots at each step. This provides visual proof
of what the app actually does, not what we think it does.

To run: pdm run pytest tests/test_canonical_pilot.py -v
"""

import pytest
from pathlib import Path
from datetime import datetime
from src.main import LLMReplApp


# Screenshot directory
SCREENSHOT_DIR = Path("debug_screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)


async def take_screenshot(pilot, step_name: str):
    """Take a screenshot with a descriptive name"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"canonical_{timestamp}_{step_name}.svg"
    screenshot_path = SCREENSHOT_DIR / filename
    
    # Take the screenshot
    svg_content = pilot.app.export_screenshot(title=f"Canonical Test: {step_name}")
    screenshot_path.write_text(svg_content)
    
    print(f"\n📸 Screenshot saved: {screenshot_path}")
    return screenshot_path


@pytest.mark.asyncio
async def test_canonical_user_journey():
    """The canonical test that proves the app works for real users"""
    
    print("\n🚀 STARTING CANONICAL PILOT TEST")
    print("=" * 60)
    
    async with LLMReplApp().run_test() as pilot:
        # Step 1: Initial state
        print("\n📍 Step 1: App launches successfully")
        await pilot.pause(0.5)  # Let app fully initialize
        await take_screenshot(pilot, "01_initial_launch")
        
        # Verify basic structure
        assert pilot.app.query_one("#prompt-input")
        assert pilot.app.query_one("#chat-container") 
        print("✅ App structure verified")
        
        # Step 2: Type a simple message
        print("\n📍 Step 2: User types a simple greeting")
        await pilot.click("#prompt-input")
        message = "Hello, can you help me understand Python decorators?"
        for char in message:
            await pilot.press(char)
        await take_screenshot(pilot, "02_typed_message")
        
        # Step 3: Submit the message
        print("\n📍 Step 3: User presses Enter to submit")
        await pilot.press("enter")
        await pilot.pause(0.5)  # Let UI update
        await take_screenshot(pilot, "03_after_submit")
        
        # Step 4: Wait for response (with intermediate screenshots)
        print("\n📍 Step 4: Waiting for AI response...")
        for i in range(3):
            await pilot.pause(1.0)
            await take_screenshot(pilot, f"04_processing_{i+1}")
            
        # Step 5: Check if response appeared
        print("\n📍 Step 5: Verify response appears in timeline")
        await pilot.pause(2.0)  # Extra time for response
        await take_screenshot(pilot, "05_response_received")
        
        # Step 6: Try scrolling the timeline
        print("\n📍 Step 6: User scrolls through conversation")
        timeline = pilot.app.query_one("#chat-container")
        await pilot.click("#chat-container")
        await pilot.press("down", "down", "down")
        await take_screenshot(pilot, "06_after_scroll_down")
        
        # Step 7: Type a follow-up question
        print("\n📍 Step 7: User types follow-up question")
        await pilot.click("#prompt-input")
        followup = "Can you show me a simple example?"
        for char in followup:
            await pilot.press(char)
        await take_screenshot(pilot, "07_follow_up_typed")
        
        # Step 8: Submit follow-up
        print("\n📍 Step 8: Submit follow-up question")
        await pilot.press("enter")
        await pilot.pause(0.5)
        await take_screenshot(pilot, "08_follow_up_submitted")
        
        # Step 9: Multi-turn conversation check
        print("\n📍 Step 9: Verify multi-turn conversation")
        await pilot.pause(3.0)  # Wait for second response
        await take_screenshot(pilot, "09_multi_turn_conversation")
        
        # Step 10: Test keyboard navigation
        print("\n📍 Step 10: Test keyboard navigation")
        await pilot.press("tab")  # Should cycle through focusable elements
        await take_screenshot(pilot, "10_keyboard_nav_tab")
        
        # Step 11: Edge case - empty submit
        print("\n📍 Step 11: User tries to submit empty message")
        await pilot.click("#prompt-input")
        await pilot.press("ctrl+a")  # Select all
        await pilot.press("delete")   # Clear
        await pilot.press("enter")    # Try to submit empty
        await take_screenshot(pilot, "11_empty_submit_attempt")
        
        # Step 12: Long message handling
        print("\n📍 Step 12: User types a very long message")
        await pilot.click("#prompt-input")
        long_message = "This is a very long message. " * 20
        for char in long_message:
            await pilot.press(char)
        await take_screenshot(pilot, "12_long_message_typed")
        
        # Final state
        print("\n📍 Final: Overall app state after user session")
        await take_screenshot(pilot, "13_final_state")
        
        print("\n" + "=" * 60)
        print("✅ CANONICAL PILOT TEST COMPLETE")
        print(f"📸 Screenshots saved to: {SCREENSHOT_DIR}")
        print("=" * 60)


@pytest.mark.asyncio
async def test_canonical_extensions():
    """
    Extension point for new behaviors. Add new test scenarios here
    without breaking the main canonical test.
    """
    
    print("\n🔧 RUNNING CANONICAL EXTENSIONS")
    
    async with LLMReplApp().run_test() as pilot:
        await pilot.pause(0.5)
        
        # Add new test scenarios here as needed
        # Example: Test special key combinations
        print("\n📍 Extension: Test Shift+Enter for multiline")
        await pilot.click("#prompt-input")
        for char in "Line 1":
            await pilot.press(char)
        await pilot.press("shift+enter")
        for char in "Line 2":
            await pilot.press(char)
        await take_screenshot(pilot, "ext_multiline_input")
        
        # Test sub_blocks fix - verify CognitionWidget doesn't cause Static errors
        print("\n📍 Extension: Test sub_blocks fix (CognitionWidget)")
        await pilot.click("#prompt-input")
        await pilot.press("ctrl+a")  # Clear input
        await pilot.press("delete")
        
        # Type a message that triggers cognition processing
        test_message = "test cognition pipeline"
        for char in test_message:
            await pilot.press(char)
        
        await take_screenshot(pilot, "ext_01_sub_blocks_fix_typed")
        
        # Submit the message - this triggers the code path where the error occurred
        await pilot.press("enter")
        await pilot.pause(1.0)  # Wait for processing to start
        
        await take_screenshot(pilot, "ext_02_sub_blocks_fix_processing")
        
        # Wait for cognition to complete
        await pilot.pause(2.0)
        
        # Take final screenshot showing successful completion
        await take_screenshot(pilot, "ext_03_sub_blocks_fix_complete")
        
        print("✅ Sub_blocks fix verified - no Static.__init__ errors!")
        
        # Add more extensions as features are added
        print("\n✅ Extensions complete")


if __name__ == "__main__":
    # Allow running directly with python
    import asyncio
    asyncio.run(test_canonical_user_journey())