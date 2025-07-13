# Task Master AI - Claude Code Integration Guide

## Essential Commands

### Core Workflow Commands

```bash
# Project Setup
task-master init                                    # Initialize Task Master in current project
task-master parse-prd .taskmaster/docs/prd.txt      # Generate tasks from PRD document
task-master models --setup                        # Configure AI models interactively

# Daily Development Workflow
task-master list                                   # Show all tasks with status
task-master next                                   # Get next available task to work on
task-master show <id>                             # View detailed task information (e.g., task-master show 1.2)
task-master set-status --id=<id> --status=done    # Mark task complete

# TDD Workflow Commands (MANDATORY for all task completion)
./task-master-generate-story --id=<id> --prompt="<user_interaction>"    # Generate user story for task
./task-master-test-story --id=<id>                                      # Run user story test with temporal grid
./task-master-validate-task --id=<id>                                   # Validate task meets TDD requirements
./task-master-complete-with-story --id=<id>                             # Complete task with TDD proof

# Task Management
task-master add-task --prompt="description" --research        # Add new task with AI assistance
task-master expand --id=<id> --research --force              # Break task into subtasks
task-master update-task --id=<id> --prompt="changes"         # Update specific task
task-master update --from=<id> --prompt="changes"            # Update multiple tasks from ID onwards
task-master update-subtask --id=<id> --prompt="notes"        # Add implementation notes to subtask

# Analysis & Planning
task-master analyze-complexity --research          # Analyze task complexity
task-master complexity-report                      # View complexity analysis
task-master expand --all --research               # Expand all eligible tasks

# Dependencies & Organization
task-master add-dependency --id=<id> --depends-on=<id>       # Add task dependency
task-master move --from=<id> --to=<id>                       # Reorganize task hierarchy
task-master validate-dependencies                            # Check for dependency issues
task-master generate                                         # Update task markdown files (usually auto-called)
```

## Key Files & Project Structure

### Core Files

- `.taskmaster/tasks/tasks.json` - Main task data file (auto-managed)
- `.taskmaster/config.json` - AI model configuration (use `task-master models` to modify)
- `.taskmaster/docs/prd.txt` - Product Requirements Document for parsing
- `.taskmaster/tasks/*.txt` - Individual task files (auto-generated from tasks.json)
- `.env` - API keys for CLI usage

### Claude Code Integration Files

- `CLAUDE.md` - Auto-loaded context for Claude Code (this file)
- `.claude/settings.json` - Claude Code tool allowlist and preferences
- `.claude/commands/` - Custom slash commands for repeated workflows
- `.mcp.json` - MCP server configuration (project-specific)

### Directory Structure

```
project/
├── .taskmaster/
│   ├── tasks/              # Task files directory
│   │   ├── tasks.json      # Main task database
│   │   ├── task-1.md      # Individual task files
│   │   └── task-2.md
│   ├── docs/              # Documentation directory
│   │   ├── prd.txt        # Product requirements
│   ├── reports/           # Analysis reports directory
│   │   └── task-complexity-report.json
│   ├── templates/         # Template files
│   │   └── example_prd.txt  # Example PRD template
│   └── config.json        # AI models & settings
├── .claude/
│   ├── settings.json      # Claude Code configuration
│   └── commands/         # Custom slash commands
├── .env                  # API keys
├── .mcp.json            # MCP configuration
└── CLAUDE.md            # This file - auto-loaded by Claude Code
```

## MCP Integration

Task Master provides an MCP server that Claude Code can connect to. Configure in `.mcp.json`:

```json
{
  "mcpServers": {
    "task-master-ai": {
      "command": "npx",
      "args": ["-y", "--package=task-master-ai", "task-master-ai"],
      "env": {
        "ANTHROPIC_API_KEY": "your_key_here",
        "PERPLEXITY_API_KEY": "your_key_here",
        "OPENAI_API_KEY": "OPENAI_API_KEY_HERE",
        "GOOGLE_API_KEY": "GOOGLE_API_KEY_HERE",
        "XAI_API_KEY": "XAI_API_KEY_HERE",
        "OPENROUTER_API_KEY": "OPENROUTER_API_KEY_HERE",
        "MISTRAL_API_KEY": "MISTRAL_API_KEY_HERE",
        "AZURE_OPENAI_API_KEY": "AZURE_OPENAI_API_KEY_HERE",
        "OLLAMA_API_KEY": "OLLAMA_API_KEY_HERE"
      }
    }
  }
}
```

### Essential MCP Tools

