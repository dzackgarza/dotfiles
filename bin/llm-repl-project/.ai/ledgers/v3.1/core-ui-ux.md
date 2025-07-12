# Sacred GUI Three-Area Layout Implementation

**Branch:** feat/sacred-gui-layout
**Summary:** Implement the canonical Sacred GUI architecture with three distinct areas following the immutable design defined in CLAUDE.md. This establishes the foundation for all future UI development.
**Status:** Planning
**Created:** 2025-07-10
**Updated:** 2025-07-12

## Context

### Problem Statement
The current UI architecture does not follow the canonical Sacred GUI design or industry best practices for Textual chat applications. We need to implement the immutable three-area layout: Sacred Timeline (top), Live Workspace (middle), and PromptInput (bottom). This architecture is non-negotiable and must implement both the specified design AND proven industry standards for streaming, dynamic content management, and error surfacing.

### Success Criteria
- [ ] Three-area layout matches CLAUDE.md canonical design exactly
- [ ] Sacred Timeline uses VerticalScroll with simple blocks + hrules (V3 pattern)
- [ ] Live Workspace shows/hides dynamically based on cognition state
- [ ] No nested container violations (simple widgets only)
- [ ] V3's proven scroll architecture replicated in both areas
- [ ] Industry-standard error surfacing with fail-fast validation
- [ ] Thread-safe streaming updates using `call_from_thread()`
- [ ] Smart auto-scroll behavior (only when user is at bottom)
- [ ] Content-driven dynamic resizing with `height: auto`

### User-Visible Behaviors
When this ledger is complete, the user will see:

1. **Three distinct areas: Sacred Timeline (top), Live Workspace (middle), Input (bottom)**
2. **Sacred Timeline displays completed conversation history with turn separators**
3. **Live Workspace appears/disappears based on processing state**
4. **2-way split layout when workspace is hidden (Sacred Timeline + Input only)**
5. **3-way split layout when workspace is visible (all three areas)**
6. **Smooth, responsive scrolling in both Sacred Timeline and Live Workspace**
7. **Content automatically resizes to fit container without layout conflicts**
8. **Error messages appear immediately when validation fails**
9. **Streaming content updates in real-time without blocking the UI**
10. **Auto-scroll only occurs when user is viewing the bottom of content**

## Sacred GUI Layout Specification

### Canonical Layout (from CLAUDE.md)
```
┌─────────────────────────┐
│ VerticalScroll (SACRED) │ ← Sacred Timeline
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
│ VerticalScroll (LIVE)   │ ← Live Cognition Workspace  
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

### Immutable Architecture Rules
1. **Sacred Timeline (Top)**: VerticalScroll with simple blocks + hrules between turns
2. **Live Workspace (Middle)**: VerticalScroll with streaming sub-modules + final assistant response  
3. **Input (Bottom)**: PromptInput for user queries
4. **No nested containers**: Each scroll area contains only simple widgets - NO Vertical-in-Vertical
5. **Turn completion**: Live workspace contents → Sacred Timeline as blocks, workspace clears
6. **Visual separation**: hrules mark turn boundaries in Sacred Timeline  
7. **Unlimited scaling**: Live workspace can handle N sub-modules via scrolling
8. **Assistant response**: Always final sub-module in live workspace
9. **Workspace visibility**: Live workspace DISAPPEARS/COLLAPSES between turns (2-way split when idle)

### Industry Best Practices Integration

Following proven Textual chat application patterns:

**Layered Architecture Enforcement:**
- **Presentation Layer**: `SacredTimelineWidget`, `LiveWorkspaceWidget`, `SimpleBlockWidget` with clear boundaries
- **Application Logic Layer**: `UnifiedAsyncProcessor` with streaming and error handling
- **Data Access Layer**: `ResponseGenerator` and API client abstractions
- **Strict Separation**: Clear interface contracts and validation at all boundaries

**Dynamic Content Management:**
- **VerticalScroll Containers**: Both areas use V3's proven scroll pattern  
- **Reactive Attributes**: Automatic UI updates when content changes
- **Content-Driven Heights**: `height: auto` CSS - no hardcoded dimensions
- **Smart Auto-Scroll**: Only scroll when user is at bottom (prevents interruption)
- **Thread-Safe Updates**: Use `call_from_thread()` for worker thread UI updates

**Error Surfacing & Diagnostics:**
- **Fail-Fast Validation**: All widget boundaries assert types and values immediately
- **Error Boundaries**: Major UI sections catch/display errors without crashes
- **Central Error Handler**: Development mode displays error banners immediately
- **State Auditing**: Integrity checks after key events with logging