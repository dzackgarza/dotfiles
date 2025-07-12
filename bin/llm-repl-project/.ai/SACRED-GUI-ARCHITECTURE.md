# SACRED GUI ARCHITECTURE - CANONICAL LAYOUT

**STATUS**: IMMUTABLE - DO NOT MODIFY THIS DESIGN

This document enshrines the canonical GUI architecture for the LLM REPL V3-minimal project. This design is the result of extensive debugging of layout conflicts and MUST be adhered to.

## THE CANONICAL LAYOUT STATES

### IDLE STATE (2-way split - LIKE V3)
```
┌─────────────────────────┐
│ VerticalScroll (SACRED) │ ← Sacred Timeline (V3's chat pattern)
│ ├── System Block       │
│ ├─────────────────────  │ ← hrule
│ ├── User Block         │ ← Turn 1 
│ ├── Cognition Block    │
│ ├── Assistant Block    │
│ ├─────────────────────  │ ← hrule
│ ├── User Block         │ ← Turn 2
│ ├── Cognition Block    │
│ ├── Assistant Block    │
│ └── [scrolls...]       │
├─────────────────────────┤
│ PromptInput             │
└─────────────────────────┘
```

### ACTIVE STATE (3-way split - during cognition)
```
┌─────────────────────────┐
│ VerticalScroll (SACRED) │ ← Sacred Timeline (V3's chat pattern)
│ ├── System Block       │
│ ├─────────────────────  │ ← hrule
│ ├── User Block         │ ← Turn 1 
│ ├── Cognition Block    │
│ ├── Assistant Block    │
│ ├─────────────────────  │ ← hrule
│ ├── User Block         │ ← Turn 2
│ ├── Cognition Block    │
│ ├── Assistant Block    │
│ ├─────────────────────  │ ← hrule  
│ ├── User Block         │ ← Turn 3 (current)
│ └── [scrolls...]       │
├─────────────────────────┤
│ VerticalScroll (LIVE)   │ ← Live Workspace (V3's scroll pattern) 
│ ├── Route Query        │ ← sub-module 1
│ ├── Call Tool          │ ← sub-module 2
│ ├── Format Output      │ ← sub-module 3
│ ├── ...                │ ← sub-modules 4 through N
│ ├── Sub-module N       │ ← final cognition sub-module
│ └── Assistant Response │ ← always last (streaming)
├─────────────────────────┤
│ PromptInput             │
└─────────────────────────┘
```

## IMMUTABLE ARCHITECTURE RULES

### 1. Sacred Timeline (Top Section)
- **Type**: `VerticalScroll` container
- **Contents**: Simple block widgets + hrule separators
- **Purpose**: Immutable conversation history
- **Scrolling**: Natural scrolling when content exceeds height
- **Turn separation**: hrules between User→Cognition→Assistant groups

### 2. Live Workspace (Middle Section)  
- **Type**: `VerticalScroll` container
- **Contents**: Sub-module widgets + final assistant response
- **Purpose**: Real-time cognition process visualization
- **Scrolling**: Can handle unlimited sub-modules (N)
- **Assistant response**: Always appears as final sub-module

### 3. Input Area (Bottom Section)
- **Type**: `PromptInput` widget
- **Purpose**: User input capture
- **Behavior**: Fixed height, multiline support

## CRITICAL DESIGN PRINCIPLES

### NO Nested Containers
- **FORBIDDEN**: `Vertical` inside `VerticalScroll`
- **FORBIDDEN**: Container widgets with child containers
- **REQUIRED**: Only simple widgets as direct children

### Clean Separation of Concerns
- **Sacred Timeline**: History only, no live updates
- **Live Workspace**: Current turn only, cleared after completion
- **No interference**: Each section manages its own layout independently

### Turn Lifecycle
1. **Idle state**: 2-way split (Sacred Timeline + PromptInput) - Live workspace HIDDEN
2. **User input**: Added to Sacred Timeline, Live workspace APPEARS (3-way split)
3. **Cognition starts**: Live workspace shows sub-modules streaming
4. **Assistant response**: Appears as final sub-module in live workspace
5. **Turn completion**: Cognition + Assistant moved to Sacred Timeline
6. **Workspace cleared**: Live workspace DISAPPEARS/COLLAPSES back to 2-way split

## WHY THIS ARCHITECTURE WORKS

### Based on V3's PROVEN Success
- **V3 GUI works perfectly** - we know this from actual usage
- Sacred Timeline copies V3's exact `VerticalScroll + Chatbox` pattern
- Live workspace uses V3's identical scroll architecture
- **No reinventing** - we use what we KNOW works

### Solves Layout Conflicts
- Each scroll area has simple, flat widget hierarchy (like V3)
- No nested containers fighting for height allocation
- Clean separation prevents interference between areas
- **V3 never had these problems** - we follow its proven pattern

### Unlimited Scalability
- Sacred Timeline: Unlimited conversation history
- Live workspace: Unlimited sub-modules per turn
- Both scale via natural scrolling

## IMPLEMENTATION REQUIREMENTS

### File Structure
```
src/main.py                    # Implements 3-way split layout
src/widgets/sacred_timeline.py # Top section implementation
src/widgets/live_workspace.py  # Middle section implementation  
src/widgets/prompt_input.py    # Bottom section implementation
```

### CSS Requirements
- Each scroll area: `height: auto` widgets only
- No flex height distribution between sibling widgets
- hrules: Simple separator widgets, no container properties

### Event Flow
1. **Idle**: 2-way layout (Sacred Timeline + PromptInput)
2. **User input**: Sacred Timeline + Live workspace activation (3-way layout)
3. **Sub-module events**: Live workspace updates
4. **Turn completion**: Sacred Timeline + Live workspace collapse to 2-way layout

## FORBIDDEN PATTERNS

### ❌ Nested Scroll Containers
```python
# FORBIDDEN
VerticalScroll(
    children=[
        Vertical(  # ← This creates layout conflicts
            children=[...]
        )
    ]
)
```

### ❌ Mixed Live/Historical Content
```python
# FORBIDDEN - mixing live and historical in same container
Sacred Timeline + Live blocks in same scroll area
```

### ❌ Complex Widget Hierarchies
```python
# FORBIDDEN - deep nesting
UnifiedBlockWidget(Vertical(
    children=[
        HeaderWidget(Horizontal(...)),  # ← Too deep
        ContentWidget(Vertical(...))    # ← Too deep  
    ]
))
```

## REQUIRED PATTERNS

### ✅ V3's Proven Pattern
```python
# REQUIRED - Copy V3's exact structure
VerticalScroll(
    children=[
        SimpleBlockWidget(),  # ← Like V3's Chatbox
        HRuleWidget(),       # ← Simple separator
        SimpleBlockWidget()  # ← Like V3's Chatbox
    ]
)
```

### ✅ V3's Clean Separation
```python
# REQUIRED - V3's container pattern
sacred_timeline = VerticalScroll()  # V3's chat_container pattern
live_workspace = VerticalScroll()   # Same V3 scroll pattern
```

## ENFORCEMENT

This architecture is **IMMUTABLE**. Any changes require:
1. Documentation of why the current design fails
2. Proposal for alternative that maintains separation of concerns
3. Proof that alternative solves layout conflicts
4. Update to this canonical document

**No exceptions. This design is the result of extensive debugging and MUST be preserved.**