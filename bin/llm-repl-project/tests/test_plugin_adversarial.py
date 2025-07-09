"""
Adversarial tests for the plugin architecture.

These tests are designed to break the plugin system and find architectural flaws:
- Edge cases and error conditions
- Plugin interface compliance
- Resource exhaustion
- State corruption
- Concurrent access issues
- Memory leaks
- Plugin lifecycle violations
- Error propagation
"""

import pytest
import asyncio
import gc
import sys
import threading
import time
from pathlib import Path
from unittest.mock import Mock, AsyncMock
from typing import Any, Dict

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from plugins.base import (
    BlockPlugin, PluginState, PluginCapability, PluginMetadata, 
    RenderContext, PluginEvent
)
from plugins.registry import PluginManager, PluginWorkflow, WorkflowStep
from plugins.blocks import (
    UserInputPlugin, SystemCheckPlugin, WelcomePlugin,
    ProcessingPlugin, AssistantResponsePlugin
)


class MaliciousPlugin(BlockPlugin):
    """Plugin designed to break the system."""
    
    def __init__(self, failure_mode: str = "none"):
        super().__init__()
        self.failure_mode = failure_mode
        self.call_count = 0
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="malicious_plugin",
            version="1.0.0",
            description="Plugin designed to cause problems",
            author="Test",
            capabilities=[PluginCapability.USER_INPUT],
            dependencies=[]
        )
    
    async def _on_initialize(self) -> None:
        # Check for failure mode in config
        failure_mode = self._config.get("failure_mode", self.failure_mode)
        if failure_mode == "init_failure":
            raise RuntimeError("Initialization failed")
        self.call_count += 1
    
    async def _on_activate(self) -> None:
        failure_mode = self._config.get("failure_mode", self.failure_mode)
        if failure_mode == "activate_failure":
            raise RuntimeError("Activation failed")
        self.call_count += 1
    
    async def _on_deactivate(self) -> None:
        failure_mode = self._config.get("failure_mode", self.failure_mode)
        if failure_mode == "deactivate_failure":
            raise RuntimeError("Deactivation failed")
        self.call_count += 1
    
    async def _on_process(self, input_data: Any, context: Dict[str, Any]) -> Any:
        self.call_count += 1
        
        failure_mode = self._config.get("failure_mode", self.failure_mode)
        if failure_mode == "process_failure":
            raise RuntimeError("Processing failed")
        elif failure_mode == "infinite_loop":
            while True:
                await asyncio.sleep(0.001)
        elif failure_mode == "memory_leak":
            # Create large objects to simulate memory leak
            self._data["large_data"] = [i for i in range(1000000)]
        elif failure_mode == "state_corruption":
            # Directly modify state (should not be allowed)
            self._state = "corrupted"
        elif failure_mode == "slow_processing":
            await asyncio.sleep(10)
        
        return {"result": "malicious_result", "call_count": self.call_count}
    
    async def _on_render(self, context: RenderContext) -> Dict[str, Any]:
        failure_mode = self._config.get("failure_mode", self.failure_mode)
        if failure_mode == "render_failure":
            raise RuntimeError("Rendering failed")
        
        return {
            "render_type": "malicious",
            "title": "Malicious Plugin",
            "content": f"Failure mode: {failure_mode}",
            "call_count": self.call_count
        }


