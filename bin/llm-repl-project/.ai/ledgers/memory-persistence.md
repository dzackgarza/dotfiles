# Feature: Memory and Context Persistence

**Created:** 2025-07-10
**Status:** 🔴 Up Next
**Priority:** Medium

## Overview

Implement a hierarchical memory system that allows the AI to maintain context across sessions and provides users with control over what the AI remembers.

## Goals

- Support project-specific context (GEMINI.md / CLAUDE.md style)
- Enable cross-session memory persistence
- Allow dynamic memory updates during conversation
- Implement hierarchical context loading

## Technical Approach

### Memory Types

1. **Hierarchical Project Context**
   - Global: `~/.llm-repl/MEMORY.md`
   - Project: `./MEMORY.md` or `./CLAUDE.md`
   - Directory: `./src/MEMORY.md`
   - Merged hierarchically (most specific wins)

2. **Session Memory**
   - Save important facts during conversation
   - `/memory add <text>` - Add to memory
   - `/memory show` - Display current memory
   - `/memory refresh` - Reload from files

3. **Conversation Checkpoints**
   - Save entire conversation state
   - Resume from checkpoints
   - Branch conversations

### Implementation Structure

```python
class MemorySystem:
    def __init__(self):
        self.hierarchical_memory = HierarchicalMemory()
        self.session_memory = SessionMemory()
        self.checkpoints = CheckpointManager()
    
    def load_context(self, path: Path) -> str:
        """Load hierarchical context from current path"""
        contexts = []
        # Walk up directory tree collecting MEMORY.md files
        # Merge with global context
        return self.merge_contexts(contexts)
    
    def save_memory(self, key: str, value: str):
        """Save to session memory"""
        self.session_memory.add(key, value)
    
    def checkpoint(self, tag: str):
        """Save conversation checkpoint"""
        self.checkpoints.save(tag, self.get_full_context())
```

### File Format

```markdown
# Project Context

## Overview
This project is a CLI tool for...

## Conventions
- Use functional programming style
- All errors should fail fast

## Current Focus
Working on implementing shell integration
```

## Success Criteria

- [ ] Hierarchical context loading
- [ ] Dynamic memory commands
- [ ] Conversation checkpointing
- [ ] Memory persistence across sessions
- [ ] Clear memory management UI

## Future Enhancements

- Vector database for semantic search
- Automatic context summarization
- Memory decay/importance scoring
- Integration with external knowledge bases
- Shared team memory spaces