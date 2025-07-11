
# Ledger: File Editing System

**Goal:** To implement a safe, transparent, and intelligent file editing system that leverages Unix-style patching and provides a beautiful visual diff view for user review.

## 1. Core Philosophy

- **Safety First:** Prevent accidental data loss by using patch-based editing and user confirmation.
- **Transparency:** Clearly show proposed changes before they are applied.
- **Reliability:** Leverage robust Unix tools (`diff`, `patch`) for accurate and consistent modifications.
- **Intelligence:** Utilize LLMs to generate precise changes and resolve conflicts.

## 2. Core Functionality

### 2.1. Principled File Editing with Unix-Style Patching

#### Feature

- A `/edit <file_path> "instruction for change"` command that generates and applies Unix-style patches.
- The plugin will not directly write to the file. Instead, it will:
    1.  Read the target file.
    2.  Provide the file's content and the user's instruction to an LLM.
    3.  Instruct the LLM to generate a `diff -u` style patch as its output.
    4.  Present the patch to the user for review and confirmation.
    5.  Upon confirmation, apply the patch to the original file.

#### Implementation Details

1.  **Prompt Engineering:** Carefully construct the prompt to the LLM to ensure it produces a valid `diff -u` formatted patch.
2.  **Patch Generation:** The LLM will generate the patch text.
3.  **Patch Validation & Preview:** Optionally run `patch --dry-run` to verify the patch and display it to the user with syntax highlighting.
4.  **User Confirmation:** Prompt the user to confirm the patch application.
5.  **Patch Application:** Apply the patch using the `patch` command-line utility. Notify the user if the patch fails to apply.

### 2.2. Unix Patching Tools Integration

#### Feature

- Implement file modification by generating and applying patches using standard Unix patching tools (`diff`, `patch`).

#### Implementation Details

-   Modify the LLM prompting strategy to request diffs.
-   Implement a Python wrapper for `diff` and `patch` utilities (using `subprocess`).
-   Develop logic for conflict detection and resolution (initial: report conflict, later: interactive resolution).

### 2.3. Intelligent and Beautiful Diff View

#### Feature

- Provide a visually appealing and intelligent diff view for proposed file changes, enhancing transparency and user review within the TUI.

#### Implementation Details

-   **`DiffViewer` Widget:** New Textual widget to display side-by-side or unified diffs.
-   **Syntax Highlighting:** Support syntax highlighting within the diff view for code changes (leveraging `rich-content-display-engine.md`).
-   **User Interaction:** Provide options to accept or reject changes directly from the diff view.

## 3. Advanced Features

-   **Multi-file Edits:** Extend the command to accept multiple file paths and generate a single, multi-file patch.
-   **Interactive Patching:** Allow the user to accept or reject individual hunks within a patch.
-   **Conflict Resolution:** If a patch fails to apply, the AI could be invoked again to try and resolve the conflict by re-generating the patch against the new file content.
-   **Revert Patches:** Ability to revert previously applied patches.
