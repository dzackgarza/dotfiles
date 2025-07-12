#!/usr/bin/env python3
"""
Random Perspective Check - Occasionally injects broader thinking reminders
Fires with higher frequency for Edit operations to avoid monkey-patching
"""

import json
import sys
import random
from pathlib import Path

from question_loader import get_questions_by_context, get_questions_by_category
from hook_logger import log_hook_execution

def main():
    hook_input = json.loads(sys.stdin.read())
    tool_name = hook_input.get('tool_name', '')
    
    # Only trigger on file writing operations
    if tool_name not in ['Write', 'Edit', 'MultiEdit']:
        log_hook_execution("random-perspective-check", tool_name, "approve", "Not a write operation")
        sys.exit(0)  # Approve - not a write operation
    
    # Higher frequency for Edit operations (patching suggests problems)
    if tool_name == 'Edit':
        trigger_chance = 4  # 1 in 4 chance for Edit
    else:
        trigger_chance = 8  # 1 in 8 chance for Write/MultiEdit
    
    if random.randint(1, trigger_chance) != 1:
        log_hook_execution("random-perspective-check", tool_name, "approve", f"Random check not triggered (1/{trigger_chance})")
        sys.exit(0)  # Approve - random check not triggered
    
    # Get contextual questions based on tool type
    if tool_name == 'Edit':
        # Editing suggests patching - focus on research and V3 patterns
        questions = get_questions_by_context('edit_operations', 1)
        if not questions:
            questions = get_questions_by_category('research_first', 1)
    else:
        # Writing/MultiEdit - broader perspective questions
        questions = get_questions_by_category('reset_questions', 1)
    
    if not questions:
        questions = ["Are you sure we're not just swatting flies?"]
    
    message = questions[0]
    
    log_hook_execution("random-perspective-check", tool_name, "approve", f"Triggered: {message}")
    
    # Show message to Claude via stderr
    print(message, file=sys.stderr)
    sys.exit(0)  # Approve but with message

if __name__ == "__main__":
    main()