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
    screenshot_dir = Path("./debug_screenshots")
    
    if not screenshot_dir.exists():
        return False, "the debug_screenshots directory doesn't even exist"
    
    # Look for any screenshots (not just canonical)
    all_screenshots = list(screenshot_dir.glob("*.svg")) + list(screenshot_dir.glob("*.png"))
    canonical_screenshots = list(screenshot_dir.glob("canonical_*.svg"))
    
    if not all_screenshots:
        return False, "no debug screenshots found at all"
    
    if not canonical_screenshots:
        # Check when the last screenshot was taken
        latest_any = max(all_screenshots, key=lambda p: p.stat().st_mtime)
        age_minutes = (time.time() - latest_any.stat().st_mtime) / 60
        if age_minutes < 60:  # Within last hour
            return False, f"no canonical screenshots found (last debug screenshot was {int(age_minutes)} minutes ago: {latest_any.name})"
        else:
            hours = int(age_minutes / 60)
            return False, f"no canonical screenshots found (last debug screenshot was {hours} hours ago: {latest_any.name})"
    
    # Check recency of canonical screenshots (within last 5 minutes is fresh enough)
    latest = max(canonical_screenshots, key=lambda p: p.stat().st_mtime)
    age_minutes = (time.time() - latest.stat().st_mtime) / 60
    
    if age_minutes < 5:
        # Check if we have a complete set (at least 10 screenshots suggests full run)
        if len(canonical_screenshots) >= 10:
            return True, f"fresh canonical test run found ({len(canonical_screenshots)} screenshots, {int(age_minutes)} min old)"
    
    if age_minutes < 60:
        return False, f"canonical screenshots are {int(age_minutes)} minutes old (latest: {latest.name})"
    else:
        hours = int(age_minutes / 60)
        return False, f"canonical screenshots are {hours} hours old (latest: {latest.name})"

