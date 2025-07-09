"""Plugin manager and composition system."""

import asyncio
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum

from .base import (
    BlockPlugin, PluginRegistry, PluginEvent, PluginState, 
    PluginCapability, RenderContext
)


class WorkflowState(str, Enum):
    """States of a plugin workflow."""
    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class WorkflowStep:
    """A step in a plugin workflow."""
    plugin_name: str
    config: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)  # Plugin names this step depends on
    optional: bool = False  # If True, workflow continues even if this step fails
    

@dataclass
class PluginWorkflow:
    """A workflow composed of multiple plugin steps."""
    name: str
    description: str
    steps: List[WorkflowStep]
    parallel_steps: List[List[str]] = field(default_factory=list)  # Steps that can run in parallel
    

class PluginManager:
    """
    Manages plugin lifecycles, composition, and communication.
    
    This is the orchestrator that:
    - Loads and manages plugin instances
    - Handles inter-plugin communication via events
    - Composes plugins into workflows
    - Provides a unified interface for the application
    """
    
    def __init__(self):
        self.registry = PluginRegistry()
        self.active_plugins: Dict[str, BlockPlugin] = {}
        self.workflows: Dict[str, PluginWorkflow] = {}
        self.event_queue: asyncio.Queue = asyncio.Queue()
        self.event_handlers: Dict[str, List[str]] = {}  # event_type -> list of plugin_ids
        self._running = False
        self._event_task: Optional[asyncio.Task] = None
    
    async def start(self) -> None:
        """Start the plugin manager."""
        self._running = True
        self._event_task = asyncio.create_task(self._process_events())
    
    async def stop(self) -> None:
        """Stop the plugin manager."""
        self._running = False
        if self._event_task:
            await self.event_queue.put(None)  # Sentinel to stop event processing
            await self._event_task
        
        # Deactivate all active plugins
        plugin_ids = list(self.active_plugins.keys())
        for plugin_id in plugin_ids:
            try:
                await self.remove_plugin(plugin_id)
            except Exception:
                pass  # Best effort cleanup
        
        # Ensure all plugins are removed
        self.active_plugins.clear()
    
    def register_plugin_class(self, plugin_class: type) -> None:
        """Register a plugin class."""
        self.registry.register_plugin(plugin_class)
    
    def register_workflow(self, workflow: PluginWorkflow) -> None:
        """Register a workflow."""
        # Validate workflow
        available_plugins = set(self.registry.list_plugins())
        workflow_plugins = {step.plugin_name for step in workflow.steps}
        
        missing_plugins = workflow_plugins - available_plugins
        if missing_plugins:
            raise ValueError(f"Workflow references unknown plugins: {missing_plugins}")
        
        self.workflows[workflow.name] = workflow
    
    async def create_plugin(self, plugin_name: str, 
                          config: Dict[str, Any] = None) -> Optional[str]:
        """
        Create and activate a plugin instance.
        Returns the plugin instance ID.
        """
        plugin = await self.registry.create_plugin_instance(plugin_name, config or {})
        if not plugin:
            return None
        
        try:
            await plugin.activate()
            self.active_plugins[plugin.plugin_id] = plugin
            
            # Auto-register for events if plugin has event handling
            if hasattr(plugin, '_auto_event_types'):
                for event_type in plugin._auto_event_types:
                    self.register_event_handler(event_type, plugin.plugin_id)
            
            return plugin.plugin_id
        except Exception as e:
            # Plugin activation failed, clean up
            self.registry.remove_plugin_instance(plugin.plugin_id)
            return None
    
    async def remove_plugin(self, plugin_id: str) -> bool:
        """Remove and deactivate a plugin instance."""
        plugin = self.active_plugins.get(plugin_id)
        if not plugin:
            return False
        
        try:
            await plugin.deactivate()
            del self.active_plugins[plugin_id]
            self.registry.remove_plugin_instance(plugin_id)
            
            # Remove from event handlers
            for event_type, handlers in self.event_handlers.items():
                if plugin_id in handlers:
                    handlers.remove(plugin_id)
            
            return True
        except Exception:
            return False
    
    def register_event_handler(self, event_type: str, plugin_id: str) -> None:
        """Register a plugin to handle specific event types."""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        
        if plugin_id not in self.event_handlers[event_type]:
            self.event_handlers[event_type].append(plugin_id)
    
    async def emit_event(self, event: PluginEvent) -> None:
        """Emit an event to the event system."""
        await self.event_queue.put(event)
    
    async def _process_events(self) -> None:
        """Process events from the queue."""
        while self._running:
            try:
                event = await self.event_queue.get()
                if event is None:  # Sentinel
                    break
                
                await self._handle_event(event)
            except Exception as e:
                # Log error but continue processing
                print(f"Error processing event: {e}")
    
    async def _handle_event(self, event: PluginEvent) -> None:
        """Handle a single event."""
        # If event has a specific target, send only to that plugin
        if event.target_plugin:
            plugin = self.active_plugins.get(event.target_plugin)
            if plugin:
                try:
                    response = await plugin.handle_event(event)
                    if response:
                        await self.emit_event(response)
                except Exception as e:
                    print(f"Error handling event in plugin {event.target_plugin}: {e}")
            return
        
        # Otherwise, send to all registered handlers for this event type
        handlers = self.event_handlers.get(event.event_type, [])
        for plugin_id in handlers:
            plugin = self.active_plugins.get(plugin_id)
            if plugin:
                try:
                    response = await plugin.handle_event(event)
                    if response:
                        await self.emit_event(response)
                except Exception as e:
                    print(f"Error handling event in plugin {plugin_id}: {e}")
    
    async def execute_workflow(self, workflow_name: str, 
                             input_data: Any = None,
                             context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute a plugin workflow.
        Returns a dictionary with results from each step.
        """
        workflow = self.workflows.get(workflow_name)
        if not workflow:
            raise ValueError(f"Unknown workflow: {workflow_name}")
        
        context = context or {}
        results = {}
        created_plugins = []
        
        try:
            # Create plugin instances for each step
            step_plugins = {}
            for step in workflow.steps:
                plugin_id = await self.create_plugin(step.plugin_name, step.config)
                if not plugin_id:
                    if not step.optional:
                        raise RuntimeError(f"Failed to create required plugin: {step.plugin_name}")
                    continue
                
                step_plugins[step.plugin_name] = plugin_id
                created_plugins.append(plugin_id)
            
            # Execute steps in dependency order
            executed_steps = set()
            remaining_steps = workflow.steps.copy()
            
            while remaining_steps:
                # Find steps that can be executed (all dependencies satisfied)
                ready_steps = []
                for step in remaining_steps:
                    if all(dep in executed_steps for dep in step.dependencies):
                        ready_steps.append(step)
                
                if not ready_steps:
                    raise RuntimeError("Circular dependency detected in workflow")
                
                # Execute ready steps
                for step in ready_steps:
                    plugin_id = step_plugins.get(step.plugin_name)
                    if not plugin_id:
                        continue  # Optional step that failed to create
                    
                    plugin = self.active_plugins[plugin_id]
                    
                    try:
                        # Prepare step input (previous results + original input)
                        step_input = {
                            "input_data": input_data,
                            "previous_results": results,
                            "step_config": step.config
                        }
                        
                        result = await plugin.process(step_input, context)
                        results[step.plugin_name] = result
                        executed_steps.add(step.plugin_name)
                        
                    except Exception as e:
                        if not step.optional:
                            raise RuntimeError(f"Required step {step.plugin_name} failed: {e}")
                        results[step.plugin_name] = {"error": str(e)}
                        executed_steps.add(step.plugin_name)
                
                # Remove executed steps
                remaining_steps = [s for s in remaining_steps if s.plugin_name not in executed_steps]
            
            return {
                "workflow_name": workflow_name,
                "status": "completed",
                "results": results,
                "steps_executed": list(executed_steps)
            }
            
        except Exception as e:
            return {
                "workflow_name": workflow_name,
                "status": "failed",
                "error": str(e),
                "results": results,
                "steps_executed": list(executed_steps) if 'executed_steps' in locals() else []
            }
        
        finally:
            # Clean up created plugins
            for plugin_id in created_plugins:
                await self.remove_plugin(plugin_id)
    
    async def render_plugin(self, plugin_id: str, context: RenderContext) -> Dict[str, Any]:
        """Render a specific plugin."""
        plugin = self.active_plugins.get(plugin_id)
        if not plugin:
            return {"error": f"Plugin {plugin_id} not found"}
        
        return await plugin.render(context)
    
    async def render_all_active_plugins(self, context: RenderContext) -> List[Dict[str, Any]]:
        """Render all active plugins."""
        renders = []
        for plugin in self.active_plugins.values():
            render_data = await plugin.render(context)
            renders.append(render_data)
        return renders
    
    def get_plugin_info(self, plugin_id: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive information about a plugin."""
        plugin = self.active_plugins.get(plugin_id)
        if not plugin:
            return None
        
        return plugin.get_plugin_info()
    
    def list_active_plugins(self) -> List[str]:
        """List all active plugin IDs."""
        return list(self.active_plugins.keys())
    
    def list_available_plugins(self) -> List[str]:
        """List all available plugin classes."""
        return self.registry.list_plugins()
    
    def list_plugins_by_capability(self, capability: PluginCapability) -> List[str]:
        """List plugins that have a specific capability."""
        return self.registry.list_plugins_by_capability(capability)
    
    def list_workflows(self) -> List[str]:
        """List all registered workflows."""
        return list(self.workflows.keys())
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        return {
            "running": self._running,
            "active_plugins": len(self.active_plugins),
            "registered_plugins": len(self.registry.list_plugins()),
            "registered_workflows": len(self.workflows),
            "event_queue_size": self.event_queue.qsize(),
            "plugin_states": {
                plugin_id: plugin.state.value 
                for plugin_id, plugin in self.active_plugins.items()
            }
        }