# Event-Driven Communication System

**Branch:** feat/event-driven-communication
**Summary:** Replace V3-minimal's direct coupling with an event-driven architecture where components communicate through events, enabling loose coupling and modular plugin interaction, *crucial for managing live updates and the transition of 'live' to 'inscribed' blocks on the Sacred Timeline*.
**Status:** High Priority - Critical Architectural Foundation
**Created:** 2025-07-10
**Updated:** 2025-07-10

## Context

### Problem Statement
V3-minimal violates the Sacred Timeline communication pattern by using **DIRECT COUPLING** between components. The original design requires: "Event-Driven Communication: Components (plugins, UI, core) communicate primarily through events. This allows for loose coupling, where senders don't need direct knowledge of receivers." The current tight coupling makes the system rigid and prevents true plugin independence. **This direct coupling also hinders the transparent, real-time display of 'live' block data and the seamless, validated inscription of completed blocks to the permanent timeline.**

### Success Criteria
- [ ] Components communicate only through well-defined events
- [ ] Plugins are completely decoupled from specific UI implementations
- [ ] New plugins can be added without modifying existing components
- [ ] Event system supports both synchronous and asynchronous operations
- [ ] Event flow is traceable and debuggable
- [ ] **Live updates from plugins (e.g., streaming LLM responses, token counts, timers) are efficiently communicated to the UI via events.**
- [ ] **Events facilitate the clear distinction and management of 'live' (transient) blocks and their eventual inscription.**

### Acceptance Criteria
- [ ] Timeline updates flow through events, not direct method calls
- [ ] Plugin interactions happen via event bus, not direct references
- [ ] UI components subscribe to events rather than polling state
- [ ] Event system handles plugin failures gracefully
- [ ] Event ordering and delivery guarantees are maintained
- [ ] **Real-time updates to 'live' blocks (content, metadata, status) are driven by events.**
- [ ] **The transition of a 'live' block to an 'inscribed' block is triggered and managed through events, ensuring data integrity.**

## Technical Approach

### Architecture Changes
1. **Event Bus**: Central message routing system for all component communication
2. **Event Types**: Strongly-typed event definitions for different operations, *including specific events for live block updates and inscription*.
3. **Event Handlers**: Async event processing with error handling
4. **Plugin Integration**: Events as primary plugin communication mechanism, *especially for reporting live progress and completion*.
5. **UI Event Binding**: Reactive UI updates based on event subscriptions, *distinguishing between live and inscribed block rendering*.

### Implementation Plan
1. **Phase 1: Event Infrastructure & Live Update Events**
   - Create event bus with publish/subscribe patterns
   - Define core event types for Sacred Timeline operations, *including `LiveBlockUpdated` and `LiveBlockCompleted` events*.
   - Implement event handler registration and lifecycle

2. **Phase 2: Plugin Event Integration for Live Data**
   - Convert plugin interactions to event-based communication
   - Add event emission from plugin lifecycle methods, *especially for streaming content, token counts, and wall times*.
   - Implement inter-plugin communication via events

3. **Phase 3: UI Event Binding & Inscription Triggering**
   - Replace direct UI updates with event subscriptions
   - Add reactive UI components responding to events, *specifically for rendering live blocks and transitioning them to inscribed views*.
   - Implement event-driven timeline rendering, *where inscription is triggered by a `LiveBlockCompleted` event and validated data*.

4. **Phase 4: Advanced Event Features**
   - Add event persistence and replay capabilities
   - Implement event filtering and routing rules
   - Add event analytics and debugging tools

### Dependencies
- Plugin Architecture Foundation (plugins as event producers/consumers)
- Streaming Live Output System (streaming events for real-time updates, *especially for live block content*)
- Sacred Timeline Persistence (events trigger timeline writes, *specifically for inscribed blocks*)
- **`timeline.md` (for `TimelineBlock` definition and `TimelineManager` interaction).**
- **`streaming-live-output-system.md` (for the `LiveBlock` concept and its lifecycle).**

### Risks & Mitigations
- **Risk 1**: Event ordering issues causing inconsistent state, *especially during live-to-inscribed transitions*.
  - *Mitigation*: Event sequencing, atomic operations, state validation, *transactional updates for inscription*.