```javascript
help; // = shows available taskmaster commands
// Project setup
initialize_project; // = task-master init
parse_prd; // = task-master parse-prd

// Daily workflow
get_tasks; // = task-master list
next_task; // = task-master next
get_task; // = task-master show <id>
set_task_status; // = task-master set-status

// Task management
add_task; // = task-master add-task
expand_task; // = task-master expand
update_task; // = task-master update-task
update_subtask; // = task-master update-subtask
update; // = task-master update

// Analysis
analyze_project_complexity; // = task-master analyze-complexity
complexity_report; // = task-master complexity-report
```

## Claude Code Workflow Integration

### Standard Development Workflow

#### 1. Project Initialization

```bash
# Initialize Task Master
task-master init

# Create or obtain PRD, then parse it
task-master parse-prd .taskmaster/docs/prd.txt

# Analyze complexity and expand tasks
task-master analyze-complexity --research
task-master expand --all --research
```

If tasks already exist, another PRD can be parsed (with new information only!) using parse-prd with --append flag. This will add the generated tasks to the existing list of tasks..

#### 2. Daily Development Loop

```bash
# Start each session
task-master next                           # Find next available task
task-master show <id>                     # Review task details

# During implementation, check in code context into the tasks and subtasks
task-master update-subtask --id=<id> --prompt="implementation notes..."

# Complete tasks
task-master set-status --id=<id> --status=done
```

#### 3. Multi-Claude Workflows

For complex projects, use multiple Claude Code sessions:

```bash
# Terminal 1: Main implementation
cd project && claude

# Terminal 2: Testing and validation
cd project-test-worktree && claude

# Terminal 3: Documentation updates
cd project-docs-worktree && claude
```

### Custom Slash Commands

Create `.claude/commands/taskmaster-next.md`:

```markdown
Find the next available Task Master task and show its details.

Steps:

1. Run `task-master next` to get the next task
2. If a task is available, run `task-master show <id>` for full details
3. Provide a summary of what needs to be implemented
4. Suggest the first implementation step
```

Create `.claude/commands/taskmaster-complete.md`:

```markdown
Complete a Task Master task: $ARGUMENTS

Steps:

1. Review the current task with `task-master show $ARGUMENTS`
2. Verify all implementation is complete
3. Run any tests related to this task
4. Mark as complete: `task-master set-status --id=$ARGUMENTS --status=done`
5. Show the next available task with `task-master next`
```

## Tool Allowlist Recommendations

Add to `.claude/settings.json`:

```json
{
  "allowedTools": [
    "Edit",
    "Bash(task-master *)",
    "Bash(git commit:*)",
    "Bash(git add:*)",
    "Bash(npm run *)",
    "mcp__task_master_ai__*"
  ]
}
```

## Configuration & Setup

### API Keys Required

At least **one** of these API keys must be configured:

- `ANTHROPIC_API_KEY` (Claude models) - **Recommended**
- `PERPLEXITY_API_KEY` (Research features) - **Highly recommended**
- `OPENAI_API_KEY` (GPT models)
- `GOOGLE_API_KEY` (Gemini models)
- `MISTRAL_API_KEY` (Mistral models)
- `OPENROUTER_API_KEY` (Multiple models)
- `XAI_API_KEY` (Grok models)

An API key is required for any provider used across any of the 3 roles defined in the `models` command.

### Model Configuration

```bash
# Interactive setup (recommended)
task-master models --setup

# Set specific models
task-master models --set-main claude-3-5-sonnet-20241022
task-master models --set-research perplexity-llama-3.1-sonar-large-128k-online
task-master models --set-fallback gpt-4o-mini
```

## Task Structure & IDs

### Task ID Format

- Main tasks: `1`, `2`, `3`, etc.
- Subtasks: `1.1`, `1.2`, `2.1`, etc.
- Sub-subtasks: `1.1.1`, `1.1.2`, etc.

### Task Status Values

- `pending` - Ready to work on
- `in-progress` - Currently being worked on
- `done` - Completed and verified
- `deferred` - Postponed
- `cancelled` - No longer needed
- `blocked` - Waiting on external factors

### Task Fields

```json
{
  "id": "1.2",
  "title": "Implement user authentication",
  "description": "Set up JWT-based auth system",
  "status": "pending",
  "priority": "high",
  "dependencies": ["1.1"],
  "details": "Use bcrypt for hashing, JWT for tokens...",
  "testStrategy": "Unit tests for auth functions, integration tests for login flow",
  "subtasks": []
}
```

## MANDATORY: Test-Driven Development with User Stories

**⚠️ CRITICAL: ALL TASKS MUST FOLLOW TDD WORKFLOW ⚠️**

