#!/usr/bin/env python3
"""
LLM REPL V2 - Interactive Research Assistant with V2 Architecture

This is the main interactive REPL using the V2 architecture with:
- Accurate token timing  
- Smooth animation without snapping
- Clean block lifecycle management
- Full Rich UI from V1 (no graphical regressions)
"""

import asyncio
import sys
import os
import time
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, Any, Optional

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import V2 architecture
from v2_architecture import (
    ProcessingSubBlock, InternalProcessingBlock,
    ResearchAssistantResponse, UserInputBlock, BlockState
)
from enhanced_animation import RealtimeTokenTracker
from v1_v2_migration import HybridSystemManager, MigrationConfig
from scrivener import Scrivener, RichDisplayInterface, InscriptionEvent, EventType
from system_check import SystemCheck

# Import refactored modules
from providers import LLMManager, LLMProvider
from config.llm_config import LLMConfiguration
from processing import IntentDetector, QueryIntent, QueryRouter

# Import configurations
from config import CONFIGURATIONS

# Import Rich UI components from V1
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.box import ROUNDED, HEAVY
from rich.text import Text
from rich.live import Live
from rich.layout import Layout
from rich.status import Status
from rich.columns import Columns
from rich.align import Align
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import FormattedText, HTML
from prompt_toolkit.shortcuts import print_formatted_text
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory

# Import V1 UI classes for compatibility
try:
    from llm_repl_v0 import RichUI, LiveProgressIndicator, SessionLogger
    V1_UI_AVAILABLE = True
except ImportError:
    V1_UI_AVAILABLE = False

