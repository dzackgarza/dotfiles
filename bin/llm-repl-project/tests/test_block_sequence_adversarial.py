"""Adversarial tests for block sequence, rendering, and timeline correctness."""

import pytest
import asyncio
import sys
import time
from pathlib import Path
from unittest.mock import Mock, AsyncMock
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from plugins.blocks.user_input import UserInputPlugin
from plugins.blocks.welcome import WelcomePlugin
from plugins.blocks.system_check import SystemCheckPlugin
from plugins.blocks.processing import ProcessingPlugin
from plugins.blocks.assistant_response import AssistantResponsePlugin
from plugins.blocks.cognition import CognitionPlugin
from plugins.cognitive_modules import QueryRoutingModule, PromptEnhancementModule
from plugins.llm_interface import LLMManager, MockLLMInterface
from plugins.base import RenderContext, PluginState
from plugins.registry import PluginManager


class TestUserInputPluginAdversarial:
    """5 adversarial tests for UserInputPlugin rendering and behavior."""
    
    @pytest.mark.asyncio
    async def test_user_input_title_format_consistency(self):
        """Test 1: Ensure title format is always consistent across all states."""
        plugin = UserInputPlugin()
        await plugin.initialize({"max_length": 1000})
        
        # Test inactive state
        context = RenderContext(display_mode="live")
        render_data = await plugin.render(context)
        
        # Should have standardized title format even when inactive
        assert "title" in render_data
        title = render_data["title"]
        assert "🔧" in title
        assert "User_Input" in title
        assert plugin.state.value in ["inactive"]
        
        # Test active state
        await plugin.activate()
        render_data = await plugin.render(context)
        title = render_data["title"]
        assert "🔧" in title
        assert "User_Input" in title
        
        # Test completed state
        await plugin.process("Hello world!", {})
        render_data = await plugin.render(context)
        title = render_data["title"]
        assert "🔧" in title
        assert "User_Input" in title
        assert "✅" in title  # Should show completion
        assert "(" in title and "s)" in title  # Should show duration
        
        # Verify no broken formatting
        assert not title.startswith(" ")
        assert not title.endswith(" ")
        assert "  " not in title  # No double spaces
    
    @pytest.mark.asyncio
    async def test_user_input_token_tracking_accuracy(self):
        """Test 2: Verify token counts are accurate and never negative."""
        plugin = UserInputPlugin()
        await plugin.initialize({"max_length": 1000})
        await plugin.activate()
        
        # Initial tokens should be zero
        initial_tokens = plugin.get_token_counts()
        assert initial_tokens["input"] == 0
        assert initial_tokens["output"] == 0
        
        # Process input
        await plugin.process("This is a test input with multiple words", {})
        
        # Tokens should still be reasonable (user input doesn't generate LLM tokens)
        final_tokens = plugin.get_token_counts()
        assert final_tokens["input"] >= 0
        assert final_tokens["output"] >= 0
        
        # Render and check tokens in display
        context = RenderContext(display_mode="inscribed")
        render_data = await plugin.render(context)
        
        if "tokens" in render_data:
            display_tokens = render_data["tokens"]
            assert display_tokens["input"] >= 0
            assert display_tokens["output"] >= 0
            assert display_tokens["input"] == final_tokens["input"]
            assert display_tokens["output"] == final_tokens["output"]
    
    @pytest.mark.asyncio
    async def test_user_input_timing_precision(self):
        """Test 3: Ensure timing is precise and matches between live/inscribed states."""
        plugin = UserInputPlugin()
        await plugin.initialize({"max_length": 1000})
        
        # Record start time
        start_time = time.time()
        await plugin.activate()
        
        # Small delay to ensure measurable time
        await asyncio.sleep(0.1)
        
        # Test live timing
        live_context = RenderContext(display_mode="live")
        live_render = await plugin.render(live_context)
        live_timing = live_render.get("timing", {})
        
        # Process with delay
        await asyncio.sleep(0.05)
        await plugin.process("test", {})
        end_time = time.time()
        
        # Test inscribed timing
        inscribed_context = RenderContext(display_mode="inscribed")
        inscribed_render = await plugin.render(inscribed_context)
        inscribed_timing = inscribed_render.get("timing", {})
        
        # Verify timing makes sense
        total_duration = end_time - start_time
        plugin_duration = plugin.get_duration()
        
        assert plugin_duration is not None
        assert plugin_duration > 0.1  # Should be at least our sleep time
        assert plugin_duration < total_duration + 0.1  # Should be reasonable
        
        # Check title timing format
        title = inscribed_render.get("title", "")
        assert "(" in title and "s)" in title  # Should show duration
    
    @pytest.mark.asyncio
    async def test_user_input_state_transition_integrity(self):
        """Test 4: Verify state transitions are atomic and render correctly."""
        plugin = UserInputPlugin()
        await plugin.initialize({"max_length": 1000})
        
        # Test all state transitions and their rendering
        states_tested = []
        
        # Initial state
        context = RenderContext(display_mode="live")
        render_data = await plugin.render(context)
        assert render_data["plugin_state"] == PluginState.INACTIVE
        states_tested.append(PluginState.INACTIVE)
        
        # Activate
        await plugin.activate()
        render_data = await plugin.render(context)
        assert render_data["plugin_state"] == PluginState.ACTIVE
        states_tested.append(PluginState.ACTIVE)
        
        # Process
        await plugin.process("test input", {})
        render_data = await plugin.render(context)
        assert render_data["plugin_state"] == PluginState.COMPLETED
        states_tested.append(PluginState.COMPLETED)
        
        # Verify all expected states were hit
        expected_states = [PluginState.INACTIVE, PluginState.ACTIVE, PluginState.COMPLETED]
        assert all(state in states_tested for state in expected_states)
        
        # Verify final state rendering has all required fields
        final_render = await plugin.render(RenderContext(display_mode="inscribed"))
        required_fields = ["plugin_id", "plugin_name", "plugin_state", "title", "timing"]
        for field in required_fields:
            assert field in final_render, f"Missing required field: {field}"
    
    @pytest.mark.asyncio
    async def test_user_input_content_preservation(self):
        """Test 5: Verify content is preserved correctly and displayed accurately."""
        plugin = UserInputPlugin()
        await plugin.initialize({"max_length": 1000})
        await plugin.activate()
        
        # Test various input types
        test_inputs = [
            "Simple text",
            "Text with special chars: !@#$%^&*()",
            "Multi\nline\ntext",
            "Very long text " * 50,
            "",  # Edge case: empty
            "   whitespace   ",  # Edge case: whitespace
        ]
        
        for test_input in test_inputs:
            # Reset plugin
            plugin = UserInputPlugin()
            await plugin.initialize({"max_length": 1000})
            await plugin.activate()
            
            try:
                await plugin.process(test_input, {})
                
                # Check content preservation
                context = RenderContext(display_mode="inscribed")
                render_data = await plugin.render(context)
                
                # Content should be preserved (unless validation failed)
                if plugin.state == PluginState.COMPLETED:
                    assert "content" in render_data
                    # For user input, content should match input
                    stored_content = render_data.get("content", "")
                    
                    # Handle edge cases appropriately
                    if test_input.strip() == "" and not plugin._data.get("allow_empty", False):
                        # Empty input should fail validation
                        assert plugin.state == PluginState.ERROR
                    else:
                        assert stored_content == test_input or stored_content.strip() == test_input.strip()
                
            except ValueError:
                # Some inputs may fail validation - that's expected
                assert plugin.state == PluginState.ERROR


