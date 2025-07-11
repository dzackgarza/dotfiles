# Ledger: Sacred Timeline Git Integration

**Goal:** To establish Git as the foundational version control system for the Sacred Timeline, ensuring every turn of interaction is meticulously tracked and committed, thereby providing unparalleled resilience, debugging capabilities, and context retrieval.

## 1. Core Philosophy

-   **Ubiquitous Version Control:** The application will operate exclusively within a Git repository, making version control an inherent part of every interaction.
-   **Atomic Turn Commits:** Every single turn of the LLM-CLI interaction will result in an automatic Git commit, creating a granular and auditable history.
-   **Resilience & Debuggability:** This deep integration enables precise rollback, detailed debugging, and robust context retrieval, making the system highly resilient to errors and interruptions.

## 2. Implementation Details

### 2.1. Git Repository Requirement

#### Feature

-   The application will enforce that it is always started and operated within a valid Git repository.

#### Implementation Details

-   Upon startup, verify the current working directory is part of a Git repository (e.g., by checking for a `.git` directory).
-   If not in a Git repository, prompt the user to initialize one or exit.

### 2.2. Automatic Turn Commits

#### Feature

-   A Git commit will be automatically generated after every completed turn of interaction, regardless of file changes.

#### Implementation Details

-   **Commit Trigger:** The commit process will be triggered at the end of each user-LLM interaction cycle (a "turn").
-   **Commit Content:**
    -   All modified files within the repository will be staged and committed.
    -   If no files are changed, an empty commit will still be created to mark the turn in the timeline.
-   **Commit Message:** The commit message will be automatically generated and will include:
    -   A unique identifier for the turn.
    -   A summary of the LLM's action or the user's query.
    -   Metadata about the turn (e.g., timestamp, LLM model used).
-   **LLM Context in Commits:** The LLM's internal thought process, key decisions, and relevant context for that turn will be captured and included in the commit message or as part of the commit (e.g., in a dedicated file within the commit, or as a structured part of the commit message).

### 2.3. Sacred Timeline Integration

#### Feature

-   The Git history will serve as the definitive "Sacred Timeline" for all interactions and changes.

#### Implementation Details

-   The application's internal timeline representation will directly map to Git commits.
-   Navigation through the Sacred Timeline will correspond to Git operations (e.g., `git checkout` to revert to a specific turn's state).

### 2.4. Benefits and Use Cases

#### Feature

-   Leverage the Git-backed timeline for advanced debugging, rollback, and context retrieval.

#### Implementation Details

-   **Precise Rollback:** Users (or the LLM itself) can easily revert to any previous state of the project by checking out a specific turn's commit.
-   **Debugging Hallucinations:** If the LLM generates incorrect or "hallucinated" code, the exact changes can be identified and undone.
-   **Enhanced RAG:** The entire Git history, including commit messages and embedded LLM context, can be used as a rich source for Retrieval Augmented Generation (RAG), allowing the LLM to recall past interactions and decisions with high fidelity.
-   **Interruption Resilience:** In case of crashes or interruptions, the last committed state is always recoverable, minimizing lost work.
