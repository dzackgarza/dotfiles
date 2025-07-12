#!/usr/bin/env python3
"""
Simple pilot test that takes a manual screenshot
"""

from pathlib import Path
import sys
import datetime

# Import the app's main module
sys.path.insert(0, str(Path(__file__).parent))
from V3_minimal.src.main import LLMReplApp

def main():
    print("🚀 Starting simple pilot test...")
    
    # Create and run the app
    app = LLMReplApp()
    
    # Take a manual screenshot
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"pilot_test_{timestamp}"
    
    print(f"📸 Creating manual screenshot: {filename}")
    app.create_debug_screenshot("pilot_test")
    
    print("✅ Screenshot created!")
    print(f"📁 Check: V3-minimal/debug_screenshots/")
    
if __name__ == "__main__":
    main()