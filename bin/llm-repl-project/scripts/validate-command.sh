#!/bin/bash
# Command validation script for Claude Code hooks
# Validates commands and blocks potentially problematic ones

# Read JSON input from stdin
INPUT=$(cat)

# Extract command from tool_input
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)

# If we can't extract command from JSON, fall back to command line args
if [ -z "$COMMAND" ]; then
    COMMAND="$1"
fi

# Exit with decision JSON
approve() {
    exit 0
}

block() {
    local reason="$1"
    echo "$reason" >&2
    exit 2
}

# Check for raw pytest commands (force use of "just test")
if echo "$COMMAND" | grep -qE '(pdm run pytest|poetry run pytest|python -m pytest|^pytest)'; then
    # Allow help/info commands
    if echo "$COMMAND" | grep -qE '(--collect-only|--help|--version)'; then
        approve
    else
        block "Raw pytest commands are not allowed. Use \"just test\" to run the full test suite including linting, formatting, and comprehensive validation. This ensures all quality checks pass."
    fi
fi

# Check for GUI applications that would crash Claude Code
if echo "$COMMAND" | grep -qE 'python.*-m.*src\.main|pdm run.*src\.main|poetry run.*src\.main|just run|just run-mixed|just run-fast'; then
    block "GUI applications cannot be run in Claude Code environment. This would crash the interface. Please notify the user to run the app manually."
fi

# Check for dangerous commands
if echo "$COMMAND" | grep -qE '^(sudo|rm -rf|:(){ :|:& };:)'; then
    block "Potentially dangerous command detected. Please use caution."
fi

# Check for other banned patterns
case "$COMMAND" in
    *"pip install --force-reinstall"*)
        block "Force reinstalls can break the environment. Use regular pip install or pdm add."
        ;;
    *"rm -rf /"*)
        block "Recursive deletion of root directory is not allowed."
        ;;
    *"chmod 777"*)
        block "Setting 777 permissions is a security risk. Use more restrictive permissions."
        ;;
    *"wget"*"sudo"*|*"curl"*"sudo"*)
        block "Downloading and executing with sudo is dangerous. Review the script first."
        ;;
esac

# Default: approve
approve