#!/usr/bin/env python3
"""
Simple test to debug inscription issue
"""

import asyncio
from pathlib import Path
from src.main import LLMReplApp

async def test_simple_inscription():
    """Simple test to see if inscription works"""
    print("🔍 DEBUGGING INSCRIPTION")

    async with LLMReplApp().run_test(size=(72, 48)) as pilot:
        await pilot.pause(1.0)  # Let app initialize

        # Type and submit simple message
        print("📝 Typing simple message")
        await pilot.click("#prompt-input")
        for char in "test message":
            await pilot.press(char)

        print("🚀 Submitting message")
        await pilot.press("enter")

        # Wait for processing to complete
        print("⏳ Waiting for processing...")
        await pilot.pause(8.0)  # Wait longer for processing

        # Check what's in the timeline
        print("🔍 Checking timeline content")
        chat_container = pilot.app.query_one("#chat-container")
        children = list(chat_container.children)

        print(f"📊 Timeline has {len(children)} children:")
        for i, child in enumerate(children):
            print(f"  {i}: {child.__class__.__name__} - {getattr(child, 'classes', 'no classes')}")
            if hasattr(child, 'renderable'):
                content = str(child.renderable)[:100]
                print(f"      Content: {content}")

        # Take final screenshot
        screenshot = pilot.app.export_screenshot(title="Inscription Debug")
        Path("inscription_debug.svg").write_text(screenshot)
        print("📸 Screenshot saved: inscription_debug.svg")

if __name__ == "__main__":
    asyncio.run(test_simple_inscription())
