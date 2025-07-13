#!/usr/bin/env python3

import json
import os
import sys
import subprocess
from pathlib import Path

def get_complexity_indicator():
    """Check if recent changes indicate high complexity (simple LOC count)"""
    try:
        result = subprocess.run(['git', 'diff', '--stat'], 
                              capture_output=True, text=True, timeout=2)
        if result.returncode == 0:
            # Look for large changesets in git diff output
            return "100+" in result.stdout or "200+" in result.stdout
    except:
        pass
    return False

def main():
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)
        
        # PROPORTIONALITY CHECK - Alert on large changesets
        if get_complexity_indicator():
            print("📊 Large changeset detected. Is this proportional to the task?", file=sys.stderr)
            print("🤔 Could this have been simpler?", file=sys.stderr)
        
        # Ensure log directory exists
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
        # Handle JSON decode errors gracefully
        sys.exit(0)
    except Exception:
        # Exit cleanly on any other error
        sys.exit(0)

if __name__ == '__main__':
    main()