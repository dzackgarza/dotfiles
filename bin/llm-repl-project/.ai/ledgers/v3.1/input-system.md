# Sacred GUI Input System

**Branch:** feat/sacred-input-system
**Summary:** Implement the PromptInput component as the bottom area of the Sacred GUI architecture, with file context inclusion (@-commands) and proper integration with the three-area layout.
**Status:** Planning
**Created:** 2025-07-10
**Updated:** 2025-07-12

## Context

### Problem Statement
The input system must be implemented as the bottom area of the Sacred GUI layout, maintaining the immutable three-area architecture. The PromptInput component needs @-command support for file inclusion while respecting the canonical layout constraints.

### Success Criteria
- [ ] PromptInput positioned as bottom area in Sacred GUI layout
- [ ] File context inclusion via @-commands functional
- [ ] Input properly integrated with Sacred Timeline and Live Workspace
- [ ] No layout violations or nested container issues
- [ ] Maintains focus management across three areas

### User-Visible Behaviors
When this ledger is complete, the user will see:

1. **PromptInput as fixed bottom area in Sacred GUI layout**
2. **@-command file inclusion working with autocomplete**
3. **Proper focus transitions between Sacred Timeline, Live Workspace, and Input**
4. **Input area maintains consistent height regardless of workspace state**
5. **File context appears in appropriate area (Sacred Timeline or Live Workspace)**

## Technical Approach

### Architecture Changes
1. **SacredPromptInput**: Enhanced PromptInput for Sacred GUI architecture
2. **FileContextProcessor**: Handles @-command parsing and file inclusion
3. **LayoutFocusManager**: Manages focus across three areas
4. **ContextDisplayManager**: Routes file context to appropriate display area
