# Reference Materials

> **CRITICAL**: This directory contains WORKING implementations that should be your FIRST resource when developing. Always study how successful projects solve problems before writing new code.

This directory contains external documentation, inspiration projects, and comprehensive reference materials for development.

## Directory Overview

```
reference/
├── README.md                           # This overview
├── textual-docs/                      # Complete Textual framework documentation
├── inspiration/                       # Reference implementations and examples
│   ├── anthropic-ai-claude-code-1.0.44.tgz  # Claude Code package (56MB)
│   ├── gemini-cli/                    # Google's Gemini CLI implementation  
│   └── .opencode/                     # OpenCode project reference
└── external-apis.md                   # API documentation and integration guides
```

## Reference Materials Overview

### 📚 **Textual Framework Documentation**

```
textual-docs/
├── textual/                           # Complete Textual source and docs
│   ├── docs/                         # Official documentation  
│   ├── src/textual/                  # Framework source code
│   ├── tests/                        # Comprehensive test suite
│   └── examples/                     # Reference implementations
```

**Key Documentation Sections:**
- **Widget Development**: `textual/docs/widgets/`
- **CSS Styling**: `textual/docs/css/`  
- **Layout Systems**: `textual/docs/layout/`
- **Event Handling**: `textual/docs/events/`
- **Testing Patterns**: `textual/tests/`

### 🏆 **PROVEN WORKING IMPLEMENTATIONS**

**These are the GOLD STANDARD** - study these first before writing any new code:

#### **Claude Code Package** (`anthropic-ai-claude-code-1.0.44.tgz`)
- **Size**: 56MB
- **Purpose**: Reference implementation of Claude Code interface
- **Key Features**: Terminal UI patterns, streaming responses, error handling
- **Usage**: Extract and study for proven TUI patterns

#### **Gemini CLI** (`gemini-cli/`)  
- **Purpose**: Google's reference implementation for LLM CLI tools
- **Architecture**: Command-line interface with conversation management
- **Key Features**: Multi-model support, conversation persistence, streaming
- **Usage**: Study architecture patterns and UX approaches

#### **OpenCode Project** (`.opencode/`)
- **Purpose**: Open-source code analysis and development tools
- **Architecture**: Modular plugin system with TUI interface
- **Key Features**: Plugin architecture, code analysis, development workflows
- **Usage**: Reference for plugin system design and modular architecture

## Textual Framework Quick Reference

### 🏗️ **Core Widget Patterns**

```python
# Sacred Architecture Widget Pattern (from Textual docs)
from textual.widget import Widget
from textual.containers import VerticalScroll
from rich.panel import Panel

class SacredWidget(Widget):
    """V3-proven pattern for Sacred Architecture"""
    
    def compose(self) -> ComposeResult:
        # Use VerticalScroll for dynamic content
        with VerticalScroll(id="content-scroll") as scroll:
            scroll.can_focus = False
            yield scroll
    
    def render(self) -> RenderableType:
        # Direct render - no child widgets
        return Panel(
            self.content,
            title=self.title,
            border_style="solid"
        )
```

### ⚡ **Streaming Patterns**

```python
# Thread-safe streaming (from Textual examples)
from textual import work
from textual.worker import get_current_worker

@work(thread=True, group="streaming")
async def stream_content(self):
    """Background streaming with UI updates"""
    async for chunk in self.stream_source:
        # Thread-safe UI update
        self.app.call_from_thread(
            self.update_widget, chunk
        )
        
        # Check for cancellation
        worker = get_current_worker()
        if worker.is_cancelled:
            break
```

### 🎨 **CSS Patterns**

```css
/* Valid Textual CSS patterns */
.widget-class {
    height: auto;              /* Dynamic sizing */
    border: solid $primary;    /* Valid border syntax */
    background: $surface;      /* Theme variable */
    padding: 1;               /* Textual units */
    margin: 1 0;              /* Spacing */
}

/* Layout patterns */
.scroll-container {
    overflow-y: auto;         /* Enable scrolling */
    max-height: 80vh;         /* Limit height */
}
```

