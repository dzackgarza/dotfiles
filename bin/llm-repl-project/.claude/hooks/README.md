# Claude Code Hooks - Project Specific Implementation

This directory contains Claude Code hooks customized for this project's workflow and requirements.

## Hook Architecture

These hooks extend the canonical Claude Code hook patterns found in:
```
.claude/claude-code-hooks-mastery/.claude/hooks/
```

**Canonical hooks** provide the basic patterns for:
- JSON input/output handling via stdin/stdout
- Logging to `logs/` directory  
- Error handling with graceful exits
- Communication with Claude via stderr and exit codes

**These project hooks** extend the canonical patterns with:
- Direct confrontational questioning to force verification
- TDD workflow enforcement
- Security validation beyond basic rm/env protection
- Task Master integration and accountability

## Hook Communication Methods

All hooks follow the canonical communication patterns:

### Exit Code 2 + stderr
- **PreToolUse**: Blocks tool execution, stderr shown to Claude
- **PostToolUse**: Cannot block (tool already ran), stderr shown to Claude  
- **Stop**: Blocks stopping, stderr shown to Claude (forces continuation)

### JSON Output + Exit Code 0
Advanced control via stdout JSON with fields like:
- `{"decision": "block", "reason": "explanation"}`
- `{"continue": false, "stopReason": "reason"}`

### No Communication (Exit Code 0, no stderr)
- Normal completion with logging only

## Project-Specific Extensions

### Direct Confrontational Hooks
Based on observed patterns that work in conversation:
- "Really? Did you actually test this?"
- "Do you have any evidence that this code works?"
- "If I ran 'just run' right now, would I see anything working?"

### TDD Enforcement
- Blocks `task-master set-status --status=done` without proof
- Challenges fake temporal grid generation
- Forces verification before task completion

### Security Validation
Extends canonical security with:
- Package manager usage blocking
- Sudo command prevention
- Network exposure detection
- Textual GUI app launch blocking (forces proper testing workflow)

## File Structure

```
.claude/hooks/
├── README.md                 # This file
├── pre_tool_use.py          # Security + direct challenges before tools
├── post_tool_use.py         # Direct confrontation after tools  
├── stop.py                  # Accountability questioning before stopping
├── notification.py          # TTS notifications (from canonical)
├── subagent_stop.py         # Subagent completion (from canonical)
├── tdd-enforcement.py       # Fake temporal grid detection
└── utils/                   # Utility scripts
    ├── common_logger.py     # Logging utilities
    ├── tts/                 # Text-to-speech providers
    └── llm/                 # Language model integrations
```

## Key Principles

1. **Follow canonical patterns** for JSON handling and communication
2. **Extend with project needs** rather than replacing core functionality
3. **Use proven confrontational techniques** that force verification
4. **Log everything** for debugging and accountability
5. **Fail gracefully** to avoid breaking Claude Code execution
6. **Use absolute paths** to avoid issues with working directory changes

## Path Handling

**Important**: These hooks run from `/path/to/project/.claude/hooks/` but may need to reference files in the project root or other directories. Always use absolute paths:

```python
# Get project root (parent of .claude)
project_root = Path.cwd().parent.parent  # From .claude/hooks/ to project root

# Reference project files
ai_memories = project_root / ".ai" / "memories"
task_master_config = project_root / ".taskmaster" / "config.json"
```

This prevents "pathspec not found" and "beyond symbolic link" errors when git operations or file references are made from hook context.

## Reference

- **Canonical hooks**: `.claude/claude-code-hooks-mastery/.claude/hooks/`
- **Hook documentation**: `.claude/claude-code-hooks-mastery/README.md`
- **Claude Code hooks docs**: https://docs.anthropic.com/en/docs/claude-code/hooks