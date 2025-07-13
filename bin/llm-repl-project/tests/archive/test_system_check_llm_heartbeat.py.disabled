"""Test system check LLM heartbeat functionality."""

import pytest
import asyncio
import sys
from pathlib import Path
from unittest.mock import Mock, AsyncMock

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from plugins.blocks.system_check import SystemCheckPlugin
from plugins.llm_interface import LLMManager, MockLLMInterface, LLMRequest, LLMResponse, TokenUsage
from plugins.base import RenderContext, PluginState


class TestSystemCheckLLMHeartbeat:
    """Test LLM heartbeat functionality in SystemCheckPlugin."""
    
    @pytest.mark.asyncio
    async def test_llm_heartbeat_success(self):
        """Test successful LLM heartbeat check."""
        # Setup LLM manager with mock interface
        llm_manager = LLMManager()
        mock_interface = MockLLMInterface({"response_delay": 0.1})
        llm_manager.register_interface("test_interface", mock_interface, is_default=True)
        
        # Create system check plugin
        plugin = SystemCheckPlugin()
        await plugin.initialize({})
        await plugin.activate()
        
        # Define LLM heartbeat check
        check_data = [{
            "name": "Test LLM",
            "type": "llm_heartbeat",
            "config": {
                "provider": "mock",
                "model": "test-model",
                "interface_name": "test_interface",
                "llm_manager": llm_manager,
                "timeout": 5
            }
        }]
        
        # Process the check
        result = await plugin.process(check_data, {})
        
        # Verify the check passed
        assert result["all_passed"] is True
        assert result["summary"]["passed_checks"] == 1
        assert result["summary"]["failed_checks"] == 0
        
        # Get check results
        check_results = plugin.get_check_results()
        assert "Test LLM" in check_results
        
        llm_result = check_results["Test LLM"]
        assert llm_result["passed"] is True
        assert "mock/test-model: Online" in llm_result["message"]
        assert "↑" in llm_result["message"]  # Input tokens
        assert "↓" in llm_result["message"]  # Output tokens
        
        # Verify details
        details = llm_result["details"]
        assert details["provider"] == "mock"
        assert details["model"] == "test-model"
        assert details["response_time"] > 0
        assert details["input_tokens"] > 0
        assert details["output_tokens"] > 0
        assert details["total_tokens"] > 0
        assert "content_preview" in details
    
    @pytest.mark.asyncio
    async def test_llm_heartbeat_timeout(self):
        """Test LLM heartbeat timeout handling."""
        # Create a mock LLM manager that times out
        llm_manager = Mock()
        llm_manager.make_request = AsyncMock()
        
        async def slow_request(*args, **kwargs):
            await asyncio.sleep(2)  # Longer than timeout
            return LLMResponse(
                content="Response",
                tokens=TokenUsage(10, 10),
                duration_seconds=2.0
            )
        
        llm_manager.make_request.side_effect = slow_request
        
        # Create system check plugin
        plugin = SystemCheckPlugin()
        await plugin.initialize({})
        await plugin.activate()
        
        # Define LLM heartbeat check with short timeout
        check_data = [{
            "name": "Slow LLM",
            "type": "llm_heartbeat", 
            "config": {
                "provider": "slow_provider",
                "model": "slow-model",
                "interface_name": "slow_interface",
                "llm_manager": llm_manager,
                "timeout": 0.5  # Short timeout
            }
        }]
        
        # Process the check
        result = await plugin.process(check_data, {})
        
        # Verify the check failed due to timeout
        assert result["all_passed"] is False
        assert result["summary"]["passed_checks"] == 0
        assert result["summary"]["failed_checks"] == 1
        
        # Get check results
        check_results = plugin.get_check_results()
        assert "Slow LLM" in check_results
        
        llm_result = check_results["Slow LLM"]
        assert llm_result["passed"] is False
        assert "❌ slow_provider/slow-model: Timeout" in llm_result["message"]
        assert llm_result["details"]["error"] == "timeout"
    
    @pytest.mark.asyncio
    async def test_llm_heartbeat_no_manager(self):
        """Test LLM heartbeat with no manager provided."""
        # Create system check plugin
        plugin = SystemCheckPlugin()
        await plugin.initialize({})
        await plugin.activate()
        
        # Define LLM heartbeat check without manager
        check_data = [{
            "name": "No Manager LLM",
            "type": "llm_heartbeat",
            "config": {
                "provider": "test_provider",
                "model": "test-model",
                "interface_name": "test_interface",
                # No llm_manager provided
                "timeout": 5
            }
        }]
        
        # Process the check
        result = await plugin.process(check_data, {})
        
        # Verify the check failed
        assert result["all_passed"] is False
        
        # Get check results
        check_results = plugin.get_check_results()
        llm_result = check_results["No Manager LLM"]
        assert llm_result["passed"] is False
        assert "❌ test_provider/test-model: No LLM manager provided" in llm_result["message"]
        assert llm_result["details"]["error"] == "no_manager"
    
    @pytest.mark.asyncio
    async def test_llm_heartbeat_exception(self):
        """Test LLM heartbeat exception handling."""
        # Create a mock LLM manager that raises an exception
        llm_manager = Mock()
        llm_manager.make_request = AsyncMock()
        llm_manager.make_request.side_effect = Exception("Connection failed")
        
        # Create system check plugin
        plugin = SystemCheckPlugin()
        await plugin.initialize({})
        await plugin.activate()
        
        # Define LLM heartbeat check
        check_data = [{
            "name": "Error LLM",
            "type": "llm_heartbeat",
            "config": {
                "provider": "error_provider",
                "model": "error-model",
                "interface_name": "error_interface",
                "llm_manager": llm_manager,
                "timeout": 5
            }
        }]
        
        # Process the check
        result = await plugin.process(check_data, {})
        
        # Verify the check failed
        assert result["all_passed"] is False
        
        # Get check results
        check_results = plugin.get_check_results()
        llm_result = check_results["Error LLM"]
        assert llm_result["passed"] is False
        assert "❌ error_provider/error-model: Error - Connection failed" in llm_result["message"]
        assert "Connection failed" in llm_result["details"]["error"]
    
    @pytest.mark.asyncio
    async def test_multiple_llm_heartbeats(self):
        """Test multiple LLM heartbeat checks in one system check."""
        # Setup LLM manager with multiple interfaces
        llm_manager = LLMManager()
        
        intent_interface = MockLLMInterface({"response_delay": 0.05})
        main_interface = MockLLMInterface({"response_delay": 0.1})
        
        llm_manager.register_interface("intent", intent_interface)
        llm_manager.register_interface("main", main_interface, is_default=True)
        
        # Create system check plugin
        plugin = SystemCheckPlugin()
        await plugin.initialize({})
        await plugin.activate()
        
        # Define multiple LLM heartbeat checks
        check_data = [
            {
                "name": "Intent LLM",
                "type": "llm_heartbeat",
                "config": {
                    "provider": "ollama",
                    "model": "tinyllama",
                    "interface_name": "intent",
                    "llm_manager": llm_manager,
                    "timeout": 5
                }
            },
            {
                "name": "Main LLM", 
                "type": "llm_heartbeat",
                "config": {
                    "provider": "groq",
                    "model": "llama3-8b-8192",
                    "interface_name": "main",
                    "llm_manager": llm_manager,
                    "timeout": 5
                }
            }
        ]
        
        # Process the checks
        result = await plugin.process(check_data, {})
        
        # Verify both checks passed
        assert result["all_passed"] is True
        assert result["summary"]["passed_checks"] == 2
        assert result["summary"]["failed_checks"] == 0
        
        # Get check results
        check_results = plugin.get_check_results()
        
        # Verify intent LLM check
        assert "Intent LLM" in check_results
        intent_result = check_results["Intent LLM"]
        assert intent_result["passed"] is True
        assert "ollama/tinyllama: Online" in intent_result["message"]
        assert "↑" in intent_result["message"]  # Input tokens
        assert "↓" in intent_result["message"]  # Output tokens
        
        # Verify main LLM check
        assert "Main LLM" in check_results
        main_result = check_results["Main LLM"]
        assert main_result["passed"] is True
        assert "groq/llama3-8b-8192: Online" in main_result["message"]
        assert "↑" in main_result["message"]  # Input tokens
        assert "↓" in main_result["message"]  # Output tokens
    
    @pytest.mark.asyncio
    async def test_system_check_renders_llm_results(self):
        """Test that system check properly renders LLM heartbeat results."""
        # Setup LLM manager
        llm_manager = LLMManager()
        mock_interface = MockLLMInterface({"response_delay": 0.1})
        llm_manager.register_interface("test", mock_interface, is_default=True)
        
        # Create system check plugin
        plugin = SystemCheckPlugin()
        await plugin.initialize({})
        await plugin.activate()
        
        # Run LLM heartbeat check
        check_data = [{
            "name": "Test Provider",
            "type": "llm_heartbeat",
            "config": {
                "provider": "ollama",
                "model": "test-model",
                "interface_name": "test",
                "llm_manager": llm_manager,
                "timeout": 5
            }
        }]
        
        await plugin.process(check_data, {})
        
        # Render the plugin
        context = RenderContext(display_mode="inscribed")
        render_data = await plugin.render(context)
        
        # Verify render contains LLM check results
        assert "detailed_results" in render_data
        detailed_results = render_data["detailed_results"]
        
        assert len(detailed_results) == 1
        # Find the LLM check in the results
        llm_check = None
        for result in detailed_results:
            if result["name"] == "Test Provider":
                llm_check = result
                break
        
        assert llm_check is not None
        assert llm_check["status"] == "✅"
        assert llm_check["passed"] is True
        assert "ollama/test-model: Online" in llm_check["message"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])