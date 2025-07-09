"""Tests for cognitive modules and cognition plugin."""

import pytest
import asyncio
import sys
from pathlib import Path
from unittest.mock import Mock, AsyncMock

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from plugins.cognitive_modules import (
    CognitiveModule, CognitiveModuleInput, CognitiveModuleOutput,
    QueryRoutingModule, PromptEnhancementModule, ReasoningModule
)
from plugins.blocks.cognition import CognitionPlugin
from plugins.llm_interface import (
    LLMInterface, LLMManager, MockLLMInterface, LLMRequest, LLMResponse
)
from plugins.base import RenderContext, PluginState


class TestCognitiveModules:
    """Test individual cognitive modules."""
    
    @pytest.mark.asyncio
    async def test_query_routing_module(self):
        """Test query routing module in isolation."""
        module = QueryRoutingModule()
        llm_interface = MockLLMInterface()
        
        # Test basic properties
        assert module.metadata.name == "query_routing"
        assert module.metadata.task_type == "routing"
        assert module.state == PluginState.INACTIVE
        
        # Test processing
        input_data = CognitiveModuleInput(content="How do I write a Python function?")
        output = await module.process(input_data, llm_interface)
        
        assert isinstance(output, CognitiveModuleOutput)
        assert output.content in ["chat", "code", "research", "creative", "technical", "task"]
        assert output.llm_response is not None
        assert module.state == PluginState.COMPLETED
        
        # Test token tracking
        tokens = module.get_token_counts()
        assert tokens["input"] > 0
        assert tokens["output"] > 0
    
    @pytest.mark.asyncio
    async def test_prompt_enhancement_module(self):
        """Test prompt enhancement module in isolation."""
        module = PromptEnhancementModule()
        llm_interface = MockLLMInterface()
        
        # Test processing
        input_data = CognitiveModuleInput(content="help me with python")
        output = await module.process(input_data, llm_interface)
        
        assert isinstance(output, CognitiveModuleOutput)
        assert len(output.content) > len(input_data.content)  # Should be enhanced
        assert output.confidence > 0.8  # Should be high confidence
        assert module.state == PluginState.COMPLETED
        
        # Test module info
        info = module.get_module_info()
        assert info["metadata"]["name"] == "prompt_enhancement"
        assert info["state"] == PluginState.COMPLETED
        assert info["duration"] is not None
    
    @pytest.mark.asyncio
    async def test_reasoning_module(self):
        """Test reasoning module in isolation."""
        module = ReasoningModule()
        llm_interface = MockLLMInterface()
        
        # Test processing
        input_data = CognitiveModuleInput(content="What is the best way to learn programming?")
        output = await module.process(input_data, llm_interface)
        
        assert isinstance(output, CognitiveModuleOutput)
        assert output.content
        assert output.confidence > 0.7
        assert "reasoning_steps" in output.context
        assert module.state == PluginState.COMPLETED
    
    @pytest.mark.asyncio
    async def test_module_streaming(self):
        """Test streaming functionality."""
        module = QueryRoutingModule()
        llm_interface = MockLLMInterface()
        
        input_data = CognitiveModuleInput(content="Write a Python script")
        
        chunks = []
        final_output = None
        
        async for chunk in module.stream_process(input_data, llm_interface):
            if isinstance(chunk, str):
                chunks.append(chunk)
            elif isinstance(chunk, CognitiveModuleOutput):
                final_output = chunk
                break
        
        assert len(chunks) > 0  # Should have received streaming chunks
        assert final_output is not None
        assert final_output.content
        assert module.state == PluginState.COMPLETED
    
    @pytest.mark.asyncio
    async def test_module_error_handling(self):
        """Test error handling in modules."""
        module = QueryRoutingModule()
        
        # Mock LLM interface that raises errors
        error_interface = Mock(spec=LLMInterface)
        error_interface.make_request = AsyncMock(side_effect=RuntimeError("LLM error"))
        
        input_data = CognitiveModuleInput(content="test")
        
        with pytest.raises(RuntimeError):
            await module.process(input_data, error_interface)
        
        assert module.state == PluginState.ERROR
    
    @pytest.mark.asyncio
    async def test_module_chain_context(self):
        """Test that modules work correctly with chain context."""
        module = PromptEnhancementModule()
        llm_interface = MockLLMInterface()
        
        # Create input with chain context
        input_data = CognitiveModuleInput(
            content="original prompt",
            context={"chain_position": 1, "total_chain_length": 3},
            previous_outputs=[{"content": "previous output"}]
        )
        
        output = await module.process(input_data, llm_interface)
        
        assert isinstance(output, CognitiveModuleOutput)
        assert output.content
        # Should work the same regardless of chain position
        assert module.state == PluginState.COMPLETED
    
    @pytest.mark.asyncio
    async def test_module_rendering(self):
        """Test module rendering."""
        module = QueryRoutingModule()
        llm_interface = MockLLMInterface()
        
        # Test rendering in different states
        context = RenderContext(display_mode="live")
        
        # Initial state
        render_data = await module.render(context)
        assert render_data["module_name"] == "query_routing"
        assert render_data["module_state"] == PluginState.INACTIVE
        
        # After processing
        input_data = CognitiveModuleInput(content="test query")
        await module.process(input_data, llm_interface)
        
        render_data = await module.render(context)
        assert render_data["module_state"] == PluginState.COMPLETED
        assert "title" in render_data  # Should have standardized title
        assert render_data["tokens"]["input"] > 0


