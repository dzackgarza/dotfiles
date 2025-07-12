# CLAUDE-CONTINUE.md

## Critical Architectural Pivot (V3.15 → Sacred GUI)

### Previous State Analysis
The original V3.15 plan attempted to fix dual-system conflicts with above/below fold architecture:
- Above-fold: Sacred Timeline (immutable history)
- Below-fold: TransientBlock (active processing)
- Single Timeline ownership

### New Sacred GUI Direction (2025-07-12)
**CLAUDE.md now defines the immutable Sacred GUI architecture that supersedes V3.15:**

```
┌─────────────────────────┐
│ VerticalScroll (SACRED) │ ← Sacred Timeline (top)
├─────────────────────────┤
│ VerticalScroll (LIVE)   │ ← Live Workspace (middle) 
├─────────────────────────┤
│ PromptInput             │ ← Input (bottom)
└─────────────────────────┘
```

**This is the canonical architecture. All implementation must follow this exactly.**

### Why Sacred GUI Is Better Than V3.15
1. **Clear Three-Area Separation**: No more above/below fold confusion
2. **Proven V3 Architecture**: Both scroll areas use V3's working VerticalScroll pattern
3. **Dynamic Workspace**: Live area shows/hides (2-way ↔ 3-way split)
4. **No Nested Containers**: Simple widgets only in each scroll area
5. **Sacred Turn Structure**: User → Cognition → Assistant rhythm preserved

## Sacred GUI Implementation Strategy

### Current Implementation Status (2025-07-12)
The main application (`src/main.py`) already implements Sacred GUI basics:
- ✅ Three-area layout: `SacredTimelineWidget` + `LiveWorkspaceWidget` + `PromptInput`
- ✅ Dynamic workspace show/hide logic (`show_workspace()` / `hide_workspace()`)
- ✅ Sacred routing in `on_prompt_input_prompt_submitted()`
- ✅ 2-way ↔ 3-way split behavior

### Critical Implementation Gaps - V3 Proven Patterns

#### 1. Widget Implementation - Following V3's VerticalScroll Pattern
**SacredTimelineWidget**: Needs V3's `VerticalScroll` + mounting pattern
```python
# V3 Pattern: chat.py:95-97, 107-108, 143
with VerticalScroll(id="chat-container") as vertical_scroll:
    vertical_scroll.can_focus = False

@property
def chat_container(self) -> VerticalScroll:
    return self.query_one("#chat-container", VerticalScroll)

# Dynamic mounting: chat.py:143, 205, 337
await self.chat_container.mount(user_message_chatbox)
await self.chat_container.mount_all(chatboxes)
```

**LiveWorkspaceWidget**: Needs V3's streaming + thread-safe updates
```python
# V3 Pattern: chat.py:205, 219-230
self.app.call_from_thread(self.chat_container.mount, response_chatbox)
self.app.call_from_thread(response_chatbox.append_chunk, chunk_content)

# Auto-scroll pattern: chat.py:225-230
scroll_y = self.chat_container.scroll_y
max_scroll_y = self.chat_container.max_scroll_y
if scroll_y in range(max_scroll_y - 3, max_scroll_y + 1):
    self.app.call_from_thread(self.chat_container.scroll_end, animate=False)
```

#### 2. Turn Completion Logic - V3's Message System
**Cross-Widget Communication**: V3's message pattern (chat.py:71-90)
```python
@dataclass
class AgentResponseComplete(Message):
    chat_id: int | None
    message: ChatMessage
    chatbox: Chatbox

# Event handling: chat.py:264-272
@on(AgentResponseComplete)
def agent_finished_responding(self, event: AgentResponseComplete):
    self.chat_data.messages.append(event.message)
    event.chatbox.border_title = "Agent"
```

#### 3. Cognition Sub-Module Display - V3's Streaming Implementation
**Thread-Safe Streaming**: V3's worker pattern (chat.py:156-249)
```python
@work(thread=True, group="agent_response")
async def stream_agent_response(self):
    # LLM processing in background thread
    response_chatbox = Chatbox(message, model, classes="response-in-progress")
    self.app.call_from_thread(self.chat_container.mount, response_chatbox)
    
    # Stream updates
    async for chunk in response:
        self.app.call_from_thread(response_chatbox.append_chunk, chunk_content)
```

#### 4. hrule Separators & Workspace Collapse
- Use V3's widget mounting for separator elements
- Apply V3's CSS class-based state management for animations

### Architecture Principles (From CLAUDE.md)
1. **Sacred Timeline (Top)**: VerticalScroll with simple blocks + hrules between turns
2. **Live Workspace (Middle)**: VerticalScroll with streaming sub-modules + final assistant response  
3. **Input (Bottom)**: PromptInput for user queries
4. **No nested containers**: Each scroll area contains only simple widgets
5. **Turn completion**: Live workspace contents → Sacred Timeline as blocks, workspace clears
6. **Workspace visibility**: Disappears/collapses between turns (2-way split when idle)

### Implementation Plan (Sacred GUI v3.1 Ledgers)

**Updated ledgers in `.ai/ledgers/v3.1/` now reflect Sacred GUI architecture:**

1. **Sacred GUI Architecture Implementation** (`live-inscribed-block-system.md`)
   - Three-area layout foundation
   - Workspace show/hide logic
   - Turn completion transfers

2. **Live Workspace Cognition Pipeline** (`mock-cognition-pipeline.md`)
   - Sequential sub-module streaming
   - Route Query → Call Tool → Format Output → Assistant Response
   - Live Workspace content management

3. **Sacred GUI Three-Area Layout** (`core-ui-ux.md`)
   - Canonical layout implementation
   - 2-way/3-way split behavior
   - V3 proven scroll architecture

