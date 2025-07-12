#!/usr/bin/env python3
"""
Socratic UI Development Hook
Guides future Claude through self-questioning process for UI development
"""

import json
import sys
import random
from pathlib import Path

def load_memory_questions():
    """Load memory-guided questions from the mega-file"""
    questions_file = Path(__file__).parent / "memory-guided-questions.txt"
    
    if not questions_file.exists():
        return []
    
    try:
        with open(questions_file, 'r') as f:
            questions = [line.strip() for line in f if line.strip()]
        return questions
    except Exception:
        return []

def main():
    base_message = """I'm having trouble following what's happening here. 

Look at the latest screenshot. Really look at it. What do you see? Because from where I'm sitting, this doesn't look quite right.

Where's all this blank space coming from? What user input triggered this processing block? Why is this element narrow when others are full-width? What's missing that would make this make sense?

I think we might be patching things in without being thorough enough. But wait, if 'just test' is run at the end, won't that test still fail? 

The text area seems to be fighting with the main text area for focus... Why is the screenshot info getting mixed into the timeline?

If you removed all labels, would the flow be clear? What would confuse someone seeing this for the first time?

Don't make assumptions about what's working. The command palette opens fine, but the transient blocks continue processing when they shouldn't.

Can you help me understand what's actually broken here, not just what the code says should happen?"""

    # Inject memory question 1 in 5 times
    if random.randint(1, 5) == 1:
        questions = load_memory_questions()
        if questions:
            memory_question = random.choice(questions)
            base_message = f"{memory_question}\n\n{base_message}"

    print(json.dumps({
        "decision": "approve", 
        "message": base_message
    }))

if __name__ == "__main__":
    main()