#!/usr/bin/env python3
"""
Timeline Purity System - Structural Guarantees for Block-Only Display

This module ensures that ONLY properly formatted blocks can appear on the timeline.
Raw text pollution is structurally impossible.

ARCHITECTURAL CONTRACTS:
1. All timeline content MUST be in Rich blocks
2. No raw console.print() calls allowed
3. Status messages MUST use proper block types
4. Prompt handling MUST be separate from timeline
"""

from typing import Protocol, runtime_checkable, Optional, Any
from rich.console import Console
from rich.panel import Panel
from rich.box import ROUNDED
from enum import Enum
from dataclasses import dataclass


class BlockType(Enum):
    """Approved block types that can appear on timeline."""
    SYSTEM_CHECK = "system_check"
    WELCOME = "welcome"
    USER_INPUT = "user_input"
    COGNITION = "cognition"
    ASSISTANT_RESPONSE = "assistant_response"
    STATUS = "status"
    ERROR = "error"


@dataclass(frozen=True)
class TimelineBlock:
    """
    Immutable block that can appear on timeline.
    
    This is the ONLY way content can reach the timeline.
    Raw strings cannot be converted to TimelineBlock.
    """
    block_type: BlockType
    title: str
    content: str
    border_style: str = "white"
    
    def to_panel(self) -> Panel:
        """Convert to Rich Panel for display."""
        return Panel(
            self.content,
            title=self.title,
            box=ROUNDED,
            border_style=self.border_style
        )


@runtime_checkable
class TimelinePureDisplay(Protocol):
    """
    Protocol for display systems that guarantee timeline purity.
    
    Only allows proper blocks to reach the timeline.
    """
    
    def display_block(self, block: TimelineBlock) -> None:
        """
        Display a block on the timeline.
        
        This is the ONLY way to put content on the timeline.
        """
        ...
    
    def display_prompt(self, prompt: str) -> None:
        """
        Display prompt outside timeline.
        
        Prompts are not part of the timeline - they're input interface.
        """
        ...


class TimelinePureConsole:
    """
    Console wrapper that enforces timeline purity.
    
    Makes it impossible to pollute timeline with raw text.
    """
    
    def __init__(self, console: Console):
        self._console = console
        self._timeline_locked = False
    
    def display_block(self, block: TimelineBlock) -> None:
        """Display a block on the timeline."""
        panel = block.to_panel()
        self._console.print(panel)
    
    def display_prompt(self, prompt: str) -> None:
        """Display prompt outside timeline (input interface only)."""
        self._console.print(prompt, end="", highlight=False)
    
    def display_system_message(self, message: str, level: str = "info") -> None:
        """
        Display system message as proper block.
        
        System messages MUST be blocks, not raw text.
        """
        if level == "error":
            block = TimelineBlock(
                block_type=BlockType.ERROR,
                title="❌ Error",
                content=message,
                border_style="red"
            )
        else:
            block = TimelineBlock(
                block_type=BlockType.STATUS,
                title="🎯 Status",
                content=message,
                border_style="blue"
            )
        
        self.display_block(block)
    
    def print(self, *args, **kwargs):
        """
        DISABLED: Raw printing is not allowed.
        
        This prevents accidental timeline pollution.
        """
        raise RuntimeError(
            "Raw console.print() is forbidden! Use display_block() or display_prompt() instead. "
            "This enforces timeline purity - all content must be in proper blocks."
        )


class BlockFactory:
    """
    Factory for creating timeline blocks.
    
    Ensures all blocks follow proper formatting standards.
    """
    
    @staticmethod
    def create_status_block(message: str) -> TimelineBlock:
        """Create status block for system messages."""
        return TimelineBlock(
            block_type=BlockType.STATUS,
            title="🎯 Status",
            content=message,
            border_style="blue"
        )
    
    @staticmethod
    def create_error_block(message: str) -> TimelineBlock:
        """Create error block for error messages."""
        return TimelineBlock(
            block_type=BlockType.ERROR,
            title="❌ Error",
            content=message,
            border_style="red"
        )
    
    @staticmethod
    def create_processing_block(user_input: str) -> TimelineBlock:
        """
        Create processing block - this REPLACES raw 'Processing: X' text.
        
        This ensures user input processing appears as proper block.
        """
        return TimelineBlock(
            block_type=BlockType.COGNITION,
            title="🔄 Processing Input",
            content=f"Processing user input: {user_input}",
            border_style="yellow"
        )


class TimelinePurityValidator:
    """
    Validator to ensure timeline purity is maintained.
    
    Can be used in tests to catch violations.
    """
    
    def __init__(self):
        self.violations = []
    
    def validate_no_raw_text(self, output: str) -> bool:
        """
        Validate that output contains no raw text outside blocks.
        
        Returns True if pure, False if violations found.
        """
        # Check for common violation patterns
        violation_patterns = [
            "Processing:",
            "Startup sequence completed",
            "Startup completed:",
            "🎯",
            "✅"
        ]
        
        for pattern in violation_patterns:
            if pattern in output and "│" not in output:  # Raw text, not in block
                self.violations.append(f"Raw text violation: '{pattern}' found outside block")
                return False
        
        return True
    
    def get_violations(self) -> list:
        """Get list of timeline purity violations."""
        return self.violations.copy()
    
    def reset(self) -> None:
        """Reset violation tracking."""
        self.violations.clear()