# Streaming Live Output System

**Branch:** feat/streaming-live-output-system
**Summary:** Implement real-time streaming LLM responses with live animations, progressive rendering, and transparent thought processes in the Sacred Timeline UI, *crucially demonstrating the management of 'live' vs. 'inscribed' blocks*.
**Status:** High Priority - Critical Architectural Foundation
**Created:** 2025-07-10
**Updated:** 2025-07-10

## Context

### Problem Statement
V3-minimal violates the Sacred Timeline principle of "Streaming and Live Output" by showing only final results instantly. The original design requires: "Live State: Plugins transition to a 'live' state during execution, providing dynamic visual cues (animations, timers, streaming text)" and "Progressive Rendering: Output is streamed and progressively rendered to the UI, allowing users to follow the AI's thought process." **Furthermore, the system MUST correctly manage the transition of these 'live' (transient) blocks to 'inscribed' (persisted) blocks, ensuring only completed, validated blocks are ever added to the permanent timeline.**

### Success Criteria
- [ ] LLM responses stream character by character in real-time
- [ ] Live animations show processing state (spinners, progress bars)
- [ ] Users can follow AI's thinking process as it develops
- [ ] Token counters and timers update live during processing
- [ ] Cognition sub-blocks stream their individual outputs
- [ ] **Clear distinction and management of 'live' (transient) blocks vs. 'inscribed' (persisted) blocks.**
- [ ] **Only fully completed and validated blocks are inscribed to the Sacred Timeline.**

### Acceptance Criteria
- [ ] User sees LLM responses appearing incrementally, not all at once
- [ ] Processing blocks show live state with animations
- [ ] Token counts increment in real-time as tokens are consumed
- [ ] Timers show live duration during LLM processing
- [ ] Users can interrupt long-running operations
- [ ] **Live blocks are visually distinct from inscribed blocks in the UI.**
- [ ] **Upon completion, live blocks seamlessly transition to their inscribed state on the timeline.**
- [ ] **No partial or erroneous data from live blocks is ever persisted.**

## Technical Approach

### Architecture Changes
1. **Streaming Pipeline**: Async generators for real-time LLM response handling
2. **Live State Manager**: Manages plugin states and UI updates during processing, *including the 'live' state and transition to 'inscribed'*.
3. **Progressive Renderer**: Updates UI components incrementally as data arrives, *distinguishing between live and inscribed rendering*.
4. **Animation System**: Spinners, progress bars, live counters for processing states
5. **Interrupt Handling**: User cancellation of long-running operations
6. **Staging Area/Transient Block Store**: A mechanism to hold and manage 'live' blocks before they are finalized and inscribed to the Sacred Timeline.

### Implementation Plan
1. **Phase 1: Streaming Infrastructure & Live Block Management**
   - Implement async streaming for LLM providers
   - Create progressive text rendering widgets
   - Add live state management for plugins, *including the 'live' block concept and its lifecycle*.
   - **Design and implement the 'staging area' or 'Transient Block Store' for live blocks.**

2. **Phase 2: Live UI Components & Inscription Logic**
   - Create animated processing indicators
   - Implement live token and timer displays
   - Add progress visualization for multi-step operations
   - **Implement the logic for validating and inscribing completed live blocks to the Sacred Timeline.**

3. **Phase 3: Cognition Pipeline Streaming & Data Aggregation**
   - Stream individual cognition sub-block outputs
   - Show live transition between pipeline steps
   - Display intermediate thoughts and reasoning
   - **Ensure aggregation of wall times, token usage, and intermediate responses from nested plugins/submodules to the parent Cognition block.**

4. **Phase 4: User Control Features**
   - Add operation cancellation/interruption
   - Implement streaming pause/resume
   - Add streaming speed controls

### Dependencies
- LLM Integration Foundation (streaming LLM providers)
- Plugin Architecture Foundation (live plugin state management, nesting)
- Sacred Timeline Persistence (storing streaming metadata, *receiving inscribed blocks*)
- **`timeline.md` (for `TimelineBlock` and `TimelineManager` definitions, especially regarding live/inscribed states).**
- **`memory-and-context-management.md` (for accurate token counting).**

### Risks & Mitigations
- **Risk 1**: Performance issues with high-frequency UI updates
  - *Mitigation*: Throttled updates, efficient rendering, buffer management
- **Risk 2**: Complex state management for streaming operations, *especially live/inscribed transitions*.
  - *Mitigation*: Clear state machine, atomic updates, rollback mechanisms, *well-defined lifecycle for live blocks*.
- **Risk 3**: User experience issues with slow streaming
  - *Mitigation*: Configurable speeds, chunked updates, responsive controls
- **Risk 4**: Inadvertent persistence of incomplete/erroneous live block data.
  - *Mitigation*: Strict validation before inscription, dedicated staging area, robust error handling.

## Progress Log

### 2025-07-10 - Initial Planning
- Identified lack of streaming/live output in V3-minimal
- Analyzed Sacred Timeline requirements for progressive rendering
- Designed streaming architecture for real-time UI updates
- Created implementation strategy for live animations
- **Elevated priority to address live vs. inscribed block management.**

