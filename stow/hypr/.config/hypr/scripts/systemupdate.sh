#!/bin/bash

# Simply delegate to the Python version which handles JSON properly
SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPTS_DIR/systemupdate.py"

if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Error: Python script not found at $PYTHON_SCRIPT"
    exit 1
fi

python3 "$PYTHON_SCRIPT" "$@"