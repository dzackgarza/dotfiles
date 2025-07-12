# V3.15: Timeline Architecture Refactor

## Overview
V3.15 is a fundamental architectural refactor that eliminates the dual LiveBlock/Timeline system in favor of a unified spatial model with clear separation between processing (below-fold) and history (above-fold).

## Problem Statement
The current architecture has two competing systems (LiveBlockManager and SacredTimeline) trying to manage the same blocks, causing:
- Duplicate rendering (blocks appear in multiple places)
- Sub-blocks escaping their parent containers
- Mixed state confusion
- Progress tracking failures
- Timing display issues
- First sub-block visibility problems

## Solution
Implement a unified timeline that owns all blocks, with clear spatial separation:
- **Above-fold**: Immutable history (Sacred Timeline)
- **Below-fold**: Single transient block being processed
- **The fold**: Visual boundary between them

## Ledgers

### 1. [unified-timeline-ownership](unified-timeline-ownership.md)
**Status**: Not Started  
**Purpose**: Make TimelineWidget the single owner of all blocks  
**Key Change**: Remove LiveBlockManager entirely

### 2. [transient-block-architecture](transient-block-architecture.md)
**Status**: Not Started  
**Purpose**: Create clear separation between mutable processing and immutable history  
**Key Change**: Replace LiveBlock with TransientBlock

### 3. [spatial-timeline-rendering](spatial-timeline-rendering.md)
**Status**: Not Started  
**Purpose**: Implement visual above/below fold separation  
**Key Change**: Fixed below-fold area for active processing

### 4. [atomic-inscription-system](atomic-inscription-system.md)
**Status**: Not Started  
**Purpose**: Move complete block structures atomically from below to above fold  
**Key Change**: Transaction-based inscription with rollback

### 5. [cognition-block-refactor](cognition-block-refactor.md)
**Status**: Not Started  
**Purpose**: Fix cognition blocks to work with new architecture  
**Key Change**: CognitionTransientBlock with proper sub-block containment

## Implementation Order
Must be done in sequence:
1. `unified-timeline-ownership` - Foundation
2. `transient-block-architecture` - Core abstraction
3. `spatial-timeline-rendering` - Visual framework
4. `atomic-inscription-system` - State transitions
5. `cognition-block-refactor` - Apply to cognition

## Expected Outcomes
- No more duplicate blocks
- Sub-blocks always contained in parents
- Clear visual separation of processing vs complete
- Accurate progress and timing
- Predictable block lifecycle
- Better user understanding of system state

## Success Metrics
- Zero duplicate renders
- 100% sub-block containment
- All timing data preserved
- Smooth visual transitions
- No "lost" or "hidden" blocks

## Risks and Mitigations
- **Risk**: Major refactor could break existing features
- **Mitigation**: Implement incrementally with tests

- **Risk**: Performance impact from new architecture
- **Mitigation**: Profile and optimize hot paths

- **Risk**: Visual changes confuse users
- **Mitigation**: Clear visual design and animations

## Notes
This refactor addresses the root cause of numerous bugs we've been seeing. By having a single owner for all blocks and clear spatial separation, we eliminate entire classes of state management issues.