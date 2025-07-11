
# Ledger: Project and Task Management

**Goal:** To enable the REPL to act as a high-level project and task manager, automating common development tasks, orchestrating complex, long-running tasks, and maintaining context across multiple tool calls.

## 1. Core Philosophy

- **Automation:** Reduce boilerplate and repetitive setup tasks for project creation and maintenance.
- **Task Orchestration:** Break down complex tasks into manageable steps and track progress autonomously.
- **Context Preservation:** Ensure the AI retains relevant context across many turns and tool calls for long-running tasks.
- **Convention over Configuration:** Provide sensible defaults for common project types.

## 2. Core Functionality

### 2.1. Project Scaffolding and Management

#### Feature

- A `/project` command with subcommands for various project management tasks, such as creating new projects, initializing version control, and setting up environments.

#### Commands

-   **`/project new <type> <name>`**
    -   **Action:** Creates a new project of a specified type (e.g., `python`, `javascript`, `rust`) with the given name.
    -   **Steps:** Create directory, `git init`, `.gitignore`, virtual environment (Python), `package.json` (Node.js), `README.md`.

-   **`/project init <type>`**
    -   **Action:** Initializes a project in the current directory.

-   **`/project clean`**
    -   **Action:** Cleans up common project artifacts (e.g., `__pycache__`, `node_modules`).

### 2.2. LLM-Powered Task Management

#### Feature

- A `/task` command with subcommands for managing complex, long-running tasks that require multiple tool calls, maintaining context, and handling long contexts effectively.

#### Commands

-   **`/task new <description>`**
    -   **Action:** Creates a new long-running task. The AI will then break it down into smaller steps and populate a todo list.

-   **`/task continue`**
    -   **Action:** Instructs the AI to continue working on the current task, reviewing its todo list and executing the next step.

-   **`/task todo [add <item> | complete <id> | remove <id>]`**
    -   **Action:** Manages the todo list for the current task (for AI internal use and user manual adjustment).

-   **`/task show`**
    -   **Action:** Displays the current task's description, todo list, and relevant context.

-   **`/task context [add <text> | clear]`**
    -   **Action:** Allows adding/clearing specific context relevant to the current task.

### 2.3. Context Management for Long Tasks

#### Feature

- The plugin will intelligently manage the context provided to the LLM for long-running tasks, ensuring that relevant information is always available without exceeding token limits.

#### Implementation Details

1.  **Context Prioritization:** Prioritize context from the current task's description, todo list, and explicitly added context. Leverage long-term memory (RAG) for past interactions.
2.  **Context Summarization:** When context approaches token limits, use an LLM to summarize less critical parts of the context.

## 3. Advanced Features

-   **Custom Templates:** Allow users to define their own project templates.
-   **Dependency Management:** Integrate with package managers (e.g., `pip`, `npm`).
-   **Build/Test Automation:** Provide commands to run common build and test scripts.
-   **Task Persistence:** Tasks should be saved and loaded across sessions.
-   **Multi-Agent Collaboration:** Allow multiple AI agents to work on different parts of the same task.
