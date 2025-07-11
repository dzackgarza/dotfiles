#!/usr/bin/env python3
"""
Test Sacred Timeline Integration

Simple test to verify our merged V2-5-0/V2-5-1 components work in V3.
"""

import asyncio
import sys
from pathlib import Path

# Add V3 to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from core.blocks import TimelineBlock, BlockType, create_system_check_block, create_welcome_block, create_user_input_block
from core.timeline import TimelineManager
from core.cognition import CognitionProcessor
from config.settings import get_config


def test_sacred_timeline_components():
    """Test that our Sacred Timeline components work correctly."""
    print("🧪 Testing Sacred Timeline Components...")
    
    # Test 1: Configuration system
    print("\n1️⃣ Testing Configuration System")
    config = get_config('debug')
    print(f"✅ Config loaded: {config.name} - {config.description}")
    print(f"   Cognition delay: {config.cognition_delay}s")
    
    # Test 2: Timeline Manager
    print("\n2️⃣ Testing Timeline Manager")
    timeline = TimelineManager()
    timeline.initialize_with_startup_blocks(config.name)
    print(f"✅ Timeline initialized with {timeline.get_block_count()} blocks")
    
    # Test 3: Block creation
    print("\n3️⃣ Testing Block Creation")
    user_block = create_user_input_block("Hello, Sacred Timeline!")
    timeline.add_block(user_block)
    print(f"✅ User block created: {user_block.title}")
    print(f"   Timeline now has {timeline.get_block_count()} blocks")
    
    # Test 4: Timeline export
    print("\n4️⃣ Testing Timeline Export")
    exported = timeline.export_timeline()
    print(f"✅ Timeline exported: {len(exported)} blocks")
    for i, block in enumerate(exported):
        print(f"   Block {i+1}: {block['type']} - {block['title']}")
    
    return timeline


async def test_cognition_processor():
    """Test that the Cognition Processor works correctly."""
    print("\n\n🧠 Testing Cognition Processor...")
    
    # Test 5: Cognition processor
    print("\n5️⃣ Testing Cognition Processor")
    processor = CognitionProcessor()
    print(f"✅ Processor created with {len(processor.get_step_names())} steps:")
    for step in processor.get_step_names():
        print(f"   • {step}")
    
    # Test 6: Cognitive processing
    print("\n6️⃣ Testing Cognitive Processing")
    result = await processor.process("What is the Sacred Timeline?")
    print(f"✅ Processing complete in {result['processing_duration']:.2f}s")
    print(f"   Total tokens: {result['total_tokens']}")
    print(f"   Steps executed: {len(result['transparency_log'])}")
    
    return result


def display_timeline_text(timeline: TimelineManager):
    """Display the timeline as formatted text."""
    print("\n\n📜 Sacred Timeline Output:")
    print("=" * 80)
    print(timeline.get_timeline_text())
    print("=" * 80)


async def main():
    """Run the full Sacred Timeline integration test."""
    print("🚀 Sacred Timeline Integration Test")
    print("Testing V2-5-0/V2-5-1 merge into V3...")
    
    try:
        # Test synchronous components
        timeline = test_sacred_timeline_components()
        
        # Test asynchronous components  
        result = await test_cognition_processor()
        
        # Display final timeline
        display_timeline_text(timeline)
        
        print("\n🎉 All Sacred Timeline components working correctly!")
        print("✅ Ready for Elia integration")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error in Sacred Timeline test: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)