This project enforces Test-Driven Development through user story validation. **NO TASK CAN BE MARKED COMPLETE WITHOUT VISUAL STORY PROOF.**

### Required TDD Workflow (NEVER SKIP)

#### 1. Story-First Development (MANDATORY)
```bash
# Step 1: Get your task
task-master next

# Step 2: BEFORE ANY CODING - Generate user story first
./task-master-generate-story --id=<task-id> --prompt="<describe user interaction>"

# Step 3: Verify story fails (shows incomplete/broken behavior)  
./task-master-test-story --id=<task-id>
```

#### 2. Implementation Phase
```bash
# Step 4: Implement feature to satisfy user story
# ... write your code ...

# Step 5: Test story regularly during development
./task-master-test-story --id=<task-id>
```

#### 3. Completion Phase (MANDATORY VALIDATION)
```bash
# Step 6: Story MUST pass before completion
./task-master-test-story --id=<task-id>

# Step 7: Validate task meets all TDD requirements
./task-master-validate-task --id=<task-id>

# Step 8: Complete with story proof (only way to mark done)
./task-master-complete-with-story --id=<task-id>
```

### TDD Commands Available

```bash
# Generate user story template for task
./task-master-generate-story --id=5 --prompt="User starts conversation"

# Run user story for specific task (creates temporal grid proof)
./task-master-test-story --id=5

# Validate task completion with story proof
./task-master-validate-task --id=5

# Complete task with story validation (ONLY way to mark done)
./task-master-complete-with-story --id=5

# Helper: Show help for any command
./task-master-generate-story --help
./task-master-test-story --help
./task-master-validate-task --help
./task-master-complete-with-story --help
```

### Quality Gates (ENFORCED)

- **NO task can be marked `done` without user story validation**
- **All features must be proven through 12-step temporal grid screenshots**  
- **Visual proof required showing complete user interaction flow**
- **Story must demonstrate Sacred GUI behavior (Timeline/Workspace/Input)**

### User Story Requirements

Every task must include:
- **User Story Definition**: Clear 12-step user interaction scenario
- **Acceptance Criteria**: Specific visual/behavioral outcomes expected
- **Temporal Grid**: 4x3 screenshot grid proving story passes
- **Test-First**: Story written and failing BEFORE implementation

## Claude Code Best Practices with Task Master

### Context Management

- Use `/clear` between different tasks to maintain focus
- This CLAUDE.md file is automatically loaded for context
- Use `task-master show <id>` to pull specific task context when needed

### TDD-Enforced Implementation (MANDATORY)

1. `task-master next` - Get next task
2. `task-master generate-story --id=<id>` - **CREATE STORY FIRST**
3. `task-master test-story --id=<id>` - **VERIFY STORY FAILS**
4. `task-master show <id>` - Understand requirements
5. Explore codebase and plan implementation
6. `task-master update-subtask --id=<id> --prompt="detailed plan"` - Log plan
7. `task-master set-status --id=<id> --status=in-progress` - Start work
8. Implement code following logged plan
9. `task-master test-story --id=<id>` - **TEST STORY REGULARLY**
10. `task-master update-subtask --id=<id> --prompt="what worked/didn't work"` - Log progress
11. `task-master test-story --id=<id>` - **STORY MUST PASS**
12. `task-master complete-with-story --id=<id>` - **ONLY WAY TO COMPLETE**

### Complex Workflows with Checklists

For large migrations or multi-step processes:

1. Create a markdown PRD file describing the new changes: `touch task-migration-checklist.md` (prds can be .txt or .md)
2. Use Taskmaster to parse the new prd with `task-master parse-prd --append` (also available in MCP)
3. Use Taskmaster to expand the newly generated tasks into subtasks. Consdier using `analyze-complexity` with the correct --to and --from IDs (the new ids) to identify the ideal subtask amounts for each task. Then expand them.
4. Work through items systematically, checking them off as completed
5. Use `task-master update-subtask` to log progress on each task/subtask and/or updating/researching them before/during implementation if getting stuck

### Git Integration

Task Master works well with `gh` CLI:

```bash
# Create PR for completed task
gh pr create --title "Complete task 1.2: User authentication" --body "Implements JWT auth system as specified in task 1.2"

# Reference task in commits
git commit -m "feat: implement JWT auth (task 1.2)"
```

### Parallel Development with Git Worktrees

```bash
# Create worktrees for parallel task development
git worktree add ../project-auth feature/auth-system
git worktree add ../project-api feature/api-refactor

# Run Claude Code in each worktree
cd ../project-auth && claude    # Terminal 1: Auth work
cd ../project-api && claude     # Terminal 2: API work
```

