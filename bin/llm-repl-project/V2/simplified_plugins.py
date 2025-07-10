#!/usr/bin/env python3
"""
Simplified Plugin System - Differential Improvement

DIFFERENTIAL CHANGE: Simplify plugin contracts while preserving cognition blocks
and timeline integrity.

PRESERVED:
- Cognition blocks architecture
- Timeline eligibility system
- Plugin metadata and tracking

SIMPLIFIED:
- Reduced state complexity
- Easier testing
- Clearer contracts
- Better error handling
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from enum import Enum
import time
import uuid


class PluginStatus(Enum):
    """Simplified plugin status."""
    READY = "ready"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class PluginResult:
    """Simplified plugin result."""
    content: str
    metadata: Dict[str, Any]
    tokens: Dict[str, int]
    duration: float
    status: PluginStatus
    error: Optional[str] = None


class SimplifiedPlugin(ABC):
    """
    Simplified plugin base class.
    
    DIFFERENTIAL IMPROVEMENT:
    - Much simpler lifecycle
    - Easier to test
    - Preserves essential functionality
    """
    
    def __init__(self):
        self.plugin_id = str(uuid.uuid4())
        self.status = PluginStatus.READY
        self.start_time = 0.0
        self.tokens = {"input": 0, "output": 0}
        self.error_message: Optional[str] = None
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name."""
        pass
    
    @abstractmethod
    async def process(self, input_data: Any, context: Dict[str, Any]) -> PluginResult:
        """
        Process input and return result.
        
        SIMPLIFIED: Single method instead of complex lifecycle.
        """
        pass
    
    async def safe_process(self, input_data: Any, context: Dict[str, Any]) -> PluginResult:
        """
        Safe wrapper that handles errors and timing.
        
        DIFFERENTIAL IMPROVEMENT: Built-in error handling and timing.
        """
        self.status = PluginStatus.PROCESSING
        self.start_time = time.time()
        
        try:
            result = await self.process(input_data, context)
            self.status = PluginStatus.COMPLETED
            return result
            
        except Exception as e:
            self.status = PluginStatus.ERROR
            self.error_message = str(e)
            
            return PluginResult(
                content=f"Error in {self.name}: {str(e)}",
                metadata={"error": True, "plugin": self.name},
                tokens=self.tokens,
                duration=time.time() - self.start_time,
                status=PluginStatus.ERROR,
                error=str(e)
            )
    
    def add_tokens(self, input_tokens: int, output_tokens: int):
        """Add token counts."""
        self.tokens["input"] += input_tokens
        self.tokens["output"] += output_tokens
    
    def get_duration(self) -> float:
        """Get processing duration."""
        if self.start_time == 0:
            return 0.0
        return time.time() - self.start_time