- **Risk 2**: Performance overhead from event processing
  - *Mitigation*: Efficient event routing, batching, async processing
- **Risk 3**: Complex debugging of event-driven flows
  - *Mitigation*: Event logging, tracing, debugging tools

## Progress Log

### 2025-07-10 - Initial Planning
- Identified direct coupling violations in V3-minimal architecture
- Analyzed Sacred Timeline event-driven communication requirements
- Designed event bus architecture for component decoupling
- Created migration strategy for existing tight coupling
- **Elevated priority to address live vs. inscribed block management through events.**

## Technical Decisions

### Decision 1: Event Bus Pattern Selection
**Context**: Need efficient, reliable event routing for plugin communication  
**Options**: Observer pattern, message queue, pub/sub, actor model  
**Decision**: Publish/Subscribe with typed events and async handlers  
**Reasoning**: Flexible routing, type safety, async support, scalable  
**Consequences**: Clear event contracts but requires event design discipline

### Decision 2: Event Delivery Guarantees
**Context**: Some events are critical (timeline updates), others are optional (UI animations)  
**Options**: Fire-and-forget, at-least-once, exactly-once, best-effort  
**Decision**: Configurable delivery guarantees based on event criticality  
**Reasoning**: Critical events need reliability, non-critical events need performance  
**Consequences**: More complex event system but appropriate guarantees

### Decision 3: Event Persistence Strategy
**Context**: Events may need replay for debugging or recovery  
**Options**: No persistence, full logging, selective persistence, in-memory only  
**Decision**: Selective persistence for critical events with configurable retention  
**Reasoning**: Balance between debugging capability and performance/storage  
**Consequences**: Enhanced debugging but increased complexity

## Event System Architecture

### Core Event Bus
```python
from typing import TypeVar, Generic, Callable, Dict, List
from dataclasses import dataclass
from enum import Enum
import asyncio
import uuid

T = TypeVar('T')

class EventPriority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class Event(Generic[T]):
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: str = ""
    data: T = None
    source: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    priority: EventPriority = EventPriority.NORMAL
    persistent: bool = False

class EventBus:
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}
        self._event_queue: asyncio.Queue = asyncio.Queue()
        self._persistent_events: List[Event] = []
        self._running = False
    
    async def publish(self, event: Event) -> bool:
        """Publish an event to all registered handlers."""
        if event.persistent:
            self._persistent_events.append(event)
        
        await self._event_queue.put(event)
        return True
    
    def subscribe(self, event_type: str, handler: Callable) -> str:
        """Subscribe to events of a specific type."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        
        self._handlers[event_type].append(handler)
        handler_id = f"{event_type}_{len(self._handlers[event_type])}"
        return handler_id
    
    async def start_processing(self) -> None:
        """Start the event processing loop."""
        self._running = True
        while self._running:
            try:
                event = await self._event_queue.get()
                await self._process_event(event)
            except Exception as e:
                # Log error but continue processing
                print(f"Event processing error: {e}")
    
    async def _process_event(self, event: Event) -> None:
        """Process a single event by calling all registered handlers."""
        handlers = self._handlers.get(event.type, [])
        
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
            except Exception as e:
                print(f"Handler error for {event.type}: {e}")
```

### Sacred Timeline Event Types
```python
@dataclass
class TimelineBlockCreated:
    block_id: str
    block_type: str
    content: str
    metadata: Dict[str, Any]

@dataclass
class PluginStateChanged:
    plugin_id: str
    plugin_name: str
    old_state: str
    new_state: str
    timestamp: datetime

@dataclass
class LLMRequestStarted:
    request_id: str
    plugin_id: str
    model: str
    provider: str
    estimated_tokens: int

@dataclass
class LLMResponseChunk:
    request_id: str
    chunk: str
    tokens_consumed: int
    is_complete: bool

@dataclass
class CognitionStepCompleted:
    cognition_id: str
    step_name: str
    step_result: Dict[str, Any]
    tokens_used: int
    duration: float

# Event type constants
class EventTypes:
    TIMELINE_BLOCK_CREATED = "timeline.block.created"
    PLUGIN_STATE_CHANGED = "plugin.state.changed"
    LLM_REQUEST_STARTED = "llm.request.started"
    LLM_RESPONSE_CHUNK = "llm.response.chunk"
    COGNITION_STEP_COMPLETED = "cognition.step.completed"
    USER_INPUT_RECEIVED = "user.input.received"
    ASSISTANT_RESPONSE_READY = "assistant.response.ready"
    # New events for live block management
    LIVE_BLOCK_UPDATED = "live.block.updated"
    LIVE_BLOCK_COMPLETED = "live.block.completed"
```

