# Code Patterns

This project's architecture is dictated by its user experience. The following patterns ensure the UI is a direct and transparent reflection of the system's internal state.

## Core Architectural Patterns

These patterns define the fundamental structure and behavior of the application, ensuring modularity, integrity, and extensibility.

### The Sacred Timeline as State

The application's state is its history. The Sacred Timeline is the single source of truth.

-   **Append-Only Ledger**: The timeline is an immutable, append-only log. New blocks are added, but existing blocks are never modified. This ensures a complete and auditable history of all operations.
-   **Stateful Plugins, Stateless Core**: The core application is a stateless orchestrator. All state is encapsulated within the plugins as they execute, and the final, permanent state is inscribed into the timeline blocks themselves.

### The Sacred Turn Process

The application's main loop is not a free-form event handler; it is a strict, sequential execution of a **Turn**. A Turn is always composed of three plugin executions:

1.  **`UserPlugin`**: Captures user input.
2.  **`CognitionPlugin`**: Orchestrates a cognitive pipeline.
3.  **`AssistantPlugin`**: Formats and delivers the final response.

This pattern is the fundamental building block of the application and must not be violated.

### Plugin System Patterns

The entire application is built around a robust plugin system, enabling radical extensibility and isolated development.

-   **Plugin Interface/Contract**: All plugins adhere to a strict interface (`BlockPlugin`) that defines their lifecycle methods (initialize, activate, process, render) and mandates the provision of transparency metadata (timers, token counts, state).
-   **Plugin Manager**: A central orchestrator responsible for discovering, loading, managing the lifecycle, and composing plugins. It acts as the primary interface for interacting with plugins.
-   **Dependency Injection**: Plugins declare their dependencies, which are then provided by the Plugin Manager. This promotes loose coupling and testability.

### Multi-LLM Orchestration Pattern

The system is designed to seamlessly integrate and orchestrate multiple Large Language Models (LLMs) for hyper-optimized task execution.

-   **Provider/Model Abstraction**: A clear abstraction layer for different LLM providers and models ensures that plugins can request capabilities without being tied to specific implementations.
-   **Dynamic Routing**: The Intelligent Router (a key Cognition Submodule) dynamically selects the most appropriate LLM or tool based on the task, user intent, and available resources (local, remote, specialized).

### State Management Patterns

Beyond the Sacred Timeline, internal state is managed with precision to ensure predictability and prevent errors.

-   **State Machine**: The application's lifecycle and complex processes (like the Cognition pipeline) are managed by explicit state machines. This enforces valid transitions and prevents operations in incorrect states.
-   **Immutable Data Structures**: Where feasible, data passed between components or stored temporarily is immutable. Changes result in new data structures, simplifying debugging and ensuring data integrity.

### Guaranteed Display Completion (Proof-Based Display)

To ensure the UI accurately reflects the system's state and that critical information is truly presented to the user, the system employs a unique proof-based display mechanism.

-   **Proof Tokens**: Display operations return explicit "proof tokens" (`DisplayComplete`, `StartupComplete`). These tokens are only generated *after* content has been verifiably rendered to the terminal, preventing timing violations and ensuring that subsequent operations do not proceed until the display is complete.

### Communication Patterns

To maintain UI-agnosticism and modularity, components communicate in a decoupled manner.

-   **Event-Driven Communication**: Components (plugins, UI, core) communicate primarily through events. This allows for loose coupling, where senders don't need direct knowledge of receivers.
-   **Message Passing**: Specific data or commands are passed between components as well-defined messages, ensuring clear contracts for inter-component interaction.

## The Cognition Pipeline Pattern

The `CognitionPlugin` is a specialized **workflow orchestrator**. It does not contain monolithic processing logic. Instead, it dynamically constructs and executes a pipeline of **Cognition Submodules**.

-   **Submodule Atomicity**: Each submodule is a self-contained unit of work with a single, well-defined purpose (e.g., routing, prompt enhancement, tool execution).
-   **Sequential Execution**: Submodules are executed sequentially. The output of one submodule can be used as the input for the next.
-   **Dynamic Composition**: The pipeline of submodules can be composed dynamically based on the user's input or the application's state.

## The Plugin Contract Pattern

All plugins, including Cognition Submodules, must adhere to a strict contract enforced by the `Plugin Validator`.

-   **Self-Contained**: Plugins manage their own state and rendering logic.
-   **Transparency Mandate**: Plugins *must* provide real-time data for:
    -   State (`processing`, `completed`, `error`)
    -   Wall Time (live and final)
    -   Token Counts (live and final)
    -   Provider/Model/Tool identifiers
-   **Isolated Testability**: Plugins must be designed to be tested in isolation, without requiring the full application stack.

### Streaming and Live Output Pattern

All long-running operations, especially LLM calls, must provide real-time feedback to the user.

