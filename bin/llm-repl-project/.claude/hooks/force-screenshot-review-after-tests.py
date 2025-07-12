#!/usr/bin/env python3
"""
Force Screenshot Review After Tests Hook
Ensures visual verification after test execution
"""

import json
import sys

def main():
    print(json.dumps({
        "decision": "approve",
        "reason": "📸 Remember to take screenshots after tests to verify visual behavior"
    }))

if __name__ == "__main__":
    main()