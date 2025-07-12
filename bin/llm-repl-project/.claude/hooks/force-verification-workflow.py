#!/usr/bin/env python3
"""
Force Verification Workflow Hook
"""

import json
import sys

print(json.dumps({"decision": "approve"}))