def check_work_context():
    """Try to understand what work was being done"""
    # Check for recent test runs
    test_output = Path("./.pytest_cache/lastfailed")
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
        # Check last 30 entries for repetitive patterns (need more than 20)
        try:
            with open(log_file) as f:
                lines = f.readlines()[-30:]
                stop_hook_count = sum(1 for line in lines if "block-premature-completion" in line)
                if stop_hook_count > 20:
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
    
    # NEVER automatically allow stopping - only user can decide when work is truly complete
    
    # Show BOTH states of the Sacred GUI for complete understanding
    idle_layout = """
🔸 IDLE STATE (2-way layout):
┌─────────────────────────┐
│ Sacred Timeline (Top)   │ ← Shows conversation history
│ ├── User: Question     │   Previous conversations visible
│ ├── Assistant: Answer  │
│ ├── User: Follow-up    │
│ ├── Assistant: Response│
│ └── [conversation...]  │
├─────────────────────────┤
│ Input (Bottom)         │ ← User types here
│ [Type your message...] │
└─────────────────────────┘"""

    processing_layout = """
🔸 PROCESSING STATE (3-way layout):
┌─────────────────────────┐
│ Sacred Timeline (Top)   │ ← Previous conversations
│ ├── User: Question     │
│ ├── Assistant: Answer  │
│ └── [history...]       │
├─────────────────────────┤
│ Live Workspace (Mid)   │ ← YOUR FEATURE goes here!
│ ├── Route Query        │   Processing steps visible
│ ├── Research Step      │   User sees AI thinking
│ ├── Generate Response  │
│ └── [streaming...]     │
├─────────────────────────┤
│ Input (Bottom)         │ ← Input temporarily disabled
│ [Processing...]        │
└─────────────────────────┘"""

    comprehensive_reality_checks = [
        f"Hold on. {canonical_reason}. Can a real user actually sit down at this app right now and successfully use YOUR feature? Not your isolated test code, not your theoretical implementation - the actual feature in the real app that operates in these states:\\n\\n{idle_layout}\\n{processing_layout}\\nHave you tested it end-to-end like a human would? Did you break any existing functionality that was working perfectly before you touched it? Can you show me concrete evidence that your feature works in practice, integrates properly with the Sacred GUI architecture, and doesn't break anything that was working before? What specific steps did you take to validate this?",
        
        f"Wait, stop right there. {canonical_reason}. Did you actually research how this type of feature should work before building it? Did you look at the documentation, search for examples, understand the proper patterns? Or did you just wing it and hope for the best? The Sacred GUI has specific states and workflows:\\n\\n{idle_layout}\\n{processing_layout}\\nHave you validated that your feature works seamlessly within this architecture? Can you walk me through exactly how a user discovers, accesses, and successfully uses your feature? What evidence do you have beyond your own assumptions?",
        
        f"Really? {canonical_reason}. Have you stepped back to ask the bigger questions? Does your feature actually advance the vision of this LLM REPL project? Does it integrate naturally with the Sacred GUI's two-state architecture? Or have you built something that technically works but feels bolted-on and awkward? Here's what the app should look like:\\n\\n{idle_layout}\\n{processing_layout}\\nDoes your feature enhance this experience or detract from it? Have you tested it with the mindset of a new user who has never seen this app before? Would they be able to figure out how to use your feature without reading code or documentation? What existing functionality did you break in the process? Can users still do basic things they could do before your changes?",
        
        f"Are you serious? {canonical_reason}. Can a real person successfully use what you built right now? Where exactly does your feature appear in this flow:\\n\\n{idle_layout}\\n{processing_layout}\\nHow do users discover it exists? What UI elements did you add or modify? Can you walk through the exact steps a user would take to use your feature successfully? Have you tested these steps yourself in the actual running application? Have you tried testing your feature with real user scenarios instead of perfect conditions and synthetic data? Can you show me evidence that your feature works in practice, not just in theory?",
        
        f"Excuse me? {canonical_reason}. Are you building phantom features? Have you spent weeks writing code, run a few unit tests, and now want to declare victory without ever checking if your feature actually works in the real application? The Sacred GUI architecture expects specific behaviors:\\n\\n{idle_layout}\\n{processing_layout}\\nDoes your feature respect this architecture and integrate seamlessly? Have you sat down and used your feature like a normal user would? Not debugging it, not running it in a test harness, but actually using it for its intended purpose? What errors did you encounter? What edge cases failed? What assumptions turned out to be wrong? Can you answer these questions with specific examples?",
        
        f"Oh really? {canonical_reason}. What existing functionality still works exactly as it did before your changes? What new capability can users access because of your work? Can you demonstrate both of these things with concrete evidence? Have you run the existing tests to make sure you didn't break anything? Have you tested your new feature with real user scenarios? Here's the architecture your feature should enhance:\\n\\n{idle_layout}\\n{processing_layout}\\nIf someone else had to maintain your code starting tomorrow, would they be able to understand what you built and why? Does your code have the humility, documentation, and validation needed for sustainable development?",
        
        f"Let me get this straight. {canonical_reason}. Are you thinking like a product owner, not just a developer? The Sacred GUI provides a specific user experience:\\n\\n{idle_layout}\\n{processing_layout}\\nDoes your feature pass the 'grandmother test'? Could someone completely unfamiliar with the codebase sit down and successfully use what you built? Have you considered the error cases, the edge conditions, the ways users might misunderstand or misuse your feature? What happens when users try to use your feature in unexpected ways? How does it fail, and how does it recover? Have you tested these scenarios beyond just the happy path?",
        
        f"Are you kidding? {canonical_reason}. Have you verified that your feature works in the messy reality of real user interactions? The app has this architecture for a reason:\\n\\n{idle_layout}\\n{processing_layout}\\nDoes your feature respect this design and enhance the overall user experience? Not theoretically, but practically? Have you looked for existing implementations or patterns you could learn from? Have you considered the performance implications of your changes? What about accessibility, error handling, and edge cases? Are you asking yourself these critical questions or are you ready to hand off a potentially broken feature to someone else to debug?",
        
        f"Wait, what? {canonical_reason}. Are we on the same page about what 'feature complete' actually means? Does your feature deliver value to users, integrate seamlessly with the existing system, and not break anything that was working before? The Sacred GUI architecture provides this experience:\\n\\n{idle_layout}\\n{processing_layout}\\nDoes your feature enhance this experience, not detract from it? Can you show me exactly how your feature improves the user's workflow? What problems does it solve? How does a user discover and activate your feature? What feedback does the system provide when the feature is working correctly or when something goes wrong? Have you tested all of these aspects in the actual running application? Can you demonstrate clear value and reliable functionality?",
        
        f"Seriously? {canonical_reason}. Does your feature work reliably for real users in real scenarios? The app operates in specific states:\\n\\n{idle_layout}\\n{processing_layout}\\nDoes your feature work correctly in both states and handle the transitions between them gracefully? Have you tested this thoroughly? Have you tried to break your feature with unexpected inputs, rapid interactions, or unusual usage patterns? What happens when users do things in a different order than you expected? How does your feature behave when the system is under load or when other features are being used simultaneously? Have you explored these scenarios, or have you just proven that it works under ideal conditions?"
    ]
    
    # Always use random comprehensive reality check - cover all failure modes
    message = random.choice(comprehensive_reality_checks)
    
    # Add actionable conclusion - all questions
    message += "\\n\\nDoes your feature genuinely work for real users, integrate properly, and not break existing functionality? Can you document that with evidence? Are there gaps or problems you need to fix? Do you need to research better approaches? Do you need to test more thoroughly? Are you being honest with yourself about the current state? Do you have rock-solid evidence everything works? Are you stuck and need help? Can you confidently say a real user would succeed with your feature right now?"
    
    log_hook_execution("block-premature-completion", "Stop", "soft_block", "Comprehensive reality check")
    
    # Use stderr + exit code 2 to show message to Claude and block stopping
    print(message, file=sys.stderr)
    sys.exit(2)

if __name__ == "__main__":
    main()