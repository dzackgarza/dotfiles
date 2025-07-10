# Textual Component Mapping Ledger

**Scope:** Detailed mapping of Tkinter components to Textual equivalents  
**Focus:** Preserve functionality while achieving terminal-native aesthetics

## Component-by-Component Mapping

### 1. Main Application Container

#### Tkinter Implementation (V2-tkinter-rewrite)
```python
# main_window.py
class MainWindow:
    def __init__(self, config_name="debug", theme_name="light"):
        self.root = tk.Tk()
        self.root.title("LLM REPL V3 - Modern Interface")
        self.setup_window()
        self.create_widgets()
```

#### Textual Implementation (V3)
```python
# app.py
class LLMReplApp(App):
    """Main application - terminal-native TUI"""
    
    TITLE = "LLM REPL V3 - Terminal Interface"
    CSS_PATH = "theme/theme.tcss"
    
    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
        ("ctrl+l", "clear_timeline", "Clear"),
        ("ctrl+s", "save_timeline", "Save"),
        ("escape", "cancel_processing", "Cancel"),
    ]
    
    def __init__(self, config_name="debug"):
        super().__init__()
        self.config = get_config(config_name)
        self.timeline_manager = TimelineManager()
        self.cognition_processor = CognitionProcessor()
```

**Migration Notes:**
- Tkinter root window → Textual App class
- Window setup → CSS styling + App configuration  
- Widget creation → compose() method with yield statements

---

### 2. Timeline Display Component

#### Tkinter Implementation
```python
# timeline_view.py
class TimelineView:
    def __init__(self, parent, theme=None):
        self.text_widget = scrolledtext.ScrolledText(
            self.frame,
            state=tk.DISABLED,
            width=100,
            height=25
        )
        
    def add_block(self, block: TimelineBlock):
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, content, "block_content")
        self.text_widget.config(state=tk.DISABLED)
```

#### Textual Implementation
```python
# widgets/timeline_widget.py
class TimelineWidget(Static):
    """Timeline display using Rich renderables"""
    
    def __init__(self):
        super().__init__()
        self.timeline_manager = TimelineManager()
        self._blocks_renderable = Group()
    
    def add_block(self, block: TimelineBlock):
        """Add block as Rich renderable"""
        block_renderable = self._render_block(block)
        self._blocks_renderable.renderables.append(block_renderable)
        self.update(self._blocks_renderable)
    
    def _render_block(self, block: TimelineBlock) -> Renderable:
        """Convert TimelineBlock to Rich renderable"""
        console = Console()
        
        # Block header with color coding
        header_style = self._get_block_style(block.type)
        header = Text(block.get_formatted_header(), style=header_style)
        
        # Block content with proper formatting
        content = Text(block.content, style="white")
        
        # Separator
        separator = Text("─" * 80, style="dim")
        
        return Group(separator, header, content, Text())
```

**Migration Notes:**
- ScrolledText widget → Static widget with Rich renderables
- Manual text insertion → Rich Group of Text objects
- Text tags → Rich Text styling
- Auto-scrolling → Textual automatic scroll behavior

---

### 3. Input Panel Component

#### Tkinter Implementation  
```python
# input_panel.py
class InputPanel:
    def __init__(self, parent, theme=None):
        self.input_text = tk.Text(
            self.frame,
            width=100,
            height=5,
            wrap=tk.WORD
        )
        self.send_button = tk.Button(
            self.button_frame,
            text="Send (Enter)",
            command=self.send_message
        )
        
    def send_message(self):
        user_input = self.input_text.get("1.0", tk.END).strip()
        if self.send_callback:
            self.send_callback(user_input)
```

#### Textual Implementation
```python
# widgets/input_widget.py
class InputWidget(Container):
    """Input panel with terminal-like feel"""
    
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Input(
                placeholder="Enter your message...",
                id="user-input"
            )
            yield Button("Send", id="send-btn", variant="primary")
            
        with Horizontal():
            yield Button("Clear Timeline", id="clear-btn", variant="default")
            yield Static("Ready", id="status")
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle Enter key in input"""
        if event.input.id == "user-input":
            self.send_message(event.value)
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks"""
        if event.button.id == "send-btn":
            input_widget = self.query_one("#user-input", Input)
            self.send_message(input_widget.value)
        elif event.button.id == "clear-btn":
            self.post_message(ClearTimeline())
    
    def send_message(self, text: str) -> None:
        """Send message and clear input"""
        if text.strip():
            self.post_message(UserMessage(text))
            input_widget = self.query_one("#user-input", Input)
            input_widget.value = ""
```

**Migration Notes:**
- Tkinter Text widget → Textual Input widget (terminal-like input)
- Manual button handling → Textual event system
- Callback functions → Textual message passing
- Character counting → Built into Textual Input

---

### 4. Layout and Composition