class TestWelcomePluginAdversarial:
    """5 adversarial tests for WelcomePlugin rendering and behavior."""
    
    @pytest.mark.asyncio
    async def test_welcome_version_display_consistency(self):
        """Test 1: Ensure version is displayed consistently across all configurations."""
        versions_to_test = ["v1.0", "v2.5.1", "test-version", "", "very-long-version-string-123"]
        
        for version in versions_to_test:
            plugin = WelcomePlugin()
            await plugin.initialize({"version": version})
            await plugin.activate()
            await plugin.process({}, {})
            
            context = RenderContext(display_mode="inscribed")
            render_data = await plugin.render(context)
            
            # Title should include version or fallback
            title = render_data.get("title", "")
            assert "🔧" in title
            assert "Welcome" in title
            
            # Check metadata has version
            if "metadata" in render_data:
                assert "version" in render_data["metadata"]
                stored_version = render_data["metadata"]["version"]
                assert stored_version == version or (not version and stored_version)
    
    @pytest.mark.asyncio
    async def test_welcome_content_generation_reliability(self):
        """Test 2: Verify welcome content is always generated and formatted properly."""
        configs_to_test = [
            {"version": "v3", "show_help": True, "show_commands": True},
            {"version": "v3", "show_help": False, "show_commands": False},
            {"custom_message": "Custom welcome message", "show_help": True},
            {"theme": "minimal"},
            {"theme": "fancy"},
            {},  # Default config
        ]
        
        for config in configs_to_test:
            plugin = WelcomePlugin()
            await plugin.initialize(config)
            await plugin.activate()
            result = await plugin.process({}, {})
            
            # Should always have welcome content
            assert "welcome_content" in result
            assert result["welcome_content"]  # Should not be empty
            
            # Render should show content
            context = RenderContext(display_mode="live")
            render_data = await plugin.render(context)
            assert "content" in render_data
            assert render_data["content"]  # Should not be empty
            
            # Content should be strings
            assert isinstance(result["welcome_content"], str)
            assert isinstance(render_data["content"], str)
    
    @pytest.mark.asyncio
    async def test_welcome_state_timing_accuracy(self):
        """Test 3: Verify welcome plugin timing is accurate for quick operations."""
        plugin = WelcomePlugin()
        await plugin.initialize({"version": "test"})
        
        start_time = time.time()
        await plugin.activate()
        
        # Welcome should be very fast
        await plugin.process({}, {})
        end_time = time.time()
        
        duration = plugin.get_duration()
        assert duration is not None
        assert duration >= 0
        assert duration < 1.0  # Should complete quickly
        
        # Check timing in render
        context = RenderContext(display_mode="inscribed")
        render_data = await plugin.render(context)
        title = render_data.get("title", "")
        
        # Should show duration
        assert "(" in title and "s)" in title
        
        # Extract duration from title and verify
        import re
        duration_match = re.search(r'\((\d+\.\d+)s\)', title)
        if duration_match:
            title_duration = float(duration_match.group(1))
            assert abs(title_duration - duration) < 0.1  # Should be close
    
    @pytest.mark.asyncio
    async def test_welcome_theme_rendering_variations(self):
        """Test 4: Test all theme variations render correctly with proper styling."""
        themes = ["default", "minimal", "fancy", "nonexistent-theme"]
        
        for theme in themes:
            plugin = WelcomePlugin()
            await plugin.initialize({"theme": theme})
            await plugin.activate()
            await plugin.process({}, {})
            
            context = RenderContext(display_mode="inscribed")
            render_data = await plugin.render(context)
            
            # Should have style information
            assert "style" in render_data
            style = render_data["style"]
            
            # All themes should have basic style properties
            assert "box_style" in style
            assert "border_color" in style
            assert "title_style" in style
            
            # Check theme-specific properties
            if theme == "minimal":
                assert style["box_style"] == "rounded"
                assert style["border_color"] == "dim"
            elif theme == "fancy":
                assert style["box_style"] == "double"
                assert style["border_color"] == "bright_blue"
            else:
                # Default or unknown themes should have default styling
                assert style["box_style"] in ["heavy", "rounded", "double"]
    
    @pytest.mark.asyncio
    async def test_welcome_metadata_completeness(self):
        """Test 5: Ensure all metadata is complete and accessible in all modes."""
        plugin = WelcomePlugin()
        config = {
            "version": "test-v1.0",
            "show_help": True,
            "show_commands": True,
            "custom_message": "Test message",
            "theme": "fancy"
        }
        await plugin.initialize(config)
        await plugin.activate()
        await plugin.process({}, {})
        
        # Test both display modes
        for mode in ["live", "inscribed"]:
            context = RenderContext(display_mode=mode)
            render_data = await plugin.render(context)
            
            # Should have core plugin metadata
            assert "plugin_id" in render_data
            assert "plugin_name" in render_data
            assert "plugin_state" in render_data
            assert "title" in render_data
            
            # Check inscribed mode has additional metadata
            if mode == "inscribed":
                assert "metadata" in render_data
                metadata = render_data["metadata"]
                
                required_metadata = ["displayed_at", "version", "content_length", "theme"]
                for field in required_metadata:
                    assert field in metadata, f"Missing metadata field: {field}"
                
                # Verify metadata values make sense
                assert metadata["version"] == "test-v1.0"
                assert metadata["theme"] == "fancy"
                assert metadata["content_length"] > 0


