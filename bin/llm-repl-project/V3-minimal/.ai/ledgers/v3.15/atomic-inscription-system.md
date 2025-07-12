# Atomic Inscription System  

## Status: Not Started

## Overview
Implement atomic inscription that moves entire block structures from below-fold to above-fold in one indivisible operation, preserving all relationships and data.

## Problem Statement
Current inscription process has multiple steps that can fail independently:
- Parent blocks inscribe separately from sub-blocks
- Sub-blocks can be inscribed as top-level blocks
- Data can be lost during transformation
- Partial inscriptions leave system in inconsistent state
- No rollback capability if inscription fails

This causes:
- Split rendering where sub-blocks appear separately
- Lost parent-child relationships
- Missing timing or progress data
- Corrupted timeline state

## Solution Design
Create an atomic inscription system that:
1. Validates the complete block structure
2. Transforms TransientBlock → Block in memory
3. Inscribes the entire structure in one operation
4. Clears below-fold only after successful inscription
5. Provides rollback on any failure

## User-Visible Behaviors

### 1. Single Inscription Moment
**Current**: Parent and sub-blocks inscribe at different times
**New**: Entire block structure moves from below to above fold simultaneously

### 2. Preserved Block Structure
**Current**: Sub-blocks may lose their parent relationship
**New**: Complete hierarchy maintained exactly as shown during processing

### 3. Complete Data Transfer  
**Current**: Some metrics/timing data lost during inscription
**New**: Every piece of data (content, timing, tokens, progress) preserved

### 4. Clear Completion Signal
**Current**: Unclear when inscription is complete
**New**: Visual feedback (animation, sound, indicator) on successful inscription

### 5. Immediate Ready State
**Current**: Delay or confusion about when ready for next input
**New**: Below-fold immediately cleared and ready for next block

## Technical Implementation

### Atomic Inscription Method
```python
class TimelineWidget:
    async def inscribe_current_block(self) -> bool:
        """
        Atomically inscribe the below-fold block to above-fold.
        Returns True on success, False on failure.
        """
        if not self.below_fold_block:
            return False
            
        if self.below_fold_block.state != "complete":
            return False
            
        try:
            # Step 1: Validate structure
            self._validate_block_structure(self.below_fold_block)
            
            # Step 2: Create immutable copy
            immutable_block = self.below_fold_block.to_block()
            
            # Step 3: Validate conversion
            self._validate_conversion(self.below_fold_block, immutable_block)
            
            # Step 4: Begin transaction
            transaction_id = self._begin_inscription_transaction()
            
            try:
                # Step 5: Add to sacred timeline
                self.sacred_timeline.add_block(immutable_block)
                
                # Step 6: Update UI above-fold
                await self._add_block_above_fold(immutable_block)
                
                # Step 7: Clear below-fold
                self.below_fold_block = None
                await self._clear_below_fold()
                
                # Step 8: Commit transaction
                self._commit_inscription_transaction(transaction_id)
                
                # Step 9: Trigger completion effects
                await self._trigger_inscription_effects()
                
                return True
                
            except Exception as e:
                # Rollback on any failure
                self._rollback_inscription_transaction(transaction_id)
                raise InscriptionError(f"Failed to inscribe block: {e}")
                
        except ValidationError as e:
            logger.error(f"Block validation failed: {e}")
            return False
```

### Validation Methods
```python
def _validate_block_structure(self, block: TransientBlock) -> None:
    """Ensure block structure is valid for inscription"""
    if not block.id:
        raise ValidationError("Block missing ID")
        
    if not block.role:
        raise ValidationError("Block missing role")
        
    # Validate sub-blocks
    for sub_block in block.sub_blocks:
        if not sub_block.id:
            raise ValidationError(f"Sub-block missing ID")
        if not sub_block.type:
            raise ValidationError(f"Sub-block missing type")
            
    # Validate metrics
    if block.tokens_input < 0 or block.tokens_output < 0:
        raise ValidationError("Invalid token counts")
        
def _validate_conversion(self, transient: TransientBlock, immutable: Block) -> None:
    """Ensure conversion preserved all data"""
    if transient.id != immutable.id:
        raise ValidationError("ID mismatch after conversion")
        
    if len(transient.sub_blocks) != len(immutable.sub_blocks):
        raise ValidationError("Sub-block count mismatch")
        
    # Verify all content preserved
    if transient.content != immutable.content:
        raise ValidationError("Content mismatch")
```

