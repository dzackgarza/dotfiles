# clean_history README

## Overview
`clean_history` is a research-backed tool for cleaning and deduplicating zsh history files. It removes multiline and noisy commands, deduplicates both exact and similar commands using fuzzy matching, and outputs a file optimized for Ctrl+R and FZF usability.

## Features
- Removes multiline and complex commands
- Removes trivial/noisy commands (configurable)
- Deduplicates both exact and similar commands (fuzzy matching, configurable threshold)
- Keeps only the most recent occurrence of each command
- Output is compatible with zsh Ctrl+R and FZF search

## Usage
1. **Extract single-line, non-trivial commands:**
   ```sh
   python3 extract_singleline_history.py
   # Input: zsh_history_testcopy, Output: zsh_history_testcopy_extracted
   ```
2. **Deduplicate similar commands:**
   ```sh
   python3 dedup_fuzzy_history.py
   # Input: zsh_history_testcopy_extracted, Output: zsh_history_testcopy_deduped
   ```
3. **(Optional) Replace your history file:**
   ```sh
   cp zsh_history_testcopy_deduped ~/.zsh_history_clean
   ```

## Configuration
- Edit `NOISE` in `extract_singleline_history.py` to change which commands are ignored.
- Edit `SIMILARITY_THRESHOLD` in `dedup_fuzzy_history.py` to adjust fuzzy deduplication strictness.

## Quality Checklist
See `clean_history_quality_checklist.md` for validation steps and QA results.

## Research & References
- [Shell history best practices](https://martinheinz.dev/blog/110)
- [zsh-history-analysis](https://github.com/bamos/zsh-history-analysis)
- [Deduplication scripts](https://stackoverflow.com/questions/72293670/delete-duplicate-commands-of-zsh-history-keeping-last-occurence)

## Decision Log & Lessons Learned
See `clean_history_project_plan.md` for project plan, decision log, and lessons learned.

## License
MIT
