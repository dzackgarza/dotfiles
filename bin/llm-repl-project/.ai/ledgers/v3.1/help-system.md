
# Ledger: Dynamic Help System

**Goal:** To implement a comprehensive and dynamic help system that provides context-aware assistance to the user, including a dedicated help overlay and integration with command discovery.

## 1. Core Philosophy

- **Discoverability:** Users should be able to easily discover all available commands, their usage, and keybindings.
- **Context-Aware:** The help system should reflect the current state of the application, including dynamically loaded plugins and context-specific information.
- **Self-Documenting:** Plugins should contribute their own help text, making the system easy to maintain and ensuring accuracy.

## 2. Core Functionality

### 2.1. Dynamic `/help` Command

#### Feature

- A `/help` command that lists all available commands, their descriptions, and usage examples.

#### Implementation Details

1.  **Command Registration:**
    -   All core commands (e.g., `/clear`, `/quit`, `/chat`) will register themselves with a central `HelpRegistry`.
    -   Plugins (including the new ones like `/corpus`, `/edit`, `/mcp`) will also register their commands and subcommands with the `HelpRegistry`.
2.  **Help Text Structure:**
    -   Each registered command will provide:
        -   `name`: The command name (e.g., `clear`, `corpus search`).
        -   `description`: A brief explanation of what the command does.
        -   `usage`: A short example of how to use the command.
        -   `category`: A category for grouping related commands (e.g., `Core`, `File System`, `AI`).
3.  **Dynamic Generation:**
    -   When `/help` is invoked, the `HelpRegistry` will gather all registered commands.
    -   It will then format this information into a readable output, grouped by category.

### 2.2. Help Overlay

#### Feature

- An accessible help system, triggered by `Ctrl+?` (or a similar intuitive keybinding), that displays keybindings and basic usage information in an overlay.

#### Implementation Details

1.  **`HelpOverlay` Widget:**
    -   Design `HelpOverlay` widget layout and content.
    -   Implement logic to dynamically populate keybindings from the `HelpRegistry`.
2.  **Overlay Management:**
    -   Add a global keybinding (`Ctrl+?`) to `LLMReplApp` to toggle the overlay.
    -   Ensure overlay respects `Esc` for closing (leveraging `ui-navigation-principles.md`).
    -   The overlay should be visually distinct and not interfere with the main interface.

## 3. Advanced Features

-   **Contextual Help:** `/help <command_name>` to get detailed help for a specific command.
-   **Searchable Help:** Allow users to search the help text for keywords.
-   **Interactive Help:** A Textual-based interactive help browser that allows users to navigate through commands and examples.
