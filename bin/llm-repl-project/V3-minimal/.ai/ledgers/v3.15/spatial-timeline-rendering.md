# Spatial Timeline Rendering

## Status: Not Started

## Overview
Implement clear spatial separation in the timeline UI with distinct above-fold (sacred/inscribed) and below-fold (transient/processing) areas.

## Problem Statement
The current timeline mixes live and inscribed blocks without clear visual hierarchy:
- Users can't tell what's processing vs. what's complete
- Blocks jump around as they transition states
- No clear boundary between mutable and immutable sections
- Confusing user experience with blocks appearing/disappearing

## Solution Design
Create explicit spatial areas in the timeline:
1. **Above-fold**: Scrollable history of inscribed blocks (Sacred Timeline)
2. **The fold**: Visual separator (line, gradient, or gap)
3. **Below-fold**: Fixed position for single transient block

This creates a clear metaphor: processing happens below, history lives above.

## User-Visible Behaviors

### 1. Visual Fold Indicator
**Current**: No separation between processing and complete blocks
**New**: Clear visual line/gradient showing the boundary between history and active processing

### 2. Fixed Transient Area
**Current**: Processing blocks appear inline with history
**New**: Below-fold area has fixed position at bottom of viewport, doesn't scroll

### 3. Auto-scroll on Inscription  
**Current**: New blocks may appear off-screen
**New**: Timeline auto-scrolls to show newly inscribed blocks while keeping transient area visible

### 4. Empty State Handling
**Current**: Unclear when no processing is happening
**New**: Below-fold shows subtle placeholder or prompt when empty

### 5. Smooth Spatial Transitions
**Current**: Blocks pop in/out of existence
**New**: Blocks animate smoothly from below-fold to above-fold position

## Technical Implementation

### Timeline Layout Structure
```python
class TimelineWidget(Container):
    """Main timeline container with spatial separation"""
    
    def compose(self) -> ComposeResult:
        # Above-fold: Scrollable history
        yield ScrollableContainer(
            *[BlockWidget(block) for block in self.above_fold_blocks],
            id="above-fold",
            classes="timeline-history"
        )
        
        # The fold: Visual separator
        yield FoldIndicator(
            id="fold-indicator",
            classes="timeline-fold"
        )
        
        # Below-fold: Fixed transient area
        yield TransientContainer(
            self.below_fold_block,
            id="below-fold", 
            classes="timeline-transient"
        )
```

### Fold Indicator Widget
```python
class FoldIndicator(Static):
    """Visual separator between inscribed and transient sections"""
    
    DEFAULT_CSS = """
    FoldIndicator {
        height: 3;
        width: 100%;
        background: linear-gradient(
            to bottom,
            $surface 0%,
            $primary 50%,
            $surface-lighten-1 100%
        );
        border-top: solid $primary-lighten-2;
        border-bottom: solid $primary-lighten-2;
    }
    
    FoldIndicator.processing {
        /* Animate during active processing */
        animation: pulse 2s ease-in-out infinite;
    }
    """
    
    def __init__(self):
        super().__init__()
        self.processing = False
        
    def set_processing(self, active: bool) -> None:
        """Update visual state based on processing"""
        self.processing = active
        self.toggle_class("processing", active)
```

### Transient Container
```python
class TransientContainer(Container):
    """Fixed container for active processing block"""
    
    DEFAULT_CSS = """
    TransientContainer {
        height: auto;
        min-height: 5;
        max-height: 50%;
        dock: bottom;
        background: $surface-lighten-1;
        border: solid $primary-lighten-3;
        padding: 1;
    }
    
    TransientContainer.empty {
        /* Subtle when no processing */
        opacity: 0.7;
        border-style: dashed;
    }
    """
    
    def __init__(self, transient_block: Optional[TransientBlock] = None):
        super().__init__()
        self.transient_block = transient_block
        
    def compose(self) -> ComposeResult:
        if self.transient_block:
            yield TransientBlockWidget(self.transient_block)
        else:
            yield Static(
                "✨ Ready for input...",
                classes="empty-state"
            )
```

### Auto-scroll Behavior
```python
class TimelineWidget:
    async def inscribe_block(self, block: Block) -> None:
        """Move block above-fold with auto-scroll"""
        # Add to above-fold
        self.above_fold_blocks.append(block)
        block_widget = BlockWidget(block)
        await self.query_one("#above-fold").mount(block_widget)
        
        # Auto-scroll to show new block
        await self.query_one("#above-fold").scroll_to_widget(
            block_widget,
            animate=True,
            duration=0.5
        )
        
        # Clear below-fold
        self.below_fold_block = None
        await self.refresh_transient_area()
```

## Acceptance Criteria

### Must Have
- [ ] Clear visual fold indicator between sections
- [ ] Fixed below-fold area that doesn't scroll
- [ ] Auto-scroll to newly inscribed blocks
- [ ] Empty state for inactive transient area
- [ ] Smooth transition animations

### Should Have
- [ ] Fold indicator shows processing state
- [ ] Responsive layout (adjusts to viewport)
- [ ] Keyboard navigation respects spatial model
- [ ] Visual consistency across themes

### Could Have
- [ ] Configurable fold styles
- [ ] Adjustable transient area height
- [ ] Fold collapse/expand animation
- [ ] Different empty state messages

## Test Plan

### Visual Testing
1. Launch app and verify fold indicator visible
2. Enter query and confirm block appears below-fold
3. Watch processing and verify block stays in place
4. Confirm smooth animation to above-fold on completion
5. Verify auto-scroll shows new inscribed block
6. Check empty state appears after inscription

### Layout Testing
- Test with different viewport sizes
- Verify responsive behavior
- Confirm fixed positioning of transient area
- Test with many blocks above-fold

### Animation Testing
- Verify smooth transitions
- No visual glitches during inscription
- Proper timing on animations

## Dependencies
- Requires `unified-timeline-ownership` 
- Works with `transient-block-architecture`
- Enables `atomic-inscription-system`

## CSS Theme Variables
```css
/* Add to theme */
--timeline-fold-height: 3;
--timeline-transient-min-height: 5;
--timeline-transient-max-height: 50%;
--timeline-fold-gradient: linear-gradient(...);
--timeline-inscription-duration: 0.5s;
```

## Notes
This spatial model provides the clear visual metaphor users need to understand what's happening in the system. The fixed below-fold area eliminates confusion about where processing occurs.