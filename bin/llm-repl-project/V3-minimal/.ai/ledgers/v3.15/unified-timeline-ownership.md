# Unified Timeline Ownership

## Status: Not Started

## Overview
Refactor the timeline to be the single owner of all blocks, eliminating the dual LiveBlock/Timeline system that causes duplicate rendering, mixed state, and sub-block separation issues.

## Problem Statement
The current architecture has two competing systems:
- `LiveBlockManager` manages live, mutable blocks during processing
- `SacredTimeline` manages immutable, inscribed blocks

This causes:
- Blocks appearing in multiple places (as live blocks AND timeline blocks)
- Sub-blocks getting inscribed separately from their parents
- Confusing state transitions where blocks exist in both systems
- Race conditions and timing issues

## Solution Design
Create a unified `TimelineWidget` that owns both:
- **Above-fold blocks**: Immutable, inscribed blocks from the Sacred Timeline
- **Below-fold block**: Single transient block currently being processed

The timeline widget becomes the single source of truth for all blocks.

## User-Visible Behaviors

### 1. Single Rendering Location
**Current**: Blocks can appear as both live blocks and timeline blocks simultaneously
**New**: Each block appears in exactly one location in the UI

### 2. Clear Visual Boundary  
**Current**: No clear separation between processing and completed blocks
**New**: Visible "fold" line separates inscribed (above) from transient (below) blocks

### 3. No Block Jumping
**Current**: Blocks disappear from live area and reappear in timeline
**New**: Blocks smoothly transition from below-fold to above-fold

### 4. Consistent Sub-block Hierarchy
**Current**: Sub-blocks can be inscribed separately, breaking parent-child relationships
**New**: Sub-blocks always remain children of their parent block

### 5. Predictable Block Lifecycle
**Current**: Unclear when blocks transition from live to inscribed
**New**: Clear progression: Create below → Process → Inscribe above → Clear below

## Technical Implementation

### Remove LiveBlockManager
```python
# DELETE: src/core/live_blocks.py (LiveBlockManager class)
# The timeline will manage all blocks directly
```

### Extend TimelineWidget
```python
class TimelineWidget(Container):
    def __init__(self):
        super().__init__()
        self.above_fold_blocks: List[Block] = []  # Sacred Timeline blocks
        self.below_fold_block: Optional[TransientBlock] = None  # Active block
        self.fold_indicator = FoldIndicator()  # Visual separator
```

### Create Transient Block Container
```python
class TransientBlockContainer(Container):
    """Fixed container below the fold for active processing"""
    def __init__(self):
        super().__init__()
        self.active_block: Optional[TransientBlock] = None
```

## Acceptance Criteria

### Must Have
- [ ] LiveBlockManager completely removed
- [ ] Timeline widget owns all blocks
- [ ] No duplicate rendering of any block
- [ ] Sub-blocks never appear as top-level blocks
- [ ] Clear visual fold indicator

### Should Have  
- [ ] Smooth animations during transitions
- [ ] Auto-scroll to keep active block visible
- [ ] Proper handling of empty below-fold state

### Could Have
- [ ] Configurable fold position
- [ ] Different fold styles (line, gradient, gap)

## Test Plan

### Manual Testing
1. Start the app and enter a query
2. Verify only one cognition block appears (below fold)
3. Watch sub-blocks execute sequentially within parent
4. Confirm block moves above-fold when complete
5. Verify no duplicate blocks anywhere
6. Check that sub-blocks stay with parent

### Automated Testing
```python
def test_no_duplicate_blocks():
    """Ensure blocks only appear in one location"""
    
def test_sub_block_containment():
    """Verify sub-blocks remain with parents"""
    
def test_timeline_ownership():
    """Confirm timeline owns all blocks"""
```

## Dependencies
- Must complete before `transient-block-architecture`
- Blocks `cognition-block-refactor`

## Notes
This is the foundational refactor that enables all other improvements. It must be done carefully to avoid breaking existing functionality.