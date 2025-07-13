# Scroll-Stealing Fix

## User Story

From the conversation:
> "the user can not currently scroll the timeline up at all, it snaps to the bottom. Now, we DO want the timeline to autoscroll in most obvious cases. However, we do not want to 'steal' the focus from the user if they are scrolling up to review history."

And critically:
> "the user can not scroll while updates are happening, the timeline is quickly snapped back to the bottom. This is behaviour we can't have."

## Problem Statement

Users cannot scroll the timeline while updates are happening - the timeline is quickly snapped back to the bottom. This happens because:

1. **10Hz timer updates**: CognitionProgress runs a timer at 10Hz that triggers callbacks
2. **No update differentiation**: All updates (progress timers vs content changes) trigger scroll attempts  
3. **Race conditions**: Multiple widgets independently trigger scrolls with different timing logic

## Root Cause Analysis

The fundamental issue is architectural - we're mixing different types of updates:
- **Progress updates**: 10Hz timer ticks, token counter increments (should NOT trigger scrolls)
- **Content updates**: New blocks, meaningful content changes (SHOULD trigger scrolls when appropriate)

Currently both types flow through the same callback chain, causing 10+ scroll attempts per second during cognition blocks.

## Solution Design

### 1. Separate Callback Types

Split LiveBlock callbacks into two distinct types:
- `content_update_callbacks`: For meaningful changes that may trigger scrolls
- `progress_update_callbacks`: For visual-only updates (timers, progress bars)

### 2. Update CognitionProgress Integration

Currently CognitionProgress timer updates trigger content callbacks. Fix:
- Route timer updates through progress callbacks only
- Keep content callbacks for structural changes (new sub-blocks)

### 3. Widget-Level Scroll Control

- Progress callbacks update display but never trigger scrolls
- Content callbacks can trigger scrolls based on user intent
- Remove timing-based throttling in favor of proper event routing

## Implementation Steps

### Step 1: Update LiveBlock callback system
```python
# In live_blocks.py
class LiveBlock:
    def __init__(self, role: str, initial_content: str = ""):
        # Split callbacks by type
        self.content_update_callbacks: List[Callable] = []  
        self.progress_update_callbacks: List[Callable] = []
        
    def add_update_callback(self, callback: Callable) -> None:
        """Content updates - can trigger scrolls"""
        self.content_update_callbacks.append(callback)
        
    def add_progress_callback(self, callback: Callable) -> None:
        """Progress updates - display only, no scrolls"""
        self.progress_update_callbacks.append(callback)
```

### Step 2: Fix CognitionProgress routing
```python
# In live_blocks.py
def _on_progress_update(self, progress: CognitionProgress) -> None:
    """Route timer updates to progress callbacks only"""
    if self.cognition_progress:
        status_line = self.cognition_progress.get_status_line()
        self.data.content = status_line
        self._notify_progress_update()  # NOT _notify_update()
```

### Step 3: Update widget scroll logic
```python
# In live_block_widget.py
def __init__(self, live_block: LiveBlock, **kwargs):
    # Subscribe to both types
    self.live_block.add_update_callback(self._on_content_update)
    self.live_block.add_progress_callback(self._on_progress_update)
    
def _on_progress_update(self, block: LiveBlock) -> None:
    """Progress updates - no scroll triggering"""
    self._update_all_displays()
    
def _on_content_update(self, block: LiveBlock) -> None:
    """Content updates - can trigger smart scroll"""
    self._update_all_displays()
    # Scroll logic here based on user intent
```

### Step 4: Simplify timeline scroll logic
Remove complex timing/cooldown logic in favor of simpler user intent detection:
- Track if user is "following" (near bottom of timeline)
- Only auto-scroll if user is following
- Grace period after manual scroll

## Research & Common Patterns

This is a classic GUI problem seen in:
- Chat applications (WhatsApp, Discord, Slack)
- Terminal emulators (iTerm2, Windows Terminal)
- Log viewers (tail -f, journalctl --follow)
- Live streaming consoles

Common solutions:
1. **"Sticky bottom" pattern**: Auto-scroll only when already at bottom
2. **"New messages" indicator**: Show button when content added while scrolled up
3. **Pause on interaction**: Any user scroll pauses auto-scroll temporarily
4. **Smart following**: Resume auto-scroll when user returns to bottom

## Expected Behaviors

1. **During cognition blocks**: 10Hz timer updates display smoothly without triggering scrolls
2. **New blocks added**: Auto-scroll only if user is following the conversation
3. **User scrolls up**: Timeline stays put, no scroll-stealing during any updates
4. **User returns to bottom**: Auto-scroll resumes for new content
5. **Live updates continue**: Progress bars, timers, and tokens animate without affecting scroll

## Testing Approach

1. Create test that tracks callback types separately
2. Verify 10Hz timer generates progress callbacks only
3. Verify new blocks generate content callbacks
4. Confirm scroll triggers only on content updates when user is following

## Success Criteria

- [ ] Users can scroll up and review history without interruption
- [ ] Progress animations (timers, tokens) update smoothly  
- [ ] Auto-scroll works for users following the conversation
- [ ] No timing-based hacks or cooldowns needed

## Investigation Summary

From testing with `test_scroll_fix.py`:
- Expected: ~10 progress updates per second, few content updates
- Actual: 42 content updates, 0 progress updates
- Root cause: CognitionProgress timer calls `_notify_update()` which triggers content callbacks

The architectural change is sound, but the implementation is incomplete. The 10Hz timer from CognitionProgress is still flowing through the content callback chain, triggering scroll attempts every 100ms.

## Current Status

Partially implemented:
- ✅ Dual callback system added to LiveBlock
- ✅ Widget subscribes to both callback types
- ✅ Scroll logic separated by callback type
- ❌ CognitionProgress still using content callbacks
- ❌ Need to update LiveBlock's `_on_progress_update` to properly route

The scroll-stealing persists because the most frequent update source (10Hz timer) is still triggering scroll attempts.