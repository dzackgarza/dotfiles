#!/usr/bin/env python3
"""
Pilot test script for LLM REPL V3-minimal
Runs the app, enters commands, captures screenshots, and reports results
"""

import subprocess
import time
import os
import sys
from pathlib import Path
import pexpect

def run_pilot_test():
    """Run the pilot test and capture screenshots"""
    print("🚀 Starting LLM REPL Pilot Test...")
    
    # Ensure we're in the right directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Get screenshot directory
    screenshot_dir = project_dir / "V3-minimal" / "debug_screenshots"
    
    # Count initial screenshots
    initial_screenshots = list(screenshot_dir.glob("*.svg")) if screenshot_dir.exists() else []
    initial_count = len(initial_screenshots)
    
    print(f"📸 Initial screenshots in {screenshot_dir}: {initial_count}")
    
    # Start the app with pexpect for better control
    print("▶️  Starting the app with pexpect...")
    app = pexpect.spawn("pdm run python -m V3-minimal.src.main", 
                        encoding='utf-8', 
                        timeout=30)
    
    test_results = []
    
    try:
        # Wait for app to initialize
        print("⏳ Waiting for app to initialize...")
        time.sleep(5)
        
        # Send 's' key to take initial screenshot
        print("\n📸 Taking initial screenshot (ctrl+s)...")
        app.send('\x13')  # Ctrl+S
        time.sleep(1)
        
        # Test 1: Simple greeting
        print("\n📝 Test 1: Sending 'hello world'")
        app.send("hello world\n")
        time.sleep(3)
        app.send('\x13')  # Take screenshot
        test_results.append("Test 1: Sent 'hello world'")
        
        # Test 2: Test that might trigger the error
        print("\n📝 Test 2: Sending 'test error'")
        app.send("test error\n")
        time.sleep(3)
        app.send('\x13')  # Take screenshot
        test_results.append("Test 2: Sent 'test error'")
        
        # Test 3: Debug info
        print("\n📝 Test 3: Getting debug info (ctrl+d)")
        app.send('\x04')  # Ctrl+D
        time.sleep(2)
        app.send('\x13')  # Take screenshot
        test_results.append("Test 3: Debug info")
        
        # Test 4: Another message
        print("\n📝 Test 4: Sending 'what is 2+2?'")
        app.send("what is 2+2?\n")
        time.sleep(3)
        app.send('\x13')  # Take screenshot
        test_results.append("Test 4: Math question")
        
        # Final screenshot
        print("\n📸 Taking final screenshot...")
        time.sleep(2)
        app.send('\x13')  # Final screenshot
        
        # Exit gracefully
        print("\n🛑 Sending quit command (ctrl+c)...")
        app.send('\x03')  # Ctrl+C
        time.sleep(1)
        
    except pexpect.TIMEOUT:
        print("⏱️  Timeout occurred - app may be unresponsive")
    except Exception as e:
        print(f"❌ Error during pilot test: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Terminate the app
        print("\n🛑 Terminating app...")
        try:
            app.terminate()
            app.wait()
        except:
            pass
    
    # Count final screenshots
    final_screenshots = list(screenshot_dir.glob("*.svg")) if screenshot_dir.exists() else []
    final_count = len(final_screenshots)
    new_screenshots = final_count - initial_count
    
    print("\n✅ Pilot test completed!")
    print(f"\n📊 RESULTS:")
    print(f"- Screenshot directory: {screenshot_dir}")
    print(f"- Initial screenshots: {initial_count}")
    print(f"- Final screenshots: {final_count}")
    print(f"- New screenshots created: {new_screenshots}")
    print(f"\n📋 Tests performed:")
    for result in test_results:
        print(f"  - {result}")
    
    if new_screenshots > 0:
        print(f"\n🎉 Success! {new_screenshots} new screenshots were created.")
        print(f"\n📸 Latest screenshots:")
        # Show the 5 most recent screenshots
        recent_screenshots = sorted(final_screenshots, key=lambda p: p.stat().st_mtime)[-5:]
        for screenshot in recent_screenshots:
            print(f"  - {screenshot.name}")
    
    print(f"\n🔍 Next steps:")
    print(f"1. Review the screenshots in: {screenshot_dir}")
    print(f"2. Look for the error: 'Static.__init__() got an unexpected keyword argument sub_blocks'")
    print(f"3. Check if the GUI is rendering properly")
    print(f"4. The most recent screenshot should show the current state")
    
    return new_screenshots > 0

if __name__ == "__main__":
    # Check if pexpect is available
    try:
        import pexpect
    except ImportError:
        print("❌ pexpect is required. Install with: pdm add pexpect")
        sys.exit(1)
    
    success = run_pilot_test()
    sys.exit(0 if success else 1)