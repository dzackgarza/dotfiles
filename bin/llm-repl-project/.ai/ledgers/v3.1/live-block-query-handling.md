# Ledger: Live Block Query Handling

**Goal:** To define the behavior when a user submits a query while a "live" block (e.g., a streaming response from an LLM, a long-running tool execution) is still pending. The system should gracefully handle this input, providing flexibility for how the live block's processing is affected.

## 1. Core Principles

-   **Responsiveness:** The system should immediately acknowledge user input, even if a live block is active.
-   **Contextual Integration:** User input should be integrated into the ongoing conversation or processing in a logical and contextually relevant manner.
-   **Flexibility:** Provide mechanisms for plugins or the core system to decide how to best incorporate the new input, whether by extending the current turn, buffering, or re-evaluating.

## 2. Implementation Details

### 2.1. Buffering User Input

#### Feature

-   When a user sends a query while a live block is pending, the input should be buffered.

#### Implementation Details

-   Implement an input buffer that temporarily stores user queries received during an active live block.
-   The buffer should be capable of storing multiple queries in sequence.

### 2.2. Integration with Live Blocks

#### Feature

-   Define strategies for how buffered user input interacts with the pending live block.

#### Implementation Details

-   **Option A: Continue and Extend Turn:** The buffered query can be appended to the current turn's context, allowing the live block to continue its operation and potentially extend its output based on the new input. This is suitable for conversational extensions or clarifications.
-   **Option B: Internal Plugin Re-evaluation:** For plugins or tools that are currently executing, the buffered query can trigger an internal re-evaluation. The plugin can decide to:
    -   Combine the new input with its current state and continue processing.
    -   Re-run its operation with all buffered queries as new context, discarding previous partial results (if appropriate).
-   **Option C: New Round of Plugin Execution:** The buffered query can initiate a new, internal round of the same plugin's execution, with its results combined with the ongoing live block's output. This is useful for iterative refinement or parallel processing.

### 2.3. Plugin Decision-Making

#### Feature

-   Plugins or tool executions should have the ability to signal how they prefer to handle buffered user input.

#### Implementation Details

-   Introduce a mechanism (e.g., a flag, a callback, or a specific return type) that allows a live block or plugin to indicate its preferred handling strategy for incoming user queries.
-   If no specific strategy is indicated, a default behavior (e.g., buffering and appending to the next available turn) should be applied.

### 2.4. User Feedback

#### Feature

-   Provide clear visual feedback to the user when their input is buffered or being integrated into a live block.

#### Implementation Details

-   Display a subtle indicator (e.g., a small icon, a temporary message) to confirm that the user's query has been received and is being processed in the background or buffered.
-   Update the UI to reflect how the live block is adapting to the new input (e.g., extended output, new sub-blocks).

### Implementation Plan
1. **Phase 1: Planning** - Review and plan implementation
2. **Phase 2: Implementation** - Core development work
3. **Phase 3: Testing** - Testing and validation
4. **Phase 4: UX Polish** - Final polish and user experience improvements
5. **Phase 5: Integration** - Integrate ledger into the main system