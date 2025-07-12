# Reference Guide

> **CRITICAL**: These are WORKING implementations that should be your FIRST resource when developing. Always study how successful projects solve problems before writing new code.

## Primary Working References (Study These First)

### 1. V3 Chat Implementation (HIGHEST PRIORITY)

**Location**: `V3/elia_chat/widgets/`

**Why Critical**: V3's chat interface works perfectly in production with proven patterns.

**Key Files to Study**:

```bash
V3/elia_chat/widgets/
├── chat.py              # 🏆 GOLDEN REFERENCE: VerticalScroll + dynamic content
├── chatbox.py           # 🏆 GOLDEN REFERENCE: Simple Widget with render()
├── conversation.py      # Thread-safe message handling
└── chat.tcss           # Working CSS patterns
```

**V3 Patterns to Copy**:

```python
# COPY THIS: V3's VerticalScroll pattern
class ChatContainer(VerticalScroll):
    def compose(self) -> ComposeResult:
        # Simple widgets only - NO nested containers
        for message in self.messages:
            yield Chatbox(message)

# COPY THIS: V3's simple widget pattern  
class Chatbox(Widget):
    def render(self) -> RenderableType:
        # Direct render - no child widgets
        return Panel(self.content, border_style=self.border_style)

# COPY THIS: V3's thread-safe updates
@work(thread=True)
async def add_message(self):
    # Thread-safe UI update
    self.app.call_from_thread(self.chat_container.mount, chatbox)
```

**V3 CSS Patterns to Copy**:

```css
/* COPY FROM: V3/elia_chat/widgets/chat.tcss */
.chat-container {
    height: 100%;
    border: solid blue;     /* Valid Textual syntax */
    background: #1a1a1a;
}

.chatbox {
    height: auto;          /* Content-driven sizing */
    margin: 1 0;
    padding: 1;
}
```

### 2. Claude Code Package (Production TUI Patterns)

**Location**: `reference/inspiration/anthropic-ai-claude-code-1.0.44.tgz`

**Why Important**: Production-ready terminal UI patterns and error handling.

**Extract and Study**:

```bash
cd reference/inspiration/
tar -xzf anthropic-ai-claude-code-1.0.44.tgz
find claude-code/ -name "*.py" | xargs grep -l "textual\|TUI\|terminal"
```

**Patterns to Extract**:
- Error boundary implementations
- Streaming response handling
- Performance optimization patterns
- Terminal UI best practices
- Configuration management

### 3. Gemini CLI (LLM Interface Patterns)

**Location**: `reference/inspiration/gemini-cli/`

**Why Valuable**: Working LLM terminal interface with conversation management.

**Study These Patterns**:

```bash
cd reference/inspiration/gemini-cli/
find . -name "*.py" | xargs grep -l "stream\|response\|chat\|conversation"
```

**Key Concepts to Adapt**:
- Multi-model conversation management
- Command parsing and routing
- Configuration and persistence
- User experience patterns
- LLM API integration

### 4. Textual Framework Examples

**Location**: `reference/textual-docs/textual/examples/`

**Why Essential**: Official framework patterns and best practices.

**Critical Examples**:

```bash
textual/examples/
├── calculator.py          # Widget composition patterns
├── code_browser.py        # File tree navigation
├── dictionary.py          # API integration and search
├── markdown_browser.py    # Content rendering
├── stopwatch.py          # Real-time updates
└── tree_view.py          # Hierarchical data display
```

**Patterns to Study**:

```python
# From calculator.py - Error handling
try:
    result = self.calculate()
except Exception as e:
    self.display_error(str(e))

# From stopwatch.py - Real-time updates
@work(thread=True)
async def update_timer(self):
    while self.running:
        self.call_from_thread(self.update_display)
        await asyncio.sleep(0.1)

# From dictionary.py - API integration
async def search(self, term):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"/api/search?q={term}")
        return response.json()
```

## Working Pattern Libraries

### Textual Widget Patterns

**Core Scrollable Patterns** (Copy These):

```python
# From textual/widgets/scroll_view.py
class ScrollableContainer(ScrollView):
    def __init__(self):
        super().__init__()
        self.can_focus = False  # V3 pattern
    
    def add_content(self, content):
        self.mount(content)
        if self.should_auto_scroll():
            self.scroll_end()

# From textual/widgets/vertical_scroll.py  
class DynamicContainer(VerticalScroll):
    def compose(self) -> ComposeResult:
        # Only yield simple widgets
        for item in self.items:
            yield SimpleWidget(item)
```

