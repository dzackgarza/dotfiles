#!/usr/bin/env python3
"""
Quick test to validate typewriter speed hypothesis.

This creates a minimal test that measures actual vs expected speed.
"""

import asyncio
import time
from src.core.animation_clock import animate_text_typewriter

async def test_typewriter_speed():
    """Test if chars_per_second parameter actually affects speed"""
    
    test_text = "This is a test of the typewriter animation speed to see if the parameter has any real effect."
    
    print("Testing typewriter animation speeds...")
    print(f"Test text length: {len(test_text)} characters")
    print()
    
    # Test cases: [chars_per_second, expected_duration]
    test_cases = [
        (10, len(test_text) / 10),      # Should take ~8.8 seconds  
        (100, len(test_text) / 100),    # Should take ~0.88 seconds
        (1000, len(test_text) / 1000),  # Should take ~0.088 seconds
        (10000, len(test_text) / 10000) # Should take ~0.0088 seconds
    ]
    
    for chars_per_sec, expected_duration in test_cases:
        print(f"\n--- Testing {chars_per_sec} chars/sec (expected: {expected_duration:.3f}s) ---")
        
        result_text = ""
        
        def capture_text(partial: str):
            nonlocal result_text
            result_text = partial
            # Print progress every 10 chars to see actual speed
            if len(partial) % 10 == 0:
                print(f"Progress: {len(partial)}/{len(test_text)} chars", end="\r")
        
        start_time = time.time()
        await animate_text_typewriter(test_text, capture_text, chars_per_second=chars_per_sec)
        actual_duration = time.time() - start_time
        
        print(f"\nActual duration: {actual_duration:.3f}s")
        print(f"Expected duration: {expected_duration:.3f}s") 
        print(f"Speed ratio: {actual_duration/expected_duration:.2f}x expected")
        
        if abs(actual_duration - expected_duration) < 0.1:
            print("✅ PASS: Speed matches expectation")
        else:
            print("❌ FAIL: Speed does not match parameter")

if __name__ == "__main__":
    asyncio.run(test_typewriter_speed())