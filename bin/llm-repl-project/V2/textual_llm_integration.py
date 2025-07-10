#!/usr/bin/env python3
"""
Textual LLM Integration - Connects Textual UI with existing LLM infrastructure

INTEGRATION APPROACH:
- Preserves your existing LLM interfaces and cognitive modules
- Integrates with your plugin architecture
- Maintains cognition blocks concept
- Uses Textual for bulletproof UI
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import (
    Header, Footer, Input, Static, Button, 
    RichLog, ProgressBar, Label, Markdown, Select
)
from textual.reactive import reactive
from textual.binding import Binding
from textual.css.query import NoMatches

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

import asyncio
import time
from typing import Optional, List, Dict, Any, AsyncGenerator
from dataclasses import dataclass
from enum import Enum
import uuid
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import existing LLM infrastructure
try:
    from plugins.llm_interface import LLMManager, MockLLMInterface
    from plugins.cognitive_modules import QueryRoutingModule, PromptEnhancementModule, CognitiveModuleInput
    from config.llm_config import CONFIGURATIONS
except ImportError as e:
    print(f"Warning: Could not import existing LLM infrastructure: {e}")
    print("Running in standalone mode with mock implementations")


class MessageType(Enum):
    """Types of messages in the conversation."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    COGNITION = "cognition"
    ERROR = "error"


@dataclass
class ConversationMessage:
    """A message in the conversation timeline."""
    id: str
    type: MessageType
    content: str
    timestamp: float
    metadata: Dict[str, Any]
    tokens: Dict[str, int] = None
    
    def __post_init__(self):
        if self.tokens is None:
            self.tokens = {"input": 0, "output": 0}


