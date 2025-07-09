"""Base plugin interfaces and contracts for the LLM REPL plugin system."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol, Union
from pydantic import BaseModel, Field, ConfigDict
import uuid


class PluginState(str, Enum):
    """Plugin lifecycle states."""
    INACTIVE = "inactive"
    ACTIVE = "active"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"


class PluginCapability(str, Enum):
    """Plugin capabilities - what the plugin can do."""
    USER_INPUT = "user_input"
    SYSTEM_CHECK = "system_check"
    WELCOME_MESSAGE = "welcome_message"
    QUERY_PROCESSING = "query_processing"
    RESPONSE_GENERATION = "response_generation"
    DISPLAY_RENDERING = "display_rendering"
    STATE_MANAGEMENT = "state_management"


@dataclass
class PluginMetadata:
    """Metadata about a plugin."""
    name: str
    version: str
    description: str
    author: str
    capabilities: List[PluginCapability]
    dependencies: List[str] = field(default_factory=list)
    config_schema: Optional[Dict[str, Any]] = None
    

class RenderContext(BaseModel):
    """Context information for rendering."""
    display_mode: str = "live"  # live, inscribed, preview
    theme: str = "default"
    width: Optional[int] = None
    height: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    model_config = ConfigDict(arbitrary_types_allowed=True)


class PluginEvent(BaseModel):
    """Event that can be emitted by plugins."""
    event_type: str
    source_plugin: str
    target_plugin: Optional[str] = None
    data: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)
    
    model_config = ConfigDict(arbitrary_types_allowed=True)


class PluginInterface(Protocol):
    """Interface that all plugins must implement."""
    
    @property
    def metadata(self) -> PluginMetadata:
        """Get plugin metadata."""
        ...
    
    @property
    def state(self) -> PluginState:
        """Get current plugin state."""
        ...
    
    async def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialize the plugin with configuration."""
        ...
    
    async def activate(self) -> None:
        """Activate the plugin."""
        ...
    
    async def deactivate(self) -> None:
        """Deactivate the plugin."""
        ...
    
    async def process(self, input_data: Any, context: Dict[str, Any]) -> Any:
        """Process input and return output."""
        ...
    
    async def render(self, context: RenderContext) -> Dict[str, Any]:
        """Render the plugin's output."""
        ...
    
    async def handle_event(self, event: PluginEvent) -> Optional[PluginEvent]:
        """Handle an incoming event."""
        ...


