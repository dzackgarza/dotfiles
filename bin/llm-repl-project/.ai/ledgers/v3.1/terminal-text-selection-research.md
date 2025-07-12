# Terminal Text Selection Research Ledger

**Problem Statement**: Users cannot select and copy text from timeline blocks in our Textual TUI application, which breaks fundamental terminal expectations.

**Core Requirements**:
1. Click anywhere, drag anywhere text selection (terminal cursor behavior)
2. Ctrl+Shift+C clipboard integration 
3. Preserve rich markdown rendering capabilities
4. Maintain Sacred Timeline architecture integrity
5. Support selection across block boundaries

**Research Status**: IN PROGRESS

## Research Questions

### 1. Framework-Level Text Selection
- **Q**: How does Textual handle mouse events vs terminal native selection?
- **Q**: Can Textual widgets be made truly selectable without breaking layout?
- **Q**: What is the relationship between application mode and text selection?
- **Q**: Are there Textual configuration options for text selection behavior?

### 2. Widget Architecture Analysis
- **Q**: Which Textual widgets support native text selection?
- **Q**: How do RichLog, TextArea, Static, and other widgets handle selection?
- **Q**: Can we create custom selectable widgets that preserve our layout?
- **Q**: What are the size/layout implications of different widget types?

### 3. Terminal Integration
- **Q**: How do other successful TUI apps (htop, vim, etc.) handle text selection?
- **Q**: Can we run in a hybrid mode that preserves terminal selection?
- **Q**: What terminal emulator features affect text selection in TUI apps?
- **Q**: Is there a way to delegate selection to the terminal while keeping rich UI?

### 4. Alternative Approaches
- **Q**: Can we implement "copy mode" like tmux/screen?
- **Q**: Is there a way to extract raw text representation for clipboard?
- **Q**: Can we use keyboard shortcuts to copy structured data?
- **Q**: Should we consider inline mode vs application mode?

## Research Findings

### Framework Behavior
- **Finding**: Textual's application mode captures all mouse events, preventing terminal selection
- **Finding**: Static widgets are display-only, not interactive
- **Finding**: RichLog widgets have different sizing behavior that breaks layout
- **Finding**: Mouse event overrides don't restore terminal selection

### Widget Compatibility
- **Finding**: Most Textual widgets prioritize UI interaction over text selection
- **Finding**: Layout and sizing are tightly coupled to widget type
- **Finding**: Rich content rendering and text selection seem mutually exclusive

## Hypotheses to Test

### H1: Inline Mode Solution
**Hypothesis**: Running in inline mode preserves terminal text selection
**Test**: Modify main.py to use app.run(inline=True)
**Prediction**: Text selection works but layout changes dramatically
**Status**: PENDING

### H2: Custom Widget Solution  
**Hypothesis**: We can create custom widgets that support both rich rendering and selection
**Test**: Extend Static widget with selection capabilities
**Prediction**: Complex but potentially viable
**Status**: PENDING

### H3: Copy Mode Solution
**Hypothesis**: Implement a toggle mode for text selection like tmux
**Test**: Add keyboard shortcut to enter/exit copy mode
**Prediction**: User-friendly but requires learning new interaction
**Status**: PENDING

### H4: Terminal Detection Solution
**Hypothesis**: Different terminals have different capabilities we can leverage
**Test**: Detect terminal type and adjust behavior accordingly
**Prediction**: Fragmented solution but might work for common cases
**Status**: PENDING

## Test Plan

### Phase 1: Framework Research
1. Test inline mode behavior and layout implications
2. Research Textual documentation for text selection APIs
3. Analyze source code of successful TUI applications
4. Test different terminal emulators with our app

### Phase 2: Widget Experiments
1. Test all Textual widgets for selection behavior
2. Experiment with widget composition for hybrid solutions
3. Create minimal test cases for each approach
4. Measure performance and layout impact

### Phase 3: Implementation Prototypes
1. Build proof-of-concept for top 2 approaches
2. Test with real timeline content and markdown
3. Verify clipboard integration works correctly
4. Test across different terminal environments

## Success Criteria

### Must Have
- [ ] Click anywhere, drag anywhere text selection
- [ ] Ctrl+Shift+C copies to system clipboard
- [ ] No regression in visual layout or rich content
- [ ] Works across timeline block boundaries
- [ ] Maintains Sacred Timeline architecture

### Should Have  
- [ ] Works in major terminal emulators (kitty, alacritty, gnome-terminal)
- [ ] Preserves markdown formatting in copied text
- [ ] Intuitive user experience (no learning curve)
- [ ] Good performance with large timelines

### Could Have
- [ ] Smart selection of code blocks, structured data
- [ ] Multiple selection modes (text, block, structured)
- [ ] Export timeline to various formats
- [ ] Integration with terminal multiplexers

## Implementation Strategy

### Selected Approach: TBD
**Rationale**: [To be determined after research completion]
**Implementation Plan**: [To be written after approach selection]
**Risk Assessment**: [To be evaluated after prototyping]

## Notes and Observations

- Terminal text selection is a fundamental UX expectation
- The tension between rich UI and terminal native behavior is real
- Textual framework prioritizes modern UI over terminal compatibility
- Most TUI frameworks face this same challenge
- Solution may require framework-level changes or creative workarounds

## Next Actions

1. **Research Phase**: Complete systematic testing of all hypotheses
2. **Documentation Review**: Deep dive into Textual docs and source code
3. **Community Research**: Check Textual Discord/GitHub for similar issues
4. **Prototype Development**: Build minimal test cases for viable approaches
5. **Decision Point**: Choose implementation approach based on research findings

---

**Status**: Research in progress - systematic investigation required before implementation
**Owner**: AI Agent
**Timeline**: Research phase should complete before any implementation attempts
**Dependencies**: Textual framework documentation, terminal behavior analysis