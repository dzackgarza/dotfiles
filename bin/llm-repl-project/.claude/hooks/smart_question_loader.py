#!/usr/bin/env python3
"""
Smart Question Loader - Principled organization of memory-guided questions
"""

import json
import random
from pathlib import Path
from typing import List, Dict, Optional

class SmartQuestionLoader:
    def __init__(self):
        self.questions_file = Path(__file__).parent / "memory-questions-organized.json"
        self.questions_data = self._load_questions()
    
    def _load_questions(self) -> Dict:
        """Load the organized questions from JSON"""
        try:
            with open(self.questions_file, 'r') as f:
                return json.load(f)
        except Exception:
            # Fallback to basic questions if file doesn't exist
            return {
                "categories": {
                    "fallback": {
                        "weight": 1.0,
                        "questions": [
                            "Are you sure we're not just swatting flies?",
                            "Do we need to take a step back?",
                            "Are we solving the right problem here?"
                        ]
                    }
                }
            }
    
    def get_questions_for_context(self, context: str, count: int = 3) -> List[str]:
        """Get questions appropriate for the given context"""
        if not self.questions_data:
            return []
        
        # Get categories relevant to this context
        context_triggers = self.questions_data.get("context_triggers", {})
        relevant_categories = context_triggers.get(context, [])
        
        if not relevant_categories:
            # If no specific context, use weighted random selection
            relevant_categories = list(self.questions_data["categories"].keys())
        
        # Collect questions from relevant categories with weights
        weighted_questions = []
        for category_name in relevant_categories:
            category = self.questions_data["categories"].get(category_name, {})
            weight = category.get("weight", 1.0)
            questions = category.get("questions", [])
            
            # Add each question multiple times based on weight
            repeat_count = int(weight * 10)  # Convert weight to repeat count
            for question in questions:
                weighted_questions.extend([question] * repeat_count)
        
        if not weighted_questions:
            return []
        
        # Random selection without replacement
        selected = random.sample(weighted_questions, min(count, len(set(weighted_questions))))
        return list(set(selected))[:count]  # Remove duplicates and limit count
    
    def get_high_priority_questions(self, count: int = 3) -> List[str]:
        """Get highest priority questions regardless of context"""
        high_priority_categories = ["just_run_evidence", "testing_methodology", "research_first"]
        
        questions = []
        for category_name in high_priority_categories:
            category = self.questions_data["categories"].get(category_name, {})
            questions.extend(category.get("questions", []))
        
        if not questions:
            return []
        
        return random.sample(questions, min(count, len(questions)))
    
    def detect_context_from_content(self, content: str, tool_name: str = "") -> str:
        """Detect context from content and tool usage patterns"""
        content_lower = content.lower()
        
        # Context detection patterns
        if "test" in content_lower and ("fail" in content_lower or "pass" in content_lower):
            return "test_failure"
        
        if tool_name == "Edit" and content_lower:
            return "edit_operations"
        
        if any(word in content_lower for word in ["fixed", "completed", "done", "working"]):
            return "completion_attempts"
        
        if any(word in content_lower for word in ["widget", "component", "ui", "gui"]):
            return "widget_development"
        
        if any(word in content_lower for word in ["should", "must", "obviously", "clearly"]):
            return "overconfidence_detected"
        
        # Default context
        return "general"

# Convenience functions for hooks
def get_contextual_questions(context: str, count: int = 3) -> List[str]:
    """Get questions for a specific context"""
    loader = SmartQuestionLoader()
    return loader.get_questions_for_context(context, count)

def get_questions_from_content(content: str, tool_name: str = "", count: int = 3) -> List[str]:
    """Get questions based on content analysis"""
    loader = SmartQuestionLoader()
    context = loader.detect_context_from_content(content, tool_name)
    return loader.get_questions_for_context(context, count)

def get_priority_questions(count: int = 3) -> List[str]:
    """Get high-priority questions"""
    loader = SmartQuestionLoader()
    return loader.get_high_priority_questions(count)

if __name__ == "__main__":
    # Test the loader
    loader = SmartQuestionLoader()
    print("Testing context: stop_hook")
    questions = loader.get_questions_for_context("stop_hook", 3)
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q}")