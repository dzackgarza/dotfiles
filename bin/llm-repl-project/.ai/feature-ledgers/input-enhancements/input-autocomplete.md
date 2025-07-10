# Feature: Input Autocomplete

## Overview

This feature provides intelligent autocomplete suggestions within the main application input box, enhancing user productivity by reducing typing and guiding command entry. It leverages the `textual-autocomplete` library to display context-aware suggestions for commands, arguments, and history.

## Sub-Features and User Tests

### 1. Core Autocomplete Functionality

**Description:** Integrate the `textual-autocomplete` library with the main `Input` widget to display a dropdown list of suggestions as the user types.

**User Stories:**
- As a user, when I start typing a command, I should see relevant suggestions appear below the input box.
- As a user, I can navigate the suggestions using arrow keys and select one to complete my input.

**End-to-End User Tests:**
- **Test 1.1 (Command Suggestion):**
    - **Precondition:** The input box is empty.
    - **Action:** User types `g`.
    - **Expected Outcome:** A dropdown appears below the input box, suggesting commands starting with `g` (e.g., `git`, `grep`, `generate`). User can press `Down Arrow` to highlight `git` and `Enter` to complete the input to `git`.
- **Test 1.2 (Filtering Suggestions):**
    - **Precondition:** The input box is empty.
    - **Action:** User types `pyt`.
    - **Expected Outcome:** The dropdown shows suggestions like `python`, `pytest`, `pylint`, filtering out irrelevant commands.
- **Test 1.3 (No Suggestions):**
    - **Precondition:** The input box is empty.
    - **Action:** User types `xyzzy` (a non-existent command).
    - **Expected Outcome:** No dropdown appears, or an empty dropdown is shown, indicating no matching suggestions.

### 2. Context-Aware Suggestions

**Description:** Provide dynamic suggestions based on the current input context, including command arguments, file system paths, and command history.

**User Stories:**
- As a user, when I type a command followed by a space, I should see suggestions relevant to that command's arguments or common next steps.
- As a user, when I'm typing a file path, the system should suggest directories and files.

**End-to-End User Tests:**
- **Test 2.1 (File Path Completion):**
    - **Precondition:** The input box is empty. The current directory contains `src/` and `README.md`.
    - **Action:** User types `ls src/`.
    - **Expected Outcome:** The dropdown suggests contents of the `src/` directory (e.g., `src/main.py`, `src/utils/`).
- **Test 2.2 (Git Subcommand Completion):**
    - **Precondition:** The input box is empty.
    - **Action:** User types `git ` (with a trailing space).
    - **Expected Outcome:** The dropdown suggests common Git subcommands (e.g., `add`, `commit`, `status`, `branch`).
- **Test 2.3 (History-Based Completion):**
    - **Precondition:** The command history contains `python my_script.py`.
    - **Action:** User types `pyt`.
    - **Expected Outcome:** The dropdown includes `python my_script.py` as a suggestion, alongside other `pyt`-starting commands.
- **Test 2.4 (Dynamic Argument Completion):**
    - **Precondition:** The input box is empty. A mock tool `mytool` exists with a subcommand `config` that takes arguments `user` and `host`.
    - **Action:** User types `mytool config ` (with a trailing space).
    - **Expected Outcome:** The dropdown suggests `user` and `host` as possible arguments.

### 3. Fuzzy Matching for Suggestions

**Description:** Suggestions will be filtered using fuzzy matching, allowing users to find commands or items even with typos or partial, non-sequential input.

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
