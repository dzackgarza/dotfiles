#!/usr/bin/env python3
"""
PostToolUse hook that prompts Claude with contextual questions
Uses the block decision to ensure Claude sees and responds to the messages
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
    tool_response = hook_input.get('tool_response', {})
    
    # Only trigger for certain tools and occasionally
    if tool_name not in ['Edit', 'Write', 'MultiEdit']:
        sys.exit(0)
    
    # Higher chance for Edit (suggests patching)
    if tool_name == 'Edit':
        trigger_chance = 6  # 1 in 6
    else:
        trigger_chance = 10  # 1 in 10
    
    if random.randint(1, trigger_chance) != 1:
        log_hook_execution("post-tool-prompt", tool_name, "approve", f"Random check not triggered (1/{trigger_chance})")
        sys.exit(0)
    
    # Get contextual questions
    if tool_name == 'Edit':
        questions = get_questions_by_context('edit_operations', 2)
        if not questions:
            questions = get_questions_by_category('v3_reference', 2)
    else:
        questions = get_questions_by_category('project_alignment', 2)
    
    if not questions:
        questions = ["Have you verified this change works as expected?", "Does this follow the existing patterns in the codebase?"]
    
    # Combine questions into a conversational prompt
    prompt = " ".join(questions) + " Take a moment to reflect before continuing."
    
    log_hook_execution("post-tool-prompt", tool_name, "block", f"Prompting with reflection questions")
    
    # Use block decision to prompt Claude
    print(json.dumps({
        "decision": "block",
        "reason": prompt
    }))
    sys.exit(0)

if __name__ == "__main__":
    main()