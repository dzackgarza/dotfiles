# User Stories Testing Framework

## Overview

The canonical pilot test uses **user stories** to validate Sacred GUI behavior through visual proof. Each story captures a complete user interaction journey as a 4x3 temporal grid showing state transitions over time.

## What are User Stories?

User stories are structured sequences of 12 interactions that represent real user behavior:

1. **Launch** - App starts, initial state
2. **Focus** - User attention on input field  
3. **Input** - User types message
4. **Submit** - User presses Enter
5. **Process Start** - System begins response
6. **Active** - Live workspace becomes visible
7. **Working** - Processing indicators active
8. **Streaming** - Response content flows in
9. **Complete** - Processing finishes
10. **Collapse** - Workspace hides automatically
11. **Updated** - Timeline shows conversation
12. **Ready** - Input ready for next interaction

## How to Run User Stories

### Run All Stories
```bash
# Run the full canonical test with all user stories
pdm run pytest tests/test_canonical_pilot.py::test_canonical_user_journey -v
```

### View Results
After running, check the `debug_screenshots/` directory for temporal grids:
- `{story_id}_temporal_grid_{timestamp}.png` - 4x3 grid showing all 12 steps
- Each grid provides visual proof of Sacred GUI behavior

## Creating New User Stories

### 1. Define Your Story

First, identify what user behavior you want to test:

```python
# Example: Testing error recovery
story_id = "error_recovery"
title = "User recovers from connection error gracefully"
```

### 2. Create Story Steps

Add to `tests/user_stories.py`:

```python
async def get_error_recovery_story(pilot):
    """User encounters error and recovers successfully"""
    
    return UserStory(
        id="error_recovery", 
        title="Error Recovery Flow",
        steps=[
            # Define your 12 steps here
            UserStep("01_launch", "App launches normally", 
                     lambda: pilot.pause(0.5)),
            UserStep("02_focus", "User focuses input", 
                     lambda: pilot.click("#prompt-input")),
            # ... continue with 12 total steps
        ]
    )
```

### 3. Register Your Story

Add the story to the available stories list:

```python
def list_available_stories():
    return [
        "basic_interaction",
        "error_recovery",  # <- Add your new story
        "multi_turn_conversation"
    ]
```

### 4. Implement Story Logic

Each step should:
- Perform ONE specific user action
- Return a descriptive screenshot name
- Advance the story naturally toward the next state

```python
async def submit_message():
    await pilot.press("enter")
    await pilot.pause(0.5)  # Let processing start
    return "04_submit_message_processing_starts"
```

## Story Validation Guidelines

### Each Story Must:
- Have exactly 12 steps (for 4x3 temporal grid)
- Cover one complete user interaction cycle
- Start from a known initial state
- End in a state ready for next interaction
- Test ONE specific behavior pattern

### Timing Best Practices:
- Use `pilot.pause()` to let state transitions complete
- Test at human-like interaction speeds
- Allow processing time for async operations
- Capture state AFTER actions complete

## Interpreting Temporal Grids

### Grid Layout:
```
Step 1  | Step 2  | Step 3  | Step 4
Step 5  | Step 6  | Step 7  | Step 8  
Step 9  | Step 10 | Step 11 | Step 12
```

### What to Look For:
- **Smooth transitions** - No jarring visual jumps
- **Proper state flow** - Each step follows logically
- **Sacred Architecture** - Timeline/Workspace/Input visible
- **Visual consistency** - Styling and layout maintained
- **Error states** - Graceful handling of problems

### Common Issues:
- Missing workspace visibility in steps 6-9
- Timeline not updating in step 11
- Input field not ready in step 12
- Processing indicators stuck in steps 7-8

## Using Stories for Feature Development

### Before Implementing Features:
1. Create a user story that demonstrates the desired behavior
2. Run the story - it should fail or show incomplete behavior
3. Implement the feature
4. Run the story again - it should now pass with complete visual flow

### Story-Driven Development:
```bash
# 1. Create failing story
pdm run pytest tests/test_canonical_pilot.py -k "new_feature" -v

# 2. Implement feature code
# ... make changes to src/ ...

# 3. Verify story now passes
pdm run pytest tests/test_canonical_pilot.py -k "new_feature" -v

# 4. Check temporal grid shows complete flow
ls debug_screenshots/new_feature_temporal_grid_*.png
```

## Technical Details

### Screenshot Architecture:
- Screenshots taken in SVG format (vector graphics)
- Converted to PNG for temporal grid creation
- Individual screenshots NOT saved to disk (only grids)
- PIL used for grid composition with labels

### Dependencies:
- `cairosvg` - SVG to PNG conversion
- `PIL` (Pillow) - Image grid creation
- `pytest` - Test framework
- Textual's test harness for app simulation

### Grid Metadata:
- Timestamp in filename for version tracking
- Step labels show interaction type and expected state
- 4x3 layout optimized for Sacred GUI's 3-area architecture
- High resolution for detailed visual inspection

## Troubleshooting

### No Screenshots Generated:
- Check `cairosvg` installation: `pdm add cairosvg`
- Verify PIL available: `pdm add pillow`
- Ensure test runs with `-v` flag for verbose output

### Grid Creation Fails:
- Confirm exactly 12 steps in story
- Check that story steps return proper screenshot names
- Verify `debug_screenshots/` directory exists and is writable

### Story Doesn't Match Expected Behavior:
- Add more `pilot.pause()` calls for state transitions
- Check timing - some actions need longer to complete
- Verify story logic matches actual user interaction patterns
- Use temporal grid to identify where flow breaks down

---

**Remember**: User stories are visual proof of Sacred GUI behavior. They should capture real user interactions, not internal implementation details.