# Textual Migration Architecture Ledger

**Scope:** Port V2-tkinter-rewrite to V3-textual for Sway aesthetic integration  
**Target:** Terminal-native LLM REPL with authentic terminal feel  
**Aesthetic Goal:** Seamless integration with Arch + Sway tiled terminal setup

## Architecture Mapping: Tkinter → Textual

### Application Structure
```
V2-tkinter-rewrite/          →  V3/
├── main.py                  →  main.py (Textual App)
├── config/                  →  config/ (unchanged)
├── core/                    →  core/ (unchanged - business logic)
│   ├── blocks.py           →  blocks.py (preserve block system)
│   ├── cognition.py        →  cognition.py (preserve processing)
│   └── timeline.py         →  timeline.py (preserve timeline)
└── ui/                     →  widgets/
    ├── main_window.py      →  app.py (Textual App class)
    ├── timeline_view.py    →  timeline_widget.py (Rich renderable)
    ├── input_panel.py      →  input_widget.py (Textual Input)
    └── styles.py           →  theme.py (Textual CSS)
```

### Core Architecture Principles

#### Preserve V2-tkinter-rewrite Strengths
- **Clean component separation**: UI ↔ Business Logic
- **Working block system**: TimelineBlock, BlockType enums
- **Solid cognition pipeline**: CognitionProcessor with transparency
- **Comprehensive testing**: 311-line test suite
- **Configuration system**: Multi-environment configs

#### Textual-Specific Adaptations
- **App as Container**: Textual App replaces Tkinter root window
- **Widgets as Components**: Textual widgets replace Tkinter widgets
- **Rich Renderables**: Timeline blocks become Rich renderables
- **CSS Styling**: Textual CSS replaces manual styling
- **Reactive Updates**: Textual reactive system for state changes

## Component Architecture

### 1. Main Application (App.py)
```python
class LLMReplApp(App):
    """Main Textual application - replaces MainWindow"""
    
    # Bindings for Sway-compatible keyboard shortcuts
    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
        ("ctrl+l", "clear_timeline", "Clear"),
        ("ctrl+s", "save_timeline", "Save"),
        ("escape", "cancel_processing", "Cancel"),
    ]
    
    # CSS styling for terminal aesthetic
    CSS_PATH = "theme.tcss"
```

### 2. Timeline Widget (timeline_widget.py)
```python
class TimelineWidget(Static):
    """Timeline display - replaces timeline_view.py"""
    
    def __init__(self):
        super().__init__()
        self.timeline_manager = TimelineManager()
    
    def render(self) -> RenderableType:
        """Render timeline as Rich console output"""
        return self._render_blocks()
```

### 3. Input Widget (input_widget.py)
```python
class InputWidget(Vertical):
    """Input panel - replaces input_panel.py"""
    
    def compose(self) -> ComposeResult:
        yield Input(placeholder="Enter your message...")
        yield Button("Send", id="send-btn")
```

### 4. Theme System (theme.py + theme.tcss)
- **Python Theme**: Color schemes, font definitions
- **Textual CSS**: Widget styling, layout, spacing
- **Terminal Integration**: Respect terminal color schemes

## Data Flow Architecture

### Input Processing Pipeline
```
User Input → InputWidget → LLMReplApp → CognitionProcessor → TimelineManager → TimelineWidget
```

### Block Rendering Pipeline  
```
TimelineBlock → Rich Renderable → TimelineWidget → Terminal Display
```

### State Management
- **Reactive Properties**: Textual reactive system for UI updates
- **Message Passing**: Textual message system for component communication
- **Event Handling**: Textual event system for user interactions

## Integration Points

### Core Module Preservation
- **blocks.py**: Keep TimelineBlock, BlockType, factory functions
- **timeline.py**: Keep TimelineManager, block management logic  
- **cognition.py**: Keep CognitionProcessor, cognitive steps
- **settings.py**: Keep configuration system

### UI Module Transformation
- **main_window.py** → **app.py**: Tkinter App → Textual App
- **timeline_view.py** → **timeline_widget.py**: Tkinter ScrolledText → Textual Static
- **input_panel.py** → **input_widget.py**: Tkinter Text → Textual Input
- **styles.py** → **theme.py + theme.tcss**: Manual styling → Textual CSS

## Technical Requirements

### Dependencies
```python
# New dependencies for V3
textual>=0.50.0      # Main TUI framework
rich>=13.0.0         # Text rendering (included with textual)

# Preserved dependencies from V2-tkinter-rewrite
asyncio              # For cognition processing
pathlib              # For config management
argparse             # For CLI interface
```

### File Structure
```
V3/
├── main.py                 # Application entry point
├── app.py                  # Main Textual App class
├── widgets/                # Textual widgets
│   ├── __init__.py
│   ├── timeline_widget.py  # Timeline display
│   ├── input_widget.py     # Input handling
│   └── status_widget.py    # Status bar
├── theme/                  # Styling and themes
│   ├── __init__.py
│   ├── theme.py           # Python theme definitions
│   └── theme.tcss         # Textual CSS
├── core/                   # Business logic (preserved)
│   ├── __init__.py
│   ├── blocks.py
│   ├── timeline.py
│   └── cognition.py
├── config/                 # Configuration (preserved)
│   ├── __init__.py
│   └── settings.py
└── tests/                  # Test suite
    ├── __init__.py
    ├── test_widgets.py     # Widget testing
    └── test_integration.py # Integration testing
```

## Migration Strategy

### Phase 1: Foundation (1-2 days)
1. Create basic Textual App structure
2. Port configuration system
3. Create minimal timeline widget
4. Create basic input widget

### Phase 2: Core Integration (2-3 days)
1. Integrate timeline manager
2. Port cognition processor
3. Implement block rendering
4. Add keyboard shortcuts

### Phase 3: Styling & Polish (1-2 days)
1. Create terminal-aesthetic theme
2. Implement responsive layout
3. Add status indicators
4. Polish keyboard navigation

### Phase 4: Testing & Validation (1 day)
1. Port existing tests
2. Add Textual-specific tests
3. Validate Sway integration
4. Performance testing

## Success Metrics

### Functional Requirements
- ✅ All V2-tkinter-rewrite functionality preserved
- ✅ Timeline blocks render correctly
- ✅ Cognition processing works identically
- ✅ Configuration system maintained
- ✅ Test suite passes

### Aesthetic Requirements  
- ✅ Looks like native terminal application
- ✅ Integrates seamlessly with Sway tiling
- ✅ Input feels like terminal input
- ✅ Respects terminal transparency/themes
- ✅ Matches dmenu/rofi aesthetic language

### Technical Requirements
- ✅ No Xwayland dependency issues
- ✅ Proper gap behavior in Sway
- ✅ Terminal transparency support
- ✅ Keyboard-driven navigation
- ✅ Fast startup and responsiveness