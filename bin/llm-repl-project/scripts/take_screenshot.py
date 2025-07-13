#!/usr/bin/env python3
"""
Quick manual screenshot script for testing
"""

from datetime import datetime
from pathlib import Path

# Create a marker file to indicate we want a screenshot
screenshot_dir = Path("V3-minimal/debug_screenshots")
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
marker_file = screenshot_dir / f"manual_screenshot_request_{timestamp}.txt"

with open(marker_file, "w") as f:
    f.write(f"Manual screenshot requested at {timestamp}\n")
    f.write("Please run the app and press Ctrl+S to take a screenshot\n")
    f.write("Then check this directory for the new .svg file\n")

print(f"📸 Screenshot request created: {marker_file.name}")
print(f"\n🔍 To take a screenshot:")
print(f"1. Run: pdm run python -m V3-minimal.src.main")
print(f"2. Press Ctrl+S to capture the current state")
print(f"3. Try entering some text to trigger the error (if it still exists)")
print(f"4. Check {screenshot_dir} for new .svg files")
print(f"\n✅ The sub_blocks error should now be fixed!")