class TestPluginAdversarial:
    """Adversarial tests for the plugin system."""
    
    @pytest.mark.asyncio
    async def test_plugin_initialization_failure(self):
        """Test that plugin initialization failures are handled gracefully."""
        manager = PluginManager()
        await manager.start()
        
        try:
            manager.register_plugin_class(MaliciousPlugin)
            
            # This should fail gracefully
            plugin_id = await manager.create_plugin("malicious_plugin", {
                "failure_mode": "init_failure"
            })
            
            # Should return None on failure
            assert plugin_id is None
            
        finally:
            await manager.stop()
    
    @pytest.mark.asyncio
    async def test_plugin_activation_failure(self):
        """Test that plugin activation failures are handled gracefully."""
        plugin = MaliciousPlugin("activate_failure")
        
        await plugin.initialize({})
        
        # This should raise an error
        with pytest.raises(RuntimeError, match="Activation failed"):
            await plugin.activate()
        
        # Plugin should remain in INACTIVE state
        assert plugin.state == PluginState.INACTIVE
    
    @pytest.mark.asyncio
    async def test_plugin_processing_failure(self):
        """Test that plugin processing failures are handled correctly."""
        plugin = MaliciousPlugin("process_failure")
        
        await plugin.initialize({})
        await plugin.activate()
        
        # This should raise an error and put plugin in ERROR state
        with pytest.raises(RuntimeError, match="Processing failed"):
            await plugin.process("test", {})
        
        assert plugin.state == PluginState.ERROR
    
    @pytest.mark.asyncio
    async def test_plugin_render_failure(self):
        """Test that plugin render failures are handled gracefully."""
        plugin = MaliciousPlugin("render_failure")
        
        await plugin.initialize({})
        await plugin.activate()
        
        # Render should return error data instead of crashing
        context = RenderContext(display_mode="live")
        render_data = await plugin.render(context)
        
        assert render_data["plugin_state"] == PluginState.ERROR
        assert "error" in render_data
    
    @pytest.mark.asyncio
    async def test_plugin_state_corruption_protection(self):
        """Test that plugins cannot directly corrupt their state."""
        plugin = MaliciousPlugin("state_corruption")
        
        await plugin.initialize({})
        await plugin.activate()
        
        # Process should complete despite trying to corrupt state
        result = await plugin.process("test", {})
        
        # State should still be valid (COMPLETED), not corrupted
        assert plugin.state == PluginState.COMPLETED
        assert result["result"] == "malicious_result"
    
    @pytest.mark.asyncio
    async def test_plugin_timeout_protection(self):
        """Test that long-running plugins don't block the system."""
        plugin = MaliciousPlugin("slow_processing")
        
        await plugin.initialize({})
        await plugin.activate()
        
        # This should timeout (using asyncio.wait_for)
        with pytest.raises(asyncio.TimeoutError):
            await asyncio.wait_for(
                plugin.process("test", {}),
                timeout=1.0
            )
    
    @pytest.mark.asyncio
    async def test_plugin_memory_leak_detection(self):
        """Test detection of memory leaks in plugins."""
        plugin = MaliciousPlugin("memory_leak")
        
        await plugin.initialize({})
        await plugin.activate()
        
        # Check memory usage before
        initial_size = len(gc.get_objects())
        
        # Process should create large objects
        await plugin.process("test", {})
        
        # Check memory usage after
        after_size = len(gc.get_objects())
        
        # Should have significantly more objects
        assert after_size > initial_size + 100000
        
        # Cleanup
        await plugin.deactivate()
        gc.collect()
    
    @pytest.mark.asyncio
    async def test_plugin_manager_error_isolation(self):
        """Test that plugin manager isolates errors from other plugins."""
        manager = PluginManager()
        await manager.start()
        
        try:
            # Register both good and bad plugins
            manager.register_plugin_class(MaliciousPlugin)
            manager.register_plugin_class(UserInputPlugin)
            
            # Create good plugin
            good_plugin_id = await manager.create_plugin("user_input", {
                "max_length": 1000
            })
            assert good_plugin_id is not None
            
            # Create bad plugin
            bad_plugin_id = await manager.create_plugin("malicious_plugin", {
                "failure_mode": "process_failure"
            })
            assert bad_plugin_id is not None
            
            # Good plugin should work
            good_plugin = manager.active_plugins[good_plugin_id]
            good_result = await good_plugin.process("test input", {})
            assert good_result["input"] == "test input"
            
            # Bad plugin should fail but not affect good plugin
            bad_plugin = manager.active_plugins[bad_plugin_id]
            with pytest.raises(RuntimeError):
                await bad_plugin.process("test", {})
            
            # Good plugin should still work after bad plugin fails
            good_result2 = await good_plugin.process("test input 2", {})
            assert good_result2["input"] == "test input 2"
            
        finally:
            await manager.stop()
    
    @pytest.mark.asyncio
    async def test_plugin_workflow_failure_handling(self):
        """Test workflow failure handling and partial completion."""
        manager = PluginManager()
        await manager.start()
        
        try:
            manager.register_plugin_class(MaliciousPlugin)
            manager.register_plugin_class(UserInputPlugin)
            
            # Create workflow with both good and bad steps
            workflow = PluginWorkflow(
                name="test_workflow",
                description="Test workflow with failures",
                steps=[
                    WorkflowStep(
                        plugin_name="user_input",
                        config={"max_length": 1000}
                    ),
                    WorkflowStep(
                        plugin_name="malicious_plugin",
                        config={"failure_mode": "process_failure"},
                        optional=True  # This should not stop workflow
                    ),
                    WorkflowStep(
                        plugin_name="user_input",
                        config={"max_length": 1000},
                        dependencies=["user_input"]
                    )
                ]
            )
            
            manager.register_workflow(workflow)
            
            # Execute workflow
            result = await manager.execute_workflow(
                "test_workflow",
                {"input": "test data"},
                {}
            )
            
            # Should complete despite optional step failure
            assert result["status"] == "completed"
            assert "user_input" in result["results"]
            assert "malicious_plugin" in result["results"]
            
        finally:
            await manager.stop()
    
    @pytest.mark.asyncio
    async def test_plugin_concurrent_access(self):
        """Test concurrent access to plugins."""
        manager = PluginManager()
        await manager.start()
        
        try:
            manager.register_plugin_class(UserInputPlugin)
            
            # Create multiple plugin instances
            plugin_ids = []
            for i in range(10):
                plugin_id = await manager.create_plugin("user_input", {
                    "max_length": 1000
                })
                plugin_ids.append(plugin_id)
            
            # Process concurrently
            async def process_plugin(plugin_id, data):
                plugin = manager.active_plugins[plugin_id]
                return await plugin.process(f"test {data}", {})
            
            # Run many concurrent operations
            tasks = []
            for i in range(100):
                plugin_id = plugin_ids[i % len(plugin_ids)]
                task = asyncio.create_task(process_plugin(plugin_id, i))
                tasks.append(task)
            
            # Wait for all to complete
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Check that most succeeded
            successful = [r for r in results if isinstance(r, dict)]
            assert len(successful) > 90  # Allow some failures due to concurrency
            
        finally:
            await manager.stop()
    
    @pytest.mark.asyncio
    async def test_plugin_lifecycle_violations(self):
        """Test that plugin lifecycle violations are caught."""
        plugin = UserInputPlugin()
        
        # Cannot process before initialization
        with pytest.raises(ValueError, match="Cannot process in state"):
            await plugin.process("test", {})
        
        # Cannot activate before initialization
        with pytest.raises(ValueError, match="Cannot activate plugin in state"):
            await plugin.activate()
        
        # Initialize properly
        await plugin.initialize({})
        
        # Cannot process before activation
        with pytest.raises(ValueError, match="Cannot process in state"):
            await plugin.process("test", {})
        
        # Activate properly
        await plugin.activate()
        
        # Now processing should work
        result = await plugin.process("test", {})
        assert result["input"] == "test"
        
        # Cannot activate when already completed
        with pytest.raises(ValueError, match="Cannot activate plugin in state"):
            await plugin.activate()
    
    @pytest.mark.asyncio
    async def test_plugin_resource_cleanup(self):
        """Test that plugins properly clean up resources."""
        manager = PluginManager()
        await manager.start()
        
        try:
            manager.register_plugin_class(UserInputPlugin)
            
            # Create many plugins
            plugin_ids = []
            for i in range(100):
                plugin_id = await manager.create_plugin("user_input", {})
                plugin_ids.append(plugin_id)
            
            # Check they're all active
            assert len(manager.active_plugins) == 100
            
            # Remove half of them
            for i in range(50):
                success = await manager.remove_plugin(plugin_ids[i])
                assert success
            
            # Should have 50 left
            assert len(manager.active_plugins) == 50
            
            # Stop manager (should cleanup remaining plugins)
            await manager.stop()
            
            # Should be empty after stop
            assert len(manager.active_plugins) == 0
            
        finally:
            # Ensure cleanup even if test fails
            if manager._running:
                await manager.stop()
    
    @pytest.mark.asyncio
    async def test_plugin_interface_compliance(self):
        """Test that all plugins properly implement the interface."""
        plugins_to_test = [
            UserInputPlugin,
            SystemCheckPlugin,
            WelcomePlugin,
            ProcessingPlugin,
            AssistantResponsePlugin
        ]
        
        for plugin_class in plugins_to_test:
            plugin = plugin_class()
            
            # Check metadata property
            metadata = plugin.metadata
            assert hasattr(metadata, 'name')
            assert hasattr(metadata, 'version')
            assert hasattr(metadata, 'description')
            assert hasattr(metadata, 'author')
            assert hasattr(metadata, 'capabilities')
            assert isinstance(metadata.capabilities, list)
            
            # Check state property
            assert hasattr(plugin, 'state')
            assert plugin.state == PluginState.INACTIVE
            
            # Check lifecycle methods exist
            assert hasattr(plugin, 'initialize')
            assert hasattr(plugin, 'activate')
            assert hasattr(plugin, 'deactivate')
            assert hasattr(plugin, 'process')
            assert hasattr(plugin, 'render')
            assert hasattr(plugin, 'handle_event')
            
            # Test basic lifecycle
            await plugin.initialize({})
            await plugin.activate()
            
            # All plugins should be able to render
            context = RenderContext(display_mode="live")
            render_data = await plugin.render(context)
            assert isinstance(render_data, dict)
            assert "plugin_id" in render_data
            assert "plugin_name" in render_data
            
            await plugin.deactivate()
    
    @pytest.mark.asyncio
    async def test_plugin_event_system_stress(self):
        """Test the event system under stress."""
        manager = PluginManager()
        await manager.start()
        
        try:
            # Create event that might cause issues
            malicious_event = PluginEvent(
                event_type="malicious_event",
                source_plugin="test",
                data={"large_data": [i for i in range(10000)]}
            )
            
            # Emit many events rapidly
            for i in range(1000):
                await manager.emit_event(malicious_event)
            
            # Wait for events to process
            await asyncio.sleep(0.1)
            
            # System should still be responsive
            status = manager.get_system_status()
            assert status["running"] == True
            
        finally:
            await manager.stop()
    
    @pytest.mark.asyncio
    async def test_plugin_circular_dependencies(self):
        """Test detection of circular dependencies in workflows."""
        manager = PluginManager()
        await manager.start()
        
        try:
            manager.register_plugin_class(UserInputPlugin)
            
            # Create workflow with circular dependencies
            circular_workflow = PluginWorkflow(
                name="circular_workflow",
                description="Workflow with circular dependencies",
                steps=[
                    WorkflowStep(
                        plugin_name="user_input",
                        config={},
                        dependencies=["user_input"]  # Depends on itself
                    )
                ]
            )
            
            manager.register_workflow(circular_workflow)
            
            # Should detect circular dependency
            result = await manager.execute_workflow(
                "circular_workflow",
                {"input": "test"},
                {}
            )
            
            assert result["status"] == "failed"
            assert "circular dependency" in result["error"].lower()
            
        finally:
            await manager.stop()


