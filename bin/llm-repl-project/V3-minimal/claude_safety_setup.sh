#!/bin/bash
# Claude Code Safety Setup
# Prevents accidental GUI app launches that corrupt the interface

echo "🛡️  Setting up Claude Code safety aliases..."

# Alias main app to safe version
alias main-app='echo "❌ ERROR: Cannot run GUI app in Claude Code! Use manual terminal instead."'
alias run-app='echo "❌ ERROR: Cannot run GUI app in Claude Code! Use manual terminal instead."'

# Alias demo scripts to safe versions  
alias live-demo='echo "❌ ERROR: Cannot run live demo in Claude Code! Test with unit tests instead."'
alias scenario-demo='echo "❌ ERROR: Cannot run scenario demo in Claude Code! Test with unit tests instead."'

# Alias python module runs that could be GUI
alias python-main='echo "❌ ERROR: Use pytest for testing, not direct python runs!"'

# Override common dangerous patterns
function pdm() {
    if [[ "$*" == *"run python -m src.main"* ]]; then
        echo "❌ ERROR: Cannot run GUI app in Claude Code environment!"
        echo "This would corrupt the Claude Code interface."
        echo "Run this command manually in a separate terminal."
        return 1
    elif [[ "$*" == *"run python src/main.py"* ]]; then
        echo "❌ ERROR: Cannot run GUI app in Claude Code environment!"
        return 1
    elif [[ "$*" == *"run python"* ]] && [[ "$*" == *"demo"* ]]; then
        echo "❌ ERROR: Cannot run demo apps in Claude Code environment!"
        return 1
    else
        # Safe to run - pass through to real pdm
        command pdm "$@"
    fi
}

# Override python command for main module
function python() {
    if [[ "$*" == *"-m src.main"* ]] || [[ "$*" == *"src/main.py"* ]]; then
        echo "❌ ERROR: Cannot run GUI app in Claude Code environment!"
        echo "This would corrupt the Claude Code interface."
        return 1
    elif [[ "$*" == *"demo"* ]] && [[ "$*" == *".py"* ]]; then
        echo "❌ ERROR: Cannot run demo apps in Claude Code environment!"
        return 1
    else
        # Safe to run - pass through to real python
        command python "$@"
    fi
}

echo "✅ Claude Code safety aliases active!"
echo "   - GUI app launches are blocked"
echo "   - Demo script runs are blocked"
echo "   - Only pytest and safe commands allowed"
echo ""
echo "💡 To run GUI apps, use a separate terminal outside Claude Code"