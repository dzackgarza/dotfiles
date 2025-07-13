#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""
PostToolUse Hook - Tool Completion Logging and Validation

CLAUDE COMMUNICATION METHODS:
================================================================================
This hook can directly communicate with Claude using these methods:

1. EXIT CODE 2 + stderr:
   - Tool has already executed (CANNOT be blocked)
   - stderr content is automatically fed to Claude as an error message
   - Used for post-execution validation failures
   - Example: sys.exit(2) with print("ERROR: validation failed", file=sys.stderr)

2. JSON OUTPUT + EXIT CODE 0:
   Advanced control via stdout JSON:
   
   a) Decision Control:
      {"decision": "block", "reason": "explanation"}
      - Shows error to Claude (tool already ran, cannot undo)
      - Claude receives reason and must respond accordingly
      
   b) Session Control:
      {"continue": false, "stopReason": "reason"}
      - Stops Claude entirely, reason shown to user (NOT Claude)

3. NO COMMUNICATION (Exit Code 0, no stderr):
   - Normal completion, only logging occurs
   - No Claude interaction

CURRENT IMPLEMENTATION: Uses method #3 (no communication) - pure logging
NOTE: Could be extended to validate tool results and communicate failures to Claude
================================================================================
"""

import json
import os
import sys
from pathlib import Path

def provide_tdd_feedback(tool_name, tool_input, tool_result):
    """
    Provide immediate TDD feedback after tool execution.
    """
    # After code implementation feedback
    if tool_name in ['Edit', 'Write', 'MultiEdit']:
        file_path = tool_input.get('file_path', '')
        if 'src/' in file_path and file_path.endswith(('.py', '.js', '.ts')):
            print("🧪 TEST NOW: Run your user story to verify implementation", file=sys.stderr)
            print("   Command: task-master test-story --id=<current-task>", file=sys.stderr)
    
    # After getting next task
    if tool_name == 'Bash':
        command = tool_input.get('command', '')
        if 'task-master next' in command:
            print("📖 TDD WORKFLOW REMINDER:", file=sys.stderr)
            print("   1. task-master generate-story --id=<task-id>", file=sys.stderr)
            print("   2. task-master test-story --id=<task-id> (verify fails)", file=sys.stderr)
            print("   3. Implement feature", file=sys.stderr)
            print("   4. task-master test-story --id=<task-id> (verify passes)", file=sys.stderr)
            print("   5. task-master complete-with-story --id=<task-id>", file=sys.stderr)
            
        # Error recovery reminders
        result_text = str(tool_result.get('result', ''))
        if 'error' in result_text.lower() or 'failed' in result_text.lower():
            print("🚨 Consider: Does this error affect your user story?", file=sys.stderr)
            print("   Action: Re-run task-master test-story --id=<task> to verify", file=sys.stderr)

def main():
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)
        
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        tool_result = input_data.get('tool_result', {})
        
        # Provide TDD feedback
        provide_tdd_feedback(tool_name, tool_input, tool_result)
        
        # Simple logging like canonical hooks
        log_dir = Path.cwd() / '.claude' / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / 'post_tool_use.json'
        
        # Read existing log data or initialize empty list
        if log_path.exists():
            with open(log_path, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []
        
        # Append new data
        log_data.append(input_data)
        
        # Write back to file with formatting
        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        sys.exit(0)
        
    except json.JSONDecodeError:
        sys.exit(0)
    except Exception:
        sys.exit(0)

if __name__ == '__main__':
    main()