## Development Resources

### 📖 **Essential Textual Documentation**

| Topic | Location | Description |
|-------|----------|-------------|
| **Widget Development** | `textual/docs/widgets/` | Complete widget creation guide |
| **CSS Reference** | `textual/docs/css/` | Valid properties and syntax |
| **Layout Systems** | `textual/docs/layout/` | Container and positioning |
| **Event Handling** | `textual/docs/events/` | Message system and interactions |
| **Testing Guide** | `textual/docs/testing/` | Testing patterns and utilities |
| **Performance** | `textual/docs/performance/` | Optimization best practices |

### 🔧 **Useful Textual Examples**

```python
# Key examples from textual/examples/
examples/
├── calculator.py          # Widget composition patterns
├── code_browser.py        # File tree navigation  
├── dictionary.py          # API integration and search
├── markdown_browser.py    # Content rendering
├── stopwatch.py          # Real-time updates
└── tree_view.py          # Hierarchical data display
```

### 🎯 **Sacred Architecture References**

**From Claude Code Package:**
- Terminal UI best practices
- Streaming response handling  
- Error boundary implementations
- Performance optimization patterns

**From Gemini CLI:**
- Multi-model conversation management
- Command parsing and routing
- Configuration and persistence
- User experience patterns

**From OpenCode Project:**
- Plugin architecture design
- Modular system organization
- Development workflow integration
- Code analysis patterns

## CRITICAL: How to Use Working References

### 🎯 **Development Workflow with Known Working Code**

```bash
# STEP 1: Study V3's proven chat pattern (HIGHEST PRIORITY)
cd V3/elia_chat/widgets/
cat chat.py  # Study VerticalScroll + render() pattern
grep -n "VerticalScroll\|call_from_thread\|mount" *.py

# STEP 2: Extract Claude Code reference patterns
cd reference/inspiration/
tar -xzf anthropic-ai-claude-code-1.0.44.tgz
find claude-code/ -name "*.py" | xargs grep -l "textual"

# STEP 3: Study Gemini CLI for LLM integration patterns
cd reference/inspiration/gemini-cli/
find . -name "*.py" | xargs grep -l "stream\|response\|chat"

# STEP 4: Textual framework examples (when V3 isn't enough)
cd reference/textual-docs/textual/examples/
grep -rn "VerticalScroll\|Widget\|render" .
```

### 🚫 **What NOT to Do**

```
❌ Write widgets from scratch without studying working examples
❌ Invent novel patterns when proven ones exist  
❌ Skip reference review when implementing features
❌ Reinvent scrolling, streaming, or layout patterns
❌ Create new architectures without studying successful ones
```

## Integration Guidelines

### 🔄 **Using Reference Materials**

1. **Study First**: Review reference implementations before coding
2. **Extract Patterns**: Identify proven approaches and adapt for Sacred Architecture
3. **Validate Compliance**: Ensure references align with Sacred GUI principles
4. **Document Decisions**: Record why specific patterns were chosen or adapted

### 📋 **Reference Checklist**

```
┌─ REFERENCE MATERIAL USAGE CHECKLIST ─────────────────────┐
│                                                           │
│  ☐ Studied relevant Textual documentation               │
│  ☐ Reviewed similar implementations in inspiration/      │
│  ☐ Validated patterns against Sacred Architecture        │
│  ☐ Tested pattern compatibility with V3 approach        │
│  ☐ Documented pattern selection rationale               │
│  ☐ Updated Sacred Architecture docs if needed            │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

## Cross-References

- **Architecture**: See `../architecture/` for Sacred GUI specifications
- **Implementation**: See `../implementation/` for development guides  
- **Testing**: See `../testing/` for validation approaches
- **Design**: See `../design/` for styling guidelines
- **Ledgers**: See `../ledgers/` for feature tracking