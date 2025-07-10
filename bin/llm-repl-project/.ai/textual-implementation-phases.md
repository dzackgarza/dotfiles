# Textual Implementation Phases Ledger

**Scope:** Step-by-step implementation plan for V2-tkinter-rewrite → V3-textual migration  
**Timeline:** 5-7 days total with parallel workstreams  
**Goal:** Fully functional terminal-native LLM REPL

## Implementation Phases Overview

```
Phase 1: Foundation (Days 1-2)
├── Basic Textual app structure
├── Core module integration  
├── Minimal UI layout
└── Configuration system

Phase 2: Core Features (Days 2-4) 
├── Timeline widget implementation
├── Input widget with terminal feel
├── Block rendering system
└── Message passing integration

Phase 3: Styling & Polish (Days 4-5)
├── Terminal-native theming
├── Responsive design
├── Keyboard shortcuts
└── Status indicators

Phase 4: Testing & Validation (Days 5-6)
├── Port existing tests
├── Textual-specific testing
├── Sway integration validation
└── Performance optimization

Phase 5: Documentation & Launch (Day 7)
├── Update documentation
├── Migration guide
├── Performance benchmarking
└── Production readiness
```

---

## Phase 1: Foundation (Days 1-2)

### Day 1: Project Structure & Basic App

#### 1.1 Create V3 Directory Structure
```bash
# Create V3 project structure
mkdir -p V3/{widgets,theme,core,config,tests}
touch V3/{__init__.py,main.py,app.py}
touch V3/widgets/{__init__.py,timeline_widget.py,input_widget.py}
touch V3/theme/{__init__.py,theme.py,theme.tcss}
touch V3/core/__init__.py
touch V3/config/__init__.py  
touch V3/tests/{__init__.py,test_app.py}
```

#### 1.2 Basic Dependencies & Requirements
```python
# V3/requirements.txt
textual>=0.50.0
rich>=13.0.0
asyncio  # Built-in
pathlib  # Built-in
argparse  # Built-in
pytest>=7.0.0  # For testing
```

#### 1.3 Minimal Textual App
```python
# V3/app.py - Basic app structure
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Header, Footer, Static, Input, Button
from config.settings import get_config

class LLMReplApp(App):
    """LLM REPL V3 - Terminal Interface"""
    
    TITLE = "LLM REPL V3 - Terminal Interface"
    CSS_PATH = "theme/theme.tcss"
    
    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
        ("ctrl+l", "clear_timeline", "Clear"),
        ("escape", "cancel", "Cancel"),
    ]
    
    def __init__(self, config_name: str = "debug"):
        super().__init__()
        self.config = get_config(config_name)
    
    def compose(self) -> ComposeResult:
        """Compose the application layout"""
        yield Header()
        
        with Vertical():
            # Timeline placeholder
            yield Static("Timeline will go here", id="timeline-placeholder")
            
            # Input placeholder  
            with Horizontal():
                yield Input(placeholder="Enter message...", id="user-input")
                yield Button("Send", id="send-btn", variant="primary")
        
        yield Footer()
    
    def action_clear_timeline(self) -> None:
        """Clear timeline action"""
        self.notify("Clear timeline (not implemented)")
    
    def action_cancel(self) -> None:
        """Cancel current operation"""
        self.notify("Cancel (not implemented)")

# V3/main.py - Entry point
#!/usr/bin/env python3
import argparse
from app import LLMReplApp

def main():
    parser = argparse.ArgumentParser(description="LLM REPL V3 - Terminal Interface")
    parser.add_argument("--config", default="debug", choices=["debug", "fast", "demo"])
    args = parser.parse_args()
    
    app = LLMReplApp(config_name=args.config)
    app.run()

if __name__ == "__main__":
    main()
```

#### 1.4 Copy Core Modules (Day 1 End)
```bash
# Copy unchanged core business logic from V2-tkinter-rewrite
cp V2-tkinter-rewrite/core/* V3/core/
cp V2-tkinter-rewrite/config/* V3/config/

# Verify core modules work with simple import test
cd V3 && python -c "from core.blocks import TimelineBlock; print('✅ Core modules imported successfully')"
```

