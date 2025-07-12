#!/usr/bin/env python3
"""
Ledger Accountability System

Adds human review process to ledger completion:
1. Agent must identify user-visible behaviors before starting
2. Agent must request human review before completion
3. Human approves/rejects based on actual behavior verification
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import List

def extract_user_behaviors_from_ledger(ledger_path: Path) -> List[str]:
    """Extract specific user-visible behaviors from ledger description."""
    with open(ledger_path, 'r') as f:
        content = f.read()
    
    behaviors = []
    
    # Look for explicit behavior sections
    behavior_patterns = [
        r'User will see:?\s*\n((?:\s*[-*]\s*.+\n?)+)',
        r'User-visible behavior:?\s*\n((?:\s*[-*]\s*.+\n?)+)',
        r'What the user experiences:?\s*\n((?:\s*[-*]\s*.+\n?)+)',
        r'User experience:?\s*\n((?:\s*[-*]\s*.+\n?)+)'
    ]
    
    for pattern in behavior_patterns:
        matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            behavior_text = match.group(1)
            for line in behavior_text.split('\n'):
                line = line.strip()
                if line.startswith(('-', '*')):
                    behavior = line[1:].strip()
                    if behavior:
                        behaviors.append(behavior)
    
    return behaviors

def request_human_review(ledger_name: str, user_behaviors: List[str]):
    """Request human review with user-visible behaviors."""
    print(f"\n🚨 HUMAN REVIEW REQUIRED for ledger: {ledger_name}")
    print(f"═══════════════════════════════════════════════════════")
    print(f"Agent claims the following user-visible behaviors are now implemented:")
    for i, behavior in enumerate(user_behaviors, 1):
        print(f"  {i}. {behavior}")
    
    print(f"\n💡 INSTRUCTIONS FOR HUMAN REVIEWER:")
    print(f"   1. Test the application and verify each behavior is actually present")
    print(f"   2. If behaviors work as described:")
    print(f"      → Run: python scripts/ledger_tracker.py approve-review {ledger_name}")
    print(f"   3. If behaviors are missing or broken:")
    print(f"      → Run: python scripts/ledger_tracker.py reject-review {ledger_name} 'specific feedback'")
    print(f"═══════════════════════════════════════════════════════")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python ledger_accountability.py <ledger_name> <ledger_file>")
        sys.exit(1)
    
    ledger_name = sys.argv[1]
    ledger_file = Path(sys.argv[2])
    
    behaviors = extract_user_behaviors_from_ledger(ledger_file)
    
    if not behaviors:
        print(f"❌ ACCOUNTABILITY ERROR: No user-visible behaviors found in {ledger_file}")
        print("   Ledger must include a section like 'User will see:' with specific behaviors")
        sys.exit(1)
    
    request_human_review(ledger_name, behaviors)