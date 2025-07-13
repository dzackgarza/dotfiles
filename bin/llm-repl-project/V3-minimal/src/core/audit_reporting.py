"""
Audit Trail Reporting and Management System

Provides high-level tools for analyzing, searching, and reconstructing
block operation audit trails for system administrators and developers.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import json

from .block_audit_logger import (
    audit_logger, 
    AuditLogEntry, 
    OperationType, 
    LogLevel
)


class AuditReportManager:
    """
    High-level manager for audit reporting and analysis.
    
    Provides system administrators with tools to understand system behavior,
    troubleshoot issues, and ensure data integrity.
    """
    
    def __init__(self):
        self.logger = audit_logger
    
    def get_block_timeline(self, block_id: str) -> Dict[str, Any]:
        """
        Get complete timeline for a specific block with analysis.
        
        Returns a comprehensive view of all operations performed on a block.
        """
        entries = self.logger.reconstruct_block_timeline(block_id)
        
        if not entries:
            return {
                "block_id": block_id,
                "status": "not_found",
                "message": "No audit trail found for this block"
            }
        
        # Analyze the timeline
        timeline_analysis = {
            "block_id": block_id,
            "status": "found",
            "total_operations": len(entries),
            "operation_summary": self._analyze_operations(entries),
            "timeline": [],
            "performance_summary": self._analyze_performance(entries),
            "error_summary": self._analyze_errors(entries),
            "integrity_summary": self._analyze_integrity(entries)
        }
        
        # Build detailed timeline
        for entry in entries:
            timeline_entry = {
                "timestamp": entry.metadata.timestamp,
                "operation_type": entry.metadata.operation_type.value,
                "level": entry.level.value,
                "message": entry.message,
                "operation_id": entry.metadata.operation_id,
                "thread_id": entry.metadata.thread_id
            }
            
            # Add performance data if available
            if entry.performance_metrics:
                timeline_entry["performance"] = entry.performance_metrics
            
            # Add error context if available
            if entry.error_context:
                timeline_entry["error"] = {
                    "type": entry.error_context.get("error_type"),
                    "message": entry.error_context.get("error_message")
                }
            
            # Add validation results if available
            if entry.integrity_results:
                timeline_entry["validation"] = entry.integrity_results
            
            timeline_analysis["timeline"].append(timeline_entry)
        
        return timeline_analysis
    
    def search_operations(self, 
                         query: str,
                         operation_type: Optional[str] = None,
                         level: Optional[str] = None,
                         since: Optional[str] = None,
                         until: Optional[str] = None,
                         limit: int = 100) -> Dict[str, Any]:
        """
        Search audit logs with flexible criteria.
        
        Args:
            query: Text to search for in messages and details
            operation_type: Filter by operation type
            level: Filter by log level  
            since: ISO timestamp - only entries after this time
            until: ISO timestamp - only entries before this time
            limit: Maximum results to return
        """
        # Parse timestamps if provided
        since_dt = datetime.fromisoformat(since) if since else None
        until_dt = datetime.fromisoformat(until) if until else None
        
        # Convert string filters to enums
        op_type = OperationType(operation_type) if operation_type else None
        log_level = LogLevel(level) if level else None
        
        # Get base filtered entries
        entries = self.logger.get_operation_history(
            operation_type=op_type,
            level=log_level,
            since=since_dt,
            limit=limit * 2  # Get more than needed for text filtering
        )
        
        # Apply additional filters
        filtered_entries = []
        for entry in entries:
            # Time range filter
            entry_time = datetime.fromisoformat(entry.metadata.timestamp)
            if until_dt and entry_time > until_dt:
                continue
            
            # Text search in message and details
            if query:
                searchable_text = entry.message.lower()
                if entry.details:
                    searchable_text += " " + json.dumps(entry.details).lower()
                
                if query.lower() not in searchable_text:
                    continue
            
            filtered_entries.append(entry)
            
            if len(filtered_entries) >= limit:
                break
        
        # Build search results
        results = {
            "query": query,
            "filters": {
                "operation_type": operation_type,
                "level": level,
                "since": since,
                "until": until
            },
            "total_matches": len(filtered_entries),
            "entries": []
        }
        
        for entry in filtered_entries:
            result_entry = {
                "timestamp": entry.metadata.timestamp,
                "block_id": entry.metadata.block_id,
                "operation_type": entry.metadata.operation_type.value,
                "level": entry.level.value,
                "message": entry.message,
                "operation_id": entry.metadata.operation_id
            }
            
            # Add relevant context based on search
            if entry.error_context and (not level or level == "error"):
                result_entry["error"] = entry.error_context
            
            if entry.performance_metrics and "performance" in query.lower():
                result_entry["performance"] = entry.performance_metrics
            
            results["entries"].append(result_entry)
        
        return results
    
    def get_system_health_report(self, 
                                hours_back: int = 24) -> Dict[str, Any]:
        """
        Generate comprehensive system health report.
        
        Analyzes recent operations to identify issues, patterns, and performance.
        """
        since = datetime.now() - timedelta(hours=hours_back)
        entries = self.logger.get_operation_history(since=since)
        
        if not entries:
            return {
                "status": "no_data",
                "message": f"No audit data found for the last {hours_back} hours"
            }
        
        report = {
            "report_period": f"Last {hours_back} hours",
            "generated_at": datetime.now().isoformat(),
            "total_operations": len(entries),
            "operation_breakdown": self._analyze_operations(entries),
            "error_analysis": self._analyze_errors(entries),
            "performance_analysis": self._analyze_performance(entries),
            "integrity_analysis": self._analyze_integrity(entries),
            "block_activity": self._analyze_block_activity(entries),
            "recommendations": self._generate_recommendations(entries)
        }
        
        return report
    
    def export_block_audit_trail(self, 
                                block_id: str,
                                output_path: Optional[Path] = None) -> Path:
        """
        Export complete audit trail for a specific block.
        
        Creates a detailed report for forensic analysis or compliance.
        """
        timeline = self.get_block_timeline(block_id)
        
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = Path(f"audit_export_block_{block_id}_{timestamp}.json")
        
        # Add export metadata
        export_data = {
            "export_metadata": {
                "block_id": block_id,
                "exported_at": datetime.now().isoformat(),
                "export_type": "block_audit_trail",
                "tool_version": "V3-minimal"
            },
            "audit_trail": timeline
        }
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        return output_path
    
    def validate_system_integrity(self) -> Dict[str, Any]:
        """
        Run comprehensive system integrity validation.
        
        Checks for inconsistencies, missing data, and potential issues.
        """
        # Get recent entries for analysis
        recent_entries = self.logger.get_operation_history(limit=1000)
        
        integrity_report = {
            "validated_at": datetime.now().isoformat(),
            "checks_performed": [],
            "issues_found": [],
            "recommendations": []
        }
        
        # Check 1: Operation continuity
        self._check_operation_continuity(recent_entries, integrity_report)
        
        # Check 2: State transition validity
        self._check_state_transitions(recent_entries, integrity_report)
        
        # Check 3: Error pattern analysis
        self._check_error_patterns(recent_entries, integrity_report)
        
        # Check 4: Performance anomalies
        self._check_performance_anomalies(recent_entries, integrity_report)
        
        # Generate overall status
        total_issues = len(integrity_report["issues_found"])
        if total_issues == 0:
            integrity_report["status"] = "healthy"
        elif total_issues <= 3:
            integrity_report["status"] = "warning"
        else:
            integrity_report["status"] = "critical"
        
        return integrity_report
    
    def _analyze_operations(self, entries: List[AuditLogEntry]) -> Dict[str, Any]:
        """Analyze operation type distribution and patterns."""
        op_counts = {}
        for entry in entries:
            op_type = entry.metadata.operation_type.value
            op_counts[op_type] = op_counts.get(op_type, 0) + 1
        
        return {
            "by_type": op_counts,
            "most_common": max(op_counts.items(), key=lambda x: x[1]) if op_counts else None,
            "unique_operations": len(op_counts)
        }
    
    def _analyze_errors(self, entries: List[AuditLogEntry]) -> Dict[str, Any]:
        """Analyze error patterns and frequency."""
        error_entries = [e for e in entries if e.level == LogLevel.ERROR]
        
        if not error_entries:
            return {"status": "no_errors", "count": 0}
        
        error_types = {}
        for entry in error_entries:
            if entry.error_context and "error_type" in entry.error_context:
                error_type = entry.error_context["error_type"]
                error_types[error_type] = error_types.get(error_type, 0) + 1
        
        return {
            "status": "errors_found",
            "count": len(error_entries),
            "error_rate": len(error_entries) / len(entries) * 100,
            "by_type": error_types,
            "most_recent": error_entries[0].metadata.timestamp if error_entries else None
        }
    
    def _analyze_performance(self, entries: List[AuditLogEntry]) -> Dict[str, Any]:
        """Analyze performance metrics across operations."""
        perf_entries = [e for e in entries if e.performance_metrics]
        
        if not perf_entries:
            return {"status": "no_performance_data"}
        
        durations = []
        for entry in perf_entries:
            if "duration_seconds" in entry.performance_metrics:
                durations.append(entry.performance_metrics["duration_seconds"])
        
        if not durations:
            return {"status": "no_duration_data"}
        
        return {
            "status": "data_available",
            "operation_count": len(durations),
            "avg_duration": sum(durations) / len(durations),
            "min_duration": min(durations),
            "max_duration": max(durations),
            "slow_operations": len([d for d in durations if d > 1.0])
        }
    
    def _analyze_integrity(self, entries: List[AuditLogEntry]) -> Dict[str, Any]:
        """Analyze data integrity check results."""
        integrity_entries = [e for e in entries if e.integrity_results]
        
        if not integrity_entries:
            return {"status": "no_integrity_data"}
        
        total_checks = 0
        passed_checks = 0
        
        for entry in integrity_entries:
            for check_name, result in entry.integrity_results.items():
                total_checks += 1
                if result:
                    passed_checks += 1
        
        return {
            "status": "data_available",
            "total_checks": total_checks,
            "passed_checks": passed_checks,
            "pass_rate": passed_checks / total_checks * 100 if total_checks > 0 else 0,
            "failed_checks": total_checks - passed_checks
        }
    
    def _analyze_block_activity(self, entries: List[AuditLogEntry]) -> Dict[str, Any]:
        """Analyze per-block activity patterns."""
        block_ops = {}
        for entry in entries:
            block_id = entry.metadata.block_id
            if block_id not in block_ops:
                block_ops[block_id] = {"operations": 0, "errors": 0}
            
            block_ops[block_id]["operations"] += 1
            if entry.level == LogLevel.ERROR:
                block_ops[block_id]["errors"] += 1
        
        # Find most active blocks
        most_active = sorted(block_ops.items(), key=lambda x: x[1]["operations"], reverse=True)[:5]
        
        return {
            "unique_blocks": len(block_ops),
            "most_active": most_active,
            "blocks_with_errors": len([b for b, stats in block_ops.items() if stats["errors"] > 0])
        }
    
    def _generate_recommendations(self, entries: List[AuditLogEntry]) -> List[str]:
        """Generate actionable recommendations based on audit data."""
        recommendations = []
        
        # Check error rate
        error_entries = [e for e in entries if e.level == LogLevel.ERROR]
        error_rate = len(error_entries) / len(entries) * 100 if entries else 0
        
        if error_rate > 10:
            recommendations.append(f"High error rate ({error_rate:.1f}%) - investigate common failure patterns")
        
        # Check performance
        perf_entries = [e for e in entries if e.performance_metrics and "duration_seconds" in e.performance_metrics]
        if perf_entries:
            avg_duration = sum(e.performance_metrics["duration_seconds"] for e in perf_entries) / len(perf_entries)
            if avg_duration > 2.0:
                recommendations.append(f"Average operation duration ({avg_duration:.2f}s) is high - consider performance optimization")
        
        # Check integrity
        integrity_entries = [e for e in entries if e.integrity_results]
        if integrity_entries:
            failed_checks = sum(1 for e in integrity_entries for result in e.integrity_results.values() if not result)
            if failed_checks > 0:
                recommendations.append(f"Found {failed_checks} failed integrity checks - review data consistency")
        
        if not recommendations:
            recommendations.append("System appears healthy - continue monitoring")
        
        return recommendations
    
    def _check_operation_continuity(self, entries: List[AuditLogEntry], report: Dict[str, Any]):
        """Check for operation continuity issues."""
        report["checks_performed"].append("operation_continuity")
        
        # Check for incomplete operations (start without end)
        operation_starts = {}
        operation_ends = set()
        
        for entry in entries:
            op_id = entry.metadata.operation_id
            if "Started" in entry.message:
                operation_starts[op_id] = entry.metadata.timestamp
            elif "Completed" in entry.message or "Failed" in entry.message:
                operation_ends.add(op_id)
        
        incomplete_ops = set(operation_starts.keys()) - operation_ends
        if incomplete_ops:
            report["issues_found"].append({
                "type": "incomplete_operations",
                "count": len(incomplete_ops),
                "description": f"Found {len(incomplete_ops)} operations that started but never completed"
            })
    
    def _check_state_transitions(self, entries: List[AuditLogEntry], report: Dict[str, Any]):
        """Check for invalid state transitions."""
        report["checks_performed"].append("state_transitions")
        
        transition_entries = [e for e in entries if e.metadata.operation_type == OperationType.STATE_TRANSITION]
        invalid_transitions = []
        
        for entry in transition_entries:
            if entry.details:
                from_state = entry.details.get("from_state")
                to_state = entry.details.get("to_state")
                
                # Check for invalid transitions (basic validation)
                if from_state == to_state:
                    invalid_transitions.append(f"Block {entry.metadata.block_id}: redundant transition {from_state} -> {to_state}")
        
        if invalid_transitions:
            report["issues_found"].append({
                "type": "invalid_state_transitions", 
                "count": len(invalid_transitions),
                "examples": invalid_transitions[:3]
            })
    
    def _check_error_patterns(self, entries: List[AuditLogEntry], report: Dict[str, Any]):
        """Check for concerning error patterns."""
        report["checks_performed"].append("error_patterns")
        
        error_entries = [e for e in entries if e.level == LogLevel.ERROR]
        
        # Check for rapid error sequences
        if len(error_entries) >= 5:
            error_times = [datetime.fromisoformat(e.metadata.timestamp) for e in error_entries[:5]]
            time_span = error_times[0] - error_times[-1]
            
            if time_span.total_seconds() < 60:  # 5 errors in under a minute
                report["issues_found"].append({
                    "type": "rapid_error_sequence",
                    "description": "Found 5 errors within 60 seconds - possible cascade failure"
                })
    
    def _check_performance_anomalies(self, entries: List[AuditLogEntry], report: Dict[str, Any]):
        """Check for performance anomalies."""
        report["checks_performed"].append("performance_anomalies")
        
        perf_entries = [e for e in entries if e.performance_metrics and "duration_seconds" in e.performance_metrics]
        
        if len(perf_entries) < 10:
            return
        
        durations = [e.performance_metrics["duration_seconds"] for e in perf_entries]
        avg_duration = sum(durations) / len(durations)
        
        # Check for operations taking significantly longer than average
        slow_ops = [d for d in durations if d > avg_duration * 3]
        
        if slow_ops:
            report["issues_found"].append({
                "type": "performance_anomalies",
                "count": len(slow_ops),
                "description": f"Found {len(slow_ops)} operations taking >3x average duration"
            })


# Global report manager instance
report_manager = AuditReportManager()