4. **Sacred Timeline Implementation** (`timeline.md`)
   - Top area historical record
   - hrule turn separators
   - Append-only integrity

5. **Sacred GUI Input System** (`input-system.md`)
   - Bottom area PromptInput
   - @-command file inclusion
   - Focus management across areas

### Why Sacred GUI Fixes Everything

Sacred GUI eliminates architectural conflicts through clear spatial separation:
- **No Dual Systems**: Single UnifiedTimeline manages both areas
- **Clear Ownership**: Sacred Timeline owns history, Live Workspace owns active processing
- **Spatial Clarity**: Three distinct areas prevent rendering conflicts
- **Proven Architecture**: Uses V3's working VerticalScroll pattern for both scroll areas
- **Dynamic Behavior**: Workspace show/hide provides natural processing state indication

### Next Steps (Priority Order) - Using V3 Proven Patterns

1. **Implement Missing Widgets** (`SacredTimelineWidget`, `LiveWorkspaceWidget`)
   - Use V3's `VerticalScroll` + `chat_container` pattern from `chat.py:95-108`
   - Apply V3's dynamic mounting pattern from `chat.py:143, 205, 337`
   - Implement V3's thread-safe updates using `call_from_thread()`

2. **Add Turn Completion Logic** (Live → Sacred transfer mechanism)
   - Use V3's message system pattern from `chat.py:71-90` for cross-widget communication
   - Apply V3's event handling pattern from `chat.py:264-272`
   - Implement batch transfer using V3's `mount_all()` pattern

3. **Implement Cognition Streaming** (Sequential sub-modules in Live Workspace)
   - Use V3's streaming pattern: `@work(thread=True)` + `call_from_thread()`
   - Apply V3's auto-scroll logic from `chat.py:225-230`
   - Use V3's dynamic border titles for progress indication

4. **Add hrule Separators** (Turn boundaries in Sacred Timeline)
   - Use V3's widget mounting pattern for separator elements
   - Apply V3's CSS styling approach for visual boundaries

5. **Refine Workspace Animations** (Show/hide transitions)
   - Use V3's CSS class-based state management
   - Apply V3's animation patterns for smooth transitions

### Key Principles (Updated)

> **"Sacred GUI has three immutable areas: Sacred Timeline (history), Live Workspace (active processing), and PromptInput (user interface). Each area has a single, clear purpose with no overlap or confusion."**

### Current Implementation Status

The application architecture in `src/main.py` already demonstrates Sacred GUI understanding:
- Three-area layout structure ✅
- Workspace show/hide calls ✅ 
- Sacred routing logic ✅
- Error handling with Sacred Timeline ✅

### V3 Proven Patterns for Implementation

**Key V3 Files for Reference:**
- `/V3/elia_chat/widgets/chat.py` - Master pattern for VerticalScroll + dynamic mounting
- `/V3/elia_chat/app.py` - App-level organization and screen management
- `/V3/elia_chat/screens/chat_screen.py` - Screen composition patterns

**V3's Architecture Success Factors:**
1. **Simple VerticalScroll**: No nested containers, just `mount()` widgets directly
2. **Thread-Safe Updates**: `call_from_thread()` for UI updates from worker threads
3. **Smart Auto-Scroll**: Only scroll when user is at bottom (prevents interruption)
4. **Message System**: `@dataclass` messages + `@on()` handlers for cross-widget communication
5. **Focus Management**: Clear patterns for moving focus between input and content areas

**Next**: Implement `SacredTimelineWidget` and `LiveWorkspaceWidget` using these exact V3 patterns.

## Industry Best Practices Integration

**Textual Chat App Design Standards Applied:**
Following the comprehensive industry report for Textual chat applications, the Sacred GUI implementation incorporates:

### Layered Architecture Enforcement
- **Presentation Layer**: `SacredTimelineWidget`, `LiveWorkspaceWidget`, `SimpleBlockWidget` 
- **Application Logic Layer**: `UnifiedAsyncProcessor` with streaming and error handling
- **Data Access Layer**: `ResponseGenerator` and API client abstractions
- **Strict Separation**: Clear interface contracts and validation at all boundaries

### Dynamic Content Management (V3 + Industry Standards)
- **VerticalScroll Containers**: Both Sacred and Live areas use V3's proven scroll pattern
- **Reactive Attributes**: Automatic UI updates when content changes
- **Content-Driven Heights**: `height: auto` CSS - no hardcoded dimensions
- **Smart Auto-Scroll**: V3's pattern - only scroll when user is at bottom
- **Loading States**: Streaming indicators and smooth live-to-inscribed transitions

### Error Surfacing & Diagnostics Implementation
- **Fail-Fast Validation**: All widget boundaries assert types and values
- **Error Boundaries**: Major UI sections catch/display errors without crashes
- **Central Error Handler**: Development mode displays error banners immediately
- **State Auditing**: Integrity checks after block creation, streaming, inscription
- **Action Logging**: All mutations logged with context for debugging

### Widget Test Strategy
- **Streaming Simulation**: Test harnesses for live content updates and scroll behavior
- **Resizing Tests**: Validate widgets handle content size changes gracefully
- **Error Scenario Testing**: Ensure error handling doesn't crash the app
- **Layout Conflict Detection**: Verify no nested container issues

The Sacred GUI architecture now represents both V3's proven patterns AND industry-standard practices for robust, maintainable Textual chat applications.

## Migration Notes

Current approach maintains backward compatibility:
- `UnifiedTimeline` continues managing block lifecycle
- Sacred GUI adds spatial organization without breaking existing logic
- Progressive enhancement: implement widgets → add features → refine behavior
- All existing tests continue working with Sacred GUI implementation

The result is a predictable, user-friendly interface that matches mental models of conversation flow.