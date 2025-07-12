# Implementation Guide

> **CRITICAL**: Always start by copying working patterns from V3, then adapt for Sacred GUI Architecture. NEVER write widgets from scratch.

## Development Workflow (Required Order)

### 1. Study Working Code FIRST

```bash
# STEP 1: Study V3's proven patterns
cd V3/elia_chat/widgets/
cat chat.py          # VerticalScroll + dynamic content
cat chatbox.py       # Simple Widget with render()

# STEP 2: Find similar patterns in references
cd .ai/docs/REFERENCE-GUIDE.md  # Working examples
cd reference/inspiration/       # Claude Code, Gemini CLI
```

### 2. Copy, Don't Create

```python
# ✅ CORRECT: Copy V3 pattern, adapt for Sacred GUI
class SacredTimelineWidget(VerticalScroll):
    """COPIED from V3's chat_container pattern"""
    
    def __init__(self):
        super().__init__(id="sacred-timeline")
        self.blocks = []
    
    def add_block(self, block_data):
        # V3's mounting pattern
        block_widget = SimpleBlockWidget(block_data)
        self.mount(block_widget)
        
        # V3's auto-scroll pattern
        if self.scroll_y >= self.max_scroll_y - 1:
            self.scroll_end()

# ✅ CORRECT: Copy V3's Chatbox pattern  
class SimpleBlockWidget(Widget):
    """COPIED from V3's Chatbox pattern"""
    
    def render(self) -> RenderableType:
        # Direct render like V3 - no child widgets
        return Panel(
            self.content,
            title=self.title,
            border_style=self.border_style
        )
```

### 3. Adapt for Sacred Architecture

```python
# Adapt V3 pattern for our three-area layout
class LiveWorkspaceWidget(VerticalScroll):
    """V3's dynamic container adapted for cognition streaming"""
    
    def __init__(self):
        super().__init__(id="live-workspace", classes="hidden")
        self.sub_modules = []
    
    def show_workspace(self):
        """2-way → 3-way split"""
        self.remove_class("hidden")
    
    def hide_workspace(self):
        """3-way → 2-way split"""
        self.add_class("hidden")
        self.remove_children()  # Clear for next turn
```

## Widget Development Patterns

### V3's Proven Widget Template

```python
# TEMPLATE: Copy this exact pattern for all widgets
class ExampleWidget(Widget):
    """
    Sacred Architecture Widget Template
    COPIED FROM: V3/elia_chat/widgets/chatbox.py
    """
    
    def __init__(self, data):
        super().__init__()
        # Fail-fast validation (V3 pattern)
        self.data = self._validate_data(data)
        self.update_timer = None
    
    def render(self) -> RenderableType:
        """
        V3's render pattern - NO child widgets!
        Direct Panel rendering only
        """
        return Panel(
            self._build_content(),
            title=self._get_title(), 
            border_style=self._get_border_style()
        )
    
    def _validate_data(self, data):
        """V3's fail-fast validation"""
        if not hasattr(data, 'required_field'):
            raise ValueError(f"Invalid data: {data}")
        return data
    
    def _build_content(self) -> str:
        """Generate content for Panel"""
        return str(self.data.content)
    
    def _get_title(self) -> str:
        """Dynamic title based on data"""
        return f"{self.data.role}: {self.data.timestamp}"
    
    def _get_border_style(self) -> str:
        """Color coding like V3"""
        role_colors = {
            "user": "green",
            "assistant": "blue", 
            "cognition": "yellow",
            "system": "red"
        }
        return role_colors.get(self.data.role, "white")
```

### Thread-Safe Streaming (V3 Pattern)

```python
# COPIED FROM: V3/elia_chat/widgets/chat.py line 194
@work(thread=True, group="streaming")
async def stream_cognition_step(self, step_data):
    """V3's proven thread-safe streaming pattern"""
    
    # Create sub-module widget
    sub_module = SubModuleWidget(step_data)
    
    # Thread-safe UI update (V3's exact pattern)
    self.app.call_from_thread(
        self.live_workspace.mount, 
        sub_module
    )
    
    # Stream content updates
    async for chunk in step_data.stream():
        # V3's thread-safe content update
        self.app.call_from_thread(
            sub_module.update_content,
            chunk
        )
        
        # Check for cancellation (V3 pattern)
        worker = get_current_worker()
        if worker.is_cancelled:
            break
    
    # Mark as complete (V3 pattern)
    self.app.call_from_thread(
        sub_module.mark_complete
    )
```

