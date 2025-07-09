#!/usr/bin/env python3
"""Debug what external test actually sees"""

import pexpect
from pathlib import Path

def debug_what_external_test_sees():
    """Debug what pexpect actually sees when running 'just run'"""
    
    project_root = Path(__file__).parent
    
    print("🔍 DEBUGGING EXTERNAL TEST VIEW")
    print("=" * 50)
    
    # Spawn the same way as the test
    child = pexpect.spawn('just run', timeout=10, cwd=project_root, encoding='utf-8')
    
    try:
        # Read everything that appears for first 3 seconds
        import time
        time.sleep(3)
        
        # Get all output
        output = child.before or ""
        
        print("📋 RAW OUTPUT THAT EXTERNAL TEST SEES:")
        print("-" * 50)
        print(repr(output))
        print("-" * 50)
        print("📋 FORMATTED OUTPUT:")
        print(output)
        print("-" * 50)
        
        # Check if there's a prompt
        if child.after:
            print(f"📋 AFTER BUFFER: {repr(child.after)}")
        
        # Send quit to clean up
        child.sendline('/quit')
        child.expect(pexpect.EOF)
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print(f"📋 BUFFER: {repr(child.before)}")
        print(f"📋 AFTER: {repr(child.after)}")
    finally:
        if child.isalive():
            child.terminate()

if __name__ == "__main__":
    debug_what_external_test_sees()