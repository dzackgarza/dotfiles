"""
Wall Time and Token Usage Tracker

Implements Task 11.3: Track wall time and token usage for each block with 
millisecond precision for concurrent operations without interference.
"""

import time
import threading
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional, List, Any
from contextlib import contextmanager
from .block_metadata import BlockMetadata, ProcessingStage


@dataclass
class WallTimeRecord:
    """Records wall time for a specific operation"""
    start_time: float
    end_time: Optional[float] = None
    stage: str = "unknown"
    
    @property
    def duration_ms(self) -> Optional[float]:
        """Get duration in milliseconds"""
        if self.end_time is None:
            return None
        return (self.end_time - self.start_time) * 1000
    
    @property
    def is_complete(self) -> bool:
        """Check if timing is complete"""
        return self.end_time is not None


@dataclass 
class TokenUsageRecord:
    """Records token usage for a specific operation"""
    input_tokens: int = 0
    output_tokens: int = 0
    model_name: str = "unknown"
    cost_estimate: Optional[float] = None
    
    @property
    def total_tokens(self) -> int:
        """Total tokens consumed"""
        return self.input_tokens + self.output_tokens


@dataclass
class BlockPerformanceMetrics:
    """Complete performance metrics for a block"""
    block_id: str
    
    # Wall time tracking
    total_wall_time: WallTimeRecord = field(default_factory=lambda: WallTimeRecord(time.time()))
    stage_timings: Dict[str, WallTimeRecord] = field(default_factory=dict)
    
    # Token usage tracking  
    token_usage: TokenUsageRecord = field(default_factory=TokenUsageRecord)
    
    # Processing breakdown
    creation_time_ms: float = 0.0
    processing_time_ms: float = 0.0
    completion_time_ms: float = 0.0
    inscription_time_ms: float = 0.0
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    
    def start_stage(self, stage: str) -> None:
        """Start timing a processing stage"""
        self.stage_timings[stage] = WallTimeRecord(time.time(), stage=stage)
    
    def end_stage(self, stage: str) -> Optional[float]:
        """End timing a processing stage, returns duration in ms"""
        if stage in self.stage_timings:
            self.stage_timings[stage].end_time = time.time()
            return self.stage_timings[stage].duration_ms
        return None
    
    def complete_block(self) -> None:
        """Mark block as completed and finalize timing"""
        self.total_wall_time.end_time = time.time()
        self.completed_at = datetime.now()
    
    def add_tokens(self, input_tokens: int, output_tokens: int, model: str = "unknown") -> None:
        """Add token usage to the record"""
        self.token_usage.input_tokens += input_tokens
        self.token_usage.output_tokens += output_tokens
        if model != "unknown":
            self.token_usage.model_name = model
    
    def get_breakdown_summary(self) -> Dict[str, float]:
        """Get processing time breakdown in milliseconds"""
        return {
            stage: record.duration_ms or 0.0 
            for stage, record in self.stage_timings.items()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API queries"""
        return {
            "block_id": self.block_id,
            "total_wall_time_ms": self.total_wall_time.duration_ms or 0.0,
            "stage_breakdown_ms": self.get_breakdown_summary(),
            "token_usage": {
                "input_tokens": self.token_usage.input_tokens,
                "output_tokens": self.token_usage.output_tokens,
                "total_tokens": self.token_usage.total_tokens,
                "model_name": self.token_usage.model_name,
                "cost_estimate": self.token_usage.cost_estimate
            },
            "timestamps": {
                "created_at": self.created_at.isoformat(),
                "completed_at": self.completed_at.isoformat() if self.completed_at else None
            },
            "processing_times_ms": {
                "creation": self.creation_time_ms,
                "processing": self.processing_time_ms,
                "completion": self.completion_time_ms,
                "inscription": self.inscription_time_ms
            }
        }


class WallTimeTracker:
    """
    Thread-safe tracker for wall time and token usage per block.
    
    Implements Task 11.3 requirements:
    - Millisecond precision wall time tracking
    - Token usage per block 
    - Processing time breakdown by stage
    - Cost estimates when available
    - Thread-safe for concurrent operations
    """
    
    def __init__(self):
        self._metrics: Dict[str, BlockPerformanceMetrics] = {}
        self._lock = threading.RLock()  # Reentrant lock for nested operations
        
    def start_block_tracking(self, block_id: str) -> BlockPerformanceMetrics:
        """Start tracking a new block"""
        with self._lock:
            if block_id in self._metrics:
                return self._metrics[block_id]
            
            metrics = BlockPerformanceMetrics(block_id=block_id)
            self._metrics[block_id] = metrics
            return metrics
    
    def get_block_metrics(self, block_id: str) -> Optional[BlockPerformanceMetrics]:
        """Get metrics for a specific block"""
        with self._lock:
            return self._metrics.get(block_id)
    
    def record_tokens(self, block_id: str, input_tokens: int, output_tokens: int, 
                     model: str = "unknown", cost: Optional[float] = None) -> None:
        """Record token usage for a block"""
        with self._lock:
            if block_id not in self._metrics:
                self.start_block_tracking(block_id)
            
            metrics = self._metrics[block_id]
            metrics.add_tokens(input_tokens, output_tokens, model)
            if cost is not None:
                metrics.token_usage.cost_estimate = cost
    
    @contextmanager
    def time_stage(self, block_id: str, stage: str):
        """Context manager to time a processing stage"""
        with self._lock:
            if block_id not in self._metrics:
                self.start_block_tracking(block_id)
            
            metrics = self._metrics[block_id]
        
        # Start timing outside the lock to minimize lock time
        metrics.start_stage(stage)
        
        try:
            yield
        finally:
            # End timing and update breakdown
            duration_ms = metrics.end_stage(stage)
            
            with self._lock:
                # Update specific timing fields
                if stage == "creation":
                    metrics.creation_time_ms = duration_ms or 0.0
                elif stage == "processing":
                    metrics.processing_time_ms = duration_ms or 0.0
                elif stage == "completion":
                    metrics.completion_time_ms = duration_ms or 0.0
                elif stage == "inscription":
                    metrics.inscription_time_ms = duration_ms or 0.0
    
    def complete_block(self, block_id: str) -> Optional[Dict[str, Any]]:
        """Mark block as completed and return final metrics"""
        with self._lock:
            if block_id not in self._metrics:
                return None
            
            metrics = self._metrics[block_id]
            metrics.complete_block()
            return metrics.to_dict()
    
    def get_all_metrics(self) -> Dict[str, Dict[str, Any]]:
        """Get metrics for all tracked blocks"""
        with self._lock:
            return {
                block_id: metrics.to_dict() 
                for block_id, metrics in self._metrics.items()
            }
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics across all blocks"""
        with self._lock:
            if not self._metrics:
                return {"total_blocks": 0}
            
            completed_blocks = [m for m in self._metrics.values() if m.completed_at]
            
            if not completed_blocks:
                return {
                    "total_blocks": len(self._metrics),
                    "completed_blocks": 0
                }
            
            # Calculate averages for completed blocks
            avg_wall_time = sum(
                m.total_wall_time.duration_ms or 0.0 for m in completed_blocks
            ) / len(completed_blocks)
            
            total_input_tokens = sum(m.token_usage.input_tokens for m in completed_blocks)
            total_output_tokens = sum(m.token_usage.output_tokens for m in completed_blocks)
            
            avg_input_tokens = total_input_tokens / len(completed_blocks)
            avg_output_tokens = total_output_tokens / len(completed_blocks)
            
            return {
                "total_blocks": len(self._metrics),
                "completed_blocks": len(completed_blocks),
                "average_wall_time_ms": round(avg_wall_time, 2),
                "total_tokens": {
                    "input": total_input_tokens,
                    "output": total_output_tokens,
                    "total": total_input_tokens + total_output_tokens
                },
                "average_tokens_per_block": {
                    "input": round(avg_input_tokens, 1),
                    "output": round(avg_output_tokens, 1)
                }
            }
    
    def cleanup_old_metrics(self, max_age_hours: int = 24) -> int:
        """Clean up metrics older than specified hours, returns count removed"""
        cutoff_time = datetime.now().timestamp() - (max_age_hours * 3600)
        removed_count = 0
        
        with self._lock:
            to_remove = []
            for block_id, metrics in self._metrics.items():
                if metrics.created_at.timestamp() < cutoff_time:
                    to_remove.append(block_id)
            
            for block_id in to_remove:
                del self._metrics[block_id]
                removed_count += 1
        
        return removed_count


# Global tracker instance
_global_tracker: Optional[WallTimeTracker] = None
_tracker_lock = threading.Lock()


def get_wall_time_tracker() -> WallTimeTracker:
    """Get the global wall time tracker instance"""
    global _global_tracker
    
    if _global_tracker is None:
        with _tracker_lock:
            if _global_tracker is None:
                _global_tracker = WallTimeTracker()
    
    return _global_tracker


# Convenience functions for easy integration
def track_block_creation(block_id: str) -> BlockPerformanceMetrics:
    """Start tracking a new block"""
    return get_wall_time_tracker().start_block_tracking(block_id)


def record_block_tokens(block_id: str, input_tokens: int, output_tokens: int, 
                       model: str = "unknown", cost: Optional[float] = None) -> None:
    """Record token usage for a block"""
    get_wall_time_tracker().record_tokens(block_id, input_tokens, output_tokens, model, cost)


def time_block_stage(block_id: str, stage: str):
    """Context manager to time a block processing stage"""
    return get_wall_time_tracker().time_stage(block_id, stage)


def complete_block_tracking(block_id: str) -> Optional[Dict[str, Any]]:
    """Complete tracking for a block and return metrics"""
    return get_wall_time_tracker().complete_block(block_id)


def query_block_metrics(block_id: str) -> Optional[Dict[str, Any]]:
    """Query metrics for a specific block"""
    metrics = get_wall_time_tracker().get_block_metrics(block_id)
    return metrics.to_dict() if metrics else None


def query_all_metrics() -> Dict[str, Dict[str, Any]]:
    """Query metrics for all blocks"""
    return get_wall_time_tracker().get_all_metrics()


def get_performance_summary() -> Dict[str, Any]:
    """Get performance summary statistics"""
    return get_wall_time_tracker().get_summary_stats()