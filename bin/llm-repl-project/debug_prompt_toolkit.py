#!/usr/bin/env python3
"""
Debug script to isolate prompt_toolkit freeze issue.
"""

import sys
import asyncio
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.styles import Style

async def test_basic_prompt():
    """Test the most basic prompt_toolkit usage."""
    print("Testing basic prompt_toolkit...")
    print(f"TTY status: {sys.stdin.isatty()}")
    
    try:
        # Most basic prompt
        session = PromptSession(
            message="> ",
            multiline=False,
            mouse_support=False,
            history=InMemoryHistory(),
        )
        
        print("About to call prompt_async()...")
        result = await session.prompt_async()
        print(f"Got result: {result}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

def test_sync_prompt():
    """Test synchronous prompt for comparison."""
    print("\nTesting synchronous prompt...")
    
    try:
        from prompt_toolkit.shortcuts import prompt
        result = prompt("> ")
        print(f"Sync result: {result}")
    except Exception as e:
        print(f"Sync error: {e}")
        import traceback
        traceback.print_exc()

async def test_simple_input():
    """Test even simpler input method."""
    print("\nTesting simple input()...")
    
    try:
        print("Type something:", end=" ", flush=True)
        result = input()
        print(f"Simple input result: {result}")
    except Exception as e:
        print(f"Simple input error: {e}")

async def main():
    """Test different input methods."""
    await test_basic_prompt()
    test_sync_prompt()
    await test_simple_input()

if __name__ == "__main__":
    asyncio.run(main())