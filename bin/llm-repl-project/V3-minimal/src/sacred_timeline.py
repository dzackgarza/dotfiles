"""Sacred Timeline - Immutable append-only log of all operations"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol
from uuid import uuid4
import json


@dataclass
class Block:
    """A single immutable block in the Sacred Timeline"""

    id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    role: str = ""  # "user", "system", "assistant", "cognition", "turn"
    content: str = ""
    metadata: dict = field(default_factory=dict)
    time_taken: float | None = None  # Time taken for this block in seconds
    tokens_input: int | None = None  # Number of input tokens
    tokens_output: int | None = None  # Number of output tokens

    def to_dict(self) -> dict:
        """Serialize block for storage"""
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "role": self.role,
            "content": self.content,
            "metadata": self.metadata,
            "time_taken": self.time_taken,
            "tokens_input": self.tokens_input,
            "tokens_output": self.tokens_output,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Block":
        """Deserialize block from storage"""
        return cls(
            id=data["id"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            role=data["role"],
            content=data.get("content", ""),
            metadata=data.get("metadata", {}),
            time_taken=data.get("time_taken"),
            tokens_input=data.get("tokens_input"),
            tokens_output=data.get("tokens_output"),
        )


class TimelineObserver(Protocol):
    """Observer for timeline changes"""

    def on_block_added(self, block: Block) -> None:
        """Called when a new block is added"""
        ...


class SacredTimeline:
    """
    The Sacred Timeline - append-only, immutable log of all operations.

    Core Principles:
    - Append-only: Blocks can only be added, never modified or deleted
    - Immutable: Once written, blocks cannot change
    - Observable: Changes trigger notifications to observers
    - Persistent: Timeline can be saved/loaded
    """

    def __init__(self):
        self._blocks: list[Block] = []
        self._observers: list[TimelineObserver] = []

    def add_block(
        self,
        role: str,
        content: str,
        metadata: dict | None = None,
        time_taken: float | None = None,
        tokens_input: int | None = None,
        tokens_output: int | None = None,
    ) -> Block:
        """Add a new block to the timeline"""
        block = Block(
            role=role,
            content=content,
            metadata=metadata or {},
            time_taken=time_taken,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
        )

        # Append-only: blocks can only be added
        self._blocks.append(block)

        # Notify observers
        for observer in self._observers:
            observer.on_block_added(block)

        return block

    def get_blocks(self) -> list[Block]:
        """Get all blocks (read-only copy)"""
        return self._blocks.copy()

    def get_blocks_by_role(self, role: str) -> list[Block]:
        """Get blocks filtered by role"""
        return [block for block in self._blocks if block.role == role]

    def add_observer(self, observer: TimelineObserver) -> None:
        """Add an observer for timeline changes"""
        self._observers.append(observer)

    def remove_observer(self, observer: TimelineObserver) -> None:
        """Remove an observer"""
        if observer in self._observers:
            self._observers.remove(observer)

    def save_to_file(self, filepath: str) -> None:
        """Save timeline to JSON file"""
        data = {
            "blocks": [block.to_dict() for block in self._blocks],
            "saved_at": datetime.now().isoformat(),
        }

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    def load_from_file(self, filepath: str) -> None:
        """Load timeline from JSON file"""
        with open(filepath) as f:
            data = json.load(f)

        # Clear current timeline and load blocks
        self._blocks = []
        for block_data in data.get("blocks", []):
            block = Block.from_dict(block_data)
            self._blocks.append(block)

            # Notify observers of loaded blocks
            for observer in self._observers:
                observer.on_block_added(block)

    def clear_timeline(self) -> None:
        """Clear all blocks from the timeline"""
        self._blocks = []

    def __len__(self) -> int:
        """Number of blocks in timeline"""
        return len(self._blocks)

    def __repr__(self) -> str:
        return f"SacredTimeline({len(self._blocks)} blocks)"


# Global timeline instance
timeline = SacredTimeline()