**Input Handling Patterns**:

```python
# From textual/widgets/input.py
class TextInput(Input):
    def on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            self.post_message(self.Submitted(self.value))
            self.value = ""  # Clear for next input

# From textual/widgets/text_area.py
class MultiLineInput(TextArea):
    def on_key(self, event: events.Key) -> None:
        if event.key == "ctrl+enter":
            self.post_message(self.Submitted(self.text))
```

### CSS Pattern Library

**Layout Patterns** (Textual-Valid):

```css
/* From textual core CSS */
.container {
    height: 100%;
    width: 100%;
    display: block;
}

.scrollable {
    overflow-y: auto;
    height: auto;
    max-height: 80vh;
}

.content-driven {
    height: auto;          /* Key pattern - never fixed heights */
    min-height: 3;
    width: auto;
    min-width: 10;
}
```

**Color and Border Patterns**:

```css
/* Valid Textual CSS syntax */
.widget {
    border: solid blue;    /* NOT border-color: blue */
    background: #1a1a1a;   /* NOT background-color */
    color: white;
    opacity: 0.8;
}

.focused {
    border: solid yellow;
    box-shadow: 0 0 0 1px yellow; /* Limited shadow support */
}
```

## Anti-Pattern Examples (What NOT to Copy)

### Broken Widget Patterns (DON'T DO THIS)

```python
# ❌ BROKEN: Nested containers in VerticalScroll
class BrokenWidget(Widget):
    def compose(self) -> ComposeResult:
        with VerticalScroll():
            with Vertical():     # ❌ Nested containers
                yield SomeWidget()

# ❌ BROKEN: Complex child widget hierarchies
class OverComplexWidget(Widget):
    def compose(self) -> ComposeResult:
        with Container():
            with ScrollView():
                with Vertical():
                    with Horizontal():  # ❌ Too much nesting
                        yield Widget()
```

### Invalid CSS Patterns (DON'T USE)

```css
/* ❌ These properties don't exist in Textual */
.broken-widget {
    border-color: blue;     /* Use: border: solid blue */
    background-color: red;  /* Use: background: red */
    font-family: Arial;     /* Not supported */
    font-size: 14px;        /* Not supported */
    border-radius: 5px;     /* Not supported */
    position: absolute;     /* Not supported */
    z-index: 100;          /* Not supported */
}
```

## Quick Reference Commands

### Extract and Study Patterns

```bash
# STEP 1: Study V3's proven patterns (HIGHEST PRIORITY)
cd V3/elia_chat/widgets/
cat chat.py | grep -A 10 "class\|def\|mount\|VerticalScroll"
cat chatbox.py | grep -A 5 "render\|Panel\|border"

# STEP 2: Extract Claude Code patterns
cd reference/inspiration/
tar -xzf anthropic-ai-claude-code-1.0.44.tgz
find claude-code/ -name "*.py" | head -10
grep -r "textual\|TUI" claude-code/ | head -5

# STEP 3: Study Gemini CLI patterns  
cd reference/inspiration/gemini-cli/
find . -name "*.py" | xargs grep -l "class.*Widget\|stream\|async"

# STEP 4: Search Textual examples for specific patterns
cd reference/textual-docs/textual/examples/
grep -rn "VerticalScroll\|Widget\|render\|mount" . | head -10
grep -rn "call_from_thread\|work\|async" . | head -5
```

### Pattern Search Queries

```bash
# Find scrolling patterns
grep -r "VerticalScroll\|ScrollView" reference/ | head -10

# Find widget composition patterns  
grep -r "def compose\|ComposeResult" reference/ | head -10

# Find render patterns
grep -r "def render\|RenderableType" reference/ | head -10

# Find threading patterns
grep -r "call_from_thread\|@work" reference/ | head -10

# Find CSS patterns
find reference/ -name "*.css" -o -name "*.tcss" | xargs grep -h "border\|background\|height"
```

### Validation Commands

