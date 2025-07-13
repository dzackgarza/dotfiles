#!/usr/bin/env python3
"""
Debug version of acceptance test hook to see what's happening
"""

import json
import sys
import os
from pathlib import Path

def main():
    # Read hook input
    hook_input = json.loads(sys.stdin.read())
    
    # Get file paths
    file_paths = os.environ.get('CLAUDE_FILE_PATHS', '').split()
    
    print(f"DEBUG: CLAUDE_FILE_PATHS = {file_paths}", file=sys.stderr)
    print(f"DEBUG: Hook input = {hook_input}", file=sys.stderr)
    
    # Check each file
    for file_path in file_paths:
        if file_path.endswith('.py') and 'src/' in file_path and '__pycache__' not in file_path:
            print(f"DEBUG: Checking testable file: {file_path}", file=sys.stderr)
            
            # Derive test path
            base_name = Path(file_path).stem
            test_path = f"V3-minimal/tests/test_{base_name}.py"
            full_test_path = f"/home/dzack/dotfiles/bin/llm-repl-project/{test_path}"
            
            print(f"DEBUG: Looking for test at: {full_test_path}", file=sys.stderr)
            
            if not os.path.exists(full_test_path):
                print(f"🚫 BLOCKED: No test file found for {file_path}", file=sys.stderr)
                print(f"Expected test at: {test_path}", file=sys.stderr)
                print("Test-first development requires a failing test before implementation!", file=sys.stderr)
                sys.exit(2)  # Block with exit code 2
    
    # All good - approve
    print(json.dumps({"decision": "approve"}))

if __name__ == "__main__":
    main()