## Troubleshooting

### AI Commands Failing

```bash
# Check API keys are configured
cat .env                           # For CLI usage

# Verify model configuration
task-master models

# Test with different model
task-master models --set-fallback gpt-4o-mini
```

### MCP Connection Issues

- Check `.mcp.json` configuration
- Verify Node.js installation
- Use `--mcp-debug` flag when starting Claude Code
- Use CLI as fallback if MCP unavailable

### Task File Sync Issues

```bash
# Regenerate task files from tasks.json
task-master generate

# Fix dependency issues
task-master fix-dependencies
```

DO NOT RE-INITIALIZE. That will not do anything beyond re-adding the same Taskmaster core files.

## Important Notes

### AI-Powered Operations

These commands make AI calls and may take up to a minute:

- `parse_prd` / `task-master parse-prd`
- `analyze_project_complexity` / `task-master analyze-complexity`
- `expand_task` / `task-master expand`
- `expand_all` / `task-master expand --all`
- `add_task` / `task-master add-task`
- `update` / `task-master update`
- `update_task` / `task-master update-task`
- `update_subtask` / `task-master update-subtask`

### File Management

- Never manually edit `tasks.json` - use commands instead
- Never manually edit `.taskmaster/config.json` - use `task-master models`
- Task markdown files in `tasks/` are auto-generated
- Run `task-master generate` after manual changes to tasks.json

### Claude Code Session Management

- Use `/clear` frequently to maintain focused context
- Create custom slash commands for repeated Task Master workflows
- Configure tool allowlist to streamline permissions
- Use headless mode for automation: `claude -p "task-master next"`

### Multi-Task Updates

- Use `update --from=<id>` to update multiple future tasks
- Use `update-task --id=<id>` for single task updates
- Use `update-subtask --id=<id>` for implementation logging

### Research Mode

- Add `--research` flag for research-based AI enhancement
- Requires a research model API key like Perplexity (`PERPLEXITY_API_KEY`) in environment
- Provides more informed task creation and updates
- Recommended for complex technical tasks

## AI-Driven Development Workflow

The Cursor agent is pre-configured (via the rules file) to follow this workflow:

### 1. Task Discovery and Selection

Ask the agent to list available tasks:

> What tasks are available to work on next?
> Can you show me tasks 1, 3, and 5 to understand their current status?

The agent will:
- Run `task-master list` to see all tasks
- Run `task-master next` to determine the next task to work on
- Run `task-master show 1,3,5` to display multiple tasks with interactive options
- Analyze dependencies to determine which tasks are ready to be worked on
- Prioritize tasks based on priority level and ID order
- Suggest the next task(s) to implement

### 2. Task Implementation

When implementing a task, the agent will:
- Reference the task's details section for implementation specifics
- Consider dependencies on previous tasks
- Follow the project's coding standards
- Create appropriate tests based on the task's testStrategy

You can ask:
> Let's implement task 3. What does it involve?

#### 2.1. Viewing Multiple Tasks

For efficient context gathering and batch operations:
> Show me tasks 5, 7, and 9 so I can plan my implementation approach.

The agent will:
- Run `task-master show 5,7,9` to display a compact summary table
- Show task status, priority, and progress indicators
- Provide an interactive action menu with batch operations
- Allow you to perform group actions like marking multiple tasks as in-progress

### 3. Task Verification

Before marking a task as complete, verify it according to:
- The task's specified testStrategy
- Any automated tests in the codebase
- Manual verification if required

### 4. Task Completion

When a task is completed, tell the agent:
> Task 3 is now complete. Please update its status.

The agent will execute:
```bash
task-master set-status --id=3 --status=done
```

### 5. Handling Implementation Drift

If during implementation, you discover that:
- The current approach differs significantly from what was planned
- Future tasks need to be modified due to current implementation choices
- New dependencies or requirements have emerged

Tell the agent:
> We've decided to use MongoDB instead of PostgreSQL. Can you update all future tasks (from ID 4) to reflect this change?

The agent will execute:
```bash
task-master update --from=4 --prompt="Now we are using MongoDB instead of PostgreSQL."

# OR, if research is needed to find best practices for MongoDB:
task-master update --from=4 --prompt="Update to use MongoDB, researching best practices" --research
```

This will rewrite or re-scope subsequent tasks in tasks.json while preserving completed work.

### 6. Reorganizing Tasks

If you need to reorganize your task structure:
> I think subtask 5.2 would fit better as part of task 7 instead. Can you move it there?

The agent will execute:
```bash
task-master move --from=5.2 --to=7.3
```