## Plugin Event Integration

### Event-Driven Plugin Base
```python
class EventDrivenPlugin(BlockPlugin):
    def __init__(self, event_bus: EventBus):
        super().__init__()
        self.event_bus = event_bus
        self._setup_event_handlers()
    
    def _setup_event_handlers(self) -> None:
        """Override in subclasses to register event handlers."""
        pass
    
    async def emit_event(self, event_type: str, data: Any,
                        priority: EventPriority = EventPriority.NORMAL) -> None:
        """Emit an event from this plugin."""
        event = Event(
            type=event_type,
            data=data,
            source=self.metadata.name,
            priority=priority
        )
        await self.event_bus.publish(event)
    
    async def emit_state_change(self, new_state: PluginState) -> None:
        """Emit plugin state change event."""
        await self.emit_event(
            EventTypes.PLUGIN_STATE_CHANGED,
            PluginStateChanged(
                plugin_id=self.plugin_id,
                plugin_name=self.metadata.name,
                old_state=self.state.value,
                new_state=new_state.value,
                timestamp=datetime.now()
            ),
            priority=EventPriority.HIGH
        )
        self.state = new_state
```

### Event-Driven Cognition Plugin
```python
class EventDrivenCognitionPlugin(EventDrivenPlugin):
    def _setup_event_handlers(self) -> None:
        self.event_bus.subscribe(
            EventTypes.USER_INPUT_RECEIVED,
            self._handle_user_input
        )
    
    async def _handle_user_input(self, event: Event[UserInputReceived]) -> None:
        """Handle user input event to start cognition processing."""
        await self.emit_state_change(PluginState.PROCESSING)
        
        try:
            # Start cognition processing
            cognition_result = await self._process_cognition(event.data.content)
            
            # Emit completion event
            await self.emit_event(
                EventTypes.COGNITION_STEP_COMPLETED,
                CognitionStepCompleted(
                    cognition_id=self.plugin_id,
                    step_name="complete",
                    step_result=cognition_result,
                    tokens_used=cognition_result.get("tokens", 0),
                    duration=self._timer.duration
                )
            )
            
            await self.emit_state_change(PluginState.COMPLETED)
            
        except Exception as e:
            await self.emit_state_change(PluginState.ERROR)
            raise
```

## UI Event Integration

