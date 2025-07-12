#!/bin/bash

# GUI Application Blocker Hook
# Prevents Claude Code agents from running GUI applications

# Read the command from jq
COMMAND=$(jq -r '.tool_input.command')

# Comprehensive GUI app detection patterns
GUI_PATTERNS=(
    # Direct GUI app execution
    "python.*-m.*src\.main"
    "pdm run.*python.*-m.*src\.main"
    "pdm run.*src\.main"
    "poetry run.*src\.main"
    "just run"
    "just run-mixed"
    "just run-fast"
    
    # Bypass attempts
    "timeout.*python.*-m.*src\.main"
    "timeout.*pdm run.*src\.main"
    "nohup.*python.*-m.*src\.main"
    "screen.*python.*-m.*src\.main"
    "tmux.*python.*-m.*src\.main"
    
    # GUI frameworks
    "textual run"
    "textual.*dev"
    "tkinter"
    "pyqt"
    "pyside"
    "kivy"
    "pygame"
    "wx"
    "fltk"
    "gtk"
    "qt"
    
    # Common GUI patterns
    ".*main\.py.*gui"
    ".*app\.py.*run"
    ".*\.main\(\)"
    "python.*app\.py"
    
    # X11/Wayland indicators
    "DISPLAY="
    "WAYLAND_DISPLAY="
    "export DISPLAY"
    "xvfb"
    "Xvfb"
)

# Check each pattern
for pattern in "${GUI_PATTERNS[@]}"; do
    if echo "$COMMAND" | grep -qE "$pattern"; then
        echo '{
            "decision": "block", 
            "reason": "🚫 GUI APPLICATIONS BANNED 🚫\n\nPattern detected: '"$pattern"'\nCommand: '"$COMMAND"'\n\nGUI apps break Claude Code interface!\n\n✅ CORRECT APPROACH:\n• Use existing screenshots in debug_screenshots/\n• Analyze code statically\n• Review test outputs\n\n❌ VIOLATION: This breaks CLAUDE.md cardinal rule"
        }'
        exit 0
    fi
done

# Allow the command
echo '{"decision": "approve"}'