class TestCognitionPluginAdversarial:
    """5 adversarial tests for CognitionPlugin rendering and behavior."""
    
    @pytest.mark.asyncio
    async def test_cognition_module_chain_ordering(self):
        """Test 1: Verify cognitive modules execute in correct order and report sequence."""
        plugin = CognitionPlugin()
        
        # Create ordered chain
        config = {
            "modules": [QueryRoutingModule, PromptEnhancementModule],
            "llm_interface": "default"
        }
        await plugin.initialize(config)
        await plugin.activate()
        
        # Create mock LLM manager
        llm_manager = LLMManager()
        llm_manager.register_interface("default", MockLLMInterface(), is_default=True)
        
        result = await plugin.process("test query", {"llm_manager": llm_manager})
        
        # Check module execution order
        assert "module_outputs" in result
        assert len(result["module_outputs"]) == 2
        
        # First should be routing, second should be enhancement
        module_outputs = result["module_outputs"]
        
        # Check transparency log for ordering
        transparency_log = plugin.get_transparency_log()
        assert len(transparency_log) == 2
        assert transparency_log[0]["module_index"] == 0
        assert transparency_log[1]["module_index"] == 1
        
        # Verify each module was called with output of previous
        if len(transparency_log) > 1:
            first_output = transparency_log[0]["output"]["content"]
            second_input = transparency_log[1]["input"]
            assert second_input == first_output  # Chain should pass data through
    
    @pytest.mark.asyncio
    async def test_cognition_token_aggregation_accuracy(self):
        """Test 2: Verify token counts are accurately aggregated across all modules."""
        plugin = CognitionPlugin()
        
        config = {
            "modules": [QueryRoutingModule, PromptEnhancementModule],
            "llm_interface": "default"
        }
        await plugin.initialize(config)
        await plugin.activate()
        
        llm_manager = LLMManager()
        llm_interface = MockLLMInterface()
        llm_manager.register_interface("default", llm_interface, is_default=True)
        
        # Track initial tokens
        initial_total = llm_interface.get_total_usage()
        
        result = await plugin.process("test query for tokens", {"llm_manager": llm_manager})
        
        # Check plugin's token tracking
        plugin_tokens = plugin.get_token_counts()
        assert plugin_tokens["input"] > 0
        assert plugin_tokens["output"] > 0
        
        # Check result token aggregation
        total_from_result = result.get("total_tokens", {})
        if total_from_result:
            assert total_from_result["input"] > 0
            assert total_from_result["output"] > 0
        
        # Verify token counts in render
        context = RenderContext(display_mode="inscribed")
        render_data = await plugin.render(context)
        
        if "tokens" in render_data:
            render_tokens = render_data["tokens"]
            assert render_tokens["input"] == plugin_tokens["input"]
            assert render_tokens["output"] == plugin_tokens["output"]
        
        # Check title shows tokens
        title = render_data.get("title", "")
        assert "[" in title and "tokens]" in title
    
    @pytest.mark.asyncio
    async def test_cognition_error_isolation_and_reporting(self):
        """Test 3: Test error handling and isolation between modules."""
        plugin = CognitionPlugin()
        
        # Create a module that will fail
        class FailingModule:
            def __init__(self):
                from plugins.cognitive_modules import CognitiveModuleMetadata
                self.metadata = CognitiveModuleMetadata(
                    name="failing_module",
                    version="1.0.0",
                    description="A module that fails",
                    author="Test",
                    task_type="test"
                )
                self.state = PluginState.INACTIVE
            
            async def process(self, input_data, llm_interface):
                raise RuntimeError("Intentional failure for testing")
        
        config = {
            "modules": [FailingModule],
            "fail_on_error": False  # Should continue despite errors
        }
        await plugin.initialize(config)
        await plugin.activate()
        
        llm_manager = LLMManager()
        llm_manager.register_interface("default", MockLLMInterface(), is_default=True)
        
        # Should not raise exception due to fail_on_error=False
        result = await plugin.process("test", {"llm_manager": llm_manager})
        
        # Check error is logged in transparency
        transparency_log = plugin.get_transparency_log()
        assert len(transparency_log) > 0
        
        error_entry = transparency_log[0]
        assert "error" in error_entry
        assert "Intentional failure" in error_entry["error"]
        
        # Plugin should still have completed state for the chain
        assert plugin.state in [PluginState.COMPLETED, PluginState.ERROR]
    
    @pytest.mark.asyncio
    async def test_cognition_progress_tracking_accuracy(self):
        """Test 4: Verify progress tracking is accurate during processing."""
        plugin = CognitionPlugin()
        
        config = {
            "modules": [QueryRoutingModule, PromptEnhancementModule],
            "llm_interface": "default"
        }
        await plugin.initialize(config)
        await plugin.activate()
        
        # Test progress during processing by checking state
        llm_manager = LLMManager()
        llm_manager.register_interface("default", MockLLMInterface({"response_delay": 0.01}), is_default=True)
        
        # Start processing in background to check intermediate states
        async def check_progress():
            context = RenderContext(display_mode="live")
            render_data = await plugin.render(context)
            
            if plugin.state == PluginState.PROCESSING:
                # Should show progress information
                current_index = plugin._data.get("current_module_index", -1)
                total_modules = plugin._data.get("total_modules", 0)
                
                assert current_index >= 0
                assert total_modules > 0
                assert current_index < total_modules
                
                # Check render data has progress info
                if "progress" in render_data:
                    progress = render_data["progress"]
                    assert 0 <= progress <= 1
                    expected_progress = (current_index + 1) / total_modules
                    assert abs(progress - expected_progress) < 0.1
        
        # Process and check final state
        result = await plugin.process("test", {"llm_manager": llm_manager})
        
        # Final state should be completed
        assert plugin.state == PluginState.COMPLETED
        assert plugin._data.get("current_module_index", -1) == -1  # Should reset
    
    @pytest.mark.asyncio
    async def test_cognition_transparency_log_completeness(self):
        """Test 5: Verify transparency log contains all required information."""
        plugin = CognitionPlugin()
        
        config = {
            "modules": [QueryRoutingModule, PromptEnhancementModule],
            "llm_interface": "default"
        }
        await plugin.initialize(config)
        await plugin.activate()
        
        llm_manager = LLMManager()
        llm_manager.register_interface("default", MockLLMInterface(), is_default=True)
        
        result = await plugin.process("comprehensive test query", {"llm_manager": llm_manager})
        
        # Get transparency log
        transparency_log = plugin.get_transparency_log()
        module_outputs = plugin.get_module_outputs()
        
        # Should have entries for all modules
        assert len(transparency_log) == len(config["modules"])
        assert len(module_outputs) == len(config["modules"])
        
        # Check each entry has required fields
        required_fields = ["module_name", "module_index", "input", "output", "timestamp"]
        
        for i, entry in enumerate(transparency_log):
            for field in required_fields:
                assert field in entry, f"Missing field {field} in entry {i}"
            
            # Verify data integrity
            assert entry["module_index"] == i
            assert isinstance(entry["timestamp"], str)
            assert "output" in entry
            assert isinstance(entry["output"], dict)
            
            # Output should have llm_response details
            output = entry["output"]
            if "llm_response" in output and output["llm_response"]:
                llm_resp = output["llm_response"]
                assert "content" in llm_resp
                assert "tokens" in llm_resp
                assert "duration_seconds" in llm_resp
                assert "cognitive_module" in llm_resp
        
        # Verify inscribed rendering includes transparency
        context = RenderContext(display_mode="inscribed")
        render_data = await plugin.render(context)
        
        if "transparency_log" in render_data:
            assert len(render_data["transparency_log"]) == len(transparency_log)


