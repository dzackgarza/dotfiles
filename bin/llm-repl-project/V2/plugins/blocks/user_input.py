"""User input plugin - displays submitted user input in inscribed state only."""

from typing import Any, Dict
from datetime import datetime

from ..base import BlockPlugin, PluginMetadata, PluginCapability, RenderContext


class UserInputPlugin(BlockPlugin):
    """
    Plugin that displays submitted user input.
    
    This plugin handles the inscribed display of user input after it has been
    submitted through the persistent input system. It does not handle live input
    capture, which is managed by the UI input system.
    
    Features:
    - Displays submitted input in a clean, consistent format
    - Shows input metadata (timestamp, length, etc.)
    - Validates input constraints
    - Provides input history for the timeline
    """
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="user_input",
            version="1.0.0",
            description="Handles user input capture and display",
            author="LLM REPL Team",
            capabilities=[PluginCapability.USER_INPUT, PluginCapability.DISPLAY_RENDERING],
            dependencies=[],
            config_schema={
                "type": "object",
                "properties": {
                    "max_length": {"type": "integer", "default": 10000},
                    "allow_empty": {"type": "boolean", "default": False},
                    "prompt_style": {"type": "string", "default": "default"}
                }
            }
        )
    
    async def _on_initialize(self) -> None:
        """Initialize the user input plugin."""
        self._data.update({
            "max_length": self._config.get("max_length", 10000),
            "allow_empty": self._config.get("allow_empty", False),
            "prompt_style": self._config.get("prompt_style", "default"),
            "user_input": "",
            "input_timestamp": None,
            "validation_errors": []
        })
    
    async def _on_activate(self) -> None:
        """Activate the user input plugin."""
        self._data["activated_at"] = datetime.now().isoformat()
    
    async def _on_deactivate(self) -> None:
        """Deactivate the user input plugin."""
        self._data["deactivated_at"] = datetime.now().isoformat()
    
    async def _on_process(self, input_data: Any, context: Dict[str, Any]) -> Any:
        """Process user input."""
        if isinstance(input_data, str):
            user_input = input_data
        elif isinstance(input_data, dict) and "input" in input_data:
            user_input = input_data["input"]
        else:
            raise ValueError("Invalid input data for user input plugin")
        
        # Validate input
        validation_errors = []
        
        if not user_input.strip() and not self._data["allow_empty"]:
            validation_errors.append("Input cannot be empty")
        
        if len(user_input) > self._data["max_length"]:
            validation_errors.append(f"Input exceeds maximum length of {self._data['max_length']}")
        
        if validation_errors:
            self._data["validation_errors"] = validation_errors
            raise ValueError(f"Input validation failed: {', '.join(validation_errors)}")
        
        # Store the input
        self._data.update({
            "user_input": user_input,
            "input_timestamp": datetime.now().isoformat(),
            "validation_errors": [],
            "processed": True
        })
        
        return {
            "input": user_input,
            "timestamp": self._data["input_timestamp"],
            "plugin_id": self.plugin_id
        }
    
    async def _on_render(self, context: RenderContext) -> Dict[str, Any]:
        """Render the user input display."""
        user_input = self._data.get("user_input", "")
        
        # Base render data
        render_data = {
            "render_type": "user_input",
            "content": user_input,
            "display_mode": context.display_mode,
            "style": {
                "box_style": "rounded",
                "border_color": "green",
                "title_style": "bold",
            }
        }
        
        # Note: Title will be set by standardized display formatter
        
        # Add state-specific content
        if self._state.value == "completed":
            render_data["timestamp"] = self._data.get("input_timestamp")
            render_data["style"]["border_color"] = "green"
        elif self._state.value == "error":
            render_data["error_message"] = self._data.get("validation_errors", [])
            render_data["style"]["border_color"] = "red"
        
        # Add metadata (this plugin is primarily for inscribed display)
        render_data["metadata"] = {
            "processed_at": self._data.get("input_timestamp"),
            "character_count": len(user_input),
            "word_count": len(user_input.split()) if user_input else 0,
            "multiline": "\n" in user_input
        }
        
        return render_data
    
    def get_user_input(self) -> str:
        """Get the captured user input."""
        return self._data.get("user_input", "")
    
    def get_input_metadata(self) -> Dict[str, Any]:
        """Get metadata about the input."""
        return {
            "input_length": len(self._data.get("user_input", "")),
            "input_timestamp": self._data.get("input_timestamp"),
            "validation_errors": self._data.get("validation_errors", []),
            "processed": self._data.get("processed", False)
        }