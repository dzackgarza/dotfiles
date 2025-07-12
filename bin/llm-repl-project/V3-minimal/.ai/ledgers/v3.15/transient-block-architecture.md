# Transient Block Architecture

## Status: Not Started

## Overview
Implement `TransientBlock` as a self-contained processing unit that lives below-the-fold during execution and converts to an immutable `Block` when complete.

## Problem Statement
The current `LiveBlock` class tries to serve two incompatible purposes:
- Be a mutable container for real-time updates during processing
- Be an immutable timeline entry after inscription

This dual nature causes:
- State leakage between live and inscribed versions
- Confusion about when mutations are allowed
- Complex transformation logic during inscription
- Lost data during the conversion process

## Solution Design
Create a clear separation:
- `TransientBlock`: Mutable, lives below-fold, handles processing
- `Block`: Immutable, lives above-fold, represents history

TransientBlock manages its entire lifecycle and converts itself to a Block atomically.

## User-Visible Behaviors

### 1. Real-time Sub-block Streaming
**Current**: Sub-blocks may not update smoothly or show partial state
**New**: Each sub-block streams content character-by-character with smooth animations

### 2. Clear Sequential Execution  
**Current**: Sub-blocks may appear to run in parallel or out of order
**New**: Each sub-block visibly completes before the next begins

### 3. Atomic Block Completion
**Current**: Parent and sub-blocks inscribe separately, causing split rendering
**New**: Entire block structure moves above-fold as one complete unit

### 4. Progress Data Preservation
**Current**: Timing and token data may be lost during inscription
**New**: All metrics (time, tokens, progress) preserved exactly

### 5. Visual State Clarity
**Current**: Unclear when a block is "processing" vs "complete"
**New**: Distinct visual states with clear transitions

## Technical Implementation

### TransientBlock Base Class
```python
@dataclass
class TransientBlock:
    """A mutable block that lives below-fold during processing"""
    
    id: str = field(default_factory=lambda: str(uuid4()))
    role: str = ""  # "cognition", "assistant", etc.
    content: str = ""
    sub_blocks: List[TransientSubBlock] = field(default_factory=list)
    
    # Real-time state
    state: Literal["initializing", "processing", "finalizing", "complete"] = "initializing"
    progress: float = 0.0  # 0.0 to 1.0
    start_time: float = field(default_factory=time.time)
    
    # Metrics
    tokens_input: int = 0
    tokens_output: int = 0
    
    # Update callbacks for UI
    content_callbacks: List[Callable] = field(default_factory=list)
    progress_callbacks: List[Callable] = field(default_factory=list)
    
    async def run(self) -> None:
        """Override in subclasses to implement processing logic"""
        raise NotImplementedError
        
    def to_block(self) -> Block:
        """Convert to immutable Block for inscription"""
        return Block(
            id=self.id,
            role=self.role,
            content=self.content,
            metadata={
                "processing_time": time.time() - self.start_time,
                "tokens_input": self.tokens_input,
                "tokens_output": self.tokens_output,
            },
            sub_blocks=[sb.to_sub_block() for sb in self.sub_blocks]
        )
```

### TransientSubBlock
```python
@dataclass  
class TransientSubBlock:
    """A mutable sub-block within a TransientBlock"""
    
    id: str = field(default_factory=lambda: str(uuid4()))
    type: str = ""  # "route_query", "call_tool", etc.
    content: str = ""
    progress: float = 0.0
    
    # Metrics tracked independently
    wall_time: float = 0.0
    tokens_input: int = 0
    tokens_output: int = 0
    
    def to_sub_block(self) -> SubBlock:
        """Convert to immutable SubBlock"""
        return SubBlock(
            id=self.id,
            type=self.type,
            content=self.content,
            # Note: SubBlock doesn't store metrics, they go in parent's metadata
        )
```

### Update Mechanism
```python
class TransientBlock:
    def stream_content(self, text: str) -> None:
        """Append content and notify callbacks"""
        self.content += text
        for callback in self.content_callbacks:
            callback(self)
            
    def update_progress(self, progress: float) -> None:
        """Update progress and notify callbacks"""
        self.progress = progress
        for callback in self.progress_callbacks:
            callback(self)
```

## Acceptance Criteria

### Must Have
- [ ] TransientBlock class with clear lifecycle
- [ ] Atomic conversion to immutable Block
- [ ] Real-time update callbacks working
- [ ] Sub-blocks remain contained within parent
- [ ] All timing/token data preserved

### Should Have
- [ ] Smooth streaming animations
- [ ] Progress bars update in real-time
- [ ] Clear visual state indicators
- [ ] Graceful error handling

### Could Have
- [ ] Cancelable operations
- [ ] Pause/resume capability
- [ ] Different animation styles

## Test Plan

### Unit Tests
```python
def test_transient_block_lifecycle():
    """Verify initialization → processing → complete flow"""
    
def test_atomic_conversion():
    """Ensure to_block() preserves all data"""
    
def test_sub_block_containment():
    """Verify sub-blocks stay with parent"""
    
def test_real_time_updates():
    """Confirm callbacks fire on updates"""
```

### Integration Tests
1. Create TransientBlock below-fold
2. Add sub-blocks during processing
3. Stream content to each sub-block
4. Update progress metrics
5. Convert to Block
6. Verify all data preserved

## Dependencies
- Requires `unified-timeline-ownership` to be complete
- Blocks `cognition-block-refactor`

## Migration Notes
- LiveBlock will be completely replaced
- Existing block creation code must be updated
- UI widgets need to handle TransientBlock callbacks

## Notes
This provides the clean separation between mutable processing state and immutable history that the current architecture lacks.