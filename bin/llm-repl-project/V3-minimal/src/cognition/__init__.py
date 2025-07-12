"""Cognition Module System

Hot-swappable plugin architecture for cognition processing.
"""

from .base import CognitionModule, CognitionEvent, CognitionResult
from .manager import CognitionManager
from .noop_module import NoOpCognitionModule
from .mock_module import MockCognitionModule

__all__ = [
    "CognitionModule",
    "CognitionEvent",
    "CognitionResult",
    "CognitionManager",
    "NoOpCognitionModule",
    "MockCognitionModule",
]
