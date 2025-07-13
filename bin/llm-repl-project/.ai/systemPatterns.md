# System Patterns: LLM REPL - Architecture and Design Principles

## System Architecture

The LLM REPL project is built upon a **Sacred GUI Architecture** featuring a three-area layout: Sacred Timeline, Live Workspace, and Input. This design is immutable and critical for transparent AI cognition.

### Three-Area Layout (2-way ↔ 3-way split)

*   **Sacred Timeline (Top)**: A `VerticalScroll` container for immutable conversation history, using simple block widgets and `hrule` separators. It follows V3's proven chat pattern.
*   **Live Workspace (Middle)**: A `VerticalScroll` container for real-time cognition process visualization, showing sub-module widgets and the final assistant response. It is visible only during active processing.
*   **Input (Bottom)**: A `PromptInput` widget for user input, with fixed height and multiline support.

## Key Technical Decisions

*   **No Nested Containers**: A critical design principle. `Vertical` inside `VerticalScroll` or any container widgets with child containers are forbidden to prevent layout conflicts. Only simple widgets are allowed as direct children.
*   **Clean Separation of Concerns**: Each section (Timeline, Workspace, Input) manages its own layout independently, preventing interference.
*   **Turn Lifecycle**: A defined sequence of states: Idle (2-way split) → User Input (3-way split, Live Workspace appears) → Cognition Processing → Assistant Response → Turn Completion (content moves to Sacred Timeline, Live Workspace disappears).

## Design Patterns in Use

*   **V3's Proven Success**: The architecture is heavily based on V3's working GUI patterns, particularly the `VerticalScroll + Chatbox` pattern for content display.
*   **Fail-Fast Validation**: Assertions and validation at all boundaries to immediately expose architectural flaws during development.
*   **Error Boundaries**: UI sections are wrapped to catch and display errors gracefully without crashing the application.
*   **Unlimited Scalability**: Both Sacred Timeline and Live Workspace are designed to handle unlimited content via natural scrolling.
*   **Reactive Attributes**: Automatic UI updates when content changes.
*   **Smart Auto-Scroll**: Content automatically scrolls only when the user is near the bottom, preventing interruption.
*   **Thread-Safe Updates**: All UI updates from worker threads use `call_from_thread()` to ensure thread safety.

## Component Relationships

*   **Sacred Timeline**: Immutable history display.
*   **Live Workspace**: Dynamic cognition streaming.
*   **PromptInput**: User interaction.
*   **SimpleBlockWidget**: Used for all content blocks in the Sacred Timeline.
*   **SubModuleWidget**: Used for pipeline steps in the Live Workspace.

## Critical Implementation Paths

*   **User Input Processing Flow**: Validation → Timeline Addition → Workspace Activation → Async Processing Start.
*   **Cognition Pipeline Processing Flow**: Sequential execution of submodules (Route Query, Research Domain, Generate Examples, Synthesize Response, Assistant Response) with real-time UI updates.
*   **Error Handling & Validation Patterns**: Implementation of `ErrorBoundaryWidget` and a fail-fast validation pipeline for user input.
*   **Responsive Design Patterns**: Auto-scroll behavior and content-driven height management.
