"""Async input processing with real live block updates"""

import asyncio
from typing import TYPE_CHECKING, TypedDict
from datetime import datetime
import random

from ..sacred_timeline import SubBlock
from .live_blocks import LiveBlockManager

if TYPE_CHECKING:
    from ..sacred_timeline import SacredTimeline
    from .response_generator import ResponseGenerator
    from textual.app import App


class SubModuleData(TypedDict):
    name: str
    icon: str
    model: str
    time: float
    tokens_in: int
    tokens_out: int


class AsyncInputProcessor:
    """Async version that shows real live updates"""
    
    def __init__(
        self, 
        timeline: "SacredTimeline", 
        response_generator: "ResponseGenerator",
        app: "App" = None
    ):
        self.timeline = timeline
        self.response_generator = response_generator
        self.live_block_manager = LiveBlockManager()
        self.app = app
        
    async def process_user_input_async(self, user_input: str) -> None:
        """Process user input with real async updates"""
        user_input = user_input.strip()
        if not user_input:
            return
            
        # Add user message immediately
        self.timeline.add_block(role="user", content=user_input)
        
        # Start cognition processing with live updates
        await self._add_cognition_block_async(user_input)
        
        # Generate assistant response after cognition completes
        response = self.response_generator.generate_response(user_input)
        self.timeline.add_block(role="assistant", content=response)
        
    async def _add_cognition_block_async(self, user_input: str) -> None:
        """Add cognition block with real async updates"""
        
        # Create live block and notify observers immediately
        live_block = self.live_block_manager.create_live_block(
            role="cognition",
            initial_content="**Cognition Pipeline** starting...\n\n⏳ Initializing..."
        )
        
        # Notify observers about the new live block
        for observer in self.timeline._observers:
            if hasattr(observer, "on_live_block_update"):
                observer.on_live_block_update(live_block)
        
        # Register update callback
        def notify_update(block):
            for observer in self.timeline._observers:
                if hasattr(observer, "on_live_block_update"):
                    observer.on_live_block_update(block)
        
        live_block.add_update_callback(notify_update)
        
        # Define sub-modules
        sub_modules_data: list[SubModuleData] = [
            {
                "name": "Route query",
                "icon": "🧠",
                "model": "tinyllama-v2",
                "time": random.uniform(0.3, 0.8),
                "tokens_in": random.randint(5, 15),
                "tokens_out": random.randint(1, 5),
            },
            {
                "name": "Call tool",
                "icon": "🛠️",
                "model": "brave_web_search",
                "time": random.uniform(1.5, 3.0),
                "tokens_in": random.randint(10, 20),
                "tokens_out": random.randint(1000, 1500),
            },
            {
                "name": "Format output",
                "icon": "🤖",
                "model": "mistral-7b-instruct",
                "time": random.uniform(0.8, 1.5),
                "tokens_in": random.randint(400, 600),
                "tokens_out": random.randint(200, 300),
            },
        ]
        
        total_time = 0.0
        total_tokens_in = 0
        total_tokens_out = 0
        
        # Process each sub-module with real delays
        for i, sub_module in enumerate(sub_modules_data):
            # Update main block to show current step
            main_content = (
                f"**Cognition Pipeline** in progress...\n\n"
                f"⏳ Step {i + 1}/{len(sub_modules_data)}: {sub_module['icon']} {sub_module['name']}\n"
                f"📊 Progress: {'█' * (i * 3)}{'░' * ((3 - i) * 3)}\n"
                f"🔢 Tokens so far: {total_tokens_in}↑ / {total_tokens_out}↓"
            )
            live_block.update_content(main_content)
            
            # Create sub-block that starts in processing state
            sub_content = f"Model: `{sub_module['model']}`\nStatus: ⏳ Processing..."
            sub_live_block = self.live_block_manager.create_live_block(
                role=sub_module["name"].lower().replace(" ", "_"),
                initial_content=sub_content
            )
            
            # Add sub-block and update progress
            live_block.add_sub_block(sub_live_block)
            progress = (i + 0.5) / len(sub_modules_data)
            live_block.update_progress(progress)
            
            # Simulate processing with real delay
            await asyncio.sleep(sub_module["time"])
            
            # Update sub-block to complete
            sub_live_block.update_content(
                f"Model: `{sub_module['model']}`\nStatus: ✅ Complete"
            )
            
            # Update totals
            total_time += sub_module["time"]
            total_tokens_in += sub_module["tokens_in"]
            total_tokens_out += sub_module["tokens_out"]
            
            # Update tokens on main block
            live_block.update_tokens(sub_module["tokens_in"], sub_module["tokens_out"])
            
            # Update progress
            progress = (i + 1) / len(sub_modules_data)
            live_block.update_progress(progress)
            
            # Small delay between steps
            await asyncio.sleep(0.1)
        
        # Final summary
        main_cognition_content = (
            f"**Cognition Pipeline** completed in {total_time:.1f}s\n\n"
            f"📊 **Summary**: {len(sub_modules_data)} modules executed\n"
            f"🔢 **Total Tokens**: {total_tokens_in}↑ / {total_tokens_out}↓\n"
            f"⚡ **Pipeline**: Route → Tool → Format"
        )
        live_block.update_content(main_cognition_content)
        live_block.data.wall_time_seconds = total_time
        
        # Small delay before inscribing
        await asyncio.sleep(0.2)
        
        # Inscribe the block
        inscribed_block = self.live_block_manager.inscribe_block(live_block.id)
        
        if inscribed_block:
            # Inscribe sub-blocks first
            for sub_block in live_block.data.sub_blocks:
                self.live_block_manager.inscribe_block(sub_block.id)
            
            # Add to timeline
            self.timeline.add_block(
                role=inscribed_block.role,
                content=inscribed_block.content,
                metadata=inscribed_block.metadata,
                time_taken=inscribed_block.metadata.get("wall_time_seconds", total_time),
                tokens_input=inscribed_block.metadata.get("tokens_input", 0),
                tokens_output=inscribed_block.metadata.get("tokens_output", 0),
                sub_blocks=[
                    SubBlock(
                        type=sb.get("role", "unknown"),
                        content=sb.get("data", {}).get("content", ""),
                    )
                    for sb in inscribed_block.metadata.get("sub_blocks", [])
                ],
            )