#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "groq",
#     "python-dotenv",
# ]
# ///

import os
import sys
from dotenv import load_dotenv


def prompt_llm(prompt_text):
    """
    Base Groq LLM prompting method using fastest model.

    Args:
        prompt_text (str): The prompt to send to the model

    Returns:
        str: The model's response text, or None if error
    """
    load_dotenv()

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None

    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Fastest Groq model
            messages=[
                {"role": "user", "content": prompt_text}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Groq error: {e}", file=sys.stderr)
        return None


def main():
    """Main entry point for command line usage"""
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--completion', action='store_true', 
                       help='Generate a session completion message')
    parser.add_argument('prompt', nargs='?', 
                       help='Custom prompt text')
    
    args = parser.parse_args()
    
    if args.completion:
        # Generate session completion message
        prompt = """Generate a brief, professional completion message for a coding session. 
        Keep it under 20 words. Focus on what was accomplished. 
        Examples: "Successfully implemented user authentication", "Completed API refactoring", "Fixed critical bugs in payment system"."""
        
        result = prompt_llm(prompt)
        if result:
            print(result)
        else:
            print("Session completed successfully.")
    
    elif args.prompt:
        result = prompt_llm(args.prompt)
        if result:
            print(result)
        else:
            sys.exit(1)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()