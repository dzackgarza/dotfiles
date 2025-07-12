#!/usr/bin/env python3
"""
Simple YAML-based question loader for all hooks
"""

import yaml
import random
from pathlib import Path
from typing import List, Dict, Optional

def load_questions_yaml() -> Dict:
    """Load questions from YAML file"""
    questions_file = Path(__file__).parent / "memory-questions.yaml"
    
    try:
        with open(questions_file, 'r') as f:
            return yaml.safe_load(f)
    except Exception:
        # Fallback questions if YAML file doesn't exist
        return {
            'fallback': {
                'weight': 1.0,
                'questions': [
                    "Are you sure we're not just swatting flies?",
                    "Do we need to take a step back?",
                    "Are we solving the right problem here?"
                ]
            }
        }

def get_questions_by_category(category: str, count: int = 3) -> List[str]:
    """Get random questions from a specific category"""
    data = load_questions_yaml()
    
    if category not in data:
        # Return high-priority questions as fallback
        category = 'just_run_evidence'
    
    questions = data.get(category, {}).get('questions', [])
    if not questions:
        return []
    
    return random.sample(questions, min(count, len(questions)))

def get_questions_by_context(context: str, count: int = 3) -> List[str]:
    """Get questions relevant to a specific context"""
    data = load_questions_yaml()
    relevant_questions = []
    
    # Find all categories that match this context
    for category_name, category_data in data.items():
        contexts = category_data.get('contexts', [])
        if context in contexts:
            weight = category_data.get('weight', 1.0)
            questions = category_data.get('questions', [])
            
            # Add questions with weight multiplier
            repeat_count = max(1, int(weight * 10))
            for question in questions:
                relevant_questions.extend([question] * repeat_count)
    
    if not relevant_questions:
        # Fallback to high-priority categories
        return get_questions_by_category('just_run_evidence', count)
    
    # Remove duplicates and sample
    unique_questions = list(set(relevant_questions))
    return random.sample(unique_questions, min(count, len(unique_questions)))

def get_weighted_random_questions(count: int = 3) -> List[str]:
    """Get random questions weighted by category importance"""
    data = load_questions_yaml()
    weighted_questions = []
    
    for category_name, category_data in data.items():
        weight = category_data.get('weight', 1.0)
        questions = category_data.get('questions', [])
        
        # Add questions with weight multiplier
        repeat_count = max(1, int(weight * 10))
        for question in questions:
            weighted_questions.extend([question] * repeat_count)
    
    if not weighted_questions:
        return []
    
    # Remove duplicates and sample
    unique_questions = list(set(weighted_questions))
    return random.sample(unique_questions, min(count, len(unique_questions)))

def get_high_priority_questions(count: int = 3) -> List[str]:
    """Get questions from highest priority categories"""
    high_priority_categories = ['just_run_evidence', 'testing_methodology', 'research_first']
    
    all_questions = []
    for category in high_priority_categories:
        questions = get_questions_by_category(category, count)
        all_questions.extend(questions)
    
    # Remove duplicates and sample
    unique_questions = list(set(all_questions))
    return random.sample(unique_questions, min(count, len(unique_questions)))

# Legacy compatibility - for scripts that expect this function
def load_memory_questions() -> List[str]:
    """Legacy function that returns all questions as a flat list"""
    data = load_questions_yaml()
    all_questions = []
    
    for category_data in data.values():
        questions = category_data.get('questions', [])
        all_questions.extend(questions)
    
    return all_questions

if __name__ == "__main__":
    # Test the loader
    print("Testing question loader...")
    print("\n1. High priority questions:")
    for i, q in enumerate(get_high_priority_questions(3), 1):
        print(f"   {i}. {q}")
    
    print("\n2. Stop hook context questions:")
    for i, q in enumerate(get_questions_by_context('stop_hook', 3), 1):
        print(f"   {i}. {q}")
    
    print("\n3. Testing methodology questions:")
    for i, q in enumerate(get_questions_by_category('testing_methodology', 3), 1):
        print(f"   {i}. {q}")