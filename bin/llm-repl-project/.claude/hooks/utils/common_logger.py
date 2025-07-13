#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""
Common logging module for Claude Code hooks.
Provides unified logging functionality across all hook types.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime


class HookLogger:
    """Unified logger for Claude Code hooks."""
    
    def __init__(self, hook_type: str, base_dir: Optional[Path] = None):
        """
        Initialize the logger for a specific hook type.
        
        Args:
            hook_type: The type of hook (e.g., 'pre_tool_use', 'post_tool_use')
            base_dir: Base directory for logs (defaults to current working directory)
        """
        self.hook_type = hook_type
        self.base_dir = base_dir or Path.cwd()
        self.log_dir = self.base_dir / 'logs'
        self.log_file = self.log_dir / f'{hook_type}.json'
        
        # Ensure log directory exists
        self.log_dir.mkdir(parents=True, exist_ok=True)
    
    def log_event(self, data: Dict[str, Any]) -> None:
        """
        Log an event to the appropriate log file.
        
        Args:
            data: The event data to log
        """
        try:
            # Add timestamp to the data
            enriched_data = {
                **data,
                '_timestamp': datetime.now().isoformat(),
                '_hook_type': self.hook_type
            }
            
            # Read existing log data or initialize empty list
            if self.log_file.exists():
                with open(self.log_file, 'r') as f:
                    try:
                        log_data = json.load(f)
                        if not isinstance(log_data, list):
                            log_data = []
                    except (json.JSONDecodeError, ValueError):
                        log_data = []
            else:
                log_data = []
            
            # Append new data
            log_data.append(enriched_data)
            
            # Write back to file with formatting
            with open(self.log_file, 'w') as f:
                json.dump(log_data, f, indent=2)
                
        except Exception:
            # Fail silently to avoid breaking hook execution
            pass
    
    def log_error(self, error_msg: str, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Log an error event.
        
        Args:
            error_msg: Error message
            data: Optional additional data
        """
        error_data = {
            'error': error_msg,
            'data': data or {}
        }
        self.log_event(error_data)
    
    def log_security_block(self, reason: str, blocked_data: Dict[str, Any]) -> None:
        """
        Log a security block event.
        
        Args:
            reason: Reason for blocking
            blocked_data: The data that was blocked
        """
        security_data = {
            'security_block': True,
            'reason': reason,
            'blocked_data': blocked_data
        }
        self.log_event(security_data)


def create_logger(hook_type: str) -> HookLogger:
    """
    Factory function to create a logger for a specific hook type.
    
    Args:
        hook_type: The type of hook
        
    Returns:
        Configured HookLogger instance
    """
    return HookLogger(hook_type)


# Configuration for different log formats (extensible for future needs)
class LogConfig:
    """Configuration class for logging behavior."""
    
    @staticmethod
    def should_log_to_console() -> bool:
        """Check if logs should also go to console."""
        return os.getenv('CLAUDE_HOOKS_CONSOLE_LOG', 'false').lower() == 'true'
    
    @staticmethod
    def get_log_level() -> str:
        """Get the log level from environment."""
        return os.getenv('CLAUDE_HOOKS_LOG_LEVEL', 'info').lower()
    
    @staticmethod
    def get_max_log_entries() -> int:
        """Get maximum number of log entries to keep."""
        try:
            return int(os.getenv('CLAUDE_HOOKS_MAX_LOG_ENTRIES', '1000'))
        except ValueError:
            return 1000
    
    @staticmethod
    def should_rotate_logs() -> bool:
        """Check if log rotation is enabled."""
        return os.getenv('CLAUDE_HOOKS_ROTATE_LOGS', 'false').lower() == 'true'


class AdvancedHookLogger(HookLogger):
    """Advanced logger with additional features like rotation and filtering."""
    
    def __init__(self, hook_type: str, base_dir: Optional[Path] = None):
        super().__init__(hook_type, base_dir)
        self.config = LogConfig()
    
    def log_event(self, data: Dict[str, Any]) -> None:
        """Enhanced log_event with rotation and filtering."""
        try:
            # Add timestamp and metadata
            enriched_data = {
                **data,
                '_timestamp': datetime.now().isoformat(),
                '_hook_type': self.hook_type
            }
            
            # Console logging if enabled
            if self.config.should_log_to_console():
                print(f"[{self.hook_type}] {json.dumps(enriched_data, indent=2)}")
            
            # Read existing log data
            if self.log_file.exists():
                with open(self.log_file, 'r') as f:
                    try:
                        log_data = json.load(f)
                        if not isinstance(log_data, list):
                            log_data = []
                    except (json.JSONDecodeError, ValueError):
                        log_data = []
            else:
                log_data = []
            
            # Append new data
            log_data.append(enriched_data)
            
            # Rotate logs if needed
            if self.config.should_rotate_logs():
                max_entries = self.config.get_max_log_entries()
                if len(log_data) > max_entries:
                    log_data = log_data[-max_entries:]
            
            # Write back to file
            with open(self.log_file, 'w') as f:
                json.dump(log_data, f, indent=2)
                
        except Exception:
            # Fail silently
            pass