class BlockPlugin(ABC):
    """
    Base class for block plugins.
    
    Each block plugin is a self-contained unit that:
    - Manages its own state and lifecycle
    - Knows how to render itself
    - Can communicate with other plugins via events
    - Is configurable and testable in isolation
    """
    
    def __init__(self, plugin_id: Optional[str] = None):
        self.plugin_id = plugin_id or str(uuid.uuid4())
        self._state = PluginState.INACTIVE
        self._config: Dict[str, Any] = {}
        self._data: Dict[str, Any] = {}
        self._created_at = datetime.now()
        self._activated_at: Optional[datetime] = None
        self._completed_at: Optional[datetime] = None
        self._initialized = False
        
        # Initialize display components
        from .display import PluginTimer, PluginTokenCounter
        self._timer = PluginTimer()
        self._token_counter = PluginTokenCounter()
        
    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        """Get plugin metadata."""
        pass
    
    @property
    def state(self) -> PluginState:
        """Get current plugin state."""
        return self._state
    
    @property
    def plugin_data(self) -> Dict[str, Any]:
        """Get plugin's internal data."""
        return self._data.copy()
    
    async def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialize the plugin with configuration."""
        try:
            self._config = config.copy()
            await self._on_initialize()
            self._initialized = True
            return True
        except Exception as e:
            self._state = PluginState.ERROR
            self._data["error"] = str(e)
            return False
    
    async def activate(self) -> None:
        """Activate the plugin."""
        if not self._initialized:
            raise ValueError(f"Cannot activate plugin in state {self._state}")
        if self._state != PluginState.INACTIVE:
            raise ValueError(f"Cannot activate plugin in state {self._state}")
        
        try:
            self._state = PluginState.ACTIVE
            self._activated_at = datetime.now()
            self._timer.start()
            await self._on_activate()
        except Exception as e:
            # Reset state on activation failure
            self._state = PluginState.INACTIVE
            self._activated_at = None
            self._data["error"] = str(e)
            raise
    
    async def deactivate(self) -> None:
        """Deactivate the plugin."""
        if self._state in [PluginState.PROCESSING]:
            # Allow deactivation from processing state
            pass
        elif self._state not in [PluginState.ACTIVE, PluginState.COMPLETED]:
            raise ValueError(f"Cannot deactivate plugin in state {self._state}")
        
        await self._on_deactivate()
        self._state = PluginState.INACTIVE
    
    async def process(self, input_data: Any, context: Dict[str, Any]) -> Any:
        """Process input and return output."""
        if self._state not in [PluginState.ACTIVE, PluginState.PROCESSING, PluginState.COMPLETED]:
            raise ValueError(f"Cannot process in state {self._state}")
        
        self._state = PluginState.PROCESSING
        try:
            result = await self._on_process(input_data, context)
            self._state = PluginState.COMPLETED
            self._completed_at = datetime.now()
            self._timer.stop()
            return result
        except Exception as e:
            self._state = PluginState.ERROR
            self._data["error"] = str(e)
            self._timer.stop()
            raise
    
    async def render(self, context: RenderContext) -> Dict[str, Any]:
        """Render the plugin's output."""
        try:
            render_data = await self._on_render(context)
            
            # Add plugin metadata to render data
            render_data.update({
                "plugin_id": self.plugin_id,
                "plugin_name": self.metadata.name,
                "plugin_state": self._state,
                "created_at": self._created_at.isoformat(),
                "activated_at": self._activated_at.isoformat() if self._activated_at else None,
                "completed_at": self._completed_at.isoformat() if self._completed_at else None,
            })
            
            # Apply standardized display formatting
            from .display import PluginDisplayFormatter
            
            duration = self._timer.get_duration()
            tokens = self._token_counter.get_counts()
            animated = context.display_mode == "live" and self._state == PluginState.PROCESSING
            
            render_data = PluginDisplayFormatter.standardize_render_data(
                render_data, 
                self.metadata.name, 
                self._state, 
                duration, 
                tokens, 
                animated
            )
            
            return render_data
        except Exception as e:
            # Return error rendering with standardized format
            from .display import PluginDisplayFormatter
            
            error_data = {
                "plugin_id": self.plugin_id,
                "plugin_name": self.metadata.name,
                "plugin_state": PluginState.ERROR,
                "error": str(e),
                "render_type": "error"
            }
            
            return PluginDisplayFormatter.standardize_render_data(
                error_data, 
                self.metadata.name, 
                PluginState.ERROR, 
                self._timer.get_duration(), 
                self._token_counter.get_counts(), 
                False
            )
    
    async def handle_event(self, event: PluginEvent) -> Optional[PluginEvent]:
        """Handle an incoming event."""
        return await self._on_event(event)
    
    def get_plugin_info(self) -> Dict[str, Any]:
        """Get comprehensive plugin information."""
        duration = self._timer.get_duration()
        
        return {
            "plugin_id": self.plugin_id,
            "metadata": {
                "name": self.metadata.name,
                "version": self.metadata.version,
                "description": self.metadata.description,
                "author": self.metadata.author,
                "capabilities": [cap.value for cap in self.metadata.capabilities],
                "dependencies": self.metadata.dependencies,
            },
            "state": self._state,
            "timestamps": {
                "created_at": self._created_at.isoformat(),
                "activated_at": self._activated_at.isoformat() if self._activated_at else None,
                "completed_at": self._completed_at.isoformat() if self._completed_at else None,
                "duration_seconds": duration,
            },
            "config": self._config,
            "data": self._data,
            "tokens": self._token_counter.get_counts(),
        }
    
    def add_input_tokens(self, count: int) -> None:
        """Add input tokens to the counter."""
        self._token_counter.add_input_tokens(count)
    
    def add_output_tokens(self, count: int) -> None:
        """Add output tokens to the counter."""
        self._token_counter.add_output_tokens(count)
    
    def get_token_counts(self) -> Dict[str, int]:
        """Get current token counts."""
        return self._token_counter.get_counts()
    
    def get_duration(self) -> Optional[float]:
        """Get plugin duration in seconds."""
        return self._timer.get_duration()
    
    def get_live_duration(self) -> float:
        """Get live duration in seconds."""
        return self._timer.get_live_duration()
    
    # Abstract methods that subclasses must implement
    
    @abstractmethod
    async def _on_initialize(self) -> None:
        """Called during initialization."""
        pass
    
    @abstractmethod
    async def _on_activate(self) -> None:
        """Called when plugin is activated."""
        pass
    
    @abstractmethod
    async def _on_deactivate(self) -> None:
        """Called when plugin is deactivated."""
        pass
    
    @abstractmethod
    async def _on_process(self, input_data: Any, context: Dict[str, Any]) -> Any:
        """Called to process input data."""
        pass
    
    @abstractmethod
    async def _on_render(self, context: RenderContext) -> Dict[str, Any]:
        """Called to render the plugin's output."""
        pass
    
    async def _on_event(self, event: PluginEvent) -> Optional[PluginEvent]:
        """Called when an event is received. Override to handle events."""
        return None