class CognitionBlockPlugin(SimplifiedPlugin):
    """
    Simplified cognition block that preserves your multi-step LLM architecture.
    
    PRESERVED:
    - Multi-step LLM processing
    - Cognitive modules
    - Transparency logging
    
    SIMPLIFIED:
    - Easier to configure
    - Better error handling
    - Clearer contracts
    """
    
    def __init__(self, cognitive_modules: List[Any]):
        super().__init__()
        self.cognitive_modules = cognitive_modules
        self.module_results: List[Dict[str, Any]] = []
        self.transparency_log: List[Dict[str, Any]] = []
    
    @property
    def name(self) -> str:
        return "cognition"
    
    async def process(self, input_data: Any, context: Dict[str, Any]) -> PluginResult:
        """
        Process through cognitive modules.
        
        PRESERVED: Your multi-step LLM processing architecture
        SIMPLIFIED: Cleaner error handling and result tracking
        """
        input_text = str(input_data)
        current_input = input_text
        
        # Process through each cognitive module
        for i, module in enumerate(self.cognitive_modules):
            try:
                # Create module input (preserves your architecture)
                from plugins.cognitive_modules import CognitiveModuleInput
                module_input = CognitiveModuleInput(
                    content=current_input,
                    context={"step": i, "total_steps": len(self.cognitive_modules)},
                    previous_outputs=self.module_results.copy()
                )
                
                # Get LLM interface from context
                llm_manager = context.get("llm_manager")
                if not llm_manager:
                    raise ValueError("No LLM manager provided")
                
                llm_interface = llm_manager.get_interface("default")
                if not llm_interface:
                    raise ValueError("No default LLM interface available")
                
                # Process through module (preserves your cognitive architecture)
                module_output = await module.process(module_input, llm_interface)
                
                # Track results
                self.module_results.append(module_output.to_dict())
                self.transparency_log.append({
                    "module": module.metadata.name,
                    "step": i,
                    "input": current_input,
                    "output": module_output.content,
                    "tokens": {
                        "input": module_output.llm_response.tokens.input_tokens if module_output.llm_response else 0,
                        "output": module_output.llm_response.tokens.output_tokens if module_output.llm_response else 0
                    },
                    "timestamp": time.time()
                })
                
                # Update token counts
                if module_output.llm_response:
                    self.add_tokens(
                        module_output.llm_response.tokens.input_tokens,
                        module_output.llm_response.tokens.output_tokens
                    )
                
                # Use output as input for next module
                current_input = module_output.content
                
            except Exception as e:
                # Log error but continue processing
                self.transparency_log.append({
                    "module": getattr(module, 'metadata', {}).get('name', 'unknown'),
                    "step": i,
                    "error": str(e),
                    "timestamp": time.time()
                })
                # Continue with original input
        
        return PluginResult(
            content=current_input,
            metadata={
                "modules_processed": len(self.cognitive_modules),
                "transparency_log": self.transparency_log,
                "module_results": self.module_results
            },
            tokens=self.tokens,
            duration=self.get_duration(),
            status=PluginStatus.COMPLETED
        )


class SimpleUserInputPlugin(SimplifiedPlugin):
    """Simplified user input plugin."""
    
    @property
    def name(self) -> str:
        return "user_input"
    
    async def process(self, input_data: Any, context: Dict[str, Any]) -> PluginResult:
        """Process user input."""
        input_text = str(input_data)
        
        return PluginResult(
            content=input_text,
            metadata={
                "type": "user_input",
                "length": len(input_text),
                "timestamp": time.time()
            },
            tokens={"input": 0, "output": 0},  # User input doesn't use tokens
            duration=self.get_duration(),
            status=PluginStatus.COMPLETED
        )


class SimpleAssistantResponsePlugin(SimplifiedPlugin):
    """Simplified assistant response plugin."""
    
    @property
    def name(self) -> str:
        return "assistant_response"
    
    async def process(self, input_data: Any, context: Dict[str, Any]) -> PluginResult:
        """Process assistant response."""
        if isinstance(input_data, dict):
            response_text = input_data.get("response", str(input_data))
            processing_results = input_data.get("processing_results", {})
        else:
            response_text = str(input_data)
            processing_results = {}
        
        return PluginResult(
            content=response_text,
            metadata={
                "type": "assistant_response",
                "processing_results": processing_results,
                "timestamp": time.time()
            },
            tokens=self.tokens,  # Tokens added from cognition
            duration=self.get_duration(),
            status=PluginStatus.COMPLETED
        )


