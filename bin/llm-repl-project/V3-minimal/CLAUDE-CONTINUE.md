# CLAUDE-CONTINUE.md

## Current State (After 2+ hours of bug fixes)

### What We Tried
We spent significant time trying to fix the cognition sub-module implementation:
1. Modified sub-modules to use parent block's cognition_progress
2. Added timing tracking to sub-blocks
3. Fixed progress updates to reach 100%
4. Updated display methods to show real-time progress

### What's Still Broken
Despite these fixes, fundamental architectural issues remain:
- **Mixed rendering**: Sub-blocks appear both inside cognition blocks AND separately in timeline
- **Inconsistent containment**: Only 2 of 3 sub-blocks render within parent initially
- **Duplicate blocks**: Same content appears in multiple places
- **State confusion**: Live blocks and timeline blocks coexist awkwardly

### Root Cause Identified
The problem isn't in the implementation details - it's in the architecture. We have two competing systems:
- `LiveBlockManager` managing mutable, real-time blocks
- `SacredTimeline` managing immutable, historical blocks

These systems don't compose cleanly, leading to:
- Sub-blocks being inscribed independently (breaking containment)
- Confusion about who owns what data
- Complex transformation logic that loses information
- No clear lifecycle for blocks

## Architectural Solution: V3.15

### Core Insight
The UI naturally has two areas:
- **Above the fold**: Inscribed history (scrollable, immutable)
- **Below the fold**: Active processing (fixed position, mutable)

The Timeline should own BOTH areas, eliminating the dual-system confusion.

### Key Changes Required

1. **Unified Ownership**
   - Delete LiveBlockManager entirely
   - TimelineWidget owns all blocks
   - Single source of truth

2. **Spatial Separation**
   - Above-fold: Sacred Timeline (immutable Block objects)
   - Below-fold: Single TransientBlock being processed
   - Visual fold indicator between them

3. **Clean Block Lifecycle**
   - Create TransientBlock below-fold
   - Process with real-time updates
   - Atomically inscribe entire structure above-fold
   - Clear below-fold

4. **Proper Containment**
   - Sub-blocks NEVER exist independently
   - They're always part of their parent
   - Inscription preserves exact structure

### Implementation Plan

See `.ai/ledgers/v3.15/` for detailed implementation ledgers:

1. **[unified-timeline-ownership.md](../../../.ai/ledgers/v3.15/unified-timeline-ownership.md)**
   - Remove LiveBlockManager
   - Make Timeline the single owner

2. **[transient-block-architecture.md](../../../.ai/ledgers/v3.15/transient-block-architecture.md)**
   - Replace LiveBlock with TransientBlock
   - Clear separation of mutable vs immutable

3. **[spatial-timeline-rendering.md](../../../.ai/ledgers/v3.15/spatial-timeline-rendering.md)**
   - Visual above/below fold separation
   - Fixed below-fold area

4. **[atomic-inscription-system.md](../../../.ai/ledgers/v3.15/atomic-inscription-system.md)**
   - Move entire structures atomically
   - Transaction-based with rollback

5. **[cognition-block-refactor.md](../../../.ai/ledgers/v3.15/cognition-block-refactor.md)**
   - Fix cognition to use new architecture
   - Ensure proper sub-block containment

### Why This Fixes Everything

The current bugs all stem from having two systems fighting over the same data:
- **Duplicate rendering** → Single owner, single location
- **Lost sub-blocks** → Atomic inscription preserves structure
- **Timing issues** → Clear lifecycle with proper state tracking
- **Progress failures** → TransientBlock owns its complete state

### Next Steps

1. **DO NOT** continue patching the current system - it's fundamentally broken
2. **DO** implement V3.15 ledgers in order
3. **TEST** each ledger thoroughly before moving to the next
4. **EXPECT** this to be a significant refactor but worth it

### Key Principle

> "The Timeline owns everything. Blocks are either above the fold (inscribed in history) or below the fold (actively processing). There is no other state."

This eliminates the entire class of ownership and lifecycle bugs we've been fighting.

## Migration Notes

When implementing V3.15:
- All `LiveBlock` code will be removed
- `AsyncInputProcessor` will create `TransientBlock` instances
- UI widgets will need updates for new callbacks
- Tests will need updates for new architecture

The end result will be a much cleaner, more predictable system that matches users' mental model of how the timeline works.