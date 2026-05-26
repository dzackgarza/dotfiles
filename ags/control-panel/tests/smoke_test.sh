#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

ags quit 2>/dev/null || true

# Run for 15s, capture output
output=$(timeout 15 ags run . 2>&1) || true

if echo "$output" | grep -q '\[ERR\]'; then
    echo "FAIL: error logs detected"
    echo "$output" | grep '\[ERR\]'
    exit 1
fi

echo "PASS: no error logs in 15s window"
exit 0
