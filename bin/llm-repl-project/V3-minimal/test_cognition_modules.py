#!/usr/bin/env python
"""Test cognition modules independently"""

import asyncio
from src.cognition import CognitionManager, CognitionEvent, CognitionResult


async def test_noop_module():
    """Test NoOp module pass-through"""
    print("=== Testing NoOp Module ===")
    
    manager = CognitionManager()
    manager.set_module("NoOp Module")
    
    # Set up callbacks to print events
    async def print_staging_event(event: CognitionEvent):
        print(f"[STAGING] {event.type}: {event.content}")
    
    async def print_timeline_result(result: CognitionResult):
        print(f"[TIMELINE] Role: {result.role}")
        print(f"[TIMELINE] Content: {result.content}")
        print(f"[TIMELINE] Metadata: {result.metadata}")
    
    manager.set_staging_callback(print_staging_event)
    manager.set_timeline_callback(print_timeline_result)
    
    # Process a query
    result = await manager.process_query("Hello, world!")
    print(f"Result: {result}")
    print()


async def test_mock_module():
    """Test Mock module with 2s computation"""
    print("=== Testing Mock Module ===")
    
    manager = CognitionManager()
    manager.set_module("Mock Cognition Module")
    
    # Set up callbacks to print events
    async def print_staging_event(event: CognitionEvent):
        print(f"[STAGING] {event.type}: {event.content.strip()}")
    
    async def print_timeline_result(result: CognitionResult):
        print(f"\n[TIMELINE] Role: {result.role}")
        print(f"[TIMELINE] Content: {result.content}")
        print(f"[TIMELINE] Sub-blocks: {len(result.sub_blocks)}")
        for i, sub in enumerate(result.sub_blocks):
            print(f"  [{i}] {sub['module_name']}: {sub['content']}")
        print(f"[TIMELINE] Metadata: {result.metadata}")
    
    manager.set_staging_callback(print_staging_event)
    manager.set_timeline_callback(print_timeline_result)
    
    # Process a query
    print("Processing query...")
    result = await manager.process_query("Explain quantum computing in simple terms")
    print(f"\nFinal result: {result}")


async def main():
    """Run all tests"""
    await test_noop_module()
    await test_mock_module()
    
    print("\n✅ All tests completed!")


if __name__ == "__main__":
    asyncio.run(main())