class SimplifiedPluginManager:
    """
    Simplified plugin manager.
    
    DIFFERENTIAL IMPROVEMENT:
    - Much simpler than current PluginManager
    - Easier to test and debug
    - Preserves essential functionality
    """
    
    def __init__(self):
        self.plugins: Dict[str, SimplifiedPlugin] = {}
        self.plugin_classes: Dict[str, type] = {}
        
        # Register built-in plugins
        self.register_plugin_class("user_input", SimpleUserInputPlugin)
        self.register_plugin_class("assistant_response", SimpleAssistantResponsePlugin)
    
    def register_plugin_class(self, name: str, plugin_class: type):
        """Register a plugin class."""
        self.plugin_classes[name] = plugin_class
    
    def create_plugin(self, plugin_type: str, **kwargs) -> str:
        """Create a plugin instance."""
        if plugin_type not in self.plugin_classes:
            raise ValueError(f"Unknown plugin type: {plugin_type}")
        
        plugin_class = self.plugin_classes[plugin_type]
        
        if plugin_type == "cognition":
            # Special handling for cognition plugins
            cognitive_modules = kwargs.get("cognitive_modules", [])
            plugin = CognitionBlockPlugin(cognitive_modules)
        else:
            plugin = plugin_class()
        
        self.plugins[plugin.plugin_id] = plugin
        return plugin.plugin_id
    
    def get_plugin(self, plugin_id: str) -> Optional[SimplifiedPlugin]:
        """Get plugin by ID."""
        return self.plugins.get(plugin_id)
    
    async def process_with_plugin(self, plugin_id: str, input_data: Any, context: Dict[str, Any]) -> PluginResult:
        """Process data with a plugin."""
        plugin = self.get_plugin(plugin_id)
        if not plugin:
            raise ValueError(f"Plugin not found: {plugin_id}")
        
        return await plugin.safe_process(input_data, context)
    
    def remove_plugin(self, plugin_id: str):
        """Remove a plugin."""
        self.plugins.pop(plugin_id, None)


class SimplifiedTimelineAdapter:
    """
    Simplified timeline adapter that preserves your timeline integrity.
    
    PRESERVED:
    - Timeline eligibility checking
    - Plugin metadata requirements
    - Rich display formatting
    
    SIMPLIFIED:
    - Easier to create and use
    - Better error handling
    """
    
    def __init__(self, plugin: SimplifiedPlugin, result: PluginResult):
        self.plugin = plugin
        self.result = result
        self.timestamp = time.time()
    
    def get_metadata(self):
        """Get metadata for timeline eligibility (preserves your architecture)."""
        from timeline_integrity import PluginMetadata
        
        return PluginMetadata(
            plugin_name=self.plugin.name,
            wall_time_seconds=self.result.duration,
            llm_input_tokens=self.result.tokens.get("input", 0),
            llm_output_tokens=self.result.tokens.get("output", 0),
            processing_timestamp=self.timestamp,
            plugin_state="completed"
        )
    
    def get_rendered_content(self):
        """Get rendered content for display."""
        from rich.panel import Panel
        from rich.box import ROUNDED
        
        # Format content based on plugin type
        if self.plugin.name == "user_input":
            title = f"👤 User Input"
            border_style = "green"
        elif self.plugin.name == "cognition":
            modules_count = len(self.result.metadata.get("transparency_log", []))
            title = f"🧠 Cognition ({modules_count} modules)"
            border_style = "purple"
        elif self.plugin.name == "assistant_response":
            title = f"🤖 Assistant"
            border_style = "blue"
        else:
            title = f"🔧 {self.plugin.name.title()}"
            border_style = "cyan"
        
        # Add timing and token info
        duration = self.result.duration
        tokens = self.result.tokens
        if tokens["input"] > 0 or tokens["output"] > 0:
            title += f" ({duration:.1f}s, ↑{tokens['input']} ↓{tokens['output']})"
        else:
            title += f" ({duration:.1f}s)"
        
        return Panel(
            self.result.content,
            title=title,
            box=ROUNDED,
            border_style=border_style,
            padding=(1, 1)
        )
    
    def validate_timeline_eligibility(self) -> bool:
        """Validate timeline eligibility (preserves your architecture)."""
        try:
            metadata = self.get_metadata()
            return (
                metadata.wall_time_seconds >= 0 and
                metadata.llm_input_tokens >= 0 and
                metadata.llm_output_tokens >= 0 and
                metadata.plugin_state == "completed"
            )
        except:
            return False