#!/usr/bin/env python3
"""
Stop hook that intelligently checks if work is complete.
Prevents endless loops while ensuring quality.
"""

import json
import sys
import random
from pathlib import Path
import time

from question_loader import get_questions_by_context, get_high_priority_questions
from hook_logger import log_hook_execution

def check_recent_canonical_run():
    """Check if canonical test was run recently with good results"""
    screenshot_dir = Path("./V3-minimal/debug_screenshots")
    
    if not screenshot_dir.exists():
        return False, "No debug_screenshots directory"
    
    # Look for canonical screenshots
    canonical_screenshots = list(screenshot_dir.glob("canonical_*.svg"))
    if not canonical_screenshots:
        return False, "No canonical screenshots found"
    
    # Check recency (within last 5 minutes is fresh enough)
    latest = max(canonical_screenshots, key=lambda p: p.stat().st_mtime)
    age_minutes = (time.time() - latest.stat().st_mtime) / 60
    
    if age_minutes < 5:
        # Check if we have a complete set (at least 10 screenshots suggests full run)
        if len(canonical_screenshots) >= 10:
            return True, f"Fresh canonical test run found ({len(canonical_screenshots)} screenshots, {int(age_minutes)} min old)"
    
    return False, f"Canonical screenshots are {int(age_minutes)} minutes old"

def check_work_context():
    """Try to understand what work was being done"""
    # Check for recent test runs
    test_output = Path("./V3-minimal/.pytest_cache/lastfailed")
    if test_output.exists():
        # If no failures in recent test cache, that's good
        try:
            with open(test_output) as f:
                content = f.read()
                if content.strip() == "{}":  # Empty dict means no failures
                    return "tests_passing"
        except:
            pass
    
    # Check if we're in a repetitive screenshot loop
    log_file = Path("/home/dzack/dotfiles/bin/llm-repl-project/.claude/hooks/logs/hook_execution.log")
    if log_file.exists():
        # Check last 10 entries for repetitive patterns
        try:
            with open(log_file) as f:
                lines = f.readlines()[-10:]
                stop_hook_count = sum(1 for line in lines if "block-premature-completion" in line)
                if stop_hook_count > 3:
                    return "repetitive_loop"
        except:
            pass
    
    return "normal_work"

def main():
    hook_input = json.loads(sys.stdin.read())
    
    log_hook_execution("block-premature-completion", "Stop", "checking", "Intelligent completion check")
    
    # Check if canonical test was run recently
    canonical_fresh, canonical_reason = check_recent_canonical_run()
    
    # Check work context
    context = check_work_context()
    
    # If we're in a repetitive loop, break it
    if context == "repetitive_loop":
        log_hook_execution("block-premature-completion", "Stop", "approve", "Breaking repetitive loop")
        print(json.dumps({
            "decision": "approve",
            "reason": "Alright, let's stop going in circles. The work looks complete enough. Time to move on to something else."
        }))
        return
    
    # If canonical test is fresh and tests are passing, guide to next steps
    if canonical_fresh and context == "tests_passing":
        log_hook_execution("block-premature-completion", "Stop", "approve", "Work complete - suggesting next steps")
        next_steps = [
            "Good work, everything's verified. You should probably commit these changes before you lose them. Just run git add and commit with a message about what you fixed.",
            "Tests are passing and the canonical screenshots look good. Time to request a human review with the ledger system, or just move on to the next task.",
            "Feature's working as shown in the screenshots. Maybe save those screenshots somewhere permanent as proof, then update CLAUDE-CONTINUE.md with what you learned.",
            "Everything checks out. The implementation is complete and verified. Document what worked in CLAUDE-CONTINUE.md so the next session knows."
        ]
        print(json.dumps({
            "decision": "approve", 
            "reason": random.choice(next_steps)
        }))
        return
    
    # If canonical test is fresh, guide towards completion
    if canonical_fresh:
        log_hook_execution("block-premature-completion", "Stop", "approve", "Fresh canonical test, guiding to completion")
        completion_hints = [
            f"{canonical_reason}, which is pretty recent. The work looks done. Time to commit your changes and move on.",
            f"{canonical_reason} and that's fresh enough. Ready to request human review or shall we tackle something else?",
            f"{canonical_reason}, so we have good evidence. Document this fix in CLAUDE-CONTINUE.md before you forget the details.",
            f"{canonical_reason}. Save those screenshots somewhere permanent if this was an important fix, then we're done here."
        ]
        print(json.dumps({
            "decision": "approve",
            "reason": random.choice(completion_hints)
        }))
        return
    
    # If we get here, canonical test isn't fresh - but don't always demand it
    if random.randint(1, 3) == 1:  # 1/3 chance to ask about tests
        message = f"Hold on, {canonical_reason}. Want to run the canonical test real quick with pdm run pytest tests/test_canonical_pilot.py -v? Or is the feature actually working fine and we don't need more proof?"
    else:
        # Ask about completion status instead
        completion_checks = [
            "Are we done here? Is the feature working the way it should? If you're happy with it, just say the word and we'll wrap up.",
            "Quick check before we finish up. Does this solve the original problem? Are there any edge cases you're worried about? Or are we good to go?",
            "So where are we at? Is everything working as intended? Should we commit these changes or is there something else that needs fixing?",
            "Let me ask you straight up. Is this feature complete? Does it do what it's supposed to do? If yes, let's move on. If not, what's still broken?",
            "Before we close this out, is there anything else you need to fix? Or can we call this done and maybe update CLAUDE-CONTINUE.md with what worked?",
            "Looks like you've been at this for a while. Is it working now? Any reason we can't just commit and move on to something else?"
        ]
        message = random.choice(completion_checks)
    
    # Always provide clear escape via system notification
    message += " If you're done, send me a system notification saying complete. If you're stuck, send a system notification asking for help. Otherwise keep going."
    
    log_hook_execution("block-premature-completion", "Stop", "soft_block", "Gentle completion check")
    
    # Use stderr to show message
    print(message, file=sys.stderr)
    sys.exit(2)  # Soft block with escape options

if __name__ == "__main__":
    main()