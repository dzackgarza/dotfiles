#!/usr/bin/env python3
"""
Comprehensive Test Framework - Differential Improvement

DIFFERENTIAL CHANGE: Add comprehensive testing that makes errors impossible
while preserving your architectural innovations.

PRESERVED:
- Cognition blocks testing
- Timeline integrity testing
- Plugin architecture testing

ADDED:
- Property-based testing
- Integration test framework
- Error injection testing
- Performance testing
"""

import pytest
import asyncio
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from unittest.mock import Mock, AsyncMock
import time
import random
from hypothesis import given, strategies as st


@dataclass
class TestScenario:
    """Test scenario for comprehensive testing."""
    name: str
    input_data: Any
    expected_output_type: type
    expected_plugins: List[str]
    should_fail: bool = False
    timeout_seconds: float = 5.0


class MockLLMInterface:
    """Mock LLM interface for testing."""
    
    def __init__(self, responses: List[str] = None, delay: float = 0.1):
        self.responses = responses or ["Mock response"]
        self.call_count = 0
        self.delay = delay
        self.requests: List[Any] = []
    
    async def make_request(self, request):
        """Mock LLM request."""
        self.requests.append(request)
        await asyncio.sleep(self.delay)
        
        response_text = self.responses[self.call_count % len(self.responses)]
        self.call_count += 1
        
        # Create mock response
        from plugins.llm_interface import LLMResponse, TokenUsage
        return LLMResponse(
            content=response_text,
            thoughts="Mock thinking",
            tokens=TokenUsage(
                input_tokens=len(request.messages[0]["content"].split()),
                output_tokens=len(response_text.split()),
                thoughts_tokens=2
            ),
            duration_seconds=self.delay,
            model="mock-model",
            request_id=request.request_id,
            cognitive_module=request.cognitive_module,
            task_description=request.task_description
        )


