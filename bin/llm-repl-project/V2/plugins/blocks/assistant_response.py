"""Assistant response plugin - handles assistant responses as an independent plugin."""

from typing import Any, Dict, Optional
from datetime import datetime

from ..base import BlockPlugin, PluginMetadata, PluginCapability, RenderContext


class AssistantResponsePlugin(BlockPlugin):
    """
    Plugin that handles assistant responses.
    
    This plugin is completely self-contained and manages:
    - Generating assistant responses
    - Formatting response content
    - Rendering response display
    - Tracking response metadata
    """
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="assistant_response",
            version="1.0.0",
            description="Handles assistant response generation and display",
            author="LLM REPL Team",
            capabilities=[PluginCapability.RESPONSE_GENERATION, PluginCapability.DISPLAY_RENDERING],
            dependencies=[],
            config_schema={
                "type": "object",
                "properties": {
                    "max_length": {"type": "integer", "default": 50000},
                    "format_markdown": {"type": "boolean", "default": True},
                    "show_metadata": {"type": "boolean", "default": True},
                    "response_style": {"type": "string", "default": "default"}
                }
            }
        )
    
    async def _on_initialize(self) -> None:
        """Initialize the assistant response plugin."""
        self._data.update({
            "max_length": self._config.get("max_length", 50000),
            "format_markdown": self._config.get("format_markdown", True),
            "show_metadata": self._config.get("show_metadata", True),
            "response_style": self._config.get("response_style", "default"),
            "response_content": "",
            "response_metadata": {},
            "generation_start_time": None,
            "generation_end_time": None,
            "original_query": "",
            "routing_info": ""
        })
    
    async def _on_activate(self) -> None:
        """Activate the assistant response plugin."""
        self._data["generation_start_time"] = datetime.now().isoformat()
    
    async def _on_deactivate(self) -> None:
        """Deactivate the assistant response plugin."""
        if not self._data.get("generation_end_time"):
            self._data["generation_end_time"] = datetime.now().isoformat()
    
    async def _on_process(self, input_data: Any, context: Dict[str, Any]) -> Any:
        """Process assistant response generation."""
        # Extract response data from input
        if isinstance(input_data, str):
            response_content = input_data
            routing_info = ""
        elif isinstance(input_data, dict):
            response_content = input_data.get("response", input_data.get("content", ""))
            routing_info = input_data.get("routing_info", "")
            self._data["original_query"] = input_data.get("query", "")
            
            # Extract metadata from processing results
            if "processing_results" in input_data:
                processing_results = input_data["processing_results"]
                self._data["response_metadata"].update({
                    "tokens": processing_results.get("total_tokens", {}),
                    "processing_duration": processing_results.get("processing_duration", 0),
                    "processing_steps": list(processing_results.get("step_results", {}).keys())
                })
        else:
            raise ValueError("Assistant response plugin requires string or dict input")
        
        # Validate response length
        if len(response_content) > self._data["max_length"]:
            response_content = response_content[:self._data["max_length"]] + "... [truncated]"
        
        # Format response if markdown is enabled
        if self._data["format_markdown"]:
            formatted_content = self._format_markdown(response_content)
        else:
            formatted_content = response_content
        
        # Update plugin data
        self._data.update({
            "response_content": formatted_content,
            "routing_info": routing_info,
            "generation_end_time": datetime.now().isoformat(),
            "content_length": len(response_content),
            "word_count": len(response_content.split()) if response_content else 0
        })
        
        return {
            "response": formatted_content,
            "routing_info": routing_info,
            "metadata": self._data["response_metadata"],
            "generation_duration": self._get_generation_duration(),
            "plugin_id": self.plugin_id
        }
    
    def _format_markdown(self, content: str) -> str:
        """Format content with markdown processing."""
        # Basic markdown formatting - in a real implementation,
        # this would use a proper markdown processor
        
        # For now, just ensure proper line breaks and spacing
        formatted = content.strip()
        
        # Add basic formatting hints
        if self._data["response_style"] == "enhanced":
            # Add some basic enhancements
            formatted = formatted.replace("**", "**")  # Keep bold
            formatted = formatted.replace("*", "*")    # Keep italic
            formatted = formatted.replace("`", "`")    # Keep code
        
        return formatted
    
    async def _on_render(self, context: RenderContext) -> Dict[str, Any]:
        """Render the assistant response display."""
        response_content = self._data.get("response_content", "")
        routing_info = self._data.get("routing_info", "")
        
        # Base render data
        render_data = {
            "render_type": "assistant_response",
            "title": "Research Assistant",
            "content": response_content,
            "display_mode": context.display_mode,
            "style": {
                "box_style": "rounded",
                "border_color": "blue",
                "title_style": "bold",
            }
        }
        
        # Add state-specific content and styling
        if self._state.value == "processing":
            render_data.update({
                "title": "Research Assistant (generating...)",
                "content": "Generating response...",
                "style": {"border_color": "yellow", "show_typing_indicator": True}
            })
            
        elif self._state.value == "completed":
            render_data.update({
                "style": {"border_color": "blue"},
                "completed": True
            })
            
            # Add routing info as footer
            if routing_info:
                render_data["footer"] = routing_info
            
            # Add metadata for inscribed mode
            if context.display_mode == "inscribed":
                render_data["metadata"] = {
                    "generated_at": self._data.get("generation_end_time"),
                    "generation_duration": self._get_generation_duration(),
                    "content_length": self._data.get("content_length", 0),
                    "word_count": self._data.get("word_count", 0),
                    "routing_info": routing_info
                }
                
                # Add response metadata if available
                if self._data.get("show_metadata"):
                    response_metadata = self._data.get("response_metadata", {})
                    if response_metadata:
                        render_data["response_metadata"] = response_metadata
        
        elif self._state.value == "error":
            render_data.update({
                "title": "Research Assistant (error)",
                "content": "❌ Error generating response",
                "style": {"border_color": "red"},
                "error": True
            })
        
        # Apply response style
        response_style = self._data.get("response_style", "default")
        if response_style == "minimal":
            render_data["style"]["box_style"] = "ascii"
        elif response_style == "enhanced":
            render_data["style"]["box_style"] = "double"
            render_data["style"]["border_color"] = "bright_blue"
        
        return render_data
    
    def _get_generation_duration(self) -> float:
        """Get response generation duration."""
        start_time = self._data.get("generation_start_time")
        end_time = self._data.get("generation_end_time")
        
        if not start_time or not end_time:
            return 0.0
        
        try:
            start_dt = datetime.fromisoformat(start_time)
            end_dt = datetime.fromisoformat(end_time)
            return (end_dt - start_dt).total_seconds()
        except:
            return 0.0
    
    def get_response_info(self) -> Dict[str, Any]:
        """Get comprehensive response information."""
        return {
            "response_content": self._data.get("response_content", ""),
            "routing_info": self._data.get("routing_info", ""),
            "original_query": self._data.get("original_query", ""),
            "generation_duration": self._get_generation_duration(),
            "content_stats": {
                "character_count": self._data.get("content_length", 0),
                "word_count": self._data.get("word_count", 0),
                "formatted_markdown": self._data.get("format_markdown", True)
            },
            "metadata": self._data.get("response_metadata", {}),
            "generation_timestamps": {
                "start": self._data.get("generation_start_time"),
                "end": self._data.get("generation_end_time")
            }
        }
    
    def update_response(self, new_content: str, routing_info: str = "") -> None:
        """Update the response content (for streaming responses)."""
        self._data["response_content"] = new_content
        self._data["routing_info"] = routing_info
        self._data["content_length"] = len(new_content)
        self._data["word_count"] = len(new_content.split()) if new_content else 0
    
    def append_to_response(self, additional_content: str) -> None:
        """Append content to the current response (for streaming)."""
        current_content = self._data.get("response_content", "")
        new_content = current_content + additional_content
        self._data["response_content"] = new_content
        self._data["content_length"] = len(new_content)
        self._data["word_count"] = len(new_content.split()) if new_content else 0