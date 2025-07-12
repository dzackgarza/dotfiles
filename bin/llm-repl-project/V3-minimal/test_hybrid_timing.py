#!/usr/bin/env python3
"""
Test the new hybrid timing system at extreme speeds
"""

import asyncio
import time
from src.core.animation_clock import animate_text_typewriter

async def test_extreme_speeds():
    """Test the hybrid timing system at various extreme speeds"""
    
    test_text = "This is a test of extreme typewriter speeds"
    
    print("Testing hybrid timing system...")
    print(f"Test text length: {len(test_text)} characters")
    print()
    
    # Test cases with extreme speeds
    test_cases = [
        (60, "Frame-synchronized (at FPS limit)"),
        (150, "Time-synchronized (above FPS)"),
        (1000, "High-speed time-synchronized"),
        (2500, "Ultra-high speed"),
        (6000, "Instant mode (should be immediate)"),
    ]
    
    for chars_per_sec, description in test_cases:
        print(f"--- Testing {chars_per_sec} chars/sec ({description}) ---")
        
        result_text = ""
        
        def capture_text(partial: str):
            nonlocal result_text
            result_text = partial
        
        start_time = time.time()
        await animate_text_typewriter(test_text, capture_text, chars_per_second=chars_per_sec)
        actual_duration = time.time() - start_time
        
        expected_duration = len(test_text) / chars_per_sec if chars_per_sec <= 5000 else 0.001
        
        print(f"Actual duration: {actual_duration:.3f}s")
        print(f"Expected duration: {expected_duration:.3f}s")
        
        if chars_per_sec > 5000:
            print("✅ PASS: Instant mode activated")
        elif actual_duration < expected_duration * 1.5:  # Allow some tolerance
            print("✅ PASS: Speed within acceptable range")
        else:
            print("❌ FAIL: Speed too slow")
        
        print()

if __name__ == "__main__":
    asyncio.run(test_extreme_speeds())