### Error Boundary Pattern (Adapted from Textual Examples)

```python
# ADAPTED FROM: textual/examples/calculator.py error handling
class ErrorBoundaryWidget(Widget):
    """Graceful error handling for Sacred Architecture"""
    
    def __init__(self, child_widget_class, *args, **kwargs):
        super().__init__()
        try:
            self.child = child_widget_class(*args, **kwargs)
            self.error = None
        except Exception as e:
            self.child = None
            self.error = e
            self.log.error(f"Widget creation failed: {e}")
    
    def render(self) -> RenderableType:
        if self.error:
            return Panel(
                f"[red]Error: {self.error}[/red]\n"
                f"[dim]Widget: {self.child.__class__.__name__}[/dim]",
                title="Widget Error",
                border_style="red"
            )
        return self.child.render()

# Usage pattern
def create_safe_widget(widget_class, *args, **kwargs):
    """Factory for error-boundary wrapped widgets"""
    return ErrorBoundaryWidget(widget_class, *args, **kwargs)
```

## Layout Implementation (V3-Based)

### Main App Layout (Copy V3's Structure)

```python
# COPIED FROM: V3/elia_chat/widgets/chat.py compose() method
class LLMReplApp(App):
    def compose(self) -> ComposeResult:
        """Sacred Architecture: V3's proven layout pattern"""
        
        with Vertical(id="main-container"):
            # Sacred Timeline (V3's chat_container)
            yield SacredTimelineWidget(id="sacred-timeline")
            
            # Live Workspace (V3's dynamic container, initially hidden)
            yield LiveWorkspaceWidget(id="live-workspace", classes="hidden")
            
            # Input (V3's input pattern)
            yield PromptInput(id="prompt-input")
    
    def on_mount(self):
        """V3's initialization pattern"""
        self.sacred_timeline = self.query_one("#sacred-timeline")
        self.live_workspace = self.query_one("#live-workspace")
        self.prompt_input = self.query_one("#prompt-input")
        
        # Focus input (V3 pattern)
        self.prompt_input.focus()
```

### State Transitions (V3-Inspired)

```python
class WorkspaceController:
    """Manages 2-way ↔ 3-way split transitions"""
    
    def __init__(self, app):
        self.app = app
        self.timeline = app.query_one("#sacred-timeline")
        self.workspace = app.query_one("#live-workspace")
    
    async def start_turn(self, user_input):
        """2-way → 3-way: Show live workspace"""
        
        # Add user block to timeline (V3 pattern)
        user_block = InscribedBlock("user", user_input)
        await self.timeline.add_block(user_block)
        
        # Show workspace (2-way → 3-way)
        self.workspace.show_workspace()
        
        # Start cognition processing
        await self.process_cognition(user_input)
    
    async def complete_turn(self, assistant_response):
        """3-way → 2-way: Move content to timeline"""
        
        # Add assistant block to timeline
        assistant_block = InscribedBlock("assistant", assistant_response)
        await self.timeline.add_block(assistant_block)
        
        # Hide workspace (3-way → 2-way)
        self.workspace.hide_workspace()
        
        # Focus input for next turn
        self.app.query_one("#prompt-input").focus()
```

## CSS Implementation (V3-Compatible)

### Sacred Architecture Styles (Copy V3)

```css
/* COPIED FROM: V3's chat container styles */
.sacred-timeline {
    height: 100%;
    border: solid $primary;
    background: $surface;
    padding: 1;
}

/* V3's Chatbox styles adapted */
.simple-block {
    height: auto;          /* V3's content-driven sizing */
    min-width: 12;         /* V3's minimum width */
    margin: 1 0;           /* V3's spacing */
    padding: 1;            /* V3's padding */
}

.simple-block-user {
    border: solid green;   /* V3's color coding */
}

.simple-block-assistant {
    border: solid blue;
}

.simple-block-cognition {
    border: solid yellow;
}

/* Live workspace (V3's dynamic container) */
.live-workspace {
    height: auto;
    max-height: 50vh;      /* Limit to half screen */
    border: solid yellow;
    background: $surface;
    padding: 1;
}

.live-workspace.hidden {
    display: none;         /* Clean 2-way split */
}

/* Sub-modules (V3's dynamic content) */
.sub-module {
    height: auto;
    margin: 0 0 1 0;
    padding: 1;
    border: solid gray;
}

.sub-module.active {
    border: solid yellow;  /* Currently processing */
}

.sub-module.completed {
    border: solid green;   /* Finished */
    opacity: 0.8;
}
```

