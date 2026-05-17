#!/bin/bash
# Test runner that forces the use of Sage's Python

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if sage is available
if ! command -v sage &> /dev/null; then
    echo "Error: Sage is not available. Please install Sage or add it to your PATH."
    exit 1
fi

# Export PYTHONPATH to include the package directory
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

# Run the test suite using Sage's Python
sage -python -m tests.test_suite "$@"
