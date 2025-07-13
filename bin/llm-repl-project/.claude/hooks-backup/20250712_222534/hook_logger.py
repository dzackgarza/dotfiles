#!/usr/bin/env python3
"""
Simple logging utility for hooks to prove they're running
"""

import os
from datetime import datetime
from pathlib import Path

def log_hook_execution(hook_name: str, tool_name: str, decision: str, message: str = ""):
    """Log hook execution to prove hooks are running"""
    log_dir = Path("/home/dzack/dotfiles/bin/llm-repl-project/.claude/hooks/logs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / "hook_execution.log"
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] HOOK: {hook_name} | TOOL: {tool_name} | DECISION: {decision}"
    
    if message:
        log_entry += f" | MESSAGE: {message[:100]}..."
    
    log_entry += "\n"
    
    # Append to log file
    with open(log_file, 'a') as f:
        f.write(log_entry)
    
    # Also create a recent activity file for easy checking
    recent_file = log_dir / "last_hook_activity.txt"
    with open(recent_file, 'w') as f:
        f.write(f"Last hook: {hook_name}\n")
        f.write(f"Time: {timestamp}\n")
        f.write(f"Tool: {tool_name}\n")
        f.write(f"Decision: {decision}\n")
        if message:
            f.write(f"Message: {message}\n")