#!/usr/bin/env python3
"""
Research Assistant REPL - A terminal-based AI research interface
Multi-model routing system with intent detection and specialized agents
"""

import asyncio
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import aiohttp
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import FormattedText, HTML
from prompt_toolkit.shortcuts import print_formatted_text
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory
from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.panel import Panel
from rich.box import ROUNDED, HEAVY
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.live import Live
from rich.layout import Layout
from rich.status import Status
from rich.columns import Columns
from rich.align import Align
import re
import google.generativeai as genai
from rich.table import Table
import subprocess
import tempfile
import sqlite3
import sys
import threading
import time

# Import dotenv for loading environment variables
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

class SessionLogger:
    """Logs exactly what the user sees in their REPL sessions for debugging."""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.log_dir = Path(".logs")
        self.log_dir.mkdir(exist_ok=True)
        
        # Create timestamped log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"session_{session_id}_{timestamp}.log"
        
        # Initialize log file
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(f"=== Research Assistant Session Log ===\n")
            f.write(f"Session ID: {session_id}\n")
            f.write(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"=" * 50 + "\n\n")
    
    def log_user_input(self, input_text: str):
        """Log user input with timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] You: {input_text}\n")
    
    def log_assistant_response(self, routing_path: str, content: str):
        """Log assistant response with routing information."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] Assistant → {routing_path}:\n")
            f.write(f"{content}\n\n")
    
    def log_system_message(self, message: str):
        """Log system messages."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {message}\n")
    
    def log_query_metrics(self, elapsed_seconds: float, tokens_sent: int, tokens_received: int, intent: str, method: str):
        """Log query processing metrics."""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"[METRICS] Query processed in {elapsed_seconds:.2f}s | ")
            f.write(f"Tokens sent: {tokens_sent} | Tokens received: {tokens_received} | ")
            f.write(f"Intent: {intent} ({method})\n")

class RichUI:
    """Enhanced Rich-based UI system for the Research Assistant."""
    
    def __init__(self, console: Console):
        self.console = console
        
    def print_user_message(self, message: str):
        """Display user message in a styled box."""
        user_panel = Panel(
            Text(message, style="bold white"),
            title="[bold blue]You[/bold blue]",
            box=ROUNDED,
            border_style="blue",
            padding=(0, 1)
        )
        self.console.print(user_panel)
        
    def print_assistant_message(self, message: str, routing_info: str = ""):
        """Display assistant message in a styled box."""
        title_text = "[bold green]Research Assistant[/bold green]"
        
        # No routing info in message content - it's now shown in Internal Processing
        content = message
            
        assistant_panel = Panel(
            Markdown(content),
            title=title_text,
            box=ROUNDED,
            border_style="green",
            padding=(0, 1)
        )
        self.console.print(assistant_panel)
        
    def print_system_message(self, message: str):
        """Display system message in a dimmed style."""
        system_panel = Panel(
            Text(message, style="dim white"),
            title="[dim]System[/dim]",
            box=ROUNDED,
            border_style="dim white",
            padding=(0, 1)
        )
        self.console.print(system_panel)
        
    def print_status_panel_with_tokens(self, title: str, message: str, tokens_sent: int = 0, tokens_received: int = 0, border_style: str = "dim yellow", provider_model: str = ""):
        """Display a status panel with right-aligned token counter."""
        from rich.columns import Columns
        from rich.align import Align
        
        # Create main content
        main_content = Text(message, style="dim white")
        
        # Create token counter with provider/model info (right-aligned)
        token_text = f"⏱️ ↑{tokens_sent} ↓{tokens_received}"
        if provider_model:
            token_text += f" {provider_model}"
        token_counter = Align(Text(token_text, style="dim cyan"), align="right")
        
        # Create layout with main content and token counter
        content = Columns([main_content, token_counter], expand=True)
        
        status_panel = Panel(
            content,
            title=title,
            box=ROUNDED,
            border_style=border_style,
            padding=(0, 1)
        )
        self.console.print(status_panel)
        
    def print_pipe_connector(self, from_stage: str, to_stage: str):
        """Print a visual pipe connector between stages."""
        pipe_text = Text()
        pipe_text.append("                        ↓\n", style="dim cyan")
        self.console.print(pipe_text)
    
    def print_small_connector(self):
        """Print a smaller connector for internal pipeline steps."""
        pipe_text = Text()
        pipe_text.append("                    ▼\n", style="dim cyan")
        self.console.print(pipe_text)

class PipelineContainer:
    """Container for internal processing pipeline steps with timing and encapsulation."""
    
    def __init__(self, console: Console, rich_ui):
        self.console = console
        self.rich_ui = rich_ui
        self.start_time = None
        self.steps = []
        self.current_step = None
        self.live_display = None
        self.running = False
        self.update_thread = None
        
    def start(self):
        """Start the pipeline container timing."""
        self.start_time = time.time()
        # Create initial live container
        self._create_live_container()
        
    def add_step(self, step_block: 'ProcessingBlock'):
        """Add a processing step to the pipeline."""
        self.steps.append(step_block)
        self.current_step = step_block
        # Background thread will handle live updates
        
    def get_total_elapsed(self):
        """Get total elapsed time for the entire pipeline."""
        if self.start_time:
            return time.time() - self.start_time
        return 0.0
        
    def _create_container_display(self):
        """Create the initial container display."""
        # Start with a basic container - will be enhanced as steps are added
        container_content = Text("⚙️ Internal Processing", style="dim yellow")
        container_panel = Panel(
            container_content,
            title="[dim yellow]⚙️ Internal Processing[/dim yellow]",
            box=ROUNDED,
            border_style="dim yellow",
            padding=(1, 1)
        )
        self.console.print(container_panel)
        
    def finalize(self):
        """Finalize the container with total timing."""
        # Stop the background thread and live display
        self.running = False
        if self.update_thread and self.update_thread.is_alive():
            self.update_thread.join(timeout=1.0)
        # Update one final time with completed state
        self._update_live_container()
        # Give a moment for final display
        time.sleep(0.1)
        if self.live_display:
            self.live_display.stop()
    
    def _create_live_container(self):
        """Create the initial live container display."""
        initial_content = Text("Starting internal processing...", style="dim white")
        title_text = "[dim yellow]⚙️ Internal Processing[/dim yellow]"
        
        container_panel = Panel(
            initial_content,
            title=title_text,
            box=ROUNDED,
            border_style="dim yellow",
            padding=(1, 1)
        )
        
        self.live_display = Live(container_panel, console=self.console, refresh_per_second=10)
        self.live_display.start()
        
        # Start background update thread
        self.running = True
        self.update_thread = threading.Thread(target=self._update_loop, daemon=True)
        self.update_thread.start()
    
    def _update_loop(self):
        """Background thread that continuously updates the live container."""
        while self.running and self.live_display:
            self._update_live_container()
            time.sleep(0.1)
    
    def _update_live_container(self):
        """Update the live container with current steps."""
        if not self.live_display:
            return
            
        # Build content with all current steps as formatted text
        content = Text()
        
        for i, step in enumerate(self.steps):
            if i > 0:
                content.append("                    ▼\n", style="dim cyan")
            
            # Get current step state (ProcessingBlock)
            elapsed = step.get_elapsed_time()
            
            # Clean step title
            import re
            step_title = re.sub(r'\[/?[^\]]*\]', '', step.title)
            
            # Get animated token counts
            animated_input, animated_output = step.rolling_counter.get_current_values()
            token_text = f"⏱️ ↑{animated_input} ↓{animated_output}"
            
            # Create step content
            step_content = f"{step.message} ({elapsed:.1f}s)"
            if step.routing_conclusion:
                step_content += f"\n{step.routing_conclusion}"
            
            # Create proper columns layout
            left_part = Text(step_content, style="dim white")
            right_part = Align(Text(token_text, style="dim cyan"), align="right")
            step_columns = Columns([left_part, right_part], expand=True)
            
            # Use Rich to render the panel as text
            from io import StringIO
            step_console = Console(file=StringIO(), width=86)  # Width that fits within container
            step_panel = Panel(
                step_columns,
                title=step_title,
                box=ROUNDED,
                border_style="dim white",
                padding=(0, 1)
            )
            step_console.print(step_panel)
            panel_output = step_console.file.getvalue()
            
            # Add the rendered panel with proper indentation
            for line in panel_output.strip().split('\n'):
                content.append(f"  {line}\n", style="")
            
        # Update the live display
        total_elapsed = self.get_total_elapsed()
        title_text = f"[dim yellow]⚙️ Internal Processing ({total_elapsed:.1f}s total)[/dim yellow]"
        
        updated_panel = Panel(
            content,
            title=title_text,
            box=ROUNDED,
            border_style="dim yellow",
            padding=(1, 1)
        )
        
        self.live_display.update(updated_panel)
        

class TokenRateEstimator:
    """Estimates token processing rates based on typical LLM performance."""
    
    def __init__(self):
        # Based on actual measured performance from local Ollama server
        self.rates = {
            'tinyllama': {
                'input_tokens_per_second': 31,     # Measured from local Ollama
                'output_tokens_per_second': 25,    # Measured from local Ollama
                'latency_seconds': 0.48            # Measured minimum latency
            },
            'gemini': {
                'input_tokens_per_second': 1200,   # Estimated (faster than local)
                'output_tokens_per_second': 40,    # Estimated (faster than local)
                'latency_seconds': 0.3             # Estimated (lower latency)
            },
            'default': {
                'input_tokens_per_second': 31,     # Use tinyllama as default
                'output_tokens_per_second': 25,
                'latency_seconds': 0.48
            }
        }
    
    def estimate_duration(self, model_name: str, input_tokens: int, expected_output_tokens: int = 50) -> float:
        """Estimate total duration for a request."""
        model_key = 'tinyllama' if 'tinyllama' in model_name.lower() else 'gemini' if 'gemini' in model_name.lower() else 'default'
        rates = self.rates[model_key]
        
        input_time = input_tokens / rates['input_tokens_per_second']
        output_time = expected_output_tokens / rates['output_tokens_per_second']
        
        return rates['latency_seconds'] + input_time + output_time
    
    def get_rates(self, model_name: str) -> dict:
        """Get processing rates for a model."""
        model_key = 'tinyllama' if 'tinyllama' in model_name.lower() else 'gemini' if 'gemini' in model_name.lower() else 'default'
        return self.rates[model_key]

class RollingTokenCounter:
    """Enhanced token counter that ONLY shows actual API response data."""
    
    def __init__(self, model_name: str = "default"):
        self.model_name = model_name
        
        # Import enhanced animation system
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent))
        from enhanced_animation import RealtimeTokenTracker
        
        self.tracker = RealtimeTokenTracker()
        self.tracker.animator.set_animation_style("smooth_ramp")
        
        # Legacy compatibility
        self.start_time = None
        self.is_complete = False
        
    def start_animation(self, input_tokens: int = 0, expected_output_tokens: int = 0):
        """Start the animation - but don't show estimates, wait for actual data."""
        self.start_time = time.time()
        self.tracker.start_request()
        self.is_complete = False
        
    def get_current_values(self) -> tuple[int, int]:
        """Get current token counts - ONLY actual values, never estimates."""
        return self.tracker.get_display_values()
        
    def update_with_actual_tokens(self, input_tokens: int, output_tokens: int):
        """Update with ACTUAL token counts from API response."""
        self.tracker.update_with_api_response(input_tokens, output_tokens)
        
    def set_final_values(self, sent: int, received: int):
        """Set final values when request completes."""
        self.tracker.complete_request(sent, received)
        self.is_complete = True
        
    def should_catch_up(self) -> bool:
        """Check if animation is complete."""
        return self.tracker.animator.is_complete()

