# Unified Timeline Ownership

**Branch:** feat/unified-timeline-ownership
**Summary:** Resolve fundamental architectural conflict between LiveBlock system and Timeline by establishing clear ownership model and atomic state transitions
**Status:** Planning  
**Created:** 2025-07-12
**Updated:** 2025-07-12

## Context

### Problem Statement

From architectural analysis report:
> "The fundamental issue is we have two separate systems trying to manage the same data:
> 1. LiveBlock system - Creates live blocks with real-time updates, manages sub-blocks
> 2. Timeline system - Expects immutable blocks with sub-blocks already complete"

This creates:
- **No clear ownership model** - Who owns sub-blocks? LiveBlock? Timeline? Both?
- **Mixed responsibilities** - LiveBlockManager manages both live updates AND timeline persistence
- **Impedance mismatch** - Live blocks are mutable with real-time updates, Timeline expects immutable snapshots
- **No proper state machine** - Blocks transition from live→inscribed without clear rules about sub-blocks
- **Duplicate rendering** - Once as live widgets, once as timeline blocks
- **Lost parent-child relationships** - Sub-blocks get inscribed separately

### Root Cause

We're trying to retrofit a hierarchical, real-time streaming system onto a flat, immutable timeline that wasn't designed for it. The V3.1 implementation created two parallel systems without resolving their fundamental incompatibility.

### Success Criteria
- [ ] Single source of truth for all blocks (live and inscribed)
- [ ] Clear ownership model with no ambiguity
- [ ] Atomic transitions preserving all relationships
- [ ] No duplicate rendering or lost data
- [ ] Proper state machine for block lifecycle

## Solution Design

### Option A: Timeline Owns Everything (Recommended)

Make Timeline the single source of truth, capable of handling both live and inscribed blocks natively.

```python
class UnifiedTimeline:
    """Single timeline that handles both live and inscribed blocks"""
    
    def __init__(self):
        self._blocks: List[Union[LiveBlock, InscribedBlock]] = []
        self._observers: List[TimelineObserver] = []
        
    def add_live_block(self, role: str, content: str = "") -> LiveBlock:
        """Create and add a live block to timeline"""
        block = LiveBlock(role, content)
        self._blocks.append(block)
        self._notify_observers(BlockAdded(block))
        return block
        
    def inscribe_block(self, block_id: str) -> InscribedBlock:
        """Atomically convert live block to inscribed, including sub-blocks"""
        live_block = self._find_live_block(block_id)
        if not live_block:
            raise ValueError(f"No live block with id {block_id}")
            
        # Atomic transformation including all sub-blocks
        inscribed = self._transform_to_inscribed(live_block)
        
        # Replace in timeline
        idx = self._blocks.index(live_block)
        self._blocks[idx] = inscribed
        
        self._notify_observers(BlockInscribed(inscribed))
        return inscribed
```

### Option B: Proper State Machine

Keep dual systems but implement strict state machine with clear ownership transfers.

```python
class BlockLifecycle:
    """State machine for block lifecycle management"""
    
    def __init__(self, live_manager: LiveBlockManager, timeline: Timeline):
        self.live_manager = live_manager
        self.timeline = timeline
        
    async def transition_to_timeline(self, block_id: str) -> None:
        """Atomic transition from live to timeline"""
        # 1. Get complete live block tree
        live_tree = await self.live_manager.get_block_tree(block_id)
        
        # 2. Stop all live updates
        await self.live_manager.freeze_block_tree(block_id)
        
        # 3. Transform to timeline format atomically
        timeline_blocks = self._transform_tree_to_timeline(live_tree)
        
        # 4. Add to timeline as single transaction
        self.timeline.add_block_tree(timeline_blocks)
        
        # 5. Remove from live manager
        await self.live_manager.remove_block_tree(block_id)
```

## Implementation Steps

