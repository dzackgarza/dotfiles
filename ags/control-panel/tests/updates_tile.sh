#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

ags quit 2>/dev/null || true

# Run for 30s to give the updates poll time to fire
output=$(timeout 30 ags run . 2>&1) || true

# Must see the poll fire
if ! echo "$output" | grep -q 'updates.*refresh starting'; then
    echo "FAIL: updates poll never started"
    exit 1
fi

# Must see completion (OK or FAILED)
if ! echo "$output" | grep -q 'updates.*refresh \(OK\|FAILED\)'; then
    echo "FAIL: updates poll started but never completed"
    exit 1
fi

# Must not have error-level logs from the updates reader
if echo "$output" | grep 'updates' | grep -q '\[ERR\]'; then
    echo "FAIL: updates poll logged errors"
    exit 1
fi

echo "PASS: updates poll completed"
exit 0
