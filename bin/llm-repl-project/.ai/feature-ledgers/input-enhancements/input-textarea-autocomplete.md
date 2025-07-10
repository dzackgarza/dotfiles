# Feature: TextArea Autocomplete

## Overview

This feature provides intelligent autocomplete suggestions for the application's primary input box, which will be implemented using `textual.widgets.TextArea`. The goal is to offer context-aware suggestions for commands, arguments, and history, while leveraging `TextArea`'s advanced editing capabilities like multi-line input and syntax highlighting.

## Sub-Features and User Tests

### 1. Autocomplete Suggestion Display

**Description:** Implement a mechanism to display a dropdown list of suggestions below the `TextArea` as the user types. This will require either adapting an existing library (like `textual-autocomplete`) or building a custom solution that integrates seamlessly with `TextArea`'s text management.

**User Stories:**
- As a user, when I start typing in the input box, I should see relevant suggestions appear below it.
- As a user, I can navigate the suggestions using arrow keys and select one to complete my input.

**End-to-End User Tests:**
- **Test 1.1 (Basic Command Suggestion):**
    - **Precondition:** The `TextArea` is empty.
    - **Action:** User types `g`.
    - **Expected Outcome:** A dropdown appears below the `TextArea`, suggesting commands starting with `g` (e.g., `git`, `grep`, `generate`). User can press `Down Arrow` to highlight `git` and `Enter` to complete the input to `git`.
- **Test 1.2 (Filtering Suggestions):**
    - **Precondition:** The `TextArea` is empty.
    - **Action:** User types `pyt`.
    - **Expected Outcome:** The dropdown shows suggestions like `python`, `pytest`, `pylint`, filtering out irrelevant commands.
- **Test 1.3 (No Suggestions):**
    - **Precondition:** The `TextArea` is empty.
    - **Action:** User types `xyzzy` (a non-existent command).
    - **Expected Outcome:** No dropdown appears, or an empty dropdown is shown, indicating no matching suggestions.

### 2. Context-Aware Suggestions for TextArea

**Description:** Provide dynamic suggestions based on the current input context within the `TextArea`, including command arguments, file system paths, and command history. This will require parsing `TextArea`'s content to determine context.

**User Stories:**
- As a user, when I type a command followed by a space, I should see suggestions relevant to that command's arguments or common next steps.
- As a user, when I'm typing a file path, the system should suggest directories and files.

**End-to-End User Tests:**
- **Test 2.1 (File Path Completion):**
    - **Precondition:** The `TextArea` is empty. The current directory contains `src/` and `README.md`.
    - **Action:** User types `ls src/`.
    - **Expected Outcome:** The dropdown suggests contents of the `src/` directory (e.g., `src/main.py`, `src/utils/`).
- **Test 2.2 (Git Subcommand Completion):**
    - **Precondition:** The `TextArea` is empty.
    - **Action:** User types `git ` (with a trailing space).
    - **Expected Outcome:** The dropdown suggests common Git subcommands (e.g., `add`, `commit`, `status`, `branch`).
- **Test 2.3 (History-Based Completion):**
    - **Precondition:** The command history contains `python my_script.py`.
    - **Action:** User types `pyt`.
    - **Expected Outcome:** The dropdown includes `python my_script.py` as a suggestion, alongside other `pyt`-starting commands.

### 3. Fuzzy Matching for TextArea Suggestions

**Description:** Suggestions will be filtered using fuzzy matching, allowing users to find commands or items even with typos or partial, non-sequential input within the `TextArea`.

**User Stories:**
- As a user, I can find a command even if I don't type its exact beginning, or if I make a small typo.

**End-to-End User Tests:**
- **Test 3.1 (Fuzzy Command Matching):**
    - **Precondition:** The command `generate_report` exists.
    - **Action:** User types `genrep`.
    - **Expected Outcome:** The dropdown suggests `generate_report` as a top match, even though the input is not a direct prefix.
- **Test 3.2 (Fuzzy Path Matching):**
    - **Precondition:** A file `src/utils/helper_functions.py` exists.
    - **Action:** User types `s/u/h_f`.
    - **Expected Outcome:** The dropdown suggests `src/utils/helper_functions.py` as a match.
