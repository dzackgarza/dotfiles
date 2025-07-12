#!/bin/bash
# Test script for code review hook

SCRIPT_PATH="/home/dzack/dotfiles/bin/llm-repl-project/scripts/code-review-hook.sh"
PROJECT_ROOT="/home/dzack/dotfiles/bin/llm-repl-project"

echo "Testing Code Review Hook..."
echo

# Test 1: Python file review
echo "Test 1: Python file review"
export CLAUDE_FILE_PATHS="$PROJECT_ROOT/V3-minimal/src/main.py"
$SCRIPT_PATH
echo

# Test 2: CSS file review  
echo "Test 2: CSS/TCSS file review"
export CLAUDE_FILE_PATHS="$PROJECT_ROOT/V3-minimal/src/theme.tcss"
$SCRIPT_PATH
echo

# Test 3: Multiple files
echo "Test 3: Multiple file review"
export CLAUDE_FILE_PATHS="$PROJECT_ROOT/V3-minimal/src/main.py $PROJECT_ROOT/V3-minimal/src/widgets/chatbox.tcss"
$SCRIPT_PATH
echo

# Test 4: JSON file
echo "Test 4: JSON file review"
export CLAUDE_FILE_PATHS="$PROJECT_ROOT/.claude/settings.json"
$SCRIPT_PATH
echo

# Test 5: Non-existent file (should handle gracefully)
echo "Test 5: Non-existent file"
export CLAUDE_FILE_PATHS="/non/existent/file.py"
$SCRIPT_PATH
echo

# Test 6: No files specified
echo "Test 6: No files specified"
unset CLAUDE_FILE_PATHS
$SCRIPT_PATH

echo "Code review hook testing complete!"