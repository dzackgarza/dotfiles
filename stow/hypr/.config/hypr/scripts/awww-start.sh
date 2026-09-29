#!/usr/bin/env bash

set -euo pipefail

if awww query >/dev/null 2>&1; then
    exit 0
fi

awww-daemon >/dev/null 2>&1 &

for _ in {1..50}; do
    if awww query >/dev/null 2>&1; then
        exit 0
    fi
    sleep 0.1
done

printf '%s\n' "awww daemon did not become ready" >&2
exit 1
