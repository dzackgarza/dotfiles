"""Tests for performance monitoring system."""

import pytest
import time

from src.core.performance_monitor import (
    PerformanceMetrics,
    PerformanceWarning,
    PerformanceMonitor,
    OptimizedLiveBlockManager,
)
from src.core.live_blocks import LiveBlockManager


class TestPerformanceMetrics:
    """Test PerformanceMetrics dataclass."""

    def test_initialization(self):
        """Test metrics initialization with defaults."""
        metrics = PerformanceMetrics()

        assert metrics.block_creation_time == 0.0
        assert metrics.block_update_time == 0.0
        assert metrics.simulation_time == 0.0
        assert metrics.inscription_time == 0.0
        assert metrics.ui_update_time == 0.0
        assert metrics.memory_usage_mb == 0.0
        assert metrics.active_blocks_count == 0
        assert metrics.update_frequency_hz == 0.0
        assert metrics.callback_execution_time == 0.0

    def test_initialization_with_values(self):
        """Test metrics initialization with custom values."""
        metrics = PerformanceMetrics(
            block_creation_time=0.05, memory_usage_mb=10.5, active_blocks_count=5
        )

        assert metrics.block_creation_time == 0.05
        assert metrics.memory_usage_mb == 10.5
        assert metrics.active_blocks_count == 5


class TestPerformanceWarning:
    """Test PerformanceWarning dataclass."""

    def test_initialization(self):
        """Test warning initialization."""
        from datetime import datetime

        timestamp = datetime.now()
        warning = PerformanceWarning(
            timestamp=timestamp,
            severity="high",
            component="test_component",
            message="Test warning message",
            metrics={"test_value": 100},
            suggested_action="Take action",
        )

        assert warning.timestamp == timestamp
        assert warning.severity == "high"
        assert warning.component == "test_component"
        assert warning.message == "Test warning message"
        assert warning.metrics == {"test_value": 100}
        assert warning.suggested_action == "Take action"


