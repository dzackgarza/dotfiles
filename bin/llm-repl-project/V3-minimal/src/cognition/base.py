"""Base Cognition Module Interface

Hot-swappable plugin architecture for cognition modules.
All cognition logic must be contained within the module.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Callable, Awaitable
from dataclasses import dataclass


@dataclass
class CognitionEvent:
    """Event emitted during cognition processing"""

    type: str  # 'start', 'update', 'complete', 'error'
    content: str
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class CognitionResult:
    """Result of cognition processing to be inscribed in timeline"""

    role: str = "cognition"
    content: str = ""
    sub_blocks: Optional[list] = None
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.sub_blocks is None:
            self.sub_blocks = []
        if self.metadata is None:
            self.metadata = {}


class CognitionModule(ABC):
    """Base interface for all cognition modules"""

    def __init__(self):
        self.staging_callback: Optional[Callable[[CognitionEvent], Awaitable[None]]] = (
            None
        )
        self.timeline_callback: Optional[
            Callable[[CognitionResult], Awaitable[None]]
        ] = None

    def set_staging_callback(
        self, callback: Callable[[CognitionEvent], Awaitable[None]]
    ):
        """Set callback for staging area updates"""
        self.staging_callback = callback

    def set_timeline_callback(
        self, callback: Callable[[CognitionResult], Awaitable[None]]
    ):
        """Set callback for timeline inscription"""
        self.timeline_callback = callback

    async def emit_staging_event(self, event: CognitionEvent):
        """Emit event to staging area"""
        if self.staging_callback:
            await self.staging_callback(event)

    async def inscribe_to_timeline(self, result: CognitionResult):
        """Inscribe result to timeline"""
        if self.timeline_callback:
            await self.timeline_callback(result)

    @abstractmethod
    async def process(
        self, query: str, context: Optional[Dict[str, Any]] = None
    ) -> CognitionResult:
        """Process user query through cognition

        Args:
            query: User's input query
            context: Optional context (previous turns, etc.)

        Returns:
            CognitionResult to be inscribed in timeline
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Get module name for display"""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Get module description"""
        pass
