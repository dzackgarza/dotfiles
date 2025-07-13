"""
Enhanced Block Metadata and Data Structures

This module defines standardized metadata structures and enhanced data classes
for Sacred Timeline blocks, extending the existing LiveBlock/InscribedBlock system.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum
import uuid


@dataclass
class BlockMetadata:
    """Standardized metadata for all Sacred Timeline blocks
    
    This structure provides consistent metadata tracking across both
    live and inscribed blocks, enhancing the existing block system.
    """

    # Timing and performance
    wall_time_seconds: float = 0.0
    creation_timestamp: datetime = field(default_factory=datetime.now)
    inscription_timestamp: Optional[datetime] = None

    # Token usage tracking
    tokens_input: int = 0
    tokens_output: int = 0
    model_name: Optional[str] = None

    # Processing information
    processing_steps: List[str] = field(default_factory=list)
    completion_status: str = "pending"  # pending, completed, error, cancelled

    # Error handling
    error_info: Optional[Dict[str, Any]] = None
    retry_count: int = 0

    # User annotations and context
    user_annotations: List[str] = field(default_factory=list)
    importance_level: str = "normal"  # low, normal, high, critical
    tags: List[str] = field(default_factory=list)

    # Relationship tracking
    parent_block_id: Optional[str] = None
    related_block_ids: List[str] = field(default_factory=list)
    conversation_turn: int = 0

    # Processing context
    original_prompt: Optional[str] = None
    processing_context: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "wall_time_seconds": self.wall_time_seconds,
            "creation_timestamp": self.creation_timestamp.isoformat(),
            "inscription_timestamp": self.inscription_timestamp.isoformat() if self.inscription_timestamp else None,
            "tokens_input": self.tokens_input,
            "tokens_output": self.tokens_output,
            "model_name": self.model_name,
            "processing_steps": self.processing_steps,
            "completion_status": self.completion_status,
            "error_info": self.error_info,
            "retry_count": self.retry_count,
            "user_annotations": self.user_annotations,
            "importance_level": self.importance_level,
            "tags": self.tags,
            "parent_block_id": self.parent_block_id,
            "related_block_ids": self.related_block_ids,
            "conversation_turn": self.conversation_turn,
            "original_prompt": self.original_prompt,
            "processing_context": self.processing_context
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BlockMetadata":
        """Create from dictionary"""
        creation_timestamp = datetime.fromisoformat(data["creation_timestamp"])
        inscription_timestamp = None
        if data.get("inscription_timestamp"):
            inscription_timestamp = datetime.fromisoformat(data["inscription_timestamp"])

        return cls(
            wall_time_seconds=data.get("wall_time_seconds", 0.0),
            creation_timestamp=creation_timestamp,
            inscription_timestamp=inscription_timestamp,
            tokens_input=data.get("tokens_input", 0),
            tokens_output=data.get("tokens_output", 0),
            model_name=data.get("model_name"),
            processing_steps=data.get("processing_steps", []),
            completion_status=data.get("completion_status", "pending"),
            error_info=data.get("error_info"),
            retry_count=data.get("retry_count", 0),
            user_annotations=data.get("user_annotations", []),
            importance_level=data.get("importance_level", "normal"),
            tags=data.get("tags", []),
            parent_block_id=data.get("parent_block_id"),
            related_block_ids=data.get("related_block_ids", []),
            conversation_turn=data.get("conversation_turn", 0),
            original_prompt=data.get("original_prompt"),
            processing_context=data.get("processing_context", {})
        )


class BlockRole(Enum):
    """Standardized block roles for Sacred Timeline"""

    USER = "user"           # 👤 User input
    ASSISTANT = "assistant" # 🤖 AI responses
    COGNITION = "cognition" # 🧠 Thinking process
    TOOL = "tool"          # 🛠️ Tool execution
    SYSTEM = "system"      # ⚙️ System messages
    SUB_MODULE = "sub_module"  # └─ Sub-processing steps
    ERROR = "error"        # ❌ Error messages
    DEBUG = "debug"        # 🐛 Debug information


class ProcessingStage(Enum):
    """Stages of block processing lifecycle"""

    CREATED = "created"           # Block just created
    QUEUED = "queued"            # Waiting for processing
    PROCESSING = "processing"     # Currently being processed
    STREAMING = "streaming"       # Content streaming in
    COMPLETING = "completing"     # Finalizing content
    COMPLETED = "completed"       # Processing finished
    TRANSITIONING = "transitioning"  # Moving to inscribed state
    INSCRIBED = "inscribed"       # Permanently in timeline
    ERROR = "error"              # Processing failed
    CANCELLED = "cancelled"       # Processing cancelled


@dataclass
class CognitionStep:
    """Individual step in cognition processing
    
    Provides detailed tracking of each step in the AI thinking process.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    icon: str = "⚡"

    # Timing
    start_time: float = field(default_factory=lambda: datetime.now().timestamp())
    end_time: Optional[float] = None
    estimated_duration: Optional[float] = None

    # Token usage
    tokens_in: int = 0
    tokens_out: int = 0

    # Results
    result: Optional[str] = None
    error: Optional[str] = None
    status: ProcessingStage = ProcessingStage.CREATED

    # Progress tracking
    progress_percentage: float = 0.0
    substeps: List[str] = field(default_factory=list)

    @property
    def duration(self) -> Optional[float]:
        """Calculate step duration if completed"""
        if self.end_time:
            return self.end_time - self.start_time
        return None

    @property
    def is_completed(self) -> bool:
        """Check if step is completed"""
        return self.status in [ProcessingStage.COMPLETED, ProcessingStage.INSCRIBED]

    @property
    def is_error(self) -> bool:
        """Check if step has error"""
        return self.status == ProcessingStage.ERROR or self.error is not None

    def mark_completed(self, result: Optional[str] = None) -> None:
        """Mark step as completed"""
        self.end_time = datetime.now().timestamp()
        self.status = ProcessingStage.COMPLETED
        self.progress_percentage = 1.0
        if result:
            self.result = result

    def mark_error(self, error_message: str) -> None:
        """Mark step as failed with error"""
        self.end_time = datetime.now().timestamp()
        self.status = ProcessingStage.ERROR
        self.error = error_message

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "icon": self.icon,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "estimated_duration": self.estimated_duration,
            "tokens_in": self.tokens_in,
            "tokens_out": self.tokens_out,
            "result": self.result,
            "error": self.error,
            "status": self.status.value,
            "progress_percentage": self.progress_percentage,
            "substeps": self.substeps
        }