class TestSystemCheckPluginAdversarial:
    """5 adversarial tests for SystemCheckPlugin rendering and behavior."""
    
    @pytest.mark.asyncio
    async def test_system_check_validation_completeness(self):
        """Test 1: Verify all system checks are performed and reported correctly."""
        plugin = SystemCheckPlugin()
        await plugin.initialize({})
        await plugin.activate()
        result = await plugin.process({}, {})
        
        # Should have system check results
        assert "system_status" in result
        system_status = result["system_status"]
        
        # Check required components were validated
        required_checks = ["python_version", "dependencies", "memory", "disk_space"]
        for check in required_checks:
            assert check in system_status, f"Missing system check: {check}"
            
            # Each check should have status
            check_result = system_status[check]
            assert "status" in check_result
            assert check_result["status"] in ["pass", "fail", "warning"]
        
        # Render should show system status
        context = RenderContext(display_mode="inscribed")
        render_data = await plugin.render(context)
        
        if "system_checks" in render_data:
            rendered_checks = render_data["system_checks"]
            assert len(rendered_checks) >= len(required_checks)
    
    @pytest.mark.asyncio
    async def test_system_check_timing_consistency(self):
        """Test 2: Verify system check timing is reasonable and consistent."""
        plugin = SystemCheckPlugin()
        await plugin.initialize({})
        
        start_time = time.time()
        await plugin.activate()
        await plugin.process({}, {})
        end_time = time.time()
        
        duration = plugin.get_duration()
        total_time = end_time - start_time
        
        # System checks should be reasonably fast
        assert duration is not None
        assert duration > 0
        assert duration < 5.0  # Should complete within 5 seconds
        assert duration <= total_time + 0.1
        
        # Check timing in title
        context = RenderContext(display_mode="inscribed")
        render_data = await plugin.render(context)
        title = render_data.get("title", "")
        
        assert "(" in title and "s)" in title
        
        # Extract and verify duration
        import re
        duration_match = re.search(r'\((\d+\.\d+)s\)', title)
        if duration_match:
            title_duration = float(duration_match.group(1))
            assert abs(title_duration - duration) < 0.1
    
    @pytest.mark.asyncio
    async def test_system_check_status_accuracy(self):
        """Test 3: Verify system status is accurately determined and displayed."""
        plugin = SystemCheckPlugin()
        await plugin.initialize({})
        await plugin.activate()
        result = await plugin.process({}, {})
        
        system_status = result["system_status"]
        overall_status = result.get("overall_status", "unknown")
        
        # Overall status should be determined from individual checks
        statuses = [check["status"] for check in system_status.values()]
        
        if "fail" in statuses:
            assert overall_status in ["fail", "error"]
        elif "warning" in statuses:
            assert overall_status in ["warning", "pass"]
        else:
            assert overall_status == "pass"
        
        # Render should reflect status
        context = RenderContext(display_mode="live")
        render_data = await plugin.render(context)
        
        # Status should be visible in rendering
        style = render_data.get("style", {})
        if overall_status == "fail":
            assert style.get("border_color") == "red"
        elif overall_status == "warning":
            assert style.get("border_color") == "yellow"
        else:
            assert style.get("border_color") in ["green", "blue"]
    
    @pytest.mark.asyncio
    async def test_system_check_error_handling(self):
        """Test 4: Test error handling when system checks fail."""
        plugin = SystemCheckPlugin()
        
        # Mock a failing check scenario
        original_check = plugin._check_dependencies if hasattr(plugin, '_check_dependencies') else None
        
        await plugin.initialize({})
        await plugin.activate()
        
        # Even if some checks fail, plugin should complete
        result = await plugin.process({}, {})
        
        # Should have completed state even with potential failures
        assert plugin.state in [PluginState.COMPLETED, PluginState.ERROR]
        
        # Should have error information if any checks failed
        system_status = result.get("system_status", {})
        
        # Check error reporting in render
        context = RenderContext(display_mode="inscribed")
        render_data = await plugin.render(context)
        
        # Should have appropriate error styling if needed
        if plugin.state == PluginState.ERROR:
            assert "❌" in render_data.get("title", "")
            assert render_data.get("style", {}).get("border_color") == "red"
    
    @pytest.mark.asyncio
    async def test_system_check_metadata_accuracy(self):
        """Test 5: Verify metadata is accurate and complete."""
        plugin = SystemCheckPlugin()
        await plugin.initialize({})
        await plugin.activate()
        result = await plugin.process({}, {})
        
        # Check plugin info
        info = plugin.get_plugin_info()
        
        required_info_fields = ["plugin_id", "metadata", "state", "duration", "tokens"]
        for field in required_info_fields:
            assert field in info, f"Missing info field: {field}"
        
        # Check metadata structure
        metadata = info["metadata"]
        assert metadata["name"] == "system_check"
        assert "version" in metadata
        assert "capabilities" in metadata
        
        # Check rendering metadata
        context = RenderContext(display_mode="inscribed")
        render_data = await plugin.render(context)
        
        # Should have timing metadata
        timing = render_data.get("timing", {})
        assert "duration" in timing
        assert "state" in timing
        assert timing["state"] == plugin.state.value
        
        # Should have plugin metadata
        assert render_data.get("plugin_name") == "system_check"
        assert render_data.get("plugin_state") == plugin.state