## Technical Decisions

### Decision 1: Streaming Update Frequency
**Context**: Need to balance responsiveness with performance  
**Options**: Character-by-character, word-by-word, chunk-based, time-based  
**Decision**: Hybrid approach - words for fast models, chunks for slow models  
**Reasoning**: Optimal user experience without overwhelming UI updates  
**Consequences**: Adaptive streaming based on response speed

### Decision 2: Animation Framework
**Context**: Need smooth animations for processing states  
**Options**: CSS animations, JavaScript, Rich animations, custom system  
**Decision**: Textual's animation system with Rich formatting  
**Reasoning**: Native integration with existing UI framework  
**Consequences**: Consistent animations but limited to Textual capabilities

### Decision 3: State Synchronization Strategy
**Context**: Multiple components need consistent live state updates  
**Options**: Event bus, direct updates, reactive state, message passing  
**Decision**: Event-driven updates with reactive state containers  
**Reasoning**: Decoupled components, efficient updates, clear data flow  
**Consequences**: More complex but maintainable streaming architecture

## Streaming Architecture Design

### Streaming LLM Interface
```python
class StreamingLLMProvider(ABC):
    @abstractmethod
    async def stream_request(self, request: LLMRequest) -> AsyncIterator[StreamChunk]:
        pass

@dataclass
class StreamChunk:
    content: str
    is_complete: bool = False
    tokens_consumed: int = 0
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

class StreamingManager:
    async def stream_response(self, provider: StreamingLLMProvider, 
                            request: LLMRequest) -> AsyncIterator[StreamChunk]:
        async for chunk in provider.stream_request(request):
            # Process and emit chunk with live updates
            yield self._process_chunk(chunk)
```

### Live State Management
```python
# Conceptual representation of a live block in the staging area
@dataclass
class LiveBlock:
    id: str
    type: str # e.g., "user_input", "cognition", "assistant"
    state: Literal["processing", "completed", "error"]
    content: str = ""
    tokens: int = 0
    start_time: datetime = field(default_factory=datetime.now)
    last_update: datetime = field(default_factory=datetime.now)
    # Add fields for nested blocks, intermediate thoughts, etc.

class LiveBlockManager:
    def __init__(self):
        self._live_blocks: Dict[str, LiveBlock] = {}
        self._observers: List[Callable[[LiveBlock], None]] = [] # For UI updates

    def start_live_block(self, block_id: str, block_type: str) -> LiveBlock:
        live_block = LiveBlock(
            id=block_id,
            type=block_type,
            state="processing",
            start_time=datetime.now()
        )
        self._live_blocks[block_id] = live_block
        self._notify_observers(live_block)
        return live_block

    def update_live_block(self, block_id: str, content_chunk: str, tokens_delta: int = 0) -> None:
        if block_id in self._live_blocks:
            live_block = self._live_blocks[block_id]
            live_block.content += content_chunk
            live_block.tokens += tokens_delta
            live_block.last_update = datetime.now()
            self._notify_observers(live_block)

    async def complete_live_block(self, block_id: str, final_content: Any, final_metadata: Dict[str, Any]) -> TimelineBlock:
        # Validate and transition to inscribed state
        if block_id in self._live_blocks:
            live_block = self._live_blocks.pop(block_id) # Remove from live management
            live_block.state = "completed"
            # Create a formal TimelineBlock for inscription
            inscribed_block = TimelineBlock(
                id=live_block.id,
                timestamp=live_block.start_time,
                role=live_block.type, # Assuming type maps directly to role
                content=final_content,
                metadata={**live_block.metadata, **final_metadata, "wall_time_seconds": (datetime.now() - live_block.start_time).total_seconds()}
            )
            # Notify observers (e.g., UI to replace live view with inscribed view)
            self._notify_observers(live_block) # Notify about state change
            return inscribed_block
        raise ValueError(f"Live block {block_id} not found.")

    def _notify_observers(self, live_block: LiveBlock):
        for observer in self._observers:
            observer(live_block)

    def add_observer(self, observer: Callable[[LiveBlock], None]):
        self._observers.append(observer)

    def remove_observer(self, observer: Callable[[LiveBlock], None]):
        self._observers.remove(observer)
```

### Progressive UI Components
```python
class StreamingTextWidget(Widget):
    def __init__(self, target_text: str = ""):
        super().__init__()
        self.target_text = target_text
        self.current_text = ""
        self.streaming = False
    
    async def stream_text(self, text_stream: AsyncIterator[str]) -> None:
        self.streaming = True
        async for chunk in text_stream:
            self.current_text += chunk
            self.refresh()
            await asyncio.sleep(0.01)  # Small delay for smooth animation
        self.streaming = False

class LiveTokenCounter(Widget):
    def __init__(self):
        super().__init__()
        self.count = 0
        self.target_count = 0
    
    def update_count(self, new_count: int) -> None:
        self.target_count = new_count
        # Animate counter to new value
        self.animate_to_count()

class ProcessingSpinner(Widget):
    def __init__(self):
        super().__init__()
        self.active = False
        self.spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.current_char = 0
    
    def start_spinning(self) -> None:
        self.active = True
        self.set_interval(0.1, self._update_spinner)
    
    def _update_spinner(self) -> None:
        if self.active:
            self.current_char = (self.current_char + 1) % len(self.spinner_chars)
            self.refresh()
```

