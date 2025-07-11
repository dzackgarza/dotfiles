
# Ledger: Manual Context Re-Injection

**Goal:** To provide a mechanism for users to manually re-inject specific past turns or blocks from the Sacred Timeline into the current query, effectively reminding the LLM of forgotten context.

## 1. Core Philosophy

- **User Control:** Empower the user to directly influence the LLM's context when automatic RAG or context management falls short.
- **Context Correction:** Provide a "hack" to overcome LLM context window limitations or "forgetfulness" without resorting to manual copy-pasting.
- **Transparency:** Clearly indicate when context has been manually re-injected.

## 2. Core Functionality

### 2.1. Re-Inject Command

#### Feature

- A command (e.g., `/reinject <block_id> [block_id...]`) that allows the user to select one or more past blocks from the Sacred Timeline and include their content in the next prompt sent to the LLM.

#### Implementation Details

1.  **Block Selection:**
    -   Users will identify blocks by their unique `block_id` (which should be visible in the UI, perhaps on hover or via a `/timeline show_ids` command).
    -   Support for selecting multiple blocks.
2.  **Content Extraction:**
    -   Retrieve the full content of the selected blocks from the persistent Sacred Timeline database (leveraging `timeline-persistence-and-rag.md`).
3.  **Prompt Augmentation:**
    -   The content of the re-injected blocks will be prepended to the user's next query, clearly demarcated (e.g., with a special markdown block or comment) to indicate it's re-injected context.
    -   The re-injected content will be treated as high-priority context for the LLM.
4.  **UI Feedback:**
    -   Visually indicate in the UI when a query has been augmented with re-injected context (e.g., a small icon next to the input prompt).

### 2.2. Interactive Block Selection (Advanced)

#### Feature

- An interactive mode (e.g., `/reinject --interactive`) that allows users to browse the timeline and visually select blocks for re-injection.

#### Implementation Details

-   Launch a Textual overlay that displays the timeline.
-   Allow users to navigate and select blocks (e.g., using arrow keys and spacebar).
-   Display a preview of the content of selected blocks.

## 3. Integration Points

-   **`timeline-persistence-and-rag.md`:** Provides access to the full Sacred Timeline content.
-   **`memory-and-context-management.md`:** This feature complements RAG by providing manual control over context injection.
-   **`rich-content-display-engine.md`:** Re-injected content should be rendered correctly in the prompt sent to the LLM.

## 4. Advanced Features

-   **Summarization of Re-injected Content:** If re-injecting a large block, offer to summarize it before injection to save tokens.
-   **Semantic Search for Re-injection:** Allow users to search the timeline semantically to find blocks to re-inject.
-   **Re-injecting Partial Blocks:** Select specific parts of a block for re-injection.