class TestPluginDisplay:
    """Test plugin display consistency and formatting."""
    
    @pytest.mark.asyncio
    async def test_all_plugins_have_consistent_display(self):
        """Test that all plugins follow the same display format."""
        plugins_to_test = [
            (UserInputPlugin, {"max_length": 1000}),
            (SystemCheckPlugin, {}),
            (WelcomePlugin, {"version": "test"}),
            (ProcessingPlugin, {}),
            (AssistantResponsePlugin, {})
        ]
        
        for plugin_class, config in plugins_to_test:
            plugin = plugin_class()
            await plugin.initialize(config)
            await plugin.activate()
            
            # Test live rendering
            live_context = RenderContext(display_mode="live")
            live_render = await plugin.render(live_context)
            
            # All plugins should have these fields
            assert "plugin_id" in live_render
            assert "plugin_name" in live_render
            assert "plugin_state" in live_render
            assert "render_type" in live_render
            assert "title" in live_render
            
            # Test inscribed rendering
            inscribed_context = RenderContext(display_mode="inscribed")
            inscribed_render = await plugin.render(inscribed_context)
            
            assert "plugin_id" in inscribed_render
            assert "plugin_name" in inscribed_render
            assert "plugin_state" in inscribed_render
            
            await plugin.deactivate()
    
    @pytest.mark.asyncio
    async def test_plugin_timing_information(self):
        """Test that plugins provide timing information."""
        plugin = UserInputPlugin()
        await plugin.initialize({"max_length": 1000})
        await plugin.activate()
        
        # Check timing info is available
        plugin_info = plugin.get_plugin_info()
        assert "timestamps" in plugin_info
        assert "created_at" in plugin_info["timestamps"]
        assert "activated_at" in plugin_info["timestamps"]
        
        await plugin.process("test", {})
        
        # After processing, should have completion time
        plugin_info = plugin.get_plugin_info()
        assert "completed_at" in plugin_info["timestamps"]
        assert "duration_seconds" in plugin_info["timestamps"]
        
        # Duration should be reasonable
        duration = plugin_info["timestamps"]["duration_seconds"]
        assert duration is not None
        assert duration >= 0
        assert duration < 10  # Should complete quickly
    
    @pytest.mark.asyncio
    async def test_plugin_error_display_consistency(self):
        """Test that error displays are consistent across plugins."""
        plugin = MaliciousPlugin("render_failure")
        await plugin.initialize({})
        await plugin.activate()
        
        # Force plugin into error state
        try:
            await plugin.process("test", {})
        except:
            pass
        
        # Error rendering should be consistent
        context = RenderContext(display_mode="live")
        render_data = await plugin.render(context)
        
        assert render_data["plugin_state"] == PluginState.ERROR
        assert "error" in render_data
        assert "render_type" in render_data
        assert render_data["render_type"] == "error"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])