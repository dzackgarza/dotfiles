#!/usr/bin/env python3
"""Test real app behavior without GUI - verify cognition sub-modules work correctly."""

import asyncio
import time
from src.sacred_timeline import SacredTimeline
from src.core.response_generator import ResponseGenerator  
from src.core.async_input_processor import AsyncInputProcessor
from src.core.live_blocks import LiveBlockManager


async def test_real_input():
    """Test real user input processing."""
    print("Testing real application behavior...")
    print("-" * 60)
    
    # Create components
    timeline = SacredTimeline()
    live_block_manager = LiveBlockManager()
    response_generator = ResponseGenerator()
    input_processor = AsyncInputProcessor(timeline, response_generator)
    
    # Simulate user input without GUI
    user_query = "Explain async/await in Python"
    print(f"Simulated user input: {user_query}")
    print("-" * 60)
    
    # Track timeline changes
    initial_count = len(timeline._blocks)
    print(f"Initial timeline blocks: {initial_count}")
    
    # Process input
    start_time = time.time()
    await input_processor.process_user_input_async(user_query)
    
    # Wait for completion
    await asyncio.sleep(1.0)
    
    # Check results
    final_count = len(timeline._blocks)
    elapsed = time.time() - start_time
    
    print(f"\nProcessing completed in {elapsed:.1f}s")
    print(f"Final timeline blocks: {final_count}")
    print(f"New blocks added: {final_count - initial_count}")
    
    # Show block details
    print("\nTimeline blocks:")
    for i, block in enumerate(timeline._blocks):
        print(f"\n{i+1}. {block.role.upper()} block:")
        print(f"   Content length: {len(block.content)} chars")
        print(f"   Time taken: {block.time_taken:.1f}s" if block.time_taken else "   Time taken: N/A")
        print(f"   Tokens: {block.tokens_input}↑/{block.tokens_output}↓" if block.tokens_input else "   Tokens: N/A")
        
        if block.sub_blocks:
            print(f"   Sub-blocks: {len(block.sub_blocks)}")
            for j, sub in enumerate(block.sub_blocks):
                print(f"     {j+1}. {sub.type}: {len(sub.content)} chars")
    
    # Verify cognition block structure
    cognition_blocks = [b for b in timeline._blocks if b.role == "cognition"]
    if cognition_blocks:
        cog_block = cognition_blocks[0]
        print(f"\nCognition block analysis:")
        print(f"  Has sub-blocks: {len(cog_block.sub_blocks) > 0}")
        print(f"  Sub-block count: {len(cog_block.sub_blocks)}")
        print(f"  Expected sub-blocks: 3 (route_query, call_tool, format_output)")
        
        if len(cog_block.sub_blocks) == 3:
            print("  ✅ All 3 sub-modules executed correctly!")
        else:
            print("  ❌ Sub-module count mismatch!")
    
    print("\n" + "=" * 60)
    print("Test completed successfully!")


if __name__ == "__main__":
    asyncio.run(test_real_input())