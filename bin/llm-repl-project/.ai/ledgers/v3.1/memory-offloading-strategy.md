# Ledger: Memory Offloading Strategy

**Goal:** To ensure that lengthy chat histories and conversational context are never persistently stored in user-space memory, but are instead immediately offloaded to a multi-tiered database system for efficient management, scalability, and resilience.

## 1. Core Philosophy

-   **Zero User-Space Persistence:** User-space memory is treated as ephemeral for chat history; all significant conversational data is immediately persisted externally.
-   **Performance & Scalability:** Optimize for fast access to recent context while ensuring long-term durability and the ability to handle extensive histories.
-   **Resilience:** Protect against data loss due to application crashes or system restarts by ensuring data is always externalized.

## 2. Implementation Details

### 2.1. Immediate Offloading from User-Space Memory

#### Feature

-   Any incoming or generated chat content, once processed, will be immediately pushed out of user-space memory into a fast-access database caching layer.

#### Implementation Details

-   **Event-Driven Persistence:** As soon as a `TimelineBlock` (User, Assistant, Cognition, etc.) is finalized or a significant chunk of streaming data is received, it will be serialized and written to the medium-term caching layer.
-   **Minimal In-Memory Footprint:** Only the currently active or very recently accessed blocks will reside in user-space memory, and only for the duration of active processing or display.

### 2.2. Multi-Tiered Database System

#### Feature

-   Implement a two-tiered database system for chat history: a fast-access caching layer for medium-term memory and a durable database for long-term storage.

#### Implementation Details

-   **Tier 1: Fast-Access Database Caching Layer (Medium-Term Memory):**
    -   **Purpose:** Provide extremely fast read/write access for recent conversational history and context that the LLM frequently needs to access.
    -   **Technology:** Consider in-memory databases with fast serialization/deserialization, or highly optimized SQLite configurations for caching (e.g., WAL mode, in-memory database for active session, then flushed to disk).
    -   **Data:** Stores recent `TimelineBlocks`, scratchpad data, and potentially vector embeddings for RAG.
    -   **Eviction Policy:** Implement a policy to move older data to the long-term storage or evict it if it exceeds a configurable cache size.

-   **Tier 2: SQLite Database (Long-Term Memory):**
    -   **Purpose:** Provide durable, persistent storage for the entire Sacred Timeline and all associated conversational data.
    -   **Technology:** SQLite, due to its file-based nature, ease of deployment, and robustness for local applications.
    -   **Data:** Stores all `TimelineBlocks`, including their content, metadata, and links to Git commits (as per `sacred-timeline-git-integration.md`). Also stores chat branching information and user-provided knowledge base data.
    -   **Synchronization:** Data from the fast-access caching layer will be asynchronously or periodically flushed/synchronized to the SQLite database.

### 2.3. Integration with Sacred Timeline and Ledgers

#### Feature

-   The memory offloading strategy will seamlessly integrate with the Sacred Timeline and the LLM's long-running work ledgers.

#### Implementation Details

-   **Sacred Timeline:** Each `TimelineBlock` will have a corresponding entry in both the medium-term cache and the long-term SQLite database, linked to its Git commit.
-   **LLM Ledgers:** The LLM's individual task ledgers (as defined in `long-running-work-ledger-system.md` and `long-running-work-ledger-file-structure.md`) will also be stored persistently, likely directly in the long-term SQLite database or as separate files managed by the system.
-   **RAG Integration:** The RAG system (from `memory-and-context-management.md`) will primarily query the medium-term cache for recent context and fall back to the long-term SQLite for older, less frequently accessed data.

## 3. Benefits

-   **Reduced Memory Footprint:** Prevents the application from consuming excessive RAM, especially during long sessions.
-   **Enhanced Stability:** Minimizes the risk of crashes due to out-of-memory errors.
-   **Improved Scalability:** Allows for handling arbitrarily long conversation histories without performance degradation.
-   **Robust Recovery:** Ensures that all conversational context is preserved and recoverable across sessions and system interruptions.

### Implementation Plan
1. **Phase 1: Planning** - Review and plan implementation
2. **Phase 2: Implementation** - Core development work
3. **Phase 3: Testing** - Testing and validation
4. **Phase 4: UX Polish** - Final polish and user experience improvements
5. **Phase 5: Integration** - Integrate ledger into the main system