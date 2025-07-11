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
