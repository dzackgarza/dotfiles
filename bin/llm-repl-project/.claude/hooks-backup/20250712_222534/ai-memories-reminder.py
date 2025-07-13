#!/usr/bin/env python3
"""
AI Memories Reminder Hook
Reminds about learning from past experiences
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
    # 1 in 8 chance to inject a memory question
    if random.randint(1, 8) == 1:
        questions = load_memory_questions()
        if questions:
            memory_question = random.choice(questions)
            print(json.dumps({
                "decision": "approve",
                "reason": f"💭 AI Memory: {memory_question}"
            }))
            return
    
    print(json.dumps({"decision": "approve"}))

if __name__ == "__main__":
    main()