"""
Animation Clock - Global FPS-based timing system

Provides consistent frame-rate based animation timing across the entire application.
Tests run the same animation code as production, just at higher FPS for speed.
"""

import asyncio
from typing import Optional, Callable


class AnimationClock:
    """Global animation timing controller with configurable FPS."""

    # Fallback values if configuration isn't available
    _DEFAULT_PRODUCTION_FPS = 60
    _DEFAULT_DEVELOPMENT_FPS = 120
    _DEFAULT_TESTING_FPS = 1000

    _fps: int = _DEFAULT_PRODUCTION_FPS
    _frame_duration: float = 1.0 / _DEFAULT_PRODUCTION_FPS
    _last_frame_time: Optional[float] = None
    _config_loaded: bool = False

    # Config-loaded FPS values (set by _load_config_if_needed)
    _production_fps: int = _DEFAULT_PRODUCTION_FPS
    _development_fps: int = _DEFAULT_DEVELOPMENT_FPS
    _testing_fps: int = _DEFAULT_TESTING_FPS

    @classmethod
    def _load_config_if_needed(cls) -> None:
        """Load configuration if not already loaded"""
        if cls._config_loaded:
            return

        try:
            # Try different import paths for flexibility
            try:
                from ..config.enhanced_config import get_config_loader
            except ImportError:
                from src.config.enhanced_config import get_config_loader

            loader = get_config_loader()
            config = loader.config

            # Use configuration values
            cls._production_fps = config.animation.fps.production
            cls._development_fps = config.animation.fps.development
            cls._testing_fps = config.animation.fps.testing
            cls._config_loaded = True
        except (ImportError, Exception):
            # Configuration not available, use defaults
            cls._production_fps = cls._DEFAULT_PRODUCTION_FPS
            cls._development_fps = cls._DEFAULT_DEVELOPMENT_FPS
            cls._testing_fps = cls._DEFAULT_TESTING_FPS
            cls._config_loaded = True

    @classmethod
    def set_fps(cls, fps: int) -> None:
        """Set global animation frame rate.

        Args:
            fps: Frames per second (1-10000)

        Examples:
            AnimationClock.set_fps(60)    # Production: smooth
            AnimationClock.set_fps(120)   # Development: fast feedback
            AnimationClock.set_fps(1000)  # Testing: super fast but real
        """
        if fps < 1 or fps > 10000:
            raise ValueError(f"FPS must be between 1-10000, got {fps}")

        cls._fps = fps
        cls._frame_duration = 1.0 / fps
        cls._last_frame_time = None

    @classmethod
    def get_fps(cls) -> int:
        """Get current FPS setting."""
        return cls._fps

    @classmethod
    def get_frame_duration(cls) -> float:
        """Get duration of one frame in seconds."""
        return cls._frame_duration

    @classmethod
    async def wait_frame(cls) -> None:
        """Wait for one animation frame.

        This is the fundamental animation primitive - all animations
        should be built using this instead of arbitrary sleep() calls.
        """
        await asyncio.sleep(cls._frame_duration)

    @classmethod
    async def wait_frames(cls, count: int) -> None:
        """Wait for multiple animation frames.

        Args:
            count: Number of frames to wait

        Example:
            await AnimationClock.wait_frames(3)  # Wait 3 frames
        """
        if count <= 0:
            return
        await asyncio.sleep(cls._frame_duration * count)

    @classmethod
    async def animate_over_time(cls, duration_seconds: float) -> int:
        """Calculate how many frames are needed for a given duration.

        Args:
            duration_seconds: Desired animation duration

        Returns:
            Number of frames for that duration at current FPS

        Example:
            frames = await AnimationClock.animate_over_time(0.5)  # 0.5 second animation
            # At 60 FPS: 30 frames
            # At 1000 FPS: 500 frames (same animation, just faster)
        """
        return max(1, int(duration_seconds * cls._fps))

    @classmethod
    def set_production_mode(cls) -> None:
        """Set production FPS for smooth user experience."""
        cls._load_config_if_needed()
        cls.set_fps(cls._production_fps)

    @classmethod
    def set_development_mode(cls) -> None:
        """Set development FPS for faster feedback."""
        cls._load_config_if_needed()
        cls.set_fps(cls._development_fps)

    @classmethod
    def set_testing_mode(cls) -> None:
        """Set testing FPS for fast tests that still validate real behavior."""
        cls._load_config_if_needed()
        cls.set_fps(cls._testing_fps)

    @classmethod
    def get_mode_info(cls) -> dict:
        """Get information about current animation mode."""
        cls._load_config_if_needed()

        if cls._fps == cls._production_fps:
            mode = "production"
        elif cls._fps == cls._development_fps:
            mode = "development"
        elif cls._fps == cls._testing_fps:
            mode = "testing"
        else:
            mode = "custom"

        return {
            "mode": mode,
            "fps": cls._fps,
            "frame_duration_ms": cls._frame_duration * 1000,
            "frames_per_second": cls._fps,
        }


