"""Base class for cognition sub-modules."""

import asyncio
from abc import ABC, abstractmethod
from typing import Optional, Callable

from ..live_blocks import LiveBlock, CognitionProgress


class SubModule(ABC):
    """Base class for all cognition sub-modules."""
    
    def __init__(self, live_block: LiveBlock):
        """Initialize sub-module with its live block."""
        self.live_block = live_block
        self.completion_callback: Optional[Callable] = None
        self._is_complete = False
        
    def set_completion_callback(self, callback: Callable) -> None:
        """Set callback to notify parent when complete."""
        self.completion_callback = callback
        
    @abstractmethod
    async def execute(self) -> None:
        """Execute the sub-module's task. Must be implemented by subclasses."""
        pass
        
    @abstractmethod
    def get_initial_content(self) -> str:
        """Get initial content for the live block."""
        pass
        
    async def _notify_completion(self) -> None:
        """Notify parent that this sub-module is complete."""
        self._is_complete = True
        if self.completion_callback:
            await self.completion_callback()
            
    @property
    def is_complete(self) -> bool:
        """Check if sub-module has completed execution."""
        return self._is_complete