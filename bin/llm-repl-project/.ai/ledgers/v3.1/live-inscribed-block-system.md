# Sacred GUI Architecture Implementation

**Branch:** feat/sacred-gui-architecture
**Summary:** Implement the canonical Sacred GUI layout with three distinct areas: Sacred Timeline (top), Live Workspace (middle), and Input (bottom). This replaces the single-timeline approach with the immutable dual-scroll architecture defined in CLAUDE.md.
**Status:** Planning
**Created:** 2025-07-10
**Updated:** 2025-07-12

## Context

### Problem Statement
The current single-timeline architecture conflicts with the Sacred GUI design. We need to implement the canonical three-area layout: Sacred Timeline for completed turns, Live Workspace for active cognition processing, and PromptInput at bottom. This architecture solves all layout conflicts and provides clean separation between history and active processing.

### Success Criteria
- [ ] Three-area Sacred GUI layout implemented correctly
- [ ] Sacred Timeline displays completed turns with hrule separators
- [ ] Live Workspace shows/hides based on cognition state
- [ ] Turn completion moves Live Workspace → Sacred Timeline
- [ ] No nested container violations (simple widgets only)

### User-Visible Behaviors
When this ledger is complete, the user will see:

1. **Three distinct areas: Sacred Timeline (top), Live Workspace (middle), Input (bottom)**
2. **Sacred Timeline shows completed conversation turns separated by horizontal rules**
3. **Live Workspace appears during cognition with streaming sub-modules**
4. **Live Workspace disappears/collapses when idle (2-way split layout)**
5. **Turn completion transfers Live Workspace content to Sacred Timeline as permanent blocks**

### Acceptance Criteria
- [ ] Sacred Timeline contains only completed User → Cognition → Assistant turns
- [ ] Live Workspace dynamically shows/hides based on processing state
- [ ] Each scroll area contains simple widgets with no nested containers
- [ ] hrules visually separate turns in Sacred Timeline
- [ ] Assistant response always appears as final sub-module in Live Workspace

## Technical Approach

### Architecture Changes
1. **SacredTimelineWidget**: VerticalScroll containing completed conversation turns
2. **LiveWorkspaceWidget**: VerticalScroll containing active cognition sub-modules
3. **WorkspaceManager**: Controls Live Workspace visibility and content transfer
4. **TurnSeparator**: hrule widgets that separate conversation turns
5. **ThreeAreaLayout**: Main container organizing Sacred Timeline + Live Workspace + Input

### Implementation Plan
1. **Phase 1: Live Block Foundation**
   - Create LiveBlock class with mutable state and update methods
   - Implement LiveBlockManager for transient block management
   - Add basic live → inscribed transition mechanism

2. **Phase 2: Visual Representation**
   - Design Textual widgets for live vs inscribed blocks
   - Implement real-time animations (spinners, progress bars, counters)
   - Add transition animations between states

3. **Phase 3: Mock Data Integration**
   - Create realistic mock scenarios (coding, debugging, research)
   - Add configurable timing and token data
   - Implement various live block types and behaviors

4. **Phase 4: UX Polish**
   - Refine animations and transitions
   - Add user controls for live block interaction
   - Optimize performance with multiple live blocks

5. **Phase 5: Integration**
   - Integrate ledger into the main system

5. **Phase 5: Integration**
   - Integrate ledger into the main system

## Live Block Architecture