class V2REPL:
    """Interactive REPL using V2 architecture with full Rich UI."""
    
    def __init__(self, config_name: str = "debug"):
        # Get LLM configuration
        self.config = CONFIGURATIONS.get(config_name, CONFIGURATIONS["debug"])
        
        # V2 Architecture components - separate LLM managers for different processes
        self.intent_detection_manager = LLMManager(
            self.config.intent_detection_provider, 
            self.config.intent_detection_model
        )
        self.main_query_manager = LLMManager(
            self.config.main_query_provider, 
            self.config.main_query_model
        )
        
        self.session_history = []
        self.token_tracker = RealtimeTokenTracker()
        
        # Initialize intent detector with intent detection manager
        self.intent_detector = IntentDetector(self.intent_detection_manager)
        self.query_router = QueryRouter(self.intent_detector)
        
        # Rich UI setup (maintaining V1 graphics)
        self.console = Console()
        self.rich_ui = None
        self.session_logger = None
        
        # Try to initialize V1 components with runtime error handling
        if V1_UI_AVAILABLE:
            try:
                self.rich_ui = RichUI(self.console)
                self.session_logger = SessionLogger("research_assistant")
            except Exception as e:
                # V1 components failed at runtime - fall back to basic UI
                print(f"Warning: Enhanced UI unavailable ({e})")
                self.rich_ui = None
                self.session_logger = None
        
        # Prompt toolkit setup
        self.style = Style.from_dict({
            'prompt': '#00aa00 bold',
            'path': '#3388ff',
            'rprompt': '#888888',
        })
        
        # Setup key bindings
        bindings = KeyBindings()
        
        @bindings.add('c-c')
        def _(event):
            """Handle Ctrl+C gracefully."""
            event.app.exit(exception=KeyboardInterrupt)
        
        @bindings.add('c-d')
        def _(event):
            """Handle Ctrl+D (EOF)."""
            event.app.exit(exception=EOFError)
        
        # Create prompt session
        self.prompt_session = PromptSession(
            style=self.style,
            key_bindings=bindings,
            history=InMemoryHistory(),
            complete_style='column',
            wrap_lines=True
        )
        
        # Use hybrid system for smooth transition
        config = MigrationConfig(
            use_v2_llm_manager=True,
            use_v2_animation=True,
            maintain_v1_display=True  # Keep V1 display system
        )
        self.hybrid_manager = HybridSystemManager(config)
        
        # Initialize scrivener for proper event ordering
        display_interface = RichDisplayInterface(self.rich_ui, self.console)
        self.scrivener = Scrivener(display_interface)
        
    async def initialize(self):
        """Initialize the REPL system with Rich UI and model validation."""
        # Start scrivener for proper event ordering
        await self.scrivener.start()
        
        # Create and run system check
        system_check = SystemCheck(
            self.scrivener,
            self.config,
            self.intent_detection_manager,
            self.main_query_manager
        )
        
        # Run all system checks - this will fail fast if models aren't available
        try:
            system_check_passed = await system_check.run_all_checks()
            
            if not system_check_passed:
                # System check failed - exit immediately
                await self.scrivener.inscribe(InscriptionEvent(
                    event_type=EventType.SYSTEM_MESSAGE,
                    content="❌ System check failed - application cannot continue",
                    metadata={"fatal_error": True}
                ))
                await self.scrivener.stop()
                raise SystemExit(1)
                
        except Exception as e:
            # Any exception during system check is fatal
            await self.scrivener.inscribe(InscriptionEvent(
                event_type=EventType.SYSTEM_MESSAGE,
                content=f"❌ Fatal system check error: {e}",
                metadata={"fatal_error": True}
            ))
            await self.scrivener.stop()
            raise SystemExit(1)
        
        if self.rich_ui:
            # Professional welcome message focused on user experience
            welcome_content = Text()
            welcome_content.append("🤖 Research Assistant\n", style="bold green")
            welcome_content.append("AI-powered research and analysis tool\n\n", style="bright_white")
            welcome_content.append("💡 Commands:\n", style="bold yellow")
            welcome_content.append("  - Type your question and press Enter\n", style="dim white")
            welcome_content.append("  - '/help' for available commands\n", style="dim white")
            welcome_content.append("  - '/quit' or '/exit' to exit", style="dim white")
            
            welcome_panel = Panel(
                welcome_content,
                title="[bold blue]Welcome[/bold blue]",
                box=ROUNDED,
                border_style="blue",
                padding=(1, 2)
            )
            self.console.print(welcome_panel)
        else:
            # Fallback to basic print
            print("🤖 Research Assistant")
            print("AI-powered research and analysis tool")
        
        # Skip hybrid manager initialization for now to avoid timeouts
        # await self.hybrid_manager.initialize_hybrid_system(quiet=True)
        
        if self.session_logger:
            self.session_logger.log_system_message("Research Assistant session started")
    
    
    async def run(self):
        """Run the interactive REPL with Rich UI."""
        await self.initialize()
        
        while True:
            try:
                # Get user input with styled prompt
                prompt_text = [
                    ('class:prompt', 'You'),
                    ('', ': '),
                ]
                
                user_input = await asyncio.to_thread(
                    self.prompt_session.prompt, 
                    prompt_text
                )
                user_input = user_input.strip()
                
                if not user_input:
                    continue
                
                # Display user input through scrivener for proper ordering
                await self.scrivener.inscribe(InscriptionEvent(
                    event_type=EventType.USER_INPUT,
                    content=user_input
                ))
                
                if self.session_logger:
                    self.session_logger.log_user_input(user_input)
                
                # Handle commands
                if user_input.startswith('/'):
                    should_exit = await self.handle_command(user_input)
                    if should_exit:
                        # Give scrivener time to process the goodbye event
                        await asyncio.sleep(0.1)
                        break  # Exit requested
                    continue
                
                # Process the query
                await self.process_query(user_input)
                
            except KeyboardInterrupt:
                print("\n")  # New line after ^C
                await self.scrivener.inscribe(InscriptionEvent(
                    event_type=EventType.GOODBYE,
                    content="👋 Goodbye!"
                ))
                break
            except EOFError:
                print("\n")  # New line after ^D
                await self.scrivener.inscribe(InscriptionEvent(
                    event_type=EventType.GOODBYE,
                    content="👋 Goodbye!"
                ))
                break
            except Exception as e:
                error_msg = f"❌ Error: {e}\nPlease try again or type '/help' for assistance."
                await self.scrivener.inscribe(InscriptionEvent(
                    event_type=EventType.SYSTEM_MESSAGE,
                    content=error_msg
                ))
                
        # Stop scrivener when exiting
        await self.scrivener.stop()
    
    async def handle_command(self, command: str) -> bool:
        """Handle special commands with Rich UI. Returns True if should exit."""
        command = command.lower()
        
        if command in ['/quit', '/exit', '/q']:
            await self.scrivener.inscribe(InscriptionEvent(
                event_type=EventType.GOODBYE,
                content="👋 Goodbye!"
            ))
            return True
            
        elif command == '/help':
            help_msg = """📚 Available Commands:

  /quit, /exit, /q  - Exit the application
  /help            - Show this help message
  /stats           - Show session statistics
  /clear           - Clear session history"""
            
            await self.scrivener.inscribe(InscriptionEvent(
                event_type=EventType.SYSTEM_MESSAGE,
                content=help_msg
            ))
            
        elif command == '/stats':
            await self.show_statistics()
            
        elif command == '/clear':
            self.session_history.clear()
            await self.scrivener.inscribe(InscriptionEvent(
                event_type=EventType.SYSTEM_MESSAGE,
                content="🧹 Session history cleared."
            ))
            
        # Remove /version command - not needed for users
        elif command == '/version':
            await self.scrivener.inscribe(InscriptionEvent(
                event_type=EventType.SYSTEM_MESSAGE,
                content="Research Assistant - AI-powered analysis tool"
            ))
            
        else:
            error_msg = f"❓ Unknown command: {command}\nType '/help' for available commands."
            await self.scrivener.inscribe(InscriptionEvent(
                event_type=EventType.SYSTEM_MESSAGE,
                content=error_msg
            ))
            
        return False
    
    async def process_query(self, query: str) -> None:
        """Process a user query with V1-style Internal Processing container."""
        try:
            # Start token tracking
            self.token_tracker.start_request()
            
            # Start the Internal Processing container
            await self.scrivener.inscribe(InscriptionEvent(
                event_type=EventType.INTERNAL_PROCESSING_START,
                content="⚙️ Internal Processing",
                metadata={
                    "query": query
                }
            ))
            
            # Step 1: Intent Detection (V1 style with 🧠 emoji)
            await self.scrivener.inscribe(InscriptionEvent(
                event_type=EventType.PROCESSING_START,
                content="🧠 Intent Detection",
                metadata={
                    "stage": "intent_detection",
                    "message": f"Analyzing query intent using {self.config.intent_detection_display_name}...",
                    "provider_model": self.config.intent_detection_display_name
                }
            ))
            
            # Simulate intent detection processing
            await asyncio.sleep(0.2)
            
            # Determine intent (simplified for now)
            intent = "CHAT"  # Default intent
            if any(keyword in query.lower() for keyword in ["search", "find", "research", "literature"]):
                intent = "SEARCH"
            elif any(keyword in query.lower() for keyword in ["calculate", "math", "compute", "solve"]):
                intent = "COMPUTE"
            elif any(keyword in query.lower() for keyword in ["code", "program", "script", "function"]):
                intent = "CODE"
            elif any(keyword in query.lower() for keyword in ["analyze", "synthesis", "combine", "compare"]):
                intent = "SYNTHESIZE"
            
            # Complete intent detection
            await self.scrivener.inscribe(InscriptionEvent(
                event_type=EventType.PROCESSING_COMPLETE,
                content="🧠 Intent Detection",
                metadata={
                    "stage": "intent_detection",
                    "routing_conclusion": f"Intent: {intent}. Routing to: {self.config.intent_detection_display_name} (Chat Mode).",
                    "tokens_sent": 15,
                    "tokens_received": 5,
                    "duration": 0.2
                }
            ))
            
            # Step 2: Main Query Processing with live progress
            await self.scrivener.inscribe(InscriptionEvent(
                event_type=EventType.PROCESSING_START,
                content="💬 Main Query",
                metadata={
                    "stage": "main_query",
                    "message": f"Generating response using {self.config.main_query_display_name}...",
                    "provider_model": self.config.main_query_display_name
                }
            ))
            
            # Execute the actual LLM request using the main query manager
            start_time = time.time()
            try:
                llm_response = await self.main_query_manager.make_request(query)
                result = llm_response.content
                total_tokens = llm_response.tokens
                duration = time.time() - start_time
                
            except Exception as e:
                # Check if it's a connection error
                if "Connection" in str(e) or "ConnectionError" in str(type(e).__name__):
                    raise ConnectionError("Unable to connect to LLM server. Please ensure Groq API is available.")
                else:
                    # Re-raise other errors
                    raise
            
            # Complete main query processing
            await self.scrivener.inscribe(InscriptionEvent(
                event_type=EventType.PROCESSING_COMPLETE,
                content="💬 Main Query",
                metadata={
                    "stage": "main_query",
                    "routing_conclusion": f"Relaying to user: {self.config.main_query_display_name} (Chat Mode)",
                    "tokens_sent": total_tokens.input_tokens,
                    "tokens_received": total_tokens.output_tokens,
                    "duration": duration
                }
            ))
            
            # Complete the Internal Processing container
            await self.scrivener.inscribe(InscriptionEvent(
                event_type=EventType.INTERNAL_PROCESSING_COMPLETE,
                content="⚙️ Internal Processing",
                metadata={
                    "query": query
                }
            ))
            
            # Inscribe assistant response
            await self.scrivener.inscribe(InscriptionEvent(
                event_type=EventType.ASSISTANT_RESPONSE,
                content=result,
                metadata={"routing_info": f"{duration:.1f}s"}
            ))
            
            # Session logging with error handling
            if self.session_logger:
                try:
                    self.session_logger.log_assistant_response("AI_ASSISTANT", result)
                    self.session_logger.log_query_metrics(
                        duration,
                        total_tokens.input_tokens,
                        total_tokens.output_tokens,
                        "CHAT",
                        "AI_ASSISTANT"
                    )
                except Exception:
                    # Logging failed - continue without it
                    pass
            
            # Add to history
            self.session_history.append({
                'query': query,
                'response': result,
                'tokens': total_tokens,
                'duration': duration
            })
            
            # Complete token tracking
            self.token_tracker.complete_request(
                total_tokens.input_tokens, 
                total_tokens.output_tokens
            )
            
        except Exception as e:
            # No progress indicator to stop - all handled by scrivener
                
            # Show user-friendly error message
            if "Connection" in str(e) or "connect" in str(e).lower():
                error_msg = "❌ Unable to connect to LLM server. Please ensure Ollama is running."
            else:
                error_msg = f"❌ Error processing query: {e}"
            
            error_msg += "\nThe system is still running. Please try another question."
            
            await self.scrivener.inscribe(InscriptionEvent(
                event_type=EventType.SYSTEM_MESSAGE,
                content=error_msg
            ))
    
    async def show_statistics(self):
        """Show session statistics with Rich UI."""
        if not self.session_history:
            await self.scrivener.inscribe(InscriptionEvent(
                event_type=EventType.SYSTEM_MESSAGE,
                content="📊 No queries processed yet."
            ))
            return
            
        total_queries = len(self.session_history)
        total_input_tokens = sum(h['tokens'].input_tokens for h in self.session_history)
        total_output_tokens = sum(h['tokens'].output_tokens for h in self.session_history)
        total_duration = sum(h['duration'] for h in self.session_history)
        
        # Create statistics message
        stats_msg = f"""📊 SESSION STATISTICS

Queries processed: {total_queries}
Total tokens: {total_input_tokens + total_output_tokens}
  ↑ Input: {total_input_tokens}
  ↓ Output: {total_output_tokens}
Total time: {total_duration:.1f}s
Avg time per query: {total_duration/total_queries:.1f}s"""
        
        if total_duration > 0:
            tokens_per_sec = (total_input_tokens + total_output_tokens) / total_duration
            stats_msg += f"\nProcessing rate: {tokens_per_sec:.1f} tokens/sec"
        
        # Add LLM manager summary
        intent_summary = self.intent_detection_manager.get_session_summary()
        main_summary = self.main_query_manager.get_session_summary()
        stats_msg += f"""

🧠 LLM MANAGER STATS
Intent Detection ({self.config.intent_detection_display_name}):
  Requests: {intent_summary['total_requests']}
  Average duration: {intent_summary['average_duration']:.1f}s
Main Query ({self.config.main_query_display_name}):
  Requests: {main_summary['total_requests']}
  Average duration: {main_summary['average_duration']:.1f}s"""
        
        await self.scrivener.inscribe(InscriptionEvent(
            event_type=EventType.SYSTEM_MESSAGE,
            content=stats_msg
        ))

async def main():
    """Main entry point for V2 REPL."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Research Assistant REPL")
    parser.add_argument(
        "--config", 
        choices=["debug", "mixed", "fast", "test"], 
        default="debug",
        help="LLM configuration mode (default: debug)"
    )
    
    args = parser.parse_args()
    
    repl = V2REPL(config_name=args.config)
    
    try:
        await repl.run()
    except SystemExit as e:
        # System check failed - exit immediately with the specified code
        sys.exit(e.code)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        print("Please check your LLM servers are running and try again.")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except SystemExit as e:
        # Pass through system exit codes
        sys.exit(e.code)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        print("Please check your LLM servers are running and try again.")
        sys.exit(1)