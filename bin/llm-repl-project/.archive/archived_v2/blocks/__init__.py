"""Unified block system for LLM REPL."""

from .base import Block, BlockType, BlockState
from .user import UserBlock
from .system import SystemCheckBlock, WelcomeBlock
from .processing import InternalProcessingBlock, ProcessingSubBlock
from .assistant import AssistantBlock
from .registry import BlockRegistry, BlockSequence

__all__ = [
    'Block',
    'BlockType',
    'BlockState',
    'UserBlock',
    'SystemCheckBlock',
    'WelcomeBlock',
    'InternalProcessingBlock',
    'ProcessingSubBlock',
    'AssistantBlock',
    'BlockRegistry',
    'BlockSequence'
]