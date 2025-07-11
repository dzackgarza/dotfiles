"""
Performance Monitor for Live Block System

Monitors and optimizes the performance of live blocks,
providing metrics and automatic optimizations.
"""

import time
from typing import Dict, List, Any
from dataclasses import dataclass
from collections import deque
from datetime import datetime, timedelta

from .live_blocks import LiveBlock, LiveBlockManager


@dataclass
class PerformanceMetrics:
    """Performance metrics for live block operations."""

    block_creation_time: float = 0.0
    block_update_time: float = 0.0
    simulation_time: float = 0.0
    inscription_time: float = 0.0
    ui_update_time: float = 0.0
    memory_usage_mb: float = 0.0
    active_blocks_count: int = 0
    update_frequency_hz: float = 0.0
    callback_execution_time: float = 0.0
    timestamp: float = 0.0


@dataclass
class PerformanceWarning:
    """Warning about performance issues."""

    timestamp: datetime
    severity: str  # "low", "medium", "high", "critical"
    component: str
    message: str
    metrics: Dict[str, Any]
    suggested_action: str


class PerformanceMonitor:
    """Monitors performance of the live block system."""

    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.metrics_history: deque = deque(maxlen=max_history)
        self.warnings: List[PerformanceWarning] = []
        self.start_time = time.time()

        # Performance thresholds
        self.thresholds = {
            "block_creation_ms": 100,  # Max time for block creation
            "ui_update_ms": 16,  # Target 60fps
            "simulation_ms": 5000,  # Max simulation time
            "callback_ms": 10,  # Max callback execution
            "memory_mb": 100,  # Max memory usage
            "active_blocks": 50,  # Max concurrent blocks
            "update_hz": 30,  # Max update frequency
        }

        # Optimization flags
        self.optimizations_enabled = {
            "lazy_ui_updates": True,
            "callback_batching": True,
            "memory_cleanup": True,
            "throttle_updates": True,
        }

        # Performance counters
        self.counters = {
            "blocks_created": 0,
            "blocks_inscribed": 0,
            "ui_updates": 0,
            "callbacks_executed": 0,
            "optimizations_applied": 0,
        }

    def start_timing(self, operation: str) -> float:
        """Start timing an operation."""
        return time.time()

    def end_timing(self, start_time: float, operation: str) -> float:
        """End timing an operation and record metrics."""
        duration = time.time() - start_time
        self._record_operation_time(operation, duration)
        return duration

    def _record_operation_time(self, operation: str, duration: float) -> None:
        """Record timing for an operation."""
        duration_ms = duration * 1000

        # Check for performance issues
        threshold_key = f"{operation}_ms"
        if threshold_key in self.thresholds:
            threshold = self.thresholds[threshold_key]
            if duration_ms > threshold:
                self._add_warning(
                    severity="medium" if duration_ms < threshold * 2 else "high",
                    component=operation,
                    message=f"{operation} took {duration_ms:.1f}ms (threshold: {threshold}ms)",
                    metrics={"duration_ms": duration_ms, "threshold_ms": threshold},
                    suggested_action=f"Consider optimizing {operation} performance",
                )

    def record_metrics(self, manager: LiveBlockManager) -> PerformanceMetrics:
        """Record current performance metrics."""
        current_time = time.time()

        # Calculate memory usage (approximate)
        memory_usage = self._estimate_memory_usage(manager)

        # Calculate update frequency
        recent_updates = len(
            [m for m in self.metrics_history if (current_time - m.timestamp) < 1.0]
        )

        metrics = PerformanceMetrics(
            memory_usage_mb=memory_usage,
            active_blocks_count=len(manager.get_live_blocks()),
            update_frequency_hz=recent_updates,
            timestamp=current_time,
        )
        self.metrics_history.append(metrics)

        # Check for performance issues
        self._check_performance_thresholds(metrics)

        return metrics

    def _estimate_memory_usage(self, manager: LiveBlockManager) -> float:
        """Estimate memory usage of live blocks."""
        total_size = 0

        for block in manager.get_live_blocks():
            # Estimate size of block content and metadata
            content_size = len(block.data.content.encode("utf-8"))
            metadata_size = len(str(block.data.metadata).encode("utf-8"))
            sub_blocks_size = len(block.data.sub_blocks) * 1000  # Rough estimate

            total_size += (
                content_size + metadata_size + sub_blocks_size + 1000
            )  # Base object size

        return total_size / (1024 * 1024)  # Convert to MB

    def _check_performance_thresholds(self, metrics: PerformanceMetrics) -> None:
        """Check metrics against performance thresholds."""
        checks = [
            (metrics.memory_usage_mb, "memory_mb", "Memory usage"),
            (metrics.active_blocks_count, "active_blocks", "Active blocks count"),
            (metrics.update_frequency_hz, "update_hz", "Update frequency"),
        ]

        for value, threshold_key, description in checks:
            if threshold_key in self.thresholds:
                threshold = self.thresholds[threshold_key]
                if value > threshold:
                    severity = "high" if value > threshold * 1.5 else "medium"
                    self._add_warning(
                        severity=severity,
                        component="system",
                        message=f"{description} ({value:.1f}) exceeds threshold ({threshold})",
                        metrics={threshold_key: value, "threshold": threshold},
                        suggested_action=self._get_optimization_suggestion(
                            threshold_key
                        ),
                    )

    def _get_optimization_suggestion(self, metric: str) -> str:
        """Get optimization suggestion for a metric."""
        suggestions = {
            "memory_mb": "Consider inscribing old blocks or reducing content size",
            "active_blocks": "Inscribe completed blocks to reduce active count",
            "update_hz": "Enable update throttling or reduce update frequency",
            "callback_ms": "Optimize callback functions or enable batching",
        }
        return suggestions.get(metric, "Review system performance")

    def _add_warning(
        self,
        severity: str,
        component: str,
        message: str,
        metrics: Dict[str, Any],
        suggested_action: str,
    ) -> None:
        """Add a performance warning."""
        warning = PerformanceWarning(
            timestamp=datetime.now(),
            severity=severity,
            component=component,
            message=message,
            metrics=metrics,
            suggested_action=suggested_action,
        )

        self.warnings.append(warning)

        # Keep only recent warnings
        cutoff = datetime.now() - timedelta(minutes=10)
        self.warnings = [w for w in self.warnings if w.timestamp > cutoff]

    def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report."""
        if not self.metrics_history:
            return {"status": "no_data", "message": "No performance data available"}

        recent_metrics = list(self.metrics_history)[-10:]  # Last 10 measurements

        # Calculate averages
        avg_memory = sum(m.memory_usage_mb for m in recent_metrics) / len(
            recent_metrics
        )
        avg_blocks = sum(m.active_blocks_count for m in recent_metrics) / len(
            recent_metrics
        )
        avg_frequency = sum(m.update_frequency_hz for m in recent_metrics) / len(
            recent_metrics
        )

        # Count warnings by severity
        warning_counts: dict[str, int] = {}
        for warning in self.warnings:
            warning_counts[warning.severity] = (
                warning_counts.get(warning.severity, 0) + 1
            )

        # Determine overall status
        if warning_counts.get("critical", 0) > 0:
            status = "critical"
        elif warning_counts.get("high", 0) > 0:
            status = "warning"
        elif warning_counts.get("medium", 0) > 0:
            status = "caution"
        else:
            status = "good"

        return {
            "status": status,
            "uptime_seconds": time.time() - self.start_time,
            "metrics": {
                "average_memory_mb": round(avg_memory, 2),
                "average_active_blocks": round(avg_blocks, 1),
                "average_update_frequency": round(avg_frequency, 1),
                "total_blocks_created": self.counters["blocks_created"],
                "total_blocks_inscribed": self.counters["blocks_inscribed"],
                "total_ui_updates": self.counters["ui_updates"],
            },
            "warnings": {
                "total": len(self.warnings),
                "by_severity": warning_counts,
                "recent": [
                    {
                        "severity": w.severity,
                        "component": w.component,
                        "message": w.message,
                        "suggested_action": w.suggested_action,
                    }
                    for w in self.warnings[-5:]  # Last 5 warnings
                ],
            },
            "optimizations": {
                "enabled": self.optimizations_enabled.copy(),
                "applied_count": self.counters["optimizations_applied"],
            },
        }

    def apply_optimization(self, optimization: str) -> bool:
        """Apply a specific optimization."""
        if optimization not in self.optimizations_enabled:
            return False

        if optimization == "lazy_ui_updates":
            # Implementation would throttle UI updates
            pass
        elif optimization == "callback_batching":
            # Implementation would batch callback executions
            pass
        elif optimization == "memory_cleanup":
            # Implementation would trigger memory cleanup
            pass
        elif optimization == "throttle_updates":
            # Implementation would reduce update frequency
            pass

        self.counters["optimizations_applied"] += 1
        return True

    def get_optimization_recommendations(self) -> List[Dict[str, Any]]:
        """Get recommendations for performance optimizations."""
        recommendations: list[dict[str, Any]] = []

        if not self.metrics_history:
            return recommendations

        latest_metrics = self.metrics_history[-1]

        # Memory optimization
        if latest_metrics.memory_usage_mb > self.thresholds["memory_mb"] * 0.8:
            recommendations.append(
                {
                    "type": "memory",
                    "priority": "high",
                    "description": "Memory usage is approaching limits",
                    "action": "Enable memory cleanup optimization",
                    "optimization": "memory_cleanup",
                }
            )

        # Active blocks optimization
        if latest_metrics.active_blocks_count > self.thresholds["active_blocks"] * 0.8:
            recommendations.append(
                {
                    "type": "blocks",
                    "priority": "medium",
                    "description": "Many active blocks may impact performance",
                    "action": "Inscribe completed blocks more aggressively",
                    "optimization": "auto_inscription",
                }
            )

        # Update frequency optimization
        if latest_metrics.update_frequency_hz > self.thresholds["update_hz"] * 0.8:
            recommendations.append(
                {
                    "type": "updates",
                    "priority": "medium",
                    "description": "High update frequency may cause UI lag",
                    "action": "Enable update throttling",
                    "optimization": "throttle_updates",
                }
            )

        return recommendations


class OptimizedLiveBlockManager(LiveBlockManager):
    """LiveBlockManager with performance monitoring and optimizations."""

    def __init__(self):
        super().__init__()
        self.performance_monitor = PerformanceMonitor()
        self._last_cleanup = time.time()
        self._cleanup_interval = 30.0  # seconds

    def create_live_block(self, role: str, initial_content: str = "") -> LiveBlock:
        """Create live block with performance monitoring."""
        start_time = self.performance_monitor.start_timing("block_creation")

        block = super().create_live_block(role, initial_content)

        self.performance_monitor.end_timing(start_time, "block_creation")
        self.performance_monitor.counters["blocks_created"] += 1

        # Periodic cleanup
        self._maybe_perform_cleanup()

        return block

    def inscribe_block(self, block_id: str):
        """Inscribe block with performance monitoring."""
        start_time = self.performance_monitor.start_timing("inscription")

        result = super().inscribe_block(block_id)

        if result is not None:  # inscribe_block returns InscribedBlock or None
            self.performance_monitor.end_timing(start_time, "inscription")
            self.performance_monitor.counters["blocks_inscribed"] += 1

        return result

    def _maybe_perform_cleanup(self) -> None:
        """Perform cleanup if needed."""
        current_time = time.time()
        if current_time - self._last_cleanup > self._cleanup_interval:
            self._perform_cleanup()
            self._last_cleanup = current_time

    def _perform_cleanup(self) -> None:
        """Perform performance cleanup."""
        # Auto-inscribe blocks that have been live for too long
        current_time = time.time()
        old_blocks = []

        for block in self.get_live_blocks():
            block_age = current_time - block.created_at.timestamp()
            if block_age > 300:  # 5 minutes
                old_blocks.append(block.id)

        for block_id in old_blocks:
            self.inscribe_block(block_id)

        if old_blocks:
            self.performance_monitor.counters["optimizations_applied"] += 1

    def get_performance_status(self) -> Dict[str, Any]:
        """Get current performance status."""
        self.performance_monitor.record_metrics(self)
        return self.performance_monitor.get_performance_report()
