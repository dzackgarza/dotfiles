# Implementation Guides

> **CRITICAL: Copy Working Patterns**: Always start by studying and copying patterns from V3, Gemini CLI, or Claude Code. Adapt proven implementations rather than building from scratch.

This directory contains practical implementation guides, migration strategies, and technical development resources.

## Files Overview

```
implementation/
├── README.md                           # This overview
├── textual-implementation-phases.md    # Phased development approach
├── textual-migration-architecture.md   # Migration architecture considerations
├── elia-integration-plan.md           # Elia framework integration
├── textual-component-mapping.md       # Widget mapping strategies
├── patterns.md                        # Code patterns and philosophy
├── ollama-setup.md                    # Local LLM setup guide
└── widget-development-guide.md        # [Generated] Step-by-step widget creation
```

## Implementation Phases

### 📋 **Phase 1: Foundation Setup**
```
┌─ Foundation Requirements ─────────────────────────────────┐
│ ☐ Sacred GUI three-area layout (main.py)                 │
│ ☐ VerticalScroll containers for Timeline + Workspace     │
│ ☐ PromptInput widget with validation                     │
│ ☐ Basic CSS styling with valid Textual properties        │
│ ☐ Error boundary implementation                          │
└───────────────────────────────────────────────────────────┘
```

### 🏗️ **Phase 2: Core Widgets**
```
┌─ Widget Development Order ───────────────────────────────┐
│ 1. SimpleBlockWidget (V3 Chatbox pattern)               │
│ 2. SacredTimelineWidget (VerticalScroll + blocks)       │
│ 3. LiveWorkspaceWidget (VerticalScroll + sub-modules)   │
│ 4. SubModuleWidget (streaming cognition steps)          │
│ 5. ErrorBoundaryWidget (graceful error handling)        │
└───────────────────────────────────────────────────────────┘
```

### ⚡ **Phase 3: Dynamic Features**
```
┌─ Advanced Functionality ─────────────────────────────────┐
│ ☐ Thread-safe streaming with call_from_thread()         │
│ ☐ Smart auto-scroll behavior                            │
│ ☐ Workspace show/hide transitions (2-way ↔ 3-way)      │
│ ☐ Content-driven dynamic resizing                       │
│ ☐ Real-time progress indicators                         │
└───────────────────────────────────────────────────────────┘
```

## CRITICAL: Start With Working Code

### 🏆 **Development Workflow (Required Order)**

```
1. 📚 STUDY V3 FIRST    → V3/elia_chat/widgets/chat.py
2. 📋 COPY PATTERN      → Take working VerticalScroll + render()
3. 🔧 ADAPT FOR SACRED  → Modify for our three-area layout
4. ✅ TEST AGAINST V3   → Ensure it works like reference
5. 📝 DOCUMENT CHANGES  → Record what was adapted and why
```

### 1. Widget Development Pattern (Based on V3)
```python
# Sacred Architecture Widget Template (COPIED FROM V3 PATTERN)
class ExampleWidget(Widget):
    """
    Sacred Architecture Widget Template
    
    COPIED FROM V3's proven pattern:
    - render() method (no child widgets) ← V3/elia_chat/widgets/chatbox.py
    - Input validation in __init__ ← Standard V3 practice
    - Content-driven sizing ← V3 chat container pattern
    - Error boundary compatible ← V3 error handling
    """
    
    def __init__(self, data):
        super().__init__()
        self.data = self._validate_data(data)  # V3 pattern
    
    def render(self) -> RenderableType:
        # DIRECT COPY of V3 pattern: render(), no children
        return Panel(
            self._build_content(),
            title=self._get_title(),
            border_style=self._get_border_style()
        )
    
    def _validate_data(self, data):
        # Fail-fast validation (V3 pattern)
        if not hasattr(data, 'required_field'):
            raise ValueError(f"Invalid data: {data}")
        return data
```

### 2. Thread-Safe Update Pattern (COPIED FROM V3)
```python
# DIRECT COPY from V3/elia_chat/widgets/chat.py:194
@work(thread=True, group="streaming")
async def stream_content(self):
    async for chunk in stream_source:
        # V3's proven thread-safe UI update pattern
        self.app.call_from_thread(
            self.update_content, chunk  # V3: self.chat_container.mount
        )
```

### 3. Error Boundary Usage (Adapted from Working Examples)
```python
# Adapted from Textual examples + Claude Code patterns
def create_safe_widget(widget_class, *args, **kwargs):
    try:
        widget = widget_class(*args, **kwargs)
        return ErrorBoundaryWidget(widget)  # Pattern from textual/examples/
    except Exception as e:
        return ErrorDisplayWidget(e)  # Graceful fallback
```

## File Descriptions

### 📝 **Core Implementation Guides**

**`textual-implementation-phases.md`**
- Detailed phased development approach
- Milestone definitions and success criteria
- Dependencies between implementation phases

**`textual-migration-architecture.md`**  
- Architecture considerations for migrating to Sacred GUI
- Compatibility requirements and migration strategies
- V3 pattern integration guidelines

**`elia-integration-plan.md`**
- Integration strategy with Elia framework
- API compatibility and shared component usage
- Migration path from existing implementations

### 🛠️ **Technical Resources**

**`textual-component-mapping.md`**
- Mapping of Sacred Architecture components to Textual widgets
- Widget selection criteria and implementation patterns
- Performance considerations for different widget types

**`patterns.md`** 
- Code patterns and development philosophy
- Sacred Architecture-specific coding standards
- V3 pattern compliance guidelines

**`ollama-setup.md`**
- Local LLM setup and configuration
- Model selection and performance optimization
- Development environment configuration

## Development Workflow

```
┌─ Sacred Architecture Development Workflow ───────────────┐
│                                                           │
│  1. Read GUI-VISION.md     → Visual understanding        │
│  2. Check patterns.md      → Coding standards            │
│  3. Follow phase guide     → Structured development      │
│  4. Validate with tests    → See ../testing/             │
│  5. Style with design      → See ../design/              │
│  6. Document changes       → Update relevant files       │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

## Cross-References

- **Architecture**: See `../architecture/` for design specifications
- **Testing**: See `../testing/` for validation strategies  
- **Design**: See `../design/` for styling guidelines
- **Reference**: See `../reference/` for external documentation
- **Ledgers**: See `../ledgers/` for feature tracking