# User Story Generation Prompt Template

Use this template when generating user stories for tasks with `task-master generate-story`.

## Template Format

```bash
task-master generate-story --id=[TASK_ID] --prompt="[USER_INTERACTION_DESCRIPTION]"
```

## Example Prompts by Task Type

### Layout/UI Tasks
```bash
task-master generate-story --id=2 --prompt="User launches app and sees Sacred GUI layout with three distinct areas: Timeline at top showing empty state, collapsed Workspace in middle, and Input area at bottom ready for typing"
```

### Conversation Flow Tasks  
```bash
task-master generate-story --id=5 --prompt="User types first message, sees cognition processing with visual indicators, receives assistant response, and timeline updates to show complete conversation"
```

### State Management Tasks
```bash
task-master generate-story --id=7 --prompt="User triggers processing and sees app transition from 2-way split (Timeline + Input) to 3-way split (Timeline + Workspace + Input) during processing, then back to 2-way split when complete"
```

### Error Handling Tasks
```bash
task-master generate-story --id=9 --prompt="User encounters error condition, sees clear error message with recovery options, takes corrective action, and successfully continues with normal operation"
```

### Widget/Component Tasks
```bash
task-master generate-story --id=3 --prompt="User sees timeline blocks with proper color coding: blue for user input, green for cognition processing, and purple for assistant responses, with clear visual distinctions"
```

## Story Requirements Checklist

Every generated story must demonstrate:
- [ ] **Sacred GUI Architecture**: Timeline/Workspace/Input areas visible
- [ ] **User Interaction**: Real user actions, not system events
- [ ] **Visual Proof**: Each step shows expected UI state
- [ ] **Complete Flow**: 12 steps from launch to ready-for-next
- [ ] **Error Handling**: Graceful handling of edge cases
- [ ] **Responsive Behavior**: Smooth transitions and animations

## Temporal Grid Validation

The generated story will create a 4x3 temporal grid showing:
```
Step 1  | Step 2  | Step 3  | Step 4
Step 5  | Step 6  | Step 7  | Step 8  
Step 9  | Step 10 | Step 11 | Step 12
```

Verify grid shows:
- **Smooth progression** between steps
- **Sacred GUI behavior** in all relevant steps
- **Proper state transitions** (idle ↔ processing)
- **Visual consistency** throughout flow
- **Error recovery** if applicable

## Common Story Patterns

### Basic Interaction Pattern
1. **Launch** → Clean app start
2. **Focus** → User clicks input
3. **Input** → User types message
4. **Submit** → User presses Enter
5. **Process Start** → System begins
6. **Active** → Processing visible
7. **Working** → Indicators active
8. **Streaming** → Response flows
9. **Complete** → Processing done
10. **Collapse** → Workspace hides
11. **Updated** → Timeline shows result
12. **Ready** → Input ready again

### Error Recovery Pattern
1. **Normal** → App in good state
2. **Problem Input** → User enters problematic data
3. **Submit Bad** → User submits bad input
4. **Error Processing** → System detects error
5. **Error Display** → Error message shown
6. **User Sees** → User notices error
7. **Recovery Action** → User takes corrective action
8. **Good Input** → User enters valid data
9. **Recovery Submit** → User resubmits
10. **Normal Processing** → System processes normally
11. **Success Response** → Good response received
12. **Recovered** → App back to normal state

Use these patterns as starting points for your specific task stories.

---
*Generate stories that prove features work through real user interaction*