@dataclass
class EnhancedCognitionProgress:
    """Enhanced cognition progress tracking with detailed step information
    
    Extends the existing CognitionProgress with more detailed tracking.
    """

    # Basic progress info
    start_time: float = field(default_factory=lambda: datetime.now().timestamp())
    total_steps: int = 0
    completed_steps: int = 0

    # Detailed step tracking
    steps: List[CognitionStep] = field(default_factory=list)
    current_step_index: int = -1

    # Overall status
    overall_status: ProcessingStage = ProcessingStage.CREATED
    estimated_total_time: Optional[float] = None

    # Aggregated metrics
    total_tokens_input: int = 0
    total_tokens_output: int = 0

    @property
    def current_step(self) -> Optional[CognitionStep]:
        """Get currently active step"""
        if 0 <= self.current_step_index < len(self.steps):
            return self.steps[self.current_step_index]
        return None

    @property
    def elapsed_time(self) -> float:
        """Total elapsed time"""
        return datetime.now().timestamp() - self.start_time

    @property
    def progress_percentage(self) -> float:
        """Overall progress percentage"""
        if self.total_steps == 0:
            return 0.0
        return min(1.0, self.completed_steps / self.total_steps)

    @property
    def estimated_remaining_time(self) -> Optional[float]:
        """Estimate remaining time based on progress"""
        if self.progress_percentage > 0 and self.estimated_total_time:
            return self.estimated_total_time * (1.0 - self.progress_percentage)
        return None

    def add_step(self, step: CognitionStep) -> None:
        """Add a new cognition step"""
        self.steps.append(step)
        self.total_steps = len(self.steps)

    def start_next_step(self) -> Optional[CognitionStep]:
        """Move to next step and start it"""
        if self.current_step:
            # Complete current step if not already completed
            if not self.current_step.is_completed:
                self.current_step.mark_completed()
                self.completed_steps += 1

        # Move to next step
        self.current_step_index += 1
        if self.current_step_index < len(self.steps):
            current = self.current_step
            if current:
                current.status = ProcessingStage.PROCESSING
                current.start_time = datetime.now().timestamp()
            return current

        return None

    def complete_current_step(self, result: Optional[str] = None, tokens_in: int = 0, tokens_out: int = 0) -> None:
        """Complete the current step"""
        if self.current_step and not self.current_step.is_completed:
            self.current_step.mark_completed(result)
            self.current_step.tokens_in += tokens_in
            self.current_step.tokens_out += tokens_out
            self.completed_steps += 1

            # Update aggregated metrics
            self.total_tokens_input += tokens_in
            self.total_tokens_output += tokens_out

    def get_status_summary(self) -> str:
        """Get human-readable status summary"""
        if self.current_step:
            step_info = f"{self.current_step.icon} {self.current_step.name}"
        else:
            step_info = "🎯 Starting..."

        progress_bar = "█" * int(self.progress_percentage * 20) + "░" * (20 - int(self.progress_percentage * 20))
        percentage = int(self.progress_percentage * 100)

        return f"{step_info}\n[{progress_bar}] {percentage}% | ⏱️ {self.elapsed_time:.1f}s | 🔢 {self.total_tokens_input}↑/{self.total_tokens_output}↓"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "start_time": self.start_time,
            "total_steps": self.total_steps,
            "completed_steps": self.completed_steps,
            "steps": [step.to_dict() for step in self.steps],
            "current_step_index": self.current_step_index,
            "overall_status": self.overall_status.value,
            "estimated_total_time": self.estimated_total_time,
            "total_tokens_input": self.total_tokens_input,
            "total_tokens_output": self.total_tokens_output
        }


