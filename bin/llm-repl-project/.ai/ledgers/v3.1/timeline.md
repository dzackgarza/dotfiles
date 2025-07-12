# Sacred Timeline Implementation

**Branch:** feat/sacred-timeline
**Summary:** Implement the Sacred Timeline as the top area of the Sacred GUI architecture, containing completed conversation turns separated by hrules. This is the immutable historical record following the append-only Sacred Timeline principles.
**Status:** Planning
**Created:** 2025-07-10
**Updated:** 2025-07-12

## Context

### Problem Statement
The Sacred Timeline must be implemented as the top area of the Sacred GUI layout, containing only completed conversation turns in the format: User → Cognition → Assistant blocks, separated by hrules. This timeline represents the immutable historical record and must follow the Sacred Timeline principles of append-only integrity.

### Success Criteria
- [ ] Sacred Timeline as top VerticalScroll in Sacred GUI layout
- [ ] Displays completed turns: User → Cognition → Assistant with hrule separators
- [ ] Append-only integrity maintained (no editing/deletion of inscribed content)
- [ ] Simple block widgets only (no nested containers)
- [ ] Context management integration for LLM token limits

### User-Visible Behaviors
When this ledger is complete, the user will see:

1. **Sacred Timeline as top scroll area showing conversation history**
2. **Each completed turn shows User → Cognition → Assistant blocks**
3. **Horizontal rules visually separate conversation turns**
4. **No live/dynamic content - only static historical records**
5. **Smooth scrolling through conversation history**

## Technical Approach

### Architecture Changes
1. **SacredTimelineWidget**: Top VerticalScroll containing completed turns
2. **TurnBlockWidget**: Simple widgets for User/Cognition/Assistant blocks
3. **TurnSeparatorWidget**: hrule widgets between conversation turns
4. **TimelineHistoryManager**: Manages append-only operations
5. **ContextPruningManager**: Handles context window management

### Implementation Plan
1. **Phase 1: Planning** - Review and plan implementation
2. **Phase 2: Implementation** - Core development work
3. **Phase 3: Testing** - Testing and validation
4. **Phase 4: UX Polish** - Final polish and user experience improvements
5. **Phase 5: Integration** - Integrate ledger into the main system

## Implementation Details

The timeline feature will be implemented using the `Textual` library, which provides a powerful and flexible framework for creating terminal-based user interfaces. The timeline will be implemented as a custom `Textual` widget, which will be responsible for rendering the timeline and handling user input.

The timeline will be composed of a set of blocks, which will be represented as custom `Textual` widgets. Each block will be responsible for rendering a specific type of content, such as a message, a cognitive block, or a timer.

The timeline will be updated in real-time, as new messages and cognitive blocks are added to the conversation. The timeline will also support the dynamic transitioning of blocks between different states, which will be implemented using `Textual`'s reactive properties and data binding features.

### Formalizing the `TimelineBlock`

To ensure the integrity and consistency of the Sacred Timeline, all data inscribed upon it will conform to a strict `TimelineBlock` dataclass. This provides a clear, type-safe contract for every entry.

```python
# src/core/timeline_block.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Literal, Optional
import uuid

@dataclass
class TimelineBlock:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    role: Literal["user", "system", "assistant", "cognition", "error"]
    content: Any
    metadata: Dict[str, Any] = field(default_factory=dict)
    # Add other fields as needed, e.g., token_counts, wall_time_seconds
```

### Centralizing `TimelineManager` for Integrity

The `TimelineManager` will be responsible for enforcing the core principles of the Sacred Timeline: immutability and append-only. It will act as the single point of entry for adding new blocks, ensuring all blocks conform to the `TimelineBlock` structure.

```python
# src/core/timeline_manager.py
from typing import List, Callable
from src.core.timeline_block import TimelineBlock # Import the new dataclass

class TimelineManager:
    def __init__(self):
        self._blocks: List[TimelineBlock] = []
        self._observers: List[Callable[[TimelineBlock], None]] = []

    def add_block(self, block: TimelineBlock):
        # Enforce append-only: no modification or insertion
        # Add validation for TimelineBlock structure here
        if not isinstance(block, TimelineBlock):
            raise TypeError("Only TimelineBlock instances can be added to the timeline.")
        # Further validation (e.g., immutability checks if needed)

        self._blocks.append(block)
        for observer in self._observers:
            observer(block)

    def get_all_blocks(self) -> List[TimelineBlock]:
        return list(self._blocks) # Return a copy to prevent external modification

    def add_observer(self, observer: Callable[[TimelineBlock], None]):
        self._observers.append(observer)

    def remove_observer(self, observer: Callable[[TimelineBlock], None]):
        self._observers.remove(observer)

timeline = TimelineManager() # Maintain a singleton instance for global access
```

### Context Management Integration

The `TimelineManager` will expose methods and properties that allow the `MemoryAndContextManager` (from `memory-and-context-management.md`) to efficiently retrieve and prune timeline data for LLM context. This includes:

-   **`get_context_for_llm(max_tokens: int) -> List[TimelineBlock]`:** A method that returns a list of `TimelineBlock`s optimized for LLM context, respecting `max_tokens` and applying pruning strategies (e.g., recency, relevance, summarization) as defined in the `MemoryAndContextManager`.
-   **Metadata for Pruning:** `TimelineBlock`s will include metadata (e.g., `token_count`, `relevance_score`) to assist the context manager in making intelligent pruning decisions.

## Status

This feature is currently in the planning phase. The next steps are to:

1. Create a more detailed technical design for the timeline feature.
2. Implement a prototype of the timeline feature using the `Textual` library.
3. Integrate the timeline feature with the rest of the application.