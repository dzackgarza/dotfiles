#!/usr/bin/env python3
"""
Test hook to verify message visibility
Tests different output methods to see what Claude actually sees
"""

import json
import sys
import os
import random
from hook_logger import log_hook_execution

def main():
    hook_input = json.loads(sys.stdin.read())
    tool_name = hook_input.get('tool_name', '')
    
    # Always log that we ran
    log_hook_execution("test-hook-visibility", tool_name, "testing", "Testing message visibility")
    
    # Test 1: Write to a file to prove hook is running
    with open("/home/dzack/dotfiles/bin/llm-repl-project/.claude/hooks/logs/test_visibility.txt", "a") as f:
        f.write(f"Hook ran for {tool_name} at {os.environ.get('USER', 'unknown')}\n")
    
    # Test 2: Try stderr output (should show to Claude)
    print(f"🧪 TEST HOOK: This is a stderr message for {tool_name} - can you see this?", file=sys.stderr)
    
    # Test 3: Try JSON format for PreToolUse with BLOCK to see if Claude sees it
    if tool_name in ['Read', 'Write', 'Edit']:
        # Test if Claude sees block messages
        if random.randint(1, 10) == 1:  # 10% chance to test blocking
            print(json.dumps({
                "decision": "block",
                "reason": f"🔬 TEST HOOK BLOCK: Testing {tool_name} - Claude, can you see THIS message? (This is just a test, retry the operation)"
            }))
        else:
            # Normal approve - goes to user
            print(json.dumps({
                "decision": "approve",
                "reason": f"🔬 TEST HOOK APPROVE: Testing {tool_name} - this goes to terminal"
            }))
    
    # Always exit 0 for JSON format
    sys.exit(0)

if __name__ == "__main__":
    main()