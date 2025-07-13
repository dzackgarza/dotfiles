#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

"""
Stop Hook - Session Completion and Continuation Control

CLAUDE COMMUNICATION METHODS:
================================================================================
This hook can directly communicate with Claude using these methods:

1. EXIT CODE 2 + stderr:
   - Blocks Claude from stopping (forces continuation)
   - stderr content is automatically fed to Claude as instructions
   - Claude receives the message and must continue working
   - Example: sys.exit(2) with print("Continue: tests are failing", file=sys.stderr)

2. JSON OUTPUT + EXIT CODE 0:
   Advanced control via stdout JSON:
   
   a) Decision Control:
      {"decision": "block", "reason": "explanation"}
      - Prevents Claude from stopping
      - Reason tells Claude how to proceed
      - Claude receives reason and continues working
      
   b) Session Control:
      {"continue": false, "stopReason": "reason"}
      - Stops Claude entirely, reason shown to user (NOT Claude)

3. NO COMMUNICATION (Exit Code 0, no stderr):
   - Allows normal session completion
   - Only logging and TTS occurs

CURRENT IMPLEMENTATION: Uses method #3 (no communication) - allows normal completion
NOTE: Could be extended with loop mode to enforce completion criteria
================================================================================
"""

import argparse
import json
import os
import sys
import random
import subprocess
from pathlib import Path
from datetime import datetime
from utils.common_logger import create_logger

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional


def get_completion_messages():
    """Return list of friendly completion messages."""
    return [
        "Work complete!",
        "All done!",
        "Task finished!",
        "Job complete!",
        "Ready for next task!"
    ]




def get_llm_completion_message():
    """
    Generate completion message using available LLM services.
    Priority order: Groq > Gemini > fallback to random message
    
    Returns:
        str: Generated or fallback completion message
    """
    # Get current script directory and construct utils/llm path
    script_dir = Path(__file__).parent
    llm_dir = script_dir / "utils" / "llm"
    
    # Try Groq first (highest priority - fast and good)
    if os.getenv('GROQ_API_KEY'):
        groq_script = llm_dir / "groq_client.py"
        if groq_script.exists():
            try:
                result = subprocess.run([
                    "uv", "run", str(groq_script), "--completion"
                ], 
                capture_output=True,
                text=True,
                timeout=10
                )
                if result.returncode == 0 and result.stdout.strip():
                    return result.stdout.strip()
            except (subprocess.TimeoutExpired, subprocess.SubprocessError):
                pass
    
    # Try Gemini second (good fallback)
    if os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY'):
        gemini_script = llm_dir / "gemini.py"
        if gemini_script.exists():
            try:
                result = subprocess.run([
                    "uv", "run", str(gemini_script), "--completion"
                ], 
                capture_output=True,
                text=True,
                timeout=10
                )
                if result.returncode == 0 and result.stdout.strip():
                    return result.stdout.strip()
            except (subprocess.TimeoutExpired, subprocess.SubprocessError):
                pass
    
    # Fallback to random predefined message
    messages = get_completion_messages()
    return random.choice(messages)



# ================================================================================
# LOOP MODE - COMPLETION ENFORCEMENT
# ================================================================================

