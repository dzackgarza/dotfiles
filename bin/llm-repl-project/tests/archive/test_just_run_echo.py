"""Echo tests that match 'just run' behavior to ensure test coverage reflects reality."""

import pytest
import asyncio
import sys
import time
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch

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


class TestJustRunEcho:
    """Tests that echo the exact behavior of 'just run' to ensure test coverage reflects reality."""
    
    @pytest.mark.asyncio
    async def test_echo_startup_sequence(self):
        """Echo test: Verify startup sequence matches what 'just run' would produce."""
        
        # This test simulates exactly what happens when you run 'just run'
        # 1. System startup
        # 2. Configuration validation
        # 3. Welcome display
        
        startup_sequence = []
        
        # Step 1: System Check (equivalent to system initialization)
        system_check = SystemCheckPlugin()
        await system_check.initialize({})
        await system_check.activate()
        
        start_time = time.time()
        system_result = await system_check.process({}, {})
        end_time = time.time()
        
        startup_sequence.append({
            "plugin": "system_check",
            "state": system_check.state,
            "duration": end_time - start_time,
            "result": system_result
        })
        
        # Step 2: Welcome Message (equivalent to welcome display)
        welcome = WelcomePlugin()
        await welcome.initialize({"version": "v3", "show_help": True, "show_commands": True})
        await welcome.activate()
        
        start_time = time.time()
        welcome_result = await welcome.process({}, {})
        end_time = time.time()
        
        startup_sequence.append({
            "plugin": "welcome",
            "state": welcome.state,
            "duration": end_time - start_time,
            "result": welcome_result
        })
        
        # Verify startup sequence is correct
        assert len(startup_sequence) == 2
        assert startup_sequence[0]["plugin"] == "system_check"
        assert startup_sequence[1]["plugin"] == "welcome"
        
        # Both should have completed successfully
        assert startup_sequence[0]["state"] == PluginState.COMPLETED
        assert startup_sequence[1]["state"] == PluginState.COMPLETED
        
        # Both should have reasonable timing
        assert startup_sequence[0]["duration"] < 5.0  # System check shouldn't take too long
        assert startup_sequence[1]["duration"] < 1.0  # Welcome should be fast
        
        # Both should have valid results
        assert startup_sequence[0]["result"] is not None
        assert startup_sequence[1]["result"] is not None
        assert "welcome_content" in startup_sequence[1]["result"]
        
        # Test rendering matches expected format
        for i, step in enumerate(startup_sequence):
            plugin = system_check if i == 0 else welcome
            context = RenderContext(display_mode="inscribed")
            render_data = await plugin.render(context)
            
            # Should have standardized title format
            title = render_data.get("title", "")
            assert "🔧" in title  # Standardized prefix
            assert "✅" in title  # Completion indicator
            assert "(" in title and "s)" in title  # Duration
            
            # Should have complete metadata
            assert "plugin_id" in render_data
            assert "plugin_name" in render_data
            assert "plugin_state" in render_data
            assert render_data["plugin_state"] == PluginState.COMPLETED
    
    @pytest.mark.asyncio
    async def test_echo_single_query_processing(self):
        """Echo test: Verify single query processing matches 'just run' behavior."""
        
        # This simulates the exact flow when a user types a question
        # 1. User input capture
        # 2. Query processing (routing + enhancement)
        # 3. Assistant response generation
        
        query = "How do I write a Python function?"
        processing_sequence = []
        
        # Step 1: User Input
        user_input = UserInputPlugin()
        await user_input.initialize({"max_length": 10000})
        await user_input.activate()
        
        start_time = time.time()
        user_result = await user_input.process(query, {})
        end_time = time.time()
        
        processing_sequence.append({
            "plugin": "user_input",
            "state": user_input.state,
            "duration": end_time - start_time,
            "result": user_result,
            "tokens": user_input.get_token_counts()
        })
        
        # Step 2: Cognition Processing
        cognition = CognitionPlugin()
        await cognition.initialize({
            "modules": [QueryRoutingModule, PromptEnhancementModule],
            "llm_interface": "default"
        })
        await cognition.activate()
        
        # Setup LLM manager
        llm_manager = LLMManager()
        llm_manager.register_interface("default", MockLLMInterface(), is_default=True)
        
        start_time = time.time()
        cognition_result = await cognition.process(query, {"llm_manager": llm_manager})
        end_time = time.time()
        
        processing_sequence.append({
            "plugin": "cognition",
            "state": cognition.state,
            "duration": end_time - start_time,
            "result": cognition_result,
            "tokens": cognition.get_token_counts()
        })
        
        # Step 3: Assistant Response
        assistant = AssistantResponsePlugin()
        await assistant.initialize({"format_markdown": True})
        await assistant.activate()
        
        # Simulate response with processing results
        # Get tokens from cognition plugin, not from result
        cognition_tokens_actual = cognition.get_token_counts()
        assistant.add_input_tokens(cognition_tokens_actual.get("input", 0))
        assistant.add_output_tokens(cognition_tokens_actual.get("output", 0))
        
        start_time = time.time()
        assistant_result = await assistant.process({
            "response": cognition_result["final_output"],
            "processing_results": cognition_result
        }, {})
        end_time = time.time()
        
        processing_sequence.append({
            "plugin": "assistant_response",
            "state": assistant.state,
            "duration": end_time - start_time,
            "result": assistant_result,
            "tokens": assistant.get_token_counts()
        })
        
        # Verify processing sequence is correct
        assert len(processing_sequence) == 3
        assert processing_sequence[0]["plugin"] == "user_input"
        assert processing_sequence[1]["plugin"] == "cognition"
        assert processing_sequence[2]["plugin"] == "assistant_response"
        
        # All should have completed successfully
        for step in processing_sequence:
            assert step["state"] == PluginState.COMPLETED
            assert step["duration"] >= 0
            assert step["result"] is not None
        
        # Check token flow
        user_tokens = processing_sequence[0]["tokens"]
        cognition_tokens = processing_sequence[1]["tokens"]
        assistant_tokens = processing_sequence[2]["tokens"]
        
        # User input shouldn't generate tokens
        assert user_tokens["input"] == 0
        assert user_tokens["output"] == 0
        
        # Cognition should have tokens from LLM calls
        assert cognition_tokens["input"] > 0
        assert cognition_tokens["output"] > 0
        
        # Assistant should have tokens from cognition (if we added them)
        # Note: Assistant gets tokens from cognition results
        total_cognition_tokens = cognition_tokens["input"] + cognition_tokens["output"]
        total_assistant_tokens = assistant_tokens["input"] + assistant_tokens["output"]
        assert total_assistant_tokens >= 0  # Should have some tokens or none
        
        # Assistant should have tokens from cognition (if we added them properly)
        # The tokens should flow from cognition to assistant
        assert total_assistant_tokens >= 0
        
        # If cognition produced tokens, assistant should reflect them
        if total_cognition_tokens > 0:
            assert total_assistant_tokens > 0
        
        # Check content flow
        assert processing_sequence[0]["result"]["input"] == query
        assert processing_sequence[1]["result"]["final_output"]
        assert processing_sequence[2]["result"]["response"]
        
        # Test rendering for each step
        plugins = [user_input, cognition, assistant]
        for i, plugin in enumerate(plugins):
            context = RenderContext(display_mode="inscribed")
            render_data = await plugin.render(context)
            
            # Should have standardized format
            title = render_data.get("title", "")
            assert "🔧" in title
            assert "✅" in title
            assert "(" in title and "s)" in title
            
            # Should show tokens for plugins that use them
            if i > 0:  # Not user input
                if plugin.get_token_counts()["input"] + plugin.get_token_counts()["output"] > 0:
                    assert "[" in title and "tokens]" in title
    
    @pytest.mark.asyncio
    async def test_echo_multi_turn_conversation(self):
        """Echo test: Verify multi-turn conversation matches 'just run' behavior."""
        
        # This simulates multiple back-and-forth exchanges
        conversation_turns = [
            "Hello, how are you?",
            "What's the weather like?",
            "Can you help me write Python code?"
        ]
        
        full_conversation = []
        
        # Setup persistent LLM manager
        llm_manager = LLMManager()
        llm_manager.register_interface("default", MockLLMInterface(), is_default=True)
        
        for turn_num, query in enumerate(conversation_turns):
            turn_sequence = []
            
            # User Input
            user_input = UserInputPlugin()
            await user_input.initialize({"max_length": 10000})
            await user_input.activate()
            await user_input.process(query, {})
            
            turn_sequence.append({
                "type": "user_input",
                "plugin": user_input,
                "query": query,
                "turn": turn_num
            })
            
            # Cognition Processing
            cognition = CognitionPlugin()
            await cognition.initialize({
                "modules": [QueryRoutingModule, PromptEnhancementModule],
                "llm_interface": "default"
            })
            await cognition.activate()
            cognition_result = await cognition.process(query, {"llm_manager": llm_manager})
            
            turn_sequence.append({
                "type": "cognition",
                "plugin": cognition,
                "result": cognition_result,
                "turn": turn_num
            })
            
            # Assistant Response
            assistant = AssistantResponsePlugin()
            await assistant.initialize({"format_markdown": True})
            await assistant.activate()
            assistant.add_input_tokens(cognition_result.get("total_tokens", {}).get("input", 0))
            assistant.add_output_tokens(cognition_result.get("total_tokens", {}).get("output", 0))
            await assistant.process({
                "response": cognition_result["final_output"],
                "processing_results": cognition_result
            }, {})
            
            turn_sequence.append({
                "type": "assistant_response",
                "plugin": assistant,
                "turn": turn_num
            })
            
            full_conversation.extend(turn_sequence)
        
        # Verify conversation structure
        assert len(full_conversation) == len(conversation_turns) * 3  # 3 plugins per turn
        
        # Check sequence pattern
        for i in range(len(conversation_turns)):
            base_index = i * 3
            assert full_conversation[base_index]["type"] == "user_input"
            assert full_conversation[base_index + 1]["type"] == "cognition"
            assert full_conversation[base_index + 2]["type"] == "assistant_response"
            assert full_conversation[base_index]["turn"] == i
        
        # Check all plugins completed successfully
        for step in full_conversation:
            assert step["plugin"].state == PluginState.COMPLETED
        
        # Check timeline ordering
        timestamps = []
        for step in full_conversation:
            plugin_info = step["plugin"].get_plugin_info()
            created_at = plugin_info["timestamps"]["created_at"]
            timestamps.append(created_at)
        
        # Timestamps should be in chronological order
        for i in range(1, len(timestamps)):
            assert timestamps[i] >= timestamps[i-1]
    
    @pytest.mark.asyncio
    async def test_echo_error_handling(self):
        """Echo test: Verify error handling matches 'just run' behavior."""
        
        # Test various error scenarios that could occur in 'just run'
        error_scenarios = [
            {"type": "invalid_input", "input": ""},  # Empty input
            {"type": "long_input", "input": "x" * 20000},  # Too long input
            {"type": "special_chars", "input": "Test\x00\x01\x02"},  # Special characters
        ]
        
        for scenario in error_scenarios:
            # Test User Input Error Handling
            user_input = UserInputPlugin()
            await user_input.initialize({"max_length": 1000, "allow_empty": False})
            await user_input.activate()
            
            try:
                await user_input.process(scenario["input"], {})
                
                # If no exception, check state
                if scenario["type"] == "invalid_input":
                    # Empty input should fail
                    assert user_input.state == PluginState.ERROR
                elif scenario["type"] == "long_input":
                    # Too long input should fail
                    assert user_input.state == PluginState.ERROR
                else:
                    # Special chars might succeed
                    assert user_input.state in [PluginState.COMPLETED, PluginState.ERROR]
                    
            except ValueError:
                # Exception is expected for invalid inputs
                assert user_input.state == PluginState.ERROR
            
            # Test error rendering
            context = RenderContext(display_mode="inscribed")
            render_data = await user_input.render(context)
            
            if user_input.state == PluginState.ERROR:
                title = render_data.get("title", "")
                assert "❌" in title  # Error indicator
                assert "🔧" in title  # Still standardized
                
                # Should have error styling
                style = render_data.get("style", {})
                assert style.get("border_color") == "red"
    
    @pytest.mark.asyncio
    async def test_echo_performance_characteristics(self):
        """Echo test: Verify performance characteristics match 'just run' expectations."""
        
        # Test performance metrics that would be visible in 'just run'
        performance_tests = []
        
        # Test 1: Quick operations should be fast
        quick_ops = [
            ("welcome", WelcomePlugin, {}),
            ("user_input", UserInputPlugin, {"max_length": 1000}),
        ]
        
        for name, plugin_class, config in quick_ops:
            plugin = plugin_class()
            await plugin.initialize(config)
            await plugin.activate()
            
            start_time = time.time()
            if name == "welcome":
                await plugin.process({}, {})
            else:
                await plugin.process("Test input", {})
            end_time = time.time()
            
            duration = end_time - start_time
            performance_tests.append({
                "plugin": name,
                "duration": duration,
                "expected_max": 1.0  # Should be under 1 second
            })
        
        # Test 2: Processing operations should be reasonable
        llm_manager = LLMManager()
        llm_manager.register_interface("default", MockLLMInterface({"response_delay": 0.1}), is_default=True)
        
        cognition = CognitionPlugin()
        await cognition.initialize({
            "modules": [QueryRoutingModule, PromptEnhancementModule],
            "llm_interface": "default"
        })
        await cognition.activate()
        
        start_time = time.time()
        await cognition.process("Test query for performance", {"llm_manager": llm_manager})
        end_time = time.time()
        
        performance_tests.append({
            "plugin": "cognition",
            "duration": end_time - start_time,
            "expected_max": 5.0  # Should be under 5 seconds
        })
        
        # Verify all performance expectations
        for test in performance_tests:
            assert test["duration"] < test["expected_max"], \
                f"{test['plugin']} took {test['duration']:.2f}s, expected < {test['expected_max']}s"
        
        # Test timing accuracy in rendering
        for test in performance_tests:
            plugin_name = test["plugin"]
            if plugin_name == "welcome":
                plugin = WelcomePlugin()
                await plugin.initialize({})
                await plugin.activate()
                await plugin.process({}, {})
            elif plugin_name == "user_input":
                plugin = UserInputPlugin()
                await plugin.initialize({"max_length": 1000})
                await plugin.activate()
                await plugin.process("Test", {})
            else:
                plugin = cognition
            
            context = RenderContext(display_mode="inscribed")
            render_data = await plugin.render(context)
            
            # Extract timing from title
            title = render_data.get("title", "")
            import re
            duration_match = re.search(r'\((\d+\.\d+)s\)', title)
            
            if duration_match:
                displayed_duration = float(duration_match.group(1))
                actual_duration = plugin.get_duration()
                
                # Should be close to actual duration
                if actual_duration:
                    assert abs(displayed_duration - actual_duration) < 0.5, \
                        f"Duration mismatch: displayed {displayed_duration}s, actual {actual_duration}s"
    
    @pytest.mark.asyncio
    async def test_echo_memory_and_state_management(self):
        """Echo test: Verify memory and state management matches 'just run' behavior."""
        
        # Test that multiple plugin instances don't interfere with each other
        # (This would be important in 'just run' for conversation history)
        
        manager = PluginManager()
        await manager.start()
        
        try:
            # Register plugins
            manager.register_plugin_class(UserInputPlugin)
            manager.register_plugin_class(WelcomePlugin)
            manager.register_plugin_class(SystemCheckPlugin)
            
            # Create multiple instances
            plugin_instances = []
            
            # Create startup sequence
            system_check_id = await manager.create_plugin("system_check", {})
            welcome_id = await manager.create_plugin("welcome", {"version": "test"})
            
            # Create multiple user inputs (simulating conversation)
            user_inputs = []
            for i in range(3):
                user_id = await manager.create_plugin("user_input", {"max_length": 1000})
                user_plugin = manager.active_plugins[user_id]
                await user_plugin.process(f"Message {i}", {})
                user_inputs.append(user_id)
            
            # Verify all plugins are tracked
            assert len(manager.active_plugins) == 5  # 1 system + 1 welcome + 3 user
            
            # Verify each plugin maintains its own state
            for user_id in user_inputs:
                user_plugin = manager.active_plugins[user_id]
                assert user_plugin.state == PluginState.COMPLETED
                
                # Each should have unique content
                context = RenderContext(display_mode="inscribed")
                render_data = await user_plugin.render(context)
                content = render_data.get("content", "")
                
                # Should contain the specific message for this instance
                assert any(f"Message {i}" in content for i in range(3))
            
            # Test plugin info uniqueness
            plugin_infos = []
            for plugin_id in manager.active_plugins:
                plugin = manager.active_plugins[plugin_id]
                info = plugin.get_plugin_info()
                plugin_infos.append(info)
            
            # All should have unique IDs
            plugin_ids = [info["plugin_id"] for info in plugin_infos]
            assert len(plugin_ids) == len(set(plugin_ids))  # All unique
            
            # All should have reasonable timestamps
            for info in plugin_infos:
                timestamps = info["timestamps"]
                assert "created_at" in timestamps
                assert "activated_at" in timestamps
                
                # Created time should be valid
                created_time = timestamps["created_at"]
                assert created_time is not None
                
        finally:
            await manager.stop()
            
            # After stop, should be cleaned up
            assert len(manager.active_plugins) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])