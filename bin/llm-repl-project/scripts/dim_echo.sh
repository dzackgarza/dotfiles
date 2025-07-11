#!/bin/bash
# Simple script to print dimmed text using tput

# Check if tput is available and terminal supports dim
if command -v tput >/dev/null 2>&1 && tput dim >/dev/null 2>&1; then
    # Use tput to set dim mode
    echo "$(tput dim)$*$(tput sgr0)"
else
    # Fallback to plain echo
    echo "$*"
fi