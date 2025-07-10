# Feature: File Context Inclusion (@-commands)

**Created:** 2025-07-10
**Status:** 🔴 Up Next
**Priority:** High

## Overview

Implement @ commands to include file and directory contents as context in prompts, similar to Gemini CLI's @ functionality. This allows users to reference local files directly in their queries.

## Goals

- Enable easy inclusion of file contents in prompts
- Support both single files and directories
- Implement git-aware filtering (exclude .gitignore'd files)
- Handle binary files gracefully
- Support multimodal content (images, PDFs)

## Technical Approach

### Command Syntax
- `@path/to/file.txt` - Include single file
- `@src/` - Include all files in directory
- `What does @README.md say?` - Inline usage
- Escape spaces: `@My\ Documents/file.txt`

### Implementation Details

1. **Parser Enhancement**
   - Detect @ symbols in user input
   - Extract file paths
   - Handle multiple @ references in single prompt

2. **File Reader Plugin**
   - Read file contents
   - Apply git-aware filtering
   - Handle large files (truncate/paginate)
   - Support binary file detection

3. **Context Injection**
   - Inject file contents into prompt
   - Maintain clear boundaries
   - Show tool execution in timeline

## Success Criteria

- [ ] @ commands work for single files
- [ ] Directory traversal with git filtering
- [ ] Clear visual indication when files are included
- [ ] Error handling for missing/unreadable files
- [ ] Performance with large codebases

## Future Enhancements

- Glob pattern support: `@src/**/*.py`
- Syntax highlighting in included code
- Smart summarization for large files
- Integration with memory system