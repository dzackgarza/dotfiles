#!/usr/bin/env python3
"""
Debug the animation clock to find the bottleneck
"""

import asyncio
from src.core.animation_clock import AnimationClock

async def debug_animation_clock():
    print("Animation Clock Debug")
    print(f"Current FPS: {AnimationClock.get_fps()}")
    print(f"Frame duration: {AnimationClock.get_frame_duration():.6f}s")
    print()
    
    # Test the problematic calculation
    test_speeds = [10, 100, 1000, 10000]
    
    for chars_per_second in test_speeds:
        seconds_per_char = 1.0 / chars_per_second
        frames_per_char = max(1, await AnimationClock.animate_over_time(seconds_per_char))
        
        print(f"chars_per_second: {chars_per_second}")
        print(f"  seconds_per_char: {seconds_per_char:.6f}")
        print(f"  frames_per_char: {frames_per_char}")
        print(f"  actual_seconds_per_char: {frames_per_char * AnimationClock.get_frame_duration():.6f}")
        print(f"  actual_chars_per_second: {1.0 / (frames_per_char * AnimationClock.get_frame_duration()):.2f}")
        print()

if __name__ == "__main__":
    asyncio.run(debug_animation_clock())