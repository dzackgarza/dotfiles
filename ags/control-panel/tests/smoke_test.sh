#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

ags quit 2>/dev/null || true

# Run for 30s — long enough for all polls to fire at least once
output=$(timeout 30 ags run . 2>&1) || true

# Assert no error-level logs
if echo "$output" | grep -q '\[ERR\]'; then
    echo "FAIL: error logs detected"
    echo "$output" | grep '\[ERR\]'
    exit 1
fi

# Assert updates poll completed (started + finished)
if ! echo "$output" | grep -q 'updates.*refresh starting'; then
    echo "FAIL: updates poll never started"
    exit 1
fi
if ! echo "$output" | grep -qE 'updates.*(refresh OK|refresh FAILED)'; then
    echo "FAIL: updates poll started but never completed"
    exit 1
fi

echo "PASS: no error logs in 30s window, updates poll completed"
exit 0
