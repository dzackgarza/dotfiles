# Architecture

## CRITICAL: Build From Known Working Code

> **Fundamental Principle**: It is MUCH better to work from a KNOWN working implementation, like V3 or the inspiration repositories, and build off of that, than to reinvent something. Always research how successful projects solve similar problems first.

**Key Working References:**
- **V3 Chat Implementation**: `reference/inspiration/V3/elia_chat/widgets/chat.py` - Proven VerticalScroll + render() pattern
- **Gemini CLI**: `reference/inspiration/gemini-cli/` - Working LLM terminal interface
- **Claude Code**: `reference/inspiration/anthropic-ai-claude-code/` - Production TUI patterns
- **Textual Examples**: `reference/textual-docs/textual/examples/` - Framework best practices

## Guiding Philosophies

This project is built on foundational principles that align with industry best practices for Textual chat applications:

1.  **The Timeline is Sacred**: The central data structure is a persistent, append-only timeline of "blocks." Each block represents a discrete unit of work (user input, AI cognition, tool output, etc.). Once inscribed, a block is an immutable part of the application's history, used for context in all future operations. It is the absolute source of truth.

2.  **The UI Reflects the Architecture**: The application's output MUST be a direct reflection of its internal architecture. The user's mental model of the visual timeline of blocks dictates the system's design. Each block corresponds to a self-contained, independently testable plugin. There is no hidden magic.

3.  **Textual Chat App Design Standards**: Following industry best practices for dynamic, streaming chat interfaces:
    - **Layered Architecture**: Clear separation between Presentation (Textual widgets), Application Logic (streaming/error handling), and Data Access (API connections)
    - **Componentization**: Modular, self-contained widgets that manage their own state
    - **Fail-Fast Error Surfacing**: Assertions and validation at all boundaries to expose architectural flaws during development
    - **Dynamic Content Management**: VerticalScroll containers with reactive attributes for real-time updates

## The Sacred Turn Structure

The primary application flow, which populates the Sacred Timeline, is organized into **Turns**. Each Turn consists of three mandatory, sequential plugin executions:

1.  **`[User Plugin]`**: Captures and inscribes the user's input.
2.  **`[Cognition Plugin]`**: A special container plugin that orchestrates a dynamic, transparent pipeline of sub-modules to process the user's input.
3.  **`[Assistant Plugin]`**: Takes the final output from the Cognition pipeline and presents it to the user.

This `User -> Cognition -> Assistant` sequence is immutable and forms the fundamental rhythm of the application.

## The Cognition Block: A Pipeline of Thought

The `Cognition` block is not a monolith. It is a workflow orchestrator that executes a sequence of **Cognition Submodules**. Its visual representation on the timeline must show this internal process unfolding dynamically.

**Cognition Pipeline Visualization:**
```
┌─ COGNITION PIPELINE EXECUTION ───────────────────────────┐
│                                                           │
│  Input: "Explain quantum computing basics"               │
│           ↓                                               │
│  ┌─ Route Query ──────────────────────────────────────┐  │
│  │ Model: tinyllama | Duration: 0.3s | Tokens: 45     │  │
│  │ Decision: "EDUCATIONAL → Use tutorial approach"     │  │
│  └─────────────────────────────────────────────────────┘  │
│           ↓                                               │
│  ┌─ Research Domain ──────────────────────────────────┐  │
│  │ Model: phi-3.5 | Duration: 1.2s | Tokens: 284      │  │
│  │ Output: "Key concepts: superposition, entanglement" │  │
│  └─────────────────────────────────────────────────────┘  │
│           ↓                                               │
│  ┌─ Generate Examples ────────────────────────────────┐  │
│  │ Model: deepseek | Duration: 2.1s | Tokens: 412     │  │
│  │ Output: "Code samples + visual analogies"          │  │
│  └─────────────────────────────────────────────────────┘  │
│           ↓                                               │
│  ┌─ Synthesize Response ──────────────────────────────┐  │
│  │ Model: claude | Duration: 0.8s | Tokens: 156       │  │
│  │ Output: "Structured educational explanation"       │  │
│  └─────────────────────────────────────────────────────┘  │
│           ↓                                               │
│  Final Response: Complete quantum computing explanation   │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

**Example Workflow:**
`[[ Cognition ]] = [[ Route Query (tinyllama) ]] → [[ Research Domain (phi-3.5) ]] → [[ Generate Examples (deepseek) ]] → [[ Synthesize Response (claude) ]]`

Each submodule in this pipeline is its own unit with a strict transparency contract:
-   **A Specific Task**: Clearly defined purpose (e.g., routing, enhancing, tool use).
-   **A Specific Model/Tool**: Explicitly names the LLM provider, model, or shell tool being used.
-   **Dedicated Timers**: Tracks its own wall time.
-   **Dedicated Token Counts**: Tracks its own input/output tokens.
-   **Streaming Output**: Must stream its thoughts or raw output as it's generated.
-   **Finalized Artifact**: Inscribes its final, clean output into the Cognition block's record.

The UI must render this sequence live, showing each submodule appear, run (with animations), and finalize before the next begins.

## Textual Chat Application Architecture

**Sacred GUI Architecture Implementation:**
Following proven industry patterns for dynamic, streaming chat applications using Textual's VerticalScroll containers:

**Three-Layer Widget Architecture:**
1. **SacredTimelineWidget** (VerticalScroll): Immutable history display using V3's proven chat container pattern
2. **LiveWorkspaceWidget** (VerticalScroll): Dynamic cognition streaming with thread-safe updates via `call_from_thread()`
3. **PromptInput**: User interface with validation and focus management

**Streaming Content Management:**
- **Dynamic Resizing**: Content-driven widget height, no hardcoded sizes
- **Smart Auto-Scroll**: Only scroll when user is at bottom to prevent interruption
- **Error Boundaries**: Wrap major UI sections to catch/display errors without app crashes
- **State Auditing**: Integrity checks after key events with immediate error surfacing

**Thread-Safe Streaming Pattern (V3 Proven):**
```python
# Background worker thread
@work(thread=True)
async def stream_cognition():
    # LLM processing
    self.app.call_from_thread(workspace.mount, sub_module_widget)
    # Stream updates
    async for chunk in response:
        self.app.call_from_thread(widget.append_chunk, chunk)
```

**Central State Management:**
- **UnifiedTimeline**: Central state object managing all blocks and streaming
- **Explicit Mutations**: All state changes through validated service methods
- **Event-Driven Updates**: Textual's message system for cross-widget communication
- **Unidirectional Data Flow**: Live workspace → Sacred timeline transfer on completion
