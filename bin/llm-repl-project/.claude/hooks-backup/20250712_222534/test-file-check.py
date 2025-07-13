#!/usr/bin/env python3
"""
Test File Check - Questions test file creation patterns

When Claude creates or edits test files, this hook asks whether they're
testing the real app or just mocking, and whether they should extend
the canonical test instead of creating new ones.
"""

import json
import sys
import os
import random
from hook_logger import log_hook_execution

def main():
    hook_input = json.loads(sys.stdin.read())
    tool_name = hook_input.get('tool_name', '')
    
    # Get file paths
    file_paths = os.environ.get('CLAUDE_FILE_PATHS', '').split()
    
    # Check if any file has "test" in the name
    test_files = [f for f in file_paths if 'test' in f.lower() and f.endswith('.py')]
    
    if not test_files:
        log_hook_execution("test-file-check", tool_name, "approve", "No test files")
        sys.exit(0)  # Approve - no test files
    
    # Always trigger for test files - these questions are too important
    questions = [
        "🎭 Are you testing mock-ups or the REAL app? Mocks lie, the real app tells the truth.",
        "🔄 Are you reinventing canonical tests instead of extending test_canonical_pilot.py?",
        "🎪 Another test file? Why not add to test_canonical_extensions() instead?",
        "🤔 Is this testing what users actually see, or internal implementation details?",
        "📸 Does this test take screenshots of the REAL app like the canonical test does?",
        "🎯 The canonical test runs the actual app - does yours, or is it full of mocks?",
        "🚫 No mocks allowed in canonical tests - are you following that rule?",
        "🔍 test_canonical_pilot.py is our source of truth - why create a separate test?",
        "💭 Are you testing the actual user experience or just unit testing internals?",
        "📝 Should this be a new test file or an extension to test_canonical_extensions()?",
        "🎨 The canonical test proves the app works - what does your test prove?",
        "🏗️ Building another test pyramid? The canonical test is the only pyramid we need.",
        "🔬 Testing implementation details that users never see? That's test theater.",
        "🎭 Mock objects in your test? The canonical test uses the REAL app instead.",
        "📊 How many test files do we need? One canonical test should cover everything."
    ]
    
    # Specific checks based on file content
    canonical_reminders = [
        "\n\n🎯 CANONICAL REMINDER: Extend test_canonical_extensions() for new features",
        "\n\n📸 CANONICAL PATTERN: Real app → User actions → Screenshots → Verification",
        "\n\n🚫 NO MOCKS: The canonical test runs the actual app, just like 'just run'",
        "\n\n✅ EXTEND DON'T RECREATE: Add to test_canonical_extensions(), don't make new files"
    ]
    
    message = random.choice(questions)
    
    # Always add a canonical reminder
    message += random.choice(canonical_reminders)
    
    # If they're creating a new test file (not editing existing)
    if tool_name in ['Write', 'MultiEdit'] and any('test_' in f and f != 'test_canonical_pilot.py' for f in test_files):
        message += "\n\n⚠️ Creating a new test file? Consider extending test_canonical_pilot.py instead!"
    
    log_hook_execution("test-file-check", tool_name, "approve", f"Test file question: {message[:50]}...")
    
    # Show message to Claude via stderr
    print(message, file=sys.stderr)
    sys.exit(0)  # Approve but with message

if __name__ == "__main__":
    main()