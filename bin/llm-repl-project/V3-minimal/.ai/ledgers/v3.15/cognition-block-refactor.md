# Cognition Block Refactor

## Status: Not Started

## Overview
Refactor cognition blocks to work with the new TransientBlock architecture, ensuring clean sub-module orchestration and eliminating the rendering issues plaguing the current implementation.

## Problem Statement
Current cognition block implementation has fundamental issues:
- Sub-modules execute but their blocks escape containment
- Progress tracking fails because sub-blocks lack cognition_progress
- Mixed responsibilities between orchestration and display
- Sub-blocks appear both inside cognition block AND as separate timeline entries
- Timing shows 0s for sub-operations
- First sub-block often hidden or not rendered

These stem from trying to retrofit hierarchical live blocks onto a flat timeline system.

## Solution Design
Implement `CognitionTransientBlock` that:
1. Extends `TransientBlock` with cognition-specific orchestration
2. Creates and owns sub-blocks throughout their lifecycle  
3. Executes sub-modules strictly sequentially
4. Aggregates metrics from all sub-operations
5. Converts to a properly structured Block with contained sub-blocks

## User-Visible Behaviors

### 1. Clear Pipeline Visualization
**Current**: Sub-blocks may appear outside parent or not render
**New**: All sub-blocks clearly contained within cognition block borders

### 2. True Sequential Execution
**Current**: Sub-blocks may appear to overlap or run in parallel
**New**: Each stage visibly completes before the next begins, with clear transitions

### 3. Accurate Progress Tracking  
**Current**: Progress stuck at 0% or jumps erratically
**New**: Smooth progression: 0% → 33% → 67% → 100% as each stage completes

### 4. Complete Timing Information
**Current**: Sub-operations show 0s or missing timing
**New**: Each sub-block shows its execution time, parent shows total

### 5. Unified Completion
**Current**: Parent and children complete at different times
**New**: Entire pipeline completes atomically and moves above-fold as one unit

## Technical Implementation

### CognitionTransientBlock Class
```python
class CognitionTransientBlock(TransientBlock):
    """Specialized TransientBlock for cognition pipeline orchestration"""
    
    def __init__(self, query: str):
        super().__init__(role="cognition")
        self.query = query
        self.pipeline_stages = [
            RouteQueryStage,
            CallToolStage, 
            FormatOutputStage
        ]
        self.completed_stages = 0
        
    async def run(self) -> None:
        """Execute cognition pipeline with proper orchestration"""
        self.state = "processing"
        self.content = "🧠 **Cognition Pipeline**\n"
        self.stream_content(f"Processing query: {self.query}\n\n")
        
        total_stages = len(self.pipeline_stages)
        
        for i, stage_class in enumerate(self.pipeline_stages):
            # Create sub-block for this stage
            sub_block = TransientSubBlock(
                type=stage_class.block_type,
                content=stage_class.initial_content()
            )
            self.sub_blocks.append(sub_block)
            
            # Create and run stage
            stage = stage_class(
                query=self.query,
                sub_block=sub_block,
                parent=self
            )
            
            # Execute stage
            stage_start = time.time()
            await stage.execute()
            sub_block.wall_time = time.time() - stage_start
            
            # Update metrics
            self.tokens_input += sub_block.tokens_input
            self.tokens_output += sub_block.tokens_output
            
            # Update progress
            self.completed_stages += 1
            self.update_progress(self.completed_stages / total_stages)
            
            # Brief pause between stages for visual clarity
            await asyncio.sleep(0.1)
            
        self.state = "complete"
```

### Pipeline Stage Base Class
```python
class CognitionStage(ABC):
    """Base class for cognition pipeline stages"""
    
    block_type: str = ""  # Override in subclasses
    
    def __init__(self, query: str, sub_block: TransientSubBlock, parent: CognitionTransientBlock):
        self.query = query
        self.sub_block = sub_block
        self.parent = parent
        
    @classmethod
    @abstractmethod
    def initial_content(cls) -> str:
        """Return initial content for the sub-block"""
        pass
        
    @abstractmethod
    async def execute(self) -> None:
        """Execute this stage of the pipeline"""
        pass
        
    def update_content(self, content: str) -> None:
        """Update sub-block content and notify parent"""
        self.sub_block.content = content
        self.parent.notify_sub_block_update(self.sub_block)
        
    def stream_content(self, text: str) -> None:
        """Stream append to sub-block content"""
        self.sub_block.content += text
        self.parent.notify_sub_block_update(self.sub_block)
```