class TestPerformanceMonitor:
    """Test PerformanceMonitor functionality."""

    def test_initialization(self):
        """Test monitor initializes correctly."""
        monitor = PerformanceMonitor()

        assert monitor.max_history == 1000
        assert len(monitor.metrics_history) == 0
        assert len(monitor.warnings) == 0
        assert monitor.start_time > 0

        # Check thresholds are set
        assert "block_creation_ms" in monitor.thresholds
        assert "memory_mb" in monitor.thresholds
        assert "active_blocks" in monitor.thresholds

        # Check optimizations are configured
        assert "lazy_ui_updates" in monitor.optimizations_enabled
        assert "memory_cleanup" in monitor.optimizations_enabled

        # Check counters are initialized
        assert monitor.counters["blocks_created"] == 0
        assert monitor.counters["blocks_inscribed"] == 0

    def test_custom_max_history(self):
        """Test monitor with custom max history."""
        monitor = PerformanceMonitor(max_history=500)
        assert monitor.max_history == 500
        assert monitor.metrics_history.maxlen == 500

    def test_timing_operations(self):
        """Test timing functionality."""
        monitor = PerformanceMonitor()

        start_time = monitor.start_timing("test_operation")
        assert isinstance(start_time, float)
        assert start_time > 0

        # Small delay to ensure measurable duration
        time.sleep(0.01)

        duration = monitor.end_timing(start_time, "test_operation")
        assert duration > 0
        assert duration < 1.0  # Should be small

    def test_operation_time_recording(self):
        """Test operation time recording and threshold checking."""
        monitor = PerformanceMonitor()

        # Set a low threshold for testing
        monitor.thresholds["test_operation_ms"] = 1.0  # 1ms

        start_time = time.time()
        time.sleep(0.005)  # 5ms delay

        # This should trigger a warning
        monitor.end_timing(start_time, "test_operation")

        # Check that a warning was generated
        assert len(monitor.warnings) > 0
        warning = monitor.warnings[-1]
        assert warning.component == "test_operation"
        assert "threshold" in warning.message.lower()

    def test_record_metrics(self):
        """Test metrics recording from manager."""
        monitor = PerformanceMonitor()
        manager = LiveBlockManager()

        # Create some live blocks
        block1 = manager.create_live_block("user", "Test content")
        block2 = manager.create_live_block("assistant", "Response content")

        metrics = monitor.record_metrics(manager)

        assert isinstance(metrics, PerformanceMetrics)
        assert metrics.active_blocks_count == 2
        assert metrics.memory_usage_mb >= 0
        assert hasattr(metrics, "timestamp")

        # Check that metrics were added to history
        assert len(monitor.metrics_history) == 1
        assert monitor.metrics_history[0] == metrics

    def test_memory_estimation(self):
        """Test memory usage estimation."""
        monitor = PerformanceMonitor()
        manager = LiveBlockManager()

        # Create a block with substantial content
        large_content = "x" * 10000  # 10KB content
        block = manager.create_live_block("user", large_content)

        memory_usage = monitor._estimate_memory_usage(manager)

        assert memory_usage > 0
        assert isinstance(memory_usage, float)

    def test_performance_threshold_checking(self):
        """Test performance threshold checking."""
        monitor = PerformanceMonitor()

        # Create metrics that exceed thresholds
        metrics = PerformanceMetrics(
            memory_usage_mb=150,  # Above default 100MB threshold
            active_blocks_count=60,  # Above default 50 blocks threshold
            update_frequency_hz=40,  # Above default 30Hz threshold
        )

        initial_warnings = len(monitor.warnings)
        monitor._check_performance_thresholds(metrics)

        # Should have generated warnings
        assert len(monitor.warnings) > initial_warnings

        # Check warning content
        memory_warnings = [w for w in monitor.warnings if "Memory usage" in w.message]
        blocks_warnings = [w for w in monitor.warnings if "Active blocks" in w.message]
        frequency_warnings = [
            w for w in monitor.warnings if "Update frequency" in w.message
        ]

        assert len(memory_warnings) > 0
        assert len(blocks_warnings) > 0
        assert len(frequency_warnings) > 0

    def test_optimization_suggestions(self):
        """Test optimization suggestions."""
        monitor = PerformanceMonitor()

        suggestions = {
            "memory_mb": monitor._get_optimization_suggestion("memory_mb"),
            "active_blocks": monitor._get_optimization_suggestion("active_blocks"),
            "update_hz": monitor._get_optimization_suggestion("update_hz"),
            "callback_ms": monitor._get_optimization_suggestion("callback_ms"),
            "unknown": monitor._get_optimization_suggestion("unknown_metric"),
        }

        assert "inscrib" in suggestions["memory_mb"].lower()
        assert "inscrib" in suggestions["active_blocks"].lower()
        assert "throttl" in suggestions["update_hz"].lower()
        assert "optim" in suggestions["callback_ms"].lower()
        assert suggestions["unknown"] == "Review system performance"

    def test_performance_report_no_data(self):
        """Test performance report with no data."""
        monitor = PerformanceMonitor()

        report = monitor.get_performance_report()

        assert report["status"] == "no_data"
        assert "No performance data available" in report["message"]

    def test_performance_report_with_data(self):
        """Test performance report with metrics data."""
        monitor = PerformanceMonitor()
        manager = LiveBlockManager()

        # Generate some metrics
        for i in range(5):
            manager.create_live_block("user", f"Test content {i}")
            monitor.record_metrics(manager)
            time.sleep(0.01)  # Small delay between measurements

        report = monitor.get_performance_report()

        assert report["status"] in ["good", "caution", "warning", "critical"]
        assert "uptime_seconds" in report
        assert "metrics" in report
        assert "warnings" in report
        assert "optimizations" in report

        metrics = report["metrics"]
        assert "average_memory_mb" in metrics
        assert "average_active_blocks" in metrics
        assert "average_update_frequency" in metrics
        assert "total_blocks_created" in metrics

        warnings = report["warnings"]
        assert "total" in warnings
        assert "by_severity" in warnings
        assert "recent" in warnings

    def test_apply_optimization(self):
        """Test optimization application."""
        monitor = PerformanceMonitor()

        initial_count = monitor.counters["optimizations_applied"]

        # Apply valid optimization
        result = monitor.apply_optimization("memory_cleanup")
        assert result is True
        assert monitor.counters["optimizations_applied"] == initial_count + 1

        # Apply invalid optimization
        result = monitor.apply_optimization("invalid_optimization")
        assert result is False
        assert monitor.counters["optimizations_applied"] == initial_count + 1

    def test_optimization_recommendations(self):
        """Test optimization recommendations."""
        monitor = PerformanceMonitor()

        # No metrics - no recommendations
        recommendations = monitor.get_optimization_recommendations()
        assert recommendations == []

        # Add metrics that trigger recommendations
        high_memory_metrics = PerformanceMetrics(
            memory_usage_mb=85,  # 85% of 100MB threshold
            active_blocks_count=45,  # 90% of 50 blocks threshold
            update_frequency_hz=28,  # 93% of 30Hz threshold
        )

        monitor.metrics_history.append(high_memory_metrics)

        recommendations = monitor.get_optimization_recommendations()

        assert len(recommendations) > 0

        # Check recommendation structure
        for rec in recommendations:
            assert "type" in rec
            assert "priority" in rec
            assert "description" in rec
            assert "action" in rec
            assert rec["priority"] in ["low", "medium", "high"]

    def test_warning_cleanup(self):
        """Test that old warnings are cleaned up."""
        monitor = PerformanceMonitor()

        # Add a warning manually with old timestamp
        from datetime import datetime, timedelta

        old_warning = PerformanceWarning(
            timestamp=datetime.now() - timedelta(minutes=15),
            severity="low",
            component="test",
            message="Old warning",
            metrics={},
            suggested_action="None",
        )

        monitor.warnings.append(old_warning)
        assert len(monitor.warnings) == 1

        # Add a new warning through normal process
        monitor._add_warning(
            severity="medium",
            component="test",
            message="New warning",
            metrics={},
            suggested_action="Action",
        )

        # Old warning should be cleaned up (older than 10 minutes)
        recent_warnings = [
            w
            for w in monitor.warnings
            if (datetime.now() - w.timestamp).total_seconds() < 600
        ]
        assert len(recent_warnings) == 1
        assert recent_warnings[0].message == "New warning"


