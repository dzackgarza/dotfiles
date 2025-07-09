#!/usr/bin/env python3
"""
Enhanced Animation System for Token Counting

Key principles:
1. NEVER show estimated tokens - only show actual API response data
2. Use smooth curves with continuous derivatives 
3. Handle early completion gracefully without snapping
4. Provide realistic timing based on empirical measurements
"""

import time
import math
from typing import Tuple, Optional, Callable
from dataclasses import dataclass

@dataclass
class AnimationKeyframe:
    """A keyframe in the animation timeline."""
    timestamp: float
    input_tokens: int
    output_tokens: int

class SmoothAnimationCurve:
    """
    Smooth animation curves using cubic Bezier functions.
    Provides continuous derivatives for natural motion.
    """
    
    @staticmethod
    def cubic_bezier(t: float, p0: float, p1: float, p2: float, p3: float) -> float:
        """Cubic Bezier curve with control points p0, p1, p2, p3."""
        return (1-t)**3 * p0 + 3*(1-t)**2*t * p1 + 3*(1-t)*t**2 * p2 + t**3 * p3
    
    @staticmethod
    def ease_in_out_cubic(t: float) -> float:
        """Smooth ease-in-out curve with continuous derivatives."""
        return 3*t**2 - 2*t**3
    
    @staticmethod
    def ease_out_exponential(t: float, steepness: float = 3.0) -> float:
        """Exponential ease-out for rapid initial progress, then slowdown."""
        return 1 - math.exp(-steepness * t)
    
    @staticmethod
    def sigmoid_curve(t: float, midpoint: float = 0.5, steepness: float = 10.0) -> float:
        """S-curve for gradual start, rapid middle, gradual end."""
        shifted = steepness * (t - midpoint)
        return 1 / (1 + math.exp(-shifted))

class ActualTokenAnimator:
    """
    Animation system that ONLY shows actual token counts from API responses.
    Never displays estimates - waits for real data.
    """
    
    def __init__(self):
        self.keyframes: list[AnimationKeyframe] = []
        self.start_time: Optional[float] = None
        self.current_input = 0
        self.current_output = 0
        self.animation_style = "smooth_ramp"  # smooth_ramp, bezier, sigmoid
        
    def start_animation(self, initial_timestamp: Optional[float] = None):
        """Start the animation timeline."""
        self.start_time = initial_timestamp or time.time()
        self.keyframes = []
        self.current_input = 0
        self.current_output = 0
        
        # Add initial keyframe (no tokens yet)
        self.add_keyframe(0, 0)
    
    def add_keyframe(self, input_tokens: int, output_tokens: int, timestamp: Optional[float] = None):
        """Add a keyframe with ACTUAL token data from API response."""
        if self.start_time is None:
            self.start_animation()
            
        current_time = timestamp or time.time()
        elapsed = current_time - self.start_time
        
        keyframe = AnimationKeyframe(
            timestamp=elapsed,
            input_tokens=input_tokens,
            output_tokens=output_tokens
        )
        
        self.keyframes.append(keyframe)
        
        # Sort keyframes by timestamp to handle out-of-order updates
        self.keyframes.sort(key=lambda k: k.timestamp)
    
    def get_current_animated_values(self, current_time: Optional[float] = None) -> Tuple[int, int]:
        """
        Get current animated token values based on actual keyframes.
        Uses smooth interpolation between known data points.
        """
        if not self.keyframes or self.start_time is None:
            return 0, 0
            
        current_time = current_time or time.time()
        elapsed = current_time - self.start_time
        
        # If before first keyframe, show zeros
        if elapsed <= self.keyframes[0].timestamp:
            return 0, 0
        
        # If after last keyframe, show final values
        if elapsed >= self.keyframes[-1].timestamp:
            final = self.keyframes[-1]
            return final.input_tokens, final.output_tokens
        
        # Find the two keyframes to interpolate between
        prev_keyframe = self.keyframes[0]
        next_keyframe = self.keyframes[-1]
        
        for i, keyframe in enumerate(self.keyframes):
            if keyframe.timestamp <= elapsed:
                prev_keyframe = keyframe
                if i + 1 < len(self.keyframes):
                    next_keyframe = self.keyframes[i + 1]
            else:
                break
        
        # If we're exactly on a keyframe, return its values
        if prev_keyframe.timestamp == elapsed:
            return prev_keyframe.input_tokens, prev_keyframe.output_tokens
        
        # Interpolate between prev and next keyframes
        if prev_keyframe.timestamp == next_keyframe.timestamp:
            return next_keyframe.input_tokens, next_keyframe.output_tokens
        
        # Calculate interpolation factor
        duration = next_keyframe.timestamp - prev_keyframe.timestamp
        progress = (elapsed - prev_keyframe.timestamp) / duration
        
        # Apply smooth animation curve
        if self.animation_style == "bezier":
            smooth_progress = SmoothAnimationCurve.cubic_bezier(progress, 0, 0.25, 0.75, 1)
        elif self.animation_style == "sigmoid":
            smooth_progress = SmoothAnimationCurve.sigmoid_curve(progress)
        else:  # smooth_ramp
            smooth_progress = SmoothAnimationCurve.ease_in_out_cubic(progress)
        
        # Interpolate token values
        input_diff = next_keyframe.input_tokens - prev_keyframe.input_tokens
        output_diff = next_keyframe.output_tokens - prev_keyframe.output_tokens
        
        animated_input = prev_keyframe.input_tokens + int(smooth_progress * input_diff)
        animated_output = prev_keyframe.output_tokens + int(smooth_progress * output_diff)
        
        return animated_input, animated_output
    
    def set_animation_style(self, style: str):
        """Set the animation curve style."""
        valid_styles = ["smooth_ramp", "bezier", "sigmoid"]
        if style in valid_styles:
            self.animation_style = style
    
    def get_animation_progress(self) -> float:
        """Get overall animation progress (0.0 to 1.0)."""
        if not self.keyframes or self.start_time is None:
            return 0.0
            
        current_time = time.time()
        elapsed = current_time - self.start_time
        
        if not self.keyframes:
            return 0.0
        
        total_duration = self.keyframes[-1].timestamp
        if total_duration <= 0:
            return 1.0
            
        return min(1.0, elapsed / total_duration)
    
    def is_complete(self) -> bool:
        """Check if animation has reached final keyframe."""
        if not self.keyframes or self.start_time is None:
            return False
            
        current_time = time.time()
        elapsed = current_time - self.start_time
        
        return elapsed >= self.keyframes[-1].timestamp

