# Active Features

**Last Updated:** 2025-07-10

This file tracks all active features and their current status. Features are now organized by their target version in dedicated directories under `.ai/ledgers/`.

## How to find features:

*   **V3.1 (MVP Chatbot Functionality):** See features in `/.ai/ledgers/v3.1/`
*   **V3.2 (Continuation Passing Style):** See features in `/.ai/ledgers/v3.2/`
*   **V3.3 (Advanced Reasoning):** See features in `/.ai/ledgers/v3.3/`

For a high-level overview of the roadmap, refer to `/.ai/ledgers/roadmap.md`.

---

## Status Definitions

- **🟢 In Progress**: Actively being developed
- **🔴 Up Next**: Ready to start, prioritized
- **🟡 Blocked**: Waiting for dependencies or decisions
- **🔵 Under Review**: Complete and awaiting review/approval
- **📋 Backlog**: Planned for future development

## Usage

1. **Starting a feature**: Move its ledger into the `v3.1` (or current target) directory.
2. **Blocked feature**: Add a note to its ledger.
3. **Completed feature**: Mark its status in the ledger as "Under Review".
4. **Approved feature**: Move its ledger to the `archived` directory (if not already in a versioned directory).

## Commands

```bash
# Create a new feature (adds to the current target version directory)
wrinkl feature my-new-feature

# List all features (will list by versioned directories)
wrinkl list

# Archive completed feature
wrinkl archive my-completed-feature
```

---

*This file serves as a high-level guide. Detailed feature tracking is now within versioned ledger directories.*