### Example Stage Implementation
```python
class RouteQueryStage(CognitionStage):
    """Analyze query intent and determine routing"""
    
    block_type = "route_query"
    
    @classmethod
    def initial_content(cls) -> str:
        return (
            "🎯 **Route Query**\n"
            "Analyzing user intent...\n"
        )
        
    async def execute(self) -> None:
        """Analyze the query and determine route"""
        # Simulate progressive updates
        steps = [
            "📊 Tokenizing input...",
            "🔍 Analyzing patterns...", 
            "🎯 Route determined: SEARCH"
        ]
        
        for step in steps:
            self.stream_content(f"\n→ {step}")
            await asyncio.sleep(0.3)  # Simulate processing
            
        # Set metrics
        self.sub_block.tokens_input = 15
        self.sub_block.tokens_output = 3
        self.sub_block.progress = 1.0
```

### Progress Aggregation
```python
class CognitionTransientBlock:
    def notify_sub_block_update(self, sub_block: TransientSubBlock) -> None:
        """Called when a sub-block updates"""
        # Trigger UI update for the sub-block
        for callback in self.content_callbacks:
            callback(self)
            
    def get_aggregate_progress(self) -> Dict[str, Any]:
        """Calculate overall progress metrics"""
        return {
            "stages_complete": self.completed_stages,
            "stages_total": len(self.pipeline_stages),
            "total_tokens_in": sum(sb.tokens_input for sb in self.sub_blocks),
            "total_tokens_out": sum(sb.tokens_output for sb in self.sub_blocks),
            "total_time": sum(sb.wall_time for sb in self.sub_blocks),
            "sub_block_metrics": [
                {
                    "type": sb.type,
                    "time": sb.wall_time,
                    "tokens": f"{sb.tokens_input}↑/{sb.tokens_output}↓"
                }
                for sb in self.sub_blocks
            ]
        }
```

### Conversion to Immutable Block
```python
def to_block(self) -> Block:
    """Convert to immutable Block with properly nested sub-blocks"""
    metrics = self.get_aggregate_progress()
    
    return Block(
        id=self.id,
        role=self.role,
        content=self.content,
        metadata={
            "query": self.query,
            "pipeline_metrics": metrics,
            "wall_time_seconds": time.time() - self.start_time,
        },
        time_taken=metrics["total_time"],
        tokens_input=metrics["total_tokens_in"],
        tokens_output=metrics["total_tokens_out"],
        sub_blocks=[sb.to_sub_block() for sb in self.sub_blocks]
    )
```

## Acceptance Criteria

### Must Have
- [ ] All sub-blocks visually contained within parent
- [ ] Sequential execution clearly visible
- [ ] Progress tracking works (0% → 100%)
- [ ] All timing data accurate and displayed
- [ ] Clean conversion to immutable structure

### Should Have
- [ ] Smooth animations between stages
- [ ] Error handling for failed stages
- [ ] Cancelable pipeline execution
- [ ] Stage retry capability

### Could Have
- [ ] Configurable pipeline stages
- [ ] Parallel stage execution option
- [ ] Pipeline visualization modes
- [ ] Stage performance metrics

## Test Plan

### Visual Tests
1. Enter query and watch cognition block appear
2. Verify all 3 sub-blocks render inside parent
3. Confirm sequential execution visible
4. Watch progress bar update smoothly
5. Check timing shows for each stage
6. Verify atomic inscription of entire structure

### Unit Tests
```python
def test_pipeline_orchestration():
    """Verify stages execute in order"""
    
def test_metric_aggregation():
    """Ensure metrics sum correctly"""
    
def test_progress_updates():
    """Confirm progress tracks accurately"""
    
def test_atomic_structure():
    """Verify sub-blocks stay contained"""
```

### Edge Cases
- Pipeline stage failures
- Cancelled execution
- Very long running stages
- Empty or invalid queries

## Dependencies
- Requires all other v3.15 ledgers to be complete
- This is the final integration piece

## Migration Impact
- `AsyncInputProcessor` will use `CognitionTransientBlock`
- Remove all `LiveBlock` cognition code
- Update any code expecting flat sub-blocks

## Notes
This refactor eliminates the entire class of bugs we've been seeing by ensuring sub-blocks can never escape their parent context. The clear stage progression gives users confidence in what the system is doing.