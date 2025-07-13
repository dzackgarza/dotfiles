"""
Block Operation Audit Logger

Provides comprehensive transparency and auditing for all block operations.
Tracks every operation with timestamps, metadata, and error context.
"""

import json
import threading
import time
import traceback
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from uuid import uuid4


class OperationType(Enum):
    """Types of block operations that can be audited."""
    CREATION = "creation"
    MODIFICATION = "modification"
    STATE_TRANSITION = "state_transition"
    DELETION = "deletion"
    VALIDATION = "validation"
    ERROR = "error"
    PERFORMANCE = "performance"
    INTEGRITY_CHECK = "integrity_check"


class LogLevel(Enum):
    """Log severity levels."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class OperationMetadata:
    """Metadata for a block operation."""
    operation_id: str
    block_id: str
    operation_type: OperationType
    timestamp: str
    thread_id: int
    user_context: Optional[str] = None
    session_id: Optional[str] = None
    source_location: Optional[str] = None


@dataclass
class AuditLogEntry:
    """Complete audit log entry for a block operation."""
    metadata: OperationMetadata
    level: LogLevel
    message: str
    details: Dict[str, Any]
    error_context: Optional[Dict[str, Any]] = None
    performance_metrics: Optional[Dict[str, float]] = None
    data_snapshot: Optional[Dict[str, Any]] = None
    integrity_results: Optional[Dict[str, bool]] = None


class BlockAuditLogger:
    """
    Comprehensive audit logging system for block operations.
    
    Provides full transparency and traceability for all block-related operations
    with support for filtering, searching, and reconstruction of operation sequences.
    """
    
    def __init__(self, log_directory: Optional[Path] = None):
        self._log_directory = log_directory or Path("logs/block_audit")
        self._log_directory.mkdir(parents=True, exist_ok=True)
        
        self._entries: List[AuditLogEntry] = []
        self._lock = threading.RLock()
        self._session_id = str(uuid4())[:8]
        
        # Performance tracking
        self._operation_timings: Dict[str, float] = {}
        self._active_operations: Dict[str, float] = {}
        
        # Initialize log files
        self._current_log_file = self._log_directory / f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
        
    def start_operation(self, 
                       block_id: str, 
                       operation_type: OperationType,
                       user_context: Optional[str] = None,
                       **kwargs) -> str:
        """
        Start tracking a block operation.
        
        Returns:
            operation_id: Unique identifier for this operation
        """
        operation_id = str(uuid4())
        
        with self._lock:
            # Track start time for performance metrics
            self._active_operations[operation_id] = time.perf_counter()
            
            # Create metadata
            metadata = OperationMetadata(
                operation_id=operation_id,
                block_id=block_id,
                operation_type=operation_type,
                timestamp=datetime.now(timezone.utc).isoformat(),
                thread_id=threading.get_ident(),
                user_context=user_context,
                session_id=self._session_id,
                source_location=self._get_caller_location()
            )
            
            # Log operation start
            self._log_entry(
                metadata=metadata,
                level=LogLevel.INFO,
                message=f"Started {operation_type.value} operation for block {block_id}",
                details=kwargs
            )
            
        return operation_id
    
    def end_operation(self, 
                     operation_id: str, 
                     success: bool = True,
                     result_data: Optional[Dict[str, Any]] = None,
                     **kwargs):
        """End tracking a block operation and record final metrics."""
        with self._lock:
            if operation_id not in self._active_operations:
                self.log_error(
                    block_id="unknown",
                    operation_type=OperationType.ERROR,
                    message=f"Attempted to end unknown operation {operation_id}",
                    error_context={"operation_id": operation_id}
                )
                return
            
            # Calculate performance metrics
            start_time = self._active_operations.pop(operation_id)
            duration = time.perf_counter() - start_time
            self._operation_timings[operation_id] = duration
            
            # Find original metadata
            original_entry = None
            for entry in reversed(self._entries):
                if entry.metadata.operation_id == operation_id:
                    original_entry = entry
                    break
            
            if not original_entry:
                return
            
            # Log completion
            completion_metadata = OperationMetadata(
                operation_id=operation_id,
                block_id=original_entry.metadata.block_id,
                operation_type=original_entry.metadata.operation_type,
                timestamp=datetime.now(timezone.utc).isoformat(),
                thread_id=threading.get_ident(),
                user_context=original_entry.metadata.user_context,
                session_id=self._session_id,
                source_location=self._get_caller_location()
            )
            
            level = LogLevel.INFO if success else LogLevel.ERROR
            message = f"{'Completed' if success else 'Failed'} {original_entry.metadata.operation_type.value} operation"
            
            details = {
                "success": success,
                "duration_seconds": duration,
                **(result_data or {}),
                **kwargs
            }
            
            performance_metrics = {
                "duration_seconds": duration,
                "start_timestamp": start_time,
                "end_timestamp": time.perf_counter()
            }
            
            self._log_entry(
                metadata=completion_metadata,
                level=level,
                message=message,
                details=details,
                performance_metrics=performance_metrics
            )
    
    def log_state_transition(self,
                           block_id: str,
                           from_state: str,
                           to_state: str,
                           operation_id: Optional[str] = None,
                           validation_results: Optional[Dict[str, bool]] = None,
                           **kwargs):
        """Log a block state transition with full context."""
        op_id = operation_id or self.start_operation(
            block_id=block_id,
            operation_type=OperationType.STATE_TRANSITION
        )
        
        metadata = self._create_metadata(
            operation_id=op_id,
            block_id=block_id,
            operation_type=OperationType.STATE_TRANSITION
        )
        
        details = {
            "from_state": from_state,
            "to_state": to_state,
            "validation_results": validation_results,
            **kwargs
        }
        
        self._log_entry(
            metadata=metadata,
            level=LogLevel.INFO,
            message=f"Block {block_id} transitioned from {from_state} to {to_state}",
            details=details,
            integrity_results=validation_results
        )
        
        if not operation_id:  # We created it, so we end it
            self.end_operation(op_id, success=True)
    
    def log_error(self,
                 block_id: str,
                 operation_type: OperationType,
                 message: str,
                 error_context: Optional[Dict[str, Any]] = None,
                 exception: Optional[Exception] = None,
                 operation_id: Optional[str] = None):
        """Log an error with full context and stack trace."""
        op_id = operation_id or str(uuid4())
        
        metadata = self._create_metadata(
            operation_id=op_id,
            block_id=block_id,
            operation_type=operation_type
        )
        
        # Build error context
        full_error_context = {
            "error_type": type(exception).__name__ if exception else "Unknown",
            "error_message": str(exception) if exception else message,
            **(error_context or {})
        }
        
        if exception:
            full_error_context["stack_trace"] = traceback.format_exception(
                type(exception), exception, exception.__traceback__
            )
        
        self._log_entry(
            metadata=metadata,
            level=LogLevel.ERROR,
            message=message,
            details={"error_occurred": True},
            error_context=full_error_context
        )
    
    def log_performance_metric(self,
                              block_id: str,
                              operation_type: OperationType,
                              metrics: Dict[str, float],
                              operation_id: Optional[str] = None):
        """Log performance metrics for a block operation."""
        op_id = operation_id or str(uuid4())
        
        metadata = self._create_metadata(
            operation_id=op_id,
            block_id=block_id,
            operation_type=operation_type
        )
        
        self._log_entry(
            metadata=metadata,
            level=LogLevel.DEBUG,
            message=f"Performance metrics for {operation_type.value}",
            details={"metric_type": "performance"},
            performance_metrics=metrics
        )
    
    def log_integrity_check(self,
                           block_id: str,
                           check_results: Dict[str, bool],
                           data_snapshot: Optional[Dict[str, Any]] = None,
                           operation_id: Optional[str] = None):
        """Log data integrity check results."""
        op_id = operation_id or str(uuid4())
        
        metadata = self._create_metadata(
            operation_id=op_id,
            block_id=block_id,
            operation_type=OperationType.INTEGRITY_CHECK
        )
        
        all_passed = all(check_results.values())
        level = LogLevel.INFO if all_passed else LogLevel.WARNING
        
        self._log_entry(
            metadata=metadata,
            level=level,
            message=f"Integrity check {'passed' if all_passed else 'failed'} for block {block_id}",
            details={"checks_passed": sum(check_results.values()), "total_checks": len(check_results)},
            integrity_results=check_results,
            data_snapshot=data_snapshot
        )
    
    def get_operation_history(self, 
                            block_id: Optional[str] = None,
                            operation_type: Optional[OperationType] = None,
                            level: Optional[LogLevel] = None,
                            since: Optional[datetime] = None,
                            limit: Optional[int] = None) -> List[AuditLogEntry]:
        """
        Retrieve filtered operation history.
        
        Args:
            block_id: Filter by specific block ID
            operation_type: Filter by operation type
            level: Filter by log level
            since: Only entries after this timestamp
            limit: Maximum number of entries to return
        
        Returns:
            List of matching audit log entries
        """
        with self._lock:
            entries = self._entries.copy()
        
        # Apply filters
        if block_id:
            entries = [e for e in entries if e.metadata.block_id == block_id]
        
        if operation_type:
            entries = [e for e in entries if e.metadata.operation_type == operation_type]
        
        if level:
            entries = [e for e in entries if e.level == level]
        
        if since:
            since_iso = since.isoformat()
            entries = [e for e in entries if e.metadata.timestamp >= since_iso]
        
        # Sort by timestamp (newest first)
        entries.sort(key=lambda e: e.metadata.timestamp, reverse=True)
        
        if limit:
            entries = entries[:limit]
        
        return entries
    
    def reconstruct_block_timeline(self, block_id: str) -> List[AuditLogEntry]:
        """
        Reconstruct the complete timeline of operations for a specific block.
        
        Returns entries in chronological order (oldest first).
        """
        entries = self.get_operation_history(block_id=block_id)
        # Return in chronological order for timeline reconstruction
        return list(reversed(entries))
    
    def export_audit_log(self, 
                        output_path: Path,
                        format: str = "json",
                        filters: Optional[Dict[str, Any]] = None) -> Path:
        """
        Export audit log to file for analysis.
        
        Args:
            output_path: Where to save the export
            format: Export format ("json", "csv", "jsonl")
            filters: Optional filters to apply
        
        Returns:
            Path to the exported file
        """
        # Apply any filters
        entries = self._entries.copy()
        if filters:
            if 'block_id' in filters:
                entries = [e for e in entries if e.metadata.block_id == filters['block_id']]
            if 'operation_type' in filters:
                entries = [e for e in entries if e.metadata.operation_type.value == filters['operation_type']]
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if format == "json":
            data = [asdict(entry) for entry in entries]
            # Convert enums to strings
            for entry_dict in data:
                entry_dict['metadata']['operation_type'] = entry_dict['metadata']['operation_type'].value
                entry_dict['level'] = entry_dict['level'].value
            
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        
        elif format == "jsonl":
            with open(output_path, 'w') as f:
                for entry in entries:
                    entry_dict = asdict(entry)
                    entry_dict['metadata']['operation_type'] = entry_dict['metadata']['operation_type'].value
                    entry_dict['level'] = entry_dict['level'].value
                    f.write(json.dumps(entry_dict, default=str) + '\n')
        
        elif format == "csv":
            import csv
            with open(output_path, 'w', newline='') as f:
                if entries:
                    writer = csv.DictWriter(f, fieldnames=[
                        'timestamp', 'block_id', 'operation_type', 'level', 
                        'message', 'operation_id', 'thread_id'
                    ])
                    writer.writeheader()
                    for entry in entries:
                        writer.writerow({
                            'timestamp': entry.metadata.timestamp,
                            'block_id': entry.metadata.block_id,
                            'operation_type': entry.metadata.operation_type.value,
                            'level': entry.level.value,
                            'message': entry.message,
                            'operation_id': entry.metadata.operation_id,
                            'thread_id': entry.metadata.thread_id
                        })
        
        return output_path
    
    def get_performance_summary(self, 
                               operation_type: Optional[OperationType] = None) -> Dict[str, Any]:
        """Get performance summary statistics."""
        with self._lock:
            relevant_entries = self._entries.copy()
        
        if operation_type:
            relevant_entries = [
                e for e in relevant_entries 
                if e.metadata.operation_type == operation_type
            ]
        
        # Extract timing data
        timings = []
        for entry in relevant_entries:
            if entry.performance_metrics and 'duration_seconds' in entry.performance_metrics:
                timings.append(entry.performance_metrics['duration_seconds'])
        
        if not timings:
            return {"error": "No performance data available"}
        
        return {
            "operation_count": len(timings),
            "avg_duration": sum(timings) / len(timings),
            "min_duration": min(timings),
            "max_duration": max(timings),
            "total_duration": sum(timings)
        }
    
    def _create_metadata(self, 
                        operation_id: str,
                        block_id: str,
                        operation_type: OperationType) -> OperationMetadata:
        """Create metadata for a log entry."""
        return OperationMetadata(
            operation_id=operation_id,
            block_id=block_id,
            operation_type=operation_type,
            timestamp=datetime.now(timezone.utc).isoformat(),
            thread_id=threading.get_ident(),
            session_id=self._session_id,
            source_location=self._get_caller_location()
        )
    
    def _log_entry(self, 
                  metadata: OperationMetadata,
                  level: LogLevel,
                  message: str,
                  details: Dict[str, Any],
                  error_context: Optional[Dict[str, Any]] = None,
                  performance_metrics: Optional[Dict[str, float]] = None,
                  data_snapshot: Optional[Dict[str, Any]] = None,
                  integrity_results: Optional[Dict[str, bool]] = None):
        """Internal method to create and store a log entry."""
        entry = AuditLogEntry(
            metadata=metadata,
            level=level,
            message=message,
            details=details,
            error_context=error_context,
            performance_metrics=performance_metrics,
            data_snapshot=data_snapshot,
            integrity_results=integrity_results
        )
        
        with self._lock:
            self._entries.append(entry)
            
            # Also write to persistent log file
            self._write_to_file(entry)
    
    def _write_to_file(self, entry: AuditLogEntry):
        """Write log entry to persistent file."""
        try:
            entry_dict = asdict(entry)
            # Convert enums to strings for JSON serialization
            entry_dict['metadata']['operation_type'] = entry_dict['metadata']['operation_type'].value
            entry_dict['level'] = entry_dict['level'].value
            
            with open(self._current_log_file, 'a') as f:
                f.write(json.dumps(entry_dict, default=str) + '\n')
        except Exception as e:
            # Don't let logging errors break the application
            print(f"Warning: Failed to write audit log entry: {e}")
    
    def _get_caller_location(self) -> str:
        """Get the location of the calling code for audit trails."""
        try:
            frame = traceback.extract_stack()[-4]  # Skip this method and 2 wrapper calls
            return f"{frame.filename}:{frame.lineno}:{frame.name}"
        except:
            return "unknown"


# Global audit logger instance
audit_logger = BlockAuditLogger()