# Task Master Quick Reference

## Natural Language Commands for Claude Code

### Task Discovery
```
"What tasks are available to work on next?"
"Show me the next task I should work on"
"Can you show me tasks 1, 3, and 5 to understand their status?"
"List all pending tasks"
```

### Task Implementation
```
"Let's implement task 3. What does it involve?"
"Show me the details for task 5"
"I want to work on the Sacred GUI layout task"
"Break down task 5 into subtasks with security focus"
```

### Progress Updates
```
"Task 3 is complete. Please update its status"
"Mark task 2 as in-progress"
"I've finished the PromptInput widget implementation"
"Update task 5.2 with implementation notes: [details]"
```

### Project Evolution
```
"We decided to use MongoDB instead of PostgreSQL. Update all future tasks from ID 4"
"I think subtask 5.2 would fit better as part of task 7 instead"
"The Textual approach worked better than expected. Update remaining UI tasks"
"Research current best practices for async event handling in Textual"
```

## Direct CLI Commands

### Daily Workflow
```bash
task-master next                              # Get next task
task-master show 3                           # View task details
task-master list                             # Show all tasks
task-master set-status --id=3 --status=done # Complete task
```

### Task Management
```bash
# Add implementation notes
task-master update-subtask --id=3.1 --prompt="Implemented with Textual color system"

# Update multiple future tasks
task-master update --from=6 --prompt="Use Textual built-in persistence utilities"

# Break down complex tasks
task-master expand --id=5 --research --prompt="Focus on Textual best practices"

# Move tasks around
task-master move --from=5.2 --to=7.3
```

### Analysis & Planning
```bash
task-master analyze-complexity --research     # Analyze all tasks
task-master complexity-report                # View analysis results
task-master expand --all --research          # Break down all complex tasks
task-master validate-dependencies            # Check task dependencies
```

## Current Project Status

### Generated Tasks (10 total)
1. **Initialize Project with PDM** - Setup virtual environment
2. **Implement Sacred GUI Layout** - Three-area layout (Timeline/Workspace/Input)
3. **Create SimpleBlockWidget** - Timeline entries with color coding
4. **Build PromptInput Widget** - Multiline input with validation
5. **Implement Basic Conversation Flow** - User → Cognition → Assistant
6. **Add Persistent Timeline Storage** - Session restoration
7. **Implement Turn Lifecycle Management** - State switching (2-way/3-way split)
8. **Auto-Scroll and Content-Driven Sizing** - Timeline UI polish
9. **Create Error Boundary System** - Graceful failure handling
10. **Build SubModuleWidget** - Cognition step visualization

### Model Configuration
- **Main**: Google Gemini 2.0 Flash
- **Fallback**: OpenRouter DeepSeek (free tier)
- **Research**: Not configured (would need Perplexity API key)

### Integration Points
- **MCP Server**: Active through `.mcp.json`
- **Claude Code**: Integrated via `CLAUDE.md`
- **Documentation**: `.ai/task-master-integration-guide.md`

## Best Practices

### 1. Log Implementation Details
Always update subtasks with what you learned:
```bash
task-master update-subtask --id=3.1 --prompt="Used Rich markup for dynamic colors. Textual's color system handles terminal compatibility automatically."
```

### 2. Research When Stuck
Use research mode for complex decisions:
```bash
task-master expand --id=5 --research --prompt="Best practices for async widget communication in Textual framework"
```

### 3. Update Future Tasks
When you discover better approaches:
```bash
task-master update --from=8 --prompt="Textual provides built-in scroll behavior. Simplify auto-scroll implementation."
```

### 4. Natural Language First
Let Claude Code translate natural requests to commands:
- More intuitive and conversational
- Handles context and dependencies automatically
- Provides explanations and guidance

## File Locations

- **Tasks Database**: `.taskmaster/tasks/tasks.json`
- **Individual Tasks**: `.taskmaster/tasks/task-*.md`
- **Configuration**: `.taskmaster/config.json`
- **MCP Setup**: `.mcp.json`
- **Claude Integration**: `CLAUDE.md`
- **Documentation**: `.ai/task-master-*.md`

## Emergency Commands

```bash
# If tasks.json gets corrupted
task-master generate                    # Regenerate task files

# If dependencies are broken
task-master fix-dependencies           # Auto-fix dependency issues

# If you need to start over (RARELY needed)
task-master validate-dependencies      # Check first
```

Remember: Task Master works best through natural conversation with Claude Code. Let the AI handle the command translation and provide context and guidance!