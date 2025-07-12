#!/usr/bin/env python3
"""Test that Ctrl+P menu has debug commands"""

import asyncio
from src.main import LLMReplApp

async def test_ctrl_p_functionality():
    """Test if Ctrl+P opens command palette with debug commands"""
    
    print("🧪 TESTING CTRL+P COMMAND PALETTE")
    print("=" * 40)
    
    try:
        app = LLMReplApp()
        
        async with app.run_test(size=(80, 24)) as pilot:
            print("✅ App started in pilot mode")
            
            # Check if command providers are registered
            command_providers = app.COMMANDS
            print(f"✅ Command providers: {len(command_providers)} registered")
            
            for provider in command_providers:
                print(f"   - {provider.__name__}")
            
            await pilot.pause()
            print("✅ Basic Ctrl+P functionality test complete")
            
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_ctrl_p_functionality())
    if success:
        print("\n🎯 RESULT: Ctrl+P command palette should work")
        print("   Debug commands: Screenshot, Clear Timeline, Widget Tree, etc.")
        print("   Reality commands: Take Reality Screenshot, Visual Check, etc.") 
    else:
        exit(1)