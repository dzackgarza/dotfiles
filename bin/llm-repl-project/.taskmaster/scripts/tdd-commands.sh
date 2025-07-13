#!/bin/bash
"""
TDD Command Integration Scripts

These scripts bridge the gap between Task Master CLI and our TDD implementation,
providing the actual commands that Task Master CLI expects to find.
"""

# Get the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TDD_COMMANDS_SCRIPT="$PROJECT_ROOT/V3-minimal/src/tdd_integration/tdd_commands.py"

# Function to check if we're in the right directory
check_project_root() {
    if [[ ! -f "$TDD_COMMANDS_SCRIPT" ]]; then
        echo "Error: TDD commands script not found at $TDD_COMMANDS_SCRIPT"
        echo "Make sure you're running from the project root"
        exit 1
    fi
}

# Function to run TDD command with proper error handling
run_tdd_command() {
    check_project_root
    
    cd "$PROJECT_ROOT/V3-minimal"
    python "$TDD_COMMANDS_SCRIPT" "$@"
    local exit_code=$?
    
    if [[ $exit_code -ne 0 ]]; then
        echo "TDD command failed with exit code $exit_code" >&2
    fi
    
    return $exit_code
}

# Parse command and arguments
COMMAND="$1"
shift

case "$COMMAND" in
    "generate-story")
        run_tdd_command generate-story "$@"
        ;;
    "test-story")
        run_tdd_command test-story "$@"
        ;;
    "update-story")
        run_tdd_command update-story "$@"
        ;;
    "validate-task")
        run_tdd_command validate-task "$@"
        ;;
    "complete-with-story")
        run_tdd_command complete-with-story "$@"
        ;;
    "list-stories")
        run_tdd_command list-stories "$@"
        ;;
    *)
        echo "Usage: $0 {generate-story|test-story|update-story|validate-task|complete-with-story|list-stories} [options]"
        echo ""
        echo "Available commands:"
        echo "  generate-story --id=<task> --prompt='<description>'"
        echo "  test-story --id=<task>"  
        echo "  update-story --id=<task> --grid-path=<path>"
        echo "  validate-task --id=<task> [--require-story]"
        echo "  complete-with-story --id=<task> [--story-id=<story>]"
        echo "  list-stories"
        exit 1
        ;;
esac