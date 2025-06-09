# NOTE: This extension is only for Cursor, not for general VS Code use.

# Cursor Markdown Webview Extension

## Current Functionality

- Adds a command to Cursor's command palette: **Show Markdown Webview**
- When run on a Markdown file, opens a webview that renders the file using Pandoc (with all standard Pandoc markdown features)
- The extension is symlinked from this dotfiles directory for version control

## Instructions for LLM Contributors

- **Implement one tiny feature at a time.**
- **After every successful change, make a git commit.**
- **If a regression is detected, use git to roll back to the last working state.**
- **Always test that the extension loads and the main command works after each change.**
- **Do not attempt to implement large features in a single commit.**

## Ultimate Project Goal

- **Goal:** Implement either:
  - A WYSIWYG Markdown editor (like Typora) within Cursor, OR
  - A scroll-synced, side-by-side Markdown viewer (edit on left, Pandoc-rendered preview on right)
- **Requirements:**
  - Must use Pandoc for all Markdown rendering
  - Should support all Pandoc features, including math and tables
  - Should be visually modern and easy to use

---

**For new LLMs:**

- Read this README before making changes.
- Always work incrementally and use version control for every step.
