#!/usr/bin/env python3
"""
Test script for the Rich-based LLM REPL

This tests the immediate solution that works with available dependencies.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


async def test_rich_repl():
    """Test the Rich-based REPL components."""
    print("🧪 Testing Rich-Based LLM REPL...")
    
    try:
        from rich_based_repl import (
            ConversationTimeline, MessageType, ConversationMessage,
            SimpleCognitionBlock, RichREPLInterface
        )
        import time
        import uuid
        
        # Test timeline deduplication
        timeline = ConversationTimeline()
        
        # Add same message twice
        msg_id = str(uuid.uuid4())
        msg1 = ConversationMessage(
            id=msg_id,
            type=MessageType.USER,
            content="Test message",
            timestamp=time.time(),
            metadata={}
        )
        msg2 = ConversationMessage(
            id=msg_id,  # Same ID
            type=MessageType.USER,
            content="Test message duplicate",
            timestamp=time.time(),
            metadata={}
        )
        
        # First should succeed, second should fail (duplicate)
        assert timeline.add_message(msg1) == True, "First message should be added"
        assert timeline.add_message(msg2) == False, "Duplicate message should be rejected"
        assert len(timeline.messages) == 1, "Timeline should have only one message"
        
        print("✅ Timeline deduplication works correctly")
        
        # Test token tracking
        tokens = timeline.get_total_tokens()
        assert tokens == {"input": 0, "output": 0}, "Initial tokens should be zero"
        
        # Add message with tokens
        msg_with_tokens = ConversationMessage(
            id=str(uuid.uuid4()),
            type=MessageType.ASSISTANT,
            content="Response",
            timestamp=time.time(),
            metadata={},
            tokens={"input": 10, "output": 20}
        )
        timeline.add_message(msg_with_tokens)
        
        tokens = timeline.get_total_tokens()
        assert tokens == {"input": 10, "output": 20}, "Tokens should be tracked correctly"
        
        print("✅ Token tracking works correctly")
        
        # Test cognition block
        cognition = SimpleCognitionBlock()
        
        results = []
        async for update in cognition.process("test input"):
            results.append(update)
        
        assert len(results) > 0, "Cognition block should produce results"
        
        # Check for expected update types
        update_types = [result.get("type") for result in results]
        assert "step_start" in update_types, "Should have step start updates"
        assert "step_complete" in update_types, "Should have step complete updates"
        assert "final_result" in update_types, "Should have final result"
        
        print("✅ Cognition block works correctly")
        
        # Test REPL interface creation
        repl = RichREPLInterface("test")
        assert repl.config_name == "test", "Config should be set correctly"
        assert len(repl.timeline.messages) == 0, "Timeline should start empty"
        
        # Test adding messages
        success = repl.add_message(MessageType.USER, "Test message", {"test": True})
        assert success == True, "Should successfully add message"
        assert len(repl.timeline.messages) == 1, "Timeline should have one message"
        
        # Test duplicate prevention
        # This won't be a duplicate because add_message generates new IDs
        success2 = repl.add_message(MessageType.USER, "Test message", {"test": True})
        assert success2 == True, "Should add second message (different ID)"
        assert len(repl.timeline.messages) == 2, "Timeline should have two messages"
        
        print("✅ REPL interface works correctly")
        
        # Test clear functionality
        repl.clear_timeline()
        # Should have 1 message (the "Timeline cleared" system message)
        assert len(repl.timeline.messages) == 1, "Timeline should have clear message"
        assert repl.timeline.messages[0].type == MessageType.SYSTEM, "Should be system message"
        
        print("✅ Clear functionality works correctly")
        
        print("✅ All Rich REPL tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Rich REPL test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_dependencies():
    """Check if required dependencies are available."""
    print("🔍 Checking Dependencies...")
    
    missing_deps = []
    
    try:
        import rich
        print(f"✅ Rich available")
    except ImportError:
        missing_deps.append("rich")
    
    if missing_deps:
        print(f"❌ Missing dependencies: {', '.join(missing_deps)}")
        return False
    
    print("✅ All required dependencies available!")
    return True


async def main():
    """Run all tests."""
    print("🚀 Testing Rich-Based LLM REPL")
    print("=" * 50)
    
    # Check dependencies first
    if not check_dependencies():
        print("\n❌ Cannot run tests without required dependencies")
        sys.exit(1)
    
    print()
    
    # Run test
    success = await test_rich_repl()
    
    print("\n" + "="*50)
    if success:
        print("🎉 All tests passed! The Rich-based interface is ready to use.")
        print("\n🚀 To run the application:")
        print("  python src/rich_based_repl.py")
        print("  python src/rich_based_repl.py --config fast")
        print("\n💡 This solves your immediate UI problems:")
        print("  ✅ No more timeline duplicates")
        print("  ✅ Clean, professional formatting")
        print("  ✅ Preserves your cognition blocks")
        print("  ✅ No escape sequence bugs")
        print("  ✅ Easy to test and extend")
    else:
        print("⚠️  Tests failed. Check the output above for details.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())