```bash
# Validate CSS against Textual syntax
grep -r "border-color\|background-color\|font-family" src/ && echo "❌ Invalid CSS found" || echo "✅ CSS looks valid"

# Check for nested container anti-patterns
grep -r "with.*Vertical.*:" src/ | grep -v "^#" && echo "❌ Possible nesting issues" || echo "✅ No obvious nesting"

# Find V3 pattern usage
grep -r "VerticalScroll\|render()" src/ && echo "✅ Using V3 patterns" || echo "❌ Missing V3 patterns"
```

## Integration Guidelines

### How to Use Reference Materials

#### 1. Research Phase (Required)

```
🔍 BEFORE writing ANY new code:
   ↓
📚 Study V3 equivalent (chat.py, chatbox.py)
   ↓  
📚 Find similar pattern in Claude Code/Gemini CLI
   ↓
📚 Check Textual examples for framework best practices
   ↓
📝 Document which patterns you're adapting and why
```

#### 2. Adaptation Phase

```
📋 Copy working pattern as base
   ↓
🔧 Adapt for Sacred Architecture needs
   ↓
✅ Test that adapted pattern works like original
   ↓
📚 Document changes made and rationale
```

#### 3. Validation Phase

```
🧪 Test against original behavior
   ↓
🔍 Verify no anti-patterns introduced
   ↓
📊 Performance comparable to reference
   ↓
✅ Sacred Architecture compliance maintained
```

### Reference Integration Checklist

```
☐ Studied relevant V3 pattern first
☐ Found similar approach in Claude Code/Gemini CLI
☐ Reviewed Textual examples for framework compliance
☐ Identified specific code/CSS to copy
☐ Documented adaptation rationale
☐ Tested adapted pattern works like original
☐ Verified Sacred Architecture compliance
☐ No anti-patterns introduced
☐ Performance acceptable
☐ Code commented with reference sources
```

## Troubleshooting with References

### When Widgets Don't Work

```bash
# Compare against V3's working pattern
diff -u src/widgets/my_widget.py V3/elia_chat/widgets/chatbox.py

# Check if using V3's exact pattern
grep -A 5 "class.*Widget" V3/elia_chat/widgets/chatbox.py
grep -A 5 "def render" V3/elia_chat/widgets/chatbox.py
```

### When CSS Doesn't Apply

```bash
# Compare against V3's working CSS
cat V3/elia_chat/widgets/chat.tcss
diff -u src/widgets/my_widget.tcss V3/elia_chat/widgets/chat.tcss

# Validate Textual CSS syntax
grep "border-color\|background-color" src/widgets/*.tcss  # Should find nothing
```

### When Layout Breaks

```bash
# Check for nested container anti-patterns
grep -r "with.*Vertical" src/widgets/ | grep -v "^#"
grep -r "with.*ScrollView" src/widgets/ | grep -v "^#"

# Compare layout approach to V3
grep -A 10 "def compose" V3/elia_chat/widgets/chat.py
```

## Reference Documentation Map

### V3 Codebase Structure

```
V3/
├── elia_chat/
│   ├── widgets/
│   │   ├── chat.py              # 🏆 Main container pattern
│   │   ├── chatbox.py           # 🏆 Message widget pattern
│   │   ├── conversation.py      # Message management
│   │   └── chat.tcss           # 🏆 Working CSS patterns
│   ├── models/
│   │   ├── message.py          # Data structures
│   │   └── conversation.py     # State management
│   └── services/
│       ├── llm_service.py      # API integration
│       └── streaming.py        # Real-time updates
```

### Claude Code Structure (After Extraction)

```
claude-code/
├── src/
│   ├── ui/                     # TUI components
│   ├── streaming/              # Response handling
│   ├── error_handling/         # Error boundaries
│   └── config/                 # Configuration patterns
├── styles/                     # CSS patterns
└── examples/                   # Usage patterns
```

### Textual Examples Map

```
textual/examples/
├── basic_widgets/              # Simple widget patterns
├── layout_examples/            # Container patterns
├── streaming_examples/         # Real-time update patterns
├── error_handling/             # Error boundary patterns
└── css_examples/              # Styling patterns
```

---

**Remember**: These references contain PROVEN, WORKING code. Copy their patterns, adapt for Sacred Architecture, but don't reinvent solutions that already work perfectly.

**Next Steps**: After studying references, see:
- Architecture Guide → `.ai/docs/ARCHITECTURE-GUIDE.md`
- Implementation Guide → `.ai/docs/IMPLEMENTATION-GUIDE.md`
- Testing Guide → `.ai/docs/TESTING-GUIDE.md`