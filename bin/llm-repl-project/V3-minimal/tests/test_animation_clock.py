"""
Tests for Animation Clock - FPS-based timing system

Validates that animations work correctly at different frame rates
and that tests can validate real animation behavior.
"""

import pytest
import time
from src.core.animation_clock import (
    AnimationClock,
    animate_text_typewriter,
    animate_value_smooth,
)
from src.core.live_blocks import LiveBlock


class TestAnimationClock:
    """Test the core animation clock functionality."""

    def test_fps_settings(self):
        """Test FPS configuration and mode switching."""
        # Test production mode
        AnimationClock.set_production_mode()
        assert AnimationClock.get_fps() == 60
        assert AnimationClock.get_frame_duration() == pytest.approx(1.0 / 60, rel=1e-6)

        # Test development mode
        AnimationClock.set_development_mode()
        assert AnimationClock.get_fps() == 120
        assert AnimationClock.get_frame_duration() == pytest.approx(1.0 / 120, rel=1e-6)

        # Test testing mode
        AnimationClock.set_testing_mode()
        assert AnimationClock.get_fps() == 1000
        assert AnimationClock.get_frame_duration() == pytest.approx(
            1.0 / 1000, rel=1e-6
        )

        # Test custom FPS
        AnimationClock.set_fps(240)
        assert AnimationClock.get_fps() == 240
        assert AnimationClock.get_frame_duration() == pytest.approx(1.0 / 240, rel=1e-6)

    def test_invalid_fps(self):
        """Test that invalid FPS values are rejected."""
        with pytest.raises(ValueError):
            AnimationClock.set_fps(0)

        with pytest.raises(ValueError):
            AnimationClock.set_fps(-10)

        with pytest.raises(ValueError):
            AnimationClock.set_fps(20000)

    @pytest.mark.asyncio
    async def test_frame_timing(self):
        """Test that frame timing works correctly."""
        AnimationClock.set_fps(100)  # 10ms per frame

        start_time = time.time()
        await AnimationClock.wait_frame()
        elapsed = time.time() - start_time

        # Should take approximately 10ms (allowing for some variance)
        assert 0.005 < elapsed < 0.05, f"Frame took {elapsed}s, expected ~0.01s"

    @pytest.mark.asyncio
    async def test_multiple_frames(self):
        """Test waiting for multiple frames."""
        AnimationClock.set_fps(200)  # 5ms per frame

        start_time = time.time()
        await AnimationClock.wait_frames(4)
        elapsed = time.time() - start_time

        # Should take approximately 20ms (4 * 5ms)
        assert 0.010 < elapsed < 0.050, f"4 frames took {elapsed}s, expected ~0.02s"

    @pytest.mark.asyncio
    async def test_animate_over_time_calculation(self):
        """Test that duration-to-frames calculation works correctly."""
        AnimationClock.set_fps(60)
        frames = await AnimationClock.animate_over_time(0.5)  # 0.5 seconds
        assert frames == 30  # 60 FPS * 0.5s = 30 frames

        AnimationClock.set_fps(1000)
        frames = await AnimationClock.animate_over_time(0.1)  # 0.1 seconds
        assert frames == 100  # 1000 FPS * 0.1s = 100 frames


class TestFrameBasedAnimations:
    """Test that frame-based animations work at different FPS."""

    def setup_method(self):
        """Set high FPS for fast testing."""
        AnimationClock.set_testing_mode()

    @pytest.mark.asyncio
    async def test_typewriter_animation_frame_accuracy(self):
        """Test typewriter animation produces correct frame sequence."""
        updates = []

        def capture_update(text):
            updates.append(text)

        # Animate "Hi" at known speed
        await animate_text_typewriter("Hi", capture_update, chars_per_second=1000)

        # Should have updates for each character: "", "H", "Hi"
        assert len(updates) == 3, f"Expected 3 updates, got {len(updates)}: {updates}"
        assert updates[0] == ""
        assert updates[1] == "H"
        assert updates[2] == "Hi"

    @pytest.mark.asyncio
    async def test_value_animation_frame_accuracy(self):
        """Test smooth value animation produces correct progression."""
        updates = []

        def capture_update(value):
            updates.append(value)

        # Animate from 0 to 10 over short duration
        await animate_value_smooth(0.0, 10.0, 0.01, capture_update)  # Very fast

        # Should have multiple updates with smooth progression
        assert len(updates) > 1, f"Expected multiple updates, got {len(updates)}"
        assert updates[0] == 0.0, "Should start at 0.0"
        assert updates[-1] == 10.0, "Should end at 10.0"

        # Verify smooth progression (values should generally increase)
        for i in range(1, len(updates)):
            assert (
                updates[i] >= updates[i - 1]
            ), f"Value should not decrease: {updates[i-1]} -> {updates[i]}"

    @pytest.mark.asyncio
    async def test_fps_affects_animation_granularity(self):
        """Test that higher FPS produces more granular animations."""
        # Test at low FPS
        AnimationClock.set_fps(10)  # 10 FPS
        updates_low_fps = []

        def capture_low_fps(value):
            updates_low_fps.append(value)

        await animate_value_smooth(0.0, 100.0, 0.1, capture_low_fps)

        # Test at high FPS
        AnimationClock.set_fps(1000)  # 1000 FPS
        updates_high_fps = []

        def capture_high_fps(value):
            updates_high_fps.append(value)

        await animate_value_smooth(0.0, 100.0, 0.1, capture_high_fps)

        # High FPS should produce more granular updates
        assert len(updates_high_fps) > len(
            updates_low_fps
        ), f"High FPS ({len(updates_high_fps)}) should have more updates than low FPS ({len(updates_low_fps)})"


