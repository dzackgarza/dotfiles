"""
Timeline Blocks - Core Data Structures

Extracted from V2's working implementation and cleaned up.
These are the fundamental building blocks of the timeline.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any
import uuid
import time


class BlockType(Enum):
    """Types of blocks in the timeline."""
    SYSTEM_CHECK = "system_check"
    WELCOME = "welcome"
    USER_INPUT = "user_input"
    COGNITION = "cognition"
    ASSISTANT_RESPONSE = "assistant_response"
    ERROR = "error"


@dataclass
class TimelineBlock:
    """
    A block in the timeline.
    
    This is the core data structure that represents each step
    in the conversation flow. Extracted from V2's working implementation.
    """
    id: str
    type: BlockType
    title: str
    content: str
    timestamp: float
    tokens: Dict[str, int]
    metadata: Dict[str, Any]
    
    @classmethod
    def create(cls, block_type: BlockType, title: str, content: str, 
               tokens: Dict[str, int] = None, metadata: Dict[str, Any] = None) -> 'TimelineBlock':
        """Create a new timeline block with auto-generated ID and timestamp."""
        return cls(
            id=str(uuid.uuid4()),
            type=block_type,
            title=title,
            content=content,
            timestamp=time.time(),
            tokens=tokens or {"input": 0, "output": 0},
            metadata=metadata or {}
        )
    
    def get_duration_since_creation(self) -> float:
        """Get time elapsed since block creation."""
        return time.time() - self.timestamp
    
    def has_tokens(self) -> bool:
        """Check if block has any token usage."""
        return self.tokens.get("input", 0) > 0 or self.tokens.get("output", 0) > 0
    
    def get_token_summary(self) -> str:
        """Get formatted token summary."""
        if self.has_tokens():
            return f"[↑{self.tokens['input']} ↓{self.tokens['output']}]"
        return ""
    
    def get_formatted_header(self) -> str:
        """Get formatted header for display."""
        header = f"🔧 {self.title}"
        
        if self.has_tokens():
            header += f" {self.get_token_summary()}"
        
        duration = self.get_duration_since_creation()
        header += f" ({duration:.1f}s)"
        
        return header


def create_system_check_block(config_name: str) -> TimelineBlock:
    """Create a system check block."""
    content = """✅ Configuration:       System ready
✅ Dependencies:        All dependencies available

LLM Providers:
    ✅ mock            mock-model              0.1s  ↑  0 ↓  0"""
    
    return TimelineBlock.create(
        BlockType.SYSTEM_CHECK,
        "System_Check ✅",
        content,
        metadata={"source": "startup", "config": config_name}
    )


def create_welcome_block(config_name: str) -> TimelineBlock:
    """Create a welcome block."""
    content = f"""Welcome to LLM REPL V3 - Modern Interface!

Configuration: {config_name}
Architecture: Block-based timeline with cognitive processing

💡 Features:
• Modern, clean interface
• Multiline expanding input box
• Separate timeline and input areas
• Block-based display (preserves your architecture)
• Cognitive processing with transparency
• Token tracking and timing

🔧 Usage:
• Type your message in the input box below
• Press Enter to send (Shift+Enter for new line)
• Watch your query flow through cognitive blocks
• All interactions are preserved in the timeline

Ready for your queries!"""
    
    return TimelineBlock.create(
        BlockType.WELCOME,
        "Welcome ✅",
        content,
        metadata={"source": "startup", "config": config_name}
    )


def create_user_input_block(user_input: str) -> TimelineBlock:
    """Create a user input block."""
    return TimelineBlock.create(
        BlockType.USER_INPUT,
        "User_Input ✅",
        f"> {user_input}",
        metadata={"source": "user", "input_length": len(user_input)}
    )


def create_cognition_block(transparency_log: list, total_tokens: Dict[str, int], 
                          processing_duration: float) -> TimelineBlock:
    """Create a cognition block."""
    content = f"Completed processing through {len(transparency_log)} cognitive modules:\n\n"
    for log in transparency_log:
        content += f"Step {log['step']}: {log['name']} - {log['status']}\n"
    
    content += f"\nProcessing Duration: {processing_duration:.1f}s"
    
    return TimelineBlock.create(
        BlockType.COGNITION,
        "Cognition ✅",
        content,
        tokens=total_tokens,
        metadata={"transparency_log": transparency_log, "duration": processing_duration}
    )


def create_assistant_response_block(response: str, total_tokens: Dict[str, int], 
                                   processing_results: Dict[str, Any]) -> TimelineBlock:
    """Create an assistant response block."""
    return TimelineBlock.create(
        BlockType.ASSISTANT_RESPONSE,
        "Assistant_Response ✅",
        response,
        tokens=total_tokens,
        metadata={"processing_results": processing_results}
    )


def create_error_block(error_message: str) -> TimelineBlock:
    """Create an error block."""
    return TimelineBlock.create(
        BlockType.ERROR,
        "Error ❌",
        f"Error processing request: {error_message}",
        metadata={"error": error_message}
    )