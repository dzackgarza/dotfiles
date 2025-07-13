#!/usr/bin/env python3
"""
GUI Reminder Hook
Reminds about GUI testing limitations
"""

import json
import sys
import random

def main():
    # Only trigger occasionally 
    if random.randint(1, 10) == 1:
        print(json.dumps({
            "decision": "approve",
            "reason": "💡 GUI Reminder: Never run GUI apps in Claude Code - use pilot tests and screenshots for verification"
        }))
    else:
        print(json.dumps({"decision": "approve"}))

if __name__ == "__main__":
    main()