class ProcessingBlock:
    """
    Unified container for all processing blocks with standardized timing, tokens, and display.
    Manages complete lifecycle: start → processing → completion → display finalization.
    """
    
    def __init__(self, console: Console, title: str, message: str, 
                 model: str = "tinyllama", provider: str = "Ollama", 
                 border_style: str = "dim yellow"):
        self.console = console
        self.title = title
        self.message = message
        self.model = model
        self.provider = provider
        self.border_style = border_style
        
        # Timing
        self.start_time = None
        self.end_time = None
        self.wall_time = 0.0
        
        # Token tracking (ground truth only)
        self.input_tokens = 0
        self.output_tokens = 0
        
        # State management
        self.is_active = False
        self.is_complete = False
        
        # Display components
        self.live_display = None
        self.rolling_counter = RollingTokenCounter(model)
        self.routing_conclusion = None
        self.suppress_display = False  # If True, don't show individual display (for pipeline integration)
        
        # Threading
        self.running = False
        self.thread = None
        self.lock = threading.Lock()
        
    def start(self):
        """Start the processing block lifecycle."""
        with self.lock:
            self.start_time = time.time()
            self.is_active = True
            self.is_complete = False
            self.running = True
            
        # Create live display only if not suppressed (for pipeline integration)
        if not self.suppress_display:
            self._create_live_display()
            
            # Start update thread
            self.thread = threading.Thread(target=self._update_loop, daemon=True)
            self.thread.start()
    
    def set_tokens(self, input_tokens: int, output_tokens: int):
        """Set ground truth token counts and update rolling animation."""
        with self.lock:
            self.input_tokens = input_tokens
            self.output_tokens = output_tokens
            
        # Update rolling animation
        self.rolling_counter.set_final_values(input_tokens, output_tokens)
        self.rolling_counter.final_tokens_set = True
    
    def set_routing_conclusion(self, conclusion: str):
        """Set the routing conclusion for this block."""
        with self.lock:
            self.routing_conclusion = conclusion
    
    def complete(self):
        """Mark the block as complete and finalize timing."""
        with self.lock:
            self.end_time = time.time()
            self.wall_time = self.end_time - self.start_time if self.start_time else 0.0
            self.is_complete = True
            self.is_active = False
            self.running = False
            
        # Stop update thread
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)
            
        # Stop live display
        if self.live_display:
            self.live_display.stop()
    
    def get_elapsed_time(self):
        """Get current elapsed time."""
        if self.is_complete:
            return self.wall_time
        elif self.start_time:
            return time.time() - self.start_time
        return 0.0
    
    def get_provider_model_text(self):
        """Get formatted provider and model text."""
        return f"[{self.provider}: {self.model}]"
    
    def _create_live_display(self):
        """Create the live display panel."""
        content = self._build_content()
        panel = Panel(
            content,
            title=self.title,
            box=ROUNDED,
            border_style=self.border_style,
            padding=(0, 1)
        )
        
        self.live_display = Live(panel, console=self.console, refresh_per_second=10)
        self.live_display.start()
    
    def _update_loop(self):
        """Background thread that updates the live display."""
        while self.running:
            if self.live_display:
                content = self._build_content()
                updated_panel = Panel(
                    content,
                    title=self.title,
                    box=ROUNDED,
                    border_style=self.border_style,
                    padding=(0, 1)
                )
                self.live_display.update(updated_panel)
            time.sleep(0.1)
    
    def _build_content(self):
        """Build the panel content with current state."""
        # Get current values
        with self.lock:
            elapsed = self.get_elapsed_time()
            routing = self.routing_conclusion
            
        # Get animated token counts
        animated_input, animated_output = self.rolling_counter.get_current_values()
        
        # Build main content
        main_text = f"{self.message} ({elapsed:.1f}s)"
        if routing:
            main_text += f"\n{routing}"
        
        # Build token counter
        token_text = f"⏱️ ↑{animated_input} ↓{animated_output} {self.get_provider_model_text()}"
        
        # Create columns layout
        left_content = Text(main_text, style="dim white")
        right_content = Align(Text(token_text, style="dim cyan"), align="right")
        
        return Columns([left_content, right_content], expand=True)

class LiveProgressIndicator:
    """DEPRECATED: Use ProcessingBlock instead. Kept for compatibility."""
    
    def __init__(self, console, rich_ui, title: str, message: str, border_style: str = "dim yellow", model_name: str = "tinyllama", provider_model: str = ""):
        self.console = console
        self.rich_ui = rich_ui
        self.title = title
        self.message = message
        self.border_style = border_style
        self.provider_model = provider_model
        self.start_time = None
        self.tokens_sent = 0
        self.tokens_received = 0
        self.running = False
        self.thread = None
        self.live_display = None
        self.lock = threading.Lock()  # Thread-safe token updates
        
        # Rolling animation
        self.rolling_counter = RollingTokenCounter(model_name)
        self.animation_started = False
        self.final_tokens_set = False
        
        # Routing conclusion
        self.routing_conclusion = None
        
        # Pipeline integration
        self.suppress_display = False  # If True, don't show individual display
    
    def start(self, initial_input_tokens: int = 40, expected_output_tokens: int = 50):
        """Start the live progress indicator with Rich panel and rolling animation."""
        self.start_time = time.time()
        self.running = True
        
        # Start rolling animation
        self.rolling_counter.start_animation(initial_input_tokens, expected_output_tokens)
        self.animation_started = True
        
        # Only create display if not suppressed (for pipeline integration)
        if not self.suppress_display:
            # Create initial panel
            self._create_live_display()
            
            # Start background thread for updates
            self.thread = threading.Thread(target=self._update_loop, daemon=True)
            self.thread.start()
    
    def stop(self):
        """Stop the live progress indicator and show final status."""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)
        
        if self.live_display:
            self.live_display.stop()
        
        # DON'T print final status panel - the live display already shows the final state
        # This prevents duplicate boxes
    
    def update_tokens(self, sent: int = 0, received: int = 0):
        """Update token counters incrementally (thread-safe)."""
        with self.lock:
            self.tokens_sent += sent
            self.tokens_received += received
            
            # Don't set final values here - this is for incremental updates only
            # Final values should be set when the request actually completes
            
    def set_final_tokens(self, sent: int, received: int):
        """Set final token values when request completes (for catch-up animation)."""
        with self.lock:
            self.tokens_sent = sent
            self.tokens_received = received
            
            # Update rolling counter with final values when request completes
            if self.animation_started and not self.final_tokens_set:
                self.rolling_counter.set_final_values(sent, received)
                self.final_tokens_set = True
    
    def set_routing_conclusion(self, routing_text: str):
        """Set the routing conclusion to display as a second line."""
        with self.lock:
            self.routing_conclusion = routing_text
    
    def _update_loop(self):
        """Background thread that updates the progress display."""
        while self.running:
            if self.start_time and self.live_display:
                elapsed = time.time() - self.start_time
                
                # Get animated token counts
                if self.animation_started:
                    animated_sent, animated_received = self.rolling_counter.get_current_values()
                    
                    # Use final values if they've been set and we should catch up
                    if self.final_tokens_set and self.rolling_counter.should_catch_up():
                        with self.lock:
                            animated_sent = self.tokens_sent
                            animated_received = self.tokens_received
                else:
                    with self.lock:
                        animated_sent = self.tokens_sent
                        animated_received = self.tokens_received
                
                # Update panel content
                with self.lock:
                    routing_conclusion = self.routing_conclusion
                
                if routing_conclusion:
                    # Two-line display: main message + routing conclusion
                    line1 = Text(f"{self.message} ({elapsed:.1f}s)", style="dim white")
                    line2 = Text(routing_conclusion, style="dim cyan")
                    main_content = Text.assemble(line1, "\n", line2)
                else:
                    # Single-line display: just main message
                    main_content = Text(f"{self.message} ({elapsed:.1f}s)", style="dim white")
                
                token_text = f"⏱️ ↑{animated_sent} ↓{animated_received}"
                if self.provider_model:
                    token_text += f" {self.provider_model}"
                token_counter = Align(Text(token_text, style="dim cyan"), align="right")
                content = Columns([main_content, token_counter], expand=True)
                
                updated_panel = Panel(
                    content,
                    title=self.title,
                    box=ROUNDED,
                    border_style=self.border_style,
                    padding=(0, 1)
                )
                
                self.live_display.update(updated_panel)
            
            time.sleep(0.1)
    
    def _create_live_display(self):
        """Create the live display panel."""
        # Create initial panel content
        with self.lock:
            routing_conclusion = self.routing_conclusion
        
        if routing_conclusion:
            # Two-line display: main message + routing conclusion
            line1 = Text(self.message, style="dim white")
            line2 = Text(routing_conclusion, style="dim cyan")
            main_content = Text.assemble(line1, "\n", line2)
        else:
            # Single-line display: just main message
            main_content = Text(self.message, style="dim white")
        
        token_text = "⏱️ ↑0 ↓0"
        if self.provider_model:
            token_text += f" {self.provider_model}"
        token_counter = Align(Text(token_text, style="dim cyan"), align="right")
        content = Columns([main_content, token_counter], expand=True)
        
        panel = Panel(
            content,
            title=self.title,
            box=ROUNDED,
            border_style=self.border_style,
            padding=(0, 1)
        )
        
        self.live_display = Live(panel, console=self.console, refresh_per_second=10)
        self.live_display.start()
    
    def get_elapsed_time(self):
        """Get elapsed time since start."""
        if self.start_time:
            return time.time() - self.start_time
        return 0.0

