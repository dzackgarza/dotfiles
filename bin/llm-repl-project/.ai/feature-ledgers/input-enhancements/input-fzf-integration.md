# Feature: Fzf Integration for Enhanced Search

## Overview

This feature integrates the `fzf` fuzzy finder into the Textual application, providing powerful, interactive search capabilities for command history, file system navigation, and other custom data sources. It leverages Textual's `App.suspend()` method to seamlessly hand over terminal control to `fzf`.

## Sub-Features and User Tests

### 1. Fuzzy History Search (Ctrl+R)

**Description:** Users can press `Ctrl+R` to launch an `fzf` interface pre-populated with their command history, allowing for quick fuzzy searching and selection of past commands.

**User Stories:**
- As a user, I can quickly find and re-execute a command from my history, even if I only remember parts of it.
- As a user, the history search should be interactive and responsive, similar to a standard shell.

**End-to-End User Tests:**
- **Test 1.1 (Basic History Search and Selection):**
    - **Precondition:** The command history contains at least 5 entries (e.g., `ls -la`, `git status`, `python my_script.py`, `docker ps`, `kubectl get pods`).
    - **Action:** User presses `Ctrl+R` in the input box. The `fzf` interface appears. User types `py`.
    - **Expected Outcome:** `fzf` displays `python my_script.py` as a filtered result. User presses `Enter`. The `fzf` interface closes, and `python my_script.py` is inserted into the Textual input box.
- **Test 1.2 (History Search - No Match):**
    - **Precondition:** The command history is populated.
    - **Action:** User presses `Ctrl+R`. In `fzf`, user types `nonexistentcommand`.
    - **Expected Outcome:** `fzf` shows no matching results. User presses `Escape`. The `fzf` interface closes, and the Textual input box remains unchanged.
- **Test 1.3 (History Search - Empty History):**
    - **Precondition:** The command history is empty.
    - **Action:** User presses `Ctrl+R`.
    - **Expected Outcome:** `fzf` launches but shows no entries. User presses `Escape`. The Textual input box remains unchanged.

### 2. Fuzzy Directory Search (Ctrl+T)

**Description:** Users can press `Ctrl+T` to launch an `fzf` interface pre-populated with a list of directories (e.g., recently accessed, common project directories), allowing for quick navigation.

**User Stories:**
- As a user, I can quickly change to a frequently used directory without typing its full path.
- As a user, the directory search should be interactive and allow fuzzy matching.

**End-to-End User Tests:**
- **Test 2.1 (Basic Directory Search and Selection):**
    - **Precondition:** The system has access to a list of directories (e.g., `/home/user/projects/my_app`, `/home/user/docs`, `/tmp`).
    - **Action:** User presses `Ctrl+T` in the input box. The `fzf` interface appears. User types `myap`.
    - **Expected Outcome:** `fzf` displays `/home/user/projects/my_app` as a filtered result. User presses `Enter`. The `fzf` interface closes, and `cd /home/user/projects/my_app` (or just the path, depending on desired behavior) is inserted into the Textual input box.
- **Test 2.2 (Directory Search - No Match):**
    - **Precondition:** The directory list is populated.
    - **Action:** User presses `Ctrl+T`. In `fzf`, user types `nonexistentdir`.
    - **Expected Outcome:** `fzf` shows no matching results. User presses `Escape`. The Textual input box remains unchanged.

### 3. General System for Custom Fzf Searches

**Description:** Provide a flexible mechanism for developers to define new `Ctrl+?` keybindings that trigger `fzf` searches over custom data sources (e.g., bibliography entries, PDF documents, code snippets).

**User Stories:**
- As a developer, I can easily add new `fzf`-powered search commands for specific data types relevant to my application.
- As a user, I can discover and use specialized `fzf` searches for different types of content.

**End-to-End User Tests:**
- **Test 3.1 (Custom Fzf Search - Bibliography):**
    - **Precondition:** A custom `Ctrl+B` keybinding is defined to search a bibliography database. The database contains entries like "Einstein, A. (1905). On the Electrodynamics of Moving Bodies."
    - **Action:** User presses `Ctrl+B` in the input box. The `fzf` interface appears, pre-populated with bibliography entries. User types `einstein electro`.
    - **Expected Outcome:** `fzf` displays the relevant bibliography entry. User presses `Enter`. The selected entry (or a formatted citation) is inserted into the Textual input box.
- **Test 3.2 (Custom Fzf Search - PDF Documents):**
    - **Precondition:** A custom `Ctrl+P` keybinding is defined to search a collection of PDF documents by filename or metadata. The collection contains `Quantum_Mechanics_Textbook.pdf`.
    - **Action:** User presses `Ctrl+P` in the input box. The `fzf` interface appears. User types `quantum`.
    - **Expected Outcome:** `fzf` displays `Quantum_Mechanics_Textbook.pdf`. User presses `Enter`. The selected PDF path (or a command to open it) is inserted into the Textual input box.
- **Test 3.3 (Custom Fzf Search - No Data):**
    - **Precondition:** A custom `Ctrl+X` keybinding is defined for a search with an empty data source.
    - **Action:** User presses `Ctrl+X`.
    - **Expected Outcome:** `fzf` launches but shows no entries. User presses `Escape`. The Textual input box remains unchanged.