## Development Process

### 1. Widget Development Checklist

```
☐ Study V3 equivalent pattern first
☐ Copy V3 pattern, don't write from scratch  
☐ Adapt for Sacred Architecture needs
☐ Add fail-fast validation
☐ Include error boundary support
☐ Write widget-specific tests
☐ Validate CSS uses only valid Textual properties
☐ Test with streaming content simulation
```

### 2. Integration Checklist

```
☐ Widget works in isolation
☐ Integrates with UnifiedTimeline state
☐ Follows V3's thread-safe patterns
☐ Handles error boundaries gracefully
☐ CSS styles work in all screen sizes
☐ No nested container conflicts
☐ Memory leaks prevented
☐ Performance acceptable with large content
```

### 3. Sacred Architecture Compliance

```
☐ Uses VerticalScroll + render() pattern (no nested containers)
☐ Follows 2-way ↔ 3-way split behavior
☐ Maintains Sacred Timeline immutability
☐ Implements proper state transitions
☐ Error handling doesn't break app
☐ Thread-safe streaming updates
☐ Content-driven dynamic sizing
☐ Smart auto-scroll behavior
```

## Common Implementation Patterns

### Event Handling (V3 Pattern)

```python
# V3's event handling approach
class PromptInput(Widget):
    def on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            # V3's message emission pattern
            self.post_message(self.PromptSubmitted(self.text))
            self.text = ""  # Clear for next input

class LLMReplApp(App):
    def on_prompt_input_prompt_submitted(self, event):
        """Handle user input (V3 event pattern)"""
        asyncio.create_task(self.process_user_input(event.text))
```

### Content Updates (V3 Streaming)

```python
# V3's content update pattern
class SubModuleWidget(Widget):
    def __init__(self, step_data):
        super().__init__()
        self.step_data = step_data
        self.content_buffer = ""
        self.status = "pending"
    
    def update_content(self, chunk: str):
        """V3's streaming update pattern"""
        self.content_buffer += chunk
        self.refresh()  # Trigger re-render
    
    def mark_complete(self):
        """V3's completion pattern"""
        self.status = "completed"
        self.refresh()
```

### Memory Management (V3 Pattern)

```python
# V3's cleanup patterns
class LiveWorkspaceWidget(VerticalScroll):
    def clear_workspace(self):
        """Clean memory when hiding workspace"""
        # Remove all children (V3 pattern)
        self.remove_children()
        
        # Clear references
        self.sub_modules.clear()
        
        # Force garbage collection if needed
        import gc; gc.collect()
```

## File Organization (Sacred Architecture)

```
src/widgets/
├── sacred_timeline.py      # V3's chat_container → Sacred Timeline
├── live_workspace.py       # V3's dynamic container → Live Workspace
├── simple_block.py         # V3's Chatbox → Block widgets
├── sub_module.py           # V3's message → Sub-module widgets
├── prompt_input.py         # V3's input → Prompt input
└── error_boundary.py       # Graceful error handling

src/services/
├── workspace_controller.py # State transitions (2-way ↔ 3-way)
├── streaming_service.py    # V3's thread-safe streaming
└── timeline_service.py     # Sacred Timeline operations

src/state/
├── unified_timeline.py     # Central state (singleton)
└── block_models.py        # Data structures
```

## Testing Integration

```python
# Test V3 patterns work with Sacred Architecture
@pytest.mark.asyncio
async def test_v3_pattern_integration():
    """Ensure V3 patterns work in Sacred Architecture"""
    app = LLMReplApp()
    
    async with app.run_test() as pilot:
        # Test V3's VerticalScroll pattern
        timeline = app.query_one("#sacred-timeline")
        assert isinstance(timeline, VerticalScroll)
        
        # Test no nested containers (V3 rule)
        for child in timeline.children:
            assert not isinstance(child, (Vertical, VerticalScroll))
            assert hasattr(child, 'render')  # V3 render pattern
        
        # Test state transitions work
        await timeline.add_block(test_block)
        assert len(timeline.children) > 0
```

---

**Next Steps**: After implementing with these patterns, see:
- Testing Guide → `.ai/docs/TESTING-GUIDE.md`
- Design Guide → `.ai/docs/DESIGN-GUIDE.md`
- Reference Guide → `.ai/docs/REFERENCE-GUIDE.md`