**Day 1 Success Criteria:**
- ✅ V3 directory structure created
- ✅ Basic Textual app runs 
- ✅ Core business logic modules imported
- ✅ Configuration system functional

### Day 2: Layout Integration & Component Foundation

#### 2.1 Timeline Widget Foundation
```python
# V3/widgets/timeline_widget.py
from textual.widgets import Static
from textual.reactive import reactive
from rich.console import Group
from rich.text import Text
from core.timeline import TimelineManager
from core.blocks import TimelineBlock

class TimelineWidget(Static):
    """Timeline display widget"""
    
    timeline_content = reactive("")
    
    def __init__(self):
        super().__init__()
        self.timeline_manager = TimelineManager()
        self.refresh_timeline()
    
    def watch_timeline_content(self, content: str) -> None:
        """React to timeline content changes"""
        self.update(content)
    
    def add_block(self, block: TimelineBlock) -> None:
        """Add block to timeline"""
        self.timeline_manager.add_block(block)
        self.refresh_timeline()
    
    def refresh_timeline(self) -> None:
        """Refresh timeline display"""
        blocks = self.timeline_manager.get_blocks()
        if not blocks:
            self.timeline_content = "Welcome! Start by entering a message below."
            return
        
        # Simple text rendering for now - will enhance in Phase 2
        content_lines = []
        for block in blocks:
            content_lines.append(f"[bold]{block.title}[/bold]")
            content_lines.append(f"  {block.content}")
            content_lines.append("")
        
        self.timeline_content = "\\n".join(content_lines)
    
    def clear(self) -> None:
        """Clear timeline"""
        self.timeline_manager = TimelineManager()
        self.refresh_timeline()
```

#### 2.2 Input Widget Foundation  
```python
# V3/widgets/input_widget.py
from textual.widgets import Input, Button, Static
from textual.containers import Horizontal, Vertical
from textual.message import Message

class UserMessage(Message):
    """Message sent when user submits input"""
    def __init__(self, text: str):
        self.text = text
        super().__init__()

class InputWidget(Vertical):
    """Input panel widget"""
    
    def compose(self):
        with Horizontal():
            yield Input(
                placeholder="Enter your message...", 
                id="user-input"
            )
            yield Button("Send", id="send-btn", variant="primary")
        
        yield Static("Ready", id="status")
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle Enter key"""
        if event.input.id == "user-input":
            text = event.value.strip()
            if text:
                self.post_message(UserMessage(text))
                event.input.value = ""  # Clear input
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle Send button"""
        if event.button.id == "send-btn":
            input_field = self.query_one("#user-input", Input)
            text = input_field.value.strip()
            if text:
                self.post_message(UserMessage(text))
                input_field.value = ""
    
    def set_status(self, message: str, style: str = "ready") -> None:
        """Update status display"""
        status = self.query_one("#status", Static)
        status.update(message)
```

#### 2.3 Integrate Widgets into Main App
```python
# V3/app.py - Updated with real widgets
from widgets.timeline_widget import TimelineWidget
from widgets.input_widget import InputWidget, UserMessage
from core.blocks import create_user_input_block, create_assistant_response_block

class LLMReplApp(App):
    # ... existing code ...
    
    def compose(self) -> ComposeResult:
        """Compose with real widgets"""
        yield Header()
        
        with Vertical():
            yield TimelineWidget(id="timeline")
            yield InputWidget(id="input-panel")
        
        yield Footer()
    
    def on_user_message(self, message: UserMessage) -> None:
        """Handle user input message"""
        # Add user block to timeline
        user_block = create_user_input_block(message.text)
        timeline = self.query_one("#timeline", TimelineWidget)
        timeline.add_block(user_block)
        
        # For now, echo back - will add real LLM processing in Phase 2
        response_block = create_assistant_response_block(f"Echo: {message.text}")
        timeline.add_block(response_block)
        
        self.notify(f"Processed: {message.text}")
```

