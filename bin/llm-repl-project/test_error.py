#!/usr/bin/env python3
"""
Test script to reproduce the Static sub_blocks error
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent / "V3-minimal" / "src"))

# Import necessary classes
from textual.widgets import Static
from widgets.timeline import TimelineBlock, SubBlock
from datetime import datetime

# Create a test TimelineBlock with sub_blocks
test_block = TimelineBlock(
    id="test123",
    timestamp=datetime.now(),
    role="system",
    content="Test content",
    sub_blocks=[
        SubBlock(id="sub1", type="step", content="Step 1"),
        SubBlock(id="sub2", type="step", content="Step 2")
    ]
)

print("Created TimelineBlock with sub_blocks")
print(f"Block attributes: {list(vars(test_block).keys())}")

# Now let's see what happens if we try different ways to create Static
print("\nTesting different ways to create Static...")

# Test 1: Pass the block object directly
try:
    print("\nTest 1: Static(test_block)")
    static1 = Static(test_block)
    print("Success!")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Unpack block attributes
try:
    print("\nTest 2: Static(**vars(test_block))")
    static2 = Static(**vars(test_block))
    print("Success!")
except Exception as e:
    print(f"Error: {e}")

# Test 3: Pass block as renderable (correct way)
try:
    print("\nTest 3: Static(str(test_block))")
    static3 = Static(str(test_block))
    print("Success!")
except Exception as e:
    print(f"Error: {e}")

# Test 4: Look for where this might happen
print("\n\nLooking for potential issues...")
print("If TimelineBlock is passed where text is expected, it could cause this error.")
print("The error happens when attributes of TimelineBlock are unpacked into Static().")