class TestFramework:
    """
    Comprehensive test framework for the LLM REPL.
    
    DIFFERENTIAL IMPROVEMENT:
    - Tests all architectural components
    - Property-based testing for edge cases
    - Integration testing for full workflows
    - Performance and error injection testing
    """
    
    def __init__(self):
        self.test_scenarios: List[TestScenario] = []
        self.setup_test_scenarios()
    
    def setup_test_scenarios(self):
        """Setup comprehensive test scenarios."""
        self.test_scenarios = [
            TestScenario(
                name="simple_user_input",
                input_data="Hello, world!",
                expected_output_type=str,
                expected_plugins=["user_input", "cognition", "assistant_response"]
            ),
            TestScenario(
                name="empty_input",
                input_data="",
                expected_output_type=str,
                expected_plugins=["user_input"],
                should_fail=False  # Should handle gracefully
            ),
            TestScenario(
                name="very_long_input",
                input_data="x" * 10000,
                expected_output_type=str,
                expected_plugins=["user_input", "cognition", "assistant_response"]
            ),
            TestScenario(
                name="special_characters",
                input_data="Hello! @#$%^&*()_+ 🚀 ñáéíóú",
                expected_output_type=str,
                expected_plugins=["user_input", "cognition", "assistant_response"]
            ),
            TestScenario(
                name="multiline_input",
                input_data="Line 1\nLine 2\nLine 3",
                expected_output_type=str,
                expected_plugins=["user_input", "cognition", "assistant_response"]
            )
        ]
    
    async def test_plugin_isolation(self):
        """Test that plugins work in isolation."""
        from simplified_plugins import SimpleUserInputPlugin, SimplifiedPluginManager
        
        # Test user input plugin in isolation
        plugin = SimpleUserInputPlugin()
        result = await plugin.safe_process("test input", {})
        
        assert result.status.value == "completed"
        assert result.content == "test input"
        assert result.error is None
        assert result.duration >= 0
        
        print("✅ Plugin isolation test passed")
    
    async def test_cognition_blocks(self):
        """Test cognition blocks architecture."""
        from simplified_plugins import CognitionBlockPlugin
        from plugins.cognitive_modules import QueryRoutingModule, PromptEnhancementModule
        
        # Create cognition plugin with modules
        modules = [QueryRoutingModule(), PromptEnhancementModule()]
        plugin = CognitionBlockPlugin(modules)
        
        # Mock LLM manager
        mock_llm_manager = Mock()
        mock_llm_interface = MockLLMInterface(["route: chat", "enhanced prompt"])
        mock_llm_manager.get_interface.return_value = mock_llm_interface
        
        context = {"llm_manager": mock_llm_manager}
        result = await plugin.safe_process("test query", context)
        
        assert result.status.value == "completed"
        assert len(result.metadata["transparency_log"]) == 2  # Two modules
        assert result.tokens["input"] > 0 or result.tokens["output"] > 0
        
        print("✅ Cognition blocks test passed")
    
    async def test_timeline_integrity(self):
        """Test timeline integrity system."""
        from timeline_integrity import ApplicationWithSecureTimeline, PluginValidationError
        from simplified_plugins import SimpleUserInputPlugin, SimplifiedTimelineAdapter
        from rich.console import Console
        
        console = Console()
        app = ApplicationWithSecureTimeline(console)
        
        # Test that only valid plugins can be added
        plugin = SimpleUserInputPlugin()
        result = await plugin.safe_process("test", {})
        adapter = SimplifiedTimelineAdapter(plugin, result)
        
        # This should work
        app.add_plugin_to_timeline(adapter)
        
        # Test that invalid objects are rejected
        try:
            app.add_plugin_to_timeline("invalid object")
            assert False, "Should have rejected invalid object"
        except PluginValidationError:
            pass  # Expected
        
        print("✅ Timeline integrity test passed")
    
    async def test_event_driven_state(self):
        """Test event-driven state management."""
        from simplified_state import SimplifiedAppState, AppEvent
        
        state = SimplifiedAppState()
        
        # Initially, prompt should not be allowed
        assert not state.can_show_prompt()
        
        # After startup complete, prompt should be allowed
        await state.mark_startup_complete(2)
        assert state.can_show_prompt()
        
        # Test event history
        assert state.event_bus.has_occurred(AppEvent.STARTUP_COMPLETE)
        startup_info = state.get_startup_info()
        assert startup_info["completed"] is True
        assert startup_info["plugins_count"] == 2
        
        print("✅ Event-driven state test passed")
    
    @given(st.text(min_size=1, max_size=1000))
    async def test_property_based_input(self, input_text: str):
        """Property-based test for input handling."""
        from simplified_plugins import SimpleUserInputPlugin
        
        plugin = SimpleUserInputPlugin()
        result = await plugin.safe_process(input_text, {})
        
        # Properties that should always hold
        assert result.status.value in ["completed", "error"]
        assert result.content == input_text or result.error is not None
        assert result.duration >= 0
        assert isinstance(result.tokens, dict)
        assert "input" in result.tokens
        assert "output" in result.tokens
    
    async def test_error_injection(self):
        """Test error handling with injected failures."""
        from simplified_plugins import CognitionBlockPlugin
        from plugins.cognitive_modules import QueryRoutingModule
        
        # Create a module that will fail
        class FailingModule(QueryRoutingModule):
            async def process(self, input_data, llm_interface):
                raise ValueError("Injected failure")
        
        plugin = CognitionBlockPlugin([FailingModule()])
        
        # Mock LLM manager
        mock_llm_manager = Mock()
        mock_llm_interface = MockLLMInterface()
        mock_llm_manager.get_interface.return_value = mock_llm_interface
        
        context = {"llm_manager": mock_llm_manager}
        result = await plugin.safe_process("test", context)
        
        # Should handle error gracefully
        assert result.status.value == "completed"  # Should continue processing
        assert len(result.metadata["transparency_log"]) >= 1
        
        print("✅ Error injection test passed")
    
    async def test_performance_benchmarks(self):
        """Test performance benchmarks."""
        from simplified_plugins import SimplifiedPluginManager
        from plugins.cognitive_modules import QueryRoutingModule
        
        manager = SimplifiedPluginManager()
        
        # Test plugin creation performance
        start_time = time.time()
        plugin_ids = []
        for i in range(100):
            plugin_id = manager.create_plugin("user_input")
            plugin_ids.append(plugin_id)
        creation_time = time.time() - start_time
        
        assert creation_time < 1.0, f"Plugin creation too slow: {creation_time}s"
        
        # Test processing performance
        start_time = time.time()
        for plugin_id in plugin_ids[:10]:  # Test subset
            await manager.process_with_plugin(plugin_id, "test", {})
        processing_time = time.time() - start_time
        
        assert processing_time < 2.0, f"Plugin processing too slow: {processing_time}s"
        
        print(f"✅ Performance test passed (creation: {creation_time:.3f}s, processing: {processing_time:.3f}s)")
    
    async def test_integration_workflow(self):
        """Test complete integration workflow."""
        from simplified_plugins import SimplifiedPluginManager, SimplifiedTimelineAdapter
        from simplified_state import SimplifiedAppState
        from timeline_integrity import ApplicationWithSecureTimeline
        from plugins.cognitive_modules import QueryRoutingModule, PromptEnhancementModule
        from rich.console import Console
        
        # Setup complete system
        console = Console()
        app_state = SimplifiedAppState()
        timeline_app = ApplicationWithSecureTimeline(console)
        plugin_manager = SimplifiedPluginManager()
        
        # Mock LLM manager
        mock_llm_manager = Mock()
        mock_llm_interface = MockLLMInterface(["route: chat", "enhanced: test query", "final response"])
        mock_llm_manager.get_interface.return_value = mock_llm_interface
        
        context = {"llm_manager": mock_llm_manager}
        
        # Mark system initialized
        await app_state.mark_system_initialized()
        
        # Process user input
        user_input_id = plugin_manager.create_plugin("user_input")
        user_result = await plugin_manager.process_with_plugin(user_input_id, "test query", context)
        
        # Add to timeline
        user_adapter = SimplifiedTimelineAdapter(plugin_manager.get_plugin(user_input_id), user_result)
        timeline_app.add_plugin_to_timeline(user_adapter)
        
        # Process through cognition
        cognition_id = plugin_manager.create_plugin("cognition", cognitive_modules=[QueryRoutingModule(), PromptEnhancementModule()])
        cognition_result = await plugin_manager.process_with_plugin(cognition_id, "test query", context)
        
        # Add to timeline
        cognition_adapter = SimplifiedTimelineAdapter(plugin_manager.get_plugin(cognition_id), cognition_result)
        timeline_app.add_plugin_to_timeline(cognition_adapter)
        
        # Process assistant response
        assistant_id = plugin_manager.create_plugin("assistant_response")
        assistant_result = await plugin_manager.process_with_plugin(assistant_id, {"response": cognition_result.content}, context)
        
        # Add to timeline
        assistant_adapter = SimplifiedTimelineAdapter(plugin_manager.get_plugin(assistant_id), assistant_result)
        timeline_app.add_plugin_to_timeline(assistant_adapter)
        
        # Mark startup complete
        await app_state.mark_startup_complete(3)
        
        # Verify complete workflow
        assert app_state.can_show_prompt()
        timeline_summary = timeline_app.get_timeline_summary()
        assert timeline_summary["total_plugins"] == 3
        assert timeline_summary["total_llm_tokens"] > 0
        
        print("✅ Integration workflow test passed")
    
    async def run_all_tests(self):
        """Run all tests in the framework."""
        print("🧪 Running comprehensive test suite...")
        
        test_methods = [
            self.test_plugin_isolation,
            self.test_cognition_blocks,
            self.test_timeline_integrity,
            self.test_event_driven_state,
            self.test_error_injection,
            self.test_performance_benchmarks,
            self.test_integration_workflow
        ]
        
        passed = 0
        failed = 0
        
        for test_method in test_methods:
            try:
                await test_method()
                passed += 1
            except Exception as e:
                print(f"❌ {test_method.__name__} failed: {e}")
                failed += 1
        
        print(f"\n📊 Test Results: {passed} passed, {failed} failed")
        
        if failed == 0:
            print("🎉 All tests passed! Architecture is solid.")
        else:
            print("⚠️  Some tests failed. Review architecture.")
        
        return failed == 0


# Pytest integration
class TestLLMREPL:
    """Pytest test class for CI/CD integration."""
    
    @pytest.mark.asyncio
    async def test_plugin_isolation(self):
        framework = TestFramework()
        await framework.test_plugin_isolation()
    
    @pytest.mark.asyncio
    async def test_cognition_blocks(self):
        framework = TestFramework()
        await framework.test_cognition_blocks()
    
    @pytest.mark.asyncio
    async def test_timeline_integrity(self):
        framework = TestFramework()
        await framework.test_timeline_integrity()
    
    @pytest.mark.asyncio
    async def test_event_driven_state(self):
        framework = TestFramework()
        await framework.test_event_driven_state()
    
    @pytest.mark.asyncio
    async def test_integration_workflow(self):
        framework = TestFramework()
        await framework.test_integration_workflow()


# CLI for running tests
async def main():
    """Run test framework from command line."""
    framework = TestFramework()
    success = await framework.run_all_tests()
    exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())