**Day 2 Success Criteria:**
- ✅ Timeline widget displays blocks
- ✅ Input widget captures and sends messages  
- ✅ Basic message flow works (user input → timeline)
- ✅ Layout looks reasonable in terminal

---

## Phase 2: Core Features (Days 2-4)

### Day 3: LLM Integration & Processing

#### 2.1 Integrate Cognition Processor
```python
# V3/app.py - Add real LLM processing
from core.cognition import CognitionProcessor
from core.blocks import create_cognition_block

class LLMReplApp(App):
    
    def __init__(self, config_name: str = "debug"):
        super().__init__()
        self.config = get_config(config_name)
        self.cognition_processor = CognitionProcessor()
        self.cognition_processor.configure_processing_delay(self.config.cognition_delay)
        self.is_processing = False
    
    async def on_user_message(self, message: UserMessage) -> None:
        """Handle user input with real LLM processing"""
        if self.is_processing:
            self.notify("Processing in progress, please wait...")
            return
        
        # Add user block
        user_block = create_user_input_block(message.text)
        timeline = self.query_one("#timeline", TimelineWidget)
        timeline.add_block(user_block)
        
        # Update status
        input_panel = self.query_one("#input-panel", InputWidget)
        input_panel.set_status("Processing...", "processing")
        
        try:
            self.is_processing = True
            
            # Add cognition block
            cognition_block = create_cognition_block()
            timeline.add_block(cognition_block)
            
            # Process with real cognition
            result = await self.cognition_processor.process(message.text)
            
            # Add assistant response
            response_block = create_assistant_response_block(result["final_output"])
            timeline.add_block(response_block)
            
            input_panel.set_status("Ready", "ready")
            
        except Exception as e:
            error_block = create_error_block(f"Processing error: {str(e)}")
            timeline.add_block(error_block)
            input_panel.set_status("Error", "error")
        
        finally:
            self.is_processing = False
```

#### 2.2 Enhanced Block Rendering
```python
# V3/widgets/timeline_widget.py - Enhanced rendering
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from theme.theme import TerminalTheme

class TimelineWidget(Static):
    
    def __init__(self):
        super().__init__()
        self.timeline_manager = TimelineManager()
        self.theme = TerminalTheme.get_theme("tokyo_night")  # Default theme
        self.refresh_timeline()
    
    def refresh_timeline(self) -> None:
        """Enhanced timeline rendering"""
        blocks = self.timeline_manager.get_blocks()
        if not blocks:
            welcome_text = Text("Welcome to LLM REPL V3!", style="bold cyan")
            subtitle = Text("Start by entering a message below.", style="dim")
            self.update(Align.center(Group(welcome_text, subtitle)))
            return
        
        # Render blocks as Rich panels
        rendered_blocks = []
        for block in blocks:
            rendered_block = self._render_block(block)
            rendered_blocks.append(rendered_block)
        
        self.update(Group(*rendered_blocks))
    
    def _render_block(self, block: TimelineBlock) -> Panel:
        """Render individual block with theme colors"""
        # Get block-specific styling
        if block.type.value == "user_input":
            color = self.theme["colors"]["accent_user"]
            icon = "❯"
        elif block.type.value == "assistant_response":
            color = self.theme["colors"]["accent_assistant"]  
            icon = "🤖"
        elif block.type.value == "system_check":
            color = self.theme["colors"]["accent_system"]
            icon = "⚙️"
        else:
            color = self.theme["colors"]["text_secondary"]
            icon = "•"
        
        # Create header with icon and title
        header = Text(f"{icon} {block.title}", style=f"bold {color}")
        
        # Block content
        content = Text(block.content, style=self.theme["colors"]["text_primary"])
        
        # Create panel with border color
        return Panel(
            Align.left(Group(header, content)),
            border_style=color,
            padding=(0, 1),
            title=f"[dim]{block.type.value.replace('_', ' ').title()}[/dim]",
            title_align="left"
        )
```

