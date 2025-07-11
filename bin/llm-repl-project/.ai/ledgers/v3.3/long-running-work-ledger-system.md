# Ledger: Long-Running Work Ledger System

**Goal:** To establish a robust and resilient system for managing long-running tasks performed by LLMs, ensuring continuity and recovery from interruptions or crashes. This system leverages a "ledger" approach where each task is represented by a persistent file.

## 1. Core Philosophy

-   **Resilience:** Ensure that LLM work can resume seamlessly after interruptions (e.g., disconnections, system crashes) without significant loss of progress.
-   **Transparency:** Provide a clear, auditable record of ongoing and completed tasks.
-   **Autonomy:** Enable LLMs to manage their own workload and state.

## 2. Implementation Details

### 2.1. Task Representation as Ledgers

#### Feature

-   Each long-running task (e.g., implementing a feature, writing a story, developing tests) will be represented as a distinct "ledger" file.

#### Implementation Details

-   Ledger files will be created in a designated directory (e.g., `.ai/ledgers/tasks/`).
-   Each ledger file will contain a clear description of the task, its current status, and any relevant context or sub-tasks. The format should be easily parsable by the LLM (e.g., Markdown, JSON).
-   A unique identifier should be associated with each ledger file (e.g., a UUID in the filename or metadata).

### 2.2. LLM Workload Management

#### Feature

-   LLMs will organize their work into a dynamic "todo list" derived from the active ledger files.

#### Implementation Details

-   Upon startup or recovery, the LLM will scan the designated ledger directory to reconstruct its pending workload.
-   The LLM will prioritize tasks based on predefined criteria (e.g., urgency, dependencies, last modification time).
-   As the LLM processes a task, it will update the corresponding ledger file to reflect progress and intermediate results.

### 2.3. Completion and Deletion

#### Feature

-   Upon successful completion of a task, the associated ledger file will be deleted.

#### Implementation Details

-   The LLM will be responsible for marking a task as complete and initiating the deletion of its ledger file.
-   A confirmation mechanism (e.g., a final review by the LLM or a user prompt) may be implemented before deletion to prevent accidental loss of information.

### 2.4. Interruption and Recovery

#### Feature

-   The system will be resilient to interruptions, allowing LLMs to pick up work from where they left off.

#### Implementation Details

-   In case of an interruption (e.g., crash, power loss), the state of ongoing tasks will be preserved in their respective ledger files.
-   Upon restart, the LLM will identify incomplete tasks by the presence of their ledger files and resume processing from the last recorded state.
-   Mechanisms for handling corrupted ledger files (e.g., backup, manual intervention) should be considered.
