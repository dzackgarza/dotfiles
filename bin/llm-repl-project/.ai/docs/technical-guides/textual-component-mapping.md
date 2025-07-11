# Elia App Component Integration Mapping Ledger

**Scope:** Detailed mapping of LLM REPL Textual components for integration into the "Elia App" codebase.
**Focus:** How our Textual UI components (`LLMReplApp`, `TimelineWidget`, `InputWidget`) will be embedded and interact within the existing "Elia App" UI framework.
**Goal:** Preserve LLM REPL functionality and terminal-native aesthetics within the Elia App environment.

## Component-by-Component Mapping

This section outlines how our existing Textual components will be integrated, replacing or complementing parts of the "Elia App's" UI.

### 1. Main Application Container (Elia App Host)

The "Elia App" will serve as the main application container. Our `LLMReplApp` (Textual) will be instantiated and run within Elia's main loop or a designated UI area.

#### Elia App Implementation (Existing)
```python
# elia_app/main.py (Example - actual structure may vary)
class EliaApp:
    def __init__(self):
        self.root_window = ... # Elia's main UI element
        self.setup_elia_ui()
        # ... other Elia-specific initialization
    
    def run(self):
        # Elia's main event loop
        self.root_window.mainloop() 
```

#### LLM REPL Textual Implementation (Integrated)
```python
# llm_repl_ui/app.py
from textual.app import App, ComposeResult
# ... other imports for our widgets and core logic

class LLMReplApp(App):
    """Main LLM REPL Textual application, to be embedded in Elia App."""
    
    TITLE = "LLM REPL - Integrated" # Title might be overridden by Elia
    CSS_PATH = "theme/theme.tcss" # Our Textual CSS
    
    BINDINGS = [
        ("ctrl+c", "quit", "Quit"), # These bindings will apply within our Textual app
        ("ctrl+l", "clear_timeline", "Clear"),
        ("ctrl+s", "save_timeline", "Save"),
        ("escape", "cancel_processing", "Cancel"),
    ]
    
    def __init__(self, config_name="debug"):
        super().__init__()
        # Our core components remain the same
        self.config = get_config(config_name)
        self.timeline_manager = TimelineManager()
        self.cognition_processor = CognitionProcessor()
        # ...
```

**Integration Notes:**
- The `LLMReplApp` will not be the top-level application. It will be a component managed by the "Elia App."
- An `elia_adapter.py` will be responsible for instantiating `LLMReplApp` and integrating its event loop or rendering into Elia's UI.
- Keyboard bindings defined in `LLMReplApp` will function when our Textual component has focus within Elia.

---

### 2. Timeline Display Component

Our `TimelineWidget` will be responsible for rendering the conversation history using Rich renderables, maintaining its terminal-native appearance.

#### Elia App Implementation (Potential Replacement)
- If Elia App has its own text display area, it will likely be replaced or hidden by our `TimelineWidget`.

#### LLM REPL Textual Implementation (Integrated)
```python
# llm_repl_ui/widgets/timeline_widget.py
from textual.widgets import Static
from textual.reactive import reactive
from rich.console import Group
from rich.text import Text
# ... imports for our core timeline logic

class TimelineWidget(Static):
    """Timeline display using Rich renderables, embedded in Elia App."""
    
    def __init__(self):
        super().__init__()
        self.timeline_manager = TimelineManager()
        self._blocks_renderable = Group() # Rich Group to hold rendered blocks
    
    def add_block(self, block: TimelineBlock):
        """Add block as Rich renderable and update display."""
        block_renderable = self._render_block(block)
        self._blocks_renderable.renderables.append(block_renderable)
        self.update(self._blocks_renderable) # Trigger Textual to re-render
    
    def _render_block(self, block: TimelineBlock) -> Renderable:
        """Convert TimelineBlock data to a Rich renderable (e.g., Panel, Text)."""
        # This logic remains the same, ensuring consistent visual output
        # ... (Rich rendering logic for blocks)
        return Group(Text("Example Block")) # Placeholder
```

**Integration Notes:**
- The `TimelineWidget` will be placed within Elia App's UI layout, potentially occupying a significant portion of the display.
- Its rendering will rely on Textual's capabilities, which Elia App must support (e.g., by embedding Textual's display).

---

### 3. Input Panel Component

Our `InputWidget` will provide the user input area, including the text field and send button, with its familiar terminal-like feel.

#### Elia App Implementation (Potential Replacement)
- Elia App's existing input mechanisms will be replaced or bypassed by our `InputWidget`.

#### LLM REPL Textual Implementation (Integrated)
```python
# llm_repl_ui/widgets/input_widget.py
from textual.widgets import Input, Button, Static
from textual.containers import Horizontal, Vertical
from textual.message import Message # Our custom message classes

class InputWidget(Vertical):
    """Input panel with terminal-like feel, embedded in Elia App."""
    
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
        """Handle Enter key in input field, sending a UserMessage."""
        if event.input.id == "user-input":
            self.send_message(event.value)
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks (e.g., Send, Clear Timeline)."""
        if event.button.id == "send-btn":
            input_widget = self.query_one("#user-input", Input)
            self.send_message(input_widget.value)
        elif event.button.id == "clear-btn":
            self.post_message(ClearTimeline()) # Post our custom message
    
    def send_message(self, text: str) -> None:
        """Sends the user's message and clears the input field."""
        if text.strip():
            self.post_message(UserMessage(text)) # Post our custom message
            input_widget = self.query_one("#user-input", Input)
            input_widget.value = ""
```

