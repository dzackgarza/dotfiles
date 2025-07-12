#!/bin/bash
# Visual Memory Hook - Ensures tests match observable reality
# Prevents fantasy testing by requiring screenshot evidence

set -euo pipefail

PROJECT_ROOT="/home/dzack/dotfiles/bin/llm-repl-project"
SCREENSHOTS_DIR="$PROJECT_ROOT/V3-minimal/debug_screenshots"
VISUAL_MEMORY="$PROJECT_ROOT/V3-minimal/VISUAL-MEMORY.md"

# Ensure directories exist
mkdir -p "$SCREENSHOTS_DIR"

# Function to capture screenshot
capture_screenshot() {
    local feature_name="$1"
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local screenshot_path="$SCREENSHOTS_DIR/${feature_name}_${timestamp}.png"
    
    # Use gnome-screenshot, scrot, or maim depending on what's available
    if command -v gnome-screenshot &> /dev/null; then
        gnome-screenshot -f "$screenshot_path" 2>/dev/null || true
    elif command -v scrot &> /dev/null; then
        scrot "$screenshot_path" 2>/dev/null || true
    elif command -v maim &> /dev/null; then
        maim "$screenshot_path" 2>/dev/null || true
    fi
    
    echo "$screenshot_path"
}

# Function to update visual memory
update_visual_memory() {
    local screenshot_path="$1"
    local test_file="$2"
    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    
    # Append to visual memory log
    cat >> "$VISUAL_MEMORY" << EOF

## Visual State: $timestamp
**Test File**: $test_file
**Screenshot**: $screenshot_path

### Observable Elements:
- [ ] Document what you can actually see in the screenshot
- [ ] List specific text that appears
- [ ] Note element positions and layout
- [ ] Record any error messages or unexpected behavior

### Test Assertions Must Match:
\`\`\`python
# Your test must check for these EXACT observable elements
# Example: assert "Actual text from screenshot" in output
\`\`\`

---
EOF
}

# For PreToolUse: Check if we have visual evidence
if [[ "${CLAUDE_HOOK_TYPE:-}" == "PreToolUse" ]]; then
    for file in $CLAUDE_FILE_PATHS; do
        if [[ $file =~ test_.*\.py$ ]]; then
            # Extract feature name from test file
            feature_name=$(basename "$file" .py | sed 's/test_//')
            
            # Check if we have recent screenshot for this feature
            recent_screenshot=$(find "$SCREENSHOTS_DIR" -name "${feature_name}_*.png" -mtime -1 | head -1)
            
            if [[ -z "$recent_screenshot" ]]; then
                echo "⚠️  No recent screenshot found for $feature_name"
                echo "📸 Please provide a screenshot showing the actual behavior you're testing"
                echo '{"decision": "warn", "reason": "No visual evidence for test assertions"}'
            fi
        fi
    done
fi

# For PostToolUse: After running tests, remind to capture visual state
if [[ "${CLAUDE_HOOK_TYPE:-}" == "PostToolUse" ]]; then
    echo "💡 Remember to capture screenshots of actual app behavior"
    echo "   This prevents fantasy tests that don't match reality"
fi

echo '{"decision": "approve"}'