class EnhancedCognitionBlock:
    """
    Enhanced cognition block that integrates with your existing cognitive modules.
    
    PRESERVED: Your cognitive module architecture
    ENHANCED: Better streaming, error handling, progress tracking
    """
    
    def __init__(self, llm_manager: Optional[Any] = None):
        self.llm_manager = llm_manager or self._create_mock_llm_manager()
        self.cognitive_modules = [
            QueryRoutingModule(),
            PromptEnhancementModule()
        ]
        self.current_step = 0
        self.total_steps = len(self.cognitive_modules)
        self.total_tokens = {"input": 0, "output": 0}
        self.transparency_log = []
    
    def _create_mock_llm_manager(self):
        """Create mock LLM manager if real one not available."""
        try:
            manager = LLMManager()
            mock_interface = MockLLMInterface({
                "provider_name": "mock",
                "model_name": "mock-model"
            })
            manager.register_interface("default", mock_interface, is_default=True)
            return manager
        except:
            return None
    
    async def process(self, input_text: str) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Process input through cognitive modules with streaming updates.
        
        PRESERVED: Your multi-step cognitive processing
        ENHANCED: Streaming progress, better error handling
        """
        self.current_step = 0
        self.total_tokens = {"input": 0, "output": 0}
        self.transparency_log = []
        
        current_input = input_text
        
        # Yield initial status
        yield {
            "type": "status",
            "content": f"🧠 Starting cognition with {len(self.cognitive_modules)} modules...",
            "progress": 0.0,
            "step": 0,
            "total_steps": self.total_steps
        }
        
        try:
            for i, module in enumerate(self.cognitive_modules):
                self.current_step = i
                module_name = module.metadata.name
                
                # Yield step start
                yield {
                    "type": "step_start",
                    "content": f"🔄 Processing: {module_name}",
                    "progress": i / self.total_steps,
                    "step": i,
                    "total_steps": self.total_steps,
                    "module_name": module_name
                }
                
                try:
                    # Create module input (preserves your architecture)
                    module_input = CognitiveModuleInput(
                        content=current_input,
                        context={"step": i, "total_steps": self.total_steps}
                    )
                    
                    # Get LLM interface
                    llm_interface = self.llm_manager.get_interface("default") if self.llm_manager else None
                    
                    if llm_interface:
                        # Process through module (preserves your cognitive architecture)
                        module_output = await module.process(module_input, llm_interface)
                        
                        # Track results
                        self.transparency_log.append({
                            "module": module_name,
                            "step": i,
                            "input": current_input,
                            "output": module_output.content,
                            "tokens": {
                                "input": module_output.llm_response.tokens.input_tokens if module_output.llm_response else 0,
                                "output": module_output.llm_response.tokens.output_tokens if module_output.llm_response else 0
                            },
                            "timestamp": time.time()
                        })
                        
                        # Update token counts
                        if module_output.llm_response:
                            self.total_tokens["input"] += module_output.llm_response.tokens.input_tokens
                            self.total_tokens["output"] += module_output.llm_response.tokens.output_tokens
                        
                        # Use output as input for next module
                        current_input = module_output.content
                        
                        # Yield step completion
                        yield {
                            "type": "step_complete",
                            "content": f"✅ {module_name} complete",
                            "progress": (i + 1) / self.total_steps,
                            "step": i,
                            "total_steps": self.total_steps,
                            "module_name": module_name,
                            "module_output": module_output.content,
                            "tokens": module_output.llm_response.tokens.to_dict() if module_output.llm_response else {}
                        }
                    else:
                        # Mock processing if no LLM interface
                        await asyncio.sleep(0.5)  # Simulate processing
                        current_input = f"Enhanced: {current_input}"
                        
                        yield {
                            "type": "step_complete",
                            "content": f"✅ {module_name} complete (mock)",
                            "progress": (i + 1) / self.total_steps,
                            "step": i,
                            "total_steps": self.total_steps,
                            "module_name": module_name,
                            "module_output": current_input,
                            "tokens": {"input": 5, "output": 10}
                        }
                        
                        self.total_tokens["input"] += 5
                        self.total_tokens["output"] += 10
                
                except Exception as e:
                    # Log error but continue processing
                    error_log = {
                        "module": module_name,
                        "step": i,
                        "error": str(e),
                        "timestamp": time.time()
                    }
                    self.transparency_log.append(error_log)
                    
                    yield {
                        "type": "step_error",
                        "content": f"❌ {module_name} error: {str(e)}",
                        "progress": (i + 1) / self.total_steps,
                        "step": i,
                        "total_steps": self.total_steps,
                        "module_name": module_name,
                        "error": str(e)
                    }
            
            # Yield final result
            yield {
                "type": "final_result",
                "content": current_input,
                "progress": 1.0,
                "step": self.total_steps,
                "total_steps": self.total_steps,
                "tokens": self.total_tokens,
                "transparency_log": self.transparency_log
            }
            
        except Exception as e:
            yield {
                "type": "error",
                "content": f"Cognition error: {str(e)}",
                "progress": 0.0,
                "error": str(e)
            }


class MessageWidget(Static):
    """Enhanced message widget with better formatting."""
    
    def __init__(self, message: ConversationMessage, **kwargs):
        super().__init__(**kwargs)
        self.message = message
    
    def compose(self) -> ComposeResult:
        """Compose the message widget with enhanced formatting."""
        if self.message.type == MessageType.USER:
            content = Panel(
                self.message.content,
                title="👤 You",
                border_style="green",
                padding=(1, 2)
            )
        elif self.message.type == MessageType.ASSISTANT:
            tokens = self.message.tokens
            token_info = f" (↑{tokens['input']} ↓{tokens['output']})" if tokens and (tokens['input'] > 0 or tokens['output'] > 0) else ""
            content = Panel(
                self.message.content,
                title=f"🤖 Assistant{token_info}",
                border_style="blue",
                padding=(1, 2)
            )
        elif self.message.type == MessageType.COGNITION:
            # Enhanced cognition display with transparency
            transparency_log = self.message.metadata.get("transparency_log", [])
            
            if transparency_log:
                # Create table for transparency log
                table = Table(title="Cognition Process", show_header=True, header_style="bold magenta")
                table.add_column("Step", style="cyan", no_wrap=True)
                table.add_column("Module", style="green")
                table.add_column("Tokens", style="yellow", justify="right")
                table.add_column("Status", style="blue")
                
                for i, log_entry in enumerate(transparency_log):
                    if "error" in log_entry:
                        status = f"❌ {log_entry['error']}"
                        tokens = "N/A"
                    else:
                        status = "✅ Complete"
                        token_data = log_entry.get("tokens", {})
                        tokens = f"↑{token_data.get('input', 0)} ↓{token_data.get('output', 0)}"
                    
                    table.add_row(
                        str(i + 1),
                        log_entry.get("module", "Unknown"),
                        tokens,
                        status
                    )
                
                content = Panel(
                    table,
                    title="🧠 Cognition Process",
                    border_style="purple",
                    padding=(1, 2)
                )
            else:
                content = Panel(
                    self.message.content,
                    title="🧠 Cognition",
                    border_style="purple",
                    padding=(1, 2)
                )
        elif self.message.type == MessageType.SYSTEM:
            content = Panel(
                self.message.content,
                title="⚙️ System",
                border_style="yellow",
                padding=(1, 2)
            )
        else:  # ERROR
            content = Panel(
                self.message.content,
                title="❌ Error",
                border_style="red",
                padding=(1, 2)
            )
        
        yield Static(content)


class ConfigWidget(Container):
    """Widget for configuration selection."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_config = "debug"
    
    def compose(self) -> ComposeResult:
        """Compose the configuration widget."""
        with Horizontal():
            yield Label("Config:")
            yield Select(
                [
                    ("Debug", "debug"),
                    ("Mixed", "mixed"),
                    ("Fast", "fast"),
                    ("Test", "test")
                ],
                value="debug",
                id="config_select"
            )
    
    def on_select_changed(self, event: Select.Changed) -> None:
        """Handle configuration change."""
        if event.select.id == "config_select":
            self.current_config = event.value
            # Emit custom message to parent
            self.post_message(ConfigChanged(self.current_config))


