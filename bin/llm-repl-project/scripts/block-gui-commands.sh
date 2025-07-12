#!/bin/bash
# Block GUI commands for Claude Code sessions
# Source this file to prevent Claude from running GUI apps

# Block common Python GUI execution patterns that Claude uses
alias "python -m src.main"="echo '🚫 GUI BLOCKED: Use pilot tests instead of running the GUI app'"
alias "pdm run python -m src.main"="echo '🚫 GUI BLOCKED: Use pilot tests instead of running the GUI app'"
alias "python src/main.py"="echo '🚫 GUI BLOCKED: Use pilot tests instead of running the GUI app'"
alias "pdm run python src/main.py"="echo '🚫 GUI BLOCKED: Use pilot tests instead of running the GUI app'"

# Block just commands that start GUI
function just() {
    if [[ "$1" == "run" || "$1" == "run-fast" || "$1" == "run-dev" ]]; then
        echo "🚫 GUI BLOCKED: 'just $1' would start the GUI app"
        echo "💡 ALTERNATIVE: Use 'just test' or write pilot tests to verify functionality"
        echo "📝 REMEMBER: Test with pilot tests, not by running the actual GUI"
        return 1
    else
        command just "$@"
    fi
}

# Block direct textual app execution
alias textual="echo '🚫 GUI BLOCKED: Use pilot tests instead of running textual apps'"

# Create a pilot test helper
function pilot() {
    echo "📝 PILOT TEST HELPER:"
    echo "1. Create a test file that imports and calls your functions"
    echo "2. Test the logic without starting the GUI"
    echo "3. Take screenshots of working GUI state for verification"
    echo ""
    echo "Example:"
    echo "  # Create test_pilot.py"
    echo "  # Import your functions and test them"
    echo "  # Use existing debug_screenshots for visual proof"
}

echo "✅ GUI commands blocked for Claude Code session"
echo "💡 Use 'pilot' command for testing guidance"