## Streaming Cognition Pipeline

### Live Cognition Processing
```python
class StreamingCognitionPlugin(BlockPlugin):
    async def process_with_streaming(self, input_data: str) -> AsyncIterator[CognitionUpdate]:
        # Start live cognition block
        cognition_id = self._start_live_cognition()
        
        try:
            # Step 1: Route Query (streaming)
            yield CognitionUpdate(step="route_query", state="starting")
            async for update in self._stream_route_query(input_data):
                yield CognitionUpdate(step="route_query", content=update.content,
                                    tokens=update.tokens, state="processing")
            yield CognitionUpdate(step="route_query", state="completed")
            
            # Step 2: Call Tool (streaming)
            yield CognitionUpdate(step="call_tool", state="starting")
            async for update in self._stream_tool_call(input_data):
                yield CognitionUpdate(step="call_tool", content=update.content,
                                    tokens=update.tokens, state="processing")
            yield CognitionUpdate(step="call_tool", state="completed")
            
            # Step 3: Format Output (streaming)
            yield CognitionUpdate(step="format_output", state="starting")
            async for update in self._stream_format_output(input_data):
                yield CognitionUpdate(step="format_output", content=update.content,
                                    tokens=update.tokens, state="processing")
            yield CognitionUpdate(step="format_output", state="completed")
            
        finally:
            self._complete_live_cognition(cognition_id)
```

### Timeline Integration
```python
class StreamingTimelineView(TimelineView):
    def __init__(self):
        super().__init__()
        self.live_blocks: Dict[str, LiveBlockWidget] = {}
    
    async def start_streaming_block(self, block_type: str, 
                                  block_id: str) -> LiveBlockWidget:
        live_widget = LiveBlockWidget(block_type, block_id)
        self.live_blocks[block_id] = live_widget
        self.mount(live_widget)
        return live_widget
    
    async def update_streaming_block(self, block_id: str, 
                                   update: StreamUpdate) -> None:
        if block_id in self.live_blocks:
            await self.live_blocks[block_id].apply_update(update)
    
    async def complete_streaming_block(self, block_id: str,
                                     final_block: TimelineBlock) -> None:
        if block_id in self.live_blocks:
            # Replace live widget with final static block
            live_widget = self.live_blocks.pop(block_id)
            live_widget.remove()
            final_widget = TimelineBlockWidget(final_block)
            self.mount(final_widget)
```

## User Interaction Features

### Stream Control
```python
class StreamController:
    def __init__(self):
        self.paused = False
        self.cancelled = False
        self.speed_multiplier = 1.0
    
    def pause_stream(self) -> None:
        self.paused = True
    
    def resume_stream(self) -> None:
        self.paused = False
    
    def cancel_stream(self) -> None:
        self.cancelled = True
    
    def set_speed(self, multiplier: float) -> None:
        self.speed_multiplier = max(0.1, min(5.0, multiplier))
```

### Keyboard Controls
- **Space**: Pause/Resume streaming
- **Esc**: Cancel current operation
- **+/-**: Increase/Decrease streaming speed
- **S**: Skip to end of current stream

## Performance Optimizations

### Efficient Rendering
- Debounced UI updates to prevent excessive redraws
- Chunked content updates for large responses
- Virtual scrolling for long streaming outputs
- Background processing for non-visible blocks

### Memory Management
- Automatic cleanup of completed live blocks
- Streaming buffer size limits
- Garbage collection of old animation states
- Efficient event handler management

## Testing Strategy

### Unit Tests
- [ ] Streaming provider implementations
- [ ] Live state management
- [ ] Animation component behavior
- [ ] Stream control functionality

### Integration Tests
- [ ] Full streaming cognition pipeline
- [ ] UI updates during streaming
- [ ] User interaction with streaming content
- [ ] Stream cancellation and error handling

### Manual Testing
- [ ] Various streaming speeds and content types
- [ ] User interaction during streaming
- [ ] Performance with long streaming responses
- [ ] Animation smoothness and responsiveness

## Documentation Updates

- [ ] Streaming system architecture guide
- [ ] User interaction documentation
- [ ] Performance tuning guide
- [ ] Streaming plugin development guide

## Completion

### Final Status
- [ ] Real-time streaming LLM responses implemented
- [ ] Live animations and processing indicators working
- [ ] Progressive rendering of all timeline content
- [ ] User controls for stream interaction
- [ ] Performance optimized for smooth experience

### Follow-up Items
- [ ] Advanced streaming visualizations
- [ ] Collaborative streaming (multiple users)
- [ ] Streaming analytics and optimization
- [ ] Custom animation plugins

---

*This ledger tracks the implementation of real-time streaming and live output system for the Sacred Timeline, transforming static UI into dynamic, responsive AI interaction.*