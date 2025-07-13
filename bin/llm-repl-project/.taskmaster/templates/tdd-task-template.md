# TDD Task Template - Sacred GUI Project

## Task Information
- **Task ID**: [AUTO-GENERATED]
- **Title**: [TASK TITLE]
- **Priority**: [high/medium/low]
- **Dependencies**: [LIST TASK IDS]

## Description
[Brief description of what this task accomplishes]

## TDD Requirements (MANDATORY)

### User Story Definition
**Story ID**: task_[ID]_[brief_description]
**Title**: [User interaction being validated]
**Description**: [Complete user interaction scenario]

### 12-Step User Story Flow
1. **Launch**: [Initial app state]
2. **Focus**: [User attention/preparation]
3. **Input**: [User action/input]
4. **Submit**: [User triggers action]
5. **Process Start**: [System begins response]
6. **Active**: [Processing becomes visible]
7. **Working**: [Active processing indicators]
8. **Streaming**: [Content/response flows]
9. **Complete**: [Processing finishes]
10. **Collapse**: [Workspace/indicators hide]
11. **Updated**: [Interface reflects changes]
12. **Ready**: [Ready for next interaction]

### Acceptance Criteria
- [ ] [Specific visual outcome 1]
- [ ] [Specific behavioral outcome 2]
- [ ] [Sacred GUI behavior requirement 3]
- [ ] [Timeline/Workspace/Input interaction 4]

### TDD Workflow Checklist
- [ ] Generated user story before implementation: `task-master generate-story --id=[ID]`
- [ ] Verified story fails initially: `task-master test-story --id=[ID]`
- [ ] Implemented feature to satisfy story
- [ ] Verified story passes: `task-master test-story --id=[ID]`
- [ ] Generated temporal grid: `debug_screenshots/task_[ID]_temporal_grid.png`
- [ ] Completed with story proof: `task-master complete-with-story --id=[ID]`

## Implementation Details
[Technical implementation specifics]

## Test Strategy
[How to verify the implementation works]

## Notes
- **⚠️ CRITICAL**: This task CANNOT be marked complete without user story validation
- **📸 REQUIRED**: Must generate 4x3 temporal grid showing complete user interaction flow
- **🎯 FOCUS**: Story must demonstrate Sacred GUI behavior (Timeline/Workspace/Input areas)
- **🔄 WORKFLOW**: Follow TDD checklist exactly - no shortcuts allowed

## Files Modified
- [ ] [List files that will be changed]
- [ ] [Include test files created]
- [ ] [Include story files generated]

---
*This template enforces TDD through visual user story validation*