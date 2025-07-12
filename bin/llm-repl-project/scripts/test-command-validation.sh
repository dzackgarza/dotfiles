#!/bin/bash
# Test script for command validation

SCRIPT_PATH="/home/dzack/dotfiles/bin/llm-repl-project/scripts/validate-command.sh"

echo "Testing Claude Code command validation..."
echo

# Test 1: Raw pytest should be blocked
echo "Test 1: Raw pytest command"
result=$(echo '{"tool_input": {"command": "pdm run pytest tests/"}}' | $SCRIPT_PATH)
if echo "$result" | grep -q '"decision": "block"'; then
    echo "✅ PASS: Raw pytest blocked"
else
    echo "❌ FAIL: Raw pytest not blocked"
    echo "Result: $result"
fi
echo

# Test 2: pytest --help should be allowed
echo "Test 2: Pytest help command"
result=$(echo '{"tool_input": {"command": "pytest --help"}}' | $SCRIPT_PATH)
if echo "$result" | grep -q '"decision": "approve"'; then
    echo "✅ PASS: Pytest help allowed"
else
    echo "❌ FAIL: Pytest help blocked"
    echo "Result: $result"
fi
echo

# Test 3: just test should be allowed
echo "Test 3: Just test command"
result=$(echo '{"tool_input": {"command": "just test"}}' | $SCRIPT_PATH)
if echo "$result" | grep -q '"decision": "approve"'; then
    echo "✅ PASS: Just test allowed"
else
    echo "❌ FAIL: Just test blocked"
    echo "Result: $result"
fi
echo

# Test 4: GUI apps should be blocked
echo "Test 4: GUI application"
result=$(echo '{"tool_input": {"command": "python -m src.main"}}' | $SCRIPT_PATH)
if echo "$result" | grep -q '"decision": "block"'; then
    echo "✅ PASS: GUI app blocked"
else
    echo "❌ FAIL: GUI app not blocked"
    echo "Result: $result"
fi
echo

# Test 5: Dangerous commands should be blocked
echo "Test 5: Dangerous command"
result=$(echo '{"tool_input": {"command": "sudo rm -rf /"}}' | $SCRIPT_PATH)
if echo "$result" | grep -q '"decision": "block"'; then
    echo "✅ PASS: Dangerous command blocked"
else
    echo "❌ FAIL: Dangerous command not blocked"
    echo "Result: $result"
fi
echo

# Test 6: Normal commands should be allowed
echo "Test 6: Normal command"
result=$(echo '{"tool_input": {"command": "ls -la"}}' | $SCRIPT_PATH)
if echo "$result" | grep -q '"decision": "approve"'; then
    echo "✅ PASS: Normal command allowed"
else
    echo "❌ FAIL: Normal command blocked"
    echo "Result: $result"
fi
echo

echo "Command validation testing complete!"