class RealtimeTokenTracker:
    """
    Real-time token tracking system that works with actual API responses.
    Handles the complete lifecycle from request start to completion.
    """
    
    def __init__(self):
        self.animator = ActualTokenAnimator()
        self.request_start_time: Optional[float] = None
        self.is_active = False
        
    def start_request(self):
        """Start tracking a new request."""
        self.request_start_time = time.time()
        self.is_active = True
        self.animator.start_animation(self.request_start_time)
        
        # Add initial state - no tokens processed yet
        self.animator.add_keyframe(0, 0, self.request_start_time)
    
    def update_with_api_response(self, input_tokens: int, output_tokens: int, 
                               response_timestamp: Optional[float] = None):
        """
        Update with ACTUAL token counts from API response.
        This is the ONLY way tokens get updated - no estimates.
        """
        if not self.is_active:
            return
            
        timestamp = response_timestamp or time.time()
        self.animator.add_keyframe(input_tokens, output_tokens, timestamp)
    
    def complete_request(self, final_input_tokens: int, final_output_tokens: int):
        """Mark request as complete with final token counts."""
        if not self.is_active:
            return
            
        final_timestamp = time.time()
        self.animator.add_keyframe(final_input_tokens, final_output_tokens, final_timestamp)
        self.is_active = False
    
    def get_display_values(self) -> Tuple[int, int]:
        """Get current token values for display."""
        if not self.is_active:
            # If not active, show final values if available
            if self.animator.keyframes:
                final = self.animator.keyframes[-1]
                return final.input_tokens, final.output_tokens
            return 0, 0
            
        return self.animator.get_current_animated_values()
    
    def get_status(self) -> dict:
        """Get detailed status for debugging."""
        input_tokens, output_tokens = self.get_display_values()
        
        return {
            'is_active': self.is_active,
            'current_input_tokens': input_tokens,
            'current_output_tokens': output_tokens,
            'total_tokens': input_tokens + output_tokens,
            'animation_progress': self.animator.get_animation_progress(),
            'keyframes_count': len(self.animator.keyframes),
            'is_complete': self.animator.is_complete(),
            'elapsed_time': time.time() - self.request_start_time if self.request_start_time else 0
        }

# Example usage and testing
if __name__ == "__main__":
    import asyncio
    
    async def demo_animation():
        """Demonstrate the animation system."""
        print("🎬 Enhanced Token Animation Demo")
        print("=" * 40)
        
        tracker = RealtimeTokenTracker()
        
        # Start a request
        print("📤 Starting request...")
        tracker.start_request()
        
        # Simulate API responses arriving over time
        await asyncio.sleep(0.5)
        print("📡 Input processing complete...")
        tracker.update_with_api_response(45, 0)  # Input tokens processed
        
        await asyncio.sleep(1.0)
        print("🧠 Generating response...")
        tracker.update_with_api_response(45, 20)  # Some output generated
        
        await asyncio.sleep(1.5)
        print("📝 More content...")
        tracker.update_with_api_response(45, 85)  # More output
        
        await asyncio.sleep(0.8)
        print("✅ Request complete!")
        tracker.complete_request(45, 120)  # Final counts
        
        # Show animation in action
        print("\n🎭 Animation playback:")
        demo_start = time.time()
        
        while time.time() - demo_start < 3.0:
            input_tokens, output_tokens = tracker.get_display_values()
            status = tracker.get_status()
            
            print(f"\r⏱️ ↑{input_tokens:3d} ↓{output_tokens:3d} | "
                  f"Progress: {status['animation_progress']:.1%} | "
                  f"Elapsed: {status['elapsed_time']:.1f}s", end="")
            
            await asyncio.sleep(0.1)
        
        print("\n✨ Animation complete!")
    
    # Run demo
    asyncio.run(demo_animation())