### Event-Driven Timeline View
```python
class EventDrivenTimelineView(TimelineView):
    def __init__(self, event_bus: EventBus):
        super().__init__()
        self.event_bus = event_bus
        self._setup_event_subscriptions()
    
    def _setup_event_subscriptions(self) -> None:
        """Subscribe to relevant timeline events."""
        self.event_bus.subscribe(
            EventTypes.TIMELINE_BLOCK_CREATED,
            self._handle_block_created
        )
        self.event_bus.subscribe(
            EventTypes.LLM_RESPONSE_CHUNK,
            self._handle_response_chunk
        )
        self.event_bus.subscribe(
            EventTypes.PLUGIN_STATE_CHANGED,
            self._handle_plugin_state_change
        )
        # New subscriptions for live block management
        self.event_bus.subscribe(
            EventTypes.LIVE_BLOCK_UPDATED,
            self._handle_live_block_updated
        )
        self.event_bus.subscribe(
            EventTypes.LIVE_BLOCK_COMPLETED,
            self._handle_live_block_completed
        )
    
    async def _handle_block_created(self, event: Event[TimelineBlockCreated]) -> None:
        """Handle new timeline block creation."""
        block_data = event.data
        new_block = TimelineBlock(
            id=block_data.block_id,
            role=block_data.block_type,
            content=block_data.content,
            metadata=block_data.metadata,
            timestamp=event.timestamp
        )
        
        # Add block to UI (no direct timeline manipulation)
        block_widget = TimelineBlockWidget(new_block)
        self.mount(block_widget)
        self.scroll_end(animate=True)
    
    async def _handle_response_chunk(self, event: Event[LLMResponseChunk]) -> None:
        """Handle streaming LLM response chunks."""
        chunk_data = event.data
        # Update streaming widget for this request
        await self._update_streaming_content(
            chunk_data.request_id,
            chunk_data.chunk
        )
    
    async def _handle_plugin_state_change(self, event: Event[PluginStateChanged]) -> None:
        """Handle plugin state changes for UI updates."""
        state_data = event.data
        # Update plugin visualization based on new state
        await self._update_plugin_display(
            state_data.plugin_id,
            state_data.new_state
        )
    
    async def _handle_live_block_updated(self, event: Event[LiveBlockUpdated]) -> None:
        """Handle updates to a live block (e.g., new content, token counts)."""
        live_block_data = event.data
        # Find the corresponding live block widget and update its content/metadata
        if live_block_data.block_id in self.live_blocks:
            await self.live_blocks[live_block_data.block_id].update_content(
                live_block_data.content_chunk,
                live_block_data.tokens_delta,
                live_block_data.metadata
            )

    async def _handle_live_block_completed(self, event: Event[LiveBlockCompleted]) -> None:
        """Handle completion of a live block and its transition to inscribed."""
        completed_block_data = event.data
        if completed_block_data.block_id in self.live_blocks:
            # Remove live widget
            live_widget = self.live_blocks.pop(completed_block_data.block_id)
            live_widget.remove()
            # Add inscribed widget
            inscribed_widget = TimelineBlockWidget(completed_block_data.inscribed_block)
            self.mount(inscribed_widget)
            self.scroll_end(animate=True)
```

### Reactive Timeline Controller
```python
class EventDrivenTimelineController:
    def __init__(self, event_bus: EventBus, timeline_repository: TimelineRepository):
        self.event_bus = event_bus
        self.timeline_repository = timeline_repository
        self._setup_event_handlers()
    
    def _setup_event_handlers(self) -> None:
        self.event_bus.subscribe(
            EventTypes.PLUGIN_STATE_CHANGED,
            self._handle_plugin_completion
        )
        self.event_bus.subscribe(
            EventTypes.COGNITION_STEP_COMPLETED,
            self._handle_cognition_completion
        )
        # New subscription for live block completion to trigger inscription
        self.event_bus.subscribe(
            EventTypes.LIVE_BLOCK_COMPLETED,
            self._handle_live_block_inscription
        )
    
    async def _handle_plugin_completion(self, event: Event[PluginStateChanged]) -> None:
        """Handle plugin completion to create timeline blocks."""
        if event.data.new_state == PluginState.COMPLETED.value:
            # Plugin completed - create timeline block
            await self._create_timeline_block_from_plugin(event.data.plugin_id)
    
    async def _create_timeline_block_from_plugin(self, plugin_id: str) -> None:
        """Create timeline block from completed plugin."""
        # Get plugin result and create block
        plugin_result = await self._get_plugin_result(plugin_id)
        
        # Save to persistent timeline
        block = await self.timeline_repository.add_block(
            session_id=self._current_session_id,
            block=plugin_result
        )
        
        # Emit block creation event
        await self.event_bus.publish(Event(
            type=EventTypes.TIMELINE_BLOCK_CREATED,
            data=TimelineBlockCreated(
                block_id=block.id,
                block_type=block.role,
                content=block.content,
                metadata=block.metadata
            ),
            persistent=True
        ))

    async def _handle_live_block_inscription(self, event: Event[LiveBlockCompleted]) -> None:
        """Handle live block completion to inscribe it to the Sacred Timeline."""
        inscribed_block = event.data.inscribed_block
        # Add the fully validated and completed block to the Sacred Timeline
        # This assumes timeline.add_block handles the actual persistence
        timeline.add_block(inscribed_block)
        # Optionally, emit a TIMELINE_BLOCK_CREATED event for other components to react
        await self.event_bus.publish(Event(
            type=EventTypes.TIMELINE_BLOCK_CREATED,
            data=TimelineBlockCreated(
                block_id=inscribed_block.id,
                block_type=inscribed_block.role,
                content=inscribed_block.content,
                metadata=inscribed_block.metadata
            ),
            persistent=True
        ))
```