@dataclass
class BlockValidationResult:
    """Result of block data structure validation"""

    is_valid: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def add_error(self, message: str) -> None:
        """Add validation error"""
        self.errors.append(message)
        self.is_valid = False

    def add_warning(self, message: str) -> None:
        """Add validation warning"""
        self.warnings.append(message)


class BlockDataValidator:
    """Validates block data structures for integrity and consistency"""

    @staticmethod
    def validate_live_block_data(block_data: Dict[str, Any]) -> BlockValidationResult:
        """Validate live block data structure"""
        result = BlockValidationResult()

        # Required fields
        required_fields = ["content", "tokens_input", "tokens_output", "wall_time_seconds", "progress"]
        for field in required_fields:
            if field not in block_data:
                result.add_error(f"Missing required field: {field}")

        # Type validation
        if "tokens_input" in block_data and not isinstance(block_data["tokens_input"], int):
            result.add_error("tokens_input must be integer")

        if "tokens_output" in block_data and not isinstance(block_data["tokens_output"], int):
            result.add_error("tokens_output must be integer")

        if "progress" in block_data:
            progress = block_data["progress"]
            if not isinstance(progress, (int, float)) or not (0.0 <= progress <= 1.0):
                result.add_error("progress must be float between 0.0 and 1.0")

        # Business logic validation (with type safety)
        try:
            tokens_input = block_data.get("tokens_input", 0)
            if isinstance(tokens_input, (int, float)) and tokens_input < 0:
                result.add_error("tokens_input cannot be negative")
        except (TypeError, ValueError):
            pass  # Type error already caught above

        try:
            tokens_output = block_data.get("tokens_output", 0)
            if isinstance(tokens_output, (int, float)) and tokens_output < 0:
                result.add_error("tokens_output cannot be negative")
        except (TypeError, ValueError):
            pass  # Type error already caught above

        try:
            wall_time = block_data.get("wall_time_seconds", 0)
            if isinstance(wall_time, (int, float)) and wall_time < 0:
                result.add_error("wall_time_seconds cannot be negative")
        except (TypeError, ValueError):
            pass  # Type error already caught above

        return result

    @staticmethod
    def validate_inscribed_block_data(block_data: Dict[str, Any]) -> BlockValidationResult:
        """Validate inscribed block data structure"""
        result = BlockValidationResult()

        # Required fields
        required_fields = ["id", "role", "content", "timestamp"]
        for field in required_fields:
            if field not in block_data:
                result.add_error(f"Missing required field: {field}")

        # Role validation
        if "role" in block_data:
            try:
                BlockRole(block_data["role"])
            except ValueError:
                result.add_warning(f"Unknown block role: {block_data['role']}")

        # Timestamp validation
        if "timestamp" in block_data:
            try:
                if isinstance(block_data["timestamp"], str):
                    datetime.fromisoformat(block_data["timestamp"])
            except ValueError:
                result.add_error("Invalid timestamp format")

        return result

    @staticmethod
    def validate_metadata(metadata: Dict[str, Any]) -> BlockValidationResult:
        """Validate block metadata structure"""
        result = BlockValidationResult()

        # Token validation
        for token_field in ["tokens_input", "tokens_output"]:
            if token_field in metadata:
                value = metadata[token_field]
                if not isinstance(value, int) or value < 0:
                    result.add_error(f"{token_field} must be non-negative integer")

        # Status validation
        if "completion_status" in metadata:
            valid_statuses = ["pending", "completed", "error", "cancelled"]
            if metadata["completion_status"] not in valid_statuses:
                result.add_warning(f"Unknown completion status: {metadata['completion_status']}")

        return result