class PluginRegistry:
    """Registry for discovering and managing plugins."""
    
    def __init__(self):
        self._plugins: Dict[str, type] = {}
        self._instances: Dict[str, BlockPlugin] = {}
        self._plugin_metadata: Dict[str, PluginMetadata] = {}
    
    def register_plugin(self, plugin_class: type) -> None:
        """Register a plugin class."""
        if not issubclass(plugin_class, BlockPlugin):
            raise ValueError("Plugin must be a subclass of BlockPlugin")
        
        # Create a temporary instance to get metadata
        temp_instance = plugin_class()
        metadata = temp_instance.metadata
        
        self._plugins[metadata.name] = plugin_class
        self._plugin_metadata[metadata.name] = metadata
    
    def get_plugin_class(self, plugin_name: str) -> Optional[type]:
        """Get a plugin class by name."""
        return self._plugins.get(plugin_name)
    
    def get_plugin_metadata(self, plugin_name: str) -> Optional[PluginMetadata]:
        """Get plugin metadata by name."""
        return self._plugin_metadata.get(plugin_name)
    
    def list_plugins(self) -> List[str]:
        """List all registered plugin names."""
        return list(self._plugins.keys())
    
    def list_plugins_by_capability(self, capability: PluginCapability) -> List[str]:
        """List plugins that have a specific capability."""
        matching_plugins = []
        for name, metadata in self._plugin_metadata.items():
            if capability in metadata.capabilities:
                matching_plugins.append(name)
        return matching_plugins
    
    async def create_plugin_instance(self, plugin_name: str, 
                                   config: Dict[str, Any] = None) -> Optional[BlockPlugin]:
        """Create and initialize a plugin instance."""
        plugin_class = self.get_plugin_class(plugin_name)
        if not plugin_class:
            return None
        
        instance = plugin_class()
        success = await instance.initialize(config or {})
        if not success:
            return None
        
        instance_id = instance.plugin_id
        self._instances[instance_id] = instance
        return instance
    
    def get_plugin_instance(self, instance_id: str) -> Optional[BlockPlugin]:
        """Get a plugin instance by ID."""
        return self._instances.get(instance_id)
    
    def remove_plugin_instance(self, instance_id: str) -> None:
        """Remove a plugin instance."""
        self._instances.pop(instance_id, None)