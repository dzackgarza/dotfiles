#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

import argparse
import json
import sys

def main():
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('--notify', action='store_true', help='Enable notifications')
        args = parser.parse_args()
        
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)
        
        # Extract notification message
        message = input_data.get("message", "")
        
        # No-op - just exit successfully
        sys.exit(0)
        
    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully
        sys.exit(0)
    except Exception:
        # Handle any other errors gracefully
        sys.exit(0)

if __name__ == "__main__":
    main()