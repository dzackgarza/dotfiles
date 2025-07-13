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

CURRENT IMPLEMENTATION: Uses stderr messages to challenge Claude with direct questions
================================================================================
"""

import json
import os
import sys
from pathlib import Path

def provide_direct_confrontation(tool_name, tool_input, tool_result):
    """
    Direct confrontational questions that actually work to force verification.
    Based on observed successful patterns of challenging Claude.
    """
    result_text = str(tool_result.get('result', ''))
    
    # Direct challenges after code changes
    if tool_name in ['Edit', 'Write', 'MultiEdit']:
        file_path = tool_input.get('file_path', '')
        if 'src/' in file_path and file_path.endswith(('.py', '.js', '.ts')):
            print("Really? Did you actually test this?", file=sys.stderr)
            print("Do you have any evidence that this code works?", file=sys.stderr)
    
    # Direct challenges after bash commands
    if tool_name == 'Bash':
        command = tool_input.get('command', '')
        
        # Challenge test claims
        if 'test' in command.lower() and 'story' in command.lower():
            if 'success' in result_text.lower() or 'passed' in result_text.lower():
                print("Really? Did that actually test GUI interaction?", file=sys.stderr)
                print("Do you have visual proof that this shows real application behavior?", file=sys.stderr)
        
        # Challenge run commands
        if any(word in command.lower() for word in ['python', 'run', 'pdm', 'just run']):
            if 'error' not in result_text.lower():
                print("Does that really work? Are you sure I'll see something if I run that?", file=sys.stderr)
                print("Did you actually see it working, or are you assuming?", file=sys.stderr)
        
        # Challenge ignored errors
        if 'error' in result_text.lower() or 'failed' in result_text.lower():
            print("That failed. Are you going to fix it or ignore it?", file=sys.stderr)
            print("Really? You're moving on with broken code?", file=sys.stderr)
        
        # Challenge task progression
        if 'task-master' in command and 'next' in command:
            print("Really? Have you actually verified your previous work?", file=sys.stderr)
            print("Do you have any proof the last task actually works?", file=sys.stderr)
    
    # Challenge Task Master completions
    if tool_name.startswith('mcp__taskmaster-ai__'):
        if 'set_task_status' in tool_name and 'done' in str(tool_input):
            print("Really? When did you last see this working?", file=sys.stderr)
            print("Do you have any evidence this task is complete?", file=sys.stderr)

def main():
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)
        
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        tool_result = input_data.get('tool_result', {})
        
        # Provide direct confrontation
        provide_direct_confrontation(tool_name, tool_input, tool_result)
        
        # Simple logging like canonical hooks
        log_dir = Path.cwd() / 'logs'
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