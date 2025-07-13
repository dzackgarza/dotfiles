#!/usr/bin/env python3
"""
Test script for the new Textual-based LLM REPL

This script tests both the simple and enhanced versions to ensure
they work correctly and solve the original UI problems.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


async def test_simple_app():
    """Test the simple Textual app."""
    print("🧪 Testing Simple Textual App...")
    
    try:
        from textual_app import ConversationTimeline, MessageType, ConversationMessage, CognitionBlock
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
        
        # Test cognition block
        cognition = CognitionBlock("test")
        
        # Mock LLM interface
        class MockLLM:
            pass
        
        mock_llm = MockLLM()
        
        # Test processing
        results = []
        async for chunk in cognition.process("test input", mock_llm):
            results.append(chunk)
        
        assert len(results) > 0, "Cognition block should produce results"
        assert any("response to: test input" in str(result) for result in results), "Should contain response"
        
        print("✅ Cognition block works correctly")
        print("✅ Simple app tests passed!")
        
    except Exception as e:
        print(f"❌ Simple app test failed: {e}")
        return False
    
    return True


async def test_enhanced_app():
    """Test the enhanced Textual app with LLM integration."""
    print("🧪 Testing Enhanced Textual App...")
    
    try:
        from textual_llm_integration import EnhancedCognitionBlock, MessageType, ConversationMessage
        import time
        import uuid
        
        # Test enhanced cognition block
        cognition = EnhancedCognitionBlock()
        
        # Test processing
        results = []
        async for update in cognition.process("test input"):
            results.append(update)
        
        assert len(results) > 0, "Enhanced cognition should produce results"
        
        # Check for expected update types
        update_types = [result.get("type") for result in results]
        assert "status" in update_types, "Should have status updates"
        assert "final_result" in update_types, "Should have final result"
        
        print("✅ Enhanced cognition block works correctly")
        
        # Test message creation
        msg = ConversationMessage(
            id=str(uuid.uuid4()),
            type=MessageType.USER,
            content="Test message",
            timestamp=time.time(),
            metadata={"test": True}
        )
        
        assert msg.tokens == {"input": 0, "output": 0}, "Default tokens should be set"
        assert msg.type == MessageType.USER, "Message type should be preserved"
        
        print("✅ Message creation works correctly")
        print("✅ Enhanced app tests passed!")
        
    except ImportError as e:
        print(f"⚠️  Enhanced app test skipped (missing dependencies): {e}")
        return True  # Not a failure, just missing optional dependencies
    except Exception as e:
        print(f"❌ Enhanced app test failed: {e}")
        return False
    
    return True


async def test_ui_components():
    """Test UI components without running the full app."""
    print("🧪 Testing UI Components...")
    
    try:
        # Test that Textual imports work
        from textual.app import App
        from textual.widgets import Input, Static
        from rich.panel import Panel
        
        print("✅ Textual imports work correctly")
        
        # Test Rich formatting
        panel = Panel("Test content", title="Test Panel", border_style="blue")
        assert panel is not None, "Panel creation should work"
        
        print("✅ Rich formatting works correctly")
        print("✅ UI component tests passed!")
        
    except ImportError as e:
        print(f"❌ UI component test failed (missing Textual): {e}")
        print("💡 Install with: pip install textual rich")
        return False
    except Exception as e:
        print(f"❌ UI component test failed: {e}")
        return False
    
    return True


def check_dependencies():
    """Check if required dependencies are available."""
    print("🔍 Checking Dependencies...")
    
    missing_deps = []
    
    try:
        import textual
        print(f"✅ Textual {textual.__version__}")
    except ImportError:
        missing_deps.append("textual")
    
    try:
        import rich
        print(f"✅ Rich {rich.__version__}")
    except ImportError:
        missing_deps.append("rich")
    
    if missing_deps:
        print(f"❌ Missing dependencies: {', '.join(missing_deps)}")
        print("💡 Install with: pip install textual rich")
        return False
    
    print("✅ All dependencies available!")
    return True


async def main():
    """Run all tests."""
    print("🚀 Testing Textual-based LLM REPL")
    print("=" * 50)
    
    # Check dependencies first
    if not check_dependencies():
        print("\n❌ Cannot run tests without required dependencies")
        sys.exit(1)
    
    print()
    
    # Run tests
    tests = [
        ("UI Components", test_ui_components()),
        ("Simple App", test_simple_app()),
        ("Enhanced App", test_enhanced_app()),
    ]
    
    results = []
    for test_name, test_coro in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = await test_coro
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*50)
    print("📊 Test Summary:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The Textual interface is ready to use.")
        print("\n🚀 To run the application:")
        print("  python src/textual_main.py")
        print("  python src/textual_main.py --simple")
        print("  python src/textual_main.py --config fast")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())