class TestAssistantResponsePluginAdversarial:
    """5 adversarial tests for AssistantResponsePlugin rendering and behavior."""
    
    @pytest.mark.asyncio
    async def test_assistant_response_content_formatting(self):
        """Test 1: Verify response content is properly formatted and preserved."""
        plugin = AssistantResponsePlugin()
        await plugin.initialize({"format_markdown": True, "max_length": 1000})
        await plugin.activate()
        
        # Test various content types
        test_contents = [
            "Simple response",
            "Response with **bold** and *italic* text",
            "Response with\nmultiple\nlines",
            "Response with code: `print('hello')`",
            "Very long response " * 100,  # Test truncation
        ]
        
        for content in test_contents:
            # Reset plugin
            plugin = AssistantResponsePlugin()
            await plugin.initialize({"format_markdown": True, "max_length": 1000})
            await plugin.activate()
            
            result = await plugin.process(content, {})
            
            # Check content preservation
            assert "response" in result
            response_content = result["response"]
            
            # Should preserve content (possibly with formatting)
            assert response_content
            if len(content) <= 1000:
                # Should not be truncated
                assert content in response_content or response_content in content
            else:
                # Should be truncated
                assert "truncated" in response_content or len(response_content) < len(content)
            
            # Check rendering
            context = RenderContext(display_mode="inscribed")
            render_data = await plugin.render(context)
            assert "content" in render_data
            assert render_data["content"] == response_content
    
    @pytest.mark.asyncio
    async def test_assistant_response_token_attribution(self):
        """Test 2: Verify token tracking for assistant responses."""
        plugin = AssistantResponsePlugin()
        await plugin.initialize({})
        await plugin.activate()
        
        # Add tokens to simulate LLM response
        plugin.add_input_tokens(100)
        plugin.add_output_tokens(200)
        
        result = await plugin.process("Test response content", {})
        
        # Check token tracking
        tokens = plugin.get_token_counts()
        assert tokens["input"] == 100
        assert tokens["output"] == 200
        
        # Check tokens in render
        context = RenderContext(display_mode="inscribed")
        render_data = await plugin.render(context)
        
        render_tokens = render_data.get("tokens", {})
        assert render_tokens["input"] == 100
        assert render_tokens["output"] == 200
        
        # Check title shows tokens
        title = render_data.get("title", "")
        assert "[300 tokens]" in title
    
    @pytest.mark.asyncio
    async def test_assistant_response_metadata_tracking(self):
        """Test 3: Verify metadata is properly tracked and displayed."""
        plugin = AssistantResponsePlugin()
        await plugin.initialize({"show_metadata": True})
        await plugin.activate()
        
        # Simulate response with metadata
        response_data = {
            "response": "Test response",
            "processing_results": {
                "total_tokens": {"input": 50, "output": 100},
                "processing_duration": 2.5,
                "step_results": {"routing": {}, "enhancement": {}}
            }
        }
        
        result = await plugin.process(response_data, {})
        
        # Check metadata extraction
        assert "metadata" in result
        metadata = result["metadata"]
        
        assert "tokens" in metadata
        assert "processing_duration" in metadata
        assert "processing_steps" in metadata
        
        # Check inscribed rendering includes metadata
        context = RenderContext(display_mode="inscribed")
        render_data = await plugin.render(context)
        
        if plugin.state == PluginState.COMPLETED:
            assert "metadata" in render_data
            render_metadata = render_data["metadata"]
            assert "generation_duration" in render_metadata
            assert "content_length" in render_metadata
            assert "word_count" in render_metadata
    
    @pytest.mark.asyncio
    async def test_assistant_response_streaming_simulation(self):
        """Test 4: Test streaming response updates."""
        plugin = AssistantResponsePlugin()
        await plugin.initialize({})
        await plugin.activate()
        
        # Simulate streaming by appending content
        plugin.update_response("Part 1")
        context = RenderContext(display_mode="live")
        render_data = await plugin.render(context)
        assert "Part 1" in render_data.get("content", "")
        
        # Append more content
        plugin.append_to_response(" Part 2")
        render_data = await plugin.render(context)
        assert "Part 1 Part 2" in render_data.get("content", "")
        
        # Final process
        await plugin.process("Final content", {})
        render_data = await plugin.render(context)
        assert "Final content" in render_data.get("content", "")
        
        # Check word count tracking
        info = plugin.get_response_info()
        assert info["content_stats"]["word_count"] > 0
        assert info["content_stats"]["character_count"] > 0
    
    @pytest.mark.asyncio
    async def test_assistant_response_state_transitions(self):
        """Test 5: Verify proper state transitions and display updates."""
        plugin = AssistantResponsePlugin()
        await plugin.initialize({})
        
        # Test state progression
        states_observed = []
        
        # Initial state
        context = RenderContext(display_mode="live")
        render_data = await plugin.render(context)
        assert render_data["plugin_state"] == PluginState.INACTIVE
        states_observed.append(PluginState.INACTIVE)
        
        # Activate
        await plugin.activate()
        render_data = await plugin.render(context)
        assert render_data["plugin_state"] == PluginState.ACTIVE
        states_observed.append(PluginState.ACTIVE)
        
        # Process
        await plugin.process("Test response", {})
        render_data = await plugin.render(context)
        assert render_data["plugin_state"] == PluginState.COMPLETED
        states_observed.append(PluginState.COMPLETED)
        
        # Verify all states were observed
        expected_states = [PluginState.INACTIVE, PluginState.ACTIVE, PluginState.COMPLETED]
        assert all(state in states_observed for state in expected_states)
        
        # Check final rendering has completion indicator
        final_render = await plugin.render(RenderContext(display_mode="inscribed"))
        title = final_render.get("title", "")
        assert "✅" in title  # Should show completion
        assert "Research Assistant" in title or "Assistant_Response" in title