#### Tkinter Implementation
```python
# main_window.py
def create_widgets(self):
    # Timeline view (top)
    self.timeline_view = TimelineView(self.main_frame, self.theme)
    self.timeline_view.pack(fill=tk.BOTH, expand=True)
    
    # Input panel (bottom)  
    self.input_panel = InputPanel(self.main_frame, self.theme)
    self.input_panel.pack(fill=tk.X, side=tk.BOTTOM)
```

#### Textual Implementation  
```python
# app.py
def compose(self) -> ComposeResult:
    """Compose the application layout"""
    
    with Vertical():
        # Header with title and status
        yield Header()
        
        # Main content area
        with Horizontal():
            # Timeline takes most space
            yield TimelineWidget(id="timeline")
            
        # Input area at bottom
        yield InputWidget(id="input-panel")
        
        # Footer with shortcuts
        yield Footer()
```

**Migration Notes:**
- Manual pack() layout → Textual compose() with containers
- Explicit sizing → CSS-driven responsive layout
- Frame hierarchy → Container nesting with Vertical/Horizontal

---

### 5. Styling and Theming

#### Tkinter Implementation
```python
# styles.py
class ModernTheme:
    COLORS = {
        'background': '#ffffff',
        'text_primary': '#0f172a',
        'block_user': '#059669',
    }
    
    @classmethod
    def apply_to_widget(cls, widget, style_name):
        widget.configure(**cls.STYLES[style_name])
```

#### Textual Implementation
```python
# theme/theme.py
class TerminalTheme:
    """Terminal-native color schemes"""
    
    # Tokyo Night scheme  
    TOKYO_NIGHT = {
        "background": "#1a1b26",
        "surface": "#24283b", 
        "primary": "#7aa2f7",
        "user": "#9ece6a",
        "assistant": "#7dcfff",
        "error": "#f7768e",
    }
    
    # Nord scheme
    NORD = {
        "background": "#2e3440",
        "surface": "#3b4252",
        "primary": "#81a1c1", 
        "user": "#a3be8c",
        "assistant": "#88c0d0",
        "error": "#bf616a",
    }
```

```css
/* theme/theme.tcss */
App {
    background: $background;
    color: $text;
}

TimelineWidget {
    background: $surface;
    border: round $primary;
    padding: 1;
}

Input {
    background: $background;
    border: round $primary;
    color: $text;
}

.user-block {
    color: $user;
    text-style: bold;
}

.assistant-block {
    color: $assistant;
}

.error-block {
    color: $error;
}
```

**Migration Notes:**
- Python color definitions → CSS variables + Python theme objects
- Manual widget.configure() → Textual CSS selectors
- Hardcoded styling → Responsive CSS with terminal color integration

---

## Message System Mapping

### Tkinter Callbacks → Textual Messages

#### Tkinter Implementation
```python
def set_send_callback(self, callback):
    self.send_callback = callback

def on_user_input(self, text):
    self.send_callback(text)
```

#### Textual Implementation
```python
# Custom message classes
class UserMessage(Message):
    def __init__(self, text: str):
        self.text = text
        super().__init__()

class ClearTimeline(Message):
    pass

class ProcessingComplete(Message):
    def __init__(self, response: str):
        self.response = response
        super().__init__()

# Message handling in App
def on_user_message(self, message: UserMessage) -> None:
    """Handle user input"""
    # Add user block to timeline
    user_block = create_user_input_block(message.text)
    timeline = self.query_one("#timeline", TimelineWidget)
    timeline.add_block(user_block)
    
    # Start processing
    self.process_user_input(message.text)
```

**Migration Notes:**
- Callback functions → Typed Message classes
- Direct function calls → Post/handle message pattern
- Manual state management → Reactive message-driven updates

---

## Event Handling Mapping

### Keyboard Shortcuts

#### Tkinter Implementation
```python
self.input_text.bind('<Return>', self.on_enter_key)
self.input_text.bind('<Control-Return>', self.on_ctrl_enter)
self.root.bind('<Control-l>', self.clear_timeline)
```

#### Textual Implementation
```python
BINDINGS = [
    ("enter", "send_message", "Send"),
    ("ctrl+enter", "send_message", "Send"), 
    ("ctrl+l", "clear_timeline", "Clear"),
    ("ctrl+c", "quit", "Quit"),
    ("escape", "cancel_processing", "Cancel"),
]

def action_send_message(self) -> None:
    """Send current input message"""
    input_widget = self.query_one("#user-input", Input)
    if input_widget.value.strip():
        self.post_message(UserMessage(input_widget.value))

def action_clear_timeline(self) -> None:
    """Clear the timeline"""
    timeline = self.query_one("#timeline", TimelineWidget) 
    timeline.clear()
```

**Migration Notes:**
- Manual bind() calls → BINDINGS class attribute
- Event callbacks → action_* methods
- Key event objects → Simple action invocation

This mapping preserves all functionality while transitioning to terminal-native Textual components that will integrate seamlessly with Sway aesthetics.