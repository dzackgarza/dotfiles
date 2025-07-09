#!/usr/bin/env python3
"""Test script to run V1 and capture output."""

import pexpect
import sys
import time

def test_v1_interaction():
    """Test V1 interaction to see the original format."""
    print("🧪 Testing V1 REPL format...")
    
    # Start the V1 REPL
    child = pexpect.spawn('python src/llm_repl_v0.py', timeout=60)
    
    # Wait for the prompt
    child.expect('You:', timeout=30)
    
    # Send a query
    child.sendline('Hello there')
    
    # Wait for response
    child.expect('You:', timeout=30)
    
    # Quit
    child.sendline('/quit')
    
    # Wait for exit
    child.expect(pexpect.EOF, timeout=10)
    
    # Print output
    print("V1 Output:")
    print("=" * 60)
    print(child.before.decode())
    print("=" * 60)
    
    child.close()

if __name__ == "__main__":
    test_v1_interaction()