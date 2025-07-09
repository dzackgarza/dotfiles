"""User input block implementation."""

from typing import Dict, Any
from .base import Block, BlockType


class UserBlock(Block):
    """
    Represents user input as a single atomic block.
    No more split states - the user's message is captured and displayed as one unit.
    """
    
    def __init__(self, user_input: str):
        super().__init__(BlockType.USER, "You", user_input)
        self.user_input = user_input
    
    def _on_start(self) -> None:
        """User blocks start immediately when created."""
        pass
    
    def _on_complete(self) -> None:
        """User blocks complete immediately after display."""
        pass
    
    def render_live(self) -> Dict[str, Any]:
        """Render user input in live state."""
        return {
            "id": self.id,
            "type": self.metadata.type,
            "state": self.metadata.state,
            "title": "You",
            "body": self.user_input,
            "style": "user_input",
            "box_style": "rounded",
            "show_header": True
        }
    
    def render_inscribed(self) -> Dict[str, Any]:
        """Render user input in inscribed state."""
        return {
            "id": self.id,
            "type": self.metadata.type,
            "state": self.metadata.state,
            "title": "You",
            "body": self.user_input,
            "style": "user_input",
            "box_style": "rounded",
            "show_header": True,
            "timestamp": self.metadata.created_at.isoformat()
        }