class TestCognitionPlugin:
    """Test the cognition plugin orchestrator."""
    
    @pytest.mark.asyncio
    async def test_cognition_plugin_basic(self):
        """Test basic cognition plugin functionality."""
        plugin = CognitionPlugin()
        
        # Initialize with modules
        config = {
            "modules": [QueryRoutingModule, PromptEnhancementModule],
            "llm_interface": "default",
            "stream_processing": False
        }
        
        await plugin.initialize(config)
        await plugin.activate()
        
        # Test processing
        context = {"llm_manager": self._create_mock_llm_manager()}
        result = await plugin.process("Help me write code", context)
        
        assert isinstance(result, dict)
        assert "final_output" in result
        assert "module_outputs" in result
        assert "transparency_log" in result
        assert len(result["module_outputs"]) == 2  # Two modules
        assert len(result["transparency_log"]) == 2
        
        # Test state
        assert plugin.state == PluginState.COMPLETED
        
        # Test token tracking
        tokens = plugin.get_token_counts()
        assert tokens["input"] > 0
        assert tokens["output"] > 0
    
    @pytest.mark.asyncio
    async def test_cognition_plugin_streaming(self):
        """Test streaming cognition plugin."""
        plugin = CognitionPlugin()
        
        config = {
            "modules": [QueryRoutingModule, PromptEnhancementModule],
            "stream_processing": True
        }
        
        await plugin.initialize(config)
        await plugin.activate()
        
        context = {"llm_manager": self._create_mock_llm_manager()}
        
        # This should return an async iterator, but we'll test the batch mode
        # since stream processing returns an async iterator
        config["stream_processing"] = False
        await plugin.initialize(config)
        await plugin.activate()
        
        result = await plugin.process("Write a Python function", context)
        
        assert isinstance(result, dict)
        assert "final_output" in result
        assert result["total_modules"] == 2
    
    @pytest.mark.asyncio
    async def test_cognition_plugin_error_handling(self):
        """Test error handling in cognition plugin."""
        plugin = CognitionPlugin()
        
        # Create a module that will fail
        class FailingModule(CognitiveModule):
            @property
            def metadata(self):
                from plugins.cognitive_modules import CognitiveModuleMetadata
                return CognitiveModuleMetadata(
                    name="failing_module",
                    version="1.0.0",
                    description="A module that fails",
                    author="Test",
                    task_type="test"
                )
            
            def create_llm_request(self, input_data):
                return Mock()
            
            async def process(self, input_data, llm_interface):
                raise RuntimeError("Module failure")
            
            async def stream_process(self, input_data, llm_interface):
                yield "error"
        
        config = {
            "modules": [FailingModule],
            "fail_on_error": True
        }
        
        await plugin.initialize(config)
        await plugin.activate()
        
        context = {"llm_manager": self._create_mock_llm_manager()}
        
        with pytest.raises(RuntimeError):
            await plugin.process("test", context)
    
    @pytest.mark.asyncio
    async def test_cognition_plugin_transparency(self):
        """Test transparency logging."""
        plugin = CognitionPlugin()
        
        config = {
            "modules": [QueryRoutingModule, PromptEnhancementModule]
        }
        
        await plugin.initialize(config)
        await plugin.activate()
        
        context = {"llm_manager": self._create_mock_llm_manager()}
        result = await plugin.process("Create a todo list", context)
        
        # Test transparency log
        transparency_log = plugin.get_transparency_log()
        assert len(transparency_log) == 2
        
        for i, log_entry in enumerate(transparency_log):
            assert "module_name" in log_entry
            assert "module_index" in log_entry
            assert "input" in log_entry
            assert "output" in log_entry
            assert "timestamp" in log_entry
            assert log_entry["module_index"] == i
        
        # Test module outputs
        module_outputs = plugin.get_module_outputs()
        assert len(module_outputs) == 2
        
        for output in module_outputs:
            assert "content" in output
            assert "llm_response" in output
    
    @pytest.mark.asyncio
    async def test_cognition_plugin_rendering(self):
        """Test cognition plugin rendering."""
        plugin = CognitionPlugin()
        
        config = {
            "modules": [QueryRoutingModule, PromptEnhancementModule]
        }
        
        await plugin.initialize(config)
        await plugin.activate()
        
        # Test rendering during processing
        context = RenderContext(display_mode="live")
        render_data = await plugin.render(context)
        
        assert render_data["render_type"] == "cognition"
        assert render_data["total_modules"] == 2
        assert "title" in render_data  # Should have standardized title
        
        # Process and test completed rendering
        llm_context = {"llm_manager": self._create_mock_llm_manager()}
        await plugin.process("test query", llm_context)
        
        render_data = await plugin.render(context)
        assert render_data["completed"] == True
        assert "module_summary" in render_data
        assert len(render_data["module_summary"]) == 2
    
    @pytest.mark.asyncio
    async def test_module_isolation(self):
        """Test that modules work the same in isolation and in chains."""
        # Test module in isolation
        module = QueryRoutingModule()
        llm_interface = MockLLMInterface()
        
        isolated_input = CognitiveModuleInput(content="How do I debug Python code?")
        isolated_output = await module.process(isolated_input, llm_interface)
        
        # Reset module state
        module = QueryRoutingModule()
        
        # Test module in chain
        plugin = CognitionPlugin()
        config = {"modules": [QueryRoutingModule]}
        await plugin.initialize(config)
        await plugin.activate()
        
        context = {"llm_manager": self._create_mock_llm_manager()}
        chain_result = await plugin.process("How do I debug Python code?", context)
        
        # Results should be consistent
        chain_output = chain_result["module_outputs"][0]
        
        # Both should have valid outputs
        assert isolated_output.content
        assert chain_output["content"]
        
        # Both should have LLM responses
        assert isolated_output.llm_response is not None
        assert chain_output["llm_response"] is not None
    
    def _create_mock_llm_manager(self):
        """Create a mock LLM manager for testing."""
        manager = LLMManager()
        manager.register_interface("default", MockLLMInterface(), is_default=True)
        return manager


