#!/bin/bash
# Check hook execution logs

LOG_DIR="/home/dzack/dotfiles/bin/llm-repl-project/.claude/hooks/logs"

echo "=== HOOK EXECUTION LOG ==="
echo

if [ -f "$LOG_DIR/last_hook_activity.txt" ]; then
    echo "--- Last Hook Activity ---"
    cat "$LOG_DIR/last_hook_activity.txt"
    echo
fi

if [ -f "$LOG_DIR/hook_execution.log" ]; then
    echo "--- Recent Hook Executions (last 20) ---"
    tail -n 20 "$LOG_DIR/hook_execution.log"
    echo
    echo "--- Hook Execution Summary ---"
    echo "Total executions: $(wc -l < "$LOG_DIR/hook_execution.log")"
    echo "Unique hooks run: $(awk -F'|' '{print $1}' "$LOG_DIR/hook_execution.log" | awk -F': ' '{print $2}' | sort | uniq | wc -l)"
    echo
    echo "--- Hook Frequency ---"
    awk -F'|' '{print $1}' "$LOG_DIR/hook_execution.log" | awk -F': ' '{print $2}' | sort | uniq -c | sort -nr
else
    echo "No hook execution log found yet."
    echo "Hooks will log to: $LOG_DIR/hook_execution.log"
fi