### Transaction Management
```python
class InscriptionTransaction:
    """Tracks state for rollback capability"""
    def __init__(self, transaction_id: str):
        self.id = transaction_id
        self.timestamp = time.time()
        self.original_timeline_state = None
        self.original_below_fold = None
        
@dataclass
class TimelineWidget:
    _active_transactions: Dict[str, InscriptionTransaction] = field(default_factory=dict)
    
    def _begin_inscription_transaction(self) -> str:
        """Start tracking for potential rollback"""
        transaction_id = str(uuid4())
        transaction = InscriptionTransaction(transaction_id)
        
        # Snapshot current state
        transaction.original_timeline_state = self.sacred_timeline.get_state_snapshot()
        transaction.original_below_fold = copy.deepcopy(self.below_fold_block)
        
        self._active_transactions[transaction_id] = transaction
        return transaction_id
        
    def _rollback_inscription_transaction(self, transaction_id: str) -> None:
        """Restore previous state on failure"""
        transaction = self._active_transactions.get(transaction_id)
        if not transaction:
            return
            
        # Restore timeline
        self.sacred_timeline.restore_snapshot(transaction.original_timeline_state)
        
        # Restore below-fold
        self.below_fold_block = transaction.original_below_fold
        
        # Clean up
        del self._active_transactions[transaction_id]
```

### Visual Effects
```python
async def _trigger_inscription_effects(self) -> None:
    """Provide clear feedback on successful inscription"""
    # Visual effect on fold indicator
    fold = self.query_one("#fold-indicator")
    fold.add_class("inscription-flash")
    
    # Brief glow animation
    await asyncio.sleep(0.3)
    fold.remove_class("inscription-flash")
    
    # Optional: Sound effect
    if self.config.sound_enabled:
        await self.play_sound("inscription_complete")
```

## Acceptance Criteria

### Must Have
- [ ] Atomic inscription - all or nothing
- [ ] Complete structure preservation
- [ ] All data transferred correctly
- [ ] Transaction rollback on failure
- [ ] Below-fold cleared after success

### Should Have
- [ ] Visual inscription effects
- [ ] Error messages on validation failure
- [ ] Performance metrics tracked
- [ ] Inscription event logging

### Could Have
- [ ] Sound effects
- [ ] Configurable animation styles
- [ ] Batch inscription support
- [ ] Inscription history/undo

## Test Plan

### Unit Tests
```python
def test_atomic_inscription():
    """Verify all-or-nothing behavior"""
    
def test_structure_preservation():
    """Ensure hierarchy maintained"""
    
def test_data_completeness():
    """Verify no data loss"""
    
def test_rollback_on_failure():
    """Confirm state restored on error"""
```

### Integration Tests
1. Create complex block with multiple sub-blocks
2. Add extensive metadata and timing data
3. Complete processing
4. Trigger inscription
5. Verify entire structure appears above-fold
6. Confirm below-fold cleared
7. Test failure scenarios and rollback

### Error Scenarios
- Inscription during active processing
- Invalid block structure
- Network/storage failures
- Concurrent inscription attempts

## Dependencies
- Requires `unified-timeline-ownership`
- Requires `transient-block-architecture`
- Works with `spatial-timeline-rendering`

## Performance Considerations
- Inscription should complete in <100ms
- Animations should not block inscription
- Large blocks should not freeze UI
- Memory usage during deep copy

## Notes
This atomic system ensures the timeline never enters an inconsistent state. The transaction approach provides safety while the visual effects give users confidence that their work has been preserved.