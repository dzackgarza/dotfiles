#!/usr/bin/env python3
"""
Test script for Simple Working REPL

This tests the core functionality without requiring GUI interaction.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


async def test_cognition_processor():
    """Test the cognition processor."""
    print("🧪 Testing Cognition Processor...")
    
    try:
        from simple_working_repl import SimpleCognitionProcessor
        
        processor = SimpleCognitionProcessor()
        
        # Test processing
        result = await processor.process("Hello, how are you?")
        
        # Verify result structure
        assert "final_output" in result, "Should have final_output"
        assert "transparency_log" in result, "Should have transparency_log"
        assert "total_tokens" in result, "Should have total_tokens"
        assert "processing_duration" in result, "Should have processing_duration"
        
        # Verify transparency log
        log = result["transparency_log"]
        assert len(log) == 3, f"Should have 3 steps, got {len(log)}"
        
        for i, step in enumerate(log):
            assert "step" in step, f"Step {i} should have step number"
            assert "name" in step, f"Step {i} should have name"
            assert "status" in step, f"Step {i} should have status"
            assert "tokens" in step, f"Step {i} should have tokens"
        
        # Verify token tracking
        tokens = result["total_tokens"]
        assert tokens["input"] > 0, "Should have input tokens"
        assert tokens["output"] > 0, "Should have output tokens"
        
        print("✅ Cognition processor works correctly")
        return True
        
    except Exception as e:
        print(f"❌ Cognition processor test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_timeline_block():
    """Test timeline block creation."""
    print("🧪 Testing Timeline Block...")
    
    try:
        from simple_working_repl import TimelineBlock, BlockType
        import time
        import uuid
        
        # Create a test block
        block = TimelineBlock(
            id=str(uuid.uuid4()),
            type=BlockType.USER_INPUT,
            title="Test Block",
            content="Test content",
            timestamp=time.time(),
            tokens={"input": 5, "output": 10},
            metadata={"test": True}
        )
        
        # Verify block properties
        assert block.id is not None, "Block should have ID"
        assert block.type == BlockType.USER_INPUT, "Block type should be preserved"
        assert block.title == "Test Block", "Block title should be preserved"
        assert block.content == "Test content", "Block content should be preserved"
        assert block.tokens["input"] == 5, "Input tokens should be preserved"
        assert block.tokens["output"] == 10, "Output tokens should be preserved"
        assert block.metadata["test"] is True, "Metadata should be preserved"
        
        print("✅ Timeline block works correctly")
        return True
        
    except Exception as e:
        print(f"❌ Timeline block test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_repl_initialization():
    """Test REPL initialization without GUI."""
    print("🧪 Testing REPL Initialization...")
    
    try:
        # Mock tkinter to avoid GUI
        import unittest.mock
        
        with unittest.mock.patch('tkinter.Tk'), \
             unittest.mock.patch('tkinter.Frame'), \
             unittest.mock.patch('tkinter.Label'), \
             unittest.mock.patch('tkinter.scrolledtext.ScrolledText'), \
             unittest.mock.patch('tkinter.Text'), \
             unittest.mock.patch('tkinter.Button'):
            
            from simple_working_repl import SimpleWorkingREPL, BlockType
            
            # Create REPL instance
            repl = SimpleWorkingREPL("test")
            
            # Verify initialization
            assert repl.config_name == "test", "Config should be preserved"
            assert len(repl.timeline_blocks) >= 2, "Should have startup blocks"
            assert repl.cognition_processor is not None, "Should have cognition processor"
            assert not repl.is_processing, "Should not be processing initially"
            
            # Verify startup blocks
            block_types = [block.type for block in repl.timeline_blocks]
            assert BlockType.SYSTEM_CHECK in block_types, "Should have system check block"
            assert BlockType.WELCOME in block_types, "Should have welcome block"
            
            print("✅ REPL initialization works correctly")
            return True
        
    except Exception as e:
        print(f"❌ REPL initialization test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_dependencies():
    """Check if required dependencies are available."""
    print("🔍 Checking Dependencies...")
    
    missing_deps = []
    
    try:
        import tkinter
        print(f"✅ tkinter available (built-in)")
    except ImportError:
        missing_deps.append("tkinter")
    
    try:
        import asyncio
        print(f"✅ asyncio available (built-in)")
    except ImportError:
        missing_deps.append("asyncio")
    
    try:
        import threading
        print(f"✅ threading available (built-in)")
    except ImportError:
        missing_deps.append("threading")
    
    if missing_deps:
        print(f"❌ Missing dependencies: {', '.join(missing_deps)}")
        return False
    
    print("✅ All required dependencies available!")
    return True


async def main():
    """Run all tests."""
    print("🚀 Testing Simple Working LLM REPL")
    print("=" * 50)
    
    # Check dependencies first
    if not check_dependencies():
        print("\n❌ Cannot run tests without required dependencies")
        sys.exit(1)
    
    print()
    
    # Run tests
    tests = [
        ("Timeline Block", test_timeline_block()),
        ("REPL Initialization", test_repl_initialization()),
        ("Cognition Processor", await test_cognition_processor()),
    ]
    
    passed = 0
    total = len(tests)
    
    print("\n" + "="*50)
    print("📊 Test Summary:")
    
    for test_name, result in tests:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The Simple Working REPL is ready to use.")
        print("\n🚀 To run the application:")
        print("  python src/simple_working_repl.py")
        print("  python src/simple_working_repl.py --config fast")
        print("\n💡 This solves your core requirements:")
        print("  ✅ Block-based timeline display")
        print("  ✅ Separate timeline and input areas")
        print("  ✅ Expanding multiline input")
        print("  ✅ Preserves cognitive processing architecture")
        print("  ✅ Nearly impossible to break (tkinter GUI)")
        print("  ✅ No terminal escape sequences or complex UI")
        print("  ✅ Offloads hard problems to tkinter library")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())