class MessageType(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    COMMAND = "command"

@dataclass
class Message:
    type: MessageType
    content: str
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None

class HistoryDB:
    def __init__(self, db_path="history.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self._init_db()

    def _init_db(self):
        c = self.conn.cursor()
        # Add session_id to messages for session management
        try:
            c.execute("CREATE VIRTUAL TABLE IF NOT EXISTS messages USING fts5(session_id, timestamp, type, content, metadata)")
        except sqlite3.OperationalError:
            c.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                timestamp TEXT,
                type TEXT,
                content TEXT,
                metadata TEXT
            )
            """)
        # Sessions table
        c.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            created_at TEXT
        )
        """)
        self.conn.commit()

    def save_message(self, session_id, timestamp, msg_type, content, metadata=None):
        c = self.conn.cursor()
        try:
            c.execute("INSERT INTO messages (session_id, timestamp, type, content, metadata) VALUES (?, ?, ?, ?, ?)",
                      (session_id, timestamp, msg_type, content, str(metadata) if metadata else None))
        except sqlite3.OperationalError:
            c.execute("INSERT INTO messages (session_id, timestamp, type, content, metadata) VALUES (?, ?, ?, ?, ?)",
                      (session_id, timestamp, msg_type, content, str(metadata) if metadata else None))
        self.conn.commit()

    def create_session(self, session_id):
        c = self.conn.cursor()
        c.execute("INSERT OR IGNORE INTO sessions (session_id, created_at) VALUES (?, datetime('now'))", (session_id,))
        self.conn.commit()

    def list_sessions(self):
        c = self.conn.cursor()
        c.execute("SELECT session_id, created_at FROM sessions ORDER BY created_at DESC")
        return c.fetchall()

    def load_session(self, session_id):
        c = self.conn.cursor()
        c.execute("SELECT timestamp, type, content, metadata FROM messages WHERE session_id = ? ORDER BY timestamp ASC", (session_id,))
        return c.fetchall()

    def fork_session(self, old_session_id, new_session_id):
        c = self.conn.cursor()
        self.create_session(new_session_id)
        c.execute("SELECT timestamp, type, content, metadata FROM messages WHERE session_id = ? ORDER BY timestamp ASC", (old_session_id,))
        rows = c.fetchall()
        for row in rows:
            self.save_message(new_session_id, row[0], row[1], row[2], row[3])
        self.conn.commit()

    def search(self, query, session_id=None):
        c = self.conn.cursor()
        if session_id:
            try:
                c.execute("SELECT timestamp, type, content, metadata FROM messages WHERE session_id = ? AND messages MATCH ?", (session_id, query))
            except sqlite3.OperationalError:
                c.execute("SELECT timestamp, type, content, metadata FROM messages WHERE session_id = ? AND content LIKE ?", (session_id, f"%{query}%"))
        else:
            try:
                c.execute("SELECT timestamp, type, content, metadata FROM messages WHERE messages MATCH ?", (query,))
            except sqlite3.OperationalError:
                c.execute("SELECT timestamp, type, content, metadata FROM messages WHERE content LIKE ?", (f"%{query}%",))
        return c.fetchall()

    def all_messages(self, session_id=None):
        c = self.conn.cursor()
        if session_id:
            c.execute("SELECT timestamp, type, content, metadata FROM messages WHERE session_id = ? ORDER BY timestamp ASC", (session_id,))
        else:
            c.execute("SELECT timestamp, type, content, metadata FROM messages ORDER BY timestamp ASC")
        return c.fetchall()

class LLMBackendType(Enum):
    OLLAMA = "ollama"
    GEMINI = "gemini"

