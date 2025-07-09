"""Base block definition with unified state management."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict
import uuid


class BlockType(str, Enum):
    """All possible block types in the system."""
    SYSTEM_CHECK = "system_check"
    WELCOME = "welcome"
    USER = "user"
    INTERNAL_PROCESSING = "internal_processing"
    PROCESSING_SUB = "processing_sub"
    ASSISTANT = "assistant"
    ERROR = "error"


class BlockState(str, Enum):
    """Block lifecycle states."""
    CREATED = "created"
    LIVE = "live"
    INSCRIBED = "inscribed"


class BlockMetadata(BaseModel):
    """Metadata for a block."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: BlockType
    created_at: datetime = Field(default_factory=datetime.now)
    state: BlockState = BlockState.CREATED
    parent_id: Optional[str] = None
    children_ids: List[str] = Field(default_factory=list)
    
    model_config = ConfigDict(use_enum_values=True)


class BlockContent(BaseModel):
    """Content that can be displayed in a block."""
    title: str
    body: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    @field_validator('title')
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v


class Block(ABC):
    """
    Base class for all blocks. A block is an atomic unit of display that:
    1. Has a single, consistent state throughout its lifecycle
    2. Can transition from CREATED -> LIVE -> INSCRIBED
    3. Maintains its complete display information at all times
    4. Can be rendered consistently in any state
    """
    
    def __init__(self, block_type: BlockType, title: str, content: str = ""):
        self.metadata = BlockMetadata(type=block_type)
        self.content = BlockContent(title=title, body=content)
        self._start_time: Optional[float] = None
        self._end_time: Optional[float] = None
    
    @property
    def id(self) -> str:
        """Block's unique identifier."""
        return self.metadata.id
    
    @property
    def state(self) -> BlockState:
        """Current block state."""
        return self.metadata.state
    
    @property
    def duration(self) -> Optional[float]:
        """Duration in seconds if block has completed."""
        if self._start_time and self._end_time:
            return self._end_time - self._start_time
        return None
    
    def start(self) -> None:
        """Transition block to LIVE state."""
        if self.metadata.state != BlockState.CREATED:
            raise ValueError(f"Cannot start block in state {self.metadata.state}")
        self.metadata.state = BlockState.LIVE
        self._start_time = datetime.now().timestamp()
        self._on_start()
    
    def complete(self) -> None:
        """Transition block to INSCRIBED state."""
        if self.metadata.state != BlockState.LIVE:
            raise ValueError(f"Cannot complete block in state {self.metadata.state}")
        self.metadata.state = BlockState.INSCRIBED
        self._end_time = datetime.now().timestamp()
        self._on_complete()
    
    def add_child(self, child: 'Block') -> None:
        """Add a child block."""
        self.metadata.children_ids.append(child.id)
        child.metadata.parent_id = self.id
    
    @abstractmethod
    def _on_start(self) -> None:
        """Hook called when block starts."""
        pass
    
    @abstractmethod
    def _on_complete(self) -> None:
        """Hook called when block completes."""
        pass
    
    @abstractmethod
    def render_live(self) -> Dict[str, Any]:
        """Render block in LIVE state."""
        pass
    
    @abstractmethod
    def render_inscribed(self) -> Dict[str, Any]:
        """Render block in INSCRIBED state."""
        pass
    
    def render(self) -> Dict[str, Any]:
        """Render block based on current state."""
        if self.metadata.state == BlockState.CREATED:
            return self.render_created()
        elif self.metadata.state == BlockState.LIVE:
            return self.render_live()
        elif self.metadata.state == BlockState.INSCRIBED:
            return self.render_inscribed()
        else:
            raise ValueError(f"Unknown state: {self.metadata.state}")
    
    def render_created(self) -> Dict[str, Any]:
        """Default render for CREATED state."""
        return {
            "id": self.id,
            "type": self.metadata.type,
            "state": self.metadata.state,
            "title": self.content.title,
            "body": self.content.body,
            "created_at": self.metadata.created_at.isoformat()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert block to dictionary for serialization."""
        return {
            "metadata": self.metadata.dict(),
            "content": self.content.dict(),
            "duration": self.duration,
            "render": self.render()
        }