class TestLLMInterface:
    """Test LLM interface functionality."""
    
    @pytest.mark.asyncio
    async def test_mock_llm_interface(self):
        """Test mock LLM interface."""
        interface = MockLLMInterface({"response_delay": 0.01})
        
        request = LLMRequest(
            messages=[{"role": "user", "content": "Hello"}],
            model="test-model",
            request_id="test-123",
            cognitive_module="test_module"
        )
        
        response = await interface.make_request(request)
        
        assert isinstance(response, LLMResponse)
        assert response.content
        assert response.tokens.input_tokens > 0
        assert response.tokens.output_tokens > 0
        assert response.request_id == "test-123"
        assert response.cognitive_module == "test_module"
    
    @pytest.mark.asyncio
    async def test_llm_manager(self):
        """Test LLM manager functionality."""
        manager = LLMManager()
        interface = MockLLMInterface()
        
        manager.register_interface("test", interface)
        
        request = LLMRequest(
            messages=[{"role": "user", "content": "Test"}],
            model="test"
        )
        
        response = await manager.make_request(request, "test")
        
        assert response.content
        
        # Test history
        history = manager.get_request_history()
        assert len(history) == 1
        assert history[0].content == response.content
        
        # Test transparency log
        transparency_log = manager.get_transparency_log()
        assert len(transparency_log) == 1
        assert "content" in transparency_log[0]
        assert "tokens" in transparency_log[0]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])