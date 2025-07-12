#!/bin/bash
# Debug script to see what Claude Code sends to hooks

echo "=== DEBUG HOOK CALLED ===" >&2
echo "Arguments: $@" >&2
echo "Stdin content:" >&2
cat >&2
echo "=== END DEBUG ===" >&2

# Always approve for now
echo '{"decision": "approve"}'