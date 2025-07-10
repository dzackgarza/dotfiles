# clean_history Project Plan (Research-Backed)

## Objective
Create a robust, research-backed script to clean and deduplicate zsh history files, optimizing for Ctrl+R usability and advanced similarity-based deduplication.

## Research Sources
- https://martinheinz.dev/blog/110 (Shell history best practices)
- https://github.com/bamos/zsh-history-analysis (Advanced history analysis)
- https://stackoverflow.com/questions/72293670/delete-duplicate-commands-of-zsh-history-keeping-last-occurence (Deduplication scripts)

## Key Features
- Remove multiline and complex commands
- Remove trivial/noisy commands (configurable)
- Deduplicate both exact and similar commands (fuzzy matching)
- Keep only the most recent occurrence
- Output a cleaned file compatible with zsh Ctrl+R and FZF

## Workflow & Checkpoints
1. **Requirements & Research** (done)
2. **Design & Planning** (this doc)
3. **Implement Extraction & Filtering**
   - Extract single-line commands
   - Remove noise (e.g., trivial commands)
   - Checkpoint: Validate extraction on sample and real data
4. **Implement Deduplication**
   - Exact deduplication (keep most recent)
   - Fuzzy/similarity deduplication (tunable threshold)
   - Checkpoint: Validate deduplication on test and real data
5. **Output & Usability Validation**
   - Ensure output works with Ctrl+R, FZF, and zsh
   - Checkpoint: Manual and automated search tests
6. **Testing & Quality Assurance**
   - Unit tests for extraction, filtering, deduplication
   - Regression tests on real history files
   - Checkpoint: All tests pass, no data loss
7. **Documentation & Handoff**
   - Document usage, options, and design decisions
   - Prepare handoff package (README, changelog, sources)

## Validation Steps
- Compare before/after history for loss, noise, and usability
- Test with zsh Ctrl+R and FZF
- Peer/code review (if available)

## Progress Tracker
- [x] Research & requirements
- [x] Initial implementation
- [ ] Extraction/Filtering validation
- [ ] Deduplication validation
- [ ] Usability validation
- [ ] Documentation
- [ ] Handoff

## Issue Log
- [ ] Awk RS compatibility (solved by Python extraction)
- [ ] Fuzzy deduplication threshold tuning
- [ ] Handling of edge cases (e.g., commands with semicolons)

## Quality Checklist
- [ ] No multiline or complex commands in output
- [ ] No trivial/noisy commands (unless user wants)
- [ ] No duplicate or highly similar commands
- [ ] Output is compatible with zsh/FZF search
- [ ] Script is documented and configurable

## Handoff Documentation
- README with usage, options, and design rationale
- Changelog with all major changes and decisions
- Citations for all research and best practices

---
# Decision Log
- Use Python for extraction and deduplication for reliability and flexibility
- Use rapidfuzz for similarity-based deduplication
- Follow zsh/FZF best practices for usability
- Make noise filtering and deduplication threshold configurable

# Lessons Learned
- Awk RS is not portable for regex; Python is more robust
- Fuzzy deduplication is rare but valuable for usability
- Usability is best validated with real-world search (Ctrl+R, FZF)