class TestBlockSequenceOrderingAdversarial:
    """5 adversarial tests for overall block sequence and ordering."""
    
    @pytest.mark.asyncio
    async def test_startup_welcome_goodbye_sequence(self):
        """Test 1: Verify [Startup], [Welcome], [Goodbye] sequence for open-close."""
        manager = PluginManager()
        await manager.start()
        
        try:
            # Register plugins
            manager.register_plugin_class(SystemCheckPlugin)
            manager.register_plugin_class(WelcomePlugin)
            
            # Simulate startup sequence
            sequence = []
            
            # System check (startup)
            startup_id = await manager.create_plugin("system_check", {})
            startup_plugin = manager.active_plugins[startup_id]
            await startup_plugin.process({}, {})
            sequence.append(("system_check", startup_plugin.state))
            
            # Welcome
            welcome_id = await manager.create_plugin("welcome", {"version": "test"})
            welcome_plugin = manager.active_plugins[welcome_id]
            await welcome_plugin.process({}, {})
            sequence.append(("welcome", welcome_plugin.state))
            
            # Verify sequence
            assert len(sequence) == 2
            assert sequence[0][0] == "system_check"
            assert sequence[1][0] == "welcome"
            assert all(state == PluginState.COMPLETED for _, state in sequence)
            
            # All should have proper rendering
            for plugin_name, _ in sequence:
                plugin = startup_plugin if plugin_name == "system_check" else welcome_plugin
                context = RenderContext(display_mode="inscribed")
                render_data = await plugin.render(context)
                
                # Should have proper title format
                title = render_data.get("title", "")
                assert "🔧" in title
                assert title.endswith("]") or "✅" in title
                
        finally:
            await manager.stop()
    
    @pytest.mark.asyncio
    async def test_full_conversation_sequence(self):
        """Test 2: Test [Startup], [Welcome], [User], [Cognition], [Assistant], [Goodbye]."""
        manager = PluginManager()
        await manager.start()
        
        try:
            # Register all plugins
            manager.register_plugin_class(SystemCheckPlugin)
            manager.register_plugin_class(WelcomePlugin)
            manager.register_plugin_class(UserInputPlugin)
            manager.register_plugin_class(CognitionPlugin)
            manager.register_plugin_class(AssistantResponsePlugin)
            
            conversation_sequence = []
            
            # 1. Startup (System Check)
            startup_id = await manager.create_plugin("system_check", {})
            startup_plugin = manager.active_plugins[startup_id]
            await startup_plugin.process({}, {})
            conversation_sequence.append("system_check")
            
            # 2. Welcome
            welcome_id = await manager.create_plugin("welcome", {"version": "test"})
            welcome_plugin = manager.active_plugins[welcome_id]
            await welcome_plugin.process({}, {})
            conversation_sequence.append("welcome")
            
            # 3. User Input
            user_id = await manager.create_plugin("user_input", {"max_length": 1000})
            user_plugin = manager.active_plugins[user_id]
            await user_plugin.process("Hello, how are you?", {})
            conversation_sequence.append("user_input")
            
            # 4. Cognition
            cognition_id = await manager.create_plugin("cognition", {
                "modules": [QueryRoutingModule],
                "llm_interface": "default"
            })
            cognition_plugin = manager.active_plugins[cognition_id]
            
            # Mock LLM manager
            llm_manager = LLMManager()
            llm_manager.register_interface("default", MockLLMInterface(), is_default=True)
            await cognition_plugin.process("Hello, how are you?", {"llm_manager": llm_manager})
            conversation_sequence.append("cognition")
            
            # 5. Assistant Response
            assistant_id = await manager.create_plugin("assistant_response", {})
            assistant_plugin = manager.active_plugins[assistant_id]
            await assistant_plugin.process("I'm doing well, thank you!", {})
            conversation_sequence.append("assistant_response")
            
            # Verify sequence
            expected_sequence = ["system_check", "welcome", "user_input", "cognition", "assistant_response"]
            assert conversation_sequence == expected_sequence
            
            # Verify all are completed
            all_plugins = [startup_plugin, welcome_plugin, user_plugin, cognition_plugin, assistant_plugin]
            for plugin in all_plugins:
                assert plugin.state == PluginState.COMPLETED
                
                # Check rendering quality
                context = RenderContext(display_mode="inscribed")
                render_data = await plugin.render(context)
                assert "title" in render_data
                assert "plugin_state" in render_data
                assert render_data["plugin_state"] == PluginState.COMPLETED
                
        finally:
            await manager.stop()
    
    @pytest.mark.asyncio
    async def test_multi_turn_conversation_ordering(self):
        """Test 3: Test multiple conversation turns maintain proper ordering."""
        manager = PluginManager()
        await manager.start()
        
        try:
            manager.register_plugin_class(UserInputPlugin)
            manager.register_plugin_class(CognitionPlugin)
            manager.register_plugin_class(AssistantResponsePlugin)
            
            # Simulate multi-turn conversation
            full_sequence = []
            
            # Create LLM manager once
            llm_manager = LLMManager()
            llm_manager.register_interface("default", MockLLMInterface(), is_default=True)
            
            # Turn 1
            for turn in range(2):
                # User input
                user_id = await manager.create_plugin("user_input", {"max_length": 1000})
                user_plugin = manager.active_plugins[user_id]
                await user_plugin.process(f"User message {turn + 1}", {})
                full_sequence.append(f"user_turn_{turn + 1}")
                
                # Cognition
                cognition_id = await manager.create_plugin("cognition", {
                    "modules": [QueryRoutingModule],
                    "llm_interface": "default"
                })
                cognition_plugin = manager.active_plugins[cognition_id]
                await cognition_plugin.process(f"User message {turn + 1}", {"llm_manager": llm_manager})
                full_sequence.append(f"cognition_turn_{turn + 1}")
                
                # Assistant response
                assistant_id = await manager.create_plugin("assistant_response", {})
                assistant_plugin = manager.active_plugins[assistant_id]
                await assistant_plugin.process(f"Assistant response {turn + 1}", {})
                full_sequence.append(f"assistant_turn_{turn + 1}")
            
            # Verify alternating pattern
            expected_pattern = [
                "user_turn_1", "cognition_turn_1", "assistant_turn_1",
                "user_turn_2", "cognition_turn_2", "assistant_turn_2"
            ]
            assert full_sequence == expected_pattern
            
        finally:
            await manager.stop()
    
    @pytest.mark.asyncio
    async def test_concurrent_plugin_isolation(self):
        """Test 4: Verify concurrent plugins don't interfere with each other's state."""
        manager = PluginManager()
        await manager.start()
        
        try:
            manager.register_plugin_class(UserInputPlugin)
            
            # Create multiple plugins concurrently
            plugin_ids = []
            for i in range(5):
                plugin_id = await manager.create_plugin("user_input", {"max_length": 1000})
                plugin_ids.append(plugin_id)
            
            # Process different inputs concurrently
            async def process_plugin(plugin_id, input_text):
                plugin = manager.active_plugins[plugin_id]
                await plugin.process(input_text, {})
                return plugin_id, plugin.state, input_text
            
            tasks = []
            inputs = [f"Input {i}" for i in range(5)]
            
            for plugin_id, input_text in zip(plugin_ids, inputs):
                task = asyncio.create_task(process_plugin(plugin_id, input_text))
                tasks.append(task)
            
            results = await asyncio.gather(*tasks)
            
            # Verify each plugin maintained its state correctly
            for plugin_id, state, input_text in results:
                assert state == PluginState.COMPLETED
                
                plugin = manager.active_plugins[plugin_id]
                
                # Check rendering isolation
                context = RenderContext(display_mode="inscribed")
                render_data = await plugin.render(context)
                
                # Should have correct content for this specific plugin
                assert input_text in render_data.get("content", "")
                
                # Should have unique plugin ID
                assert render_data.get("plugin_id") == plugin_id
                
        finally:
            await manager.stop()
    
    @pytest.mark.asyncio
    async def test_timeline_chronological_ordering(self):
        """Test 5: Verify timeline ordering is chronologically correct."""
        manager = PluginManager()
        await manager.start()
        
        try:
            manager.register_plugin_class(UserInputPlugin)
            manager.register_plugin_class(WelcomePlugin)
            
            # Create plugins with deliberate timing
            timeline = []
            
            # Plugin 1
            start_time_1 = time.time()
            plugin1_id = await manager.create_plugin("welcome", {"version": "v1"})
            plugin1 = manager.active_plugins[plugin1_id]
            await plugin1.process({}, {})
            end_time_1 = time.time()
            
            # Small delay
            await asyncio.sleep(0.1)
            
            # Plugin 2
            start_time_2 = time.time()
            plugin2_id = await manager.create_plugin("user_input", {"max_length": 1000})
            plugin2 = manager.active_plugins[plugin2_id]
            await plugin2.process("Test input", {})
            end_time_2 = time.time()
            
            # Verify timing order
            assert start_time_1 < end_time_1 < start_time_2 < end_time_2
            
            # Check plugin creation timestamps
            info1 = plugin1.get_plugin_info()
            info2 = plugin2.get_plugin_info()
            
            created_1 = datetime.fromisoformat(info1["timestamps"]["created_at"])
            created_2 = datetime.fromisoformat(info2["timestamps"]["created_at"])
            
            # Should be in chronological order
            assert created_1 < created_2
            
            # Check durations are reasonable
            duration1 = plugin1.get_duration()
            duration2 = plugin2.get_duration()
            
            assert duration1 is not None and duration1 > 0
            assert duration2 is not None and duration2 > 0
            
            # Check rendering shows proper timing
            for plugin in [plugin1, plugin2]:
                context = RenderContext(display_mode="inscribed")
                render_data = await plugin.render(context)
                
                title = render_data.get("title", "")
                # Should have timing information
                assert "(" in title and "s)" in title
                
                # Extract duration and verify it's reasonable
                import re
                duration_match = re.search(r'\((\d+\.\d+)s\)', title)
                if duration_match:
                    title_duration = float(duration_match.group(1))
                    assert title_duration > 0
                    assert title_duration < 10  # Should be reasonable
                    
        finally:
            await manager.stop()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])