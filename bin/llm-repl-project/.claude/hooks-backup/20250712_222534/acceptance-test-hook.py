#!/usr/bin/env python3
"""
Acceptance Test Hook
Enforces test-first development - blocks code changes without failing tests
"""

import json
import sys
import os
from pathlib import Path
from hook_logger import log_hook_execution

def main():
    # Read hook input
    hook_input = json.loads(sys.stdin.read())
    tool_name = hook_input.get('tool_name', '')
    
    # Get file paths
    file_paths = os.environ.get('CLAUDE_FILE_PATHS', '').split()
    
    log_hook_execution("acceptance-test-hook", tool_name, "checking", f"Files: {file_paths}")
    
    # Check each file
    for file_path in file_paths:
        if file_path.endswith('.py') and 'src/' in file_path and '__pycache__' not in file_path and not file_path.endswith('__init__.py'):
            # Derive test path
            base_name = Path(file_path).stem
            test_path = f"tests/test_{base_name}.py"
            full_test_path = f"/home/dzack/dotfiles/bin/llm-repl-project/V3-minimal/{test_path}"
            
            if not os.path.exists(full_test_path):
                # BLOCK - no test exists
                log_hook_execution("acceptance-test-hook", tool_name, "block", f"No test for {file_path}")
                error_message = f"""🚫 BLOCKED: Test-First Development Required

No test file found for {file_path}
Expected test at: {test_path}

You must create a FAILING acceptance test before implementing code.

Quick start:
1. Create {test_path}
2. Write a test that defines the desired user behavior
3. Ensure the test FAILS with current implementation
4. Then implement the code to make it pass

The test IS the specification!"""
                print(error_message, file=sys.stderr)
                sys.exit(2)
    
    # All files have tests - approve silently
    log_hook_execution("acceptance-test-hook", tool_name, "approve", "All files have tests")
    sys.exit(0)

if __name__ == "__main__":
    main()