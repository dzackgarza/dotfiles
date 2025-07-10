"""Plugin system for LLM REPL blocks."""

from .base import BlockPlugin, PluginInterface, PluginMetadata, PluginRegistry
from .registry import PluginManager

__all__ = [
    'BlockPlugin',
    'PluginInterface', 
    'PluginMetadata',
    'PluginRegistry',
    'PluginManager'
]