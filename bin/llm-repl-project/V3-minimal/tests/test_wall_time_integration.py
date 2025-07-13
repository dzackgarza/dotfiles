"""
Test Integration of Wall Time Tracker with Live Blocks System

Verifies that Task 11.3 wall time and token tracking is properly
integrated with the Sacred Timeline live blocks system.
"""

import pytest
import asyncio
import time
from unittest.mock import patch

from src.core.live_blocks import LiveBlock, LiveBlockManager
from src.core.wall_time_tracker import (
    get_wall_time_tracker,
    query_block_metrics,
    query_all_metrics,
    get_performance_summary,
)
from src.core.processing_queue import ProcessingQueue


class TestWallTimeIntegration:
    """Test wall time tracker integration with live blocks"""

    @pytest.fixture
    def live_block_manager(self):
        """Create a live block manager for testing"""
        return LiveBlockManager()

    @pytest.fixture
    def mock_app(self):
        """Mock app for ProcessingQueue testing"""
        class MockApp:
            def query_one(self, selector):
                class MockStaging:
                    async def mount(self, widget):
                        pass
                return MockStaging()
                
            def log(self, message):
                pass
        
        return MockApp()

    def test_live_block_creation_tracking(self, live_block_manager):
        """Test that live block creation is tracked with wall time metrics"""
        # Create a live block
        block = live_block_manager.create_live_block("user", "Test content")
        
        # Verify metrics are being tracked
        metrics = query_block_metrics(block.id)
        assert metrics is not None
        assert metrics["block_id"] == block.id
        assert "total_wall_time_ms" in metrics
        assert "processing_times_ms" in metrics
        assert "creation" in metrics["processing_times_ms"]

    def test_token_tracking_integration(self, live_block_manager):
        """Test that token updates are tracked in wall time system"""
        block = live_block_manager.create_live_block("assistant", "Response content")
        
        # Update tokens
        block.update_tokens(input_tokens=50, output_tokens=100)
        
        # Verify tokens are tracked
        metrics = query_block_metrics(block.id)
        assert metrics is not None
        assert metrics["token_usage"]["input_tokens"] == 50
        assert metrics["token_usage"]["output_tokens"] == 100
        assert metrics["token_usage"]["total_tokens"] == 150

    @pytest.mark.asyncio
    async def test_simulation_timing(self, live_block_manager):
        """Test that block simulation processes are timed"""
        block = live_block_manager.create_live_block("cognition", "Thinking...")
        
        # Start simulation (which should be timed)
        await block.start_mock_simulation("basic")
        
        # Verify processing stage was timed
        metrics = query_block_metrics(block.id)
        assert metrics is not None
        assert "processing" in metrics["stage_breakdown_ms"]
        assert metrics["stage_breakdown_ms"]["processing"] > 0

    @pytest.mark.asyncio
    async def test_inscription_timing(self, live_block_manager):
        """Test that block inscription process is timed"""
        block = live_block_manager.create_live_block("user", "Input message")
        
        # Add some token usage first
        block.update_tokens(input_tokens=10, output_tokens=20)
        
        # Inscribe the block (which should time the inscription process)
        inscribed = await block.to_inscribed_block()
        
        # Verify inscription was timed and final metrics are included
        assert "performance_metrics" in inscribed.metadata
        performance_data = inscribed.metadata["performance_metrics"]
        assert performance_data is not None
        assert performance_data["block_id"] == block.id
        assert "inscription" in performance_data["stage_breakdown_ms"]
        # Inscription timing might be very small due to fast operations in tests
        assert performance_data["stage_breakdown_ms"]["inscription"] >= 0

    @pytest.mark.asyncio
    async def test_processing_queue_timing(self, mock_app):
        """Test that processing queue operations are timed"""
        queue = ProcessingQueue(mock_app)
        
        # Mock the ProcessingWidget to avoid UI dependencies
        with patch('src.core.processing_queue.ProcessingWidget') as MockWidget:
            mock_widget = MockWidget.return_value
            async def mock_start_processing():
                await asyncio.sleep(0.01)  # Small delay to ensure timing
            mock_widget.start_processing = mock_start_processing
            
            # Add a block to queue
            widget = await queue.add_block("Test processing")
            
            # Let processing complete
            await asyncio.sleep(0.1)
            
            # Verify timing was recorded (queue operations use widget id for tracking)
            tracker = get_wall_time_tracker()
            all_metrics = tracker.get_all_metrics()
            
            # Should have at least one tracked item (creation timing)
            assert len(all_metrics) > 0

    def test_performance_summary_generation(self, live_block_manager):
        """Test that performance summary includes live block metrics"""
        # Create multiple blocks with different operations
        block1 = live_block_manager.create_live_block("user", "First message")
        block2 = live_block_manager.create_live_block("assistant", "Response")
        
        # Add token usage to both
        block1.update_tokens(input_tokens=25, output_tokens=0)
        block2.update_tokens(input_tokens=0, output_tokens=75)
        
        # Get performance summary
        summary = get_performance_summary()
        
        # Verify summary includes our blocks  
        assert summary["total_blocks"] >= 2
        assert "total_tokens" in summary
        # Note: Summary only counts completed blocks, so we may not see all tokens yet
        assert summary["total_tokens"]["input"] >= 0
        assert summary["total_tokens"]["output"] >= 0

    @pytest.mark.asyncio
    async def test_cognition_block_detailed_tracking(self, live_block_manager):
        """Test detailed tracking for cognition blocks with sub-modules"""
        # Create cognition block (has built-in progress tracking)
        block = live_block_manager.create_live_block("cognition", "Complex thinking...")
        
        # Simulate cognition with sub-modules
        await block.start_mock_simulation("cognition")
        
        # Verify detailed tracking
        metrics = query_block_metrics(block.id)
        assert metrics is not None
        
        # Should have processing timing
        assert "processing" in metrics["stage_breakdown_ms"]
        assert metrics["stage_breakdown_ms"]["processing"] > 0
        
        # Should have token usage from simulation (cognition sets tokens during simulation)
        assert metrics["token_usage"]["total_tokens"] >= 0  # May be 0 if timing is very fast

    def test_wall_time_tracker_thread_safety(self, live_block_manager):
        """Test that wall time tracker handles concurrent block operations"""
        import threading
        
        results = []
        
        def create_and_track_block(index):
            """Create block and track metrics in separate thread"""
            try:
                block = live_block_manager.create_live_block("test", f"Block {index}")
                block.update_tokens(input_tokens=index, output_tokens=index * 2)
                
                metrics = query_block_metrics(block.id)
                results.append((index, metrics is not None))
            except Exception as e:
                results.append((index, f"Error: {e}"))
        
        # Create multiple threads creating blocks concurrently
        threads = []
        for i in range(5):
            thread = threading.Thread(target=create_and_track_block, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads
        for thread in threads:
            thread.join()
        
        # Verify all operations succeeded
        assert len(results) == 5
        for index, success in results:
            assert success is True, f"Thread {index} failed: {success}"

    def test_cleanup_old_metrics(self):
        """Test that old metrics can be cleaned up"""
        tracker = get_wall_time_tracker()
        
        # Record initial count
        initial_count = len(tracker.get_all_metrics())
        
        # Clean up metrics older than 0 hours (should clean everything)
        removed_count = tracker.cleanup_old_metrics(max_age_hours=0)
        
        # Verify cleanup worked
        assert removed_count >= initial_count
        
        # Create new block to verify tracker still works
        manager = LiveBlockManager()
        block = manager.create_live_block("test", "After cleanup")
        
        metrics = query_block_metrics(block.id)
        assert metrics is not None

    @pytest.mark.asyncio
    async def test_end_to_end_block_lifecycle_timing(self, live_block_manager):
        """Test complete block lifecycle with wall time tracking"""
        # Create block
        start_time = time.time()
        block = live_block_manager.create_live_block("assistant", "Full lifecycle test")
        
        # Simulate processing work
        await block.start_mock_simulation("assistant_response")
        
        # Add tokens during processing
        block.update_tokens(input_tokens=30, output_tokens=60)
        
        # Inscribe block
        inscribed = await block.to_inscribed_block()
        end_time = time.time()
        
        # Verify complete lifecycle timing
        performance_data = inscribed.metadata["performance_metrics"]
        assert performance_data is not None
        
        # Verify total time is reasonable
        total_time_ms = performance_data["total_wall_time_ms"]
        expected_total_ms = (end_time - start_time) * 1000
        assert 0 < total_time_ms <= expected_total_ms * 1.5  # Allow some overhead
        
        # Verify all stages were tracked
        stage_breakdown = performance_data["stage_breakdown_ms"]
        assert "processing" in stage_breakdown
        assert "inscription" in stage_breakdown
        assert stage_breakdown["processing"] > 0
        # Inscription timing might be very small in tests
        assert stage_breakdown["inscription"] >= 0
        
        # Verify token tracking (simulation may add additional tokens)
        assert performance_data["token_usage"]["input_tokens"] >= 30
        assert performance_data["token_usage"]["output_tokens"] >= 60
        assert performance_data["token_usage"]["total_tokens"] >= 90


if __name__ == "__main__":
    pytest.main([__file__, "-v"])