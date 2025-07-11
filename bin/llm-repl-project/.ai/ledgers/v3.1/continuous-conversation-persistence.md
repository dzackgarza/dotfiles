
# Ledger: Continuous Conversation Persistence

**Goal:** To ensure that no conversation history is ever lost, including transient, in-progress blocks, and to make every application session feel like a continuous, unbroken conversation.

## 1. Core Philosophy

- **Never Lose History:** Every interaction, from the moment a user starts typing to the final inscribed block, must be persistently recorded.
- **Unbroken Conversation:** The concept of a "new session" is replaced by the continuation of one long, ongoing conversation.
- **Sacred Timeline Extension:** The immutability of the Sacred Timeline extends to its transient states, ensuring full auditability and recovery.

## 2. Core Functionality

### 2.1. Real-time In-Progress Block Checkpointing

#### Feature

- Periodically save the state of transient, in-progress blocks (e.g., the current `User Input` being typed, or a `Cognition` block that is actively streaming output) to a temporary, dedicated area in the persistent database.

#### Implementation Details

-   **Mechanism:** Save partial block data to a temporary table or section within the SQLite database (leveraging `timeline-persistence-and-rag.md`).
-   **Frequency:** Checkpointing will occur at regular intervals (e.g., every 5 seconds) or based on significant events (e.g., after every streamed token, after a certain number of characters typed in the input).
-   **Recovery:** On application startup, check for and load any un-inscribed, in-progress blocks. Present them to the user for continuation or discard.

### 2.2. Automatic Session Continuation

#### Feature

- Every application launch will automatically resume the last active conversation, eliminating the concept of starting a "new" session.

#### Implementation Details

-   On application launch, automatically load the *last active* timeline from the persistent database (as defined in `memory-and-context-management.md` and `timeline-persistence-and-rag.md`).
-   Optionally, allow the user to explicitly start a new "branch" or load a different saved session (linking to `Chat Branching and Resumption` from `memory-and-context-management.md`).

### 2.3. Scrollback Buffer Management

#### Feature

- The visible scrollback buffer in the UI will be a dynamic view into the entire persistent Sacred Timeline, allowing seamless navigation through the complete conversation history.

#### Implementation Details

-   The UI's scrollback buffer will not be a separate storage mechanism but a window into the persistent database.
-   Allow users to configure the size of the visible scrollback buffer (e.g., number of lines or blocks).
-   Ensure smooth scrolling and navigation (e.g., Page Up/Page Down, mouse wheel) through the entire persistent history, even if only a portion is currently visible.

### 2.4. Robust Crash Recovery

#### Feature

- The system will be able to recover gracefully from unexpected shutdowns, minimizing data loss and ensuring conversation integrity.

#### Implementation Details

-   Leverage the real-time checkpointing of in-progress blocks and the persistent Sacred Timeline.
-   On startup, perform integrity checks on the database to ensure no corruption.
-   If an in-progress block is found during recovery, prompt the user for action (continue, discard, save as new branch).

## 3. Integration Points

-   **`timeline-persistence-and-rag.md`:** This ledger provides the foundational database persistence for the Sacred Timeline.
-   **`memory-and-context-management.md`:** This ledger defines the broader context and history management, including chat branching and compression.
-   **`file-editing-system.md`:** Ensure that any in-progress file edits are also covered by the checkpointing mechanism.

## 4. Advanced Features

-   **Versioning of In-Progress Blocks:** Allow for multiple versions of an in-progress block to be saved, enabling more granular recovery options.
-   **Conflict Resolution for Recovered Blocks:** If a recovered in-progress block conflicts with a newly started interaction, provide intelligent conflict resolution options.
-   **Visual Indication of Checkpoints:** Provide subtle UI cues to indicate when an in-progress block has been checkpointed.
