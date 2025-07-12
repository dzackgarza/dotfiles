# Architecture Guide

> **CRITICAL PRINCIPLE**: Build from PROVEN working implementations. Study V3, Gemini CLI, and Claude Code patterns BEFORE designing new components.

## Sacred GUI Architecture Overview

### Three-Area Layout (IMMUTABLE)

```
┌─────────────────────────────────┐
│        Sacred Timeline         │ ← VerticalScroll (V3's chat_container pattern)
│  ┌─ Turn 1 ─────────────────┐   │
│  │ 👤 User: "Question..."   │   │
│  │ 🧠 Cognition → Response  │   │  
│  │ 🤖 Assistant: "Answer..." │   │
│  └─────────────────────────────┘   │
│  ═══════════════════════════════   │ ← hrule separators
│  ┌─ Turn 2 ─────────────────┐   │
│  │ 👤 User: "Follow-up..."  │   │
│  │ 🧠 Cognition → Response  │   │
│  │ 🤖 Assistant: "More..."  │   │
│  └─────────────────────────────┘   │
├─────────────────────────────────┤
│        Live Workspace          │ ← VerticalScroll (V3's dynamic container pattern)
│  ⚡ Route Query    [active]     │   (only visible during processing)
│  ⏳ Research       [pending]    │
│  ⏳ Synthesize     [pending]    │
│  ⏳ Response       [pending]    │
├─────────────────────────────────┤
│           Input Area            │ ← PromptInput (V3's input pattern)
│  > Next question here...        │
└─────────────────────────────────┘
```

### Why This Architecture Works