### Core Block States
```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional, List, Callable
from enum import Enum
import uuid
import asyncio

class BlockState(Enum):
    LIVE = "live"           # Currently updating, mutable
    TRANSITIONING = "transitioning"  # Moving to inscribed state
    INSCRIBED = "inscribed"  # Permanently added to timeline

@dataclass
class LiveBlockData:
    """Mutable data for live blocks."""
    content: str = ""
    tokens_input: int = 0
    tokens_output: int = 0
    wall_time_seconds: float = 0.0
    progress: float = 0.0  # 0.0 to 1.0
    sub_blocks: List['LiveBlock'] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "content": self.content,
            "tokens_input": self.tokens_input,
            "tokens_output": self.tokens_output,
            "wall_time_seconds": self.wall_time_seconds,
            "progress": self.progress,
            "sub_blocks": [block.to_dict() for block in self.sub_blocks],
            "metadata": self.metadata
        }

class LiveBlock:
    """A block in live state that can be updated in real-time."""
    
    def __init__(self, role: str, initial_content: str = ""):
        self.id = str(uuid.uuid4())
        self.role = role
        self.state = BlockState.LIVE
        self.created_at = datetime.now()
        self.data = LiveBlockData(content=initial_content)
        
        # Event handlers for UI updates
        self.update_callbacks: List[Callable] = []
        
        # Mock data simulation
        self._simulation_task: Optional[asyncio.Task] = None
        self._is_simulating = False
    
    def add_update_callback(self, callback: Callable) -> None:
        """Add callback for when block data updates."""
        self.update_callbacks.append(callback)
    
    def _notify_update(self) -> None:
        """Notify all callbacks of data update."""
        for callback in self.update_callbacks:
            try:
                callback(self)
            except Exception as e:
                print(f"Error in update callback: {e}")
    
    def update_content(self, new_content: str) -> None:
        """Update block content (only in live state)."""
        if self.state != BlockState.LIVE:
            raise ValueError("Cannot update inscribed block")
        
        self.data.content = new_content
        self._notify_update()
    
    def append_content(self, additional_content: str) -> None:
        """Append to existing content (streaming simulation)."""
        if self.state != BlockState.LIVE:
            raise ValueError("Cannot update inscribed block")
        
        self.data.content += additional_content
        self._notify_update()
    
    def update_tokens(self, input_tokens: int = 0, output_tokens: int = 0) -> None:
        """Update token counts."""
        if self.state != BlockState.LIVE:
            return
        
        self.data.tokens_input += input_tokens
        self.data.tokens_output += output_tokens
        self._notify_update()
    
    def update_progress(self, progress: float) -> None:
        """Update progress (0.0 to 1.0)."""
        if self.state != BlockState.LIVE:
            return
        
        self.data.progress = max(0.0, min(1.0, progress))
        self._notify_update()
    
    def add_sub_block(self, sub_block: 'LiveBlock') -> None:
        """Add sub-block for nested plugin simulation."""
        if self.state != BlockState.LIVE:
            return
        
        self.data.sub_blocks.append(sub_block)
        # Connect sub-block updates to parent updates
        sub_block.add_update_callback(lambda _: self._notify_update())
        self._notify_update()
    
    async def start_mock_simulation(self, scenario: str = "default") -> None:
        """Start mock data simulation for this block."""
        if self._is_simulating:
            return
        
        self._is_simulating = True
        self._simulation_task = asyncio.create_task(
            self._run_mock_simulation(scenario)
        )
    
    async def _run_mock_simulation(self, scenario: str) -> None:
        """Run mock simulation based on scenario."""
        try:
            if scenario == "cognition":
                await self._simulate_cognition_block()
            elif scenario == "assistant_response":
                await self._simulate_assistant_response()
            elif scenario == "tool_execution":
                await self._simulate_tool_execution()
            else:
                await self._simulate_basic_block()
        except asyncio.CancelledError:
            pass
        finally:
            self._is_simulating = False
    
    async def _simulate_cognition_block(self) -> None:
        """Simulate cognition block with sub-modules."""
        # Start with progress
        self.update_content("🧠 Starting cognition pipeline...")
        self.update_progress(0.1)
        await asyncio.sleep(0.5)
        
        # Sub-module 1: Route Query
        route_block = LiveBlock("sub_module", "🎯 Analyzing query intent...")
        self.add_sub_block(route_block)
        await route_block.start_mock_simulation("route_query")
        await asyncio.sleep(1.0)
        
        # Sub-module 2: Tool Selection
        tool_block = LiveBlock("sub_module", "🛠️ Selecting appropriate tools...")
        self.add_sub_block(tool_block)
        await tool_block.start_mock_simulation("tool_selection")
        await asyncio.sleep(1.5)
        
        # Sub-module 3: Response Generation
        response_block = LiveBlock("sub_module", "📝 Generating response...")
        self.add_sub_block(response_block)
        await response_block.start_mock_simulation("response_generation")
        await asyncio.sleep(2.0)
        
        # Final update
        self.update_content("🧠 Cognition pipeline completed")
        self.update_progress(1.0)
        self.update_tokens(input_tokens=15, output_tokens=3)
    
    async def _simulate_assistant_response(self) -> None:
        """Simulate streaming assistant response."""
        base_responses = [
            "I'll help you with that. Let me break this down step by step:\n\n",
            "1. First, we need to understand the core requirements\n",
            "2. Then we can design the appropriate solution\n",
            "3. Finally, we'll implement and test the result\n\n",
            "Based on your request, here's what I recommend:\n\n",
            "```python\n# Example implementation\ndef solve_problem():\n    return 'solution'\n```\n\n",
            "This approach ensures we maintain clarity while achieving the desired outcome."
        ]
        
        for i, response_chunk in enumerate(base_responses):
            self.append_content(response_chunk)
            self.update_progress((i + 1) / len(base_responses))
            self.update_tokens(output_tokens=len(response_chunk.split()))
            await asyncio.sleep(0.3 + (i * 0.1))  # Variable timing
    
    def stop_simulation(self) -> None:
        """Stop any running mock simulation."""
        if self._simulation_task and not self._simulation_task.done():
            self._simulation_task.cancel()
        self._is_simulating = False
    
    def to_inscribed_block(self) -> 'InscribedBlock':
        """Convert to inscribed block (immutable)."""
        if self.state == BlockState.INSCRIBED:
            raise ValueError("Block already inscribed")
        
        self.state = BlockState.TRANSITIONING
        self._notify_update()
        
        # Stop any simulation
        self.stop_simulation()
        
        # Create inscribed block
        inscribed = InscribedBlock(
            id=self.id,
            role=self.role,
            content=self.data.content,
            timestamp=self.created_at,
            metadata={
                **self.data.metadata,
                "wall_time_seconds": self.data.wall_time_seconds,
                "tokens_input": self.data.tokens_input,
                "tokens_output": self.data.tokens_output,
                "sub_blocks": [block.to_dict() for block in self.data.sub_blocks]
            }
        )
        
        self.state = BlockState.INSCRIBED
        self._notify_update()
        
        return inscribed