## Event Flow Examples

### Sacred Turn Structure Event Flow
```
1. User Input → USER_INPUT_RECEIVED event
2. CognitionPlugin handles → PLUGIN_STATE_CHANGED (processing)
3. LLM requests → LLM_REQUEST_STARTED events
4. Streaming responses → LLM_RESPONSE_CHUNK events, LIVE_BLOCK_UPDATED events
5. Cognition completion → COGNITION_STEP_COMPLETED event, LIVE_BLOCK_COMPLETED event
6. Timeline persistence → TIMELINE_BLOCK_CREATED event (triggered by LIVE_BLOCK_COMPLETED handling)
7. UI updates → Reactive rendering from events (distinguishing live vs. inscribed)
```

### Plugin Communication Example
```python
# Plugin A emits event
await plugin_a.emit_event("custom.data.processed", {
    "result": processed_data,
    "metadata": {"accuracy": 0.95}
})

# Plugin B handles the event
class PluginB(EventDrivenPlugin):
    def _setup_event_handlers(self):
        self.event_bus.subscribe("custom.data.processed", self._handle_processed_data)
    
    async def _handle_processed_data(self, event):
        # React to Plugin A's output
        await self._process_result(event.data["result"])
```

## Testing Strategy

### Unit Tests
- [ ] Event bus publish/subscribe functionality
- [ ] Event handler registration and execution
- [ ] Event persistence and replay
- [ ] Error handling in event processing
- [ ] **`LiveBlockManager` lifecycle (start, update, complete, inscription triggering).**

### Integration Tests
- [ ] Plugin communication through events
- [ ] UI updates from event subscriptions
- [ ] Timeline persistence triggered by events
- [ ] Event ordering and consistency
- [ ] **Full live-to-inscribed block transition, including data integrity checks.**
- [ ] **Performance of live updates under load.**

### Manual Testing
- [ ] Complete Sacred Turn Structure via events
- [ ] Plugin failure handling through events
- [ ] Event system performance under load
- [ ] Event debugging and tracing tools
- [ ] **Visual verification of live block animations and transitions.**
- [ ] **User experience during rapid live updates and inscription.**

## Documentation Updates

- [ ] Event-driven architecture guide
- [ ] Event type reference documentation
- [ ] Plugin event integration tutorial
- [ ] Event debugging and troubleshooting guide
- [ ] **Live vs. Inscribed block lifecycle documentation.**

## Performance Considerations

### Event Processing Optimization
- Async event handlers for non-blocking processing
- Event batching for high-frequency updates
- Priority-based event processing
- Handler execution monitoring and optimization

### Memory Management
- Event queue size limits
- Automatic cleanup of old persistent events
- Efficient event serialization for persistence
- Handler registration cleanup on plugin unload
- **Efficient management of `LiveBlock` objects in the staging area.**

## Completion

### Final Status
- [ ] All component communication flows through events
- [ ] Plugin interactions are completely decoupled
- [ ] UI updates reactively from event subscriptions
- [ ] Event system supports debugging and tracing
- [ ] Performance is acceptable for real-time operations
- [ ] **Robust management of 'live' and 'inscribed' blocks is implemented and proven.**

### Follow-up Items
- [ ] Event-driven plugin marketplace
- [ ] Advanced event routing and filtering
- [ ] Event system monitoring and analytics
- [ ] Cross-session event replay capabilities
- [ ] **Refinement of live block visual indicators and animations.**

---

*This ledger tracks the transformation of V3-minimal from direct coupling to event-driven architecture, enabling true plugin independence and modular communication, with a critical focus on transparent live updates and robust timeline inscription.*