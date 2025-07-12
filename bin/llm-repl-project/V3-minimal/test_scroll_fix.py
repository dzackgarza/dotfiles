#!/usr/bin/env python3
"""
Test script to verify the scroll-stealing fix.
This creates a cognition block with rapid progress updates and checks 
that scroll triggers are properly separated from progress updates.
"""

import asyncio
import time
from src.core.live_blocks import LiveBlock, LiveBlockManager

class MockScrollTracker:
    """Mock class to track scroll trigger calls."""
    def __init__(self):
        self.scroll_calls = []
        self.progress_updates = []
        self.content_updates = []
    
    def on_progress_update(self, block):
        """Track progress-only updates (should not trigger scrolls)."""
        self.progress_updates.append(time.time())
        print(f"Progress update: {len(self.progress_updates)}")
    
    def on_content_update(self, block):
        """Track content updates (can trigger scrolls).""" 
        self.content_updates.append(time.time())
        print(f"Content update: {len(self.content_updates)} - {block.data.content[:50]}")

async def test_scroll_fix():
    """Test that progress updates don't trigger excessive scroll attempts."""
    print("Testing scroll-stealing fix...")
    
    tracker = MockScrollTracker()
    
    # Create a cognition block
    manager = LiveBlockManager()
    block = manager.create_live_block("cognition", "Starting cognition...")
    
    # Subscribe to both types of updates
    block.add_progress_callback(tracker.on_progress_update)
    block.add_update_callback(tracker.on_content_update)
    
    print("Starting cognition simulation...")
    start_time = time.time()
    
    # Run cognition simulation which has 10Hz timer updates
    await block.start_mock_simulation("cognition")
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\nSimulation completed in {duration:.2f}s")
    print(f"Progress updates: {len(tracker.progress_updates)}")
    print(f"Content updates: {len(tracker.content_updates)}")
    
    # Analysis
    expected_progress_updates = int(duration * 10)  # 10Hz timer
    print(f"Expected progress updates (~10Hz): ~{expected_progress_updates}")
    
    if len(tracker.progress_updates) > len(tracker.content_updates) * 5:
        print("✅ SUCCESS: Progress updates properly separated from content updates")
        print("✅ This should prevent scroll-stealing during rapid timer updates")
    else:
        print("❌ ISSUE: Progress and content updates not properly separated")
    
    # Verify that progress updates are frequent but content updates are meaningful
    if len(tracker.progress_updates) > 10:
        print("✅ Progress updates are frequent (good for smooth animations)")
    else:
        print("❌ Progress updates seem too infrequent")
        
    if len(tracker.content_updates) < len(tracker.progress_updates) / 2:
        print("✅ Content updates are less frequent (good for scroll control)")
    else:
        print("❌ Too many content updates - may still cause scroll issues")

if __name__ == "__main__":
    asyncio.run(test_scroll_fix())