### Phase 1: Define Clear Interfaces
```python
# Ownership interface
class BlockOwner(Protocol):
    def owns_block(self, block_id: str) -> bool: ...
    def transfer_ownership(self, block_id: str, new_owner: BlockOwner) -> None: ...

# State interface  
class BlockState(Enum):
    CREATING = "creating"      # Being built
    LIVE = "live"             # Active updates
    FREEZING = "freezing"     # Preparing to inscribe
    INSCRIBED = "inscribed"   # Immutable in timeline
```

### Phase 2: Implement Unified Timeline (Option A)
1. Extend Timeline to handle LiveBlock instances
2. Add lifecycle methods to Timeline
3. Remove LiveBlockManager's ownership responsibilities
4. Make LiveBlockManager a pure factory/simulator

### Phase 3: Atomic Transitions
```python
def inscribe_with_sub_blocks(self, block_id: str) -> InscribedBlock:
    """Atomically inscribe parent and all sub-blocks"""
    with self._inscription_lock:
        # Collect full tree
        parent = self.get_block(block_id)
        sub_blocks = self._collect_sub_blocks_recursive(parent)
        
        # Transform atomically
        inscribed_parent = parent.to_inscribed()
        inscribed_parent.metadata['sub_blocks'] = [
            sub.to_inscribed().to_dict() for sub in sub_blocks
        ]
        
        # Single timeline update
        self._replace_block(parent, inscribed_parent)
        
        # Remove sub-blocks from active management
        for sub in sub_blocks:
            self._remove_block(sub.id)
            
    return inscribed_parent
```

### Phase 4: Widget Updates
- Create unified widget that handles both live and inscribed blocks
- Remove duplicate rendering logic
- Single widget tree matching timeline structure

## Testing Approach

### State Machine Tests
```python
def test_no_orphaned_sub_blocks():
    """Sub-blocks always inscribed with parent"""
    timeline = UnifiedTimeline()
    parent = timeline.add_live_block("cognition")
    sub1 = timeline.add_sub_block(parent.id, "route_query")
    sub2 = timeline.add_sub_block(parent.id, "call_tool")
    
    inscribed = timeline.inscribe_block(parent.id)
    
    # Parent inscribed
    assert isinstance(timeline.get_block(parent.id), InscribedBlock)
    
    # Sub-blocks included in parent, not separate
    assert len(inscribed.metadata['sub_blocks']) == 2
    assert timeline.get_block(sub1.id) is None  # Not separately inscribed
```

### Ownership Tests
```python
def test_clear_ownership():
    """Only one system owns a block at any time"""
    lifecycle = BlockLifecycle()
    block = lifecycle.create_live_block("user", "test")
    
    # Live manager owns it
    assert lifecycle.live_manager.owns_block(block.id)
    assert not lifecycle.timeline.owns_block(block.id)
    
    # Transition
    lifecycle.transition_to_timeline(block.id)
    
    # Timeline owns it
    assert not lifecycle.live_manager.owns_block(block.id)
    assert lifecycle.timeline.owns_block(block.id)
```

## Migration Strategy

### Step 1: Parallel Implementation
- Build UnifiedTimeline alongside existing system
- Route new code through unified system
- Keep old system for backward compatibility

### Step 2: Gradual Migration  
- Update demos to use unified system
- Migrate tests incrementally
- Add deprecation warnings to old system

### Step 3: Cutover
- Switch production to unified system
- Remove old LiveBlockManager ownership code
- Delete duplicate rendering paths

## Success Metrics

- **Zero lost sub-blocks** during inscription
- **Single rendering path** for all blocks  
- **Clear ownership** at every moment
- **Atomic transitions** with no intermediate states
- **No duplicate widgets** in UI

## Risk Mitigation

### Performance Impact
- Benchmark unified vs dual systems
- Optimize if >10% performance degradation
- Consider lazy loading for large timelines

### Breaking Changes
- Provide compatibility layer during migration
- Version the API with clear deprecation timeline
- Extensive testing before cutover