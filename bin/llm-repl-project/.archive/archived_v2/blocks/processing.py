"""Processing blocks for internal operations."""

from typing import Dict, Any, List, Optional
from .base import Block, BlockType


class ProcessingSubBlock(Block):
    """A single processing step within the internal processing pipeline."""
    
    def __init__(self, title: str, methodology: str):
        super().__init__(BlockType.PROCESSING_SUB, title)
        self.methodology = methodology
        self.tokens_sent: int = 0
        self.tokens_received: int = 0
        self.result: Optional[str] = None
        self.routing_conclusion: Optional[str] = None
    
    def _on_start(self) -> None:
        """Start processing."""
        self.content.metadata["status"] = "processing"
        self.content.metadata["message"] = self.methodology
    
    def _on_complete(self) -> None:
        """Complete processing."""
        self.content.metadata["status"] = "complete"
        if self.routing_conclusion:
            self.content.metadata["routing_conclusion"] = self.routing_conclusion
    
    def set_result(self, result: str, tokens_sent: int, tokens_received: int, 
                   routing_conclusion: Optional[str] = None) -> None:
        """Set the processing result."""
        self.result = result
        self.tokens_sent = tokens_sent
        self.tokens_received = tokens_received
        self.routing_conclusion = routing_conclusion
    
    def render_live(self) -> Dict[str, Any]:
        """Render in live/processing state."""
        return {
            "id": self.id,
            "type": self.metadata.type,
            "state": self.metadata.state,
            "title": self.content.title,
            "body": self.methodology,
            "style": "processing",
            "show_spinner": True,
            "tokens_sent": self.tokens_sent,
            "tokens_received": self.tokens_received
        }
    
    def render_inscribed(self) -> Dict[str, Any]:
        """Render in completed state."""
        render_data = {
            "id": self.id,
            "type": self.metadata.type,
            "state": self.metadata.state,
            "title": self.content.title,
            "body": self.methodology,
            "style": "processing_complete",
            "duration": self.duration,
            "tokens_sent": self.tokens_sent,
            "tokens_received": self.tokens_received
        }
        if self.routing_conclusion:
            render_data["routing_conclusion"] = self.routing_conclusion
        return render_data


class InternalProcessingBlock(Block):
    """
    Container for the entire internal processing pipeline.
    Maintains proper parent-child relationships with sub-blocks.
    """
    
    def __init__(self):
        super().__init__(BlockType.INTERNAL_PROCESSING, "⚙️ Internal Processing")
        self.sub_blocks: List[ProcessingSubBlock] = []
        self.current_sub_block_index: int = -1
    
    def add_sub_block(self, sub_block: ProcessingSubBlock) -> None:
        """Add a sub-block to the processing pipeline."""
        self.sub_blocks.append(sub_block)
        self.add_child(sub_block)
    
    def _on_start(self) -> None:
        """Start the processing pipeline."""
        self.content.metadata["status"] = "running"
        self.content.body = "Processing..."
    
    def _on_complete(self) -> None:
        """Complete the processing pipeline."""
        self.content.metadata["status"] = "complete"
        total_duration = self.duration or 0
        self.content.metadata["total_duration"] = f"{total_duration:.1f}s"
    
    def start_sub_block(self, index: int) -> ProcessingSubBlock:
        """Start a specific sub-block."""
        if index >= len(self.sub_blocks):
            raise ValueError(f"Invalid sub-block index: {index}")
        
        self.current_sub_block_index = index
        sub_block = self.sub_blocks[index]
        sub_block.start()
        return sub_block
    
    def complete_sub_block(self, index: int) -> None:
        """Complete a specific sub-block."""
        if index >= len(self.sub_blocks):
            raise ValueError(f"Invalid sub-block index: {index}")
        
        self.sub_blocks[index].complete()
    
    def get_total_tokens(self) -> Dict[str, int]:
        """Get total token counts from all sub-blocks."""
        total_sent = sum(sb.tokens_sent for sb in self.sub_blocks)
        total_received = sum(sb.tokens_received for sb in self.sub_blocks)
        return {"sent": total_sent, "received": total_received}
    
    def render_live(self) -> Dict[str, Any]:
        """Render the processing container in live state."""
        return {
            "id": self.id,
            "type": self.metadata.type,
            "state": self.metadata.state,
            "title": f"{self.content.title} (running...)",
            "body": "Processing...",
            "style": "internal_processing",
            "sub_blocks": [sb.render() for sb in self.sub_blocks],
            "current_index": self.current_sub_block_index
        }
    
    def render_inscribed(self) -> Dict[str, Any]:
        """Render the processing container in inscribed state."""
        total_duration = self.duration or 0
        return {
            "id": self.id,
            "type": self.metadata.type,
            "state": self.metadata.state,
            "title": f"{self.content.title} ({total_duration:.1f}s total)",
            "style": "internal_processing_complete",
            "sub_blocks": [sb.render() for sb in self.sub_blocks],
            "total_tokens": self.get_total_tokens(),
            "show_connections": True
        }