**Day 3 Success Criteria:**
- ✅ Real LLM processing pipeline integrated
- ✅ Cognition blocks display processing steps
- ✅ Enhanced block rendering with colors/icons
- ✅ Error handling for processing failures

### Day 4: Message System & State Management

#### 2.1 Complete Message System
```python
# V3/messages.py - Message definitions
from textual.message import Message

class UserMessage(Message):
    def __init__(self, text: str):
        self.text = text
        super().__init__()

class ClearTimeline(Message):
    pass

class ProcessingComplete(Message):
    def __init__(self, result: dict):
        self.result = result
        super().__init__()

class ProcessingError(Message):
    def __init__(self, error: str):
        self.error = error
        super().__init__()

class StatusUpdate(Message):
    def __init__(self, message: str, status_type: str = "ready"):
        self.message = message
        self.status_type = status_type
        super().__init__()
```

#### 2.2 Startup Initialization
```python
# V3/app.py - Add startup blocks
def on_mount(self) -> None:
    """Initialize app on startup"""
    timeline = self.query_one("#timeline", TimelineWidget)
    
    # Add startup blocks like V2-tkinter-rewrite
    timeline.timeline_manager.initialize_with_startup_blocks(self.config.name)
    timeline.refresh_timeline()
    
    # Focus input
    input_field = self.query_one("#user-input", Input)
    input_field.focus()
```

**Day 4 Success Criteria:**
- ✅ Complete message passing system
- ✅ Startup initialization with system blocks
- ✅ Proper state management
- ✅ Input focus and keyboard navigation

---

## Phase 3: Styling & Polish (Days 4-5)

### Day 5: Terminal-Native Theming

#### 3.1 Implement Theme System
```python
# V3/theme/theme.py - Full theme implementation
# (Use content from textual-styling-theming.md)
```

#### 3.2 Create Textual CSS
```css
/* V3/theme/theme.tcss - Terminal-native styles */
/* (Use content from textual-styling-theming.md) */
```

#### 3.3 Responsive Design
```css
/* Add responsive breakpoints for different terminal sizes */
@media (max-width: 80) {
    TimelineWidget {
        padding: 0;
    }
}

@media (max-height: 20) {
    Header {
        display: none;
    }
}
```

**Day 5 Success Criteria:**
- ✅ Tokyo Night theme fully implemented
- ✅ Responsive design for various terminal sizes
- ✅ Terminal-native aesthetic achieved
- ✅ Block type colors and styling complete

---

## Phase 4: Testing & Validation (Days 5-6)

### Day 6: Comprehensive Testing

#### 4.1 Port Existing Tests
```python
# V3/tests/test_core.py - Port from V2-tkinter-rewrite
# (Copy and adapt existing test suite)

# V3/tests/test_widgets.py - Textual-specific tests
import pytest
from textual.app import App
from widgets.timeline_widget import TimelineWidget
from widgets.input_widget import InputWidget
from core.blocks import create_user_input_block

class TestTimelineWidget:
    def test_block_addition(self):
        """Test adding blocks to timeline"""
        widget = TimelineWidget()
        block = create_user_input_block("Test message")
        
        widget.add_block(block)
        assert widget.timeline_manager.get_block_count() == 1
    
    def test_timeline_rendering(self):
        """Test timeline renders blocks correctly"""
        widget = TimelineWidget()
        block = create_user_input_block("Test message")
        widget.add_block(block)
        
        # Test that content includes our message
        assert "Test message" in widget.timeline_content

class TestInputWidget:
    def test_message_sending(self):
        """Test input widget sends messages"""
        # Implementation using Textual testing framework
        pass
```

#### 4.2 Integration Testing
```python
# V3/tests/test_integration.py
class TestIntegration:
    def test_full_user_flow(self):
        """Test complete user interaction flow"""
        # 1. Start app
        # 2. Send user message
        # 3. Verify blocks are added to timeline
        # 4. Verify cognition processing
        # 5. Verify assistant response
        pass
    
    def test_error_handling(self):
        """Test error scenarios"""
        pass
    
    def test_keyboard_shortcuts(self):
        """Test keyboard navigation"""
        pass
```

