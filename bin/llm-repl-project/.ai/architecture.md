# Architecture

## Guiding Philosophies

This project is built on two non-negotiable principles:

1.  **The Timeline is Sacred**: The central data structure is a persistent, append-only timeline of "blocks." Each block represents a discrete unit of work (user input, AI cognition, tool output, etc.). Once inscribed, a block is an immutable part of the application's history, used for context in all future operations. It is the absolute source of truth.

2.  **The UI Reflects the Architecture**: The application's output MUST be a direct reflection of its internal architecture. The user's mental model of the visual timeline of blocks dictates the system's design. Each block corresponds to a self-contained, independently testable plugin. There is no hidden magic.

## The Sacred Turn Structure

The primary application flow, which populates the Sacred Timeline, is organized into **Turns**. Each Turn consists of three mandatory, sequential plugin executions:

1.  **`[User Plugin]`**: Captures and inscribes the user's input.
2.  **`[Cognition Plugin]`**: A special container plugin that orchestrates a dynamic, transparent pipeline of sub-modules to process the user's input.
3.  **`[Assistant Plugin]`**: Takes the final output from the Cognition pipeline and presents it to the user.

This `User -> Cognition -> Assistant` sequence is immutable and forms the fundamental rhythm of the application.

## The Cognition Block: A Pipeline of Thought

The `Cognition` block is not a monolith. It is a workflow orchestrator that executes a sequence of **Cognition Submodules**. Its visual representation on the timeline must show this internal process unfolding dynamically.

**Example Workflow:**
`[[ Cognition ]] = [[ Route Query (tinyllama) ]] -> [[ Enhance Prompt (phi) ]] -> [[ Call Tool (bash) ]] -> [[ Format Output (mistral) ]]`

Each submodule in this pipeline is its own unit with a strict transparency contract:
-   **A Specific Task**: Clearly defined purpose (e.g., routing, enhancing, tool use).
-   **A Specific Model/Tool**: Explicitly names the LLM provider, model, or shell tool being used.
-   **Dedicated Timers**: Tracks its own wall time.
-   **Dedicated Token Counts**: Tracks its own input/output tokens.
-   **Streaming Output**: Must stream its thoughts or raw output as it's generated.
-   **Finalized Artifact**: Inscribes its final, clean output into the Cognition block's record.

The UI must render this sequence live, showing each submodule appear, run (with animations), and finalize before the next begins.

## Core Components

-   **Plugin Engine**: Orchestrates the `User -> Cognition -> Assistant` turn structure. It is responsible for loading plugins and their dependencies.

-   **Plugin Validator**: A critical gateway component. Before a plugin can be loaded, the validator rejects any plugin that could:
    -   Introduce graphical artifacts or violate the UI's clean, terminal-like aesthetic.
    -   Violate the timeline's integrity (e.g., attempting to modify a past block).
    -   Fail to meet the full transparency contract (missing timers, token counters, etc.).

-   **Shared Utilities**: A library of common tools available to all plugins, ensuring consistency. This includes renderers for LaTeX and Markdown, for example.

-   **UI Renderer**: A swappable component responsible for rendering the timeline blocks. It subscribes to events from the Plugin Engine and displays new or updated blocks. It must support a terminal-like aesthetic and be capable of rendering rich content including:
    -   Markdown (with syntax-highlighted code blocks)
    -   LaTeX-compatible mathematics
    -   Rich Jupyter notebook cells (inputs, outputs, plots)
    -   Interactive elements for deep linking to the filesystem (e.g., `xdg-open` for files, browser for URLs) and future support for MIME-type specific visual representations.
    -   Dynamic animations for live states.

-   **Input Processor**: A component responsible for handling user input, including multiline text and intelligently processing copy-pasted data. It will provide visual cues for attached clipboard content and ensure principled inscription of this data onto the Sacred Timeline.

-   **Intelligent Router**: A specialized plugin (likely a core Cognition Submodule) responsible for analyzing user intent and dynamically routing tasks to the most appropriate plugins, LLMs (local, remote, specialized), or external tools (bash, web search, MCP servers). This component is key to abstracting away complex commands and providing a natural language interface to the entire system.

-   **The Sacred Timeline (Database)**: The implementation of the Sacred Timeline. A persistent, append-only log that stores the final, inscribed state of every block from every turn.
