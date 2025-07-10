"""
Scrivener V2: The authoritative record keeper for all blocks.

The Scrivener maintains:
1. The exact order of all blocks as they were created
2. The visual display state of each block
3. The historical record that matches the visual display
"""

import asyncio
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from blocks import (
    Block, BlockRegistry, BlockSequence, BlockType,
    UserBlock, SystemCheckBlock, WelcomeBlock,
    InternalProcessingBlock, ProcessingSubBlock,
    AssistantBlock
)


class DisplayInterface:
    """Interface for rendering blocks to the display."""
    
    async def render_block(self, block: Block) -> None:
        """Render a block to the display."""
        raise NotImplementedError
    
    async def update_block(self, block: Block) -> None:
        """Update an existing block's display."""
        raise NotImplementedError
    
    async def clear_display(self) -> None:
        """Clear the display."""
        raise NotImplementedError


class ScrivenerV2:
    """
    The Scrivener is the source of truth for:
    1. What blocks exist
    2. What order they were created in
    3. What state each block is in
    4. What was displayed to the user
    
    The visual display MUST match the Scrivener's record exactly.
    """
    
    def __init__(self, display: DisplayInterface):
        self.display = display
        self.registry = BlockRegistry()
        self.active_blocks: Dict[str, Block] = {}
        self._event_queue: asyncio.Queue = asyncio.Queue()
        self._running = False
        self._task: Optional[asyncio.Task] = None
    
    async def start(self) -> None:
        """Start the Scrivener event loop."""
        self._running = True
        self._task = asyncio.create_task(self._process_events())
        # Start a new sequence for this session
        self.registry.start_new_sequence()
    
    async def stop(self) -> None:
        """Stop the Scrivener event loop."""
        self._running = False
        if self._task:
            await self._event_queue.put(None)  # Sentinel to stop loop
            await self._task
    
    async def _process_events(self) -> None:
        """Process events from the queue."""
        while self._running:
            try:
                event = await self._event_queue.get()
                if event is None:  # Sentinel
                    break
                await self._handle_event(event)
            except Exception as e:
                print(f"Error processing event: {e}")
    
    async def _handle_event(self, event: Dict[str, Any]) -> None:
        """Handle a single event."""
        event_type = event.get("type")
        block = event.get("block")
        
        if event_type == "create":
            await self._handle_create(block)
        elif event_type == "start":
            await self._handle_start(block)
        elif event_type == "update":
            await self._handle_update(block)
        elif event_type == "complete":
            await self._handle_complete(block)
    
    async def _handle_create(self, block: Block) -> None:
        """Handle block creation."""
        self.registry.register_block(block)
        self.active_blocks[block.id] = block
        await self.display.render_block(block)
    
    async def _handle_start(self, block: Block) -> None:
        """Handle block start."""
        block.start()
        await self.display.update_block(block)
    
    async def _handle_update(self, block: Block) -> None:
        """Handle block update."""
        await self.display.update_block(block)
    
    async def _handle_complete(self, block: Block) -> None:
        """Handle block completion."""
        block.complete()
        await self.display.update_block(block)
        # Remove from active blocks
        self.active_blocks.pop(block.id, None)
    
    # High-level block creation methods
    
    async def create_system_check(self) -> SystemCheckBlock:
        """Create and register a system check block."""
        block = SystemCheckBlock()
        await self._event_queue.put({"type": "create", "block": block})
        await self._event_queue.put({"type": "start", "block": block})
        return block
    
    async def complete_system_check(self, system_check: SystemCheckBlock) -> None:
        """Complete a system check block."""
        await self._event_queue.put({"type": "complete", "block": system_check})
    
    async def create_welcome(self, version: str = "v2") -> WelcomeBlock:
        """Create and register a welcome block."""
        block = WelcomeBlock(version)
        await self._event_queue.put({"type": "create", "block": block})
        await self._event_queue.put({"type": "start", "block": block})
        await self._event_queue.put({"type": "complete", "block": block})
        return block
    
    async def create_user_input(self, user_input: str) -> UserBlock:
        """Create and register a user input block."""
        block = UserBlock(user_input)
        await self._event_queue.put({"type": "create", "block": block})
        await self._event_queue.put({"type": "start", "block": block})
        await self._event_queue.put({"type": "complete", "block": block})
        return block
    
    async def create_internal_processing(self) -> InternalProcessingBlock:
        """Create and register an internal processing block."""
        block = InternalProcessingBlock()
        await self._event_queue.put({"type": "create", "block": block})
        await self._event_queue.put({"type": "start", "block": block})
        return block
    
    async def add_processing_step(self, 
                                  processing_block: InternalProcessingBlock,
                                  title: str, 
                                  methodology: str) -> ProcessingSubBlock:
        """Add a processing step to an internal processing block."""
        sub_block = ProcessingSubBlock(title, methodology)
        processing_block.add_sub_block(sub_block)
        self.registry.register_block(sub_block)
        await self._event_queue.put({"type": "update", "block": processing_block})
        return sub_block
    
    async def start_processing_step(self, 
                                    processing_block: InternalProcessingBlock,
                                    sub_block_index: int) -> ProcessingSubBlock:
        """Start a specific processing step."""
        sub_block = processing_block.start_sub_block(sub_block_index)
        await self._event_queue.put({"type": "update", "block": processing_block})
        return sub_block
    
    async def complete_processing_step(self,
                                       processing_block: InternalProcessingBlock,
                                       sub_block_index: int,
                                       result: str,
                                       tokens_sent: int,
                                       tokens_received: int,
                                       routing_conclusion: Optional[str] = None) -> None:
        """Complete a processing step with results."""
        sub_block = processing_block.sub_blocks[sub_block_index]
        sub_block.set_result(result, tokens_sent, tokens_received, routing_conclusion)
        processing_block.complete_sub_block(sub_block_index)
        await self._event_queue.put({"type": "update", "block": processing_block})
    
    async def complete_internal_processing(self, 
                                           processing_block: InternalProcessingBlock) -> None:
        """Complete the entire internal processing block."""
        await self._event_queue.put({"type": "complete", "block": processing_block})
    
    async def create_assistant_response(self, 
                                        response: str, 
                                        routing_info: Optional[str] = None) -> AssistantBlock:
        """Create and register an assistant response block."""
        block = AssistantBlock(response, routing_info)
        await self._event_queue.put({"type": "create", "block": block})
        await self._event_queue.put({"type": "start", "block": block})
        await self._event_queue.put({"type": "complete", "block": block})
        return block
    
    # Validation and querying methods
    
    def get_current_sequence(self) -> Optional[BlockSequence]:
        """Get the current block sequence."""
        return self.registry.get_current_sequence()
    
    def validate_sequence(self, query_type: str = "default") -> bool:
        """Validate the current block sequence."""
        return self.registry.validate_current_sequence(query_type)
    
    def get_validation_report(self, query_type: str = "default") -> Dict[str, Any]:
        """Get a detailed validation report."""
        return self.registry.get_validation_report(query_type)
    
    def get_block_history(self) -> List[Dict[str, Any]]:
        """Get the complete block history."""
        sequence = self.get_current_sequence()
        if sequence:
            return sequence.to_history()
        return []
    
    def get_display_state(self) -> List[Dict[str, Any]]:
        """Get the current display state."""
        sequence = self.get_current_sequence()
        if sequence:
            return sequence.to_display_list()
        return []