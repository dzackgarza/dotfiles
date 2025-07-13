# Unified Logging Configuration

The hooks now use a unified logging module (`utils/common_logger.py`) that provides consistent logging across all hook types.

## Features

### Automatic Enrichment
- **Timestamps**: All log entries include ISO 8601 timestamps
- **Hook Type**: Each entry is tagged with the hook type that created it
- **Enhanced Security Logging**: Security blocks include detailed context

### Environment Configuration
Configure logging behavior via environment variables:

```bash
# Enable console logging (logs to stdout in addition to files)
export CLAUDE_HOOKS_CONSOLE_LOG=true

# Set log level (currently for future use)
export CLAUDE_HOOKS_LOG_LEVEL=debug

# Enable log rotation
export CLAUDE_HOOKS_ROTATE_LOGS=true

# Set maximum log entries per file (default: 1000)
export CLAUDE_HOOKS_MAX_LOG_ENTRIES=500
```

### Log Format

#### Standard Events
```json
{
  "tool_name": "Write",
  "tool_input": {"file_path": "test.txt", "content": "test"},
  "_timestamp": "2025-07-12T22:35:23.323867",
  "_hook_type": "pre_tool_use"
}
```

#### Security Blocks
```json
{
  "security_block": true,
  "reason": "Dangerous rm command detected and prevented",
  "blocked_data": {
    "tool_name": "Bash",
    "tool_input": {"command": "rm -rf /"}
  },
  "_timestamp": "2025-07-12T22:35:34.009988",
  "_hook_type": "pre_tool_use"
}
```

#### Error Events
```json
{
  "error": "Failed to export chat transcript: Permission denied",
  "data": {"transcript_path": "/path/to/transcript.jsonl"},
  "_timestamp": "2025-07-12T22:35:45.123456",
  "_hook_type": "stop"
}
```

## Future Extensions

The logging module is designed for easy extension:

1. **Log Levels**: Filter logs by severity
2. **Remote Logging**: Send logs to external services
3. **Log Rotation**: Automatic cleanup of old logs
4. **Custom Formatters**: Support for different output formats
5. **Structured Filtering**: Query logs by hook type, time range, etc.

## Migration Benefits

- **Centralized Configuration**: Change logging behavior for all hooks in one place
- **Consistent Format**: All hooks follow the same logging structure
- **Enhanced Debugging**: Timestamps and context make troubleshooting easier
- **Security Auditing**: Detailed logging of blocked operations
- **Future-Proof**: Easy to add new logging features without updating individual hooks