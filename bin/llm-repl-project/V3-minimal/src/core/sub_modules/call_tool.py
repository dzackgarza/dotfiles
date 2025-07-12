"""Call Tool sub-module - executes tool calls."""

import asyncio
import random

from .base import SubModule


class CallToolModule(SubModule):
    """Executes tool calls like web search or code analysis."""
    
    def get_initial_content(self) -> str:
        """Get initial content for the live block."""
        return (
            "🛠️ **Call Tool**\n"
            "└─ Executing web search to gather relevant information\n\n"
            "**Provider**: Brave\n"
            "**Model**: `brave_web_search`\n"
            "**Status**: 🔄 Initializing...\n\n"
            "⏱️ 0.0s | [░░░░░░░░░░░░░░░░░░░░] 0% | 🔢 0↑/0↓"
        )
    
    async def execute(self) -> None:
        """Execute tool call."""
        # Simulate longer processing time for tool calls
        processing_time = random.uniform(1.5, 3.0)
        tokens_in = random.randint(10, 20)
        tokens_out = random.randint(1000, 1500)
        
        # Start progress tracking
        if self.live_block.cognition_progress:
            self.live_block.notify_step_started()
        
        # Simulate work with internal sleep
        steps = [
            ("Scanning available tools...", 0.2),
            ("Evaluating tool compatibility...", 0.5),
            ("Executing web search...", 0.7),
            ("Processing search results...", 0.9),
            ("Tool execution complete", 1.0)
        ]
        
        for step_text, progress in steps:
            # Update content
            self.live_block.stream_content(f"\n → {step_text}")
            
            # Update progress
            if self.live_block.cognition_progress:
                self.live_block.data.progress = progress
                
            # Simulate processing
            await asyncio.sleep(processing_time / len(steps))
        
        # Add some mock results
        self.live_block.stream_content(
            "\n\nResults found:\n"
            "• Python async/await patterns - 15 matches\n"
            "• Textual UI framework docs - 8 matches\n"
            "• Live streaming implementations - 12 matches"
        )
        
        # Complete with token counts
        if self.live_block.cognition_progress:
            self.live_block.notify_step_completed(
                tokens_in=tokens_in, 
                tokens_out=tokens_out
            )
            
        # Notify parent we're done
        await self._notify_completion()