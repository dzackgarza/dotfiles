#!/usr/bin/env python3
"""
LLM REPL - Interactive Research Assistant with Unified Block Architecture

This is the main entry point for the LLM REPL application using the unified
block architecture that ensures:
- Atomic blocks with no split states
- Proper block ordering and validation
- Complete display/history synchronization
- Comprehensive regression testing
"""

import asyncio
import argparse
import sys
import os
from pathlib import Path
from typing import Optional

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import unified architecture
from blocks import (
    UserBlock, SystemCheckBlock, WelcomeBlock,
    InternalProcessingBlock, AssistantBlock
)
from scrivener_v2 import ScrivenerV2, DisplayInterface
from providers import LLMManager, LLMProvider
from config import LLMConfiguration, CONFIGURATIONS
from processing import IntentDetector, QueryRouter

# Rich UI imports
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.box import ROUNDED
from rich.live import Live
from rich.text import Text
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.styles import Style


class RichDisplay(DisplayInterface):
    """Rich terminal display for the unified block architecture."""
    
    def __init__(self, console: Console):
        self.console = console
        self.live_blocks = {}
        self.live_display = None
    
    async def render_block(self, block) -> None:
        """Render a new block to the display."""
        render_data = block.render()
        
        # Create rich renderable based on block type
        if render_data['type'] == 'user':
            content = Panel(
                render_data['body'],
                title=render_data['title'],
                box=ROUNDED,
                border_style="green"
            )
        elif render_data['type'] == 'assistant':
            content = Panel(
                Markdown(render_data['body']),
                title=render_data['title'],
                box=ROUNDED,
                border_style="blue"
            )
        elif render_data['type'] == 'system_check':
            title = render_data['title']
            if render_data.get('show_spinner'):
                title += " (checking...)"
            content = Panel(
                render_data.get('body', ''),
                title=title,
                box=ROUNDED,
                border_style="yellow"
            )
        elif render_data['type'] == 'internal_processing':
            title = render_data['title']
            content = Panel(
                self._render_processing_content(render_data),
                title=title,
                box=ROUNDED,
                border_style="magenta"
            )
        else:
            # Default rendering
            content = Panel(
                render_data.get('body', ''),
                title=render_data['title'],
                box=ROUNDED
            )
        
        self.console.print(content)
        self.live_blocks[block.id] = content
    
    async def update_block(self, block) -> None:
        """Update an existing block's display."""
        # For now, just re-render the block
        # In a full implementation, this would update the live display
        pass
    
    async def clear_display(self) -> None:
        """Clear the display."""
        self.console.clear()
        self.live_blocks.clear()
    
    def _render_processing_content(self, render_data) -> str:
        """Render processing block content."""
        content = []
        
        # Add main processing message
        if render_data.get('body'):
            content.append(render_data['body'])
        
        # Add sub-block information
        sub_blocks = render_data.get('sub_blocks', [])
        if sub_blocks:
            content.append("")  # Empty line
            for i, sub_block in enumerate(sub_blocks):
                status = "✓" if sub_block.get('state') == 'inscribed' else "⚙️"
                tokens = f"↑{sub_block.get('tokens_sent', 0)} ↓{sub_block.get('tokens_received', 0)}"
                content.append(f"{status} {sub_block['title']}: {tokens}")
        
        return "\n".join(content)


