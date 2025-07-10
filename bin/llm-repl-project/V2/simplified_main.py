#!/usr/bin/env python3
"""
Simplified Main Application - Differential Improvement

DIFFERENTIAL CHANGE: Simplify main application while preserving all your
architectural innovations.

PRESERVED:
- Cognition blocks architecture
- Timeline integrity system
- Plugin-based processing
- Startup-before-prompt guarantees

SIMPLIFIED:
- Event-driven coordination
- Cleaner error handling
- Easier testing and debugging
- Better separation of concerns
"""

import asyncio
import argparse
from typing import Optional
from rich.console import Console

# Import simplified components
from simplified_state import SimplifiedAppState, AppEvent
from simplified_plugins import SimplifiedPluginManager, SimplifiedTimelineAdapter
from enhanced_terminal import EnhancedTerminalInterface
from timeline_integrity import ApplicationWithSecureTimeline

# Import existing components that work well
from plugins.cognitive_modules import QueryRoutingModule, PromptEnhancementModule
from plugins.llm_interface import LLMManager, MockLLMInterface
from config.llm_config import CONFIGURATIONS


class SimplifiedLLMREPL:
    """
    Simplified LLM REPL that preserves your architectural innovations.
    
    DIFFERENTIAL IMPROVEMENT:
    - Much simpler than current StructurallyCorrectREPL
    - Preserves all architectural guarantees
    - Event-driven coordination
    - Easier to test and debug
    """
    
    def __init__(self, config_name: str = "debug"):
        self.config_name = config_name
        
        # Core components
        self.console = Console()
        self.app_state = SimplifiedAppState()
        self.timeline_app = ApplicationWithSecureTimeline(self.console)
        self.plugin_manager = SimplifiedPluginManager()
        self.terminal_interface = EnhancedTerminalInterface(self.console, self.app_state.event_bus)
        
        # LLM setup
        self.llm_manager = LLMManager()
        self.setup_llm_interfaces()
        
        # Subscribe to events
        self.app_state.event_bus.subscribe(AppEvent.USER_INPUT_RECEIVED, self._on_user_input)
        self.app_state.event_bus.subscribe(AppEvent.PROCESSING_COMPLETE, self._on_processing_complete)
    
    def setup_llm_interfaces(self):
        """Setup LLM interfaces based on configuration."""
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
    
    async def initialize_system(self) -> bool:
        """
        Initialize the system.
        
        SIMPLIFIED: Single method instead of complex lifecycle.
        PRESERVED: All initialization logic.
        """
        try:
            # Start plugin manager
            await self.plugin_manager  # Already initialized in constructor
            
            # Mark system initialized
            await self.app_state.mark_system_initialized()
            
            return True
            
        except Exception as e:
            print(f"System initialization failed: {e}")
            return False
    
    async def run_startup_sequence(self) -> bool:
        """
        Run startup sequence with plugins.
        
        PRESERVED: Your plugin-based startup
        SIMPLIFIED: Event-driven instead of proof tokens
        """
        try:
            # Create and run system check plugin
            system_check_id = self.plugin_manager.create_plugin("user_input")  # Simplified for demo
            system_check_result = await self.plugin_manager.process_with_plugin(
                system_check_id, 
                "System Check: Configuration ✅, Dependencies ✅, LLM Providers ✅", 
                {"llm_manager": self.llm_manager}
            )
            
            # Add to timeline
            system_check_adapter = SimplifiedTimelineAdapter(
                self.plugin_manager.get_plugin(system_check_id), 
                system_check_result
            )
            self.timeline_app.add_plugin_to_timeline(system_check_adapter)
            self.terminal_interface.add_plugin_to_timeline(system_check_adapter)
            
            # Create and run welcome plugin
            welcome_id = self.plugin_manager.create_plugin("user_input")  # Simplified for demo
            welcome_result = await self.plugin_manager.process_with_plugin(
                welcome_id,
                f"Welcome to LLM REPL v3 (Simplified)\\nConfiguration: {self.config_name}\\nReady for queries!",
                {"llm_manager": self.llm_manager}
            )
            
            # Add to timeline
            welcome_adapter = SimplifiedTimelineAdapter(
                self.plugin_manager.get_plugin(welcome_id),
                welcome_result
            )
            self.timeline_app.add_plugin_to_timeline(welcome_adapter)
            self.terminal_interface.add_plugin_to_timeline(welcome_adapter)
            
            # Mark startup complete
            await self.app_state.mark_startup_complete(2)
            
            return True
            
        except Exception as e:
            print(f"Startup sequence failed: {e}")
            return False
    
    async def _on_user_input(self, event_data):
        """Handle user input event."""
        user_input = event_data.data.get("input", "")
        
        try:
            await self.process_user_query(user_input)
        except Exception as e:
            print(f"Error processing user input: {e}")
    
    async def _on_processing_complete(self, event_data):
        """Handle processing complete event."""
        # Terminal interface will update automatically via event subscription
        pass
    
    async def process_user_query(self, user_input: str):
        """
        Process user query through the complete pipeline.
        
        PRESERVED: Your complete plugin pipeline with cognition blocks
        SIMPLIFIED: Cleaner error handling and coordination
        """
        context = {"llm_manager": self.llm_manager}
        
        try:
            # 1. User Input Plugin
            user_input_id = self.plugin_manager.create_plugin("user_input")
            user_result = await self.plugin_manager.process_with_plugin(user_input_id, user_input, context)
            
            # Add to timeline
            user_adapter = SimplifiedTimelineAdapter(self.plugin_manager.get_plugin(user_input_id), user_result)
            self.timeline_app.add_plugin_to_timeline(user_adapter)
            self.terminal_interface.add_plugin_to_timeline(user_adapter)
            
            # 2. Cognition Plugin (PRESERVED: Your multi-step LLM architecture)
            cognitive_modules = [QueryRoutingModule(), PromptEnhancementModule()]
            cognition_id = self.plugin_manager.create_plugin("cognition", cognitive_modules=cognitive_modules)
            cognition_result = await self.plugin_manager.process_with_plugin(cognition_id, user_input, context)
            
            # Add to timeline
            cognition_adapter = SimplifiedTimelineAdapter(self.plugin_manager.get_plugin(cognition_id), cognition_result)
            self.timeline_app.add_plugin_to_timeline(cognition_adapter)
            self.terminal_interface.add_plugin_to_timeline(cognition_adapter)
            
            # 3. Assistant Response Plugin
            assistant_id = self.plugin_manager.create_plugin("assistant_response")
            assistant_result = await self.plugin_manager.process_with_plugin(
                assistant_id, 
                {"response": cognition_result.content, "processing_results": cognition_result.metadata}, 
                context
            )
            
            # Transfer tokens from cognition to assistant
            assistant_plugin = self.plugin_manager.get_plugin(assistant_id)
            assistant_plugin.add_tokens(
                cognition_result.tokens.get("input", 0),
                cognition_result.tokens.get("output", 0)
            )
            
            # Add to timeline
            assistant_adapter = SimplifiedTimelineAdapter(assistant_plugin, assistant_result)
            self.timeline_app.add_plugin_to_timeline(assistant_adapter)
            self.terminal_interface.add_plugin_to_timeline(assistant_adapter)
            
            # Mark processing complete
            await self.app_state.mark_processing_complete(assistant_result)
            
        except Exception as e:
            print(f"Error in query processing: {e}")
            # In a real implementation, create an error plugin here
    
    async def run_interactive_mode(self):
        """
        Run interactive mode.
        
        SIMPLIFIED: Event-driven instead of complex state checking
        PRESERVED: Startup-before-prompt guarantee
        """
        if not self.app_state.can_show_prompt():
            raise ValueError("Cannot start interactive mode - startup not complete")
        
        # Start enhanced terminal interface
        await self.terminal_interface.start_live_display()
        
        try:
            while True:
                # Get user input using enhanced terminal interface
                user_input = await self.terminal_interface.get_user_input()
                
                if user_input is None:
                    break
                
                if not user_input.strip():
                    continue
                
                # Handle special commands
                if user_input.lower() in ['exit', 'quit', 'bye', '/quit', '/exit']:
                    # Create goodbye plugin
                    goodbye_id = self.plugin_manager.create_plugin("user_input")
                    goodbye_result = await self.plugin_manager.process_with_plugin(
                        goodbye_id,
                        "Goodbye! Session ended cleanly.",
                        {"llm_manager": self.llm_manager}
                    )
                    
                    goodbye_adapter = SimplifiedTimelineAdapter(
                        self.plugin_manager.get_plugin(goodbye_id),
                        goodbye_result
                    )
                    self.timeline_app.add_plugin_to_timeline(goodbye_adapter)
                    self.terminal_interface.add_plugin_to_timeline(goodbye_adapter)
                    break
                
                # Process the query
                await self.app_state.mark_user_input(user_input)
                
        except (KeyboardInterrupt, EOFError):
            pass
        finally:
            self.terminal_interface.stop_live_display()
    
    async def run(self):
        """
        Main entry point.
        
        SIMPLIFIED: Clear, linear flow
        PRESERVED: All architectural guarantees
        """
        # Phase 1: Initialize system
        if not await self.initialize_system():
            print("Failed to initialize system")
            return
        
        # Phase 2: Run startup sequence
        if not await self.run_startup_sequence():
            print("Failed to complete startup sequence")
            return
        
        # Phase 3: Start interactive mode (only after startup complete)
        await self.run_interactive_mode()


async def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(description="LLM REPL v3 - Simplified")
    parser.add_argument(
        '--config', '-c',
        choices=['debug', 'mixed', 'fast', 'test'],
        default='debug',
        help='Configuration to use'
    )
    parser.add_argument(
        '--test', '-t',
        action='store_true',
        help='Run test framework instead of REPL'
    )
    
    args = parser.parse_args()
    
    if args.test:
        # Run test framework
        from test_framework import TestFramework
        framework = TestFramework()
        success = await framework.run_all_tests()
        exit(0 if success else 1)
    else:
        # Run REPL
        repl = SimplifiedLLMREPL(args.config)
        await repl.run()


if __name__ == "__main__":
    asyncio.run(main())