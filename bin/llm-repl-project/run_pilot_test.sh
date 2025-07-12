#!/bin/bash
# Pilot test script for LLM REPL V3-minimal
# This script runs the app in a controlled way and captures screenshots

echo "🚀 Starting LLM REPL Pilot Test..."
echo "This will run the app and capture screenshots for review"
echo ""

# Change to project directory
cd "$(dirname "$0")"

# Get initial screenshot count
SCREENSHOT_DIR="V3-minimal/debug_screenshots"
INITIAL_COUNT=$(ls -1 "$SCREENSHOT_DIR"/*.svg 2>/dev/null | wc -l)
echo "📸 Initial screenshots: $INITIAL_COUNT"

# Create a test input file
TEST_INPUT_FILE="pilot_test_input.txt"
cat > "$TEST_INPUT_FILE" << EOF
hello world

test message

what is 2+2?

EOF

echo "📝 Created test input file with commands"

# Run the app with the test input
echo "▶️  Running the app with test input..."
echo "(The app will process commands and then exit)"
echo ""

# Run the app with input redirection and timeout
timeout 30s pdm run python -m V3-minimal.src.main < "$TEST_INPUT_FILE" > pilot_test_output.log 2>&1

# Check the exit status
EXIT_STATUS=$?
if [ $EXIT_STATUS -eq 124 ]; then
    echo "⏱️  App timed out after 30 seconds (this is expected)"
elif [ $EXIT_STATUS -eq 0 ]; then
    echo "✅ App exited normally"
else
    echo "⚠️  App exited with status: $EXIT_STATUS"
fi

# Count final screenshots
FINAL_COUNT=$(ls -1 "$SCREENSHOT_DIR"/*.svg 2>/dev/null | wc -l)
NEW_SCREENSHOTS=$((FINAL_COUNT - INITIAL_COUNT))

echo ""
echo "📊 RESULTS:"
echo "- Initial screenshots: $INITIAL_COUNT"
echo "- Final screenshots: $FINAL_COUNT"
echo "- New screenshots created: $NEW_SCREENSHOTS"

# Show the latest screenshots
echo ""
echo "📸 Latest screenshots:"
ls -lt "$SCREENSHOT_DIR"/*.svg 2>/dev/null | head -5 | awk '{print "  - " $9}'

# Clean up
rm -f "$TEST_INPUT_FILE"

echo ""
echo "🔍 NEXT STEPS:"
echo "1. Review the screenshots in: $SCREENSHOT_DIR"
echo "2. Check the output log: pilot_test_output.log"
echo "3. Look for any errors or rendering issues"
echo "4. The error 'Static.__init__() got an unexpected keyword argument sub_blocks' should be fixed now!"
echo ""
echo "👀 Please review the screenshots and let me know what you see!"