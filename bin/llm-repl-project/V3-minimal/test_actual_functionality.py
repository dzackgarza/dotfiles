#!/usr/bin/env python3
"""
Test actual functionality of the LLM REPL
This script tests what components are actually working vs what's documented.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.main import LLMReplApp
from src.widgets.sacred_timeline import SacredTimelineWidget
from src.widgets.live_workspace import LiveWorkspaceWidget
from src.widgets.prompt_input import PromptInput
from src.core.live_blocks import LiveBlock, InscribedBlock
from src.cognition.manager import CognitionManager


def test_core_components():
    """Test if core components can be instantiated"""
    print("=== Testing Core Components ===")

    try:
        app = LLMReplApp()
        print("✅ LLMReplApp can be instantiated")
    except Exception as e:
        print(f"❌ LLMReplApp failed: {e}")
        return False

    try:
        timeline = SacredTimelineWidget()
        print("✅ SacredTimelineWidget can be instantiated")
    except Exception as e:
        print(f"❌ SacredTimelineWidget failed: {e}")

    try:
        workspace = LiveWorkspaceWidget()
        print("✅ LiveWorkspaceWidget can be instantiated")
    except Exception as e:
        print(f"❌ LiveWorkspaceWidget failed: {e}")

    try:
        prompt = PromptInput()
        print("✅ PromptInput can be instantiated")
    except Exception as e:
        print(f"❌ PromptInput failed: {e}")

    return True


def test_cognition_system():
    """Test if cognition system works"""
    print("\n=== Testing Cognition System ===")

    try:
        manager = CognitionManager()
        modules = manager.get_available_modules()
        print(f"✅ CognitionManager created with modules: {list(modules.keys())}")

        current = manager.get_current_module_name()
        print(f"✅ Current module: {current}")

        return True
    except Exception as e:
        print(f"❌ CognitionManager failed: {e}")
        return False


async def test_async_processing():
    """Test if async processing works"""
    print("\n=== Testing Async Processing ===")

    try:
        manager = CognitionManager()
        result = await manager.process_query("Hello, test query")
        print(f"✅ Async processing works: {result.content[:50]}...")
        return True
    except Exception as e:
        print(f"❌ Async processing failed: {e}")
        return False


def test_live_blocks():
    """Test live block system"""
    print("\n=== Testing Live Block System ===")

    try:
        live_block = LiveBlock(
            id="test-1",
            role="user",
            content="Test content",
            metadata={}
        )
        print(f"✅ LiveBlock created: {live_block.id}")

        inscribed_block = InscribedBlock(
            id="test-2",
            role="assistant",
            content="Response content",
            metadata={},
            timestamp="2024-01-01T00:00:00"
        )
        print(f"✅ InscribedBlock created: {inscribed_block.id}")

        return True
    except Exception as e:
        print(f"❌ Live blocks failed: {e}")
        return False


async def test_app_startup():
    """Test if app can start and run briefly"""
    print("\n=== Testing App Startup ===")

    try:
        app = LLMReplApp()

        # Test that compose() works
        components = list(app.compose())
        print(f"✅ App compose() works, created {len(components)} components")

        # Test basic properties
        print(f"✅ App title: {app.TITLE}")
        print(f"✅ App CSS path: {app.CSS_PATH}")

        return True
    except Exception as e:
        print(f"❌ App startup failed: {e}")
        return False


def test_dependency_imports():
    """Test if all dependencies are available"""
    print("\n=== Testing Dependencies ===")

    dependencies = [
        ("textual", "Textual TUI framework"),
        ("rich", "Rich text formatting"),
        ("pydantic", "Data validation"),
        ("yaml", "YAML configuration"),
        ("tiktoken", "Token counting"),
    ]

    all_good = True
    for module, description in dependencies:
        try:
            __import__(module)
            print(f"✅ {module}: {description}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            all_good = False

    return all_good


async def main():
    """Run all tests"""
    print("LLM REPL V3-minimal Functionality Test")
    print("=" * 50)

    # Test imports and dependencies
    deps_ok = test_dependency_imports()

    # Test core components
    core_ok = test_core_components()

    # Test cognition system
    cognition_ok = test_cognition_system()

    # Test live blocks
    blocks_ok = test_live_blocks()

    # Test async processing
    async_ok = await test_async_processing()

    # Test app startup
    startup_ok = await test_app_startup()

    print("\n=== Summary ===")
    tests = [
        ("Dependencies", deps_ok),
        ("Core Components", core_ok),
        ("Cognition System", cognition_ok),
        ("Live Blocks", blocks_ok),
        ("Async Processing", async_ok),
        ("App Startup", startup_ok),
    ]

    passed = sum(1 for _, ok in tests if ok)
    total = len(tests)

    for test_name, ok in tests:
        status = "✅ PASS" if ok else "❌ FAIL"
        print(f"{test_name}: {status}")

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All core functionality appears to be working!")
        print("The app should be runnable with: pdm run python src/main.py")
    else:
        print("\n⚠️  Some functionality is missing or broken.")


if __name__ == "__main__":
    asyncio.run(main())
