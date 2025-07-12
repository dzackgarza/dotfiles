#!/bin/bash
# Screenshot Reality Check Hook
# Ensures tests are grounded in actual observable behavior

set -euo pipefail

PROJECT_ROOT="/home/dzack/dotfiles/bin/llm-repl-project"
REALITY_CHECK_FILE="$PROJECT_ROOT/V3-minimal/CURRENT-REALITY.md"

# Function to check if test file has reality documentation
check_reality_grounding() {
    local test_file="$1"
    
    # Look for reality markers in test file
    if grep -q "# REALITY:" "$test_file" 2>/dev/null; then
        return 0
    fi
    
    # Check if CURRENT-REALITY.md exists and is recent (< 1 hour old)
    if [[ -f "$REALITY_CHECK_FILE" ]]; then
        local age_minutes=$(( ($(date +%s) - $(stat -c %Y "$REALITY_CHECK_FILE" 2>/dev/null || stat -f %m "$REALITY_CHECK_FILE" 2>/dev/null || echo 0)) / 60 ))
        if [[ $age_minutes -lt 60 ]]; then
            return 0
        fi
    fi
    
    return 1
}

# For PreToolUse on test files
if [[ "${CLAUDE_HOOK_TYPE:-}" == "PreToolUse" ]]; then
    for file in $CLAUDE_FILE_PATHS; do
        if [[ $file =~ test_.*\.py$ ]]; then
            if ! check_reality_grounding "$file"; then
                cat << EOF
🚫 REALITY CHECK REQUIRED

Test file: $file

You must document ACTUAL observable behavior before writing tests.

Add to your test file:
\`\`\`python
# REALITY: Screenshot taken at [timestamp]
# - User types "hello" → Shows "hello" with no formatting
# - No borders or titles visible
# - Turn separator appears BEFORE user message
# - Cognition block shows raw text "Processed through cognition pipeline"
# - Large whitespace gaps between elements
\`\`\`

Or update $REALITY_CHECK_FILE with current screenshot observations.

This prevents fantasy testing by anchoring tests to observed reality.
EOF
                echo '{"decision": "block", "reason": "Tests must be grounded in documented reality (screenshot observations)"}'
                exit 0
            fi
        fi
    done
fi

echo '{"decision": "approve"}'