#!/usr/bin/env python3
"""
LLM REPL - Interactive Research Assistant with Plugin Architecture

This is the main entry point for the LLM REPL application using the new
plugin architecture that ensures:
- Independent, self-contained plugins
- Unified display system with timing and token tracking
- Comprehensive testing and validation
- Cognitive modules for advanced processing
"""

import asyncio
import argparse
import sys
from pathlib import Path
from typing import Optional, List

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import plugin architecture
from plugins.registry import PluginManager
from plugins.llm_interface import LLMManager, MockLLMInterface
from plugins.base import RenderContext, PluginState
from scrivener import Scrivener, RichTimelineDisplay

# Rich UI imports
from rich.console import Console
from rich.panel import Panel
from rich.box import ROUNDED
from rich.text import Text

# Custom UI imports
from ui.input_system import SimpleMultilineInput


class LLMREPLv3:
    """Main LLM REPL application using the new plugin architecture."""
    
    def __init__(self, config_name: str = "debug", conversation_spacing: int = 2):
        self.config_name = config_name
        self.conversation_spacing = conversation_spacing  # Configurable spacing between conversations
        
        # Initialize console
        self.console = Console()
        
        # Initialize plugin manager
        self.plugin_manager = PluginManager()
        
        # Initialize LLM manager
        self.llm_manager = LLMManager()
        
        # Initialize input system
        self.input_system = SimpleMultilineInput()
        
        # Initialize scrivener for timeline management
        timeline_display = RichTimelineDisplay(self.console)
        self.scrivener = Scrivener(timeline_display)
        
        # Session state
        self.running = False
        self.staging_area: List[str] = []     # Plugins currently processing
        self.current_staging_plugin: Optional[str] = None  # Only one at a time
        self.plugin_sequence: List[str] = []  # Track plugin order
    
    async def initialize(self) -> bool:
        """Initialize the REPL system."""
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
            
            # For now, use mock interfaces but with proper naming
            # In a real implementation, we'd create actual provider interfaces here
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
            
            # Create startup sequence
            await self._run_startup_sequence()
            
            return True
            
        except Exception as e:
            self.console.print(f"❌ [red]Failed to initialize: {str(e)}[/red]")
            return False
    
    async def _run_startup_sequence(self) -> None:
        """Run the startup sequence of plugins."""
        # Load LLM configuration
        from config.llm_config import CONFIGURATIONS
        llm_config = CONFIGURATIONS.get(self.config_name, CONFIGURATIONS["debug"])
        
        # 1. System Check
        system_check_id = await self.plugin_manager.create_plugin("system_check", {
            "timeout_seconds": 30,
            "required_checks": ["Configuration", "Dependencies", "LLM Providers"],
            "fail_fast": False,
            "llm_config": llm_config
        })
        
        system_check_plugin = self.plugin_manager.active_plugins[system_check_id]
        
        # Run system checks including LLM heartbeat
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
        
        # Scrivener writes completed plugins to timeline
        await self._scrivener_write_to_timeline(system_check_id)
        
        # 2. Welcome Message
        welcome_id = await self.plugin_manager.create_plugin("welcome", {
            "version": "v3 (Plugin Architecture)",
            "show_help": True,
            "show_commands": True
        })
        
        welcome_plugin = self.plugin_manager.active_plugins[welcome_id]
        await welcome_plugin.process({}, {})
        
        # Scrivener writes completed plugins to timeline
        await self._scrivener_write_to_timeline(welcome_id)
    
    async def _graphics_manager_request_staging(self, plugin_id: str) -> bool:
        """Graphics Manager: Request to render a plugin in staging area."""
        # Only one plugin allowed in staging at a time
        if self.current_staging_plugin is not None:
            return False  # Staging area occupied
        
        plugin = self.plugin_manager.active_plugins[plugin_id]
        if plugin.state != PluginState.PROCESSING:
            return False  # Only processing plugins allowed in staging
        
        self.current_staging_plugin = plugin_id
        await self._render_plugin_processing(plugin)
        return True
    
    async def _graphics_manager_complete_staging(self, plugin_id: str) -> None:
        """Graphics Manager: Block completed, delete staging render and pass to scrivener."""
        if self.current_staging_plugin != plugin_id:
            return  # Not the current staging plugin
        
        # Delete the staging render (it's gone forever)
        self._clear_staging_render()
        self.current_staging_plugin = None
        
        # Pass to scrivener
        await self._scrivener_write_to_timeline(plugin_id)
    
    def _clear_staging_render(self) -> None:
        """Clear the current staging render from screen."""
        # Move up and clear the staging display
        self.console.print("\033[4A\033[K\033[3A\033[K\033[2A\033[K\033[1A\033[K", end="")
    
    async def _scrivener_write_to_timeline(self, plugin_id: str) -> None:
        """Request scrivener to inscribe plugin in timeline."""
        plugin = self.plugin_manager.active_plugins[plugin_id]
        
        # Request inscription from scrivener (scrivener will validate)
        success = await self.scrivener.inscribe_plugin(plugin, {
            'conversation_spacing': getattr(self, 'conversation_spacing', 2)
        })
        
        if not success:
            print(f"Scrivener rejected plugin {plugin_id} - state: {plugin.state}")
            return
    
    async def _render_plugin(self, plugin) -> None:
        """Render a plugin based on its internal state."""
        # Use the plugin's built-in state to determine rendering
        if plugin.state == PluginState.PROCESSING:
            await self._render_plugin_processing(plugin)
        else:
            await self._render_plugin_completed(plugin)
    
    async def _render_plugin_processing(self, plugin) -> None:
        """Render a plugin in processing state (staging area)."""
        context = RenderContext(display_mode="staging")
        render_data = await plugin.render(context)
        
        title = render_data.get("title", "Plugin")
        content = render_data.get("content", "Processing...")
        
        # Processing state styling - bright colors to show it's live
        border_color = "bright_yellow"
        if plugin.metadata.name == "cognition":
            border_color = "bright_magenta"
        elif plugin.metadata.name == "assistant_response":
            border_color = "bright_blue"
        
        panel = Panel(
            content,
            title=f"🔄 {title}",  # Add spinner to indicate processing
            box=ROUNDED,
            border_style=border_color
        )
        
        self.console.print(panel)
    
    async def _update_plugin_in_place(self, plugin) -> None:
        """Update a plugin display when it transitions from processing to completed."""
        # Move cursor up to overwrite the processing display
        self.console.print("\033[4A\033[K\033[3A\033[K\033[2A\033[K\033[1A\033[K", end="")
        
        # Re-render in completed state
        await self._render_plugin_completed(plugin)
    
    def _add_to_staging(self, plugin_id: str) -> None:
        """Add a plugin to staging area."""
        if plugin_id not in self.staging_area:
            self.staging_area.append(plugin_id)
        self.current_staging_plugin = plugin_id
    
    def _remove_from_staging(self, plugin_id: str) -> None:
        """Remove a plugin from staging area."""
        if plugin_id in self.staging_area:
            self.staging_area.remove(plugin_id)
        if self.current_staging_plugin == plugin_id:
            self.current_staging_plugin = None
    
    async def _render_plugin_completed(self, plugin) -> None:
        """Render a plugin in the timeline (completed)."""
        # Use inscribed mode to get detailed results from system check
        context = RenderContext(display_mode="inscribed")
        render_data = await plugin.render(context)
        
        # Extract display info
        title = render_data.get("title", "Plugin")
        content = render_data.get("content", "")
        
        # Handle system check special formatting
        if plugin.metadata.name == "system_check":
            if "detailed_results" in render_data:
                content_lines = []
                
                # Format non-LLM results with tab alignment
                for result in render_data["detailed_results"]:
                    status = result['status']
                    name = result['name']
                    message = result['message']
                    
                    # Tab-align the status and message
                    if "Configuration" in name:
                        content_lines.append(f"{status} Configuration:\t{message}")
                    elif "Dependencies" in name:
                        content_lines.append(f"{status} Dependencies:\t{message}")
                    else:
                        content_lines.append(f"{status} {name}:\t{message}")
                
                # Format LLM results as a table
                if "llm_results" in render_data and render_data["llm_results"]:
                    content_lines.append("")  # Empty line before LLM section
                    content_lines.append("LLM Providers:")
                    
                    for llm_result in render_data["llm_results"]:
                        status = llm_result['status']
                        details = llm_result.get('details', {})
                        provider = details.get('provider', 'unknown')
                        model = details.get('model', 'unknown')
                        response_time = details.get('response_time', 0)
                        input_tokens = details.get('input_tokens', 0)
                        output_tokens = details.get('output_tokens', 0)
                        
                        # Format as table row with tab alignment
                        content_lines.append(f"\t{status} {provider:12} {model:20} {response_time:6.1f}s  ↑{input_tokens:3} ↓{output_tokens:3}")
                
                content = "\n".join(content_lines) if content_lines else "System checks completed"
        
        # Handle user input special formatting (no "You:" prefix)
        elif plugin.metadata.name == "user_input":
            user_content = render_data.get("content", "")
            # Format multiline input nicely
            if "\n" in user_content:
                lines = user_content.split("\n")
                formatted_lines = []
                for i, line in enumerate(lines):
                    if i == 0:
                        formatted_lines.append(f"> {line}")
                    else:
                        formatted_lines.append(f"  {line}")  # Continuation indent
                content = "\n".join(formatted_lines)
            else:
                content = f"> {user_content}"
        
        # Create styled panel with different colors for different plugin types
        style = render_data.get("style", {})
        
        # Assign colors based on plugin type
        if plugin.metadata.name == "system_check":
            border_color = "yellow"
        elif plugin.metadata.name == "welcome":
            border_color = "cyan"
        elif plugin.metadata.name == "user_input":
            border_color = "green"
        elif plugin.metadata.name == "cognition":
            border_color = "magenta"
        elif plugin.metadata.name == "assistant_response":
            border_color = "blue"
        else:
            border_color = style.get("border_color", "white")
        
        panel = Panel(
            content,
            title=title,
            box=ROUNDED,
            border_style=border_color
        )
        
        self.console.print(panel)
        
        # Spacing logic:
        # - No gap between system_check and welcome (startup group)
        # - One gap after welcome (separate startup from chat)
        # - No gaps within conversation flows (user->cognition->assistant)
        # - Configurable gap after assistant_response (between conversations)
        if plugin.metadata.name == "system_check":
            # No gap after system check
            pass
        elif plugin.metadata.name == "welcome":
            # Two gaps after welcome to separate startup from chat
            self.console.print()
            self.console.print()
        elif plugin.metadata.name == "assistant_response":
            # Configurable gap after assistant response (between conversations)
            conversation_spacing = getattr(self, 'conversation_spacing', 2)  # Default to 2
            for _ in range(conversation_spacing):
                self.console.print()
        else:
            # No gaps for user_input, cognition, or staging plugins
            pass
    
    async def process_query(self, query: str) -> None:
        """Process a user query using the plugin architecture."""
        try:
            # 1. User Input Plugin (for timeline history)
            user_input_id = await self.plugin_manager.create_plugin("user_input", {
                "max_length": 10000,
                "allow_empty": False
            })
            
            user_input_plugin = self.plugin_manager.active_plugins[user_input_id]
            await user_input_plugin.process(query, {})
            
            # Scrivener writes completed plugins to timeline
            await self._scrivener_write_to_timeline(user_input_id)
            
            # 2. Cognition Plugin
            from plugins.cognitive_modules import QueryRoutingModule, PromptEnhancementModule
            
            cognition_id = await self.plugin_manager.create_plugin("cognition", {
                "modules": [QueryRoutingModule, PromptEnhancementModule],
                "llm_interface": "default",
                "stream_processing": True  # Enable streaming
            })
            
            cognition_plugin = self.plugin_manager.active_plugins[cognition_id]
            
            # Add to staging area for processing
            self._add_to_staging(cognition_id)
            
            # Process asynchronously while showing live state
            cognition_plugin._data["stream_processing"] = False
            
            # Start processing (this sets state to PROCESSING automatically)
            processing_task = asyncio.create_task(cognition_plugin.process(query, {
                "llm_manager": self.llm_manager
            }))
            
            # Render processing state (staging area)
            await self._render_plugin_processing(cognition_plugin)
            
            # Add delay to show processing state
            await asyncio.sleep(3)
            
            # Wait for processing to complete
            cognition_result = await processing_task
            
            # Move from staging to timeline (scrivener's job)
            self._remove_from_staging(cognition_id)
            # Clear the staging area display
            self._clear_staging_render()
            await self._scrivener_write_to_timeline(cognition_id)
            
            # 3. Assistant Response Plugin
            assistant_id = await self.plugin_manager.create_plugin("assistant_response", {
                "format_markdown": True
            })
            
            assistant_plugin = self.plugin_manager.active_plugins[assistant_id]
            
            # Add to staging area for processing
            self._add_to_staging(assistant_id)
            
            # Process asynchronously while showing live state
            # Transfer tokens from cognition to assistant
            cognition_tokens = cognition_plugin.get_token_counts()
            assistant_plugin.add_input_tokens(cognition_tokens.get("input", 0))
            assistant_plugin.add_output_tokens(cognition_tokens.get("output", 0))
            
            # Start processing (this sets state to PROCESSING automatically)
            processing_task = asyncio.create_task(assistant_plugin.process({
                "response": cognition_result.get("final_output", "Response generated"),
                "processing_results": cognition_result
            }, {}))
            
            # Render processing state (staging area)
            await self._render_plugin_processing(assistant_plugin)
            
            # Add delay to show processing state
            await asyncio.sleep(2)
            
            # Wait for processing to complete
            await processing_task
            
            # Move from staging to timeline (scrivener's job)
            self._remove_from_staging(assistant_id)
            # Clear the staging area display
            self._clear_staging_render()
            await self._scrivener_write_to_timeline(assistant_id)
            
        except Exception as e:
            # Create error panel
            error_panel = Panel(
                f"Error processing query: {str(e)}",
                title="❌ Error",
                box=ROUNDED,
                border_style="red"
            )
            self.console.print(error_panel)
    
    async def run(self) -> None:
        """Run the main REPL loop."""
        # Initialize system
        if not await self.initialize():
            return
        
        self.running = True
        
        try:
            while self.running:
                # Get user input using the new input system
                try:
                    # Ensure prompt is visible
                    self.console.print()  # Add a blank line for spacing
                    
                    # Get user input (the prompt display will be handled cleanly by the input system)
                    user_input = await self.input_system.get_input("> ")
                    
                    if user_input is None:
                        # User pressed Ctrl+C or Ctrl+D
                        self.console.print("\n👋 Goodbye!")
                        break
                    
                    if not user_input.strip():
                        continue
                    
                    # Handle special commands
                    if user_input.lower() in ['exit', 'quit', 'bye']:
                        self.running = False
                        break
                    elif user_input.lower() == 'stats':
                        await self.show_statistics()
                        continue
                    
                    # Process the query
                    await self.process_query(user_input)
                    
                except KeyboardInterrupt:
                    self.console.print("\n👋 Goodbye!")
                    break
                except EOFError:
                    self.console.print("\n👋 Goodbye!")
                    break
                    
        finally:
            await self.plugin_manager.stop()
    
    async def show_statistics(self) -> None:
        """Show session statistics."""
        stats_lines = [
            f"Configuration: {self.config_name}",
            f"Plugins created: {len(self.plugin_sequence)}",
            f"Active plugins: {len(self.plugin_manager.active_plugins)}",
            f"Plugin types available: {len(self.plugin_manager.registered_plugins)}"
        ]
        
        # Show plugin sequence
        if self.plugin_sequence:
            stats_lines.append("")
            stats_lines.append("Plugin Sequence:")
            for i, plugin_id in enumerate(self.plugin_sequence):
                if plugin_id in self.plugin_manager.active_plugins:
                    plugin = self.plugin_manager.active_plugins[plugin_id]
                    plugin_name = plugin.metadata.name
                    state = plugin.state.value
                    stats_lines.append(f"  {i+1}. {plugin_name} ({state})")
        
        stats_panel = Panel(
            "\n".join(stats_lines),
            title="📊 Session Statistics",
            box=ROUNDED,
            border_style="cyan"
        )
        self.console.print(stats_panel)


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="LLM REPL v3 - Plugin Architecture")
    parser.add_argument(
        '--config', '-c',
        choices=['debug', 'mixed', 'fast', 'test'],
        default='debug',
        help='Configuration to use (currently placeholder)'
    )
    
    args = parser.parse_args()
    
    # Create and run REPL
    repl = LLMREPLv3(args.config)
    await repl.run()


if __name__ == "__main__":
    asyncio.run(main())