class TestOptimizedLiveBlockManager:
    """Test OptimizedLiveBlockManager functionality."""

    def test_initialization(self):
        """Test optimized manager initializes correctly."""
        manager = OptimizedLiveBlockManager()

        assert hasattr(manager, "performance_monitor")
        assert hasattr(manager, "_last_cleanup")
        assert hasattr(manager, "_cleanup_interval")
        assert manager._cleanup_interval == 30.0

    def test_create_live_block_with_monitoring(self):
        """Test block creation with performance monitoring."""
        manager = OptimizedLiveBlockManager()

        initial_count = manager.performance_monitor.counters["blocks_created"]

        block = manager.create_live_block("user", "Test content")

        assert block is not None
        assert block.role == "user"
        assert block.data.content == "Test content"
        assert (
            manager.performance_monitor.counters["blocks_created"] == initial_count + 1
        )

    def test_inscribe_block_with_monitoring(self):
        """Test block inscription with performance monitoring."""
        manager = OptimizedLiveBlockManager()

        # Create a block
        block = manager.create_live_block("user", "Test content")
        block_id = block.id

        initial_count = manager.performance_monitor.counters["blocks_inscribed"]

        # Inscribe the block
        result = manager.inscribe_block(block_id)

        assert result is not None  # Returns InscribedBlock, not True
        assert (
            manager.performance_monitor.counters["blocks_inscribed"]
            == initial_count + 1
        )

    def test_performance_status(self):
        """Test getting performance status."""
        manager = OptimizedLiveBlockManager()

        # Create some blocks
        for i in range(3):
            manager.create_live_block("user", f"Content {i}")

        status = manager.get_performance_status()

        assert isinstance(status, dict)
        assert "status" in status
        assert "metrics" in status
        assert "warnings" in status
        assert "optimizations" in status

    def test_cleanup_trigger(self):
        """Test that cleanup is triggered appropriately."""
        manager = OptimizedLiveBlockManager()

        # Override cleanup interval for testing
        manager._cleanup_interval = 0.1  # 100ms

        # Create a block
        block = manager.create_live_block("user", "Test content")

        # Wait for cleanup interval
        time.sleep(0.15)

        # Create another block to trigger cleanup check
        block2 = manager.create_live_block("user", "Test content 2")

        # Cleanup should have been triggered
        assert manager._last_cleanup > time.time() - 1.0

    def test_automatic_cleanup(self):
        """Test automatic cleanup of old blocks."""
        manager = OptimizedLiveBlockManager()

        # Create a block and manually set its creation time to be old
        block = manager.create_live_block("user", "Old content")

        # Manually set creation time to be older than 5 minutes
        import datetime

        old_time = datetime.datetime.now() - datetime.timedelta(minutes=6)
        block.created_at = old_time

        initial_live_count = len(manager.get_live_blocks())

        # Trigger cleanup
        manager._perform_cleanup()

        # Block should have been auto-inscribed (removed from live blocks)
        assert len(manager.get_live_blocks()) == initial_live_count - 1