#### 4.3 Sway Integration Testing
```bash
# Test script for Sway integration
#!/bin/bash
# V3/tests/test_sway_integration.sh

echo "Testing Sway integration..."

# Test 1: Launch in terminal and verify it tiles properly
echo "1. Testing tiling behavior..."
alacritty -e python V3/main.py &
sleep 2
pkill -f "python V3/main.py"

# Test 2: Test with transparency
echo "2. Testing transparency support..."
# This would require manual verification

# Test 3: Test keyboard shortcuts don't conflict with Sway
echo "3. Testing keyboard shortcuts..."
# Manual test required

echo "✅ Sway integration tests complete"
```

**Day 6 Success Criteria:**
- ✅ All existing tests ported and passing
- ✅ Textual-specific functionality tested
- ✅ Integration tests validate full workflow
- ✅ Sway compatibility verified

---

## Phase 5: Documentation & Launch (Day 7)

### Day 7: Production Readiness

#### 5.1 Update Documentation
```markdown
# V3/README.md
# LLM REPL V3 - Terminal Interface

A terminal-native LLM REPL designed for integration with Arch Linux + Sway.

## Features
- Terminal-native UI using Textual framework
- Seamless Sway window manager integration
- Multiple terminal color scheme support
- Keyboard-driven interface
- Real-time LLM processing with transparency

## Installation
```bash
cd V3
pip install -r requirements.txt
python main.py
```

## Usage
- Enter messages in the input field
- Press Enter to send
- Ctrl+L to clear timeline
- Ctrl+C to quit
```

#### 5.2 Performance Benchmarking
```python
# V3/benchmarks/performance_test.py
import time
import asyncio
from app import LLMReplApp

async def benchmark_startup():
    """Benchmark app startup time"""
    start = time.time()
    app = LLMReplApp()
    # Simulate startup without GUI
    end = time.time()
    return end - start

async def benchmark_message_processing():
    """Benchmark message processing"""
    # Test processing pipeline performance
    pass

if __name__ == "__main__":
    startup_time = asyncio.run(benchmark_startup())
    print(f"Startup time: {startup_time:.3f}s")
```

#### 5.3 Migration Guide
```markdown
# V3/MIGRATION.md
# Migration from V2-tkinter-rewrite to V3

## What Changed
- UI framework: Tkinter → Textual
- Aesthetic: Desktop GUI → Terminal-native TUI
- Dependencies: Removed GUI dependencies

## What Stayed the Same
- Core business logic (blocks, timeline, cognition)
- Configuration system
- Command-line interface
- All functionality preserved

## Running V3
```bash
# Instead of:
python V2-tkinter-rewrite/main.py

# Run:
python V3/main.py
```
```

**Day 7 Success Criteria:**
- ✅ Complete documentation updated
- ✅ Performance benchmarks recorded
- ✅ Migration guide created
- ✅ Production-ready release

---

## Success Metrics & Validation

### Functional Completeness
- [ ] All V2-tkinter-rewrite features preserved
- [ ] Timeline blocks display correctly  
- [ ] User input processing works
- [ ] Cognition pipeline functional
- [ ] Configuration system working
- [ ] Keyboard shortcuts implemented

### Aesthetic Integration
- [ ] Looks like native terminal application
- [ ] Integrates with Sway tiling seamlessly
- [ ] Terminal transparency support
- [ ] Respects terminal color schemes
- [ ] Input feels like terminal input

### Technical Requirements
- [ ] No Xwayland dependencies
- [ ] Fast startup (< 1 second)
- [ ] Responsive keyboard navigation
- [ ] Proper gap behavior in Sway
- [ ] Works in various terminal emulators

### Quality Assurance
- [ ] All tests passing
- [ ] No regression from V2-tkinter-rewrite
- [ ] Performance meets expectations
- [ ] Documentation complete
- [ ] Ready for production use

This phased approach ensures systematic migration while maintaining functionality and achieving the terminal-native aesthetic goals.