@dataclass
class InscribedBlock:
    """Immutable block permanently added to Sacred Timeline."""
    id: str
    role: str
    content: str
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }
```

### Live Block Manager
```python
class LiveBlockManager:
    """Manages live blocks before timeline inscription."""
    
    def __init__(self):
        self.live_blocks: Dict[str, LiveBlock] = {}
        self.block_update_callbacks: List[Callable] = []
        
    def create_live_block(self, role: str, initial_content: str = "") -> LiveBlock:
        """Create a new live block."""
        block = LiveBlock(role, initial_content)
        self.live_blocks[block.id] = block
        
        # Add callback to notify when block updates
        block.add_update_callback(self._on_block_update)
        
        return block
    
    def _on_block_update(self, block: LiveBlock) -> None:
        """Handle live block updates."""
        for callback in self.block_update_callbacks:
            callback(block)
    
    def add_block_update_callback(self, callback: Callable) -> None:
        """Add callback for live block updates."""
        self.block_update_callbacks.append(callback)
    
    def inscribe_block(self, block_id: str) -> Optional[InscribedBlock]:
        """Convert live block to inscribed block."""
        if block_id not in self.live_blocks:
            return None
        
        live_block = self.live_blocks[block_id]
        inscribed_block = live_block.to_inscribed_block()
        
        # Remove from live blocks
        del self.live_blocks[block_id]
        
        return inscribed_block
    
    def get_live_blocks(self) -> List[LiveBlock]:
        """Get all current live blocks."""
        return list(self.live_blocks.values())
    
    def stop_all_simulations(self) -> None:
        """Stop all mock simulations."""
        for block in self.live_blocks.values():
            block.stop_simulation()
```

### Mock Scenario Generator
```python
class MockScenarioGenerator:
    """Generates realistic mock scenarios for different conversation types."""
    
    @staticmethod
    async def create_coding_conversation(live_manager: LiveBlockManager) -> List[LiveBlock]:
        """Create mock coding conversation."""
        blocks = []
        
        # User question
        user_block = live_manager.create_live_block("user", "How do I implement a binary search tree in Python?")
        blocks.append(user_block)
        
        # Cognition processing
        cognition_block = live_manager.create_live_block("cognition")
        await cognition_block.start_mock_simulation("cognition")
        blocks.append(cognition_block)
        
        # Assistant response
        assistant_block = live_manager.create_live_block("assistant")
        await assistant_block.start_mock_simulation("assistant_response")
        blocks.append(assistant_block)
        
        return blocks
    
    @staticmethod
    async def create_debugging_session(live_manager: LiveBlockManager) -> List[LiveBlock]:
        """Create mock debugging session."""
        blocks = []
        
        # Error report
        user_block = live_manager.create_live_block("user", 
            "I'm getting a KeyError in my dictionary lookup. Here's the traceback: ...")
        blocks.append(user_block)
        
        # Analysis
        cognition_block = live_manager.create_live_block("cognition")
        await cognition_block.start_mock_simulation("cognition")
        blocks.append(cognition_block)
        
        # Tool execution (mock)
        tool_block = live_manager.create_live_block("tool", "Analyzing stack trace...")
        await tool_block.start_mock_simulation("tool_execution")
        blocks.append(tool_block)
        
        return blocks
```

## Textual UI Integration

### Live Block Widget
```python
from textual.widgets import Static
from textual.containers import Vertical
from rich.text import Text
from rich.progress import Progress