-   **Live State**: Plugins and Cognition Submodules transition to a "live" state during execution, providing dynamic visual cues (e.g., animations, timers, streaming text).
-   **Progressive Rendering**: Output is streamed and progressively rendered to the UI, allowing users to follow the AI's thought process and intermediate results.
-   **Thoughts and Intermediate Reasoning**: When applicable, LLMs will stream their internal thoughts or intermediate reasoning, which will be displayed in the UI and inscribed onto the timeline.

## Shared Utilities Pattern

To ensure consistency and avoid code duplication, common functionalities are provided as shared utilities that can be injected into any plugin.

-   **Rich Content Renderers**: Standardized renderers for diverse content types, ensuring beautiful and consistent display across the application:
    -   `Markdown` (with syntax highlighting for code blocks)
    -   `LaTeX`-compatible mathematics (e.g., MathJax/KaTeX)
    -   Rich visual representations of Jupyter notebook cells (inputs, outputs, plots)
    -   Interactive elements for deep linking to the filesystem (e.g., `xdg-open` for files, browser for URLs) and future support for MIME-type specific visual representations.
    -   Diagrams (e.g., `tikzcd`, Mermaid, Graphviz - horizon feature).
-   **API Clients**: Reusable clients for interacting with various LLM providers.
-   **Clipboard Integration**: Utilities for intelligent handling of copy-pasted data, including multiline text and rich data types (horizon feature for images).

## Development Philosophy and Coding Conventions

This project follows a rigorous development philosophy focused on correctness, transparency, and maintainability.

### Environment and Dependencies

-   **Virtual Environments**: We ALWAYS use virtual environments (venv, pdm, poetry, etc.) to isolate dependencies and ensure reproducibility.
-   **Frozen Environment**: The environment is frozen for all time. We assume all users have ALL required packages and assert so, crashing otherwise.
-   **No Graceful Degradation**: If any part of the app fails (e.g., a required LLM doesn't respond to heartbeat), we crash unless there's an appropriate hard-coded fallback.

### Proof-Based Development

We use PROOFS in our code to guarantee correctness:

-   **Assert and Crash**: Assert the existence of critical components or crash. Fail fast and fail hard to surface bugs early.
-   **No Silent Failures**: Never fail silently or gracefully. This is a hobby project in constant development, not a corporate product.
-   **Try-Catch Avoidance**: Try-catch blocks are a STRONG indication of hiding failures and should be avoided.

### Testing Philosophy

-   **Echo Tests as Ground Truth**: We use "echo tests" that fully simulate a user's interaction using PRECISELY the same code path as "just run".
-   **No Test Modes**: There are no test modes or non-interactive modes. We test the canonical user code path for the actual user experience.
-   **Test-Driven Development**: We run tests before declaring "victory" and after any change, rigorously guarding against regressions.
-   **Proof of Correctness**: We PROVE correctness through real user experience testing, not abstract unit tests in isolation.

### Architectural Principles

-   **Bug Prevention Over Bug Fixing**: We don't swat bugs. We figure out WHY we didn't catch the bug and redesign the architecture to make it:
    -   A) Impossible to introduce the bug in the first place, or
    -   B) Impossible to miss catching it
-   **Complexity Management**: When a script approaches 500+ lines, we stop and rethink architecture, possibly redesigning entirely to keep complexity manageable.
-   **Modular Independence**: Developers should not need to understand 15 other files/functions/classes to work on their module beyond explicit imports.

### Code Style

-   **Functional Programming**: We stick to functional styles:
    -   Avoid deeply nested if-then chains in favor of principled logic routers
    -   Use map/reduce/filter/collect/lambda constructions
    -   Leverage list comprehensions
    -   Employ mathematical structures like sets to prove correctness
-   **Strong Typing**: Use strong typing and Pydantic types whenever possible
-   **Linting and Type Checking**: Run strong linters that catch all type errors before declaring a feature implemented

### Type Checking and Correctness Validation

We use **mypy** and **flake8** to catch correctness issues and prevent runtime errors, without enforcing style preferences.

-   **Purpose**: Focus on correctness, not style
    -   Catch type errors that would cause runtime crashes
    -   Detect undefined variables and name errors
    -   Find logical errors like duplicate parameters
    -   Prevent import errors and missing dependencies
    -   NO style enforcement - focus on correctness only

-   **What Gets Checked**:
    -   MyPy: Undefined variables, type mismatches, optional handling, import validation
    -   Flake8: Syntax errors (E9), invalid print statements (F63), logical errors (F7), undefined names (F82)

-   **What Does NOT Get Checked**: Line length, code formatting, naming conventions, import ordering, docstring style

-   **Workflow**: Run `just lint` before committing to catch type/correctness errors

### Version Control

-   **Strict Git Adherence**: We strictly adhere to git practices
-   **Revert When Stuck**: If stuck for too long, revert to the last working version and rethink the problem
-   **Extensive Documentation**: Document changes EXTENSIVELY in git history
-   **Atomic Commits**: Make small, focused commits that represent complete units of work
