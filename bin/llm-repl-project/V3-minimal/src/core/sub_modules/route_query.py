"""Route Query sub-module - analyzes user intent."""

import asyncio
import random

from .base import SubModule


class RouteQueryModule(SubModule):
    """Analyzes user query to determine appropriate response strategy."""
    
    def get_initial_content(self) -> str:
        """Get initial content for the live block."""
        return (
            "🎯 **Route Query**\n"
            "└─ Analyzing user intent and determining appropriate response strategy\n\n"
            "**Provider**: Local\n"
            "**Model**: `tinyllama-v2`\n"
            "**Status**: 🔄 Initializing...\n\n"
            "⏱️ 0.0s | [░░░░░░░░░░░░░░░░░░░░] 0% | 🔢 0↑/0↓"
        )
    
    async def execute(self) -> None:
        """Execute route query analysis."""
        # Simulate processing time
        processing_time = random.uniform(0.3, 0.8)
        tokens_in = random.randint(5, 15)
        tokens_out = random.randint(1, 5)
        
        # Start progress tracking
        if self.live_block.cognition_progress:
            self.live_block.notify_step_started()
        
        # Simulate work with internal sleep
        steps = [
            ("Analyzing query semantics...", 0.3),
            ("Detecting intent patterns...", 0.6),
            ("Route determined: CODING", 1.0)
        ]
        
        for step_text, progress in steps:
            # Update content
            self.live_block.stream_content(f"\n → {step_text}")
            
            # Update progress
            if self.live_block.cognition_progress:
                self.live_block.data.progress = progress
                
            # Simulate processing
            await asyncio.sleep(processing_time / len(steps))
        
        # Complete with token counts
        if self.live_block.cognition_progress:
            self.live_block.notify_step_completed(
                tokens_in=tokens_in, 
                tokens_out=tokens_out
            )
            
        # Notify parent we're done
        await self._notify_completion()