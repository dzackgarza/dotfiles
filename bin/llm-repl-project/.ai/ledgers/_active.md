# Active Features

**Last Updated:** 2025-07-09

This file tracks all active features and their current status. Use this as a dashboard to see what's in progress and what's coming up next.

## 🟢 In Progress

*Features currently being worked on*

- [Research Assistant Routing System](/home/dzack/dotfiles/bin/llm-repl-project/.ai/ledgers/research-assistant-routing.md) - Hybrid routing system for query classification

## 🔴 Up Next (Priority Order)

*Features ready to start, ordered by priority*

- [File Context Inclusion (@-commands)](/home/dzack/dotfiles/bin/llm-repl-project/.ai/ledgers/file-context-inclusion.md) - Include file/directory contents in prompts
- [Slash Commands System](/home/dzack/dotfiles/bin/llm-repl-project/.ai/ledgers/slash-commands.md) - Meta-level CLI control commands  
- [Shell Integration](/home/dzack/dotfiles/bin/llm-repl-project/.ai/ledgers/shell-integration.md) - Execute shell commands with security
- [Memory and Context Persistence](/home/dzack/dotfiles/bin/llm-repl-project/.ai/ledgers/memory-persistence.md) - Cross-session memory system

## 🟡 Blocked

*Features that are blocked and waiting for something*

<!-- Move features here when they're blocked -->

## 🔵 Under Review

*Features that are complete and under review*

<!-- Move features here when they're ready for review -->

## 📋 Backlog

*Features planned for future development*

**Core Extensions:**
- [Model Task Optimization](/home/dzack/dotfiles/bin/llm-repl-project/.ai/ledgers/model-task-optimization.md) - Differential model routing for optimal performance
- [MCP Integration](/home/dzack/dotfiles/bin/llm-repl-project/.ai/ledgers/mcp-integration.md) - Model Context Protocol server support
- [Multimodal Support](/home/dzack/dotfiles/bin/llm-repl-project/.ai/ledgers/multimodal-support.md) - Images, PDFs, rich media input
- [Web Search and Fetch Tools](/home/dzack/dotfiles/bin/llm-repl-project/.ai/ledgers/web-tools.md) - Real-time web information

**Roadmap Phases:**
- [Tool Execution Foundation (v3.1)](/home/dzack/dotfiles/bin/llm-repl-project/.ai/ledgers/roadmap.md) - Q1 2025
- [Continuation Passing Style (v3.2)](/home/dzack/dotfiles/bin/llm-repl-project/.ai/ledgers/roadmap.md) - Q2 2025
- [Advanced Reasoning (v3.3)](/home/dzack/dotfiles/bin/llm-repl-project/.ai/ledgers/roadmap.md) - Q3 2025
- [Production Ready (v4.0)](/home/dzack/dotfiles/bin/llm-repl-project/.ai/ledgers/roadmap.md) - Q4 2025

---

## Status Definitions

- **🟢 In Progress**: Actively being developed
- **🔴 Up Next**: Ready to start, prioritized
- **🟡 Blocked**: Waiting for dependencies or decisions
- **🔵 Under Review**: Complete and awaiting review/approval
- **📋 Backlog**: Planned for future development

## Usage

1. **Starting a feature**: Move from "Up Next" to "In Progress"
2. **Blocked feature**: Move to "Blocked" with reason
3. **Completed feature**: Move to "Under Review"
4. **Approved feature**: Archive using `wrinkl archive <feature-name>`

## Commands

```bash
# Create a new feature (adds to "Up Next")
wrinkl feature my-new-feature

# List all features
wrinkl list

# Archive completed feature
wrinkl archive my-completed-feature
```

---

*Keep this file updated as features progress through different stages.*
