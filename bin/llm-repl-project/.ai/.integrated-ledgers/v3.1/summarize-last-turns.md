
# Ledger: Summarize Last Turns Plugin

**Goal:** To provide a slash command that summarizes the last `N` turns of the conversation and re-injects that summary into the current LLM context, helping to alleviate contextual issues and manage token usage.

## 1. Core Philosophy

- **Context Refresh:** Provide a user-initiated mechanism to refresh the LLM's understanding of recent conversation history.
- **Token Efficiency:** Reduce the amount of raw conversation history sent to the LLM by replacing it with a concise summary.
- **User Control:** Empower the user to decide when and how much of the recent history should be summarized.

## 2. Core Functionality

### 2.1. `/summarize N` Command

#### Feature

- A `/summarize N` command where `N` specifies the number of most recent turns to summarize.
- The plugin will retrieve the last `N` turns from the Sacred Timeline, send them to a summarization model, and then use that summary to augment the next query to the main LLM.

#### Implementation Details

1.  **Turn Retrieval:**
    -   Retrieve the last `N` turns from the Sacred Timeline (leveraging `timeline-persistence-and-rag.md` and `memory-and-context-management.md`).
    -   Handle cases where `N` is greater than the available turns.
2.  **Summarization Model Selection:**
    -   Use a dedicated summarization model (e.g., a fast, cost-effective LLM from the `llm-routing-and-cognitive-plugins.md` ledger, specifically a model optimized for summarization).
3.  **Summary Generation:**
    -   Send the retrieved turns to the summarization model with a prompt to generate a concise summary.
4.  **Context Augmentation:**
    -   The generated summary will be prepended to the user's next query to the main LLM, clearly demarcated as a summary of previous turns.
    -   This will be similar to the mechanism used in `manual-context-re-injection.md`.
5.  **UI Feedback:**
    -   Display a message to the user indicating that the summary has been generated and will be used for the next query.
    -   Optionally, display the generated summary to the user.

## 3. Integration Points

-   **`timeline-persistence-and-rag.md`:** For retrieving past turns.
-   **`memory-and-context-management.md`:** For managing the overall context and potentially integrating with context compression.
-   **`llm-routing-and-cognitive-plugins.md`:** For selecting and utilizing the summarization model.
-   **`manual-context-re-injection.md`:** The mechanism for augmenting the prompt will be similar.

## 4. Advanced Features

-   **Configurable Summarization Depth:** Allow users to configure the maximum length of the generated summary.
-   **Automatic Summarization:** Implement a feature where the system automatically summarizes older turns when the context window approaches its limit.
-   **Summarization of Specific Blocks:** Allow users to specify a range of blocks or specific block IDs to summarize.
