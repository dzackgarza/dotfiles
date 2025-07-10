"""
LLM REPL V3 - Core Components

This module contains the core functionality extracted and refined from V2.
All the working logic is preserved while being better organized.
"""

from .blocks import (
    BlockType, TimelineBlock,
    create_system_check_block, create_welcome_block,
    create_user_input_block, create_cognition_block,
    create_assistant_response_block, create_error_block
)
from .cognition import CognitionProcessor
from .timeline import TimelineManager

__all__ = [
    'BlockType',
    'TimelineBlock',
    'create_system_check_block',
    'create_welcome_block', 
    'create_user_input_block',
    'create_cognition_block',
    'create_assistant_response_block',
    'create_error_block',
    'CognitionProcessor',
    'TimelineManager'
]