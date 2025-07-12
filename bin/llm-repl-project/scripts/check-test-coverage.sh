#!/bin/bash
# Check which source files lack corresponding test files

cd V3-minimal || exit 1

echo "Source files without tests:"
found_missing=0

find src -name "*.py" -type f | while read -r src_file; do
    basename_file=$(basename "$src_file")
    
    # Skip __init__.py files
    if [[ "$basename_file" == "__init__.py" ]]; then
        continue
    fi
    
    # Derive test filename
    test_name="test_${basename_file}"
    test_file="tests/${test_name}"
    
    # Check if test exists
    if [[ ! -f "$test_file" ]]; then
        echo "  ❌ $src_file (missing $test_file)"
        found_missing=1
    fi
done

echo ""
echo "Remember: Every feature needs a failing test first!"