class LiveBlockWidget(Vertical):
    """Widget for displaying live blocks with real-time updates."""
    
    def __init__(self, live_block: LiveBlock, **kwargs):
        super().__init__(**kwargs)
        self.live_block = live_block
        self.content_widget = Static()
        self.progress_widget = Static()
        self.metadata_widget = Static()
        
        # Subscribe to block updates
        self.live_block.add_update_callback(self._on_block_update)
        
        self.compose()
    
    def compose(self):
        yield self.content_widget
        yield self.progress_widget  
        yield self.metadata_widget
    
    def _on_block_update(self, block: LiveBlock) -> None:
        """Update widget when block data changes."""
        self.update_content()
        self.update_progress()
        self.update_metadata()
    
    def update_content(self) -> None:
        """Update content display."""
        content = Text()
        
        # Add role indicator
        role_indicator = self._get_role_indicator()
        content.append(f"{role_indicator} ", style="bold")
        
        # Add state indicator
        if self.live_block.state == BlockState.LIVE:
            content.append("● ", style="green")  # Live indicator
        elif self.live_block.state == BlockState.TRANSITIONING:
            content.append("⧗ ", style="yellow")  # Transitioning
        else:
            content.append("◉ ", style="blue")  # Inscribed
        
        # Add content
        content.append(self.live_block.data.content)
        
        self.content_widget.update(content)
    
    def update_progress(self) -> None:
        """Update progress display."""
        if self.live_block.state == BlockState.LIVE and self.live_block.data.progress > 0:
            progress_text = Text()
            progress_text.append("Progress: ")
            
            # Simple progress bar
            bar_length = 20
            filled = int(self.live_block.data.progress * bar_length)
            bar = "█" * filled + "░" * (bar_length - filled)
            progress_text.append(f"[{bar}] {self.live_block.data.progress:.1%}", style="dim")
            
            self.progress_widget.update(progress_text)
        else:
            self.progress_widget.update("")
    
    def update_metadata(self) -> None:
        """Update metadata display."""
        metadata_text = Text()
        
        # Timing
        if self.live_block.data.wall_time_seconds > 0:
            metadata_text.append(f"⏱️ {self.live_block.data.wall_time_seconds:.1f}s ")
        
        # Tokens
        if self.live_block.data.tokens_input > 0 or self.live_block.data.tokens_output > 0:
            metadata_text.append(
                f"🎯 {self.live_block.data.tokens_input}↑/{self.live_block.data.tokens_output}↓ ",
                style="dim"
            )
        
        self.metadata_widget.update(metadata_text)
    
    def _get_role_indicator(self) -> str:
        """Get indicator emoji for block role."""
        indicators = {
            "user": "👤",
            "assistant": "🤖", 
            "cognition": "🧠",
            "tool": "🛠️",
            "system": "⚙️",
            "sub_module": "└─"
        }
        return indicators.get(self.live_block.role, "•")
```

## Testing Strategy

### Unit Tests
- [ ] Live block state transitions
- [ ] Mock simulation scenarios
- [ ] LiveBlockManager functionality
- [ ] Widget update callbacks

### Integration Tests
- [ ] Live → inscribed transitions in timeline
- [ ] Multiple simultaneous live blocks
- [ ] Nested sub-block scenarios
- [ ] UI responsiveness with many live blocks

### Manual Testing
- [ ] Various mock scenarios (coding, debugging, research)
- [ ] Live block animation smoothness
- [ ] Transition visual quality
- [ ] Performance with 10+ live blocks

## Success Metrics

### Performance Targets
- Live block updates at 60fps smoothness
- < 100ms latency for state transitions
- Handle 20+ simultaneous live blocks without lag

### UX Validation
- Users understand live vs inscribed concept intuitively
- Transitions feel natural and informative
- Mock scenarios create compelling demonstration

## Documentation Updates

- [ ] Live vs inscribed block concept guide
- [ ] Mock scenario development guide
- [ ] Widget development for live blocks
- [ ] Performance optimization recommendations

## Completion

### Final Status
- [ ] Live blocks animate convincingly with realistic mock data
- [ ] Seamless live → inscribed transitions implemented
- [ ] LiveBlockManager handles transient state properly
- [ ] UI demonstrates Sacred Timeline transparency concept
- [ ] Performance validated with complex scenarios

### Follow-up Items
- [ ] Additional mock scenarios for different domains
- [ ] Advanced animation and transition effects
- [ ] User interaction with live blocks (pause, speed control)
- [ ] Integration with real plugin system (V3.2+)

---

*This ledger establishes the core Sacred Timeline concept through compelling live vs inscribed block demonstrations using sophisticated mock data.*