**✅ Based on V3's Proven Patterns:**
- Sacred Timeline uses V3's `chat_container` pattern (VerticalScroll + simple widgets)
- Live Workspace uses V3's dynamic container approach
- No nested containers (V3's golden rule)

**✅ Clean Separation of Concerns:**
- **Sacred Timeline**: Immutable conversation history
- **Live Workspace**: Real-time cognition streaming  
- **Input**: User interaction

**✅ Scalable Design:**
- Unlimited conversation history via scrolling
- Dynamic cognition pipelines (N sub-modules)
- Simple state transitions (2-way ↔ 3-way)

## Core Architectural Principles

### 1. Sacred Timeline (Append-Only Truth)

```python
# Every operation becomes an immutable block
timeline = [
    SystemBlock("LLM REPL v3.1 started"),
    UserBlock("Tell me about quantum computing"),
    CognitionBlock("Route → Research → Synthesize"),
    AssistantBlock("Quantum computing is..."),
    # ... more blocks (infinite scrolling)
]
```

**Rules:**
- Once inscribed, blocks are immutable
- Timeline is the absolute source of truth
- All context comes from timeline history
- Visual representation matches data structure

### 2. Sacred Turn Structure (Immutable Rhythm)

```
[User Input] → [Cognition Pipeline] → [Assistant Response]
```

**Every turn follows this pattern:**
1. User submits input → Live Workspace appears (2-way → 3-way)
2. Cognition pipeline executes with streaming sub-modules
3. Final response completes → Content moves to Sacred Timeline
4. Live Workspace disappears (3-way → 2-way)

### 3. V3's Proven Widget Patterns

**COPY THESE EXACT PATTERNS:**

```python
# V3's Chatbox pattern - COPY THIS
class SimpleBlockWidget(Widget):
    def render(self) -> RenderableType:
        return Panel(self.content)  # No child widgets!

# V3's chat_container pattern - COPY THIS  
class SacredTimelineWidget(VerticalScroll):
    def compose(self) -> ComposeResult:
        # Only yield simple widgets
        for block in self.blocks:
            yield SimpleBlockWidget(block)
            yield HRuleWidget()  # Simple separator
```

**❌ NEVER DO THIS (causes layout conflicts):**
```python
# BROKEN: Nested containers
class BrokenWidget(Widget):
    def compose(self) -> ComposeResult:
        with VerticalScroll():  # ❌ Nested!
            with Vertical():    # ❌ More nesting!
                yield SomeWidget()
```

## Implementation Architecture

### Widget Hierarchy (V3-Based)

```
LLMReplApp (Textual App)
├── SacredTimelineWidget (VerticalScroll)
│   ├── SimpleBlockWidget (render() only)
│   ├── HRuleWidget (render() only) 
│   └── SimpleBlockWidget (render() only)
├── LiveWorkspaceWidget (VerticalScroll) 
│   ├── SubModuleWidget (render() only)
│   ├── SubModuleWidget (render() only)
│   └── SubModuleWidget (render() only)
└── PromptInput (Widget)
```

### State Management (Centralized)

```python
# Central state object (singleton)
class UnifiedTimeline:
    def __init__(self):
        self.inscribed_blocks = []  # Sacred Timeline
        self.live_blocks = []       # Live Workspace
        self.current_state = "idle" # 2-way vs 3-way
    
    def add_live_block(self, role, content):
        """Add to Live Workspace (streaming)"""
        
    def inscribe_block(self, live_block):
        """Move to Sacred Timeline (permanent)"""
        
    def clear_workspace(self):
        """Hide Live Workspace (3-way → 2-way)"""
```

### Event Flow (Unidirectional)

```
User Input → PromptInput → UnifiedAsyncProcessor → Live Workspace
     ↓
Cognition Pipeline → SubModules → Streaming Updates
     ↓  
Completion → Sacred Timeline ← Live Workspace (cleared)
```

## Threading & Streaming Architecture

### V3's Thread-Safe Pattern (COPY THIS)

```python
# Background processing
@work(thread=True)
async def process_cognition(self):
    async for sub_module in cognition_pipeline:
        # Thread-safe UI update (V3 pattern)
        self.app.call_from_thread(
            self.live_workspace.add_sub_module, 
            sub_module
        )
        
        # Stream content updates
        async for chunk in sub_module.stream():
            self.app.call_from_thread(
                sub_module_widget.update_content,
                chunk
            )
```

### Smart Auto-Scroll (V3 Pattern)

```python
# Only scroll when user is at bottom
def should_auto_scroll(self) -> bool:
    return self.scroll_y >= self.max_scroll_y - 1

def add_content(self, content):
    self.mount(content)
    if self.should_auto_scroll():
        self.scroll_end()  # Follow new content
```

## Error Handling Architecture

### Fail-Fast Validation (At Every Boundary)

```python
class SimpleBlockWidget(Widget):
    def __init__(self, block_data):
        super().__init__()
        self.data = self._validate_block_data(block_data)
    
    def _validate_block_data(self, data):
        if not hasattr(data, 'role'):
            raise ValueError(f"Block missing 'role': {data}")
        if data.role not in ['user', 'assistant', 'cognition']:
            raise ValueError(f"Invalid role: {data.role}")
        return data
```

### Error Boundaries (Graceful Degradation)

```python
class ErrorBoundaryWidget(Widget):
    def __init__(self, child_widget):
        super().__init__()
        try:
            self.child = child_widget
            self.error = None
        except Exception as e:
            self.child = None
            self.error = e
    
    def render(self):
        if self.error:
            return Panel(f"Error: {self.error}", border_style="red")
        return self.child.render()
```

## CSS Architecture (V3-Compatible)

### Valid Textual Properties (COPY V3 PATTERNS)

```css
/* Sacred Timeline (V3's chat_container styles) */
.sacred-timeline {
    height: 100%;
    border: solid blue;      /* Valid Textual syntax */
    background: #1a1a1a;
}

/* Simple Blocks (V3's Chatbox styles) */
.simple-block {
    height: auto;           /* Content-driven sizing */
    min-width: 12;
    margin: 1 0;
    padding: 1;
    border: solid green;
}

/* Live Workspace (V3's dynamic container) */
.live-workspace {
    height: auto;
    max-height: 50vh;
    border: solid yellow;
}

.live-workspace.hidden {
    display: none;          /* 2-way split when idle */
}
```

### ❌ Invalid Properties (Will Break)

```css
/* These properties don't exist in Textual */
.broken-styles {
    border-color: blue;     /* ❌ Use: border: solid blue */
    background-color: red;  /* ❌ Use: background: red */
    font-family: Arial;     /* ❌ Not supported */
}
```

## Architecture Decision Records

### Why V3 Patterns?

**Decision**: Copy V3's VerticalScroll + render() pattern exactly

**Rationale**: 
- V3's chat interface works perfectly in production
- Proven to handle unlimited scrolling content
- No layout conflicts or sizing issues
- Thread-safe streaming patterns validated

**Alternatives Considered**:
- Custom layout managers → Rejected (too complex)
- Nested containers → Rejected (causes conflicts)
- Novel widget patterns → Rejected (untested)

### Why Three-Area Layout?

**Decision**: Sacred Timeline + Live Workspace + Input

**Rationale**:
- Clean separation of concerns (history vs processing vs input)
- Scales to unlimited content via scrolling
- Simple state transitions (2-way ↔ 3-way)
- Matches user mental model

### Why Immutable Timeline?

**Decision**: Append-only blocks, no editing

**Rationale**:
- Provides absolute source of truth
- Enables reliable context reconstruction
- Prevents state corruption
- Matches conversation flow

## Reference Implementation Paths

**Study These First (In Order):**

1. **V3's Chat Widget** - `V3/elia_chat/widgets/chat.py`
   - How VerticalScroll works with dynamic content
   - Thread-safe updates with `call_from_thread()`
   - Smart auto-scroll behavior

2. **V3's Chatbox Widget** - `V3/elia_chat/widgets/chatbox.py`  
   - Simple render() pattern (no child widgets)
   - Content-driven sizing
   - Clean Panel-based rendering

3. **Textual Examples** - `reference/textual-docs/textual/examples/`
   - Calculator for widget composition
   - Dictionary for API integration
   - Stopwatch for real-time updates

4. **Claude Code Patterns** - `reference/inspiration/anthropic-ai-claude-code/`
   - Production TUI patterns
   - Error handling approaches
   - Streaming response management

---

**Next Steps**: After understanding this architecture, see:
- Implementation Guide → `.ai/docs/IMPLEMENTATION-GUIDE.md`
- Testing Guide → `.ai/docs/TESTING-GUIDE.md`
- Design Guide → `.ai/docs/DESIGN-GUIDE.md`