class ConfigChanged(Message):
    """Message sent when configuration changes."""
    
    def __init__(self, config: str) -> None:
        self.config = config
        super().__init__()


class EnhancedLLMREPLApp(App):
    """
    Enhanced LLM REPL App with full integration.
    
    MASSIVE IMPROVEMENT:
    - Integrates with your existing LLM infrastructure
    - Preserves cognition blocks architecture
    - Professional Textual interface
    - Real-time progress tracking
    - Configuration management
    """
    
    CSS = """
    Screen {
        layout: vertical;
    }
    
    #header_container {
        height: 3;
        border: solid $primary;
        margin: 1;
    }
    
    #main_container {
        layout: vertical;
        height: 1fr;
    }
    
    #timeline_container {
        height: 1fr;
        border: solid $primary;
        margin: 1;
    }
    
    #input_container {
        height: auto;
        min-height: 4;
        border: solid $accent;
        margin: 1;
    }
    
    #status_container {
        height: 4;
        border: solid $secondary;
        margin: 1;
    }
    
    Input {
        width: 1fr;
    }
    
    ProgressBar {
        width: 30;
    }
    
    MessageWidget {
        margin: 1 0;
    }
    
    Select {
        width: 15;
    }
    """
    
    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit"),
        Binding("ctrl+l", "clear_timeline", "Clear"),
        Binding("f1", "show_help", "Help"),
        Binding("f2", "show_stats", "Stats"),
    ]
    
    def __init__(self, config_name: str = "debug", **kwargs):
        super().__init__(**kwargs)
        self.config_name = config_name
        self.timeline = []
        self.message_ids = set()
        self.llm_manager = self._setup_llm_manager()
        self.cognition_block = EnhancedCognitionBlock(self.llm_manager)
        self.is_processing = False
        self.total_tokens = {"input": 0, "output": 0}
    
    def _setup_llm_manager(self):
        """Setup LLM manager with configuration."""
        try:
            manager = LLMManager()
            
            # Get configuration
            config = CONFIGURATIONS.get(self.config_name, CONFIGURATIONS.get("debug"))
            if config:
                # Create interfaces based on configuration
                intent_interface = MockLLMInterface({
                    "provider_name": config.intent_detection_provider.value,
                    "model_name": config.intent_detection_model
                })
                main_interface = MockLLMInterface({
                    "provider_name": config.main_query_provider.value,
                    "model_name": config.main_query_model
                })
                
                manager.register_interface("intent_detection", intent_interface)
                manager.register_interface("main_query", main_interface, is_default=True)
                manager.register_interface("default", main_interface)
            else:
                # Fallback to basic mock
                mock_interface = MockLLMInterface({"provider_name": "mock", "model_name": "mock-model"})
                manager.register_interface("default", mock_interface, is_default=True)
            
            return manager
        except Exception as e:
            print(f"Warning: Could not setup LLM manager: {e}")
            return None
    
    def compose(self) -> ComposeResult:
        """Compose the main application layout."""
        yield Header()
        
        # Configuration header
        with Container(id="header_container"):
            yield ConfigWidget(id="config_widget")
        
        with Container(id="main_container"):
            # Timeline area
            with Container(id="timeline_container"):
                yield ScrollableContainer(id="timeline")
            
            # Input area
            with Container(id="input_container"):
                with Vertical():
                    yield Label("💬 Type your message (Enter to send)")
                    yield Input(placeholder="Ask me anything...", id="user_input")
            
            # Status area
            with Container(id="status_container"):
                with Vertical():
                    with Horizontal():
                        yield Label("📊 Status:", id="status_label")
                        yield Label("Ready", id="status_text")
                        yield ProgressBar(total=100, show_eta=False, id="progress_bar")
                    with Horizontal():
                        yield Label("🔢 Tokens:", id="token_label")
                        yield Label("↑0 ↓0", id="token_count")
                        yield Label("⚡ Config:", id="config_label")
                        yield Label(self.config_name, id="current_config")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Called when the app is mounted."""
        self.title = "LLM REPL - Enhanced Textual Interface"
        self.sub_title = f"Configuration: {self.config_name}"
        
        # Focus the input
        self.query_one("#user_input", Input).focus()
        
        # Add welcome message
        self.add_message(
            MessageType.SYSTEM,
            f"Welcome to Enhanced LLM REPL!\nConfiguration: {self.config_name}\nCognitive modules: {len(self.cognition_block.cognitive_modules)}\n\nType your message below and press Enter to start chatting.",
            {"source": "system", "config": self.config_name}
        )
    
    def add_message(self, msg_type: MessageType, content: str, metadata: Dict[str, Any], tokens: Dict[str, int] = None):
        """Add a message to the timeline (with deduplication)."""
        message_id = str(uuid.uuid4())
        
        # Prevent duplicates
        if message_id in self.message_ids:
            return
        
        message = ConversationMessage(
            id=message_id,
            type=msg_type,
            content=content,
            timestamp=time.time(),
            metadata=metadata,
            tokens=tokens or {"input": 0, "output": 0}
        )
        
        self.timeline.append(message)
        self.message_ids.add(message_id)
        
        # Update total tokens
        if tokens:
            self.total_tokens["input"] += tokens.get("input", 0)
            self.total_tokens["output"] += tokens.get("output", 0)
        
        # Add to UI
        timeline_container = self.query_one("#timeline", ScrollableContainer)
        widget = MessageWidget(message, id=f"msg_{message_id}")
        timeline_container.mount(widget)
        
        # Auto-scroll to bottom
        timeline_container.scroll_end(animate=True)
        
        # Update token display
        self.update_token_display()
    
    def update_token_display(self):
        """Update the token count display."""
        try:
            token_count = self.query_one("#token_count", Label)
            token_count.update(f"↑{self.total_tokens['input']} ↓{self.total_tokens['output']}")
        except NoMatches:
            pass
    
    def update_status(self, text: str, progress: float = 0.0):
        """Update the status display."""
        try:
            status_text = self.query_one("#status_text", Label)
            status_text.update(text)
            
            progress_bar = self.query_one("#progress_bar", ProgressBar)
            progress_bar.progress = int(progress * 100)
        except NoMatches:
            pass
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission."""
        if event.input.id == "user_input" and not self.is_processing:
            user_input = event.value.strip()
            if user_input:
                # Clear input immediately
                event.input.value = ""
                
                # Process the input
                self.run_worker(self.process_user_input(user_input))
    
    async def process_user_input(self, user_input: str):
        """Process user input through the enhanced cognition block."""
        self.is_processing = True
        
        try:
            # Add user message
            self.add_message(
                MessageType.USER,
                user_input,
                {"source": "user"}
            )
            
            # Process through cognition block with streaming
            cognition_steps = []
            final_result = ""
            cognition_tokens = {"input": 0, "output": 0}
            transparency_log = []
            
            async for update in self.cognition_block.process(user_input):
                update_type = update.get("type", "unknown")
                content = update.get("content", "")
                progress = update.get("progress", 0.0)
                
                if update_type == "status":
                    self.update_status(content, progress)
                elif update_type == "step_start":
                    self.update_status(content, progress)
                elif update_type == "step_complete":
                    step_info = f"✅ {update.get('module_name', 'Unknown')} complete"
                    cognition_steps.append(step_info)
                    self.update_status(step_info, progress)
                    
                    # Update tokens
                    step_tokens = update.get("tokens", {})
                    cognition_tokens["input"] += step_tokens.get("input", 0)
                    cognition_tokens["output"] += step_tokens.get("output", 0)
                elif update_type == "step_error":
                    error_info = f"❌ {update.get('module_name', 'Unknown')}: {update.get('error', 'Unknown error')}"
                    cognition_steps.append(error_info)
                    self.update_status(error_info, progress)
                elif update_type == "final_result":
                    final_result = content
                    cognition_tokens = update.get("tokens", cognition_tokens)
                    transparency_log = update.get("transparency_log", [])
                    self.update_status("✅ Processing complete", 1.0)
                elif update_type == "error":
                    self.add_message(
                        MessageType.ERROR,
                        content,
                        {"source": "cognition", "error": update.get("error", "Unknown error")}
                    )
                    self.update_status("❌ Error occurred", 0.0)
                    return
            
            # Add cognition message if there are steps
            if cognition_steps:
                cognition_content = "\n".join(cognition_steps)
                self.add_message(
                    MessageType.COGNITION,
                    cognition_content,
                    {
                        "source": "cognition",
                        "steps": len(cognition_steps),
                        "transparency_log": transparency_log
                    },
                    cognition_tokens
                )
            
            # Add assistant response
            if final_result:
                self.add_message(
                    MessageType.ASSISTANT,
                    final_result,
                    {"source": "assistant", "cognition_tokens": cognition_tokens},
                    cognition_tokens
                )
            
            self.update_status("✅ Ready", 0.0)
            
        except Exception as e:
            self.add_message(
                MessageType.ERROR,
                f"Error processing request: {str(e)}",
                {"source": "error", "error_type": type(e).__name__}
            )
            self.update_status("❌ Error occurred", 0.0)
        
        finally:
            self.is_processing = False
            # Refocus input
            self.query_one("#user_input", Input).focus()
    
    def on_config_changed(self, event: ConfigChanged) -> None:
        """Handle configuration change."""
        self.config_name = event.config
        self.sub_title = f"Configuration: {self.config_name}"
        
        # Update config display
        try:
            current_config = self.query_one("#current_config", Label)
            current_config.update(self.config_name)
        except NoMatches:
            pass
        
        # Reinitialize LLM manager
        self.llm_manager = self._setup_llm_manager()
        self.cognition_block = EnhancedCognitionBlock(self.llm_manager)
        
        # Add system message
        self.add_message(
            MessageType.SYSTEM,
            f"Configuration changed to: {self.config_name}",
            {"source": "system", "config_change": self.config_name}
        )
    
    def action_clear_timeline(self) -> None:
        """Clear the conversation timeline."""
        # Clear data
        self.timeline.clear()
        self.message_ids.clear()
        self.total_tokens = {"input": 0, "output": 0}
        
        # Clear UI
        timeline_container = self.query_one("#timeline", ScrollableContainer)
        timeline_container.remove_children()
        
        # Update displays
        self.update_token_display()
        self.update_status("✅ Ready", 0.0)
        
        # Add welcome message back
        self.add_message(
            MessageType.SYSTEM,
            "Timeline cleared. Ready for new conversation!",
            {"source": "system"}
        )
    
    def action_show_help(self) -> None:
        """Show help information."""
        help_content = """
**Enhanced LLM REPL Help**

**Keyboard Shortcuts:**
- Enter: Send message
- Ctrl+C: Quit application
- Ctrl+L: Clear timeline
- F1: Show this help
- F2: Show statistics

**Features:**
- Real-time conversation with AI
- Multi-step cognition processing
- Token usage tracking
- Configuration management
- Professional GUI interface
- Transparency logging

**Cognition Process:**
The system uses cognitive modules for enhanced processing:
1. Query Routing - Analyzes and routes your query
2. Prompt Enhancement - Optimizes the prompt for better results

Type your message in the input box and press Enter to start chatting!
        """.strip()
        
        self.add_message(
            MessageType.SYSTEM,
            help_content,
            {"source": "help"}
        )
    
    def action_show_stats(self) -> None:
        """Show statistics."""
        stats_content = f"""
**Session Statistics**

**Messages:** {len(self.timeline)}
**Total Tokens:** ↑{self.total_tokens['input']} ↓{self.total_tokens['output']}
**Configuration:** {self.config_name}
**Cognitive Modules:** {len(self.cognition_block.cognitive_modules)}

**Message Breakdown:**
- User: {len([m for m in self.timeline if m.type == MessageType.USER])}
- Assistant: {len([m for m in self.timeline if m.type == MessageType.ASSISTANT])}
- System: {len([m for m in self.timeline if m.type == MessageType.SYSTEM])}
- Cognition: {len([m for m in self.timeline if m.type == MessageType.COGNITION])}
- Errors: {len([m for m in self.timeline if m.type == MessageType.ERROR])}
        """.strip()
        
        self.add_message(
            MessageType.SYSTEM,
            stats_content,
            {"source": "stats"}
        )


async def main():
    """Main entry point for the Enhanced Textual LLM REPL."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced LLM REPL with Textual Interface")
    parser.add_argument(
        '--config', '-c',
        choices=['debug', 'mixed', 'fast', 'test'],
        default='debug',
        help='Configuration to use'
    )
    
    args = parser.parse_args()
    
    app = EnhancedLLMREPLApp(config_name=args.config)
    await app.run_async()


if __name__ == "__main__":
    asyncio.run(main())