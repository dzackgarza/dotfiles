#!/usr/bin/env python3
"""Test the current state of cognition sub-blocks."""

import asyncio
from src.core.async_input_processor import AsyncInputProcessor
from src.sacred_timeline import SacredTimeline
from src.core.response_generator import ResponseGenerator
from src.core.live_blocks import LiveBlockManager


class TestObserver:
    """Observer to check live block updates."""
    def __init__(self):
        self.blocks = []
        
    def on_block_added(self, block):
        """Called when regular block is added to timeline."""
        print(f"Timeline block added: {block.role}")
        self.blocks.append(block)
        
    def on_live_block_update(self, block):
        print(f"Live block update: {block.role} - {block.state}")
        if hasattr(block, 'cognition_progress') and block.cognition_progress:
            progress = block.cognition_progress
            print(f"  Progress: {progress.progress_percentage:.1%}")
            print(f"  Elapsed: {progress.elapsed_time:.1f}s")
            print(f"  Steps: {progress.completed_steps}/{progress.total_steps}")
        else:
            # For sub-blocks, show their timing data
            if hasattr(block, 'data'):
                print(f"  Wall time: {block.data.wall_time_seconds:.1f}s")
                print(f"  Tokens: {block.data.tokens_input}↑/{block.data.tokens_output}↓")
        print()
        

async def test_cognition():
    """Test cognition pipeline execution."""
    timeline = SacredTimeline()
    response_gen = ResponseGenerator()
    processor = AsyncInputProcessor(timeline, response_gen)
    
    # Add observer
    observer = TestObserver()
    timeline.add_observer(observer)
    
    # Test query
    print("Testing cognition pipeline...")
    await processor.process_user_input_async("Help me understand async/await in Python")
    
    # Wait a bit for all updates
    await asyncio.sleep(0.5)
    
    # Check final blocks collected by observer
    print("\nFinal timeline blocks:")
    for block in observer.blocks:
        print(f"- {block.role}: {len(block.content)} chars")
        if hasattr(block, 'sub_blocks') and block.sub_blocks:
            for sub in block.sub_blocks:
                print(f"  - {sub.type}: {len(sub.content)} chars")


if __name__ == "__main__":
    asyncio.run(test_cognition())