**Integration Notes:**
- The `InputWidget` will be positioned within Elia App's UI, likely at the bottom.
- Its event handling will rely on Textual's event system, which must be active within the embedded context.

---

### 4. Layout and Composition (within Elia App)

The overall layout will be managed by the "Elia App." Our Textual components will be composed within a designated area provided by Elia.

#### Elia App Implementation (Example of how Elia might host our components)
```python
# elia_app/ui/main_view.py (Example)
from llm_repl_ui.app import LLMReplApp
# ... other Elia UI imports

class EliaMainView:
    def __init__(self, parent):
        self.parent = parent
        self.container = EliaContainer(parent) # Elia's container for our app
        
        # Instantiate and embed our Textual app
        self.llm_repl_app_instance = LLMReplApp()
        self.llm_repl_app_instance.mount(self.container) # Mount Textual app into Elia's container
        
        # ... other Elia UI elements
```

#### LLM REPL Textual Implementation (Our internal composition remains)
```python
# llm_repl_ui/app.py (Our internal compose method)
def compose(self) -> ComposeResult:
    """Composes the internal layout of our LLM REPL Textual application."""
    
    with Vertical():
        yield Header() # Our Textual Header
        
        with Horizontal():
            yield TimelineWidget(id="timeline") # Our Textual TimelineWidget
            
        yield InputWidget(id="input-panel") # Our Textual InputWidget
        
        yield Footer() # Our Textual Footer
```

**Integration Notes:**
- The `compose` method within `LLMReplApp` defines the internal layout of our REPL.
- The "Elia App" will be responsible for placing this entire composed Textual application within its own UI hierarchy.

---

### 5. Styling and Theming

Our Textual CSS and Python theme definitions will be used to style our integrated components, aiming for consistency with Elia App's overall aesthetic or maintaining our distinct terminal-native look.

#### Elia App Implementation (Existing styling mechanisms)
- Elia App will have its own CSS, theming, or styling system. We need to understand how to either override it for our components or ensure our styles are compatible.

#### LLM REPL Textual Implementation (Our theme system)
```python
# llm_repl_ui/theme/theme.py
class TerminalTheme:
    """Terminal-native color schemes for our Textual components."""
    # ... (Tokyo Night, Nord, Dracula definitions)
    # These will be used to generate CSS variables for theme.tcss
```

```css
/* llm_repl_ui/theme/theme.tcss */
/* This CSS will target our Textual components */
App {
    background: var(--background); /* Use CSS variables for theming */
    color: var(--text-primary);
}

TimelineWidget {
    background: var(--surface);
    border: round var(--border);
    padding: 1;
}

/* ... other Textual component specific styles */
```

**Integration Notes:**
- We will need to ensure that Elia App's CSS or styling doesn't inadvertently break our Textual component's appearance.
- The `ThemeLoader` (from `textual-styling-theming.md`) will be crucial for applying our themes within the Elia App context.

---

## Message System Mapping (within Elia App)

Our custom Textual messages (`UserMessage`, `ClearTimeline`, etc.) will be used for internal communication within our LLM REPL components. If Elia App has its own event/message system, an adapter will be needed.

#### Elia App Implementation (Example event handling)
```python
# elia_app/event_system.py (Example)
class EliaEvent:
    # ...
    pass

def handle_elia_event(event: EliaEvent):
    # ...
    pass
```

#### LLM REPL Textual Implementation (Our message classes)
```python
# llm_repl_ui/messages.py
from textual.message import Message

class UserMessage(Message):
    """Custom message for user input."""
    def __init__(self, text: str):
        self.text = text
        super().__init__()

class ClearTimeline(Message):
    """Custom message to clear the timeline."""
    pass

# ... other custom messages
```

**Integration Notes:**
- The `elia_adapter.py` will likely contain logic to translate events from Elia App's UI system into our `UserMessage` (or similar) and post them to our `LLMReplApp`.
- Conversely, our `LLMReplApp` might need to post messages that Elia App can understand for certain actions (e.g., closing the application).

---

## Event Handling Mapping (within Elia App)

Keyboard shortcuts and other user interactions will be handled by Textual's event system within our embedded `LLMReplApp`.

#### Elia App Implementation (Existing event handling)
- Elia App may have its own global keyboard shortcuts or event handlers. We need to ensure ours don't conflict or are prioritized when our component is in focus.

#### LLM REPL Textual Implementation (Our BINDINGS and action methods)
```python
# llm_repl_ui/app.py (Example BINDINGS)
BINDINGS = [
    ("enter", "send_message", "Send"),
    ("ctrl+enter", "send_message", "Send"), 
    ("ctrl+l", "clear_timeline", "Clear"),
    ("ctrl+c", "quit", "Quit"),
    ("escape", "cancel_processing", "Cancel"),
]

def action_send_message(self) -> None:
    """Sends the current input message via a UserMessage."""
    input_widget = self.query_one("#user-input", Input)
    if input_widget.value.strip():
        self.post_message(UserMessage(input_widget.value))

def action_clear_timeline(self) -> None:
    """Clears the timeline by posting a ClearTimeline message."""
    timeline = self.query_one("#timeline", TimelineWidget) 
    timeline.clear()
```

**Integration Notes:**
- Textual's `BINDINGS` will handle keyboard events when our `LLMReplApp` or its child widgets have focus.
- Careful consideration is needed if Elia App has conflicting global shortcuts. This might require Elia to conditionally disable its shortcuts when our component is active.

This revised mapping focuses on how our existing Textual components will fit into the "Elia App" framework, highlighting the necessary integration points and adaptations.