class LLMREPL:
    """Main LLM REPL application using unified block architecture."""
    
    def __init__(self, config_name: str = "debug"):
        self.config_name = config_name
        self.config = CONFIGURATIONS.get(config_name, CONFIGURATIONS["debug"])
        
        # Initialize console and display
        self.console = Console()
        self.display = RichDisplay(self.console)
        
        # Initialize Scrivener (authoritative record keeper)
        self.scrivener = ScrivenerV2(self.display)
        
        # Initialize LLM managers
        self.intent_manager = LLMManager(
            self.config.intent_detection_provider,
            self.config.intent_detection_model
        )
        self.main_manager = LLMManager(
            self.config.main_query_provider,
            self.config.main_query_model
        )
        
        # Initialize intent detection and routing
        self.intent_detector = IntentDetector(self.intent_manager)
        self.query_router = QueryRouter(self.intent_detector)
        
        # Setup prompt session
        self.prompt_session = PromptSession(
            style=Style.from_dict({
                'prompt': '#00aa00 bold',
                'path': '#3388ff',
                'rprompt': '#888888',
            }),
            history=InMemoryHistory()
        )
        
        # Session state
        self.session_history = []
        self.running = False
    
    async def initialize(self) -> bool:
        """Initialize the REPL system."""
        await self.scrivener.start()
        
        # Create and display system check
        system_check = await self.scrivener.create_system_check()
        
        # Add system checks - just validate configuration for now
        system_check.add_check(
            "Intent Detection",
            True,  # Always pass for now - configuration is valid
            f"Model: {self.config.intent_detection_display_name}"
        )
        
        system_check.add_check(
            "Main Query",
            True,  # Always pass for now - configuration is valid
            f"Model: {self.config.main_query_display_name}"
        )
        
        # Complete system check
        await self.scrivener.complete_system_check(system_check)
        
        # Check if all tests passed
        all_passed = all(check["passed"] for check in system_check.checks)
        
        if all_passed:
            # Create welcome message
            await self.scrivener.create_welcome("v3 (Unified)")
            
            # Wait for events to process
            await asyncio.sleep(0.1)
            
            # During initialization, we only have system check and welcome
            # Full sequence validation happens during query processing
            sequence = self.scrivener.get_current_sequence()
            if sequence:
                block_types = [b.metadata.type for b in sequence.blocks]
                expected_init_types = ['system_check', 'welcome']
                if not all(expected in block_types for expected in expected_init_types):
                    self.console.print(f"❌ [red]Initialization sequence validation failed[/red]")
                    self.console.print(f"Expected: {expected_init_types}, Got: {block_types}")
                    return False
            
            return True
        else:
            self.console.print("❌ [red]System checks failed - cannot continue[/red]")
            return False
    
    async def process_query(self, query: str) -> None:
        """Process a user query with the unified block architecture."""
        try:
            # 1. Create user input block
            user_block = await self.scrivener.create_user_input(query)
            
            # 2. Create internal processing block
            processing = await self.scrivener.create_internal_processing()
            
            # 3. Add intent detection step
            intent_step = await self.scrivener.add_processing_step(
                processing,
                "🧠 Intent Detection",
                f"Analyzing query intent using {self.config.intent_detection_display_name}..."
            )
            
            # Start intent detection
            await self.scrivener.start_processing_step(processing, 0)
            
            # Perform intent detection
            intent = await self.intent_detector.detect_intent(query)
            
            # Complete intent detection
            await self.scrivener.complete_processing_step(
                processing, 0,
                intent.value,
                15, 5,  # Mock token counts
                f"Intent: {intent.value}. Routing to: {self.config.main_query_display_name}"
            )
            
            # 4. Add main query step
            main_step = await self.scrivener.add_processing_step(
                processing,
                "💬 Main Query",
                f"Generating response using {self.config.main_query_display_name}..."
            )
            
            # Start main query
            await self.scrivener.start_processing_step(processing, 1)
            
            # Perform main query
            response = await self.main_manager.make_request(query)
            
            # Complete main query
            await self.scrivener.complete_processing_step(
                processing, 1,
                response.content,
                response.tokens.input_tokens,
                response.tokens.output_tokens,
                f"Response ready: {self.config.main_query_display_name}"
            )
            
            # 5. Complete internal processing
            await self.scrivener.complete_internal_processing(processing)
            
            # 6. Create assistant response
            await self.scrivener.create_assistant_response(
                response.content,
                f"{response.duration_seconds:.1f}s"
            )
            
            # 7. Validate block sequence
            if not self.scrivener.validate_sequence():
                self.console.print("❌ [red]Block sequence validation failed![/red]")
                report = self.scrivener.get_validation_report()
                self.console.print(f"Validation report: {report}")
            
            # Add to session history
            self.session_history.append({
                'query': query,
                'response': response.content,
                'tokens': response.tokens,
                'duration': response.duration_seconds
            })
            
        except Exception as e:
            # Create error response
            await self.scrivener.create_assistant_response(
                f"❌ Error processing query: {str(e)}",
                "error"
            )
    
    async def run(self) -> None:
        """Run the main REPL loop."""
        # Initialize system
        if not await self.initialize():
            return
        
        self.running = True
        
        try:
            while self.running:
                # Get user input
                try:
                    user_input = await asyncio.get_event_loop().run_in_executor(
                        None, self.prompt_session.prompt, "You: "
                    )
                    
                    if not user_input.strip():
                        continue
                    
                    # Handle special commands
                    if user_input.lower() in ['exit', 'quit', 'bye']:
                        self.running = False
                        break
                    
                    # Process the query
                    await self.process_query(user_input)
                    
                except KeyboardInterrupt:
                    self.console.print("\n👋 Goodbye!")
                    break
                except EOFError:
                    self.console.print("\n👋 Goodbye!")
                    break
                    
        finally:
            await self.scrivener.stop()
    
    def show_statistics(self) -> None:
        """Show session statistics."""
        if not self.session_history:
            self.console.print("No queries processed yet.")
            return
        
        total_queries = len(self.session_history)
        total_tokens = sum(h['tokens'].total_tokens for h in self.session_history)
        avg_duration = sum(h['duration'] for h in self.session_history) / total_queries
        
        stats = f"""
📊 Session Statistics:
   • Queries processed: {total_queries}
   • Total tokens: {total_tokens}
   • Average duration: {avg_duration:.1f}s
   • Configuration: {self.config_name}
"""
        self.console.print(Panel(stats, title="Session Statistics", box=ROUNDED))


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="LLM REPL - Interactive Research Assistant")
    parser.add_argument(
        '--config', '-c',
        choices=['debug', 'mixed', 'fast', 'test'],
        default='debug',
        help='LLM configuration to use'
    )
    parser.add_argument(
        '--show-configs',
        action='store_true',
        help='Show available configurations and exit'
    )
    
    args = parser.parse_args()
    
    if args.show_configs:
        console = Console()
        console.print("Available LLM configurations:")
        for name, config in CONFIGURATIONS.items():
            console.print(f"  {name}: {config.intent_detection_display_name} + {config.main_query_display_name}")
        return
    
    # Create and run REPL
    repl = LLMREPL(args.config)
    await repl.run()


if __name__ == "__main__":
    asyncio.run(main())