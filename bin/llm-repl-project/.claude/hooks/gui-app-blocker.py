#!/usr/bin/env python3
"""
GUI App Blocker Hook
Prevents running GUI applications in Claude Code
"""

import json
import sys
import re

def main():
    hook_input = json.loads(sys.stdin.read())
    
    # Get command from tool input
    tool_input = hook_input.get('tool_input', {})
    command = tool_input.get('command', '')
    
    # Check for GUI application commands
    gui_patterns = [
        r'python\s+-m\s+src\.main',
        r'pdm\s+run\s+python\s+-m\s+src\.main',
        r'python\s+src/main\.py',
        r'pdm\s+run\s+python\s+src/main\.py',
        r'just\s+(run|run-fast|run-dev)',
        r'\.\/run',
        r'textual\s+run',
        r'textual\s+console',
        r'textual\s+app',
        r'uvicorn.*--reload'
    ]
    
    for pattern in gui_patterns:
        if re.search(pattern, command, re.IGNORECASE):
            print(json.dumps({
                "decision": "block",
                "reason": f"🚫 GUI application detected: '{command}'. This breaks Claude Code's interface. Use pilot tests instead."
            }))
            return
    
    print(json.dumps({"decision": "approve"}))

if __name__ == "__main__":
    main()