@pytest.mark.asyncio
class TestPerformanceIntegration:
    """Integration tests for performance monitoring."""

    async def test_full_scenario_monitoring(self):
        """Test performance monitoring during full scenario execution."""
        from src.core.mock_scenarios import MockScenarioGenerator

        manager = OptimizedLiveBlockManager()
        generator = MockScenarioGenerator(manager)

        # Record initial state
        initial_status = manager.get_performance_status()
        initial_blocks_created = initial_status["metrics"]["total_blocks_created"]

        # Generate a scenario
        blocks = await generator.generate_scenario("quick_question")

        # Check performance impact
        final_status = manager.get_performance_status()
        final_blocks_created = final_status["metrics"]["total_blocks_created"]

        assert final_blocks_created > initial_blocks_created
        assert final_status["status"] in ["good", "caution", "warning", "critical"]
        assert len(blocks) >= 3  # Should have generated blocks

    async def test_performance_under_load(self):
        """Test performance monitoring under heavy load."""
        manager = OptimizedLiveBlockManager()

        # Create many blocks quickly
        blocks = []
        for i in range(20):
            block = manager.create_live_block(
                "user", f"Content {i}" * 100
            )  # Larger content
            blocks.append(block)

        # Check performance status
        status = manager.get_performance_status()

        assert status["metrics"]["total_blocks_created"] >= 20
        assert status["metrics"]["average_active_blocks"] > 0

        # Memory usage should be tracked
        assert status["metrics"]["average_memory_mb"] > 0

    async def test_optimization_triggers(self):
        """Test that optimizations are triggered under load."""
        manager = OptimizedLiveBlockManager()

        # Lower thresholds to trigger optimizations more easily
        manager.performance_monitor.thresholds["active_blocks"] = 5
        manager.performance_monitor.thresholds["memory_mb"] = 1.0

        # Create blocks to exceed thresholds
        for i in range(10):
            manager.create_live_block("user", "x" * 1000)  # 1KB each

        status = manager.get_performance_status()

        # Should have warnings due to exceeded thresholds
        assert status["warnings"]["total"] > 0

        # Apply optimizations
        optimizations_applied = 0
        for opt in ["memory_cleanup", "throttle_updates"]:
            if manager.performance_monitor.apply_optimization(opt):
                optimizations_applied += 1

        assert optimizations_applied > 0
        assert manager.performance_monitor.counters["optimizations_applied"] > 0
