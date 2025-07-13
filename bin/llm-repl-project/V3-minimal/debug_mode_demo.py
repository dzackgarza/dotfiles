#!/usr/bin/env python3
"""
Debug Mode Interactive Demo

This script runs the app in debug mode and provides instructions for testing.
Run with: pdm run python debug_mode_demo.py
"""

import asyncio
from src.main import LLMReplApp
from src.core.config import Config


async def setup_debug_mode():
    """Configure debug mode settings"""
    Config.enable_debug_mode()
    Config.USE_PROCESSING_QUEUE = True
    Config.set_cognition_duration(3.0)  # Shorter for demo
    Config.set_submodule_duration(2.0)  # Shorter for demo


def print_instructions():
    """Print instructions for testing debug mode"""
    print("\n" + "="*60)
    print("🔧 DEBUG MODE DEMO - Interactive Test")
    print("="*60)
    print("\nDebug mode is now active! Here's what you can test:\n")
    print("1. Type a message and press Enter")
    print("   - Watch the staging area expand to 50% height")
    print("   - See the ProcessingWidget with timer, progress bar, and tokens")
    print("   - Notice that only one block processes at a time")
    print("\n2. Send multiple messages quickly")
    print("   - They will queue up and process sequentially")
    print("   - Each shows its state: QUEUED → PROCESSING → DONE")
    print("\n3. Use /inscribe command")
    print("   - Type '/inscribe' and press Enter to move blocks to timeline")
    print("   - Or press Ctrl+I as a shortcut")
    print("\n4. Watch the visual indicators:")
    print("   - Timer counts up during processing, freezes when done")
    print("   - Progress bar fills linearly over 5 seconds")
    print("   - Token counters show simulated up/down values")
    print("\n5. Exit with Ctrl+C")
    print("\n" + "="*60 + "\n")


async def main():
    """Run the demo"""
    await setup_debug_mode()
    print_instructions()

    # Run the app
    app = LLMReplApp()
    await app.run_async()


if __name__ == "__main__":
    asyncio.run(main())