class TestLiveBlockFrameBasedAnimations:
    """Test that LiveBlock animations work correctly with frame-based timing."""

    def setup_method(self):
        """Set high FPS for fast testing."""
        AnimationClock.set_testing_mode()

    @pytest.mark.asyncio
    async def test_live_block_content_streaming_frames(self):
        """Test that LiveBlock content streaming produces frame-accurate results."""
        block = LiveBlock("test")
        content_updates = []

        def capture_content(b):
            content_updates.append(b.data.content)

        block.add_update_callback(capture_content)

        # Stream content with animation
        await block.stream_content_animated("ABC", chars_per_second=1000)

        # Should have character-by-character progression
        assert (
            len(content_updates) >= 4
        ), f"Expected at least 4 updates, got {len(content_updates)}"

        # Should include each step: "", "A", "AB", "ABC"
        content_sequence = content_updates
        assert "" in content_sequence
        assert "A" in content_sequence
        assert "AB" in content_sequence
        assert "ABC" in content_sequence
        assert content_sequence[-1] == "ABC"

    @pytest.mark.asyncio
    async def test_live_block_token_animation_frames(self):
        """Test that LiveBlock token animation produces smooth progression."""
        block = LiveBlock("test")
        token_updates = []

        def capture_tokens(b):
            token_updates.append((b.data.tokens_input, b.data.tokens_output))

        block.add_update_callback(capture_tokens)

        # Animate tokens from (0,0) to (20,30)
        await block.animate_tokens(20, 30, duration_seconds=0.02)

        # Should have smooth progression
        assert (
            len(token_updates) > 1
        ), f"Expected multiple updates, got {len(token_updates)}"

        first_input, first_output = token_updates[0]
        last_input, last_output = token_updates[-1]

        assert (first_input, first_output) == (0, 0), "Should start at (0,0)"
        assert (last_input, last_output) == (
            20,
            30,
        ), f"Should end at (20,30), got {(last_input, last_output)}"

        # Verify monotonic progression
        for i in range(1, len(token_updates)):
            prev_input, prev_output = token_updates[i - 1]
            curr_input, curr_output = token_updates[i]
            assert curr_input >= prev_input, "Input tokens should not decrease"
            assert curr_output >= prev_output, "Output tokens should not decrease"

    @pytest.mark.asyncio
    async def test_live_block_progress_animation_frames(self):
        """Test that LiveBlock progress animation produces smooth progression."""
        block = LiveBlock("test")
        progress_updates = []

        def capture_progress(b):
            progress_updates.append(b.data.progress)

        block.add_update_callback(capture_progress)

        # Animate progress from 0.0 to 1.0
        await block.animate_progress(1.0, duration_seconds=0.02)

        # Should have smooth progression
        assert (
            len(progress_updates) > 1
        ), f"Expected multiple updates, got {len(progress_updates)}"

        first_progress = progress_updates[0]
        last_progress = progress_updates[-1]

        assert first_progress <= 0.1, f"Should start near 0.0, got {first_progress}"
        assert (
            abs(last_progress - 1.0) < 0.01
        ), f"Should end at 1.0, got {last_progress}"

        # Verify monotonic progression
        for i in range(1, len(progress_updates)):
            prev_progress = progress_updates[i - 1]
            curr_progress = progress_updates[i]
            assert (
                curr_progress >= prev_progress - 0.01
            ), f"Progress should not decrease significantly: {prev_progress} -> {curr_progress}"


class TestAnimationClockModes:
    """Test animation clock mode information and switching."""

    def test_mode_info(self):
        """Test that mode information is accurate."""
        AnimationClock.set_production_mode()
        info = AnimationClock.get_mode_info()
        assert info["mode"] == "production"
        assert info["fps"] == 60
        assert info["frame_duration_ms"] == pytest.approx(16.67, rel=1e-2)

        AnimationClock.set_development_mode()
        info = AnimationClock.get_mode_info()
        assert info["mode"] == "development"
        assert info["fps"] == 120

        AnimationClock.set_testing_mode()
        info = AnimationClock.get_mode_info()
        assert info["mode"] == "testing"
        assert info["fps"] == 1000

        AnimationClock.set_fps(333)
        info = AnimationClock.get_mode_info()
        assert info["mode"] == "custom"
        assert info["fps"] == 333

    def teardown_method(self):
        """Reset to testing mode after each test."""
        AnimationClock.set_testing_mode()
