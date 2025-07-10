"""
Timeline Manager - Timeline State Management

Extracted from V2's working implementation and enhanced.
Manages the timeline state and block operations.
"""

from typing import List, Optional, Callable
from .blocks import TimelineBlock, BlockType, create_system_check_block, create_welcome_block


class TimelineManager:
    """
    Manages timeline state and operations.
    
    Extracted from V2's working timeline management and enhanced
    with better organization and event handling.
    """
    
    def __init__(self):
        self.blocks: List[TimelineBlock] = []
        self.observers: List[Callable[[TimelineBlock], None]] = []
    
    def add_block(self, block: TimelineBlock):
        """Add a block to the timeline and notify observers."""
        self.blocks.append(block)
        self._notify_observers(block)
    
    def clear_timeline(self):
        """Clear all blocks from the timeline."""
        self.blocks.clear()
    
    def get_blocks(self) -> List[TimelineBlock]:
        """Get all timeline blocks."""
        return self.blocks.copy()
    
    def get_block_count(self) -> int:
        """Get the number of blocks in the timeline."""
        return len(self.blocks)
    
    def get_latest_block(self) -> Optional[TimelineBlock]:
        """Get the most recently added block."""
        return self.blocks[-1] if self.blocks else None
    
    def get_blocks_by_type(self, block_type: BlockType) -> List[TimelineBlock]:
        """Get all blocks of a specific type."""
        return [block for block in self.blocks if block.type == block_type]
    
    def get_total_tokens(self) -> dict:
        """Get total token usage across all blocks."""
        total = {"input": 0, "output": 0}
        for block in self.blocks:
            total["input"] += block.tokens.get("input", 0)
            total["output"] += block.tokens.get("output", 0)
        return total
    
    def get_conversation_summary(self) -> dict:
        """Get a summary of the conversation."""
        user_inputs = len(self.get_blocks_by_type(BlockType.USER_INPUT))
        assistant_responses = len(self.get_blocks_by_type(BlockType.ASSISTANT_RESPONSE))
        cognition_blocks = len(self.get_blocks_by_type(BlockType.COGNITION))
        errors = len(self.get_blocks_by_type(BlockType.ERROR))
        
        return {
            "total_blocks": len(self.blocks),
            "user_inputs": user_inputs,
            "assistant_responses": assistant_responses,
            "cognition_blocks": cognition_blocks,
            "errors": errors,
            "total_tokens": self.get_total_tokens()
        }
    
    def initialize_with_startup_blocks(self, config_name: str):
        """Initialize timeline with startup blocks."""
        # Add system check block
        system_check = create_system_check_block(config_name)
        self.add_block(system_check)
        
        # Add welcome block
        welcome = create_welcome_block(config_name)
        self.add_block(welcome)
    
    def add_observer(self, observer: Callable[[TimelineBlock], None]):
        """Add an observer that gets notified when blocks are added."""
        self.observers.append(observer)
    
    def remove_observer(self, observer: Callable[[TimelineBlock], None]):
        """Remove an observer."""
        if observer in self.observers:
            self.observers.remove(observer)
    
    def _notify_observers(self, block: TimelineBlock):
        """Notify all observers about a new block."""
        for observer in self.observers:
            try:
                observer(block)
            except Exception as e:
                # Don't let observer errors break the timeline
                print(f"Observer error: {e}")
    
    def export_timeline(self) -> List[dict]:
        """Export timeline as a list of dictionaries."""
        return [
            {
                "id": block.id,
                "type": block.type.value,
                "title": block.title,
                "content": block.content,
                "timestamp": block.timestamp,
                "tokens": block.tokens,
                "metadata": block.metadata
            }
            for block in self.blocks
        ]
    
    def get_timeline_text(self) -> str:
        """Get timeline as formatted text."""
        lines = []
        for i, block in enumerate(self.blocks):
            if i > 0:
                lines.append("─" * 80)
            
            lines.append(block.get_formatted_header())
            lines.append(block.content)
            lines.append("")  # Empty line
        
        return "\n".join(lines)