# Convenience functions for common animation patterns
async def animate_value_smooth(
    start_value: float,
    end_value: float,
    duration_seconds: float,
    callback: Callable[[float], None],
) -> None:
    """Animate a value smoothly from start to end over given duration.

    Args:
        start_value: Starting value
        end_value: Ending value
        duration_seconds: How long the animation should take
        callback: Function called with each intermediate value

    Example:
        async def update_progress(value):
            progress_bar.set_progress(value)

        # Animate progress from 0 to 1.0 over 2 seconds
        await animate_value_smooth(0.0, 1.0, 2.0, update_progress)
    """
    frames = await AnimationClock.animate_over_time(duration_seconds)
    value_delta = end_value - start_value

    for frame in range(frames + 1):
        progress = frame / frames
        current_value = start_value + (value_delta * progress)
        callback(current_value)

        if frame < frames:  # Don't wait after the last frame
            await AnimationClock.wait_frame()


async def animate_text_typewriter(
    text: str, callback: Callable[[str], None], chars_per_second: float = 50.0
) -> None:
    """Animate text appearing character by character (typewriter effect).

    Uses hybrid timing system:
    - Frame-synchronized: speeds ≤ FPS (smooth, display-synced)
    - Time-synchronized: speeds > FPS (unlimited, precise timing)
    - Instant: speeds > 5000 (no animation)

    Args:
        text: Text to animate
        callback: Function called with each partial string
        chars_per_second: How fast characters should appear

    Example:
        async def update_text(partial_text):
            text_widget.update(partial_text)

        await animate_text_typewriter("Hello World!", update_text, chars_per_second=2000)
    """
    if not text:
        callback("")
        return

    # Ultra-fast mode: instant updates for speeds > 5000 chars/sec
    if chars_per_second > 5000:
        callback(text)
        return

    current_fps = AnimationClock.get_fps()
    seconds_per_char = 1.0 / chars_per_second

    # Choose timing strategy based on speed
    if chars_per_second <= current_fps:
        # Frame-synchronized mode: smooth animation within FPS limits
        frames_per_char = max(
            1, await AnimationClock.animate_over_time(seconds_per_char)
        )

        for i in range(len(text) + 1):
            partial_text = text[:i]
            callback(partial_text)

            if i < len(text):
                await AnimationClock.wait_frames(frames_per_char)

    elif chars_per_second > 2000:
        # Batched mode: update multiple characters per iteration to reduce overhead
        batch_size = max(2, int(chars_per_second / 1000))  # Dynamic batching
        batch_delay = batch_size / chars_per_second

        for i in range(0, len(text) + 1, batch_size):
            end_idx = min(i + batch_size, len(text))
            partial_text = text[:end_idx]
            callback(partial_text)

            if end_idx < len(text):
                await asyncio.sleep(batch_delay)
    else:
        # Time-synchronized mode: character-by-character with precise timing
        for i in range(len(text) + 1):
            partial_text = text[:i]
            callback(partial_text)

            if i < len(text):
                await asyncio.sleep(seconds_per_char)