You can reorganize tasks in various ways:
- Moving a standalone task to become a subtask: `--from=5 --to=7`
- Moving a subtask to become a standalone task: `--from=5.2 --to=7`
- Moving a subtask to a different parent: `--from=5.2 --to=7.3`
- Reordering subtasks within the same parent: `--from=5.2 --to=5.4`
- Moving a task to a new ID position: `--from=5 --to=25` (even if task 25 doesn't exist yet)
- Moving multiple tasks at once: `--from=10,11,12 --to=16,17,18` (must have same number of IDs, Taskmaster will look through each position)

When moving tasks to new IDs:
- The system automatically creates placeholder tasks for non-existent destination IDs
- This prevents accidental data loss during reorganization
- Any tasks that depend on moved tasks will have their dependencies updated
- When moving a parent task, all its subtasks are automatically moved with it and renumbered

This is particularly useful as your project understanding evolves and you need to refine your task structure.

#### 6.1. Resolving Merge Conflicts with Tasks

When working with a team, you might encounter merge conflicts in your tasks.json file if multiple team members create tasks on different branches. The move command makes resolving these conflicts straightforward:

> I just merged the main branch and there's a conflict with tasks.json. My teammates created tasks 10-15 while I created tasks 10-12 on my branch. Can you help me resolve this?

The agent will help you:
1. Keep your teammates' tasks (10-15)
2. Move your tasks to new positions to avoid conflicts:

```bash
# Move your tasks to new positions (e.g., 16-18)
task-master move --from=10 --to=16
task-master move --from=11 --to=17
task-master move --from=12 --to=18
```

This approach preserves everyone's work while maintaining a clean task structure, making it much easier to handle task conflicts than trying to manually merge JSON files.

### 7. Breaking Down Complex Tasks

For complex tasks that need more granularity:
> Task 5 seems complex. Can you break it down into subtasks?

The agent will execute:
```bash
task-master expand --id=5 --num=3
```

You can provide additional context:
> Please break down task 5 with a focus on security considerations.

The agent will execute:
```bash
task-master expand --id=5 --prompt="Focus on security aspects"
```

You can also expand all pending tasks:
> Please break down all pending tasks into subtasks.

The agent will execute:
```bash
task-master expand --all
```

For research-backed subtask generation using the configured research model:
> Please break down task 5 using research-backed generation.

The agent will execute:
```bash
task-master expand --id=5 --research
```

## TDD CLI Command Reference

### File Locations
- **TDD Commands**: Project root directory (executable shell scripts)
  - `./task-master-generate-story`
  - `./task-master-test-story` 
  - `./task-master-validate-task`
  - `./task-master-complete-with-story`
- **Story Data**: `.taskmaster/stories/task_stories.json`
- **Temporal Grids**: `V3-minimal/debug_screenshots/task_*_temporal_grid_*.png`

### Integration Notes
- All TDD commands integrate with PDM environment automatically
- Commands detect project root and configuration
- Error handling provides clear next-step guidance
- Each command has comprehensive `--help` documentation

### Best Practices for Agents
1. **Always generate story before coding**: Use TDD story-first approach
2. **Test frequently during development**: Run `./task-master-test-story` regularly
3. **Validate before completion**: Use `./task-master-validate-task` before marking done
4. **Use TDD completion**: Always use `./task-master-complete-with-story` instead of manual status changes
5. **Document implementation notes**: Use `task-master update-subtask` to log progress

## Session Management Best Practices

### Git Protocol Requirements
- **ALWAYS commit changes** before session completion
- **Create feature branches** for significant implementations
- **Use descriptive commit messages** with task references
- **Tag releases** when major milestones are reached
- **Merge branches properly** using appropriate merge strategies

### Memory and Continuity
- **Update CLAUDE.md** with new patterns and instructions
- **Create memory files** in `.ai/memories/` to preserve lessons learned
- **Document TDD validation results** for audit trails
- **Preserve temporal grid evidence** for task completion proof

### Required Git Workflow Example
```bash
# Before starting work
git checkout -b feature/task-47-generate-story
git status

# During implementation
git add .
git commit -m "feat: implement task-master-generate-story CLI command (task 47)

- Created shell script wrapper for TDD generate-story command
- Added comprehensive help documentation and error handling
- Integrated with PDM environment for reliable execution
- Tested with Task 47 itself using TDD validation workflow"

# After completion and TDD validation
git checkout main
git merge feature/task-47-generate-story
git tag v1.0.0-task-47-complete
git push origin main --tags
```

---

_This guide ensures Claude Code has immediate access to Task Master's essential functionality for agentic development workflows._
