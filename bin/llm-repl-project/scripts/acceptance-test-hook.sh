#!/bin/bash
# /home/dzack/dotfiles/bin/llm-repl-project/scripts/acceptance-test-hook.sh
#
# Mandatory Acceptance Testing Hook
# Ensures test-first development: No code without failing test

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Project root
PROJECT_ROOT="/home/dzack/dotfiles/bin/llm-repl-project"
VENV_PATH="$PROJECT_ROOT/.venv/bin/activate"

# Function to derive test path from source path
derive_test_path() {
    local src_file="$1"
    # Convert src/widgets/chat.py -> tests/test_chat.py
    # Convert src/core/processor.py -> tests/test_processor.py
    local test_dir="tests"
    local base_name=$(basename "$src_file" .py)
    echo "${test_dir}/test_${base_name}.py"
}

# Function to check if file is testable source code
is_testable_source() {
    local file="$1"
    # Check if it's a Python source file in src/
    if [[ $file =~ ^src/.*\.py$ ]] && [[ ! $file =~ ^tests/ ]] && [[ ! $file =~ __pycache__ ]]; then
        # Skip __init__.py files
        if [[ $(basename "$file") == "__init__.py" ]]; then
            return 1
        fi
        return 0
    fi
    return 1
}

# Function to run a specific test
run_test() {
    local test_file="$1"
    cd "$PROJECT_ROOT/V3-minimal"
    source "$VENV_PATH"
    pdm run pytest "$test_file" -xvs >/dev/null 2>&1
    return $?
}

# Function to provide helpful error messages
show_test_creation_help() {
    local feature_name="$1"
    local test_file="$2"
    
    cat << EOF

${RED}🚫 BLOCKED: Test-First Development Required${NC}

${YELLOW}No test found at: $test_file${NC}

You must create a failing acceptance test BEFORE implementing code.

${GREEN}Quick Start:${NC}
1. Create the test file:
   ${GREEN}touch $PROJECT_ROOT/V3-minimal/$test_file${NC}

2. Write a failing test that defines the behavior:
   ${GREEN}cat > $PROJECT_ROOT/V3-minimal/$test_file << 'TEST'${NC}
import pytest
from textual.testing import AppTest
from src.main import LLMReplApp

@pytest.mark.asyncio
async def test_${feature_name}_user_interaction():
    """Test that user can interact with ${feature_name}."""
    async with LLMReplApp().run_test() as pilot:
        # Define the user interaction you want to work
        # This test should FAIL until you implement the feature
        await pilot.press("tab")  # Example interaction
        
        # Verify user-observable behavior
        # Example: assert something the user would see
        assert False, "Test not implemented - define desired behavior"
TEST

3. Verify the test fails:
   ${GREEN}just verify-failing $test_file${NC}

4. NOW you can implement the feature to make the test pass.

${YELLOW}Remember: The test IS the specification!${NC}
EOF
}

# Main validation logic
validate_files() {
    local blocked=false
    
    for file in $CLAUDE_FILE_PATHS; do
        # Skip if not testable source
        if ! is_testable_source "$file"; then
            continue
        fi
        
        # Get relative path for cleaner output
        local rel_file="${file#$PROJECT_ROOT/}"
        
        echo -e "\n${YELLOW}Checking test-first compliance for: $rel_file${NC}"
        
        # Derive test file path
        local test_file=$(derive_test_path "$file")
        local full_test_path="$PROJECT_ROOT/V3-minimal/$test_file"
        
        # Check if test exists
        if [[ ! -f "$full_test_path" ]]; then
            local feature_name=$(basename "$file" .py)
            show_test_creation_help "$feature_name" "$test_file"
            blocked=true
            continue
        fi
        
        echo -e "${GREEN}✓ Test file exists: $test_file${NC}"
        
        # Run the test
        echo -e "${YELLOW}Running test to ensure it's failing...${NC}"
        
        if run_test "$test_file"; then
            # Test passed - this is bad!
            cat << EOF

${RED}🚫 BLOCKED: Test is already passing!${NC}

File: $rel_file
Test: $test_file

${YELLOW}This violates test-first development because:${NC}
1. The test is already passing, so it's not driving new development
2. You're trying to change code without a failing test to guide you

${GREEN}To fix this:${NC}
1. Modify the test to expect the NEW behavior you want
2. Ensure the test FAILS with current implementation
3. Then implement the code to make it pass

${YELLOW}Example test modification:${NC}
# Add a new assertion for the behavior you're adding:
assert "new_feature" in result  # This should fail first!
EOF
            blocked=true
        else
            # Test failed - this is good!
            echo -e "${GREEN}✓ Test is properly failing - implementation allowed${NC}"
        fi
    done
    
    if [[ "$blocked" == "true" ]]; then
        echo -e "\n${RED}═══════════════════════════════════════${NC}" >&2
        echo -e "${RED}Test-First Development Enforcement Active${NC}" >&2
        echo -e "${RED}═══════════════════════════════════════${NC}" >&2
        echo -e "${RED}BLOCKED: Test-First Development Required${NC}" >&2
        echo -e "${RED}No failing test exists for this code.${NC}" >&2
        echo -e "${RED}Create a failing acceptance test before implementing.${NC}" >&2
        # Exit with code 2 to BLOCK the tool execution
        exit 2
    fi
}

# Handle the case when called by Claude Code hooks
if [[ -n "${CLAUDE_FILE_PATHS:-}" ]]; then
    validate_files
else
    # Manual testing mode
    if [[ $# -eq 0 ]]; then
        echo "Usage: $0 <file1> [file2] ..."
        echo "Or set CLAUDE_FILE_PATHS environment variable"
        exit 1
    fi
    
    export CLAUDE_FILE_PATHS="$*"
    validate_files
fi

# Return success JSON for Claude Code if not blocked
if [[ -n "${CLAUDE_FILE_PATHS:-}" ]]; then
    echo '{"decision": "approve"}'
fi

exit 0