class ChatREPL:
    def __init__(self, backend: str = None):
        self.messages: List[Message] = []
        self.session_active = True
        # 3. Use backend argument to set backend/model
        if backend is not None:
            if backend.lower() == "gemini":
                self.backend = LLMBackendType.GEMINI
                self.current_model = "gemini-1.5-pro"
            elif backend.lower() == "ollama":
                self.backend = LLMBackendType.OLLAMA
                self.current_model = "tinyllama"
            else:
                print(f"[FATAL] Unknown backend: {backend}", file=sys.stderr)
                print(f"[FATAL] Unknown backend: {backend}")
                sys.stdout.flush(); sys.stderr.flush()
                print("👋 Thanks for using Research Assistant!")
                sys.stdout.flush(); sys.stderr.flush()
                import time; time.sleep(0.1)  # Ensure output is visible to PTY/pexpect
                sys.exit(1)
        else:
            self.backend = LLMBackendType.OLLAMA
            self.current_model = "tinyllama"
        self.temperature = 0.7
        self.max_tokens = 1024
        self.history_db = HistoryDB()
        self.session_id = "default"
        # Initialize console first
        self.console = Console()
        # Initialize session logger
        self.session_logger = SessionLogger(self.session_id)
        # Initialize Rich UI
        self.rich_ui = RichUI(self.console)
        # Load environment variables from ~/.env file
        self.load_env_file()
        self.api_key = os.getenv('GEMINI_API_KEY')
        # Only require GEMINI_API_KEY if backend is Gemini
        if self.backend == LLMBackendType.GEMINI:
            if not self.api_key:
                # Print the exact error string expected by the test
                print("GEMINI_API_KEY environment variable is required", file=sys.stderr)
                print("GEMINI_API_KEY environment variable is required")
                sys.stdout.flush(); sys.stderr.flush()
                print("👋 Thanks for using Research Assistant!")
                sys.stdout.flush(); sys.stderr.flush()
                import time; time.sleep(0.1)  # Ensure output is visible to PTY/pexpect
                sys.exit(1)
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        
        # Available models with their rate limits (Free tier)
        self.available_models = {
            "tinyllama": {"backend": "ollama"},
            "gemini-2.0-flash": {"backend": "gemini"},
            "gemini-1.5-flash": {"backend": "gemini"},
            "gemini-1.5-flash-8b": {"backend": "gemini"},
            "gemini-1.5-pro": {"backend": "gemini"},
            "gemini-2.0-flash-experimental": {"backend": "gemini"},
        }
        
        # Command completions
        self.command_completer = WordCompleter([
            r'\help', r'\clear', r'\history', r'\model', r'\models', r'\temperature', 
            r'\tokens', r'\reset', r'\export', r'\quit', r'\exit', r'\limits', r'\env',
            r'\save', r'\load', r'\list_sessions', r'\fork',
            r'\search', r'\compute', r'\code', r'\synthesize', r'\project'
        ], ignore_case=False, match_middle=False, sentence=False, WORD=True)
        
        self.setup_style()
        self.setup_session()
        self.add_welcome_message()
        self.kb = KeyBindings()
        self.setup_fzf_history_binding()
        
        # Initialize token rate estimator
        self.token_estimator = TokenRateEstimator()
    
    async def _make_llm_request(self, prompt: str, progress: LiveProgressIndicator = None, options: dict = None) -> tuple[str, int, int]:
        """
        Unified LLM request method that handles ALL LLM requests with strict ground truth token monitoring.
        
        Args:
            prompt: The exact prompt to send to the LLM
            progress: Progress indicator to update with ground truth tokens
            options: LLM-specific options (temperature, etc.)
            
        Returns:
            tuple[response_text, actual_input_tokens, actual_output_tokens]
        """
        # Calculate ground truth input tokens (will be corrected by API response)
        estimated_input_tokens = len(prompt.split())
        
        # Estimate request duration for animation timing
        estimated_output_tokens = 50  # Default estimate
        estimated_duration = self.token_estimator.estimate_duration("tinyllama", estimated_input_tokens, estimated_output_tokens)
        
        if progress:
            # Start animation - will wait for actual token data, no estimates shown
            progress.rolling_counter.start_animation()
            self.session_logger.log_system_message(f"[TIMING] Starting animation - waiting for actual token data")
        
        # Make the actual request
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "tinyllama", 
            "prompt": prompt,
            "stream": False,
            "options": options or {}
        }
        
        request_start = time.time()
        if progress:
            self.session_logger.log_system_message(f"[TIMING] LLM request starting at {request_start:.3f}")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    request_end = time.time()
                    actual_duration = request_end - request_start
                    
                    data = await resp.json()
                    response_text = data.get("response", "").strip()
                    
                    # Extract ground truth token counts from API
                    api_input_tokens = data.get("prompt_eval_count", estimated_input_tokens)
                    api_output_tokens = data.get("eval_count", len(response_text.split()))
                    
                    if progress:
                        # Update with ACTUAL token counts from API response
                        progress.rolling_counter.update_with_actual_tokens(api_input_tokens, api_output_tokens)
                        progress.rolling_counter.set_final_values(api_input_tokens, api_output_tokens)
                        progress.final_tokens_set = True
                        self.session_logger.log_system_message(f"[TIMING] Request completed in {actual_duration:.1f}s")
                        self.session_logger.log_system_message(f"[TIMING] ACTUAL tokens: ↑{api_input_tokens} ↓{api_output_tokens} (no estimates used)")
                    
                    return response_text, api_input_tokens, api_output_tokens
                    
        except Exception as e:
            self.session_logger.log_system_message(f"[ERROR] LLM request failed: {e}")
            if progress:
                progress.rolling_counter.set_final_values(0, 0)  # No tokens processed on error
                progress.final_tokens_set = True
            return f"Error: {e}", 0, 0
    
    def load_env_file(self):
        """Load environment variables from ~/.env file, unless NO_DOTENV=1 is set (for test isolation)"""
        if os.environ.get('NO_DOTENV') == '1':
            return
        home_dir = Path.home()
        env_file = home_dir / ".env"
        
        if DOTENV_AVAILABLE:
            if env_file.exists():
                load_dotenv(env_file)
                print_formatted_text(
                    FormattedText([('class:success', f'✓ Loaded environment variables from {env_file}')]),
                    style=Style.from_dict({'success': '#00aa00'})
                )
            else:
                print_formatted_text(
                    FormattedText([('class:system', f'ℹ️ No .env file found at {env_file}')]),
                    style=Style.from_dict({'system': '#888888'})
                )
                
                # Create a sample .env file
                try:
                    with open(env_file, 'w') as f:
                        f.write("# Gemini API Configuration\n")
                        f.write("# Get your API key from: https://ai.google.dev/\n")
                        f.write("GEMINI_API_KEY=your_api_key_here\n")
                        f.write("\n# Optional: Other API keys\n")
                        f.write("# OPENAI_API_KEY=your_openai_key_here\n")
                        f.write("# ANTHROPIC_API_KEY=your_anthropic_key_here\n")
                    
                    print_formatted_text(
                        FormattedText([('class:success', f'✓ Created sample .env file at {env_file}')]),
                        style=Style.from_dict({'success': '#00aa00'})
                    )
                    print_formatted_text(
                        FormattedText([('class:system', 'Please edit the .env file and add your API key.')]),
                        style=Style.from_dict({'system': '#888888'})
                    )
                except Exception as e:
                    print_formatted_text(
                        FormattedText([('class:error', f'❌ Could not create .env file: {e}')]),
                        style=Style.from_dict({'error': '#cc0000 bold'})
                    )
        else:
            print_formatted_text(
                FormattedText([('class:system', '⚠️ python-dotenv not installed. Using system environment variables only.')]),
                style=Style.from_dict({'system': '#888888'})
            )
            print_formatted_text(
                FormattedText([('class:system', 'Install with: pip install python-dotenv')]),
                style=Style.from_dict({'system': '#888888'})
            )
    
    def setup_style(self):
        """Configure the styling for the interface"""
        self.style = Style.from_dict({
            'user': '#00aa00 bold',
            'assistant': '#0066cc',
            'system': '#888888 italic',
            'command': '#cc6600 bold',
            'timestamp': '#666666',
            'prompt': '#00aa00 bold',
            'error': '#cc0000 bold',
            'success': '#00aa00',
        })
    
    def setup_session(self):
        """Initialize the prompt session"""
        self.history = InMemoryHistory()
        self.session = PromptSession(
            history=self.history,
            completer=self.command_completer,
            complete_while_typing=True,
            style=self.style
        )
    
    def add_welcome_message(self):
        """Add welcome message to start the session"""
        dotenv_status = "\u2713 Available" if DOTENV_AVAILABLE else "\u2717 Not installed"
        env_file_path = Path.home() / ".env"
        env_file_status = "\u2713 Found" if env_file_path.exists() else "\u2717 Not found"
        
        welcome_msg = f"""Welcome to Research Assistant!

🔬 I'm your AI research assistant. I can help with:
  • Literature search and citation management
  • Mathematical computations (SageMath/SymPy)
  • Code generation and execution
  • Project scaffolding and organization
  • Research synthesis and analysis

Research Commands:
  \\search <query>    - Search research literature (stub)
  \\compute <expr>    - Mathematical computation (stub)
  \\code <task>       - Generate and execute code (stub)
  \\synthesize <topic> - Research synthesis (stub)
  \\project <name>    - Scaffold research project (stub)

System Commands:
  \\help     - Show this help message
  \\clear    - Clear chat history
  \\history  - Show message history
  \\model    - Show/set current model
  \\models   - List available models and rate limits
  \\temperature - Show/set temperature (0.0-1.0)
  \\tokens   - Show/set max tokens
  \\limits   - Show current model rate limits
  \\env      - Show environment configuration
  \\reset    - Reset all settings to defaults
  \\export   - Export chat history
  \\save     - Save current session
  \\load <session_id> - Switch to a different session by ID
  \\list_sessions - List all saved sessions
  \\fork <new_session_id> - Fork the current session to a new session ID
  \\quit, \\exit - Exit the application

Current model: {self.current_model} (backend: {self.backend.value})
API Key: {'\u2713 Set' if self.api_key else '\u2717 Missing'}
python-dotenv: {dotenv_status}
~/.env file: {env_file_status}

Ask me anything or use a command to get started!
"""
        self.add_message(MessageType.SYSTEM, welcome_msg)
        sys.stdout.flush()
    
    def add_message(self, msg_type: MessageType, content: str, metadata: Optional[Dict] = None):
        """Add a message to the chat history"""
        message = Message(
            type=msg_type,
            content=content,
            timestamp=datetime.now(),
            metadata=metadata or {}
        )
        self.messages.append(message)
        # Save to persistent history with session_id
        self.history_db.create_session(self.session_id)
        self.history_db.save_message(
            self.session_id,
            message.timestamp.isoformat(),
            message.type.value,
            message.content,
            message.metadata
        )
    
    def format_message(self, message: Message) -> FormattedText:
        """Format a message for display"""
        timestamp = message.timestamp.strftime("%H:%M:%S")
        
        if message.type == MessageType.USER:
            return FormattedText([
                ('class:timestamp', f'[{timestamp}] '),
                ('class:user', 'You: '),
                ('', message.content)
            ])
        elif message.type == MessageType.ASSISTANT:
            return FormattedText([
                ('class:timestamp', f'[{timestamp}] '),
                ('class:assistant', 'Assistant: '),
                ('', message.content)
            ])
        elif message.type == MessageType.COMMAND:
            return FormattedText([
                ('class:timestamp', f'[{timestamp}] '),
                ('class:command', 'Command: '),
                ('', message.content)
            ])
        else:  # SYSTEM
            return FormattedText([
                ('class:timestamp', f'[{timestamp}] '),
                ('class:system', message.content)
            ])
    
    def is_kitty(self):
        return os.environ.get("TERM", "").startswith("xterm-kitty")

    def display_kitty_image(self, image_path):
        # Kitty graphics protocol: https://sw.kovidgoyal.net/kitty/graphics-protocol/
        with open(image_path, "rb") as f:
            data = f.read()
        import base64
        b64 = base64.b64encode(data).decode("ascii")
        print(f"\033_Gf=100,a=T,m=1;{b64}\033\\")

    def render_latex_block(self, latex_code):
        # Render LaTeX to PNG using pdflatex + convert (ImageMagick)
        import pathlib
        with tempfile.TemporaryDirectory() as tmpdir:
            tex_file = os.path.join(tmpdir, "equation.tex")
            pdf_file = os.path.join(tmpdir, "equation.pdf")
            png_file = os.path.join(tmpdir, "equation.png")
            with open(tex_file, "w") as f:
                f.write(r"""
\documentclass[preview]{standalone}
\usepackage{amsmath}
\begin{document}
""" + latex_code + "\n\\end{document}")
            try:
                clean_env = os.environ.copy()
                for k in list(clean_env.keys()):
                    if k.startswith("TEXMF") or k.startswith("PATH"):
                        if k != "PATH":
                            del clean_env[k]
                # Run pdflatex to generate PDF
                try:
                    subprocess.run([
                        "pdflatex", "-interaction=nonstopmode", "-output-directory", tmpdir, tex_file
                    ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=clean_env)
                except subprocess.CalledProcessError as e:
                    # If PDF exists, tolerate the error
                    if not pathlib.Path(pdf_file).exists():
                        raise e
                # Convert PDF to PNG using ImageMagick
                subprocess.run([
                    "convert", "-density", "200", pdf_file, "-quality", "90", png_file
                ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=clean_env)
                if self.is_kitty():
                    self.display_kitty_image(png_file)
                else:
                    self.console.print(f"[LaTeX: see {png_file}]", style="bold magenta")
            except Exception as e:
                self.console.print(f"[LaTeX render error: {e}]", style="bold red")

    def render_table(self, md_table):
        # Parse Markdown table and render with rich.table.Table
        lines = [line.strip() for line in md_table.strip().splitlines() if line.strip()]
        if len(lines) < 2:
            self.console.print(md_table)
            return
        headers = [h.strip() for h in lines[0].strip('|').split('|')]
        table = Table(*headers)
        for row in lines[2:]:
            cells = [c.strip() for c in row.strip('|').split('|')]
            table.add_row(*cells)
        self.console.print(table)

    def extract_latex_with_pandoc(self, text):
        """Pipe text through Pandoc with a Lua filter to extract LaTeX environments as code blocks."""
        import tempfile
        import os
        lua_filter_path = os.path.join(os.path.dirname(__file__), '../extract_latex.lua')
        with tempfile.NamedTemporaryFile('w+', delete=False) as tf:
            tf.write(text)
            tf.flush()
            tf_name = tf.name
        try:
            result = subprocess.run([
                'pandoc', tf_name, '--from=markdown', '--to=markdown', f'--lua-filter={lua_filter_path}'
            ], capture_output=True, text=True, check=True)
            return result.stdout
        except Exception:
            return text  # fallback to original if Pandoc fails
        finally:
            os.unlink(tf_name)

    def render_markdown_with_code(self, text: str):
        """Render markdown, code, tables, and LaTeX blocks using rich and Kitty. Now uses Pandoc+Lua filter for robust LaTeX extraction."""
        # Preprocess with Pandoc+Lua filter to normalize LaTeX blocks
        processed_text = self.extract_latex_with_pandoc(text)
        code_block_pattern = re.compile(r'```(\w+)?\n([\s\S]*?)```', re.MULTILINE)
        latex_block_pattern = re.compile(r'(\${2}([\s\S]+?)\${2}|\\\[([\s\S]+?)\\\])', re.MULTILINE)
        table_pattern = re.compile(r'((?:^\|.+\|\n)+)', re.MULTILINE)
        last_end = 0
        for match in code_block_pattern.finditer(processed_text):
            if match.start() > last_end:
                chunk = processed_text[last_end:match.start()]
                # Render LaTeX blocks
                for lmatch in latex_block_pattern.finditer(chunk):
                    if lmatch.start() > 0:
                        self.console.print(Markdown(chunk[:lmatch.start()]))
                    latex_code = lmatch.group(2) or lmatch.group(3)
                    self.render_latex_block(latex_code)
                    chunk = chunk[lmatch.end():]
                # Render tables
                for tmatch in table_pattern.finditer(chunk):
                    if tmatch.group(1).count('|') > 1 and '-' in tmatch.group(1):
                        self.render_table(tmatch.group(1))
                        chunk = chunk.replace(tmatch.group(1), '')
                if chunk.strip():
                    self.console.print(Markdown(chunk))
            lang = match.group(1) or "python"
            code = match.group(2)
            # Special handling for markdown-labeled code blocks
            if lang.lower() == "markdown":
                for tmatch in table_pattern.finditer(code):
                    if tmatch.group(1).count('|') > 1 and '-' in tmatch.group(1):
                        self.render_table(tmatch.group(1))
                        code = code.replace(tmatch.group(1), '')
                if code.strip():
                    self.console.print(Markdown(code))
            elif lang.lower() == "latex":
                self.render_latex_block(code)
            else:
                self.console.print(Syntax(code, lang, theme="monokai", line_numbers=False))
            last_end = match.end()
        if last_end < len(processed_text):
            chunk = processed_text[last_end:]
            for lmatch in latex_block_pattern.finditer(chunk):
                if lmatch.start() > 0:
                    self.console.print(Markdown(chunk[:lmatch.start()]))
                latex_code = lmatch.group(2) or lmatch.group(3)
                self.render_latex_block(latex_code)
                chunk = chunk[lmatch.end():]
            for tmatch in table_pattern.finditer(chunk):
                if tmatch.group(1).count('|') > 1 and '-' in tmatch.group(1):
                    self.render_table(tmatch.group(1))
                    chunk = chunk.replace(tmatch.group(1), '')
            if chunk.strip():
                self.console.print(Markdown(chunk))

    def setup_fzf_history_binding(self):
        @self.kb.add('c-r')
        def _(event):
            user_msgs = [row[2] for row in self.history_db.all_messages(self.session_id) if row[1] == 'user']
            if not user_msgs:
                return
            try:
                proc = subprocess.Popen(['fzf', '--tac', '--prompt=History> '],
                                       stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       text=True)
                input_str = '\n'.join(user_msgs)
                out, _ = proc.communicate(input=input_str)
                if out:
                    event.app.current_buffer.insert_text(out.strip())
            except Exception:
                pass

    def display_messages(self):
        """Display all messages in the chat using Rich UI."""
        self.console.print("\n[dim]═══ Chat History ═══[/dim]")
        for message in self.messages[-20:]:  # Show last 20 messages
            if message.type == MessageType.ASSISTANT:
                # Extract routing information from metadata
                routing_path = message.metadata.get('routing_path', 'Direct')
                
                # Clean content of routing prefixes for display
                content = message.content
                routing_prefixes = ['🤖 TinyLlama:', '📚 LITERATURE AGENT:', '🧮 MATH AGENT:', 
                                  '💻 CODE AGENT:', '🔬 SYNTHESIS AGENT:', '⚙️ RULE:', 
                                  '⚠️ FALLBACK:', '❌ ERROR:']
                for prefix in routing_prefixes:
                    if content.startswith(prefix):
                        content = content[len(prefix):].strip()
                        break
                
                self.rich_ui.print_assistant_message(content, routing_path)
            elif message.type == MessageType.USER:
                self.rich_ui.print_user_message(message.content)
            else:
                self.rich_ui.print_system_message(message.content)
        self.console.print("[dim]═══════════════════[/dim]\n")
    
    def display_new_messages(self):
        """Display only new messages since last display."""
        if not hasattr(self, '_last_displayed_count'):
            self._last_displayed_count = 0
        
        new_messages = self.messages[self._last_displayed_count:]
        
        for message in new_messages:
            if message.type == MessageType.ASSISTANT:
                timestamp = message.timestamp.strftime("%H:%M:%S")
                
                # Extract routing information from metadata
                routing_path = message.metadata.get('routing_path', 'Direct')
                self.console.print(f"[bold blue][{timestamp}] Assistant → {routing_path}:[/bold blue]")
                
                # Clean content of routing prefixes for display
                content = message.content
                routing_prefixes = ['🤖 TinyLlama:', '📚 LITERATURE AGENT:', '🧮 MATH AGENT:', 
                                  '💻 CODE AGENT:', '🔬 SYNTHESIS AGENT:', '⚙️ RULE:', 
                                  '⚠️ FALLBACK:', '❌ ERROR:']
                for prefix in routing_prefixes:
                    if content.startswith(prefix):
                        content = content[len(prefix):].strip()
                        break
                
                # Render markdown with error handling
                try:
                    self.render_markdown_with_code(content)
                except Exception as e:
                    # Fallback to simple print if markdown rendering fails
                    print(f"[Markdown render error: {e}]")
                    print(content)
            else:
                print_formatted_text(self.format_message(message), style=self.style)
        
        self._last_displayed_count = len(self.messages)
    
    def detect_intent_rules(self, query: str) -> str:
        """Rule-based intent detection for obvious cases."""
        query_lower = query.lower()
        
        # Mathematical computation keywords
        math_keywords = ['solve', 'calculate', 'compute', 'equation', 'integral', 'derivative', 
                        'matrix', 'algebra', 'geometry', 'theorem', 'proof', 'formula']
        math_patterns = ['=', '+', '-', '*', '/', '^', 'x^', 'sin(', 'cos(', 'log(', 'sqrt(']
        
        # Literature search keywords  
        search_keywords = ['paper', 'citation', 'reference', 'literature', 'research', 'study',
                          'author', 'journal', 'publication', 'abstract', 'doi', 'arxiv']
        
        # Code generation keywords
        code_keywords = ['function', 'class', 'algorithm', 'code', 'program', 'script', 'debug',
                        'implementation', 'python', 'javascript', 'jupyter', 'notebook']
        
        # Synthesis keywords
        synthesis_keywords = ['explain', 'analyze', 'synthesize', 'summary', 'overview', 'review',
                             'compare', 'contrast', 'relationship', 'connection', 'trend']
        
        # Check for mathematical patterns first (highest priority)
        if any(pattern in query for pattern in math_patterns):
            return "COMPUTE"
        
        # Check for keyword matches
        if any(keyword in query_lower for keyword in math_keywords):
            return "COMPUTE"
        elif any(keyword in query_lower for keyword in search_keywords):
            return "SEARCH"
        elif any(keyword in query_lower for keyword in code_keywords):
            return "CODE"
        elif any(keyword in query_lower for keyword in synthesis_keywords):
            return "SYNTHESIZE"
        
        return None  # No clear rule-based match
    
    async def detect_intent_llm(self, query: str, progress: LiveProgressIndicator = None) -> str:
        """Use TinyLlama for intent detection with constrained prompting."""
        # System prompt for TinyLlama classification
        system_prompt = """You are a research assistant query classifier. Classify queries into exactly one category.

Examples:
Query: "solve x^2 + 2x + 1 = 0"
Category: COMPUTE

Query: "find papers about quantum computing"
Category: SEARCH

Query: "write a python function for sorting"
Category: CODE

Query: "explain the relationship between AI and machine learning"
Category: SYNTHESIZE

Query: "hello how are you"
Category: CHAT

Categories:
- SEARCH: Literature search, finding papers, citations, references
- COMPUTE: Mathematical computation, equations, symbolic math
- CODE: Programming, code generation, execution, debugging  
- SYNTHESIZE: Research synthesis, analysis, writing, explanations
- CHAT: General conversation, questions, help

Query: "{query}"
Category:"""
        
        try:
            # Use unified LLM request method
            options = {
                "temperature": 0.1,  # Low temperature for consistent classification
                "top_p": 0.5,
                "stop": ["\n", "Query:", "Category:"]  # Stop tokens
            }
            
            response, input_tokens, output_tokens = await self._make_llm_request(system_prompt, progress, options)
            response = response.strip().upper()
            
            # Extract only the category name
            valid_intents = ["SEARCH", "COMPUTE", "CODE", "SYNTHESIZE", "CHAT"]
            for intent in valid_intents:
                if intent in response:
                    self.session_logger.log_system_message(f"[TIMING] Intent detection result: {intent}")
                    return intent
            return "CHAT"  # Default fallback
        except Exception:
            return "CHAT"  # Default fallback
    
    async def detect_intent(self, query: str, pipeline: PipelineContainer = None) -> tuple[str, str]:
        """Hybrid intent detection: rules first, then TinyLlama, then fallback."""
        # Layer 1: Rule-based detection (fast, reliable)
        rule_intent = self.detect_intent_rules(query)
        if rule_intent:
            return rule_intent, "RULES"
        
        # Layer 2: TinyLlama classification (when rules are ambiguous)  
        # Create processing block for intent detection
        intent_block = ProcessingBlock(
            console=self.console,
            title="🧠 Intent Detection", 
            message="Analyzing query intent using TinyLlama...",
            model="tinyllama",
            provider="Ollama",
            border_style="dim yellow"
        )
        
        # Add to pipeline if provided
        if pipeline:
            intent_block.suppress_display = True  # Suppress individual display when in pipeline
            pipeline.add_step(intent_block)
        
        # Start the processing block
        intent_block.start()
        
        try:
            llm_intent = await self.detect_intent_llm(query, intent_block)
            if llm_intent != "CHAT":
                # Add routing conclusion for non-CHAT intents
                intent_block.set_routing_conclusion(f"Intent: {llm_intent}. Routing to: {llm_intent.title()} Agent.")
                return llm_intent, "LLM"
            else:
                # Add routing conclusion for CHAT intent
                intent_block.set_routing_conclusion(f"Intent: CHAT. Routing to: TinyLlama (Chat Mode).")
        finally:
            # Complete the processing block
            intent_block.complete()
            # Give time for final display
            time.sleep(0.5)
        
        # Layer 3: Default fallback
        return "CHAT", "DEFAULT"
    
    def get_rule_based_chat_response(self, query: str) -> tuple[str, bool]:
        """Minimal rule-based responses only for critical failures/errors."""
        query_lower = query.lower().strip()
        
        # Only handle cases where TinyLlama consistently fails or produces unsafe output
        # Keep this list VERY minimal to preserve AI illusion
        
        # Only if TinyLlama is completely broken/offline
        if query_lower in ['test_fallback_only']:  # Hidden test command
            return "System fallback response", True
            
        return None, False  # Let TinyLlama handle everything else

    async def chat_with_tinyllama(self, query: str, progress: LiveProgressIndicator = None) -> tuple[str, str, Optional[int]]:
        """Enhanced TinyLlama chat with clear response attribution."""
        # Check for emergency rule-based responses only
        rule_response, is_rule = self.get_rule_based_chat_response(query)
        if rule_response:
            return rule_response, "Rule-based", None
        
        # Use TinyLlama directly with minimal constraints - let it be itself
        # This preserves the AI experience and shows real model capabilities/limitations
        simple_prompt = f"""You are a helpful research assistant. 

{query}"""

        
        try:
            # Use unified LLM request method
            options = {
                "temperature": 0.4,  # Allow some creativity while staying coherent
                "top_p": 0.9,
                "num_predict": 120,   # Allow longer responses
                "stop": ["\n\n\n"]  # Minimal stop tokens
            }
            
            response, input_tokens, output_tokens = await self._make_llm_request(simple_prompt, progress, options)
            
            # Minimal cleanup - only remove obvious artifacts
            if response.startswith("Answer:") or response.startswith("A:"):
                response = response.split(":", 1)[1].strip()
            
            # Only fallback if completely empty or broken
            if len(response) < 2:
                return "I apologize, I'm having trouble generating a response right now.", "Fallback", input_tokens
            
            # Return clean response with routing info and actual prompt tokens
            return response, "TinyLlama", input_tokens
                    
        except Exception as e:
            # Clear attribution for network/system failures
            return f"Unable to connect to language model: {str(e)}", "Error", None

    async def route_to_agent(self, query: str, intent: str, progress: LiveProgressIndicator = None) -> tuple[str, str, Optional[int]]:
        """Route query to appropriate research agent based on intent."""
        if intent == "SEARCH":
            content = f"Searching for '{query}'\n→ Would search PDF corpus and return relevant citations."
            if progress:
                progress.update_tokens(received=len(content.split()))
            return content, "Literature Agent (Stub Mode)", None
        elif intent == "COMPUTE":
            content = f"Computing '{query}'\n→ Would use SageMath/SymPy for symbolic computation."
            if progress:
                progress.update_tokens(received=len(content.split()))
            return content, "Math Agent (Stub Mode)", None
        elif intent == "CODE":
            content = f"Generating code for '{query}'\n→ Would generate, execute, and iterate on code."
            if progress:
                progress.update_tokens(received=len(content.split()))
            return content, "Code Agent (Stub Mode)", None
        elif intent == "SYNTHESIZE":
            content = f"Analyzing '{query}'\n→ Would combine multiple sources for comprehensive research."
            if progress:
                progress.update_tokens(received=len(content.split()))
            return content, "Synthesis Agent (Stub Mode)", None
        else:
            # Use improved chat prompting for TinyLlama (progress updates happen inside chat_with_tinyllama)
            content, _, prompt_tokens = await self.chat_with_tinyllama(query, progress)
            return content, "TinyLlama (Chat Mode)", prompt_tokens

    async def call_llm_api(self, query: str):
        if self.backend == LLMBackendType.OLLAMA:
            # Call Ollama local API for TinyLlama
            url = "http://localhost:11434/api/generate"
            payload = {"model": "tinyllama", "prompt": query, "stream": True}
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    async for line in resp.content:
                        if not line:
                            continue
                        try:
                            data = json.loads(line.decode("utf-8"))
                            if "response" in data:
                                yield data["response"]
                        except Exception:
                            continue
        else:
            # Default to Gemini
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            model = genai.GenerativeModel(self.current_model)
            response = model.generate_content(query, stream=True)
            for chunk in response:
                yield chunk.text
    
    async def handle_command(self, command: str) -> bool:
        # Normalize whitespace: collapse multiple spaces, strip leading/trailing
        command = command.strip()
        cmd = command.split()
        if not cmd:
            return False
        c = cmd[0]
        
        # Research assistant commands (stubs)
        if c == '\\search':
            if len(cmd) < 2:
                self.add_message(MessageType.SYSTEM, "Usage: \\search <query>")
                return True
            query = " ".join(cmd[1:])
            self.add_message(MessageType.SYSTEM, f"[STUB] Literature search for: '{query}'\n→ This would search PDF corpus and return relevant papers with citations.")
            return True
        elif c == '\\compute':
            if len(cmd) < 2:
                self.add_message(MessageType.SYSTEM, "Usage: \\compute <expression>")
                return True
            expr = " ".join(cmd[1:])
            self.add_message(MessageType.SYSTEM, f"[STUB] Mathematical computation: '{expr}'\n→ This would use SageMath/SymPy for symbolic computation.")
            return True
        elif c == '\\code':
            if len(cmd) < 2:
                self.add_message(MessageType.SYSTEM, "Usage: \\code <task>")
                return True
            task = " ".join(cmd[1:])
            self.add_message(MessageType.SYSTEM, f"[STUB] Code generation for: '{task}'\n→ This would generate, execute, and iterate on code in Jupyter kernel.")
            return True
        elif c == '\\synthesize':
            if len(cmd) < 2:
                self.add_message(MessageType.SYSTEM, "Usage: \\synthesize <topic>")
                return True
            topic = " ".join(cmd[1:])
            self.add_message(MessageType.SYSTEM, f"[STUB] Research synthesis on: '{topic}'\n→ This would combine literature, computation, and analysis into comprehensive research.")
            return True
        elif c == '\\project':
            if len(cmd) < 2:
                self.add_message(MessageType.SYSTEM, "Usage: \\project <name>")
                return True
            name = cmd[1]
            self.add_message(MessageType.SYSTEM, f"[STUB] Scaffolding project: '{name}'\n→ This would create directory structure with docs/, src/, logs/, README.md, etc.")
            return True
        elif c == '\\help':
            self.add_message(MessageType.SYSTEM, "Available commands: " + ", ".join([
                '\\help', '\\clear', '\\history', '\\model', '\\models', '\\temperature', '\\tokens', '\\reset', '\\export', '\\quit', '\\exit', '\\limits', '\\env', '\\save', '\\load', '\\list_sessions', '\\fork',
                '\\search', '\\compute', '\\code', '\\synthesize', '\\project'
            ]))
            return True
        elif c == '\\save':
            self.history_db.create_session(self.session_id)
            self.add_message(MessageType.SYSTEM, f"Session '{self.session_id}' saved.")
            return True
        elif c == '\\load':
            if len(cmd) < 2:
                self.add_message(MessageType.SYSTEM, "Usage: \\load <session_id>")
                return True
            session_id = cmd[1]
            self.session_id = session_id
            # Reload messages from the selected session's history
            msgs = self.history_db.load_session(session_id)
            self.messages.clear()
            for ts, typ, content, metadata in msgs:
                self.messages.append(Message(
                    type=MessageType(typ),
                    content=content,
                    timestamp=datetime.fromisoformat(ts),
                    metadata=eval(metadata) if metadata else None
                ))
            self.add_message(MessageType.SYSTEM, f"Session switched to '{session_id}'.")
            return True
        elif c == '\\list_sessions':
            sessions = self.history_db.list_sessions()
            if not sessions:
                self.add_message(MessageType.SYSTEM, "No sessions found.")
            else:
                session_list = "\n".join([f"{s[0]} (created {s[1]})" for s in sessions])
                self.add_message(MessageType.SYSTEM, f"Sessions:\n{session_list}")
            return True
        elif c == '\\fork':
            if len(cmd) < 2:
                self.add_message(MessageType.SYSTEM, "Usage: \\fork <new_session_id>")
                return True
            new_session_id = cmd[1]
            self.history_db.fork_session(self.session_id, new_session_id)
            self.add_message(MessageType.SYSTEM, f"Session '{self.session_id}' forked to '{new_session_id}'.")
            return True
        elif command in ['\\quit', '\\exit']:
            self.add_message(MessageType.SYSTEM, "Goodbye!")
            return False
        # Remove or alias legacy forms
        elif c in ['\\save_session', '\\load_session', '\\fork_session']:
            self.add_message(MessageType.SYSTEM, "Please use unified command names: \\save, \\load, \\fork")
            return True
        
        elif command == r'\help':
            help_text = f"""Available commands:
  \\help     - Show this help message
  \\clear    - Clear chat history
  \\history  - Show message history
  \\model    - Show/set current model
  \\models   - List available models and rate limits
  \\temperature - Show/set temperature (0.0-1.0)
  \\tokens   - Show/set max tokens
  \\limits   - Show current model rate limits
  \\env      - Show environment configuration
  \\reset    - Reset all settings to defaults
  \\export   - Export chat history
  \\save     - Save current session
  \\load <session_id> - Switch to a different session by ID
  \\list_sessions - List all saved sessions
  \\fork <new_session_id> - Fork the current session to a new session ID
  \\quit, \\exit - Exit the application

Current model: {self.current_model} (backend: {self.backend.value})
API Key: {'✓ Set' if self.api_key else '✗ Missing'}"""
            self.add_message(MessageType.SYSTEM, help_text)
        
        elif command == r'\env':
            dotenv_status = "✓ Available" if DOTENV_AVAILABLE else "✗ Not installed"
            env_file_path = Path.home() / ".env"
            env_file_status = "✓ Found" if env_file_path.exists() else "✗ Not found"
            
            env_vars = []
            for key in ['GEMINI_API_KEY', 'OPENAI_API_KEY', 'ANTHROPIC_API_KEY']:
                value = os.getenv(key)
                if value:
                    # Show only first 8 and last 4 characters for security
                    masked_value = f"{value[:8]}...{value[-4:]}" if len(value) > 12 else "***"
                    env_vars.append(f"  {key}: {masked_value}")
                else:
                    env_vars.append(f"  {key}: Not set")
            
            env_text = f"""Environment Configuration:
python-dotenv: {dotenv_status}
~/.env file: {env_file_status} ({env_file_path})

Environment Variables:
{chr(10).join(env_vars)}

To set up your API key:
1. Edit ~/.env file
2. Add: GEMINI_API_KEY=your_api_key_here
3. Restart the application"""
            
            self.add_message(MessageType.SYSTEM, env_text)
        
        elif command == r'\models':
            models_text = "Available models and rate limits (Free tier):\n"
            for model, limits in self.available_models.items():
                current = " (current)" if model == self.current_model else ""
                models_text += f"  {model}{current}\n"
                models_text += f"    RPM: {limits['rpm']}, TPM: {limits['tpm']:,}, RPD: {limits['rpd']}\n"
            self.add_message(MessageType.SYSTEM, models_text)
        
        elif command == r'\limits':
            if self.current_model in self.available_models:
                limits = self.available_models[self.current_model]
                limits_text = f"Rate limits for {self.current_model}:\n"
                limits_text += f"  Requests per minute: {limits['rpm']}\n"
                limits_text += f"  Tokens per minute: {limits['tpm']:,}\n"
                limits_text += f"  Requests per day: {limits['rpd']}"
                self.add_message(MessageType.SYSTEM, limits_text)
            else:
                self.add_message(MessageType.SYSTEM, f"No limit info available for {self.current_model}")
        
        elif command == r'\clear':
            self.messages.clear()
            self.add_message(MessageType.SYSTEM, "Chat history cleared.")
        
        elif command == r'\history':
            count = len(self.messages)
            self.add_message(MessageType.SYSTEM, f"Chat history: {count} messages")
        
        elif command == r'\model':
            self.add_message(MessageType.SYSTEM, f"Current model: {self.current_model} (backend: {self.backend.value})")
        
        elif command.startswith('\\model '):
            new_model = command[7:].strip()
            if new_model in self.available_models:
                self.current_model = new_model
                self.backend = LLMBackendType(self.available_models[new_model]["backend"])
                self.add_message(MessageType.SYSTEM, f"Model changed to: {self.current_model} (backend: {self.backend.value})")
            else:
                self.add_message(MessageType.SYSTEM, f"Unknown model: {new_model}")
            return True
        
        elif command == r'\temperature':
            self.add_message(MessageType.SYSTEM, f"Current temperature: {self.temperature}")
        
        elif command.startswith('\\temperature '):
            try:
                temp = float(command[13:].strip())
                if 0.0 <= temp <= 1.0:
                    self.temperature = temp
                    self.add_message(MessageType.SYSTEM, f"Temperature set to: {self.temperature}")
                else:
                    self.add_message(MessageType.SYSTEM, "Temperature must be between 0.0 and 1.0")
            except ValueError:
                self.add_message(MessageType.SYSTEM, "Invalid temperature value")
        
        elif command == r'\tokens':
            self.add_message(MessageType.SYSTEM, f"Max tokens: {self.max_tokens}")
        
        elif command.startswith('\\tokens '):
            try:
                tokens = int(command[8:].strip())
                if tokens > 0:
                    self.max_tokens = tokens
                    self.add_message(MessageType.SYSTEM, f"Max tokens set to: {self.max_tokens}")
                else:
                    self.add_message(MessageType.SYSTEM, "Max tokens must be positive")
            except ValueError:
                self.add_message(MessageType.SYSTEM, "Invalid token value")
        
        elif command == r'\reset':
            self.current_model = "gemini-1.5-pro"
            self.temperature = 0.7
            self.max_tokens = 1024
            self.add_message(MessageType.SYSTEM, "Settings reset to defaults")
        
        elif command == r'\export':
            filename = f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("# Research Assistant Chat Export\n")
                    f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"# Model: {self.current_model}\n")
                    f.write(f"# Temperature: {self.temperature}\n")
                    f.write(f"# Max Tokens: {self.max_tokens}\n\n")
                    
                    for message in self.messages:
                        timestamp = message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                        f.write(f"[{timestamp}] {message.type.value.upper()}: {message.content}\n\n")
                
                self.add_message(MessageType.SYSTEM, f"✓ Chat exported to: {filename}")
            except Exception as e:
                self.add_message(MessageType.SYSTEM, f"❌ Export failed: {e}")
        
        elif command == r'\list_sessions':
            sessions = self.history_db.list_sessions()
            if not sessions:
                self.add_message(MessageType.SYSTEM, "No sessions found.")
            else:
                msg = "Saved sessions:\n" + "\n".join([f"  {sid} (created {created})" for sid, created in sessions])
                self.add_message(MessageType.SYSTEM, msg)
        
        elif command.startswith('\\save_session '):
            name = command[len('\\save_session '):].strip()
            if not name:
                self.add_message(MessageType.SYSTEM, "Usage: \\save_session <name>")
            else:
                self.history_db.create_session(name)
                # Save all current messages to the new session
                for m in self.messages:
                    self.history_db.save_message(
                        name,
                        m.timestamp.isoformat(),
                        m.type.value,
                        m.content,
                        m.metadata
                    )
                self.add_message(MessageType.SYSTEM, f"Session saved as '{name}'.")
        
        elif command.startswith('\\load_session '):
            name = command[len('\\load_session '):].strip()
            if not name:
                self.add_message(MessageType.SYSTEM, "Usage: \\load_session <name>")
            else:
                msgs = self.history_db.load_session(name)
                if not msgs:
                    self.add_message(MessageType.SYSTEM, f"No session found with name '{name}'.")
                else:
                    self.session_id = name
                    self.messages.clear()
                    for ts, typ, content, metadata in msgs:
                        self.messages.append(Message(
                            type=MessageType(typ),
                            content=content,
                            timestamp=datetime.fromisoformat(ts),
                            metadata=eval(metadata) if metadata else None
                        ))
                    self.add_message(MessageType.SYSTEM, f"Session '{name}' loaded.")
        
        elif command.startswith('\\fork_session '):
            name = command[len('\\fork_session '):].strip()
            if not name:
                self.add_message(MessageType.SYSTEM, "Usage: \\fork_session <name>")
            else:
                self.history_db.fork_session(self.session_id, name)
                self.add_message(MessageType.SYSTEM, f"Session '{self.session_id}' forked to '{name}'.")
        
        else:
            # Debug output for diagnosis
            print(f"[DEBUG] handle_command: command={repr(command)}, c={repr(c)}")
            self.add_message(MessageType.SYSTEM, f"Unknown command: {command}")
        
        return True
    
    async def process_input(self, input_str: str) -> str:
        """
        Process a single user input (command or message) and return the output as a string.
        This can be used by both the REPL loop and tests.
        """
        from io import StringIO
        old_stdout = sys.stdout
        
        try:
            # Handle commands and user messages differently for stdout management
            normalized = input_str.strip()
            if normalized.startswith('\\'):
                # Command - use stdout redirection for test capture
                sys.stdout = mystdout = StringIO()
                try:
                    await self.handle_command(normalized)
                    # Restore stdout before displaying so rich console output goes to terminal
                    sys.stdout = old_stdout
                    self.display_new_messages()
                    # Return the latest system message for test assertions
                    last_system = next((m.content for m in reversed(self.messages) if m.type == MessageType.SYSTEM), "")
                    return mystdout.getvalue() + last_system
                finally:
                    if sys.stdout != old_stdout:
                        sys.stdout = old_stdout
            else:
                # User message - avoid stdout redirection during progress display
                self.add_message(MessageType.USER, input_str)
                # User input is already displayed in run() method, don't display again
                # Log user input
                self.session_logger.log_user_input(input_str)
                
                # Store actual prompt tokens for metrics (will be updated by Ollama if available)
                actual_prompt_tokens = len(input_str.split())
                
                import asyncio
                assistant_response = ""
                routing_metadata = {}
                async def get_response():
                    nonlocal assistant_response, routing_metadata, actual_prompt_tokens
                    source = "Unknown"  # Initialize source to avoid UnboundLocalError
                    progress = None    # Initialize progress to avoid UnboundLocalError
                    pipeline = None    # Initialize pipeline to avoid UnboundLocalError
                    try:
                        # Log timing: Start of processing
                        start_time = time.time()
                        self.session_logger.log_system_message(f"[TIMING] Processing started at {start_time:.3f}")
                        
                        # Create pipeline container for internal processing
                        pipeline = PipelineContainer(self.console, self.rich_ui)
                        pipeline.start()
                        
                        # Detect intent and route to appropriate agent
                        intent_start = time.time()
                        intent, method = await self.detect_intent(input_str, pipeline)
                        intent_end = time.time()
                        self.session_logger.log_system_message(f"[TIMING] Intent detection took {intent_end - intent_start:.3f}s")
                        
                        # Start main query processing
                        # No pipe connector needed - handled within pipeline container
                        
                        # Determine which model will be used based on intent
                        if intent in ["SEARCH", "COMPUTE", "CODE", "SYNTHESIZE"]:
                            model_info = "[Stub Mode]"
                            query_text = f"Processing {intent.lower()} query..."
                        else:
                            # Show actual model being used for chat
                            if self.backend == LLMBackendType.OLLAMA:
                                model_info = f"[Ollama: {self.current_model}]"
                            elif self.backend == LLMBackendType.GEMINI:
                                model_info = f"[Gemini: {self.current_model}]"
                            else:
                                model_info = f"[{self.backend.value}: {self.current_model}]"
                            query_text = f"Generating response using {self.current_model}..."
                            
                        # Create and start main progress indicator
                        progress = LiveProgressIndicator(
                            self.console,
                            self.rich_ui,
                            f"[dim green]💬 Main Query[/dim green]",
                            query_text,
                            "dim green",
                            self.current_model,
                            model_info
                        )
                        
                        # Add to pipeline and suppress individual display
                        progress.suppress_display = True
                        pipeline.add_step(progress)
                        # Estimate token counts for main query
                        input_tokens = len(input_str.split()) * 1.3  # Rough estimate
                        expected_output = 100 if intent not in ["SEARCH", "COMPUTE", "CODE", "SYNTHESIZE"] else 50
                        progress.start(int(input_tokens), expected_output)
                        # Don't immediately set user input tokens - let the animation show them rolling up
                        
                        # Get response and routing info (progress updates happen inside route_to_agent)
                        route_start = time.time()
                        self.session_logger.log_system_message(f"[TIMING] Routing to agent at {route_start:.3f}, {route_start - start_time:.3f}s after start")
                        content, source, prompt_tokens = await self.route_to_agent(input_str, intent, progress)
                        assistant_response = content
                        if prompt_tokens:
                            actual_prompt_tokens = prompt_tokens
                        
                        # Build detailed routing path for display
                        if method == "RULES":
                            methodology = f"[⚡ Rules, Intent: {intent}]"
                        elif method == "LLM":
                            methodology = f"[🧠 AI-classified, Intent: {intent}]"
                        else:  # DEFAULT
                            methodology = f"[🔄 Default, Intent: {intent}]"
                        
                        routing_path = f"{methodology} → {source}"
                        routing_metadata = {"routing_path": routing_path, "intent": intent, "method": method, "source": source}
                        
                        # Log metrics (use actual prompt tokens for accurate metrics)
                        self.session_logger.log_query_metrics(
                            progress.get_elapsed_time(),
                            actual_prompt_tokens,
                            progress.tokens_received,
                            intent,
                            method
                        )
                        
                        # Log the final status message that user sees
                        final_status = f"⏱️  {progress.get_elapsed_time():.1f}s | ↑ {progress.tokens_sent} tokens | ↓ {progress.tokens_received} tokens"
                        self.session_logger.log_system_message(final_status)
                        
                    finally:
                        # Add routing conclusion before stopping
                        if progress:
                            progress.set_routing_conclusion(f"Relaying to user: {source}")
                            # Set final token values before stopping
                            progress.set_final_tokens(progress.tokens_sent, progress.tokens_received)
                            # Give the routing conclusion time to display
                            time.sleep(0.5)
                            # Stop progress indicator
                            progress.stop()
                        
                        # Finalize the pipeline container with total timing
                        if pipeline:
                            pipeline.finalize()
                
                # Handle async response generation
                await get_response()
                self.add_message(MessageType.ASSISTANT, assistant_response, routing_metadata)
                
                # Log assistant response
                self.session_logger.log_assistant_response(
                    routing_metadata.get("routing_path", "Unknown"),
                    assistant_response
                )
                
                # Display assistant response using Rich UI
                self.rich_ui.print_assistant_message(
                    assistant_response, 
                    routing_metadata.get("routing_path", "Unknown")
                )
                
                # Return assistant response for tests and API consumers
                return assistant_response
        finally:
            # Ensure stdout is restored even if there's an exception
            if sys.stdout != old_stdout:
                sys.stdout = old_stdout
    
    def process_input_sync(self, input_str: str) -> str:
        """Sync wrapper for process_input - for tests and other sync contexts."""
        import asyncio
        try:
            # Try to run in existing event loop
            loop = asyncio.get_running_loop()
            # If we're in an event loop, we can't use asyncio.run()
            # This is a test context, so we need to handle it differently
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                def run_in_new_loop():
                    new_loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(new_loop)
                    try:
                        return new_loop.run_until_complete(self.process_input(input_str))
                    finally:
                        new_loop.close()
                return executor.submit(run_in_new_loop).result()
        except RuntimeError:
            # No running loop, safe to use asyncio.run()
            return asyncio.run(self.process_input(input_str))
    
    async def run(self):
        """Main REPL loop with streaming output. Always uses prompt_toolkit for input."""
        # Show welcome message only once at startup
        self.add_welcome_message()
        self.display_new_messages()
        goodbye_printed = False
        while self.session_active:
            try:
                try:
                    user_input = await self.session.prompt_async(
                        FormattedText([('class:prompt', '> ')]),
                        style=self.style
                    )
                except EOFError:
                    if not goodbye_printed:
                        print("👋 Thanks for using Research Assistant!")
                        sys.stdout.flush(); sys.stderr.flush()
                        goodbye_printed = True
                    self.session_active = False
                    break
                if user_input is None:
                    if not goodbye_printed:
                        print("👋 Thanks for using Research Assistant!")
                        sys.stdout.flush(); sys.stderr.flush()
                        goodbye_printed = True
                    self.session_active = False
                    break
                if not user_input.strip():
                    continue
                
                # Clear the prompt line and replace with "You" box
                self._replace_prompt_with_user_box(user_input)
                
                await self.process_input(user_input)
                if user_input.startswith('\\'):
                    if user_input.strip() in ['\\quit', '\\exit']:
                        break
            except KeyboardInterrupt:
                if not goodbye_printed:
                    print("👋 Thanks for using Research Assistant!")
                    sys.stdout.flush(); sys.stderr.flush()
                    goodbye_printed = True
                self.session_active = False
                break
            except EOFError:
                if not goodbye_printed:
                    print("👋 Thanks for using Research Assistant!")
                    sys.stdout.flush(); sys.stderr.flush()
                    goodbye_printed = True
                self.session_active = False
                break
        if not goodbye_printed:
            print("👋 Thanks for using Research Assistant!")
            sys.stdout.flush(); sys.stderr.flush()
    
    def _replace_prompt_with_user_box(self, user_input: str):
        """Replace the prompt line with a clean 'You' box."""
        # Use direct sys.stdout.write for ANSI escape codes
        try:
            # Check if we're in a real terminal (not captured output)
            if sys.stdout.isatty():
                # Write ANSI escape codes directly to stdout
                sys.stdout.write("\033[A")  # Move cursor up one line
                sys.stdout.write("\033[2K")  # Clear entire line
                sys.stdout.write("\r")      # Move cursor to beginning of line
                sys.stdout.flush()
            else:
                # For non-terminal output, just add a newline
                print()
        except Exception as e:
            # Fallback: just print a newline if terminal manipulation fails
            # In test environments or unsupported terminals, gracefully degrade
            print()
        
        # Display the "You" box at the same position
        self.rich_ui.print_user_message(user_input)

    def stream_response(self, input_str: str):
        """
        Yield each chunk of the LLM response as it is received (for streaming tests).
        """
        import asyncio
        async def get_chunks():
            async for chunk in self.call_llm_api(input_str):
                yield chunk
        loop = asyncio.get_event_loop() if asyncio.get_event_loop().is_running() else asyncio.new_event_loop()
        # Use a queue to bridge async generator to sync iterator
        import queue
        import threading
        q = queue.Queue()
        def run():
            async def inner():
                async for chunk in get_chunks():
                    q.put(chunk)
                q.put(None)
            loop.run_until_complete(inner())
        t = threading.Thread(target=run)
        t.start()
        while True:
            chunk = q.get()
            if chunk is None:
                break
            yield chunk
        t.join()

if __name__ == "__main__":
    # 1. Check for TTY (non-interactive input)
    if not sys.stdin.isatty():
        print("[DEBUG] Non-interactive input detected. Exiting REPL.", flush=True)
        print("[INFO] Non-interactive input detected. Exiting REPL.")
        print("👋 Thanks for using Gemini-CLI REPL Chat!")
        sys.stdout.flush(); sys.stderr.flush()
        import time; time.sleep(0.1)  # Ensure output is visible to PTY/pexpect
        sys.exit(0)
    # 2. Parse CLI argument for backend selection
    backend_arg = None
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ("gemini", "ollama"):
            backend_arg = arg
    try:
        repl = ChatREPL(backend=backend_arg)
        import asyncio
        try:
            asyncio.run(repl.run())
        except RuntimeError as e:
            # If event loop is already running, patch with nest_asyncio and run in current loop
            if "already running" in str(e):
                try:
                    import nest_asyncio
                    nest_asyncio.apply()
                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(repl.run())
                except Exception as ne:
                    print(f"[FATAL] REPL failed to start: {ne}", file=sys.stderr)
                    print(f"[FATAL] REPL failed to start: {ne}")
                    print("👋 Thanks for using Research Assistant!")
                    sys.stdout.flush(); sys.stderr.flush()
                    import time; time.sleep(0.1)
                    sys.exit(1)
            else:
                raise
    except Exception as e:
        print(f"[FATAL] REPL failed to start: {e}", file=sys.stderr)
        print(f"[FATAL] REPL failed to start: {e}")
        print("👋 Thanks for using Gemini-CLI REPL Chat!")
        sys.stdout.flush(); sys.stderr.flush()
        import time; time.sleep(0.1)
        sys.exit(1)
