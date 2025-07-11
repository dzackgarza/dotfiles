"""Enhanced timeline block widget with sub-blocks support and elegant typography."""

from typing import Optional, Dict, List, Any
from datetime import datetime

from textual.widgets import Static
from textual.reactive import reactive
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich.console import RenderableType

from elia_chat.typography import ElegantTypography, SubBlockManager


class TimelineBlock(Static):
    """Enhanced timeline block with elegant typography and sub-blocks support."""
    
    DEFAULT_CSS = """
    TimelineBlock {
        height: auto;
        margin: 1 0;
        padding: 1;
    }
    
    .timeline-block {
        padding: 1;
        margin-bottom: 1;
        border-left: thick;
    }
    
    .timeline-block.user {
        border-left-color: $success;
    }
    
    .timeline-block.assistant {
        border-left-color: $primary;
    }
    
    .timeline-block.system {
        border-left-color: $secondary;
    }
    
    .timeline-block.error {
        border-left-color: $error;
    }
    
    .timeline-block.processing {
        border-left-color: $accent;
    }
    
    .timeline-block.warning {
        border-left-color: $warning;
    }
    
    .timeline-block.cognition {
        border-left-color: $primary;
    }
    
    .timeline-block.tool {
        border-left-color: $accent;
    }
    """
    
    # Reactive properties
    block_type: reactive[str] = reactive("assistant")
    title: reactive[str] = reactive("")
    content: reactive[str] = reactive("")
    timestamp: reactive[Optional[datetime]] = reactive(None)
    is_processing: reactive[bool] = reactive(False)
    
    def __init__(
        self,
        block_type: str = "assistant",
        title: str = "",
        content: str = "",
        timestamp: Optional[datetime] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.block_type = block_type
        self.title = title
        self.content = content
        self.timestamp = timestamp or datetime.now()
        self.sub_block_manager = SubBlockManager()
        self.block_id = f"{block_type}_{id(self)}"
        
        # Add CSS class for block type
        self.add_class(f"timeline-block")
        self.add_class(block_type)
    
    def add_sub_block(self, sub_type: str, content: str) -> str:
        """Add a sub-block to this main block."""
        return self.sub_block_manager.add_sub_block(self.block_id, sub_type, content)
    
    def update_content(self, new_content: str, append: bool = False):
        """Update the block content."""
        if append:
            self.content = f"{self.content}\n{new_content}" if self.content else new_content
        else:
            self.content = new_content
        self.refresh()
    
    def set_processing(self, processing: bool):
        """Set processing state for animated blocks."""
        self.is_processing = processing
        if processing:
            self.add_class("processing")
        else:
            self.remove_class("processing")
    
    def render(self) -> RenderableType:
        """Render the timeline block with elegant typography."""
        # Get theme color for this block type
        theme_color = ElegantTypography.get_theme_colors_for_block(self.block_type)
        
        # Create header with elegant typography
        header_text = ElegantTypography.get_block_header(
            self.block_type,
            self.title,
            ElegantTypography.format_timestamp(self.timestamp)
        )
        
        # Create header with appropriate styling
        header = Text(header_text, style=f"bold")
        
        # Create content
        content_lines = []
        if self.content:
            content_lines.append(Text(self.content))
        
        # Add sub-blocks if any
        sub_blocks = self.sub_block_manager.get_sub_blocks(self.block_id)
        for sub_block in sub_blocks:
            sub_header = ElegantTypography.get_sub_block_header(
                sub_block["type"],
                sub_block["content"]
            )
            content_lines.append(Text(f"  {sub_header}", style="dim"))
        
        # Combine all content
        if content_lines:
            content = Text.assemble(*[line for line in content_lines])
        else:
            content = Text("")
        
        # Create the final renderable
        if header_text and content:
            return Text.assemble(header, "\n", content)
        elif header_text:
            return header
        else:
            return content


class TimelineContainer(Static):
    """Container for timeline blocks with progressive mounting."""
    
    DEFAULT_CSS = """
    TimelineContainer {
        height: auto;
        padding: 1;
        scrollbar-gutter: stable;
    }
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.blocks: List[TimelineBlock] = []
    
    def add_block(
        self,
        block_type: str,
        title: str = "",
        content: str = "",
        timestamp: Optional[datetime] = None
    ) -> TimelineBlock:
        """Add a new timeline block with progressive mounting."""
        block = TimelineBlock(
            block_type=block_type,
            title=title,
            content=content,
            timestamp=timestamp
        )
        
        # Add mounting animation class
        block.add_class("mounting")
        
        # Mount the block
        self.mount(block)
        self.blocks.append(block)
        
        # Remove mounting class after a brief delay for animation
        self.call_later(0.3, lambda: block.remove_class("mounting"))
        
        return block
    
    def get_last_block(self) -> Optional[TimelineBlock]:
        """Get the most recently added block."""
        return self.blocks[-1] if self.blocks else None
    
    def update_last_block(self, content: str, append: bool = True):
        """Update the content of the last block."""
        if self.blocks:
            self.blocks[-1].update_content(content, append)


class BlockFactory:
    """Factory for creating different types of timeline blocks."""
    
    @staticmethod
    def create_user_block(content: str, timestamp: Optional[datetime] = None) -> TimelineBlock:
        """Create a user input block."""
        return TimelineBlock(
            block_type="user",
            title="",
            content=content,
            timestamp=timestamp
        )
    
    @staticmethod
    def create_assistant_block(content: str = "", timestamp: Optional[datetime] = None) -> TimelineBlock:
        """Create an assistant response block."""
        return TimelineBlock(
            block_type="assistant",
            title="",
            content=content,
            timestamp=timestamp
        )
    
    @staticmethod
    def create_system_block(title: str, content: str = "", timestamp: Optional[datetime] = None) -> TimelineBlock:
        """Create a system message block."""
        return TimelineBlock(
            block_type="system",
            title=title,
            content=content,
            timestamp=timestamp
        )
    
    @staticmethod
    def create_error_block(error_msg: str, timestamp: Optional[datetime] = None) -> TimelineBlock:
        """Create an error block."""
        return TimelineBlock(
            block_type="error",
            title="",
            content=error_msg,
            timestamp=timestamp
        )
    
    @staticmethod
    def create_cognition_block(title: str, timestamp: Optional[datetime] = None) -> TimelineBlock:
        """Create a cognition pipeline block."""
        block = TimelineBlock(
            block_type="cognition",
            title=title,
            content="",
            timestamp=timestamp
        )
        block.set_processing(True)
        return block
    
    @staticmethod
    def create_tool_block(tool_name: str, content: str = "", timestamp: Optional[datetime] = None) -> TimelineBlock:
        """Create a tool execution block."""
        return TimelineBlock(
            block_type="tool",
            title=f"executing {tool_name}",
            content=content,
            timestamp=timestamp
        )