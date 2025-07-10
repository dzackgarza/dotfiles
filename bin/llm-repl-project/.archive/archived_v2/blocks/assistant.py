"""Assistant response block implementation."""

from typing import Dict, Any, Optional
from .base import Block, BlockType


class AssistantBlock(Block):
    """
    Represents the assistant's response as a single atomic block.
    """
    
    def __init__(self, response: str, routing_info: Optional[str] = None):
        super().__init__(BlockType.ASSISTANT, "Research Assistant", response)
        self.response = response
        self.routing_info = routing_info
    
    def _on_start(self) -> None:
        """Assistant blocks start when response begins."""
        self.content.metadata["status"] = "generating"
    
    def _on_complete(self) -> None:
        """Assistant blocks complete when response is fully generated."""
        self.content.metadata["status"] = "complete"
        if self.routing_info:
            self.content.metadata["routing_info"] = self.routing_info
    
    def render_live(self) -> Dict[str, Any]:
        """Render assistant response in live state."""
        return {
            "id": self.id,
            "type": self.metadata.type,
            "state": self.metadata.state,
            "title": self.content.title,
            "body": self.response,
            "style": "assistant_response",
            "box_style": "rounded",
            "show_typing_indicator": True
        }
    
    def render_inscribed(self) -> Dict[str, Any]:
        """Render assistant response in inscribed state."""
        render_data = {
            "id": self.id,
            "type": self.metadata.type,
            "state": self.metadata.state,
            "title": self.content.title,
            "body": self.response,
            "style": "assistant_response",
            "box_style": "rounded",
            "timestamp": self.metadata.created_at.isoformat()
        }
        if self.routing_info:
            render_data["footer"] = self.routing_info
        return render_data