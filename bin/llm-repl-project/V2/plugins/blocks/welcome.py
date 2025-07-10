"""Welcome plugin - displays welcome messages as an independent plugin."""

from typing import Any, Dict
from datetime import datetime

from ..base import BlockPlugin, PluginMetadata, PluginCapability, RenderContext


class WelcomePlugin(BlockPlugin):
    """
    Plugin that displays welcome messages.
    
    This plugin is completely self-contained and manages:
    - Displaying welcome messages
    - Customizing welcome content
    - Rendering welcome display
    - Providing system information
    """
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="welcome",
            version="1.0.0",
            description="Displays welcome messages and system information",
            author="LLM REPL Team",
            capabilities=[PluginCapability.WELCOME_MESSAGE, PluginCapability.DISPLAY_RENDERING],
            dependencies=[],
            config_schema={
                "type": "object",
                "properties": {
                    "version": {"type": "string", "default": "v3"},
                    "show_help": {"type": "boolean", "default": True},
                    "show_commands": {"type": "boolean", "default": True},
                    "custom_message": {"type": "string", "default": ""},
                    "theme": {"type": "string", "default": "default"}
                }
            }
        )
    
    async def _on_initialize(self) -> None:
        """Initialize the welcome plugin."""
        self._data.update({
            "version": self._config.get("version", "v3"),
            "show_help": self._config.get("show_help", True),
            "show_commands": self._config.get("show_commands", True),
            "custom_message": self._config.get("custom_message", ""),
            "theme": self._config.get("theme", "default"),
            "display_timestamp": None,
            "welcome_content": ""
        })
    
    async def _on_activate(self) -> None:
        """Activate the welcome plugin."""
        self._data["display_timestamp"] = datetime.now().isoformat()
        
        # Generate welcome content
        welcome_content = self._generate_welcome_content()
        self._data["welcome_content"] = welcome_content
    
    async def _on_deactivate(self) -> None:
        """Deactivate the welcome plugin."""
        pass
    
    async def _on_process(self, input_data: Any, context: Dict[str, Any]) -> Any:
        """Process welcome message generation."""
        # input_data can contain custom welcome parameters
        if isinstance(input_data, dict):
            # Update data with any provided parameters
            for key in ["version", "show_help", "show_commands", "custom_message", "theme"]:
                if key in input_data:
                    self._data[key] = input_data[key]
        
        # Generate welcome content based on current data
        welcome_content = self._generate_welcome_content()
        self._data["welcome_content"] = welcome_content
        
        return {
            "welcome_content": welcome_content,
            "version": self._data["version"],
            "timestamp": self._data["display_timestamp"],
            "plugin_id": self.plugin_id
        }
    
    def _generate_welcome_content(self) -> str:
        """Generate the welcome message content."""
        version = self._data.get("version", "v3")
        custom_message = self._data.get("custom_message", "")
        show_help = self._data.get("show_help", True)
        show_commands = self._data.get("show_commands", True)
        
        # Start with basic welcome
        if custom_message:
            content = custom_message
        else:
            content = f"Welcome to LLM REPL {version}! Type your queries below."
        
        # Add help information if enabled
        if show_help:
            content += "\n\n💡 This is an AI-powered research assistant with unified block architecture."
        
        # Add commands if enabled
        if show_commands:
            content += "\n\n🔧 Available commands:"
            content += "\n   • Type any question or request"
            content += "\n   • Use 'exit' or 'quit' to exit"
            content += "\n   • All interactions are logged and validated"
        
        return content
    
    async def _on_render(self, context: RenderContext) -> Dict[str, Any]:
        """Render the welcome display."""
        version = self._data.get("version", "v3")
        welcome_content = self._data.get("welcome_content", "")
        
        # Base render data
        render_data = {
            "render_type": "welcome",
            "title": f"🚀 LLM REPL {version}",
            "content": welcome_content,
            "display_mode": context.display_mode,
            "style": {
                "box_style": "heavy",
                "border_color": "blue",
                "title_style": "bold",
            }
        }
        
        # Add theme-specific styling
        theme = self._data.get("theme", "default")
        if theme == "minimal":
            render_data["style"]["box_style"] = "rounded"
            render_data["style"]["border_color"] = "dim"
        elif theme == "fancy":
            render_data["style"]["box_style"] = "double"
            render_data["style"]["border_color"] = "bright_blue"
        
        # Add metadata for inscribed mode
        if context.display_mode == "inscribed":
            render_data["metadata"] = {
                "displayed_at": self._data.get("display_timestamp"),
                "version": version,
                "content_length": len(welcome_content),
                "theme": theme
            }
        
        return render_data
    
    def get_welcome_info(self) -> Dict[str, Any]:
        """Get information about the welcome message."""
        return {
            "version": self._data.get("version"),
            "content": self._data.get("welcome_content", ""),
            "display_timestamp": self._data.get("display_timestamp"),
            "theme": self._data.get("theme"),
            "features": {
                "help_shown": self._data.get("show_help", True),
                "commands_shown": self._data.get("show_commands", True),
                "custom_message": bool(self._data.get("custom_message"))
            }
        }
    
    def update_version(self, version: str) -> None:
        """Update the version displayed in the welcome message."""
        self._data["version"] = version
        self._data["welcome_content"] = self._generate_welcome_content()
    
    def set_custom_message(self, message: str) -> None:
        """Set a custom welcome message."""
        self._data["custom_message"] = message
        self._data["welcome_content"] = self._generate_welcome_content()
    
    def set_theme(self, theme: str) -> None:
        """Set the display theme."""
        self._data["theme"] = theme