#!/usr/bin/env python3
"""
"Don't Trust Yourself" Reminder - Like Leonard's tattoos

Key behavioral reminders that appear at decision points
to counter cognitive biases and pattern repetition.
"""

import json
import sys
import re
import random
from pathlib import Path

# Pattern-breaking reminders based on observed failure modes
BEHAVIORAL_REMINDERS = {
    'assumption_trap': [
        "🧠 YOUR BRAIN LIES: You assume code changes work without checking",
        "🔄 PATTERN DETECTED: Code change → assumption → false claim",
        "🛑 BREAK THE LOOP: Demand visual proof before believing anything"
    ],
    
    'completion_bias': [
        "✅ COMPLETION BIAS: You want to believe the work is done",
        "📸 COUNTER-MEASURE: Screenshot or it didn't happen",
        "⚠️ RED FLAG: Claiming 'fixed' without new visual evidence"
    ],
    
    'test_theater': [
        "🎭 TEST THEATER: Tests passing ≠ GUI working",
        "🏃 PILOT REQUIRED: run_test() with screenshots shows reality",
        "🕳️ ASYNC GAPS: Your 'fixes' might not execute in test timing"
    ],
    
    'rationalization': [
        "🧠 STOP RATIONALIZING: Why the broken GUI 'makes sense'",
        "📊 TRUST DATA: Screenshots > logic > assumptions",
        "🔍 LOOK CLOSER: You might be missing obvious visual issues"
    ]
}

def detect_problematic_patterns(content):
    """Detect patterns that indicate cognitive bias"""
    patterns = []
    
    # Completion claims without evidence
    if re.search(r'(fixed|completed|done|working|resolved)', content, re.IGNORECASE):
        patterns.append('completion_bias')
    
    # Assumption indicators
    if re.search(r'(should|must|will|expected)', content, re.IGNORECASE):
        patterns.append('assumption_trap')
    
    # Test-focused language
    if re.search(r'(test.*pass|pass.*test)', content, re.IGNORECASE):
        patterns.append('test_theater')
    
    # Rationalization language
    if re.search(r'(because|since|therefore|logic)', content, re.IGNORECASE):
        patterns.append('rationalization')
    
    return patterns

from question_loader import get_questions_by_category, get_questions_by_context

def get_relevant_reminders(patterns):
    """Get reminders based on detected patterns"""
    reminders = []
    
    # Always include core reminder
    reminders.append("🏆 GOLDEN RULE: Screenshots show reality, your mind shows fantasy")
    
    # Add pattern-specific reminders
    for pattern in patterns:
        if pattern in BEHAVIORAL_REMINDERS:
            reminders.extend(BEHAVIORAL_REMINDERS[pattern][:2])  # Limit to prevent overwhelm
    
    # Sometimes inject memory-guided questions (1 in 4 chance)
    if random.randint(1, 4) == 1:
        # Use contextual questions based on detected patterns
        if 'completion_bias' in patterns:
            memory_questions = get_questions_by_context('claiming_fixes', 1)
        elif 'assumption_trap' in patterns:
            memory_questions = get_questions_by_category('intellectual_humility', 1)
        elif 'test_theater' in patterns:
            memory_questions = get_questions_by_category('testing_methodology', 1)
        else:
            memory_questions = get_questions_by_category('reset_questions', 1)
        
        if memory_questions:
            memory_question = memory_questions[0]
            reminders.append(f"💭 MEMORY: {memory_question}")
    
    return list(dict.fromkeys(reminders))  # Remove duplicates

def main():
    hook_input = json.loads(sys.stdin.read())
    
    tool_name = hook_input.get('tool_name', '')
    tool_input = hook_input.get('tool_input', {})
    
    # Extract content
    content = ""
    if tool_name == 'Write':
        content = tool_input.get('content', '')
    elif tool_name == 'MultiEdit':
        edits = tool_input.get('edits', [])
        content = ' '.join([edit.get('new_string', '') for edit in edits])
    elif tool_name == 'TodoWrite':
        todos = tool_input.get('todos', [])
        for todo in todos:
            if todo.get('status') == 'completed':
                content += f" completed {todo.get('content', '')}"
    
    # Detect problematic patterns
    patterns = detect_problematic_patterns(content)
    
    if patterns:
        reminders = get_relevant_reminders(patterns)
        
        message = "🧠 DON'T TRUST YOURSELF REMINDERS:\n\n"
        for i, reminder in enumerate(reminders, 1):
            message += f"{i}. {reminder}\n"
        
        message += f"\n🔍 Detected patterns: {', '.join(patterns)}"
        message += "\n\n💭 These exist because you repeat the same mistakes without reminders."
        
        print(json.dumps({
            "decision": "approve",
            "reason": message
        }))
    else:
        print(json.dumps({"decision": "approve"}))

if __name__ == "__main__":
    main()