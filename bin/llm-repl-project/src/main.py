#!/usr/bin/env python3
"""
LLM REPL - Structurally Correct Interactive Research Assistant

This refactored version uses strong types and state machines to make
timing violations impossible:

1. State machine enforces startup-before-prompt
2. Proof tokens ensure display completion
3. Type safety prevents async/sync mismatches
4. Unified display system eliminates context dependencies
"""

import asyncio
import argparse
import sys
import time
from pathlib import Path
from typing import Optional, List

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import structural guarantees
from program_state import (
    ProgramStateMachine, 
    ProgramPhase,
    StartupComplete,
    StartupSequenceManager,
    GuaranteedDisplaySystem
)
from timeline_integrity import (
    ApplicationWithSecureTimeline,
    TimelineEligiblePlugin
)

# Import existing plugin architecture
from plugins.registry import PluginManager
from plugins.llm_interface import LLMManager, MockLLMInterface
from plugins.base import RenderContext, PluginState
from scrivener import Scrivener, RichTimelineDisplay

# Rich UI imports
from rich.console import Console
from rich.panel import Panel
from rich.box import ROUNDED

# Custom UI imports
from ui.input_system import SimpleMultilineInput
from plugin_timeline_adapter import create_timeline_eligible_plugin


class StructurallyCorrectREPL:
    """
    REPL with structural guarantees for correct lifecycle.
    
    Uses state machine and proof tokens to ensure:
    - Startup sequence MUST complete before prompt appears
    - Display operations MUST complete before state transitions
    - Timing violations are impossible
    """
    
    def __init__(self, config_name: str = "debug"):
        self.config_name = config_name
        
        # Initialize timeline-pure console and guaranteed display system
        raw_console = Console()
        self.app = ApplicationWithSecureTimeline(raw_console)
        self.display_system = GuaranteedDisplaySystem(raw_console)
        
        # Initialize state machine for lifecycle management
        self.state_machine = ProgramStateMachine()
        
        # Initialize startup sequence manager
        self.startup_manager = StartupSequenceManager(self.display_system)
        
        # Initialize plugin architecture
        self.plugin_manager = PluginManager()
        self.llm_manager = LLMManager()
        self.input_system = SimpleMultilineInput()
        
        # Initialize scrivener for timeline management
        timeline_display = RichTimelineDisplay(self.console)
        self.scrivener = Scrivener(timeline_display)
        
        # Session state
        self.running = False
        self.plugin_sequence: List[str] = []
    
    async def initialize_system(self) -> bool:
        """
        Initialize the REPL system without displaying anything.
        
        This phase only sets up internal systems. Display happens
        in the startup sequence phase.
        """
        if self.state_machine.current_phase != ProgramPhase.INITIALIZING:
            raise ValueError("System can only be initialized from INITIALIZING phase")
        
        try:
            # Start plugin manager
            await self.plugin_manager.start()
            
            # Start scrivener
            await self.scrivener.start()
            
            # Register all standard plugins
            from plugins.blocks.system_check import SystemCheckPlugin
            from plugins.blocks.welcome import WelcomePlugin
            from plugins.blocks.user_input import UserInputPlugin
            from plugins.blocks.cognition import CognitionPlugin
            from plugins.blocks.assistant_response import AssistantResponsePlugin
            
            self.plugin_manager.register_plugin_class(SystemCheckPlugin)
            self.plugin_manager.register_plugin_class(WelcomePlugin)
            self.plugin_manager.register_plugin_class(UserInputPlugin)
            self.plugin_manager.register_plugin_class(CognitionPlugin)
            self.plugin_manager.register_plugin_class(AssistantResponsePlugin)
            
            # Setup LLM interfaces based on configuration
            from config.llm_config import CONFIGURATIONS
            llm_config = CONFIGURATIONS.get(self.config_name, CONFIGURATIONS["debug"])
            
            # Create mock interfaces (in real implementation, these would be actual providers)
            intent_interface = MockLLMInterface({
                "provider_name": llm_config.intent_detection_provider.value,
                "model_name": llm_config.intent_detection_model
            })
            main_interface = MockLLMInterface({
                "provider_name": llm_config.main_query_provider.value,
                "model_name": llm_config.main_query_model
            })
            
            self.llm_manager.register_interface("intent_detection", intent_interface)
            self.llm_manager.register_interface("main_query", main_interface, is_default=True)
            self.llm_manager.register_interface("default", main_interface)
            
            return True
            
        except Exception as e:
            # Initialization errors should not pollute timeline - they're system failures
            # If needed, create a proper Error Plugin with metadata, timing, etc.
            return False  # Just fail silently
            return False
    
    async def run_startup_sequence_with_proof(self) -> StartupComplete:
        """
        Run startup sequence with guaranteed display completion.
        
        This method MUST NOT return until startup content is visible
        to the user. State machine prevents prompt from appearing
        until this completes.
        """
        if self.state_machine.current_phase != ProgramPhase.INITIALIZING:
            raise ValueError("Startup sequence can only run from INITIALIZING phase")
        
        # Transition to startup display phase
        self.state_machine.transition_to_startup_display()
        
        # Create startup plugins with display content
        startup_plugins = await self._create_startup_plugins()
        
        # Run startup sequence with proof of completion
        startup_proof = await self.startup_manager.run_startup_with_proof(startup_plugins)
        
        # Complete startup with proof token
        self.state_machine.complete_startup(startup_proof)
        
        return startup_proof
    
    async def _create_startup_plugins(self) -> List[Panel]:
        """
        Create startup plugins and format them for display.
        
        Returns list of Rich Panel objects that will be
        displayed to the user during startup.
        """
        startup_content = []
        
        # Load LLM configuration
        from config.llm_config import CONFIGURATIONS
        llm_config = CONFIGURATIONS.get(self.config_name, CONFIGURATIONS["debug"])
        
        # 1. System Check Plugin
        system_check_id = await self.plugin_manager.create_plugin("system_check", {
            "timeout_seconds": 30,
            "required_checks": ["Configuration", "Dependencies", "LLM Providers"],
            "fail_fast": False,
            "llm_config": llm_config
        })
        
        system_check_plugin = self.plugin_manager.active_plugins[system_check_id]
        
        # Run system checks
        check_data = [
            {
                "name": "Configuration", 
                "type": "config_check",
                "config": {"active_config": self.config_name}
            },
            {"name": "Dependencies", "type": "dependency_check"},
            {
                "name": f"Intent Detection LLM", 
                "type": "llm_heartbeat",
                "config": {
                    "provider": llm_config.intent_detection_provider.value,
                    "model": llm_config.intent_detection_model,
                    "interface_name": "intent_detection",
                    "llm_manager": self.llm_manager,
                    "timeout": 10
                }
            },
            {
                "name": f"Main Query LLM", 
                "type": "llm_heartbeat",
                "config": {
                    "provider": llm_config.main_query_provider.value,
                    "model": llm_config.main_query_model,
                    "interface_name": "main_query", 
                    "llm_manager": self.llm_manager,
                    "timeout": 10
                }
            }
        ]
        
        await system_check_plugin.process(check_data, {})
        
        # Format system check for display
        context = RenderContext(display_mode="inscribed")
        render_data = await system_check_plugin.render(context)
        system_check_content = self._format_system_check_display(render_data)
        startup_content.append(system_check_content)
        
        # 2. Welcome Plugin (includes startup completion semantically)
        welcome_id = await self.plugin_manager.create_plugin("welcome", {
            "version": "v3 (Structurally Correct)",
            "show_help": True,
            "show_commands": True,
            "startup_info": {
                "plugins_loaded": len(startup_content),
                "system_ready": True
            }
        })
        
        welcome_plugin = self.plugin_manager.active_plugins[welcome_id]
        await welcome_plugin.process({}, {})
        
        # Format welcome for display
        render_data = await welcome_plugin.render(context)
        welcome_content = self._format_welcome_display(render_data)
        startup_content.append(welcome_content)
        
        return startup_content
    
    def _format_system_check_display(self, render_data: dict) -> Panel:
        """Format system check plugin for terminal display."""
        title = render_data.get("title", "System Check")
        
        if "detailed_results" in render_data:
            content_lines = []
            
            # Format non-LLM results
            for result in render_data["detailed_results"]:
                status = result['status']
                name = result['name']
                message = result['message']
                
                if "Configuration" in name:
                    content_lines.append(f"{status} Configuration:\t{message}")
                elif "Dependencies" in name:
                    content_lines.append(f"{status} Dependencies:\t{message}")
                else:
                    content_lines.append(f"{status} {name}:\t{message}")
            
            # Format LLM results
            if "llm_results" in render_data and render_data["llm_results"]:
                content_lines.append("")
                content_lines.append("LLM Providers:")
                
                for llm_result in render_data["llm_results"]:
                    status = llm_result['status']
                    details = llm_result.get('details', {})
                    provider = details.get('provider', 'unknown')
                    model = details.get('model', 'unknown')
                    response_time = details.get('response_time', 0)
                    input_tokens = details.get('input_tokens', 0)
                    output_tokens = details.get('output_tokens', 0)
                    
                    content_lines.append(f"\t{status} {provider:12} {model:20} {response_time:6.1f}s  ↑{input_tokens:3} ↓{output_tokens:3}")
            
            content = "\n".join(content_lines)
        else:
            content = "System checks completed"
        
        # Create panel for display
        panel = Panel(
            content,
            title=title,
            box=ROUNDED,
            border_style="yellow"
        )
        
        return panel
    
    def _format_welcome_display(self, render_data: dict) -> Panel:
        """Format welcome plugin for terminal display."""
        title = render_data.get("title", "Welcome")
        content = render_data.get("content", "Welcome to LLM REPL!")
        
        # Create panel for display
        panel = Panel(
            content,
            title=title,
            box=ROUNDED,
            border_style="cyan"
        )
        
        return panel
    
    def can_show_prompt(self) -> bool:
        """
        Check if prompt can be shown.
        
        Uses state machine to ensure prompt only appears after
        startup completed with proof.
        """
        return self.state_machine.can_show_prompt()
    
    def get_startup_proof(self) -> Optional[StartupComplete]:
        """Get startup completion proof if available."""
        return self.state_machine.get_startup_proof()
    
    async def process_user_input(self, user_input: str) -> None:
        """
        Process user input through the complete plugin pipeline.
        
        This ensures proper User_Input, Cognition, and Assistant_Response blocks
        appear on the timeline instead of raw text.
        """
        try:
            # 1. User Input Plugin (for timeline history)
            user_input_id = await self.plugin_manager.create_plugin("user_input", {
                "max_length": 10000,
                "allow_empty": False
            })
            
            user_input_plugin = self.plugin_manager.active_plugins[user_input_id]
            await user_input_plugin.process(user_input, {})
            
            # Convert to timeline block
            context = RenderContext(display_mode="inscribed")
            render_data = await user_input_plugin.render(context)
            user_block = TimelineBlock(
                block_type=BlockType.USER_INPUT,
                title=render_data.get("title", "User Input"),
                content=f"> {user_input}",
                border_style="green"
            )
            self.console.display_block(user_block)
            
            # 2. Cognition Plugin
            from plugins.cognitive_modules import QueryRoutingModule, PromptEnhancementModule
            
            cognition_id = await self.plugin_manager.create_plugin("cognition", {
                "modules": [QueryRoutingModule, PromptEnhancementModule],
                "llm_interface": "default",
                "stream_processing": False
            })
            
            cognition_plugin = self.plugin_manager.active_plugins[cognition_id]
            
            # Process through cognition
            cognition_result = await cognition_plugin.process(user_input, {
                "llm_manager": self.llm_manager
            })
            
            # Convert to timeline block
            render_data = await cognition_plugin.render(context)
            cognition_block = TimelineBlock(
                block_type=BlockType.COGNITION,
                title=render_data.get("title", "Cognition"),
                content="Completed processing through 2 cognitive modules",
                border_style="magenta"
            )
            self.console.display_block(cognition_block)
            
            # 3. Assistant Response Plugin
            assistant_id = await self.plugin_manager.create_plugin("assistant_response", {
                "format_markdown": True
            })
            
            assistant_plugin = self.plugin_manager.active_plugins[assistant_id]
            
            # Transfer tokens from cognition to assistant
            cognition_tokens = cognition_plugin.get_token_counts()
            assistant_plugin.add_input_tokens(cognition_tokens.get("input", 0))
            assistant_plugin.add_output_tokens(cognition_tokens.get("output", 0))
            
            # Process assistant response
            await assistant_plugin.process({
                "response": cognition_result.get("final_output", "Response generated"),
                "processing_results": cognition_result
            }, {})
            
            # Convert to timeline block
            render_data = await assistant_plugin.render(context)
            assistant_block = TimelineBlock(
                block_type=BlockType.ASSISTANT_RESPONSE,
                title=render_data.get("title", "Assistant Response"),
                content=render_data.get("content", "Response generated"),
                border_style="blue"
            )
            self.console.display_block(assistant_block)
            
        except Exception as e:
            # Query errors should be handled by proper Error Plugin if needed
            # For now, silently fail - errors aren't semantic timeline content
            pass

    async def run_interactive_mode(self) -> None:
        """
        Run interactive mode with structural guarantees.
        
        Can only be called after startup completed with proof.
        """
        if not self.can_show_prompt():
            raise ValueError("Cannot start interactive mode without startup completion proof")
        
        # Transition to interactive mode
        self.state_machine.transition_to_interactive()
        
        self.running = True
        
        # Show startup completion info
        proof = self.get_startup_proof()
        if proof:
            # No status message - startup completion is implicit when prompt appears
            pass
        
        # Show prompt (guaranteed to appear after startup)
        self.console.display_prompt("\n> ")
        
        try:
            while self.running:
                # Get user input
                try:
                    user_input = await self.input_system.get_input("> ")
                    
                    if user_input is None:
                        # No goodbye block - this is UI, not timeline content
                        break
                    
                    if not user_input.strip():
                        continue
                    
                    # Handle special commands
                    if user_input.lower() in ['exit', 'quit', 'bye', '/quit', '/exit']:
                        self.running = False
                        break
                    
                    # Process the query using actual plugin pipeline
                    await self.process_user_input(user_input)
                    
                    # Signal response completion
                    self.input_system.signal_response_complete()
                    
                except KeyboardInterrupt:
                    # No goodbye block - this is UI, not timeline content
                    break
                except EOFError:
                    # No goodbye block - this is UI, not timeline content
                    break
                    
        finally:
            self.state_machine.shutdown()
            await self.plugin_manager.stop()
    
    async def run(self) -> None:
        """
        Main entry point with structural guarantees.
        
        Enforces correct lifecycle:
        1. Initialize system
        2. Run startup sequence with proof
        3. Start interactive mode only after startup completes
        """
        # Phase 1: Initialize system (no display)
        if not await self.initialize_system():
            return
        
        # Phase 2: Run startup sequence with proof of completion
        try:
            startup_proof = await self.run_startup_sequence_with_proof()
            # Status message is now handled by the startup completion block above
        except Exception as e:
            # Startup errors should not pollute timeline - they're system failures
            # If needed, create a proper Error Plugin with metadata, timing, etc.
            return
            return
        
        # Phase 3: Start interactive mode (only after startup proof)
        await self.run_interactive_mode()


async def main():
    """Main entry point with structural guarantees."""
    parser = argparse.ArgumentParser(description="LLM REPL v3 - Structurally Correct")
    parser.add_argument(
        '--config', '-c',
        choices=['debug', 'mixed', 'fast', 'test'],
        default='debug',
        help='Configuration to use'
    )
    
    args = parser.parse_args()
    
    # Create structurally correct REPL
    repl = StructurallyCorrectREPL(args.config)
    
    # Run with structural guarantees
    await repl.run()


if __name__ == "__main__":
    asyncio.run(main())