
# Ledger: Intelligent Context Pruning and Summarization

**Goal:** To implement an intelligent system for automatically managing the LLM's context window, ensuring relevant information is retained while optimizing for token limits through smart pruning and summarization.

## 1. Core Philosophy

- **Context Optimization:** Maximize the utility of the limited context window by prioritizing the most relevant information.
- **Dynamic Adaptation:** Adjust context management strategies based on the current task, conversation flow, and available token budget.
- **Transparency (Optional):** Provide insights into how context is being managed, if desired by the user.

## 2. Core Functionality

### 2.1. Context Prioritization Engine

#### Feature

- A mechanism to score and prioritize different pieces of conversational context (blocks from the Sacred Timeline, scratchpad entries, hierarchical context) based on their relevance to the current turn.

#### Implementation Details

1.  **Relevance Scoring:**
    -   **Recency:** More recent turns receive higher scores.
    -   **User Explicit Mention:** Blocks explicitly referenced by the user (e.g., via `manual-context-re-injection.md`) receive a significant boost.
    -   **Semantic Similarity:** Use embeddings (from `memory-and-context-management.md` RAG) to score blocks semantically similar to the current query.
    -   **Task Relevance:** For tasks managed by `project-and-task-management.md`, prioritize context directly related to the current todo item or task description.
2.  **Context Window Filling:**
    -   Fill the context window with the highest-scoring blocks until the token limit is reached.

### 2.2. Automatic Summarization Module

#### Feature

- When the context window approaches its limit, automatically summarize less critical or older parts of the conversation to free up tokens.

#### Implementation Details

1.  **Trigger:** Summarization is triggered when the estimated token count of the current context plus the new input exceeds a configurable threshold (e.g., 80% of the model's context window).
2.  **Summarization Target:** Identify contiguous blocks of lower-priority conversation history for summarization.
3.  **Summarization LLM:** Use a fast, cost-effective LLM (from `llm-routing-and-cognitive-plugins.md`) to generate a concise summary of the targeted blocks.
4.  **Replacement:** Replace the original blocks in the active context with their summary. The original blocks remain in the persistent Sacred Timeline.
5.  **Summary Block:** The summary itself can be represented as a new type of block in the timeline, linking back to the original summarized blocks.

### 2.3. Context Pruning (Discarding)

#### Feature

- For very long conversations, implement a strategy to completely prune (discard from active context, but not from persistent storage) the least relevant or oldest context that cannot be effectively summarized.

#### Implementation Details

-   This will be a last resort, applied only when summarization is insufficient.
-   A configurable threshold will determine when pruning occurs.
-   Users will be notified when pruning happens.

## 3. Integration Points

-   **`memory-and-context-management.md`:** Leverages the persistent Sacred Timeline, RAG embeddings, and hierarchical context.
-   **`llm-routing-and-cognitive-plugins.md`:** Utilizes LLMs for summarization and potentially for relevance scoring.
-   **`project-and-task-management.md`:** Integrates with task-specific context prioritization.
-   **`rich-content-display-engine.md`:** Summarized blocks should be rendered appropriately.

## 4. Advanced Features

-   **User Preferences for Pruning:** Allow users to set preferences for how aggressively context is pruned or summarized.
-   **Visual Context Map:** A UI element that visually represents the current context window, showing which parts are original, summarized, or pruned.
-   **Adaptive Summarization Depth:** The summarization LLM could dynamically adjust the depth of summarization based on the available token budget.
