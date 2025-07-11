"""Elegant typography system for block styling without capitals."""

from typing import Dict, Optional
from datetime import datetime


class ElegantTypography:
    """Refined typography system for blocks without capital letters."""
    
    BLOCK_TITLES = {
        "user": "user input",
        "assistant": "assistant response", 
        "system": "system message",
        "error": "error occurred",
        "processing": "processing",
        "warning": "warning",
        "cognition": "cognition pipeline",
        "tool": "tool execution",
        "subblock": "sub-process",
    }
    
    BLOCK_ICONS = {
        "user": "›",           # Simple chevron
        "assistant": "•",      # Bullet point
        "system": "⚙",         # Gear
        "error": "⚠",          # Warning triangle
        "processing": "⋯",     # Ellipsis
        "warning": "!",        # Exclamation
        "cognition": "◦",      # Small circle
        "tool": "▸",           # Right-pointing triangle
        "subblock": "‣",       # Triangular bullet
    }
    
    # Sub-block icons for nested content
    SUB_ICONS = {
        "step": "→",           # Arrow for process steps
        "detail": "◦",         # Small circle for details
        "info": "i",           # Information
        "progress": "⋯",       # Progress indicator
        "result": "✓",         # Checkmark for results
        "note": "※",           # Reference mark
    }
    
    @staticmethod
    def get_block_header(
        block_type: str, 
        title: Optional[str] = None,
        timestamp: Optional[str] = None,
        is_subblock: bool = False
    ) -> str:
        """Generate elegant block header without caps."""
        if is_subblock:
            icon = ElegantTypography.SUB_ICONS.get(block_type, "◦")
            display_title = title or block_type.replace("_", " ")
        else:
            icon = ElegantTypography.BLOCK_ICONS.get(block_type, "•")
            display_title = title or ElegantTypography.BLOCK_TITLES.get(block_type, block_type)
        
        if timestamp:
            return f"{icon} {display_title} • {timestamp}"
        else:
            return f"{icon} {display_title}"
    
    @staticmethod
    def get_sub_block_header(sub_type: str, content: str) -> str:
        """Generate header for sub-blocks within main blocks."""
        icon = ElegantTypography.SUB_ICONS.get(sub_type, "◦")
        return f"  {icon} {content}"
    
    @staticmethod
    def format_timestamp(dt: Optional[datetime] = None) -> str:
        """Format timestamp in elegant way."""
        if dt is None:
            dt = datetime.now()
        return dt.strftime("%H:%M:%S")
    
    @staticmethod
    def get_theme_colors_for_block(block_type: str) -> str:
        """Map block types to theme color properties."""
        color_mapping = {
            "user": "success",        # User input - green/positive
            "assistant": "primary",   # Assistant response - main theme color
            "system": "secondary",    # System messages - secondary theme color
            "error": "error",         # Error messages - error color
            "processing": "accent",   # Processing states - accent color
            "warning": "warning",     # Warning messages - warning color
            "cognition": "primary",   # Cognition pipeline - primary
            "tool": "accent",         # Tool execution - accent
            "subblock": "secondary",  # Sub-blocks - secondary
        }
        return color_mapping.get(block_type, "primary")


class BlockStyleConfig:
    """Configuration for block styling and sub-blocks."""
    
    # Main block configuration
    BLOCK_PADDING = "0.75rem"
    BLOCK_MARGIN = "1rem 0"
    BLOCK_BORDER_RADIUS = "0.5rem"
    BLOCK_BORDER_WIDTH = "3px"
    
    # Sub-block configuration
    SUB_BLOCK_PADDING = "0.5rem"
    SUB_BLOCK_MARGIN = "0.5rem 0"
    SUB_BLOCK_INDENT = "1.5rem"
    SUB_BLOCK_BORDER_WIDTH = "2px"
    
    # Typography configuration
    HEADER_FONT_SIZE = "0.875rem"
    HEADER_FONT_WEIGHT = "500"
    HEADER_OPACITY = "0.9"
    HEADER_LETTER_SPACING = "0.025em"
    
    CONTENT_FONT_SIZE = "0.9rem"
    CONTENT_LINE_HEIGHT = "1.5"
    
    SUB_HEADER_FONT_SIZE = "0.8rem"
    SUB_CONTENT_FONT_SIZE = "0.85rem"
    
    # Animation configuration
    TRANSITION_DURATION = "0.2s"
    TRANSITION_EASING = "ease"


class SubBlockManager:
    """Manages sub-blocks within main blocks."""
    
    def __init__(self):
        self.sub_blocks: Dict[str, list] = {}
    
    def add_sub_block(self, parent_id: str, sub_type: str, content: str) -> str:
        """Add a sub-block to a parent block."""
        if parent_id not in self.sub_blocks:
            self.sub_blocks[parent_id] = []
        
        sub_block = {
            "id": f"{parent_id}_sub_{len(self.sub_blocks[parent_id])}",
            "type": sub_type,
            "content": content,
            "timestamp": ElegantTypography.format_timestamp(),
        }
        
        self.sub_blocks[parent_id].append(sub_block)
        return sub_block["id"]
    
    def get_sub_blocks(self, parent_id: str) -> list:
        """Get all sub-blocks for a parent block."""
        return self.sub_blocks.get(parent_id, [])
    
    def format_sub_block_html(self, sub_block: dict) -> str:
        """Format sub-block as HTML with elegant styling."""
        header = ElegantTypography.get_sub_block_header(
            sub_block["type"], 
            sub_block["content"]
        )
        
        return f"""
        <div class="sub-block sub-block-{sub_block['type']}">
            <div class="sub-block-header">{header}</div>
            <div class="sub-block-timestamp">{sub_block['timestamp']}</div>
        </div>
        """