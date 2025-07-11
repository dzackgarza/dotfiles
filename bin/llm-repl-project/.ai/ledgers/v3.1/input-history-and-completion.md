
# Ledger: Input History and Completion System

**Goal:** To implement a comprehensive and persistent input history system with advanced tab completion capabilities, significantly enhancing user experience and efficiency.

## 1. Core Philosophy

- **Efficiency:** Reduce typing and cognitive load for the user.
- **Discoverability:** Help users discover available commands, subcommands, and arguments.
- **Context-Aware:** Completion suggestions should be relevant to the current input context.
- **Persistence:** History should persist across application sessions.
- **Convenience:** Provide a familiar and efficient way for users to re-use past commands and queries.

## 2. Core Functionality

### 2.1. All-Time Query History and Recall

#### Feature

- Maintain a persistent, all-time history of user queries.
- When the user presses the `Up` arrow key in the input prompt, the previous query from the history will be displayed.
- Pressing `Down` will cycle forward through the history.

#### Implementation Details

1.  **History Storage:**
    -   Store user queries in a persistent database (e.g., SQLite, leveraging `timeline-persistence-and-rag.md`). Each query will be a record in a dedicated history table.
    -   The history should be append-only.
2.  **History Management:**
    -   When a user submits a query, append it to the history database.
    -   On application startup, load a configurable number of recent history items into an in-memory buffer for quick access.
3.  **Arrow Key Recall:**
    -   The `InputWidget` will capture `Up` and `Down` arrow key presses.
    -   When `Up` is pressed, retrieve the previous item from the in-memory history buffer and populate the input field.
    -   When `Down` is pressed, retrieve the next item.
    -   Handle boundary conditions (beginning/end of history).

### 2.2. Tab Completion

#### Feature

- When the user presses the `Tab` key in the input prompt, the system will provide context-sensitive suggestions.

#### Implementation Details

1.  **Command Completion:**
    -   When the input starts with `/`, suggest available top-level commands (e.g., `/help`, `/chat`, `/project`).
    -   If a command is partially typed, complete it.
    -   If a command is fully typed, suggest its subcommands (e.g., `/project new`, `/project init`).
2.  **File Path Completion:**
    -   When the input contains a file path (e.g., after `@` or for commands like `/edit`), suggest files and directories in the current working directory or the specified path.
    -   Support relative and absolute paths.
    -   Respect `.gitignore` rules for file suggestions (leveraging `Git-Aware File Handling` from `command-and-execution.md`).
3.  **Plugin-Specific Argument Completion:**
    -   Plugins will register their expected arguments and possible values with the `HelpRegistry` (or a dedicated `CompletionRegistry`).
    -   When a plugin command is being typed, suggest valid arguments and their possible values (e.g., for `/project new`, suggest `python`, `javascript`).

### 2.3. Integration with Textual's `TextArea`

#### Feature

- Ensure seamless integration of history recall and tab completion with Textual's `TextArea` widget, leveraging its advanced editing capabilities.

#### Implementation Details

- The `InputWidget` (which will likely wrap a `TextArea`) will need to be enhanced to capture `Tab`, `Up`, and `Down` key presses.
- Custom logic will be implemented to interact with the history and completion backends, and to update the `TextArea`'s content and cursor position.

## 3. Advanced Features

-   **Searchable History:** Allow users to search their history (e.g., `Ctrl+R` for reverse-i-search, potentially integrating `fzf` as per `input-fzf-integration.md`).
-   **History Deduplication:** Prevent duplicate consecutive entries in the history.
-   **History Size Limit:** Implement a configurable limit on the number of entries in the history.
-   **Contextual History:** Potentially filter history based on the current project or context.
-   **Fuzzy Matching:** Provide suggestions even if the user's input is not an exact prefix.
-   **Dynamic Suggestions:** For commands that operate on dynamic data (e.g., `/chat resume <name>`, suggest actual saved chat names).
-   **Visual Feedback:** Display suggestions in a clear, non-intrusive way (e.g., a small overlay or inline).