def check_tests_passing():
    """
    Check if tests are passing. Returns (tests_passing, failure_reason).
    Add your test validation logic here.
    """
    try:
        # Check if V3-minimal directory exists and has tests
        # Get project root (from .claude/hooks/ to project root)
        project_root = Path.cwd().parent.parent
        v3_minimal_dir = project_root / "V3-minimal"
        if v3_minimal_dir.exists() and (v3_minimal_dir / "tests").exists():
            # Run pytest in V3-minimal directory
            result = subprocess.run(['pdm', 'run', 'pytest', '--tb=short'], 
                                  capture_output=True, text=True, timeout=30,
                                  cwd=str(v3_minimal_dir))
            if result.returncode == 0:
                return True, ""
            else:
                return False, f"Tests failing in V3-minimal: {result.stdout[-200:]}"
        else:
            # No V3-minimal tests directory, check current directory
            if Path("tests").exists():
                result = subprocess.run(['pytest', 'tests', '--tb=short'], 
                                      capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    return True, ""
                else:
                    return False, f"Tests failing: {result.stdout[-200:]}"
            else:
                # No tests found, assume OK
                return True, ""
    except (subprocess.TimeoutExpired, FileNotFoundError):
        # If pytest not found or times out, assume tests are OK
        return True, ""
    except Exception as e:
        return True, ""  # Don't block on test check errors

def check_lint_passing():
    """
    Check if linting is passing. Returns (lint_passing, failure_reason).
    """
    try:
        # Check if V3-minimal directory exists
        # Get project root (from .claude/hooks/ to project root)
        project_root = Path.cwd().parent.parent
        v3_minimal_dir = project_root / "V3-minimal"
        if v3_minimal_dir.exists():
            # Run ruff in V3-minimal directory
            result = subprocess.run(['pdm', 'run', 'ruff', 'check', '.'], 
                                  capture_output=True, text=True, timeout=10,
                                  cwd=str(v3_minimal_dir))
            if result.returncode == 0:
                return True, ""
            else:
                # Just check for E (error) level issues, not warnings
                if " E" in result.stdout:
                    return False, f"Lint errors in V3-minimal: {result.stdout[-200:]}"
                else:
                    return True, ""  # Only warnings, not blocking
        else:
            # No V3-minimal, assume OK
            return True, ""
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return True, ""  # Don't block if tools not available
    except Exception:
        return True, ""

def check_git_status_clean():
    """
    Check if git status is clean (no uncommitted changes).
    Returns (is_clean, status_info).
    """
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            if result.stdout.strip():
                return False, f"Uncommitted changes: {result.stdout.strip()[:100]}"
            else:
                return True, ""
        else:
            return True, ""  # Not a git repo or other issue
    except Exception:
        return True, ""

# Add completion checks to this list for loop mode
COMPLETION_CHECKS = [
    ("tests", check_tests_passing),
    ("lint", check_lint_passing),
    ("git", check_git_status_clean),
]

def run_loop_mode_checks():
    """
    Run all completion checks for loop mode.
    Returns (should_continue, reasons) where reasons is a list of failure reasons.
    """
    failures = []
    
    for check_name, check_func in COMPLETION_CHECKS:
        try:
            is_passing, reason = check_func()
            if not is_passing and reason:
                failures.append(f"{check_name}: {reason}")
        except Exception as e:
            # Don't block on check failures
            continue
    
    return len(failures) > 0, failures


def main():
    logger = create_logger('stop')
    
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('--chat', action='store_true', help='Copy transcript to chat.json')
        parser.add_argument('--loop', action='store_true', help='Enable loop mode - enforce completion criteria')
        args = parser.parse_args()
        
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        # Extract required fields
        session_id = input_data.get("session_id", "")
        stop_hook_active = input_data.get("stop_hook_active", False)

        # Log the event
        logger.log_event({
            **input_data, 
            'chat_export_enabled': args.chat,
            'loop_mode_enabled': args.loop
        })
        
        
        # Handle --chat switch
        if args.chat and 'transcript_path' in input_data:
            transcript_path = input_data['transcript_path']
            if os.path.exists(transcript_path):
                # Read .jsonl file and convert to JSON array
                chat_data = []
                try:
                    with open(transcript_path, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                try:
                                    chat_data.append(json.loads(line))
                                except json.JSONDecodeError:
                                    pass  # Skip invalid lines
                    
                    # Write to logs/chat.json
                    log_dir = logger.log_dir
                    chat_file = log_dir / 'chat.json'
                    with open(chat_file, 'w') as f:
                        json.dump(chat_data, f, indent=2)
                except Exception as e:
                    logger.log_error(f"Failed to export chat transcript: {str(e)}", {"transcript_path": transcript_path})

        # POINTED QUESTIONING: Force Claude to confront what they've actually accomplished
        pointed_questions = []
        
        # Add any loop mode failure messages if they exist
        if args.loop:
            should_continue, failure_reasons = run_loop_mode_checks()
            if should_continue and failure_reasons:
                pointed_questions.extend([f"❌ {reason}" for reason in failure_reasons])
                pointed_questions.append("🤨 You have failing tests - but you're trying to stop anyway?")
        
        # Direct confrontational questions that work
        pointed_questions.extend([
            "Really? What did you actually complete today?",
            "Do you have any evidence your code works?",
            "If I ran 'just run' right now, would I see anything working?",
            "Did you actually test this?",
            "Are you sure I'll see that if I run it?",
            "Do you have any visual proof that this actually appears?",
            "",
            "Really? Are you done?",
            "• Run 'task-master next' - are there more tasks?",
            "• Can you show me one thing that actually works?",
            "• Did you actually run your code?",
            "• Do your temporal grids show real GUI or fake screenshots?",
            "",
            "Really? You're stopping without proving anything works?",
            "Go test your code first."
        ])
        
        # Send pointed questions to Claude
        if pointed_questions:
            full_message = "🤨 ACCOUNTABILITY CHECK - Answer honestly:\n\n" + "\n".join(pointed_questions)
            print(full_message, file=sys.stderr)
            sys.exit(2)  # Block stopping, force self-reflection

        # Generate completion summary (but don't announce via TTS)
        completion_summary = get_llm_completion_message()
        logger.log_event({
            "session_completed": True,
            "completion_summary": completion_summary
        })

        sys.exit(0)

    except json.JSONDecodeError:
        logger.log_error("JSON decode error", {"raw_input": "invalid"})
        sys.exit(0)
    except Exception as e:
        logger.log_error(f"Unexpected error: {str(e)}", input_data if 'input_data' in locals() else {})
        sys.exit(0)


if __name__ == "__main__":
    main()
